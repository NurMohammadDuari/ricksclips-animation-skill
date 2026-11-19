// render-monitor.cpp — realtime render progress monitor (dark glass TUI)
// Watches a render's frame folder (one PNG per frame, mtime = draw time) and a log file.
// build: g++ -O2 -std=c++17 -o render-monitor render-monitor.cpp
// usage: ./render-monitor <frames-dir> [log-file]
// keys: p pause · q quit
#include <algorithm>
#include <atomic>
#include <chrono>
#include <csignal>
#include <cstdio>
#include <cstring>
#include <dirent.h>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <sstream>
#include <string>
#include <sys/ioctl.h>
#include <sys/stat.h>
#include <termios.h>
#include <unistd.h>
#include <thread>
#include <vector>

namespace fs = std::filesystem;
using clk = std::chrono::steady_clock;

static std::atomic<bool> g_stop{false};
static void on_sig(int) { g_stop = true; }

// ---------- terminal ----------
static termios g_orig{};
static void raw_mode() {
    tcgetattr(STDIN_FILENO, &g_orig);
    termios t = g_orig;
    t.c_lflag &= ~(ICANON | ECHO);
    t.c_cc[VMIN] = 0; t.c_cc[VTIME] = 0;
    tcsetattr(STDIN_FILENO, TCSANOW, &t);
}
static void restore_mode() { tcsetattr(STDIN_FILENO, TCSANOW, &g_orig); }
static int term_rows() { winsize w{}; ioctl(STDOUT_FILENO, TIOCGWINSZ, &w); return w.ws_row ? w.ws_row : 40; }
static int term_cols() { winsize w{}; ioctl(STDOUT_FILENO, TIOCGWINSZ, &w); return w.ws_col ? w.ws_col : 120; }

static std::string frame(int n, const std::string& s, int w) {
    if ((int)s.size() >= w) return s.substr(0, w);
    std::string pad = s; pad.append(w - s.size(), ' ');
    return "\x1b[38;5;" + std::to_string(n) + "m" + pad + "\x1b[0m";
}
static std::string bar(double frac, int w) {
    int f = (int)(frac * w + 0.5); f = std::max(0, std::min(w, f));
    std::string b(f, '='); if (f < w) b += '>';
    b.append(w - b.size() - (f < w ? 1 : 0) + (f < w ? 0 : 0), ' ');
    return b;
}

// ---------- proc ----------
struct ProcStat { long utime = 0, stime = 0, rss_kb = 0; double pcpu = 0; };
static ProcStat read_proc(const std::string& pid) {
    ProcStat ps;
    std::ifstream f("/proc/" + pid + "/stat");
    std::string data((std::istreambuf_iterator<char>(f)), {});
    // fields after the last ')' are space-separated: state ppid ... utime=14th overall => index 11 after comm
    auto rp = data.rfind(')');
    if (rp == std::string::npos) return ps;
    std::istringstream ss(data.substr(rp + 1));
    std::string tok; long ut = 0, st = 0; int idx = 0;
    while (ss >> tok) { if (idx == 11) ut = std::stol(tok); if (idx == 12) st = std::stol(tok); idx++; }
    std::ifstream sm("/proc/" + pid + "/statm");
    long total_pages = 0, rss_pages = 0; if (!(sm >> total_pages >> rss_pages)) rss_pages = 0;
    ps.utime = ut; ps.stime = st; ps.rss_kb = rss_pages * (sysconf(_SC_PAGESIZE) / 1024);
    static long pclk = sysconf(_SC_CLK_TCK);
    static auto last_t = clk::now(); static ProcStat last; static bool first = true;
    auto now = clk::now();
    double dts = std::chrono::duration<double>(now - last_t).count();
    if (dts > 0.05) {
        double ticks = (ps.utime + ps.stime) - (last.utime + last.stime);
        double cpu = (ticks / pclk) / dts * 100.0;
        ps.pcpu = first ? 0 : cpu;
        last = ps; last_t = now; first = false;
    } else ps.pcpu = last.pcpu;
    return ps;
}

