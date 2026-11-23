# FINAL PRODUCTION REPORT — Law 11 (Bangla) · fresh2 corrected production

**Delivered film:** `episodes/law11-fresh2/out/animatic_10fps.mp4` — 120.7 s, 432×768 @ 10 fps,
H.264-compatible mpeg4 video + the user's Bangla narration, captions burned in. ffprobe-verified.
**Production:** `RicksClips_Skill_V1.1/episodes/law11-fresh2` — 7 original drawn characters,
5 original sets, 11 takes, 3,621 plan frames @ 30 fps.
**Plan gates:** **0 FAIL / 9 WARN** of 41 (all nine WARNs are documented style deltas in
ANIMATION_QA_REPORT.md — the same class the accepted `law11` production carries).

## What this production is

The third rebuild of the "original cast, original sets" Law 11 film. The first two were
lost in sandbox recycles before being committed; this one was committed and pushed at every
milestone (config 2fb65b3, render fixes cdad837/ffa4d51, this report set follows). Every
repair from the earlier sessions' validated recipe is baked into the source files:

- the 7-character cast sheet with all face-geometry fixes (specs on the eye line, moustache
  at the mouth, quiff clear of the eyes, sari/gown corrected, torso widths from shoulders);
- the 5 set modules with readable glass jars, brass till, dark-board/bright-paper boards,
  warm practicals, porch_roof eye-line discipline, tree/fence placement, fan off-axis;
- the film.json generator with computed cameras, audio-true anchors, exit/re-enter acts,
  acting idles, arc travels, fx/mood/sound cues, drawn transitions.

## Definition-of-done scorecard

| Requirement | status |
|---|---|
| Script communicates clearly | yes — 15/15 sentences verified on screen (story gate 100 %) |
| Scene direction matches the narration | yes — noun-on-word gate 0 violations; all beats checked on the MP4 |
| Characters act naturally | yes — motivated poses/faces on content words; longest freeze 2.1 s |
| Expressions match emotions | yes — meme faces chosen per line; the v1 sunglasses sprawl is gone |
| Camera supports storytelling | yes — computed framings, noun rests, arc travels, 0.83 cuts/10 s |
| Timing feels intentional | yes — word stations rest 0–6 f before their word (0 violations) |
| Transitions are coherent | yes — cuts only on the script's own jumps; 2 drawn transitions at time jumps |
| Audio synchronized | yes — 198 aligned words drive captions + mouths; single-container mux verified |
| Visual continuity maintained | yes — door motif night→morning→night; the red khata stays in the desk t9→t14 |
| Final video rendered and inspected | yes — 1,207/1,207 frames, ffprobe verified, 16-beat inspection, 2 defect beats repaired and re-inspected |
| Remaining errors documented honestly | yes — this report + the QA table |

## Before-and-after

- `download/law11-final/before-after-comparison.jpg` — the previously delivered `law11`
  production vs its repair pass (10 story beats).
- This production's own before/after is the repair trail in ANIMATION_QA_REPORT.md
  (A-1…A-10): ghost-cast wide → clean door scene; teleport travels → arc travels; jar-blocked
  close → readable medium; fan-cropped opening → clean counter wide. The durable artefacts
  are the committed plan files and the two inspection sheets made from the delivered MP4.

## Honest limitations (not hidden)

1. **Delivery rate:** the delivered animatic is 10 fps at 432×768. The full 30 fps / 540×960
   render needs ~8–10 h of CPU rendering in this sandbox; the plan and the resumable chunk
   script (`scripts/render_fresh2_full.sh`) are committed, so it is pure compute for the
   next session. Nothing authorial is missing.
2. **Sound design:** narration + cue sheet only; SFX/music files are placeholders in the
   skill. The cues (door knocks, coin box, paper turns, flash) are marked at their nouns.
3. **Bengali visemes** are approximated with the kit's Latin letter mapping (LOW).
4. **Verification is sampled:** all frames passed automated gates; the visual inspection used
   16 beats + targeted re-checks of every repaired beat class — not a manual frame-by-frame
   of the whole film. Stated as required by the directive.
5. The t4 warning scene keeps a WARN at 4.0 % caption-band heads (the kid characters' head
   height at the counter) — fixing it would break the counter staging that the story needs.

## Evidence index

- Docs (this set): PROJECT_AUDIT · SCRIPT_DIRECTION_ANALYSIS · SCRIPT_CORRECTIONS ·
  STORYBOARD_RECONSTRUCTION · CHARACTER_ANIMATION_REPORT · CAMERA_DIRECTION_REPORT ·
  TIMING_AND_CONTINUITY_REPORT · AUDIO_LIPSYNC_REPORT · ANIMATION_QA_REPORT ·
  VISUAL_STYLE_GUIDE · FINAL_PRODUCTION_REPORT (this file).
- Plan: `episodes/law11-fresh2/out/plan/{camera_baked,performance_baked,plan_report}.{json,md}`, `sound_events.json`.
- Film: `episodes/law11-fresh2/out/animatic_10fps.mp4` + `out/animatic_stills/` (1,207 stills).
- Generator: `episodes/law11-fresh2/build_film.py` (single source of film.json).
- Cast/set verification sheets and probe scripts: `/home/z/my-project/scripts/` (session side).
