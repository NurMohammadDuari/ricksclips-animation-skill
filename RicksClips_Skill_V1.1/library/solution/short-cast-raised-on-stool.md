# Solution: a short cast member behind a counter reads only when raised on a stool

**Earned:** law11-art t8 night wides, 2026-11-21.

## What
The nephew (a kid, card height ≈1.45 m) stood behind the 1.0 m counter at `z=0`. In M shots
(~1.9 m camera) his eyes read; in W shots (2.9–3.3 m, lens 24) his head centre projected at
`head_y ≈ 0.51` — exactly the counter's top-edge line — so the shop showed a headless counter
while `visibility.json` happily reported him on screen. The gates passed; the STORY didn't.

## Fix (three moves)
1. Put a real stool in the set under his spot (`box('stool_kid', …, [.3, 1.9, 0], h .5)`)
   and raise the act to it (`pos z 0 → 0.5`) — his head clears the counter and the jars and
   reads against the lit wall. Bonus: a kid on a stool IS the story (filling too-big shoes).
2. Aim the night W stations at his eyeline (`aim z 1.35–1.4`) so his head sits at
   `head_y ≈ 0.44`, above the caption band, not under it.
3. Nudge the night `ai/si` up (1.4 → 1.62) so the card separates from the dark wall boxes.

## Why it works
`visibility.json` measures the card's projected box, not its readability; a half-occluded
short character behind hero furniture passes every gate while carrying zero emotion. Raising
the figure restores the head-vs-counter-edge margin that the reference relies on
(head centre ~0.45 of frame height, well above the counter edge in every shopkeeper shot).

## Reusable pattern
Any cast member shorter than the furniture they work behind: stool/step/crate under the
mark, act raised to the seat height, W aims at their eyeline. Check the Detect below after
every re-stage.

## Detect
For every station whose `subject` is a character, assert
`visibility[f].head_y < counter_edge_y - 0.05` in the baked frames — i.e. the head centre
clears the occluder's top edge by 5 % of frame height or more.
