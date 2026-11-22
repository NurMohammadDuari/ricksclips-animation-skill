# CAMERA_NOTE — law11-fresh (2026-11-22)

Plan status: `python3 tools/film_plan.py check` = **0 FAIL, 10 WARN of 41 gates** (baked, approved to render).
Measured-film status (`tools/check_film.py` on the rendered animatic): 4 FAIL, 2 WARN of 19 gates.
Every FAIL below carries its disposition, the same way `episodes/law11-zai/CAMERA_NOTE.md` documented them.

## Dispositions

1. **voice pace, words per second — 2.12 (gate target 3.5-4.5).**
   The narration IS the user's own Law 11 MP3 (`voice/narration.mp3`, 121.3 s, Bangla).
   The gate's own instruction is "regenerate at the right pace, never time-stretch" — the user's
   voice is the source of truth and must not be altered. ACCEPTED (audio-driven film).

2. **speed median, px/f — 0.83 measured (Rick 4.1), 1.76 planned.**
   The plan camera creeps calmer than Rick's corpus. The film still passes the plan-level gate as
   a WARN and the dead-still share (20.7 %, target <= 21). Rick-style faster flow is a maintainer
   follow-up (re-fit SEEN, same disposition as law11-zai). ACCEPTED for this episode.

3. **travel length p90 — 0.89 s measured (target 2.1-6.3).**
   The bake clips the longest planned travel (3.4 s at the ten-year time jump) to the gap its
   neighbours leave (2.35 s), and the measured detector counts only the frames above the moving
   threshold, trimming the eased ends. The film has 11 flowing travels; none reaches 2.1 s measured.
   ACCEPTED with the same re-fit follow-up as (2).

4. **rests per 10 s (plan) — 4.95 (target 2.2-4.5).**
   60 stations over 121.3 s. Merging further would fold distinct script beats (the gate-keeper
   approved it as a WARN; the scene decides, CB 2026-11-10). ACCEPTED.

## Planned flash confirmed
- s 30.97: the t4 -> t5 place cut + the `warm_up` mood at 31.1 (ma's warning -> the teaching).
  This is a planned flash (mood re-grade on the story turn), not an unplanned flicker.

## Follow-ups (maintainer)
- Re-fit the SEEN calibration between plan px/f and measured px/f (law11-zai carry-over).
- One longer unbroken travel: lay the t5 teaching beat across the counter aisle so the bake
  does not clip the ten-year time-jump move.
