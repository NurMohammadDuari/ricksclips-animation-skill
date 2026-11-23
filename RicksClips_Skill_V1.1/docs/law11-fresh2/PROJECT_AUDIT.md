# PROJECT AUDIT — Law 11 (Bangla) · `law11-fresh2` rebuilt production

**Date:** 2026-11-23 · **Production:** `RicksClips_Skill_V1.1/episodes/law11-fresh2` (7 original characters, 5 original sets, 11 takes, 3,621 frames @ 30 fps = 120.7 s)
**Source audio:** `voice/voice.mp3` (the user's own narration, 121.3 s) · **Word timings:** `voice/words.json` — 198 energy-aligned words (tools/audio_probe.py)
**Delivered animatic:** `out/animatic_10fps.mp4` — 120.7 s, 432×768 @ 10 fps, narration muxed, ffprobe-verified

## Context: why this production was rebuilt twice

The first `law11-fresh2` build (2026-11-22) was lost in a sandbox recycle before it was committed; a second rebuild met the same fate. This third rebuild was executed under one rule: **commit and push at every milestone** (config pushed at 2fb65b3, render fixes at cdad837/ffa4d51, before rendering began). Nothing in this audit is reconstructed from memory — every fact was re-derived from the files on disk.

## What already works (verified, do not touch)

| Component | Evidence |
|---|---|
| Word timings | 198 words, 0.04–120.1 s, aligned from the real MP3; sentence spans re-derived from the audio (the old design map's times were stale and were replaced) |
| 41 plan gates | `film_plan.py check` = **0 FAIL / 9 WARN** (re-verified after every repair; the 9 WARNs are the documented style deltas listed in ANIMATION_QA_REPORT.md) |
| 7 original characters | cast sheet verified in chromium: every signature reads (taqi cap + on-eye-line specs, backwards cap, Karaila topi + mouth-level moustache, quiff clear of the eyes, sari + bindi + bun, tufts, comb-back) |
| 5 original sets | dokan / basha_door / bhitore / pasher / rasta — all five render with their story furniture and anchors |
| Story gates | sentences shown 100 %, named nouns on screen at their word = 0 violations |
| Render pipeline | 1,207 animatic stills (every 3rd frame), mux verified with ffprobe, 16-beat visual inspection |

## What was broken and how it was found (all by direct inspection)

1. **CRITICAL — take boundaries used a stale timing map.** The survived design map's sentence times did not match the real audio (the narration reads slower). Every sentence span was re-derived from `words.json` and all take boundaries retimed.
2. **CRITICAL — word anchors were written as word indices** (interpreted as frame numbers), scrambling the take order. Fixed with sentence-relative token anchors using real audio times.
3. **CRITICAL — characters never exited**: after a take boundary the previous scene's cast stayed visible at their old positions (a 46 s stretch showed ghost heads inside object inserts, some 35× frame width). Fixed with exit/re-enter acts at every cut.
4. **HIGH — camera paths crossed the cast**: travels passed within 3 cm of standing heads. Fixed with segment-to-body distance checks that add arc `via` points only when a path grazes a body.
5. **HIGH — the `C` (close) framing was solved against head height, not head width**, putting lenses 0.77 m from faces (head width 0.86 of frame). Re-solved to Rick's p90 (0.52 of frame width).
6. **HIGH — colliding word beats**: pairs of word stations <1.1 s apart (চোর/মাল, খাতা/খদ্দের, বাবা/মালিকের, আমিই/ভাগ্নেরে) forced teleport-speed travels. Merged or respaced; the মাল→কাছে accusation+payoff now plays inside one quiet wide.
7. **MEDIUM — rig contract mismatches**: act `face` values must be strings (set-local names), `hat` hooks must return arrays on side views, `enter` only works on a character's first act (later re-entries need `visible: true`), episode sets import place_kit via `../../kit/sets/place_kit.js`. All found by rendering and fixed.
8. **MEDIUM — visual defects found in the rendered output itself**: ceiling-fan blades cropping the opening frame; the কথা close-up sliding into a glass jar. Both re-rendered from the corrected plan.

## What was intentionally kept

- The committed `law11` production and its 11 directive reports (this rebuild is a separate corrected production, exactly as the directive requires).
- The kit's locked renderer, camera maths, caption system and gate definitions — no kit file was modified.
- The 9 remaining WARNs (style deltas, not errors) — listed honestly in ANIMATION_QA_REPORT.md.

## Honest limitation

The 30 fps full-resolution render (3,621 frames at 540×960) needs roughly 8–10 hours of CPU rendering in this sandbox. This session delivered the complete film at 10 fps (every 3rd frame, 432×768) — a genuine watchable animatic, verified — while the resumable 30 fps render script (`scripts/render_fresh2_full.sh`, chunk 0–9) and the committed, gate-clean plan make the full-rate render a pure compute step for the next session.
