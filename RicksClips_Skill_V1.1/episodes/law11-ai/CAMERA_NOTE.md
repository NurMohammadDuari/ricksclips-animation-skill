# Camera / gate note - The 48 Laws Of Power: Law 11

Gate state: **RESULT: 1 FAIL, 8 WARN of 41 gates. Baked files and plan_report.md in /home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1/episodes/law11-ai/out/plan**. 41 gates, 8 accepted WARN.

## Accepted warnings

| gate | value | target | why accepted |
|---|---|---|---|
| rests per 10 s | 4.63 | 2.2-4.5, aim 3 (Rick 3.1, range 0.9-4.7; the plan reads about 1 higher than the picture). CB 2026-11-10: the scene decides, but the camera must flow like his | within the skill's WARN band; the plan pass is kept and the episode stays editable |
| longest travel, s | 1.87 | 3-7 in a film of 30 s or more: at least one long flowing move (Rick's long travels: median 3.0, upper quarter 4.8-9.5; Railroads and Roller Coasters 4.7) | within the skill's WARN band; the plan pass is kept and the episode stays editable |
| speed median px/f | 1.76 | about 4 (Rick 4.1, middle half 2.5-6.1) | within the skill's WARN band; the plan pass is kept and the episode stays editable |
| speed p90 px/f | 10.3 | about 23 (Rick 23, range 9.8-33.8) | within the skill's WARN band; the plan pass is kept and the episode stays editable |
| frames with a face, % | 100.0 | 45-68 (Rick 55, range 23-66): about a third of the film belongs to the world and the story object | within the skill's WARN band; the plan pass is kept and the episode stays editable |
| world-led frames (place + object framing), % of time | 10 | 25-40 (Rick: place 15 + object up to 15; his 3D films are about half world-led by eye) | within the skill's WARN band; the plan pass is kept and the episode stays editable |
| medium shots, % of time | 31 | about 20 (Rick): the middle size is the dull one | within the skill's WARN band; the plan pass is kept and the episode stays editable |
| same framing on the same subject in a row (stations) | 4 | <= 3 | within the skill's WARN band; the plan pass is kept and the episode stays editable |

## Audio analysis

- duration: 121.30 s; word times: waveform RMS; 32 speech pockets.
- loud words drive the kicks, glints and light changes; the rest stay level.

## Camera idea

Every set is generated from the story, so the floor plan is known: the cast stands on it in stage slots and each beat gets a 24 mm camera levelled to that subject's own height - whole body to show the world, medium to squeeze two people, place and object frames when the beat belongs to the room or the thing.

Signature move: One long flowing move at the middle of the film, from the establishing framing into the turn.

## Re-bake after any edit

```bash
python tools/film_plan.py check episodes/law11-ai/film.json
```
Renders read the **baked** plan in `out/plan/`, never `film.json` directly.
