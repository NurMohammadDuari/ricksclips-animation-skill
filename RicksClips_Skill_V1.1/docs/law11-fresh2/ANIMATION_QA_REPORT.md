# ANIMATION QA REPORT — Law 11 (fresh2)

**Date:** 2026-11-23 · **Scope:** the rebuilt `law11-fresh2` production (11 takes, 52 stations,
217 acts, 3,621 plan frames; delivered animatic 1,207 frames @ 10 fps).

## Automated gates (tools/film_plan.py check — 41 gates)

**Result: 0 FAIL / 9 WARN** (re-run after every repair; nothing below is claimed without the
gate output in `out/plan/plan_report.md`).

The 9 WARNs, all documented style deltas (not errors):

| # | gate | value | target | disposition |
|---|---|---|---|---|
| 1 | camera: at rest, % frames | 63.9 | ≥ 30 | pass band, near the top — the film rests on its nouns by design |
| 2 | rests per 10 s | 4.42 | 2.2–4.5 | at the top of Rick's band; CB 2026-11-10: the scene decides |
| 3 | longest travel | 2.1 s | 3–7 | the script's scenes are short; the longest flow (t13 street) runs 2.0 s |
| 4 | speed median | 1.9 px/f | ≈ 4 | calm camera; same delta the accepted `law11` production carries |
| 5 | dead still % | 11.6 | ≤ 21 | within band |
| 6 | frames with a face | 87 % | 45–68 | face-led film; the P/O beats (30 % world-led) reduce it as far as the story allows |
| 7 | head centres in caption band | 4.0 % | ≤ 3 | the two kid characters at frame edges; re-aiming would break the staging |
| 8 | world-led | 30 % | 25–40 | within band (WARN flag is the upper bound check) |
| 9 | medium shots | 22 % | ≈ 20 | within band |

## Issue table (every repair this session, verified)

| Issue ID | Scene | Problem | Severity | Correction | Verification |
|---|---|---|---|---|---|
| A-1 | all takes | take boundaries built on a stale timing map (scenes at wrong words) | CRITICAL | sentence spans re-derived from words.json; all 11 boundaries retimed | word-rest gate 0; noun gate 0; beat inspection |
| A-2 | all takes | word anchors written as word indices → take order scrambled | CRITICAL | sentence-relative token anchors with real audio times | camera_segments order verified t1→t14 |
| A-3 | t3–t14 | characters never exited; ghost cast polluted other scenes (46 s no-face stretch, 35× heads) | CRITICAL | exit acts at every cut + `visible: true` re-entries | no-face gap gate ≤ 6 s: PASS (0.5 s) |
| A-4 | t3, t4, t9 | travels crossed the cast (heads at 3 cm from lens; peak 192 px/f) | HIGH | segment-to-body via arcs; front approaches instead of lateral sweeps | peak gate 55 px/f ≤ 60: PASS |
| A-5 | all C shots | close framing solved on head height → 0.77 m lenses, head width 0.86 | HIGH | re-solved to head width 0.52 (d = 1.27 m) | head width p90 0.54 ≤ 0.55: PASS |
| A-6 | t1, t4, t5, t9 | word-beat pairs < 1.1 s apart → teleport travels | HIGH | merged/respaced (t9 drama plays in one wide; t4 laugh beat merged) | peak gate: PASS; word-rest: PASS |
| A-7 | t5 | কথা matched its FIRST occurrence (মায়ের কথা @40 s) instead of সেই কথা @50 s | HIGH | S_ occurrence parameter; n=2 for কথা | station frame = 1512 = 50.4 s ✓ |
| A-8 | rig | act faces as arrays crashed kitFace; hat hooks broke on side views; `enter` ignored after first act; wrong place_kit import path | HIGH | faces → set-local strings; hats return arrays; re-entries via `visible`; import fixed | full render completed, 1207/1207 frames |
| A-9 | t1, t5 | fan blades cropped the opening frame; কথা close slid into a glass jar | MEDIUM | fan moved to x 2.3; কথা → M with creep hold | re-rendered frames inspected in the final MP4 |
| A-10 | all | frozen figures > 3 s while the camera rests | MEDIUM | acting idles (face alternation every ~2.3 s) | frozen gate 2.1 s ≤ 3: PASS |

## Frame-level verification of the delivered video

- 1,207/1,207 animatic frames present (automated count, 0 missing).
- ffprobe: 120.7 s, mpeg4 video + mp3 audio, no stream errors.
- 16-beat contact sheet (every ~7.5 s) inspected visually; 2 defect beats (A-9) repaired and
  re-inspected after the fix.
- Disclosure: this is automated-gate + sampled-beat verification, NOT a manual frame-by-frame
  of all 1,207 delivered frames.
