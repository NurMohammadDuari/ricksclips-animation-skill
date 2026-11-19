# Plan check: ৪৮ শক্তির নিয়ম — নিয়ম ১১ (বাংলা): কাজ সবাইকে শেখান, জায়গা কাউকে না

Camera idea: **The counter that changes hands**. The sweet-shop counter is the seat of power, so every era of the story is told by WHO stands behind it: the uncle alone, Rafi behind it while the nephew learns in front, Rafi driven to the neighbour's counter for half pay, and finally Rafi back behind a counter he partly owns. The camera crosses from the customer side to the owner side whenever the power moves.

41 gates: 37 pass, 4 warn, 0 fail. 3645 frames, 121.5 s, 11 takes.

| | Gate | Value | Target | Fix |
|-|-|-|-|-|
| PASS | camera: at rest (< 2 px/f), % of frames | 72.4 | >= 30 (Rick median 32, range 6-58) |  |
| PASS | camera: rests per 10 s | 3.95 | 2.2-4.5, aim 3 (Rick 3.1, range 0.9-4.7; the plan reads about 1 higher than the picture). CB 2026-11-10: the scene decides, but the camera must flow like his |  |
| PASS | camera: rest length median, s | 1.55 | >= 0.6 (Rick 0.62); one in ten >= 1.8 |  |
| PASS | camera: longest travel, s | 3.03 | 3-7 in a film of 30 s or more: at least one long flowing move (Rick's long travels: median 3.0, upper quarter 4.8-9.5; Railroads and Roller Coasters 4.7) |  |
| WARN | camera: speed median px/f | 1.82 | about 4 (Rick 4.1, middle half 2.5-6.1) | too calm: raise the creep on the rests, add a drift, or lengthen the travels |
| WARN | camera: speed p90 px/f | 11.2 | about 23 (Rick 23, range 9.8-33.8) | the travels crawl: cover more distance or take fewer frames (set travel on the station) |
| PASS | camera: dead still (reads under 0.3 px/f when measured), % of frames | 11.7 | <= 21, aim 9 (Rick 9.3, range 1-29) |  |
| PASS | camera: speed peak px/f | 40.2 | <= 60 outside planned whips |  |
| PASS | camera: cuts per 10 s | 0.82 | <= 0.9, aim 0.4 (Rick 0.4; CB: fewer cuts) |  |
| PASS | camera: tilt while resting, deg | 0.0 | level (<= 0.5); tilt only inside a move (Rick: 0 % of holds) |  |
| PASS | camera: roll rate peak deg/f | 0.0 | <= 1.1 (Rick p99 1.08) |  |
| PASS | camera: lens outside 16-55 mm on non-insert frames, % | 0.0 | wide and close: about 24 mm = 73 deg tall (Rick, measured); long lenses only for object inserts |  |
| PASS | camera: travels that swing the view over 120 deg | 0 | 0: lay the places along the travel direction so the camera never turns back |  |
| PASS | camera: word stations not at rest on their word | 0 | 0: key nouns land with the camera at rest, 0-6 f before the word (CB's rule) |  |
| PASS | framing: first face, s | 0.0 | <= 1.5 (Rick median 0.0) |  |
| PASS | framing: face on screen, first 5 s, % | 100.0 | >= 50 (Rick 55-63) |  |
| PASS | framing: face on screen, first 15 s, % | 93.0 | >= 50 (Rick 55-63) |  |
| PASS | framing: longest stretch without a face, s | 1.0 | <= 6 |  |
| WARN | framing: frames with a face, % | 97.0 | 45-68 (Rick 55, range 23-66): about a third of the film belongs to the world and the story object | a face is on screen almost all the time: give beats to the world (a towering wall, the machine, the vehicle, a view from the air) with the character tiny or absent |
| PASS | framing: head width / frame width, median | 0.32 | about 0.25 (Rick 0.25, range 0.16-0.52) |  |
| PASS | framing: head width / frame width, p90 | 0.51 | <= 0.55 |  |
| PASS | framing: whole-body rests: figure height / frame height, median | 0.46 | about 0.45 (his head width of 0.25 at puppet proportions) |  |
| PASS | framing: whole-body rests: feet height (0 = top), median | 0.86 | 0.80-0.95: feet near the bottom, at most a fifth of the frame is empty floor |  |
| PASS | framing: head centre height, median (0 = top) | 0.49 | 0.45 (Rick 0.39-0.51), above the caption band |  |
| WARN | framing: head centres inside the caption band, % of all heads on screen | 4.6 | <= 3 (Rick 2.7) | a face sits under the caption (often the short character): re-aim, raise them on a step, or move them out of the 58-76 % band |
| PASS | framing: face frames with the head cut by the edge, % | 9.0 | <= 13 (Rick 13) |  |
| PASS | framing: face frames where the whole body fits, % | 73.0 | >= 65 (Rick 68) |  |
| PASS | camera: at rest while a face is on screen, % | 72.0 | >= 40 (Rick 41): rest on faces, move on places and objects |  |
| PASS | framing: shot mix W/M/C/P/O, % of time | 55/11/6/26/1 | whole body 45, medium 20, close <= 7, place 15, object insert <= 15 (Rick) |  |
| PASS | framing: world-led frames (place + object framing), % of time | 28 | 25-40 (Rick: place 15 + object up to 15; his 3D films are about half world-led by eye) |  |
| PASS | framing: medium shots, % of time | 11 | about 20 (Rick): the middle size is the dull one |  |
| PASS | world: places in the film | 4 | >= 4, aim 5-8 at 55 s or more (Rick's 3D films: 5-8 places) |  |
| PASS | world: share of the film in its most used light, % | 38 | <= 75: 2-3 kinds of light per film (day, golden, morning, night, interior); the light changes at the turn of the story |  |
| PASS | framing: same framing on the same subject in a row (stations) | 3 | <= 3 |  |
| PASS | story: sentences whose subject or action is on screen, % | 100.0 | >= 90 (Rick 91) |  |
| PASS | story: named nouns not on screen within 0.5 s of their word | 0 | 0 |  |
| PASS | acting: pose or face changes per 10 s on screen | 13.5 | >= 4 (Rick 4.5 on one figure, range 3-7; this counts every figure on screen) |  |
| PASS | acting: longest fully frozen figure with a resting camera, s | 2.3 | <= 3 unless something else moves |  |
| PASS | acting: held props without a hand | 0 | 0: every held prop is attached to a hand on every frame |  |
| PASS | acting: effects per 10 s | 1.6 | 1-2, on the action noun or verb (Rick) |  |
| PASS | acting: mood (light / colour) changes per minute | 16.8 | >= 12, in-shot on the word (Rick 13.7, range 3.9-15.5) |  |
