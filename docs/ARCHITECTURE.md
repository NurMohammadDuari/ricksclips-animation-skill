# Architecture — how RicksClips_Skill_V1.1 actually works

This document is the map of the codebase: what each layer does, how data flows, and where to change things.
For the step-by-step production runbook see [`PIPELINE.md`](PIPELINE.md); for episode status see [`EPISODES.md`](EPISODES.md).

```
                        ┌──────────────────────────────┐
   audio (mp3/wav) ────▶│ voice/words.json (302 words) │  word → start/end seconds
                        └──────────────┬───────────────┘
                                       │
                        ┌──────────────▼───────────────┐
   script / beats ─────▶│ episodes/<ep>/film.json      │  THE single source of truth:
   cast, sets, camera   │  places, cast, takes,        │  shot blueprint + camera + acting
                        │  stations, acts, fx, sound   │  + sound cues, all in one file
                        └──────────────┬───────────────┘
                                       │  python tools/film_plan.py check
                                       ▼
              ┌────────────────────────────────────────────────┐
              │ out/plan/camera_baked.json      per frame      │
              │ out/plan/performance_baked.json per character  │
              │ out/plan/sound_events.json      mix cues       │
              │ out/plan/plan_report.md/.json   42 gates       │
              └───────────────┬────────────────┬───────────────┘
                              │                │
             node render.mjs  │                │  node --export-lock
                              ▼                ▼
                 ┌──────────────────┐   ┌──────────────────────┐
                 │ three.js animatic│   │ out/lock/ (GLB sets, │
                 │ storyboard/stills│   │ card PNGs, lock.json)│
                 │ mp4 + voice      │   └──────────┬───────────┘
                 └──────────────────┘              │ Blender look pass
                                                   ▼
                                     final 1080p render, grade, mix
```

## 1. Repository layout

| path | what |
|---|---|
| `SKILL.md`, `CB_RULES.md`, `WORKFLOW.md`, `DENSITY_RULES.md`, `CINEMATOGRAPHY.md` | the rules the AI crew follows (source of truth for style + process) |
| `START_HERE.md`, `FILE_GUIDE.md`, `INSTALL.md`, `CHANGELOG.md` | onboarding, keep/delete policy, install, version notes |
| `tools/` | the gates and bakers: `film_plan.py`, `check_film.py`, `check_episode.py`, `measure/`, `token_report.py`, TTS/voice helpers |
| `templates/threejs_film/` | the preview kit: storyboard, animatic, stills, lock export (three.js r165 vendored) |
| `templates/vector2d_characters/` | the character package: 150 cast characters + body forms, drawn in code (SVG) |
| `templates/blender_look/` | the Blender look pass: rebuild from lock, materials, lights, grade, post |
| `templates/blender_cine/`, `templates/motion_styles/`, `templates/bridge/`, `templates/props/`, `templates/pieces/` | optional looks, motion libraries, Blender bridge, hero props, set pieces |
| `agents/` + `rules/dept/` | one agent brief and one rule slice per department (writer, camera, set, props, lighting, animator, sound, judges) |
| `library/pitfall/` + `library/solution/` | harvested lessons: each pitfall has a name, cause, fix |
| `references/` | measurements from 24 Rick Shorts (gates), locked look stills, reports |
| `examples/lightning-spear/` | a complete finished film's docs + code (no media) |
| `episodes/<name>/` | one film per folder: `film.json`, `sets/`, `voice/`, docs, `out/` artifacts |

## 2. The one file: `film.json`

Everything about a film lives in one JSON file. `tools/film_plan.py` is the only interpreter; both the three.js preview
and the Blender look pass read its baked output, so camera and timing can never drift between them.

Top-level keys:

