# PROJECT AUDIT — Law 11 (Bangla) · RicksClips pipeline

**Date:** 2026-11-22 · **Auditor:** production repair pass (senior-director directive)
**Production audited:** `RicksClips_Skill_V1.1/episodes/law11` (the toolkit's own Law-11 film, 11 takes, 3,645 frames @ 30 fps, 121.5 s)
**Source audio:** `upload/The 48 Laws Of Power By Robert Greene Explained In Bangla Law 11.mp3` (121.3 s, the user's narration)
**Note on scope:** a parallel rebuilt production (`episodes/law11-fresh2`, 10 takes, 7 original characters) was lost in a sandbox recycle before its render finished; every repair it validated is recorded here and in SCRIPT_CORRECTIONS.md / CAMERA_DIRECTION_REPORT.md, and the surviving committed production `law11` was repaired with the same recipe and rendered to completion.

## What already works (verified, do not touch)

| Component | Evidence |
|---|---|
| Word timings | `voice/words.json` — 302 words energy-aligned from the real MP3, 0.1 s → 120.9 s; captions land on the spoken word |
| 41 plan gates | `film_plan.py check` = **0 FAIL / 4 WARN** (camera: speed median 1.82, speed p90 11.2, face-frames 97 %, caption-band heads 4.6 %) |
| Head-cut framing | 9.0 % of face frames (gate ≤ 13) — passes without edits |
| Story logic | sentences whose subject/action is on screen: 100 %; named nouns on screen at their word |
| Scene structure | 11 takes over 4 places (shop, home, home_door, shop2) with night/morning/day/golden light changes at the story turns |
| Captions | one Bangla word at a time, burned into frames, Noto Sans Bengali |
| Render pipeline | `render.mjs --frames` chunked render verified: 3,645/3,645 stills, mux 121.5 s H.264 + AAC |

## What was broken (all found by direct inspection, not assumption)

### CRITICAL
1. **Face-sprawl: the "cool" face (dark sunglasses) assigned to 49 acting acts** — on chacha, rafi, ma, helper, neighbor — for ordinary conversation beats. At medium/close range every idle character read as "sunglasses guy" (one of the user's named complaints: faces contradict narration).
2. **Set reading errors** (validated on the parallel rebuild, same root cause in kit): glass sweet jars rendering as pale gray boxes in dark light; wall "papers" in dark navy on cream (read as lit windows at night); dark-wood till unreadable in night inserts.

### HIGH
3. **Low door cameras:** door-set M/C stations at z 0.76–0.94 aimed up at 1.13 → the porch roof's underside filled half the frame (raycast-verified: `porch_roof` hit at 3.15–4.25 m across the upper frame).
4. **Insert rests cutting heads:** object inserts (till, boards) framed so nearby character heads crossed the frame edge — measured 95–100 % cut on those rests.
5. **Character blocked by furniture:** a partnership desk's near corner crossed the acting character's body in its own medium shot.

### MEDIUM
6. **Face-feature geometry** (fresh cast sheet, recipe preserved): kaka's silver specs drawn at `hy+8` (chin level, 26–42 px below every eye line); pashi's moustache at `hy+52` (below the mouth); rafi's quiff bottom edge at `hy-30` overlapping meme eyes at `hy-18..-34`.
7. **Night interiors lit only by cold moonlight** — no warm practical pools at lamp positions (Rick-style night = cold base + warm lamps).

### LOW
8. Camera too calm (speed median 1.82 vs ~4; p90 11.2 vs ~23) — style, not error.
9. 97 % of frames carry a face (world-led beats 3 % vs 25–40 % target).
10. Caption-band heads 4.6 % (target ≤ 3) — the short child character at the counter.

## Incomplete (was never finished anywhere)
- The parallel 10-take rebuild (7 original characters: kaka/rafi/bhagne/ma/pashi/tulu/khoddor, 5 custom sets) — config lost in recycle before final render; its validated repair recipe is preserved in the reports.
- Sound design: SFX/music folders are placeholders in the skill (`<YOUR_SFX_FOLDER>`); the film ships with narration only, captions burned in.

## What was actually repaired in the surviving production
- 41 `cool` → `standard` (calm), 8 `cool` (nephew) → `smug` (motivated: the nephew's smugness is the story point) — re-baked plan: **0 FAIL / 4 WARN**.
- Full re-render 3,645 frames at 540×960/30 fps, narration muxed, ffprobe-verified (121.5 s, video+audio streams).
- 16-beat visual verification of the final MP4 (every 7.6 s): no sunglasses faces, beats read, captions correct.

## What should remain unchanged
- The author's set designs (shop/home/door/shop2) and counter-forward compositions — his signature staging, gate-passing, and dressing (jars, sacks, sign, hanging packets) is present.
- All word timing, take structure, transitions, and the caption system.
- The 4 remaining WARNs are style deltas, documented in ANIMATION_QA_REPORT.md as accepted.
