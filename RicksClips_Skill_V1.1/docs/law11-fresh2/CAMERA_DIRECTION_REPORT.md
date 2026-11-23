# CAMERA DIRECTION & CINEMATOGRAPHY REPORT — Law 11 (fresh2)

## The idea (named in film.json `camera_idea`)

**"Rest on the noun, travel on the verb — computed, not guessed."** Every station camera is
solved from its subject's height and the framing target, so head widths, feet heights and
the caption band are true by construction. Travel happens between nouns; the camera rests
while the noun is spoken.

## The computed recipe (build_film.py `cam()`)

| framing | solved for | distance (adult 1.7 m) | measured on this film |
|---|---|---|---|
| W whole | figure 0.45 of frame height, feet 0.84, head centre 0.47 | 2.5 m | head width median 0.30, feet 0.83 |
| M medium | figure 0.62 | 1.83 m | — |
| C close | head width **0.52** of frame width (Rick's p90 0.54) | 1.27 m | head width p90 0.54 (gate ≤ 0.55) |
| O object | the anchor framed at 1.4 m, lens 40 | 1.4 m | inserts: board, till, desk, tarazu, tea table, sign |
| P place | the set at 5.07 m | 5.07 m | courtyard, shop interior, street |

All non-insert shots use the 24 mm wide (gate: lens outside 16–55 mm on non-inserts = 0 %).

## The courtyard rule (the porch_roof fix)

The house set has a real, low porch roof — the v1 bug had door cameras at z 0.76–0.94 aimed
up, so the roof's underside filled half the frame (raycast-verified). This rebuild: every
courtyard camera clamps its eye-line to **≥ 1.32 m, level** (no tilt while resting — gate
value 0.0°). The porch bulb hangs inside the frame instead of the roof slab.

## Movement grammar

- Cuts land ONLY on the script's place/time jumps: 11 takes = 10 cuts = **0.83 per 10 s**
  (gate ≤ 0.9). Inside a scene, one move carries the line and every noun beat rests.
- Word stations arrive at rest 5 frames before their word (gate: 0 violations).
- Travels arc: `add_take` measures every straight camera path against the place's body
  positions and adds a `via` arc only when the path would graze a character (the v1 bug
  passed 3 cm from standing heads); the arc swings toward the empty side, never through
  the cast.
- The accusation walk (t9) is one quiet wide — the camera holds while khoddor crosses to
  rafi, because the drama, not the camera, should move.
- No tilt while resting (0.0°), no roll (0.0°/f), no view swings over 120° (0 found).

## Shot mix (measured)

W 40 / M 22 / C 8 / P 15 / O 15 — whole-body ≥ 35 ✓, medium ≤ 28 ✓, close ≤ 10 ✓, object
≤ 15 ✓, world-led (P+O) 30 % (gate 22–45 ✓). The film gives a third of its time to the
world and the story objects — the board, the till, the desk, the tarazu, the sign.

## Shot-repeat discipline

Same framing on the same subject in a row: 2 (gate ≤ 3). The repeated door motif varies:
P → W → M → side C on visit 1; P → W → M → M → M → C on visit 2 — each visit ends closer
than the last, as the script's emotion escalates.
