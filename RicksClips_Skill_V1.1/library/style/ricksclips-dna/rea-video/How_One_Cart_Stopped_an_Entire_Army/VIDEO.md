---
videomd: 1
name: how-one-cart-stopped-an-entire-army
description: 'hook: the strange act on screen in the first seconds; establish the place and the machine while the hero acts; the diegetic sign/alarm flips the mood Made with (inferred): live action 65%, 3D render 35%'
source:
  file: How_One_Cart_Stopped_an_Entire_Army.mp4
  sha256: 4b039db917ff99bed41149272f90a9eb75b53d1db0cdfb8ee5308861d22c5339
  duration: 66.833
  size: 720x1280
  fps: 30.0
  aspect: '9:16'
shots: 10
lang: en
made_mix:
  live_action: 0.6464
  cg_3d: 0.3536
confidence: 0.677
readers:
- tools
- agent
open_questions: 6
generator:
  name: rea-video
  version: 0.1.0
---

# How_One_Cart_Stopped_an_Entire_Army.mp4

**Verdict** (inferred): Mixed production: live action 65% + 3D render 35%; real material used: live footage (43.2s); audio: voice + 19 possible sound effects (unconfirmed signal candidates)
**Narrative**: #01 grab attention → #02-05 establish the pl… → #06-07 the diegetic sig… → #08-09 the literal payo… → #10 closing line lan…
**Made with** (inferred, by duration): live action 65%, 3D render 35%
**Remake**: 5 3D render shots → 4 generation units, 4 MiniMax H3 / H3 Max calls; live action 5 shots → 2 scenes, 4 camera setups
**Real material to collect**: 5 shots (65% of the duration), list in `video/remake.md`

## Next steps

- Remake: Capsule Cinema does the generation, assembly and checks. `rea-video remake <this dir>` hands over to it, does what can be done automatically and keeps the original elsewhere; `remake/status.md` says per shot what is left. Add incoming clips to `remake/mine.json` and run it again
- AI shots: prompts are in the generation units of `video/remake.md`; for automatic generation use Capsule Cinema: `scripts/remake_reference.py prepare <this dir>`, then `run <jobs.json> --dry-run` (paid: ask the user first)

## Open questions

- Shot #1 (0.0–4.8s): Tools say live action, the image review says 3D render; on the AI / live-action axis the fusion follows the tools (eval-calibrated): check t…
- Shot #2 (4.8–36.9s): Tools say live action, the image review says 3D render; on the AI / live-action axis the fusion follows the tools (eval-calibrated): check …
- Shot #4 (39.1–40.4s): Tools say live action, the image review says 3D render; on the AI / live-action axis the fusion follows the tools (eval-calibrated): check…
- Shot #6 (43.4–45.1s): Tools say live action, the image review says 3D render; on the AI / live-action axis the fusion follows the tools (eval-calibrated): check…
- Shot #7 (45.1–48.4s): Tools say live action, the image review says 3D render; on the AI / live-action axis the fusion follows the tools (eval-calibrated): check…
- No AI listened to the soundtrack (the review covered the picture only): real voice versus TTS is inferred from the waveform; the effects were picked off the mix…

## Map

Read this page first; for detail, open only the file you need. Each line is `path | ~tokens | what is in it · when to read it`; paths are relative to this directory.

```videomd-map
video/timeline.md | 1101 | Timeline: one line per shot · what a stretch says, which shots need review, how a shot was made
video/moments.md | 113 | Special moments · reveals, twists, climaxes, goofs: times, key frames, clips
video/content.md | 220 | Content and structure · what it says, the narrative line, structure, the script
video/cast.md | 50 | Cast, scenes and props · reference images for characters, first-frame prompts
video/sound.md | 605 | Sound · voice, music, sound effects, beats and sources
video/rhythm.md | 552 | Rhythm and key frames · when cuts and transitions happen, shot lengths, the change curve, key frames of each shot
video/look.md | 962 | Camera, lighting and editing · for filmed shots: framing, camera, lighting, kit
video/packaging.md | 100 | Packaging · subtitles, styled text, stickers, picture-in-picture: timing and style
video/remake.md | 3017 | Remake plan · generation units, shoots, code builds, real material to collect, acting and emotion
video/shots/*.md | 751 | Per-shot detail, tokens per file on average · checking one shot: what is seen, the inference and its basis, prompts, frames
breakdown.json | 40262 | Full raw data · for programs; a model rarely needs it
shots/ | - | contact sheet, first and last frame of each shot · checking by eye
storyboard.jpg | - | storyboard of the whole video · the whole video at a glance
sfx/ | - | a clip of each sound effect · finding matching effects
packaging/ | - | subtitle files, packaging timeline, sticker frames · remaking subtitles and packaging
audio.png | - | waveform and beat chart · seeing the rhythm
```

## How to read

- One shot per line: `#<n> start-end (s) | key value | …`. A key ending in `~` is the tools' inference; keys without it are visible on screen or measured directly.
- `story` job in the story and the point · `seen` what is on screen · `act` acting (emotion, strength, face) · `camera` camera move · `overlay` overlays · `made~` how it was made (inferred) · `material~` where the material came from (inferred) · `remake` remake route · `flag` needs a second look
- Full detail for a shot is in `video/shots/<n>.md` (e.g. `video/shots/07.md`).
- What is “seen” can be checked against the frames; what is “inferred” is the tools' and image readers' judgement, with the basis in each shot file. When they disagree, trust the frames.
