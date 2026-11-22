# CAMERA_NOTE — Law 11 (Bangla, 121.3 s)

Gate: `python tools/film_plan.py check episodes/law11/film.json`
Result: **0 FAIL, 4 WARN of 41 gates** (2026-11-18). Every WARN is deliberate and listed below.

## Accepted WARNs, with the reason

| gate | value | target | why it stays |
|---|---|---|---|
| camera · speed median | 1.82 px/f | ≈ 4 (Rick 4.1) | The film is 70 % interior dialogue comedy: rests carry the beats and the text. Motion is concentrated in the signature moves (the door arrivals, the counter crossings) instead of a constant drift. Judged by eye over the whole board; adding creep would make the quiet beats read as sliding. |
| camera · speed p90 | 11.5 px/f | ≈ 23 (Rick 23) | Same cause. The p90 is set by orbit turns between mid-gap stations; pushing it higher forced 120°-swing travels that broke the "who is behind the counter" geography. |
| framing · frames with a face | 97 % | 45–68 % | The story is a two-hander with a counter; faces ARE the film. Object/place frames exist (13 stations of 45) but each is short because the narration never leaves the characters for long. Cutting a face to hit the reference ratio made the board confusing in review. |
| framing · head centres in caption band | 4.6 % | ≤ 3 % | Only the kid nephew (1.35 m) at the counter-top camera; his face is fully readable above the caption, and the caption itself is one short Bangla word. |

All other 37 gates pass, including: head-cut-by-edge 12.6 % (≤ 13), whole-body fits 65 %+, longest travel 2.9 s, story nouns on screen, held props in hands, no interpenetration, shot mix W 23 / P 13 / M 6 / C 2 / O 1.

## Camera idea

**"The counter that changes hands."** The sweet-shop counter is the seat of power. Every era is told by WHO stands behind it:

- the uncle alone (t1), then Rafi behind it while the nephew learns (t3),
- Rafi driven to the neighbour's counter for half pay (t5, t7, t10),
- Rafi back behind a counter he partly owns (t12).

The camera crosses from the customer side to the owner side whenever the power moves, so the crossing itself is the story beat.

**Signature:** the home door. The uncle arrives through the same dark doorway three times — firing, scheming, begging — and the third arrival is staged from further away so his fall reads in the framing (t8, night).

## Hard-won camera rules for this set (keep for the next shop episode)

1. **Behind-counter = camera above counter-top.** Counter top is z = 1.0 m, front panel y = 1.11 m. Any camera in front of the counter at z ≤ 1.5 m cuts the subject at the chin/face. Use `pos z ≈ 1.75–1.9`, `aim z ≈ 1.30`.
2. **Close camera in front of the counter is a brown wall.** Even at the right height, y too close (< ~1.3 m from the front) fills the frame with the front panel. Pull back and use the 24 mm lens.
3. **Kid peek gag is the exception.** For the 1.35 m nephew the *only* readable framing from behind the counter is a low camera (z ≈ 1.05–1.3) that shows his cap top — used as a deliberate gag in t6, and he also stands on the customer side for his writing beat.
4. **Object inserts (O) of a prop on the counter** must aim down at the counter-top (aim z ≈ 1.05–1.1) from z ≈ 1.85; otherwise the counter hides the prop.
5. **Station arrival vs actor visibility.** An actor's `visible:true` must fire ≤ 0.15 s before the station that needs them, and `exit:true` after the camera leaves. Otherwise the START panel or the first rest frames show an empty set.
6. **Baked camera stations are sorted by arrival time, not by original list index.** In a take with an out-of-order `at` (this episode: t2, st4 at 27.7 s before st5 at 25.2 s) the baked index and the film.json index disagree. Map back before editing camera values.
7. **Screen-direction is not intuitive.** For far subjects, increasing `aim x` moves the subject screen-LEFT; near subjects can move the opposite way through parallax. Use the projection maths in `tools/film_plan.py` (or `/tmp` optimiser `law11_nudge_opt.py`) rather than guessing.

## Fixes made during review (all verified with stills)

- `light_shaft` in `sets/home.js` was an opaque `MeshBasicMaterial` and rendered as a white board — now `opacity: 0.16` and `flat()` supports `opacity`.
- 18 stations nudged by a brute-force aim-x / pos-x optimiser: head-cut frames 693 → ~137 (gate 33 % → 12.6 %).
- khata "O" inserts converted to "C" framing of Rafi writing (`shows: [khata, rafi, nephew]`) — the O framed brown counter walls; the C shows the face and the book.
- Nephew moved to the customer side for his t6 writing beat (a 1.35 m kid can never clear the counter from behind); his behind-counter shots read as a cap-peek gag.
- Timing patches: Rafi 31.3 → 31.15 (visibility), Rafi+neighbour 53.2 → 53.05, nephew 64.8 → 64.65, Rafi 69.8 → 69.65; t5 st0 travel 0.75; t9 st3 hold 1.15; t4 st0 at 48.45.

## Not done (needs the full plan / GPU)

- Blender look pass, 1080p final render (this animatic is 540×960 preview at `--scale 0.5`), colour grade, music/SFX mix, thumbnail + YouTube package.
