# Contributing

Thanks for helping make the pipeline better. This repo is a working animation studio: everything is
data + code, and every change is measured by the same gates before it is judged by eye.

## Dev setup

```bash
git clone https://github.com/NurMohammadDuari/ricksclips-animation-skill.git
cd ricksclips-animation-skill/RicksClips_Skill_V1.1/templates/threejs_film
npm install && npx playwright install chromium
cd ../..
pip install pillow numpy            # faster-whisper only for transcription
```

You need Node 20+, Python 3.11+ and **ffmpeg on PATH** (the animatic step shells out to it).

## The two commands you will use all day

```bash
python tools/film_plan.py check episodes/law11/film.json          # bake + 42 gates
node templates/threejs_film/render.mjs episodes/law11/film.json --frames 0,900,3000
node templates/threejs_film/render.mjs episodes/law11/film.json --storyboard
```

**Rule #1:** renders read the *baked* plan in `out/plan/`. After any `film.json` edit, re-run `check` first,
or you will silently render the old plan.

## What a good PR looks like

- `python tools/film_plan.py check <film>` ends with **0 FAIL**. WARNs are acceptable only with a written reason
  in that episode's `CAMERA_NOTE.md`.
- Stills/screenshots for visual changes (`--frames`), not just a description.
- No `node_modules/`, `__pycache__/`, `out/.puppet_cache/` or render temp folders in the diff.
- Keep `tools/film_plan.py` pure Python (math + json only): the Blender look pass imports it.
- Sets and episodes follow the conventions in [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
  (metres, Z up, `B2T`, mesh `name` + `userData.role`).

## Where help is most useful

| area | what to do | entry point |
|---|---|---|
| **Any-script generator** | lexicons, levelled camera formulas, stage clearing, gate repair | `tools/autofilm.py` |
| **Audio analysis** | word timing from audio + timecodes, loudness map | `tools/audio_probe.py` |
| **New characters** | script descriptors → editable castkit sheet | `tools/gen_cast.py` |
| **New set archetypes** | a data-driven maker + a layout recipe | `templates/threejs_film/sets/place_kit.js` |
| **New sets** | one module per set, `build(THREE, scene, film, ctx)` | `episodes/<ep>/sets/*.js` |
| **Poses** | add a hand target line | `templates/threejs_film/poses.mjs` |
| **Characters** | new cast sheet / body form | `templates/vector2d_characters/` |
| **Gates** | a measured rule with a target + a fix line | `tools/film_plan.py` (`gate(...)`) |
| **Docs** | clarify the runbook, add a worked example | `docs/` |
| **Episodes** | a new film built with the pipeline | `episodes/<name>/` |
| **Bugs** | repro + `out/plan/plan_report.md` + a still | open an issue |

## Style

- Bangla/English both welcome in docs; code comments in English, short and factual.
- By contributing you agree that your contribution is licensed under **CC BY 4.0**, the license of this repo.
- One idea per commit, imperative subject line (`fix: raise behind-counter cameras in law11`).
- When you fix a bug that cost you time, add it to `RicksClips_Skill_V1.1/library/pitfall/` with cause and fix —
  that library is the most valuable file in the repo.
