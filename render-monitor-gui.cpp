// render-monitor-gui.cpp — GTK3 GUI render monitor with live animation preview
// build: g++ -O2 -std=c++17 -o render-monitor-gui render-monitor-gui.cpp $(pkg-config --cflags --libs gtk+-3.0)
// usage: ./render-monitor-gui <frames-dir> [log-file]
#include <gtk/gtk.h>
#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdio>
#include <cstring>
#include <dirent.h>
#include <filesystem>
#include <fstream>
#include <sstream>
#include <string>
#include <thread>
#include <vector>

namespace fs = std::filesystem;
using clk = std::chrono::steady_clock;

struct State {
    fs::path frames_dir;
    std::string logfile;
    std::string pid;
    // progress
    long n = 0, total = 0;
    bool total_known = false;
    double rate = 0, avg_rate = 0, eta = -1, frac = 0, elapsed = 0;
    std::string status = "RENDERING";
    double pcpu = 0, rss_mb = 0;
    std::vector<double> spark;
    std::vector<std::string> log_tail;
    std::vector<std::pair<long, std::string>> last_frames; // (num, name)
    std::string serve_url;
    GtkWidget *bar = nullptr, *lbl_stats = nullptr, *lbl_status = nullptr;
    GtkWidget *lbl_elapsed = nullptr, *lbl_eta = nullptr, *lbl_cpu = nullptr;
    GtkWidget *spark_area = nullptr, *lbl_log = nullptr, *lbl_url = nullptr;
    GtkWidget *btn_preview = nullptr, *lbl_frames = nullptr;
    GtkWidget *thumbs[6] = {nullptr};
    GtkWidget *win = nullptr;
    long last_n = 0;
    std::chrono::steady_clock::time_point t_prev = clk::now();
    std::chrono::steady_clock::time_point t0 = clk::now();
};

static long count_files(const fs::path& dir, std::vector<std::pair<long, std::string>>* collect = nullptr, size_t keep_last = 0) {
    long n = 0;
    std::error_code ec;
    if (!fs::exists(dir, ec)) return 0;
    std::vector<std::pair<long, std::string>> all;
    for (auto& e : fs::directory_iterator(dir, ec)) {
        std::string nm = e.path().filename().string();
        if (nm.size() < 6 || nm.compare(0, 2, "f_") != 0) continue;
        try { all.push_back({std::stol(nm.substr(2)), nm}); } catch (...) {}
        n++;
    }
    if (collect) {
        std::sort(all.begin(), all.end(), [](auto& a, auto& b) { return a.first < b.first; });
        size_t from = (all.size() > keep_last) ? all.size() - keep_last : 0;
        collect->assign(all.begin() + from, all.end());
    }
    return n;
}

static std::string human(double s) {
    if (s < 0 || s > 360000) return "--:--:--";
    long h = (long)(s / 3600), m = ((long)s % 3600) / 60, sec = (long)s % 60;
    char b[16]; snprintf(b, sizeof b, "%02ld:%02ld:%02ld", h, m, sec); return b;
}

