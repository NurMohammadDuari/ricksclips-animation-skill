# ANIMATION QA REPORT — Law 11 (corrected production)

Verification-first: an issue is marked fixed only after re-render + frame check. Automated sampling: plan gates (41) over all 3,645 frames + 16-beat visual sheet of the final MP4 + 10-beat before/after comparison. Per-frame manual inspection was NOT done for all 3,645 frames — the sampling used is stated per row.

| Issue ID | Scene | Problem | Severity | Correction | Verification |
|---|---|---|---|---|---|
| A-1 | all (49 acts) | `cool` sunglasses face on conversation/pleading/crying beats | CRITICAL | 41 → `standard`, 8 (nephew) → `smug` (film.json acts; plan re-baked) | re-bake 0 FAIL/4 WARN; final-video beats at 77 s/90 s/110 s show calm faces |
| A-2 | door M/C stations | porch-roof underside filled upper frame (low camera) | HIGH | 10 door stations raised to eye level (z 1.30–1.42) — recipe from raycast diagnosis (`porch_roof` hit 3.15–4.25 m) | parallel-rebuild probe f_02360 clean; recipe preserved |
| A-3 | till/board inserts | bystander heads cut at frame edges during noun rests | HIGH | straight-on noun centering recipe (S-2); surviving film measures 9.0 % edge-cut (gate ≤ 13) | gate value in plan_report.md |
| A-4 | t7 desk medium | desk corner crossed the actor's body | HIGH | camera raised above desktop (z 1.06) + viewpoint past the open end | probe f_02130 after fix |
| A-5 | night shop inserts | till/boards/jars unreadable in dark light | MEDIUM | brass till, dark-green boards + cream papers + red marks, translucent jars + lids, 2 warm PointLights per interior | probes f_0290/f_1210/f_3510 warm and readable |
| A-6 | fresh cast sheet | specs at chin (hy+8), moustache below mouth (hy+52), quiff over eyes (hy-30) | MEDIUM | geometry moved to eye line (hy-16), moustache hy+18, quiff bottom hy-52 | probe f_02590/f_1670/f_3280 correct |
| A-7 | door set field | place_kit trees in the walk lane (leaf discs across the door shots); fence across the doorstep | MEDIUM | central trees moved out, fence moved behind the house, porch PointLight added | probe f_02360: clean door, warm porch |
| A-8 | whole film | camera too calm (median 1.82 px/f, p90 11.2) | LOW | accepted — style delta, rest-led fable pacing; documented, not "fixed" | plan_report WARN rows |
| A-9 | whole film | 97 % face frames (world-led beats only 3 %) | LOW | accepted for this pass; recipe for world-led beats documented in CAMERA_DIRECTION_REPORT | plan_report WARN row |
| A-10 | shop2 counter | short child's head enters the caption band 4.6 % | LOW | accepted: raise-on-step recipe documented for next pass | plan_report WARN row |
| A-11 | t5 (f≈520) | oversized red costume/backpack prop reads oddly at wide | LOW | kept — author's prop design; flagged for the next art pass | final-video beat sheet frame 4 |
| A-12 | production loss | parallel rebuild law11-fresh2 lost in sandbox recycle (untracked) | CRITICAL (process) | surviving committed production repaired + rendered instead; full repair recipe committed in these reports; lesson: commit before render | this report + git history |

## Gate summary (final baked plan)
**0 FAIL / 4 WARN of 41** — the 4 WARNs are A-8/A-9/A-10 (style deltas) + rest-length/face-share family; none is a storytelling or rendering error.

## Render verification
- 3,645/3,645 stills present (f_00000–f_03644, no gaps — chunk logs + count).
- Mux: 540×960, 30 fps, H.264 + AAC, 121.5 s, 16.1 MB — ffprobe verified.
- Final-video beat sheet: 16 beats every 7.6 s inspected; no blank frames, no placeholder text, no repeated-take artifacts, captions present.
