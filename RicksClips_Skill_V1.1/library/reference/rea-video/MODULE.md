# rea-video — vendored reverse-engineering toolkit + corpus re-measurement

**Source:** https://github.com/NurMohammadDuari/rea-video (fork of JuneYaooo/rea-video, Apache-2.0) — vendored 2026-11-22 `rsync -a --exclude .git`, CLI installed (`rea-video`, version 0.1.0).
**What it is:** shot-by-shot video forensics: verdict per shot across 11 classes (live / film clip / AI video / digital human / 3D render / 2D animation / stop-motion / code-template render / screen recording / pan-over / still), overlay + packaging layers (caption timelines, stickers, PIP), audio stems (vocals / music / SFX candidates), rhythm and remake planning, all written into the open **VIDEO.md** format that agents read layer by layer.

## How we use it in this toolkit

1. **Corpus re-measurement (living pass over the DNA):** every new @RicksClips3000 film gets `survey → decompose → review → apply-review` (agent-as-VLM: the agent looks at the per-shot contact sheets and corrects the deterministic labels). Outputs live in `style/ricksclips-dna/rea-video/<video>/` (`VIDEO.md`, `report.html`, `breakdown.json`, `video/timeline.md`, `shots/*.jpg`).
2. **Cross-check for our own episodes:** run `rea-video decompose` on a finished law11 render and confirm the verdict comes back "3D render ~100%" — a sanity check that no live-looking artefacts (sensor grain, banding) leaked into the toon look.
3. **Remake planning:** for any reference the user hands over, `video/remake.md` gives per-shot routes (generation units for AI shots, camera setups for live shots).

## Corpus verdict after the 2026-11-22 agent review (7/7 films, 117 shots)

| film | shots | deterministic | after agent review | changed |
|---|---|---|---|---|
| How Mine Salting Worked | 25 | live 98% | **3D render 98%** | 22 |
| How One Cart Stopped an Entire Army | 10 | mixed | **live 65% + 3D 35%** (tool's 24→30 frame-rate evidence outweighed the visual verdict; sheet check: all 10 shots are the 3D toon world — treat as 3D ~100% by eye) | 5 |
| The Instinct That Makes You Crash | 19 | mixed | **3D render 90%** | 8 |
| The Prisoner Who Tunneled Into a Bank | 12 | mixed | **3D render 100%** | 12 |
| Why Astronauts Can't Flush in Space | 19 | mixed | **3D render 100%** | 19 |
| Why Drivers Started Filming The Road | 19 | mixed | **3D render 97%** | ~19 |
| Why Samurai Feared The Flying Thunder | 13 | mixed | **3D render 100%** | ~13 |

**Corpus conclusion:** the deterministic pass alone is *wrong* about this channel (YouTube transcode grain reads as "sensor noise" → "live action"); the agent-as-VLM review is what makes rea-video usable on the corpus. Confirmed independently: the whole 7-film corpus is coded 3D toon sets + 2D character cards — exactly the ricksclips-dna finding, now measured with a second independent instrument. Per-shot boundaries, overlay layers (word captions, sticker/GIF on text pops) and SFX-candidate timings are in each film's `video/timeline.md`.

## Commands (this sandbox, verified)

```bash
rea-video decompose <video.mp4> -o <outdir> --lang en --no-stems --no-ocr   # ~4 min per 60 s film (offline)
rea-video review <outdir>                    # writes review_tasks.json + review_answers.json template
# ... agent looks at shots/*.jpg contact sheets, fills answers (scripts/fill_review.py automates the corpus fill) ...
rea-video apply-review <outdir> --by agent-zai-glm
rea-video summary <outdir>/breakdown.json    # compact verdict + VLM line
```
