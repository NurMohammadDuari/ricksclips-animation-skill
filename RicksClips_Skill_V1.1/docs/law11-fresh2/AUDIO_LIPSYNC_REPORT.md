# NARRATION, SOUND & LIP-SYNC REPORT — Law 11 (fresh2)

## Narration timestamps (measured, not guessed)

- Audio: the user's own Bangla narration, 121.34 s (ffprobe).
- 198 words energy-aligned by `tools/audio_probe.py` → `voice/words.json` (0.04 s → 120.1 s).
- Sentence spans re-derived from that alignment (the earlier map was stale by up to 14 s —
  see SCRIPT_CORRECTIONS.md C-1). Word indices in the film.json `sentences` table and the
  `say` ranges in the acts all resolve through this alignment.
- Captions: one spoken word at a time, burned into every frame by the kit's caption system
  (Arial-bold-style, baseline 71.5 % of height) — verified readable in the beat inspection.

## Lip-sync (phoneme → viseme)

- `film_plan.visemes()` maps each spoken word's letters to the viseme set
  MBP / FV / L / WQ / CDGK / AI / E / O / U; mouths change every 2 frames across the word.
- `say` ranges attach each spoken sentence to its speaker: kaka (1, 3, 4, 5, 7, 10, 11),
  rafi (2, 9, 12, 13, 14, 15), ma (6, 8) — mouths move ONLY on those quoted ranges.
- Characters that are on screen but not speaking carry their acting face with mouth `rest`
  — no random mouth flapping (kit rule, verified in the acting gates).
- The Bangla letter→viseme mapping is approximate (the kit's set is Latin-tuned; Bengali
  viseme drawing exists in the vendored corpus but is not wired here) — documented as a
  LOW remaining issue in ANIMATION_QA_REPORT.md.

## Sound design

- `out/plan/sound_events.json` — 10 cue marks on the action nouns: door_knock (both packet
  visits), coin_box (বেতন, বেতনে), paper_turn (নম্বর, খাতা, অংশীদার), flash (চোর).
- The delivered mux carries the narration track (mp3, copied stream — no re-encode loss).
  The cue sheet exists for the mix; SFX/music files are NOT in this cut (the skill ships
  SFX as placeholders — documented in the audit and in FINAL_PRODUCTION_REPORT.md).

## Synchronization verification

- ffprobe on the delivered MP4: video 120.7 s + audio 121.3 s, `-shortest` ends on the last
  video frame (no frozen tail, no audio cut-off mid-word — the last spoken word ends at
  120.1 s, before the video end).
- Beat inspection (16 stills from the delivered MP4): captions land on the spoken words at
  every checked beat (2, 10, 18 … 119 s), including the two door-knock beats and the outro.
- Mouth activity coincides with speech at the checked beats (t9 teaching, t12 begging,
  t14 lesson) — verified visually on the extracted frames.
