# Camera / gate note - সোনার মাছ

Gate state: **RESULT: 0 FAIL, 1 WARN of 41 gates. Baked files and plan_report.md in /home/mint/Desktop/RicksClips/RicksClips_Skill_V1.1/episodes/golden-fish/out/plan**. 41 gates, 1 accepted WARN.

## Accepted warnings

| gate | value | target | why accepted |
|---|---|---|---|
| speed median px/f | 1.8 | about 4 (Rick 4.1, middle half 2.5-6.1) | within the skill's WARN band; the plan pass is kept and the episode stays editable |

## Camera idea

Every set is generated from the story, so the floor plan is known: the cast stands on it in stage slots and each beat gets a 24 mm camera levelled to that subject's own height - whole body to show the world, medium to squeeze two people, place and object frames when the beat belongs to the room or the thing.

Signature move: One long flowing move at the middle of the film, from the establishing framing into the turn.

## Re-bake after any edit

```bash
python tools/film_plan.py check episodes/golden-fish/film.json
```
Renders read the **baked** plan in `out/plan/`, never `film.json` directly.