static gboolean tick(gpointer data) {
    State* st = (State*)data;
    auto now = clk::now();
    double dt = std::chrono::duration<double>(now - st->t_prev).count();
    if (dt < 0.3) return TRUE;
    st->t_prev = now;
    st->elapsed = std::chrono::duration<double>(now - st->t0).count();

    long new_n = count_files(st->frames_dir, &st->last_frames, 6);
    long dn = new_n - st->last_n;
    st->rate = (dt > 0 && dn >= 0) ? dn / dt : 0;
    st->last_n = st->n = new_n;
    st->spark.push_back(st->rate);
    if (st->spark.size() > 60) st->spark.erase(st->spark.begin());
    st->avg_rate = (st->n > 0 && st->elapsed > 5) ? st->n / st->elapsed : 0;
    st->eta = (st->total_known && st->n < st->total && st->avg_rate > 0.01) ? (st->total - st->n) / st->avg_rate : -1;
    st->frac = st->total_known ? (double)st->n / st->total : 0;

    // parse total from log (line with "NNN/3645  ms/frame")
    if (!st->total_known && !st->logfile.empty()) {
        std::ifstream f((st->logfile));
        std::string ln, best; size_t best_sl = std::string::npos;
        while (std::getline(f, ln)) {
            if (ln.find("ms/frame") == std::string::npos) continue;
            size_t sl = ln.find('/'), sc = ln.find_first_of("0123456789");
            if (sl != std::string::npos && sc != std::string::npos && sc < sl) { best = ln; best_sl = sl; }
        }
        if (!best.empty() && best_sl != std::string::npos) {
            size_t ds = best_sl + 1, de = best.find_first_not_of("0123456789", ds);
            if (de == std::string::npos) de = best.size();
            try { st->total = std::stol(best.substr(ds, de - ds)); } catch (...) {}
            if (st->total > 0) st->total_known = true;
        }
    }

    // status: done? muxing?
    bool mp4_done = false;
    {
        std::error_code ec;
        for (fs::path p = st->frames_dir; p != "/" && p != p.parent_path(); p = p.parent_path()) {
            fs::path cand = p / "out" / "animatic.mp4";
            if (fs::exists(cand, ec)) {
                auto mt = fs::last_write_time(cand, ec);
                auto sctp = std::chrono::time_point_cast<std::chrono::system_clock::duration>(
                    mt - fs::file_time_type::clock::now() + std::chrono::system_clock::now());
                double age = std::chrono::duration<double>(std::chrono::system_clock::now() - sctp).count();
                if (st->total_known && st->n >= st->total && age < 6.0) mp4_done = true;
                break;
            }
        }
    }
    if (st->total_known && st->n >= st->total) st->status = mp4_done ? "DONE — MP4 READY" : "MUXING (ffmpeg)";
    else if (st->elapsed > 3 && st->rate <= 0.01 && st->n > 0) st->status = "STALLED?";
    else st->status = "RENDERING";

    // proc stats
    if (!st->pid.empty()) {
        std::ifstream f("/proc/" + st->pid + "/stat");
        std::string data((std::istreambuf_iterator<char>(f)), {});
        auto rp = data.rfind(')');
        if (rp != std::string::npos) {
            std::istringstream ss(data.substr(rp + 1));
            std::string tok; long ut = 0, stt = 0; int idx = 0;
            while (ss >> tok) { if (idx == 11) ut = std::stol(tok); if (idx == 12) stt = std::stol(tok); idx++; }
            static long pclk = sysconf(_SC_CLK_TCK);
            static auto lt = clk::now(); static long put = 0, pst = 0; static bool first = true;
            if (dt > 0.05) {
                if (!first) st->pcpu = ((ut + stt - put - pst) / (double)pclk) / dt * 100.0;
                first = false; put = ut; pst = stt; lt = now;
            }
        }
        std::ifstream sm("/proc/" + st->pid + "/statm");
        long tp = 0, rp2 = 0;
        if (sm >> tp >> rp2) st->rss_mb = rp2 * (sysconf(_SC_PAGESIZE) / 1024) / 1024.0;
    }

    // log tail
    if (!st->logfile.empty()) {
        std::ifstream f((st->logfile));
        std::string ln;
        std::vector<std::string> ring(4);
        int cnt = 0;
        while (std::getline(f, ln)) { ring[cnt % 4] = ln; cnt++; }
        st->log_tail.clear();
        int k = std::min(cnt, 4);
        for (int i = 0; i < k; i++) st->log_tail.push_back(ring[(cnt - k + i + 8) % 4]);
    }

    // ---- update UI ----
    char b[512];
    if (st->bar) {
        gtk_progress_bar_set_fraction(GTK_PROGRESS_BAR(st->bar), st->frac);
        snprintf(b, sizeof b, "%ld / %s   %.1f%%", st->n, st->total_known ? std::to_string(st->total).c_str() : "?", st->frac * 100);
        gtk_progress_bar_set_text(GTK_PROGRESS_BAR(st->bar), b);
    }
    if (st->lbl_status) {
        const char* col = "#4ade80";
        if (st->status.find("DONE") != std::string::npos) col = "#22c55e";
        else if (st->status.find("MUX") != std::string::npos) col = "#facc15";
        else if (st->status.find("STALL") != std::string::npos) col = "#f87171";
        snprintf(b, sizeof b, "<span foreground='%s' size='14000'><b>%s</b></span>", col, st->status.c_str());
        gtk_label_set_markup(GTK_LABEL(st->lbl_status), b);
    }
    if (st->lbl_stats) {
        snprintf(b, sizeof b, "<b>speed</b> %.2f f/s   <b>avg</b> %.2f f/s   <b>cpu</b> %.0f%%   <b>rss</b> %.0f MB",
                 st->rate, st->avg_rate, st->pcpu, st->rss_mb);
        gtk_label_set_markup(GTK_LABEL(st->lbl_stats), b);
    }
    if (st->lbl_elapsed) { snprintf(b, sizeof b, "elapsed <b>%s</b>", human(st->elapsed).c_str()); gtk_label_set_markup(GTK_LABEL(st->lbl_elapsed), b); }
    if (st->lbl_eta) { snprintf(b, sizeof b, "eta <b><span foreground='#fbbf24'>%s</span></b>", human(st->eta).c_str()); gtk_label_set_markup(GTK_LABEL(st->lbl_eta), b); }

    if (st->spark_area) gtk_widget_queue_draw(st->spark_area);
    if (st->lbl_log) {
        std::string s = "<span font='Monospace 8' foreground='#9ca3af'>";
        for (auto& l : st->log_tail) {
            std::string e;
            for (char c : l) { if (c == '&') e += "&amp;"; else if (c == '<') e += "&lt;"; else if (c == '>') e += "&gt;"; else e += c; }
            s += e + "\n";
        }
        s += "</span>";
        gtk_label_set_markup(GTK_LABEL(st->lbl_log), s.c_str());
        gtk_label_set_yalign(GTK_LABEL(st->lbl_log), 0);
    }
    if (st->lbl_frames && !st->last_frames.empty()) {
        snprintf(b, sizeof b, "latest: %s", st->last_frames.back().second.c_str());
        gtk_label_set_text(GTK_LABEL(st->lbl_frames), b);
        // update thumbnails from disk
        for (int i = 0; i < 6 && i < (int)st->last_frames.size(); i++) {
            auto& pr = st->last_frames[st->last_frames.size() - 1 - i];
            if (!st->thumbs[i]) continue;
            char path[1024];
            snprintf(path, sizeof path, "%s/%s", st->frames_dir.c_str(), pr.second.c_str());
            GError* err = nullptr;
            GdkPixbuf* pb = gdk_pixbuf_new_from_file_at_scale(path, 108, 192, TRUE, &err);
            if (pb) {
                gtk_image_set_from_pixbuf(GTK_IMAGE(st->thumbs[i]), pb);
                g_object_unref(pb);
            }
            if (err) g_error_free(err);
        }
    }
    if (st->lbl_url && !st->serve_url.empty()) {
        snprintf(b, sizeof b, "<span foreground='#60a5fa'><a href='%s'>%s</a></span>", st->serve_url.c_str(), st->serve_url.c_str());
        gtk_label_set_markup(GTK_LABEL(st->lbl_url), b);
    } else if (st->lbl_url) {
        gtk_label_set_markup(GTK_LABEL(st->lbl_url), "<span foreground='#9ca3af'>starting player…</span>");
    }
    return TRUE;
}

