# Law 11 — NOTES (episode delivery notes)

**Title:** ৪৮ শক্তির নিয়ম — নিয়ম ১১ (বাংলা): কাজ সবাইকে শেখান, জায়গা কাউকে না
**Source:** `The 48 Laws Of Power By Robert Greene Explained In Bangla Law 11.mp3` (121.3 s)
**Format:** 1080×1920 (9:16), 30 fps, 3645 frames, three.js animatic with Bangla voice + Bangla one-word captions

## Pipeline as run (lean V1.1, no Blender)
1. Audio → `voice/voice.wav` (10.7 MB) + `voice/words.json` (302 word anchors from the script's line timestamps, `make_words.py`).
2. Two sets: `sets/shop.js` (sweet shop — counter is the seat of power), `sets/home.js` (Rafi's home + door, for `home_door`).
3. `film.json` — 4 places, 11 takes, **45 stations**, 6 characters (chacha, rafi, nephew, ma, neighbor, helper), all beats anchored to word times. Camera idea: *"The counter that changes hands"* — every era of the story is told by WHO stands behind the counter.
4. Gate: `python tools/film_plan.py check episodes/law11/film.json` → **0 FAIL, 4 WARN of 41** (framing/pacing WARNs documented as intentional; see `out/plan/plan_report.md`).
5. Storyboard: `out/storyboard.png` / `.html` + `out/storyboard_panels/` — reviewed band by band (faces, headroom, edge cuts, light_shaft opacity fix, nephew cap gag).
6. Render: `node templates/threejs_film/render.mjs film.json --animatic` → `out/animatic.mp4` (voice auto-muxed from `voice/voice.wav`, AAC, `apad` + `-shortest`).

## Shot mix (45 stations)
W 23 · P 13 · M 6 · C 2 · O 1 — world-led 28 %, face-coverage gates all PASS.

## Known WARNs (accepted)
- Head centres in caption band 4.6 % (Rick ref 2.7 %) — short characters only, faces stay readable.
- Pacing/spot WARNs resolved in review; final re-check after last patch: 0 FAIL.

## Fixed during build (pitfalls worth harvesting)
- `exit:true` without `"visible":true` on re-entry → character invisible (46.9 s face gap). **Always re-assert visible on every re-entry act.**
- `FP.check` caches bake in `F["_perf"]`; save() wrote the cache back into film.json — strip `_`-keys before every save.
- Baked camera stations are sorted by arrival time; film.json original index ≠ baked index when travels interleave.
- `light_shaft` as opaque MeshBasicMaterial renders as a white board — use low opacity.
- Travel speed gate reads backdrop px/frame: park rest stations (`creep:0`), put motion on travels/pans/kicks.

## Deliverables in this folder
| File | What |
|---|---|
| `out/animatic.mp4` | the film (H.264, 1080×1920@30 with voice — render at scale 0.5 = 540×960 preview; final Blender look pass would re-render at 1.0) |
| `out/storyboard.png/.html`, `out/storyboard_panels/` | storyboard (45 stations, START+END) |
| `out/plan/` | baked camera/performance + `plan_report.md` (gate results) |
| `film.json` | the single plan file |
| `CAPTIONS.md` | caption timing sheet from words.json |
| `voice/` | voice.wav + words.json |
| `sets/` | shop.js, home.js |

## What is NOT done (would need the full plan)
- Blender look pass + 1080p final render (needs GPU), grade, sound design/music (SFX/music folders were never provided), YouTube metadata/thumbnail package, OneDrive backup.
