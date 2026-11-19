# RicksClips — animated true-story Shorts pipeline

A working animation studio in a folder: it turns a Bangla/English narration track into a Ricks Clips-style
3D-cartoon vertical Short — three.js sets, flat 2D characters inside the 3D world, word-by-word captions,
a measured camera, and 42 automatic quality gates taken from 24 reference films.

This repository is the V1.1 skill (rules + tools + kits) plus the episodes built with it, including the
complete **Law 11** Bangla episode.

## What is in here

```
RicksClips_Skill_V1.1/          the skill: rules, tools, kits, agents
  SKILL.md, CB_RULES.md         the style + process source of truth
  tools/film_plan.py            THE gate keeper: bakes film.json → per-frame camera/performance, 42 gates
  templates/threejs_film/       preview kit: storyboard, animatic, stills, lock export (three.js r165)
  templates/vector2d_characters/150 cast characters + body forms, drawn in code
  templates/blender_look/       optional Blender look pass (materials, light, grade, 1080p)
  agents/, rules/dept/          one brief per department (writer, camera, set, props, lighting, animator…)
  library/                      harvested pitfalls and solutions
  references/                   measurements from the reference Shorts + locked look stills
  episodes/
    law11/                      Bangla Law 11 episode — full plan, sets, voice, storyboard, docs
    lantern/, railway-time/     small test episodes
docs/                           architecture, runbook, episode index (start here)
```

## Quick start

```bash
cd RicksClips_Skill_V1.1/templates/threejs_film
npm install && npx playwright install chromium
cd ../..
pip install pillow numpy              # faster-whisper only if you transcribe yourself
ffmpeg -version                       # must be on PATH

python tools/film_plan.py check episodes/law11/film.json
node templates/threejs_film/render.mjs episodes/law11/film.json --storyboard
node templates/threejs_film/render.mjs episodes/law11/film.json --frames 20,1690,3390
```

Animatic (with the Bangla voice muxed automatically):

```bash
cd episodes/law11
node ../../templates/threejs_film/render.mjs film.json --animatic --tmp /tmp/opencode
```

**Important:** renders read the *baked* plan in `out/plan/`. After editing `film.json`, always re-run
`python tools/film_plan.py check …` first.

## The Law 11 episode

- 121.5 s, 30 fps, 1080×1920 plan, 11 takes, 45 stations, 6 characters, 4 light states.
- Narration: the source Bangla track (302 words) — `voice/voice.wav`, word times in `voice/words.json`.
- Gate: **0 FAIL, 4 WARN of 41**; the accepted WARNs are documented in
  [`episodes/law11/CAMERA_NOTE.md`](RicksClips_Skill_V1.1/episodes/law11/CAMERA_NOTE.md).
- Script: [`episodes/law11/SCRIPT.md`](RicksClips_Skill_V1.1/episodes/law11/SCRIPT.md) ·
  notes: [`NOTES.md`](RicksClips_Skill_V1.1/episodes/law11/NOTES.md) ·
  storyboard: [`out/storyboard.html`](RicksClips_Skill_V1.1/episodes/law11/out/storyboard.html).

## Documentation

| doc | what |
|---|---|
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | how the pipeline works, `film.json` schema, gates, kits, extension points |
| [`docs/PIPELINE.md`](docs/PIPELINE.md) | runbook: audio → words → plan → gates → storyboard → animatic → final |
| [`docs/EPISODES.md`](docs/EPISODES.md) | episode index and status |
| [`RicksClips_Skill_V1.1/START_HERE.md`](RicksClips_Skill_V1.1/START_HERE.md) | the original read order for the AI crew |
| [`RicksClips_Skill_V1.1/CB_RULES.md`](RicksClips_Skill_V1.1/CB_RULES.md) | the full style rulebook |
| [`RicksClips_Skill_V1.1/INSTALL.md`](RicksClips_Skill_V1.1/INSTALL.md) | Windows install of the skill into Claude Code |

## Quality gates

The plan is measured before a single picture is judged. `tools/film_plan.py check` reports 42 gates in five
groups — camera (rest %, travel length, speed median/p90/peak, cuts, roll, lens…), framing (first face, face %,
head cut by edge, caption band, shot mix…), world, story (sentence subject on screen, named nouns), acting
(pose changes, frozen figures, props in hands, interpenetration, fx).

## Requirements

Node 18+, Python 3.11+, ffmpeg, Playwright Chromium. Blender + NVIDIA GPU only for the final look pass.
Fish Audio key only if you generate voice with the skill instead of supplying your own track.

## Contributors

See [`CONTRIBUTORS.md`](CONTRIBUTORS.md). Maintainer: [@NurMohammadDuari](https://github.com/NurMohammadDuari).
Want to improve the pipeline? Read [`CONTRIBUTING.md`](CONTRIBUTING.md) — new sets, poses, gates and docs are welcome.

## Licence

`RicksClips_Skill_V1.1/LICENSE.txt` — personal use, commercial videos allowed; the skill files may not be
resold or publicly published. Reference videos, music, SFX and BlenderKit assets are not included.
