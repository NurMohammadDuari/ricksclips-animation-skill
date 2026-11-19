# Production runbook — from audio to MP4

Commands are run from `RicksClips_Skill_V1.1/`. Episode folder: `episodes/<name>/`.

## 0. One-time setup

```bash
# preview kit + character package
cd templates/threejs_film && npm install && npx playwright install chromium && cd ../..
# tools
pip install pillow numpy faster-whisper
# ffmpeg must be on PATH (render.mjs shells out to it for --animatic)
ffmpeg -version
```

Optional: `python install.py` installs the skill + agents into `~/.claude/` and fills `<SKILL_ROOT>` in every text file.

## 1. Voice and word timings

`voice/words.json` is a list of `{ "w": "<word>", "s": <start s>, "e": <end s> }`, one entry per spoken word.
`voice/voice.wav` is the narration the animatic will mux.

This episode's file was written from the source track's line timings with `episodes/law11/make_words.py`
(302 words, 0.1–120.9 s). Alternative: `tools/voice_prep.py` / `tools/fish_tts.py` for Fish Audio.
Always check that the last word time matches the audio length.

## 1b. Start from any script (`autofilm.py`)

You do **not** have to write `film.json` or sets by hand. `tools/autofilm.py` takes a script (Bangla or
English, a file or a quoted string) and produces a complete episode:

```bash
python tools/autofilm.py episodes/<slug> --script story.txt [--title "..."] [--words voice/words.json] [--force]
```

What it does, in order:

1. Splits the script into sentences and times every word (real `words.json`, if given, or a speech-like track).
2. Reads the topic with Bangla + English word lists: place, character, prop, face, pose.
3. **Builds and saves all needed sets** in `episodes/<slug>/sets/set_pN.js` — ordinary editable modules,
   each a small `layout` dict passed to the shared `templates/threejs_film/sets/place_kit.js`.
   Furniture is placed by Python in explicit metres, and `clear_stage()` keeps the acting area empty.
4. **Levels** the 24 mm camera to each subject's own height (W / M / C / P formulas solved against
   `film_plan.py`'s projection): every character stands on the floor — short ones on a saved step — and
   the camera aims at their head height, not at a fixed world point.
5. Writes cast, takes, stations, acts, moods, fx, sound, `SCRIPT.md`, `SETS.md` and `CAMERA_NOTE.md`.
6. Runs `film_plan.py check` and repairs the plan until it reports **0 FAIL**. WARNs are listed with reasons
   in `CAMERA_NOTE.md`.

Then continue with §3–§7 as usual. If you supply `--words`, use the same words file for the voice track so
captions and lip-sync line up. Re-running with `--force` overwrites the generated episode.

### With narration audio + new characters

```bash
python tools/autofilm.py episodes/<slug> --audio narration.mp3 --script story.txt \
    [--title "..."] [--transcribe] [--reuse-cast] [--force]
```

`tools/audio_probe.py` reads the audio: WAV directly, other formats through ffmpeg. If ffmpeg is not
available it still uses the file's duration (mutagen) plus the script's `00:04 [রাফি]: …` timecodes, so
word times are audio-accurate without a decoder. `--transcribe` uses faster-whisper when installed.
The per-word loudness is measured from the waveform when possible, otherwise from punctuation;
`autofilm.py` spends kicks / glints / light changes on the loud words.

Unless `--reuse-cast` is given, `tools/gen_cast.py` writes `cast/sheets/story_cast.mjs` — brand-new
castkit specs (`form`, `size`, `outfit`, `coat`, `face`, `hair`) picked from the speakers and the role
words in the script. `film.json` gets `puppet_pkg: ["cast", "../../templates/vector2d_characters/code"]`
and `cast:story_cast/<role>`; the sheet and its `CAST.md` are ordinary editable files. The generator
also saves `voice/voice.wav` (or `.mp3`) next to `film.json`, which is what the animatic muxes.

Standalone: `python tools/audio_probe.py narration.wav --script story.txt --words … --report …` and
`python tools/gen_cast.py episodes/<slug> analysis.json`.

## 2. Plan the film in `film.json`

