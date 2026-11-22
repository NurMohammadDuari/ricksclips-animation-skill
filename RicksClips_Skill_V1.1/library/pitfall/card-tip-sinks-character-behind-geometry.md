# Card tip sinks a character that stands behind furniture or near a wall

**Severity:** CRITICAL (the character silently VANISHES from the render; the plan gates all pass)

**Date:** 2026-11-22 (law11-s10 sweet-shop episode)

## Symptom

`film_plan.py check` reports every framing gate PASS (the plan projects the head correctly at frame centre), `render.mjs --export-lock` draws the character's card perfectly, `visibility.json` shows the character on screen — but the rendered frames show an empty spot. No page error, no warning.

## Cause

Every character card tips to the lens: `rotation.x = -atan2(camY - (pos.y + h*.55), hd)` (film.js draw loop). The tip pushes the card's TOP edge AWAY from the camera and its feet edge TOWARD the camera — roughly `0.13 m` each way at 2.3 m distance, more as the camera gets higher or closer. If a wall or a tall piece of furniture sits just behind the character, the tipped card's top half goes INSIDE that geometry and the z-buffer culls it:

- uncle at y 3.25 with the back wall face at y 3.325: card top pushed to ~3.38 → head culled by the wall.
- uncle at y 2.98 behind a 1.0 m counter with a HIGH camera (z 1.78): the bigger tip pushed the top into the counter's back edge and sliced the head at a diagonal.

The plan never models the card's tipped footprint, so no gate can catch it.

## Rule

Stage characters in the OPEN: keep `1.5 × (card tilt reach ≈ 0.6·tan(tip)) + 0.2 m` clear behind the character's position in every station that frames them — as a rule of thumb, **≥ 0.5 m from any wall face and never inside the footprint of furniture taller than 1 m** (counter, shelf, cupboard). The tip grows with camera height and closeness, so re-check the footprint for the CLOSEST and HIGHEST station that sees the character.

Shop staging that works (law11-s10): both actors beside/in front of the counter's ends in the open floor; the counter, price board, shelves and door are BACKDROP, never between a card and its lens. A shopkeeper "behind his counter" reads fine only when the camera stays low (near head height) and the character stands ≥ 0.15 m in front of the back wall — and even then expect a diagonal slice across the chest; prefer open staging.

## Fix protocol when it appears

1. Render one still at the failing frame with the character moved to mid-room: if they appear, it is occlusion geometry, not the character build.
2. Move the character forward in `acts[].pos` until the tipped footprint clears the occluder (check the tip reach against the closest/highest camera).
3. Re-run `film_plan.py check` after moving: framing gates (head width, feet height) shift with position.
