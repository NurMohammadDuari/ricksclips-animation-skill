# Accessibility

## Our commitment

RicksClips is a terminal-first animation pipeline. We want the documentation,
the tools and the films it produces to be usable by as many people as possible.
Accessibility reports are treated as bugs.

## Supported environments

| Area | Supported |
|---|---|
| Operating systems | Linux (primary), macOS, Windows via WSL |
| Shells | bash, zsh; PowerShell for the install step only |
| Python | 3.11+ |
| Node | 20+ |
| Browser render | Playwright Chromium |
| Final look pass | Blender 4.x + NVIDIA GPU (optional) |
| Render monitor | Linux terminal; GTK3 GUI on Linux |
| Video output | 9:16, 1080×1920, 30 fps, H.264 MP4 |
| Documentation language | English and Bangla |

## Measures in this project

- Every gate in `tools/film_plan.py` prints a **name, a measured value, a target
  and a fix line**, so failures are readable as text and not only as pictures.
- The storyboard and contact sheets are HTML/PNG with frame numbers and
  timestamps, usable without watching the video.
- Captions are generated from the word timings and burned into the frame.
- Docs use headings, tables and fenced code blocks with language tags.
- `--frames` lets you inspect stills instead of scrubbing a video.
- Colour is never the only signal in the gate report (`PASS`/`WARN`/`FAIL` are
  written out).

## Known limitations

- **Terminal required.** Setup and rendering assume a command line. The only GUI
  is `tools/render-monitor/` (GTK3, Linux).
- **Films are visual.** There is no audio-description track and no SDH caption
  track. Burned-in captions are short phrases, not full subtitles.
- **The 42 gates are visual/geometric.** They do not test screen-reader output,
  caption accuracy or audio accessibility.
- **The Blender look pass needs an NVIDIA GPU.** There is no CPU-only path for
  the final 1080p look.
- **Fast cuts and camera moves.** The style uses quick cuts and shake. Creators
  must add a photosensitivity warning where needed.
- **Mixed languages.** Bangla and English appear in the same docs; there is no
  full translation of every page.
- **Large repository.** A full clone is ~1 GB because example renders are
  included; use `git clone --depth 1` on slow connections.

## Reporting a barrier

Open an issue with the **Accessibility** template:

<https://github.com/NurMohammadDuari/ricksclips-animation-skill/issues/new/choose>

Include what you were trying to do, your assistive technology and version, the
file or step that failed, and what would have worked better. We aim to respond
within **7 days**. For anything private, use the channel in
[SECURITY.md](SECURITY.md).