| key | meaning |
|---|---|
| `title`, `size`, `fps`, `end` | film metadata; `end` is frames (this film: 3645 @ 30 fps = 121.5 s) |
| `words` | path to the word-timing file (`voice/words.json`) |
| `camera_idea` | one idea per film + why + the signature move (checked by the storyboard judge) |
| `cast` | `who → { puppet, height, heads_tall }` |
| `places` | `name → { set, light, backdrop }` (`backdrop` = metres, parallax scale) |
| `props` | named props (`khata`, `coin`, …) |
| `takes` | `id, place, stations[]` — a take is a continuous camera run in one place |
| `kicks` | optional speed kicks on travels |
| `acts` | 174 timed character events in this film |
| `sentences` | the script split into narrated sentences with `subject` + `nouns` (story gates) |
| `fx`, `moods`, `sound` | effect cues, light/mood changes, mix cues |

A **station** is one camera setup inside a take:

```json
{ "at": {"s": 31.3}, "subject": "rafi", "framing": "W",
  "pos": [0.25, -0.3, 1.75], "aim": [0.0, 2.1, 1.30], "lens": 24,
  "travel": 1.2, "hold": 0.8, "shows": ["counter", "khata", "rafi"] }
```

- `at` accepts frames (`12`), words (`["word", n, offset]`) or seconds (`{"s": 1.5}`).
- `framing`: `W` whole, `M` medium, `C` close, `P` place, `O` object (drives rest speed + shot-mix gates).
- `travel` seconds to reach it; `hold` seconds of rest; `shows` is what the story gate looks for.
- Optional: `drift`, `creep`, `roll`, `dof`, `hand_at`, `card_scale`, `held3d`.

An **act** is a character event:

```json
{ "who": "rafi", "at": {"s": 31.15}, "visible": true, "pos": [0, 2.1, 0],
  "view": "34", "dir": 1, "pose": "write", "prop": "khata", "hand": "R", "face": "cool" }
```

`enter`/`exit` move off/into the doorway; **every re-entry must re-assert `visible: true`** (see pitfalls).
Poses come from `templates/threejs_film/poses.mjs`; faces from the character package; `view` is front / 34 / side / back.

## 3. `tools/film_plan.py` — bake + 42 gates

Pipeline:

1. `load()` resolves word times and `end`; `fr()` converts any time form to frames.
2. `bake_camera()` builds per-frame camera from station segments: smootherstep travels, rest motion (`drift`/`creep`),
   kicks, looks (look-at changes), clings (subject tracking). Output is one dict per frame.
3. `bake_performance()` turns acts into per-character runs (view, dir, pose, face, mouth, blink, prop, x/y).
4. `apply_looks()` / `apply_clings()` re-aim the camera when the plan asks for it.
5. `check()` runs the 42 gates and writes `out/plan/*.json` + `plan_report.md`.

The gates compare the plan against numbers measured from 24 Rick Shorts (`references/measure/gates_film.json`).
Measuring size is 720×1280 so every px/f number is comparable across episodes.

| group | gates (short) |
|---|---|
| camera (13) | at-rest %, rests/10 s, rest length, longest travel, speed median/p90/peak, dead-still %, cuts/10 s, tilt while resting, roll rate, lens range, >120° swings, word-stations-at-rest |
| framing (14) | first face, face in first 5/15 s, longest no-face, face %, head width median/p90, body-fit %, feet height, head height, caption band, head cut by edge, whole-body fits, rest-with-face, shot mix, world-led %, medium % |
| world (2) | places in the film, share of most-used light |
| story (3) | sentence subject/action on screen %, named nouns within 0.5 s, sentences table |
| acting (5+1) | pose/face changes per 10 s, frozen figure, props without hands, interpenetration, fx per 10 s, mood changes/min |

