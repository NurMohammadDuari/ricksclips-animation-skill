# Law 11 — hook (10s HQ rebuild)

**Episode:** `law11-hq10` · 2026-11-22 · 300 frames @ 30 fps · 720x1280 (published Shorts size)
**Rebuild reason:** the earlier 10s cuts (`law11-open-10s`, `law11-art-10s`) did not pass the CB RULES No.1 test against real @RicksClips3000 frames — flat untextured generic sets, occluded subjects, no warm diegetic light, weak captions. This episode is a full from-scratch rebuild of the same story hook with the measured DNA applied.

## What changed vs the old cuts (the diagnosis)

| old cut problem | hq10 fix |
|---|---|
| plain colour-mesh world, no texture | kit3d relief wood floor / plaster walls / tile counter + PBR brass trays, rail, coins, scale |
| no diegetic light | hanging lamp PointLight with bloom globe + window shaft + door spill + floor pool; lamp flicker in `update()` |
| subject occluded / half-buried | station table re-staged: chacha whole-body W shots at ~2.4 m, rafi M/CU with the glass dome moved off his axis |
| caption too small/thin | kit RICK captions (Arial 700, 3.9 % H at 71.5 %), word-by-word Bangla from the real narration timings |
| mood never re-grades | lamp re-grades cool during Rafi's disbelief line (s 4.05–7.5) and back warm — real light change, not the placeholder wash |

## Story (the hook, narration lines 1–2)

| # | s | line |
|---|------|------|
| 1 | 0.1–3.6 | কাল থেকে আর আসা লাগবে না, রাফি। আমার ভাগ্নে এখন সব পারে। (chacha fires Rafi, the nephew already owns the till) |
| 2 | 4.0–8.6 | চাচা, ১০ বছর... আপনার ভাগ্নেরে তো সব আমিই শিখাইলাম! (Rafi cannot believe it) |

## Cast

| character | puppet | rôle |
|---|---|---|
| `chacha` | `cast:bbqdad` | the uncle — declares the firing, points to the door |
| `rafi` | `cast:barista` | the hero — flinch → shrug → indignant point |
| `nephew` | `cast:backpack` | the kid already writing in the khata at HIS till |

## Camera (Mode A — one travelling take, 7 stations, 0 cuts)

W whole-body on chacha (0–3.5 s, push-in) → O insert on the till + "নতুন মালিক" tag (4.2–4.9 s) → P wide on the shop (5.35–5.9 s) → swerve M to rafi's face (6.4–7.9 s) → tighter M rest to the end. Lens 22–33 mm family, drifts 0.14–0.36 m/s on every rest, one 1.05 s swerve travel.

## Gates

`film_plan.py check`: **0 FAIL / 3 WARN of 41** (speed median 1.84 px/f WARN, feet-height WARN, caption-band heads WARN). Density on final frames: W 4/7, P 6/7, M 6/7 (G1 edge still below Rick's 0.14 median — the known look-pass gap, next round: contrast pass on the relief textures).

## Deliverable

`download/law11-hq10-10s.mp4` (10.0 s, 720x1280, real Bangla narration muxed from the Law 11 MP3 0–9.1 s).