// ---------- samples ----------
struct Sample { double t; long frames; };
struct FrameInfo { long n = 0; double last_mtime = 0; double first_mtime = 0; };

static FrameInfo scan_dir(const fs::path& dir) {
    FrameInfo fi;
    std::error_code ec;
    if (!fs::exists(dir, ec)) return fi;
    double first = 1e18, last = 0;
    for (auto it = fs::directory_iterator(dir, ec); it != fs::directory_iterator(); it.increment(ec)) {
        std::string nm = it->path().filename().string();
        if (nm.size() < 6 || nm.substr(0, 2) != "f_" || nm.substr(nm.size() - 4) != ".png") continue;
        fi.n++;
        auto mt = fs::last_write_time(it->path(), ec);
        if (ec) continue;
        auto sctp = std::chrono::time_point_cast<std::chrono::system_clock::duration>(mt - fs::file_time_type::clock::now() + std::chrono::system_clock::now());
        double ts = std::chrono::duration<double>(sctp.time_since_epoch()).count();
        first = std::min(first, ts); last = std::max(last, ts);
    }
    fi.first_mtime = (first == 1e18) ? 0 : first;
    fi.last_mtime = last;
    return fi;
}

static long count_lines(const std::string& path) {
    std::ifstream f(path);
    if (!f) return -1;
    return std::count(std::istreambuf_iterator<char>(f), std::istreambuf_iterator<char>(), '\n');
}

// latest log lines (tail)
static std::vector<std::string> tail_log(const std::string& path, int k) {
    std::vector<std::string> out;
    std::ifstream f((path));
    if (!f) return out;
    std::string ln;
    std::vector<std::string> ring(k);
    int n = 0;
    while (std::getline(f, ln)) { ring[n % k] = ln; n++; }
    for (int i = 0; i < std::min(n, k); i++) out.push_back(ring[(n - std::min(n, k) + i + k * 2) % k]);
    return out;
}

