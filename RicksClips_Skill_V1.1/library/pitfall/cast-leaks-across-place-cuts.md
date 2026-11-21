# Pitfall: cast leaks across place cuts — stale positions appear in the wrong set

**Priority:** HIGH (earned, law11-art, 2026-11-21)

## Symptom
A night shop wide shot showed a cut-off green sari and a bent dark arm hanging under the
counter edge — Ma (home position `[-0.85, 1.15]`) standing invisibly-in-plain-sight in the
SHOP set, 40+ seconds after her home scene. A systematic audit found worse: chacha leaked
428 frames into the padosi ending (a `flinch/deadInside` run that never ended), rafi stood
mid-room in his own home for 45 frames, the nephew materialised inside the night home for
25 frames, and t8 opened on a 3 s empty shop before a mid-travel pop-in cast arrival.

## Cause
Characters live in ONE world; a place change swaps the SET, not the cast. Any character
without an act at (or after) the place-cut frame keeps its previous position — which in the
new set can be inside furniture, in the customer zone, or mid-room. `enter/exit` acts placed
seconds after the cut leave leak windows; acts placed seconds BEFORE the cut leave 2-frame
teleport glitches in the old set. The 42 plan gates did NOT catch any of it: framing/story
gates read the plan's `shows` lists, not the actual rendered pixels.

## Fix
1. Bake the exact cut frames once (`camera_baked.json`: first frame where `place` changes).
2. Every `enter=True` and `exit=True` lands ON its cut frame (e.g. `act("ma", 30.67, exit=True)`).
3. Every character whose scene changes gets a fresh `pos` act at that same cut frame
   (rafi/chacha/nephew at the t5 cut, rafi at the t7 cut — not seconds later).
4. Characters who must not be in a set at all get parked hidden at their home spot:
   `act("ma", 0, pos=[-0.35, 0.85, 0], visible=False)`.
5. Long tail states need an explicit exit on the final cut of their arc
   (chacha's `deadInside` needed `act("chacha", 91.9, exit=True)`).

## Detect
Per place-cut, dump `visibility.json` and list every character on screen in the first ~1.5 s
after the cut who is not in that scene's story; plus a per-take on-screen frame count per
character (law11-art audit: `ma t5=307f, t7=221f, t8=313f` were all leaks). Scriptable in
~30 lines over `visibility.json` + the take table.

## Root cause
The plan layer reasons about characters per take, but the renderer reasons about ONE world;
nothing reconciles the two at place boundaries.

## Permanent rule
**Every place cut: a cast audit line.** Who is on stage in the new set from the first frame,
and which act puts each of them there or takes them out — at the cut frame, to the frame.

## Automation opportunity
`tools/qa/place_leak_check.py`: read baked visibility + a per-place cast table in film.json
(`"cast_by_place": {"shop_night": ["nephew","chacha"], ...}`), FAIL on any on-screen frame
outside the table.