Fill in `title, size, fps, end, words, camera_idea, cast, places, props, takes, acts, sentences, fx, moods, sound`.
Keep every station on a word or a beat, and give every sentence a `subject` and its `nouns` so the story gate can check them.

Time forms accepted anywhere: frames (`12`), words (`["word", 2, +4]`), seconds (`{"s": 31.3}`).

## 3. Gates (must pass before any render)

```bash
python tools/film_plan.py check episodes/law11/film.json | grep -E "FAIL|WARN|RESULT"
```

- `0 FAIL` is required. WARNs are allowed only if you write down why in the episode's `CAMERA_NOTE.md`.
- `check` also bakes `out/plan/camera_baked.json`, `performance_baked.json`, `sound_events.json`, `plan_report.md`.
- **Rendering reads the baked files.** After ANY `film.json` edit, re-run `check` before rendering stills —
  otherwise the render silently shows the old plan (this is the #1 wasted hour in this pipeline).

## 4. Look at it (stills + storyboard)

```bash
node templates/threejs_film/render.mjs episodes/law11/film.json --frames 20,1690,3390
node templates/threejs_film/render.mjs episodes/law11/film.json --storyboard
```

Read individual stills in `out/stills/` (watch for: head cut by frame edge, character behind furniture, empty START
panel, opaque "light" planes). Then review `out/storyboard.png` band by band.
The storyboard PNG is tall; crop bands with PIL if needed.

## 5. Animatic (with voice)

```bash
node templates/threejs_film/render.mjs film.json --animatic --tmp /tmp/opencode   # from the episode folder
```

- Renders every frame at `--scale 0.5` (540×960) into a temp folder, then muxes `voice/voice.wav` to `out/animatic.mp4`.
- Cost on this machine: ~1.4 s/frame at 540×960 → 3645 frames ≈ 85 min. Run it in the background.
- `--step 1` renders every frame (default); larger steps preview faster.
- Add `--scale 1.0` only when you want a full-size preview (4× the time).

Useful checks afterwards:

```bash
ffprobe -v error -show_entries stream=codec_type,codec_name,duration -of compact out/animatic.mp4
```

## 6. Final look (optional, GPU)

```bash
node templates/threejs_film/render.mjs film.json --export-lock      # out/lock/ for Blender
```

Then `templates/blender_look/from_lock.py` rebuilds the locked scene in Blender and adds materials, light, air,
effects, grade and the 1080p render. See `templates/threejs_film/GPU_RENDER.md`.
On a Windows/NVIDIA machine use `render_gpu.mjs` (same CLI) for the preview renders.

## 7. Deliverables

| file | what |
|---|---|
| `out/animatic.mp4` | the film, H.264 + AAC, voice muxed |
| `out/storyboard.png` / `.html` / `out/storyboard_panels/` | the one user gate |
| `out/plan/plan_report.md` | every gate with value, target, PASS/WARN/FAIL and the fix |
| `film.json`, `sets/*.js`, `voice/` | the whole film, rebuildable |
| `SCRIPT.md`, `CAMERA_NOTE.md`, `NOTES.md` | script, accepted WARNs + camera lessons, delivery notes |

## Troubleshooting

| symptom | cause | fix |
|---|---|---|
| stills don't change after editing `film.json` | render used stale `out/plan` | re-run `film_plan.py check` |
| character invisible on re-entry | `exit: true` later, re-entry act lacked `visible: true` | always re-assert `visible` |
| face cut by the counter | camera at/below counter-top in front of it | raise camera z ≈ 1.75–1.9, aim z ≈ 1.30 |
| a shot shows a brown wall | camera too close to the counter front (y < ~1.3 m from it) | pull back, keep the 24 mm lens |
| white board in frame | a `MeshBasicMaterial` "light" plane is opaque | give it `opacity` (0.15–0.2) |
| empty START panel | station arrives before the actor's `visible` act | move the act 0.05–0.15 s earlier |
| `_perf`/`_dir` keys written into `film.json` | `film_plan.load()` cache keys saved back | strip keys starting with `_` before `json.dump` |
| edge cuts everywhere | nudging the wrong station | baked index ≠ film.json index when a take's `at` values are out of order; map back first |
