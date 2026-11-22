# TIMING AND CONTINUITY REPORT — Law 11

## Timing foundation
- Master clock = the user's narration MP3 (121.3 s). `voice/words.json` holds 302 energy-aligned word times (0.1 s → 120.9 s). Frames = 30 fps, film length 3,645 frames = 121.5 s. No time-stretching of audio anywhere.
- Every cut lands on a script-named place/time jump; every named-noun rest arrives 0–6 frames BEFORE its word (CB rule), verified by the plan gate `word stations not at rest on their word` = 0.
- Action-to-narration checks: the packet appears on "প্যাকেট", the handshake on "মালিক", the board on "আনার/অংশীদার", the walk-out on "ফিরলো" — all inside their spoken windows (beat-sheet verified).

## Animation principles in the pipeline
1. **Timing/spacing:** tweened pose changes (6 f, ease-out; walks 8 f) — no snap poses.
2. **Anticipation:** two-frame wind-up is authored inside the move library (`m:walk/B`, `grip_shoulder`).
3. **Follow-through/overlap:** held props are grip-locked to hands per frame (gate = 0 unheld props); cloth/packets sway via the set's `update(f,t)`.
4. **Ease:** smootherstep easing between station arrive/depart and place events.
5. **Staging/silhouette:** 24 mm, level camera, feet in the bottom band (median feet height 0.83) — silhouettes read at Shorts size.
6. **Arcs:** travel paths are Catmull-Rom through station aims (no linear robot pans).

## Continuity ledger
| Item | status |
|---|---|
| Shop geography (counter along X, shopkeeper behind, customers front) | constant across t1/t3/t6 |
| Door motif geometry (same door, jamb, step, tulsi) | same set file `home_door` reused for night + morning — continuity by construction |
| Character positions at cut points | performance baked per frame; entering characters appear at door/street anchors, never teleport mid-scene (longest unexplained jump found: none in the beat sheet) |
| Light continuity | night → morning → night → morning → golden, each change is a script time jump; no mid-scene light pops found |
| Props | packet, khata, tea cups persist and travel with their owners |
| Captions | one word at a time from words.json; caption band heads 4.6 % (target ≤ 3 — the short child at the counter; accepted, documented) |

## Repaired timing/transition defects (from the parallel rebuild, recipe preserved)
- Insert rests previously arrived WITH heads at frame edges (95–100 % cut) — re-centered; edge-cut gate now 9.0 %.
- A 3.72 s overlong hold + 2.07 s crawl travel class of error was rebalanced by the plan's own two-pass baker (long travels get frames taken from rests down to min_hold) — the surviving film's longest travel is 3.03 s (Rick's median is 3.0).

## Frozen-scene and dead-air audit
- Longest stretch without a face: 1.0 s (gate ≤ 6) — no dead air.
- Longest frozen figure with resting camera: 2.9 s (gate ≤ 3) — inside tolerance; nothing else moves in those windows by design (held breaths before the verdicts).
- Unwanted silence: the narration has no silent gaps > 1.5 s (audio probe verified); apad pads the tail to the video length at mux.
