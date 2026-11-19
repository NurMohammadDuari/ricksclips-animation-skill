# How this episode was made

This film was generated from the **script + narration audio**, not copied from the hand-built `law11/`
episode. The command was:

```bash
python tools/autofilm.py episodes/law11-auto \
  --audio "/home/mint/Desktop/RicksClips/The 48 Laws Of Power By Robert Greene Explained In Bangla Law 11.mp3" \
  --script story-with-timecodes.txt \
  --title "৪৮ শক্তির নিয়ম — নিয়ম ১১"
```

1. `tools/audio_probe.py` read the mp3's real length (121.34 s) and the script's `00:00 [স্পিকার]:`
   timecodes, turned them into 254 timed words (`voice/words.json`) and a loudness map
   (`out/audio.json`). No ffmpeg was available on the machine, so the decoder fell back to
   mutagen duration + the script's own pockets — the word times still follow the audio line by line.
2. `tools/gen_cast.py` read the speaker labels and wrote **new characters** in
   `cast/sheets/story_cast.mjs` (chacha = dad/farmer, ma = lady/sundress, rafi = standard/three-piece)
   and `CAST.md`. `film.json` points `puppet_pkg` at this sheet plus the locked character code.
3. `tools/autofilm.py` analysed places and props from the story, built and saved 4 scene sets in
   `sets/`, staged the cast on them, levelled a 24 mm camera to each subject, and repaired the plan
   to **0 FAIL / 9 WARN of 41** (the WARNs and their reasons are in `CAMERA_NOTE.md`).
4. `node templates/threejs_film/render.mjs … --animatic` drew the saved sets and new cast and muxed
   the source narration (saved as `voice/voice.mp3`) into `out/animatic.mp4`.

Everything in this folder is editable: change a `layout` in `sets/`, a spec in
`cast/sheets/story_cast.mjs`, or a station in `film.json`, then re-run
`python tools/film_plan.py check episodes/law11-auto/film.json` before rendering again.