Exit status is textual: **FAIL** blocks, **WARN** must be documented (see each episode's `CAMERA_NOTE.md`).

## 4. `templates/threejs_film/` — the preview kit

`render.mjs` starts a tiny static server, drives headless Chromium (Playwright), and reads back frames:

| command | output |
|---|---|
| `--storyboard` | `out/storyboard.html` + `.png` (START/END panel per station + CAM/MOVE/WORD strip) |
| `--frames 0,45` | `out/stills/f_00000.png` (verification stills) |
| `--animatic` | `out/animatic.mp4` at half size; `voice/voice.wav` is muxed automatically (`apad`, `-shortest`) |
| `--visibility` | per-frame who/what is inside the frame (debug) |
| `--export-lock` | `out/lock/` GLB sets + card PNGs + `lock.json` for Blender |
| `--serve` | live preview in a browser with sound |

`render_gpu.mjs` is the same with GPU drawing on the PC (default on Windows/NVIDIA).

Inside the page:

- `film.js` + `film_page.html` — the player: `window.setup(cfg)` / `window.renderFrame(f)`.
- `puppets.mjs` — adapter to the character package (`stateKey`, `svgFor`); the package is copied to a cache and never edited.
- `poses.mjs` — pose library: hand targets in arm lengths, held props drawn at the hand.
- `sets/<name>.js` — one module per set, exports `build(THREE, scene, film, ctx)` and may return `{ update, anchors }`.
- captions — one word at a time, in the caption band (0.58–0.76 of frame height).

**Critical:** rendering reads `out/plan/`, not `film.json`. After ANY `film.json` edit you must re-run
`python tools/film_plan.py check <film>` or the render silently shows the old plan.

## 5. Sets and coordinates

Plan coordinates are metres, **Z up, Y forward** (Blender convention). three.js converts `(x, y, z) → (x, z, -y)`
through `ctx.B2T`. Every mesh gets a `name` and a `userData.role` (`ground`, `wood`, `metal`, `cloth`, `glass`,
`stone`, `brick`, `plaster`, `roof`, `water`, `foliage`, `lamp`) or an exact `userData.mat` (`wood_grain`, …).
The look pass uses those roles to assign real materials.

The episode's own `sets/` folder wins over the kit's `templates/threejs_film/sets/`.

## 6. Characters

Cast entries: `"puppet": "cast:<name>"` (a character from the 150-cast sheets), `"form:<name>"` (a body form: kid,
lady, elder, baby…), or a named puppet in `cast.mjs`. `height` is in metres and drives every framing gate.
The sheet supplies hat/hair/costume/props; the film supplies face, mouth, blink, pose.
Cast characters are drawn for the front view; back views are dashed on purpose.

## 7. Blender look pass (not used in this episode)

`node render.mjs film.json --export-lock` freezes the approved animatic into `out/lock/`, then
`templates/blender_look/from_lock.py` rebuilds exactly that scene in Blender and adds only materials, light, air,
effects, grade and the final 1080p render. This keeps the approved camera/acting byte-identical.
Requirements: Blender + NVIDIA GPU. See `templates/threejs_film/GPU_RENDER.md` and `templates/blender_look/`.

## 8. Agents and rules

`agents/*.md` are department briefs (writer, researcher, character artist, set builder, props hero, lighting, camera
director, animator, vfx, background painter, look finisher, editor/compositor, sound designer, storyboard judge,
studio director). `rules/dept/` holds the per-department slice of the big rule files; rebuild with
`python tools/slice_rules.py` after editing a rule. The lean pipeline gives the user exactly one gate (the storyboard),
then the crew works alone to the final.

## 9. Assets and what is not included

Not shipped (licensing): other creators' videos/frames, BlenderKit assets, music/SFX libraries, Fish Audio keys.
`references/video` is optional; the Rick checks need your own reference clips. Everything else rebuilds from code.

## 10. Extending the system

- **New set:** add `episodes/<ep>/sets/<name>.js` exporting `build()`; reference it from `places.<name>.set`.
- **New pose:** add a line to `POSES` in `templates/threejs_film/poses.mjs` (`[out, down]` in arm lengths); unknown poses warn and stand.
- **New character:** add a sheet/cast module in `templates/vector2d_characters/` (the characters package owns it) and use `cast:<name>`.
- **New gate:** add a `gate(...)` call in `tools/film_plan.py`; document the target and the fix line.
- **New tool:** put it in `tools/`, keep it pure-Python if Blender/`film_plan` must import it.

## 11. Known limitations

- Visibility is projection-only (no occlusion culling) — a character behind a wall still counts as visible.
- three.js preview light is approximate; only the Blender pass is final.
- Moods and fx are placeholders (colour wash, ring at the prop); the look pass designs them.
- The animatic is half-size by default (`--scale 0.5` → 540×960); the final is 1080×1920 via Blender.