static std::string human_dur(double s) {
    if (s < 0 || s > 360000) return "--:--:--";
    long h = (long)(s / 3600), m = ((long)(s) % 3600) / 60, sec = (long)s % 60;
    char b[16]; snprintf(b, sizeof b, "%02ld:%02ld:%02ld", h, m, sec); return b;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cout << "usage: " << argv[0] << " <frames-dir> [log-file]\n";
        return 1;
    }
    fs::path dir = argv[1];
    std::string logfile = argc > 2 ? argv[2] : "";
    std::string pid = "";
    // find node render pid (heuristic: node process with render.mjs in cmdline)
    {
        std::error_code ec;
        for (auto& e : fs::directory_iterator("/proc", ec)) {
            std::string p = e.path().filename().string();
            if (p.size() < 2 || p[0] < '0' || p[0] > '9') continue;
            std::ifstream cf("/proc/" + p + "/cmdline");
            std::string cmd((std::istreambuf_iterator<char>(cf)), {});
            if (cmd.find("render.mjs") != std::string::npos && cmd.find("node") == 0) { pid = p; break; }
        }
    }

    std::signal(SIGINT, on_sig); std::signal(SIGTERM, on_sig);
    if (isatty(STDIN_FILENO)) raw_mode();
    std::cout << "\x1b[?25l"   // hide cursor
              << "\x1b[?1049h"; // alt screen

    // live preview: start render.mjs --serve in the render process's cwd (the episode dir)
    std::string serve_url;
    {
        std::error_code ec;
        if (!pid.empty()) {
            fs::path cwd = fs::read_symlink("/proc/" + pid + "/cwd", ec);
            if (!ec && fs::exists(cwd / "film.json", ec)) {
                fs::path kit = cwd.parent_path().parent_path() / "templates" / "threejs_film" / "render.mjs";
                if (!fs::exists(kit, ec)) kit = fs::path("/home/mint/Desktop/RicksClips/RicksClips_Skill_V1.1/templates/threejs_film/render.mjs");
                if (fs::exists(kit, ec)) {
                    int port = 8800 + (std::stol(pid) % 500);
                    char portstr[8]; snprintf(portstr, sizeof portstr, "%d", port);
                    std::string cmd = "setsid nohup node '" + kit.string() + "' '" + (cwd / "film.json").string() + "' --serve " + portstr + " > /tmp/render-serve.log 2>&1 < /dev/null &";
                    int r = system(cmd.c_str());
                    (void)r;
                    for (int w = 0; w < 25; w++) {
                        std::this_thread::sleep_for(std::chrono::milliseconds(150));
                        std::ifstream sf("/tmp/render-serve.log");
                        std::string ln;
                        while (std::getline(sf, ln)) {
                            if (ln.find("EADDRINUSE") != std::string::npos) break;
                            if (ln.find("http://127.0.0.1:") != std::string::npos) {
                                auto p1 = ln.find("http://");
                                auto p2 = ln.find(' ', p1);
                                serve_url = ln.substr(p1, p2 - p1);
                            }
                        }
                        if (!serve_url.empty()) break;
                    }
                }
            }
        }
    }

    std::vector<Sample> samples;
    std::vector<double> spark; // speed history
    FrameInfo fi = scan_dir(dir);
    long total = 0; bool total_known = false;
    std::string total_str = "?";
    long last_n = fi.n;
    auto t_prev = clk::now();
    double rate = 0; // frames/s
    auto t0 = clk::now();
    double elapsed = 0;
    std::string status = "RENDERING";
    bool paused = false;

    // detect total from film size if possible: frames are counted; total from log "f/NNNN"
    while (!g_stop) {
        // input
        char c = 0;
        if (read(STDIN_FILENO, &c, 1) == 1) {
            if (c == 'q') break;
            if (c == 'p') paused = !paused;
        }

        auto now = clk::now();
        double dt = std::chrono::duration<double>(now - t_prev).count();
        if (dt >= 0.35) {
            t_prev = now;
            fi = scan_dir(dir);
            if (!total_known && fi.n > 0) {
                // try to read total from log: "  123/3645" pattern
                if (!logfile.empty()) {
                    std::ifstream f((logfile));
                    std::string ln, best;
                    size_t best_sl = std::string::npos;
                    while (std::getline(f, ln)) {
                        if (ln.find("ms/frame") == std::string::npos) continue;
                        size_t sl = ln.find('/');
                        size_t sc = ln.find_first_of("0123456789");
                        if (sl != std::string::npos && sc != std::string::npos && sc < sl)
                            { best = ln; best_sl = sl; }
                    }
                    if (!best.empty() && best_sl != std::string::npos) {
                        size_t ds = best_sl + 1;
                        size_t de = best.find_first_not_of("0123456789", ds);
                        if (de == std::string::npos) de = best.size();
                        try { total = std::stol(best.substr(ds, de - ds)); } catch (...) { total = 0; }
                        if (total > 0) { total_known = true; total_str = std::to_string(total); }
                    }
                }
            }
            long dn = fi.n - last_n;
            if (dt > 0 && dn >= 0) rate = dn / dt;
            last_n = fi.n;
            elapsed = std::chrono::duration<double>(now - t0).count();
            spark.push_back(rate);
            if (spark.size() > 70) spark.erase(spark.begin());
        }

        // finished? (ffmpeg stage)
        bool mp4_done = false; double mp4_size = 0;
        {
            std::error_code ec;
            fs::path mp4 = dir.parent_path().parent_path() / "out" / "animatic.mp4";
            // dir is .../tmp/film_frames_PID ; episode out is 3 up from frames dir? fallback search:
            if (!fs::exists(mp4, ec)) mp4 = fs::path("out/animatic.mp4");
            if (fs::exists(mp4, ec)) {
                mp4_size = (double)fs::file_size(mp4, ec);
                auto mt = fs::last_write_time(mp4, ec);
                auto sctp = std::chrono::time_point_cast<std::chrono::system_clock::duration>(mt - fs::file_time_type::clock::now() + std::chrono::system_clock::now());
                double age = std::chrono::duration<double>(std::chrono::system_clock::now() - sctp).count();
                if (total_known && fi.n >= total && age < 5.0) mp4_done = true;
            }
        }
        if (total_known && fi.n >= total) status = mp4_done ? "DONE — MP4 READY" : "MUXING (ffmpeg)";
        else if (fi.n > 0 && fi.last_mtime > 0 && elapsed > 3 &&
                 std::chrono::duration<double>(std::chrono::system_clock::now() -
                     std::chrono::system_clock::time_point(
                         (std::chrono::system_clock::duration)(long)(fi.last_mtime * 1e9))).count() > 6.0)
            status = paused ? "PAUSED" : "STALLED?";
        else status = paused ? "PAUSED (p)" : "RENDERING";

        // proc stats
        ProcStat ps{};
        bool have_proc = !pid.empty();
        if (have_proc) ps = read_proc(pid);
        double mem_pct = 0; long mem_total_kb = 0, mem_avail_kb = 0;
        { std::ifstream mf("/proc/meminfo"); std::string k; long v;
          while (mf >> k >> v) { if (k == "MemTotal:") mem_total_kb = v; if (k == "MemAvailable:") mem_avail_kb = v; } }
        if (mem_total_kb) mem_pct = (1.0 - (double)mem_avail_kb / mem_total_kb) * 100.0;

        double frac = total_known ? (double)fi.n / total : 0;
        double avg_rate = (fi.n > 0 && elapsed > 5) ? fi.n / elapsed : 0;
        double eta = (total_known && fi.n < total && avg_rate > 0.01) ? (total - fi.n) / avg_rate : -1;

        // ---- draw ----
        int rows = term_rows(), cols = term_cols();
        std::ostringstream o;
        o << "\x1b[H";
        auto line = [&](const std::string& s) { o << "\x1b[2K" << s.substr(0, cols - 1) << "\n"; };

        // title
        {
            int left = std::min(cols - 1, 52);
            std::string t = " RICK'S RENDER MONITOR ";
            std::string top = "\x1b[38;5;220m╭" + std::string(left - 2, '-') + "╮\x1b[0m";
            o << "\x1b[2K" << top << "\n";
            std::string mid = "\x1b[38;5;220m│\x1b[0m\x1b[1m" + t + std::string(std::max(0, left - 3 - (int)t.size()), ' ') + "\x1b[38;5;220m│\x1b[0m";
            line(mid);
            o << "\x1b[2K\x1b[38;5;220m╰" + std::string(left - 2, '-') + "╯\x1b[0m\n";
        }

        // status line
        {
            int col = 224;
            std::string dot = "\x1b[38;5;82m●\x1b[0m ";
            if (status.find("DONE") != std::string::npos) dot = "\x1b[38;5;46m✔\x1b[0m ";
            else if (status.find("PAUSED") != std::string::npos) dot = "\x1b[38;5;220m⏸\x1b[0m ";
            else if (status.find("MUX") != std::string::npos) dot = "\x1b[38;5;213m⚡\x1b[0m ";
            o << "\x1b[2K" << dot << "\x1b[1m" << frame(col, status, 40) << "\x1b[0m";
            char b[64];
            if (have_proc) { snprintf(b, sizeof b, "  cpu\x1b[38;5;245m %4.0f%%\x1b[0m  rss\x1b[38;5;245m %.0f MB\x1b[0m", ps.pcpu, ps.rss_kb / 1024.0); o << b; }
            o << "\n";
        }

        // main progress
        {
            int bw = std::max(10, std::min(cols - 58, 60));
            char b[96];
            snprintf(b, sizeof b, "%ld/%s  %5.1f%%", fi.n, total_known ? total_str.c_str() : "?", frac * 100);
            o << "  \x1b[38;5;213m" << bar(frac, bw) << "\x1b[0m  \x1b[1m" << std::left << std::setw(18) << std::string(b) << "\x1b[0m  \x1b[38;5;82m" << std::fixed << std::setprecision(2) << rate << " f/s\x1b[0m  avg \x1b[38;5;245m" << std::fixed << std::setprecision(2) << avg_rate << " f/s\x1b[0m\n";
        }

        // info row
        {
            char b[256];
            snprintf(b, sizeof b, "  elapsed \x1b[1m%s\x1b[0m   eta \x1b[1m\x1b[38;5;214m%s\x1b[0m   dir \x1b[38;5;245m%s\x1b[0m",
                     human_dur(elapsed).c_str(), human_dur(eta).c_str(), dir.filename().string().c_str());
            line(std::string(b));
        }

        // per-place color legend (film stages)
        o << "  \x1b[38;5;245mstages:\x1b[0m ";
        struct LG { const char* n; int c; } lgs[] = {
            {"storyboard", 39}, {"frames", 213}, {"ffmpeg mux", 46}, {"mp4", 82}};
        for (auto& l : lgs) o << "\x1b[38;5;" << l.c << "m■ " << l.n << "\x1b[0m  ";
        o << "\n";

        // sparkline (rate history)
        {
            o << "  \x1b[38;5;245mspeed\x1b[0m ";
            const char* blocks[] = {"▁","▂","▃","▄","▅","▆","▇","█"};
            double mx = 0.001; for (double v : spark) mx = std::max(mx, v);
            for (double v : spark) {
                int bi = (int)(v / mx * 7.999);
                o << "\x1b[38;5;" << (bi > 5 ? 82 : bi > 3 ? 220 : 245) << "m" << blocks[bi];
            }
            o << "\x1b[0m\n";
        }

        // latest frames filmstrip (last 5 PNGs)
        {
            o << "  \x1b[38;5;245mlatest\x1b[0m ";
            std::vector<std::pair<long, std::string>> items; // n, name
            std::error_code ec;
            for (auto& e : fs::directory_iterator(dir, ec)) {
                std::string nm = e.path().filename().string();
                if (nm.size() < 6 || nm.substr(0, 2) != "f_") continue;
                items.push_back({std::stol(nm.substr(2)), nm});
            }
            std::sort(items.begin(), items.end(), [](auto& a, auto& b) { return a.first < b.first; });
            int k = std::min((int)items.size(), 5);
            for (int i = items.size() - k; i < (int)items.size(); i++)
                if (i >= 0) o << "\x1b[38;5;82m▣\x1b[0m " << frame(245, items[i].second, 9) << " ";
            if (k == 0) o << "(waiting for frames)";
            o << "\n";
        }

        // log tail
        if (!logfile.empty()) {
            auto tlines = tail_log(logfile, std::max(1, std::min(4, rows - 16)));
            for (auto& ln : tlines) {
                // strip ANSI-ish noise, truncate
                std::string s;
                for (char ch : ln) { if (ch == '\t') ch = ' '; s += ch; }
                line("  \x1b[38;5;245m│\x1b[0m " + s);
            }
        }

        // live preview hint
        if (!serve_url.empty()) {
            o << "  \x1b[38;5;82m▶\x1b[0m \x1b[1mlive preview\x1b[0m \x1b[38;5;245m(open in browser, plays while rendering)\x1b[0m\n";
            o << "  \x1b[4m\x1b[38;5;81m" << serve_url << "\x1b[0m\n";
        }

        o << "\x1b[2K\n";
        o << "  \x1b[38;5;245m[p] pause · [q] quit\x1b[0m\n";
        o << "\x1b[J"; // clear below
        std::cout << o.str() << std::flush;

        std::this_thread::sleep_for(std::chrono::milliseconds(120));
    }

    // restore
    std::cout << "\x1b[?25h\x1b[?1049l" << std::flush;
    if (isatty(STDIN_FILENO)) restore_mode();
    return 0;
}