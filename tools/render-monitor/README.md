# render-monitor

Two small progress monitors for long renders. They watch a frame folder (one
PNG per frame, file mtime = draw time) and an optional log file.

| file | what | deps |
|---|---|---|
| `render-monitor.cpp` | dark-glass terminal UI | C++17, POSIX terminal |
| `render-monitor-gui.cpp` | GTK3 window with live preview and thumbnails | C++17, GTK3 |

## Build

```bash
# terminal monitor
g++ -O2 -std=c++17 -o render-monitor render-monitor.cpp

# GTK3 GUI (Linux)
g++ -O2 -std=c++17 -o render-monitor-gui render-monitor-gui.cpp \
    $(pkg-config --cflags --libs gtk+-3.0)
```

The compiled binaries are **not** committed — build them locally.

## Use

```bash
./render-monitor <frames-dir> [log-file]
./render-monitor-gui <frames-dir> [log-file]
```

Example, while `render.mjs` writes frames:

```bash
./render-monitor ../../RicksClips_Skill_V1.1/episodes/law11/film_frames_1080
```

Keys in the terminal monitor: `p` pause, `q` quit.