static int find_render_pid() {
    std::error_code ec;
    for (auto& e : fs::directory_iterator("/proc", ec)) {
        std::string p = e.path().filename().string();
        if (p.size() < 2 || p[0] < '0' || p[0] > '9') continue;
        std::ifstream cf("/proc/" + p + "/cmdline");
        std::string cmd((std::istreambuf_iterator<char>(cf)), {});
        if (cmd.find("render.mjs") != std::string::npos && cmd.compare(0, 4, "node") == 0) return std::stol(p);
    }
    return -1;
}

static void start_serve(State* st) {
    if (!st->serve_url.empty()) return;
    char pidbuf[16];
    snprintf(pidbuf, sizeof pidbuf, "%ld", st->pid.empty() ? 0 : std::stol(st->pid));
    std::error_code ec;
    fs::path cwd = st->pid.empty() ? fs::path() : fs::read_symlink("/proc/" + st->pid + "/cwd", ec);
    if (!ec && fs::exists(cwd / "film.json", ec)) {
        fs::path kit = cwd.parent_path().parent_path() / "templates" / "threejs_film" / "render.mjs";
        if (!fs::exists(kit, ec)) kit = fs::path("/home/mint/Desktop/RicksClips/RicksClips_Skill_V1.1/templates/threejs_film/render.mjs");
        if (fs::exists(kit, ec)) {
            int port = 8800 + (std::stol(pidbuf) % 500);
            char cmd[2048];
            snprintf(cmd, sizeof cmd, "setsid nohup node '%s' '%s' --serve %d > /tmp/render-serve.log 2>&1 < /dev/null &",
                     kit.c_str(), (cwd / "film.json").c_str(), port);
            system(cmd);
            // read URL
            for (int w = 0; w < 20 && st->serve_url.empty(); w++) {
                std::this_thread::sleep_for(std::chrono::milliseconds(150));
                std::ifstream sf("/tmp/render-serve.log");
                std::string ln;
                while (std::getline(sf, ln)) {
                    if (ln.find("EADDRINUSE") != std::string::npos) break;
                    if (ln.find("http://127.0.0.1:") != std::string::npos) {
                        auto p1 = ln.find("http://");
                        auto p2 = ln.find(' ', p1);
                        st->serve_url = ln.substr(p1, p2 - p1);
                    }
                }
            }
            if (!st->serve_url.empty()) {
                char cmd2[2048];
                snprintf(cmd2, sizeof cmd2, "xdg-open '%s' >/dev/null 2>&1 &", st->serve_url.c_str());
                system(cmd2);
            }
        }
    }
}

static void on_preview_clicked(GtkButton* b, gpointer data) {
    (void)b;
    State* st = (State*)data;
    start_serve(st);
}

// sparkline draw
static gboolean draw_spark(GtkDrawingArea* area, cairo_t* cr, gpointer data) {
    State* st = (State*)data;
    int w = gtk_widget_get_allocated_width(GTK_WIDGET(area));
    int h = gtk_widget_get_allocated_height(GTK_WIDGET(area));
    cairo_set_source_rgb(cr, 0.11, 0.12, 0.14);
    cairo_paint(cr);
    if (st->spark.empty()) return FALSE;
    double mx = 0.01;
    for (double v : st->spark) mx = std::max(mx, v);
    int n = st->spark.size();
    double bw = (double)w / 60;
    for (int i = 0; i < n; i++) {
        double bh = (st->spark[i] / mx) * (h - 6);
        double x = w - (n - i) * bw;
        int col = st->spark[i] > mx * 0.66 ? 0 : st->spark[i] > mx * 0.33 ? 1 : 2;
        const char* cols[] = {"#4ade80", "#facc15", "#6b7280"};
        cairo_set_source_rgba(cr, 0, 0, 0, 0);
        // parse hex
        unsigned r, g, b;
        sscanf(cols[col] + 1, "%02x%02x%02x", &r, &g, &b);
        cairo_set_source_rgb(cr, r / 255.0, g / 255.0, b / 255.0);
        cairo_rectangle(cr, x, h - bh, std::max(1.0, bw - 2), bh);
        cairo_fill(cr);
    }
    return FALSE;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        fprintf(stderr, "usage: %s <frames-dir> [log-file]\n", argv[0]);
        return 1;
    }
    State st;
    st.frames_dir = argv[1];
    if (argc > 2) st.logfile = argv[2];
    int pid = find_render_pid();
    if (pid > 0) st.pid = std::to_string(pid);

    gtk_init(&argc, &argv);

    // dark theme via CSS
    GtkCssProvider* css = gtk_css_provider_new();
    gtk_css_provider_load_from_data(css,
        "window { background-color: #0f1115; }"
        ".card { background-color: #1a1d24; border-radius: 12px; padding: 14px; }"
        ".title { color: #e5e7eb; font-size: 16px; font-weight: bold; }"
        ".sub { color: #9ca3af; font-size: 11px; }"
        "progressbar { min-height: 22px; border-radius: 11px; }"
        "progressbar trough { background-color: #262a35; border-radius: 11px; }"
        "progressbar progress { background-color: #3b82f6; border-radius: 11px; }"
        "button { background: #2563eb; color: white; border-radius: 8px; padding: 8px 18px; }"
        "button:hover { background: #1d4ed8; }",
        -1, nullptr);
    gtk_style_context_add_provider_for_screen(gdk_screen_get_default(), GTK_STYLE_PROVIDER(css), GTK_STYLE_PROVIDER_PRIORITY_USER);

    st.win = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    gtk_window_set_title(GTK_WINDOW(st.win), "RicksClips — Render Monitor");
    gtk_window_set_default_size(GTK_WINDOW(st.win), 920, 620);
    gtk_window_set_position(GTK_WINDOW(st.win), GTK_WIN_POS_CENTER);
    g_signal_connect(st.win, "destroy", G_CALLBACK(gtk_main_quit), nullptr);

    GtkWidget* outer = gtk_box_new(GTK_ORIENTATION_VERTICAL, 12);
    gtk_container_set_border_width(GTK_CONTAINER(outer), 16);
    gtk_container_add(GTK_CONTAINER(st.win), outer);

    // ---- header card ----
    GtkWidget* hdr = gtk_box_new(GTK_ORIENTATION_VERTICAL, 6);
    gtk_style_context_add_class(gtk_widget_get_style_context(GTK_WIDGET(hdr)), "card");
    GtkWidget* t = gtk_label_new("  RICK'S RENDER MONITOR");
    gtk_style_context_add_class(gtk_widget_get_style_context(GTK_WIDGET(t)), "title");
    gtk_label_set_xalign(GTK_LABEL(t), 0);
    gtk_box_pack_start(GTK_BOX(hdr), t, FALSE, FALSE, 0);
    st.lbl_status = gtk_label_new("—");
    gtk_label_set_xalign(GTK_LABEL(st.lbl_status), 0);
    gtk_box_pack_start(GTK_BOX(hdr), st.lbl_status, FALSE, FALSE, 0);
    gtk_box_pack_start(GTK_BOX(outer), hdr, FALSE, FALSE, 0);

    // ---- progress card ----
    GtkWidget* pc = gtk_box_new(GTK_ORIENTATION_VERTICAL, 8);
    gtk_style_context_add_class(gtk_widget_get_style_context(GTK_WIDGET(pc)), "card");
    st.bar = gtk_progress_bar_new();
    gtk_box_pack_start(GTK_BOX(pc), st.bar, FALSE, FALSE, 0);
    GtkWidget* row = gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 16);
    st.lbl_stats = gtk_label_new("—");
    gtk_label_set_xalign(GTK_LABEL(st.lbl_stats), 0);
    st.lbl_elapsed = gtk_label_new("—");
    st.lbl_eta = gtk_label_new("—");
    gtk_box_pack_start(GTK_BOX(row), st.lbl_stats, TRUE, TRUE, 0);
    gtk_box_pack_start(GTK_BOX(row), st.lbl_elapsed, FALSE, FALSE, 0);
    gtk_box_pack_start(GTK_BOX(row), st.lbl_eta, FALSE, FALSE, 0);
    gtk_box_pack_start(GTK_BOX(pc), row, FALSE, FALSE, 0);
    st.spark_area = gtk_drawing_area_new();
    gtk_widget_set_size_request(st.spark_area, -1, 64);
    g_signal_connect(st.spark_area, "draw", G_CALLBACK(draw_spark), &st);
    gtk_box_pack_start(GTK_BOX(pc), st.spark_area, TRUE, TRUE, 0);
    gtk_box_pack_start(GTK_BOX(outer), pc, TRUE, TRUE, 0);

    // ---- preview card ----
    GtkWidget* pv = gtk_box_new(GTK_ORIENTATION_VERTICAL, 8);
    gtk_style_context_add_class(gtk_widget_get_style_context(GTK_WIDGET(pv)), "card");
    GtkWidget* pt = gtk_label_new("  LIVE ANIMATION PLAYER");
    gtk_style_context_add_class(gtk_widget_get_style_context(GTK_WIDGET(pt)), "title");
    gtk_label_set_xalign(GTK_LABEL(pt), 0);
    gtk_box_pack_start(GTK_BOX(pv), pt, FALSE, FALSE, 0);
    st.lbl_url = gtk_label_new("<span foreground='#9ca3af'>starting player…</span>");
    gtk_label_set_xalign(GTK_LABEL(st.lbl_url), 0);
    gtk_box_pack_start(GTK_BOX(pv), st.lbl_url, FALSE, FALSE, 0);
    st.btn_preview = gtk_button_new_with_label("▶  Open live player in browser   (plays the animation while it renders — space = pause, arrows = step, 🔊 voice on)");
    g_signal_connect(st.btn_preview, "clicked", G_CALLBACK(on_preview_clicked), &st);
    gtk_box_pack_start(GTK_BOX(pv), st.btn_preview, FALSE, FALSE, 0);
    GtkWidget* hint = gtk_label_new("<span foreground='#6b7280' size='9000'>The browser page plays every frame that finishes rendering, with the Bangla voice track. Reopen anytime — it keeps playing as more frames arrive.</span>");
    gtk_label_set_xalign(GTK_LABEL(hint), 0);
    gtk_box_pack_start(GTK_BOX(pv), hint, FALSE, FALSE, 0);
    // thumbnails strip
    GtkWidget* th = gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 6);
    for (int i = 0; i < 6; i++) {
        st.thumbs[i] = gtk_image_new();
        gtk_widget_set_size_request(st.thumbs[i], 108, 192);
        gtk_box_pack_end(GTK_BOX(th), st.thumbs[i], FALSE, FALSE, 0);
    }
    gtk_box_pack_start(GTK_BOX(pv), th, FALSE, FALSE, 0);
    st.lbl_frames = gtk_label_new("latest: —");
    gtk_label_set_xalign(GTK_LABEL(st.lbl_frames), 0);
    gtk_style_context_add_class(gtk_widget_get_style_context(GTK_WIDGET(st.lbl_frames)), "sub");
    gtk_box_pack_start(GTK_BOX(pv), st.lbl_frames, FALSE, FALSE, 0);
    gtk_box_pack_start(GTK_BOX(outer), pv, FALSE, FALSE, 0);

    // ---- log card ----
    GtkWidget* lc = gtk_box_new(GTK_ORIENTATION_VERTICAL, 4);
    gtk_style_context_add_class(gtk_widget_get_style_context(GTK_WIDGET(lc)), "card");
    GtkWidget* lt = gtk_label_new("render log");
    gtk_style_context_add_class(gtk_widget_get_style_context(GTK_WIDGET(lt)), "sub");
    gtk_label_set_xalign(GTK_LABEL(lt), 0);
    gtk_box_pack_start(GTK_BOX(lc), lt, FALSE, FALSE, 0);
    st.lbl_log = gtk_label_new("");
    gtk_label_set_xalign(GTK_LABEL(st.lbl_log), 0);
    gtk_box_pack_start(GTK_BOX(lc), st.lbl_log, TRUE, TRUE, 0);
    gtk_box_pack_start(GTK_BOX(outer), lc, TRUE, TRUE, 0);

    gtk_widget_show_all(st.win);
    g_timeout_add(400, tick, &st);
    // auto-start preview
    g_idle_add((GSourceFunc)([](gpointer d) -> gboolean { start_serve((State*)d); return FALSE; }), &st);
    gtk_main();
    return 0;
}