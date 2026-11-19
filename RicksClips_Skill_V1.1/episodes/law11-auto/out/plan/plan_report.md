# Plan check: ৪৮ শক্তির নিয়ম — নিয়ম ১১

Camera idea: **Level the camera to each subject**. Every set is generated from the story, so the floor plan is known: the cast stands on it in stage slots and each beat gets a 24 mm camera levelled to that subject's own height - whole body to show the world, medium to squeeze two people, place and object frames when the beat belongs to the room or the thing.

41 gates: 32 pass, 9 warn, 0 fail. 3661 frames, 122.0 s, 4 takes.

| | Gate | Value | Target | Fix |
|-|-|-|-|-|
| PASS | camera: at rest (< 2 px/f), % of frames | 82.6 | >= 30 (Rick median 32, range 6-58) |  |
| WARN | camera: rests per 10 s | 4.59 | 2.2-4.5, aim 3 (Rick 3.1, range 0.9-4.7; the plan reads about 1 higher than the picture). CB 2026-11-10: the scene decides, but the camera must flow like his | station hopping: merge neighbouring stations and let ONE move flow through them (follow the thing that moves, cross the set, rise over it) |
| PASS | camera: rest length median, s | 1.13 | >= 0.6 (Rick 0.62); one in ten >= 1.8 |  |
| WARN | camera: longest travel, s | 1.87 | 3-7 in a film of 30 s or more: at least one long flowing move (Rick's long travels: median 3.0, upper quarter 4.8-9.5; Railroads and Roller Coasters 4.7) | every move is a short hop: where the scene has something to follow (a train, a walk, a falling thing, a line of rails) let one move run 4-5 s (station key travel) |
| WARN | camera: speed median px/f | 1.76 | about 4 (Rick 4.1, middle half 2.5-6.1) | too calm: raise the creep on the rests, add a drift, or lengthen the travels |
| WARN | camera: speed p90 px/f | 10.3 | about 23 (Rick 23, range 9.8-33.8) | the travels crawl: cover more distance or take fewer frames (set travel on the station) |
| PASS | camera: dead still (reads under 0.3 px/f when measured), % of frames | 1.4 | <= 21, aim 9 (Rick 9.3, range 1-29) |  |
| WARN | camera: speed peak px/f | 74.6 | <= 60 outside planned whips | only passes and whips may exceed 40, for <= 10 f with motion blur |
| PASS | camera: cuts per 10 s | 0.25 | <= 0.9, aim 0.4 (Rick 0.4; CB: fewer cuts) |  |
| PASS | camera: tilt while resting, deg | 0.0 | level (<= 0.5); tilt only inside a move (Rick: 0 % of holds) |  |
| PASS | camera: roll rate peak deg/f | 0.0 | <= 1.1 (Rick p99 1.08) |  |
| PASS | camera: lens outside 16-55 mm on non-insert frames, % | 0.0 | wide and close: about 24 mm = 73 deg tall (Rick, measured); long lenses only for object inserts |  |
| PASS | camera: travels that swing the view over 120 deg | 0 | 0: lay the places along the travel direction so the camera never turns back |  |
| PASS | camera: word stations not at rest on their word | 0 | 0: key nouns land with the camera at rest, 0-6 f before the word (CB's rule) |  |
| PASS | framing: first face, s | 0.0 | <= 1.5 (Rick median 0.0) |  |
| PASS | framing: face on screen, first 5 s, % | 100.0 | >= 50 (Rick 55-63) |  |
| PASS | framing: face on screen, first 15 s, % | 100.0 | >= 50 (Rick 55-63) |  |
| PASS | framing: longest stretch without a face, s | 0.0 | <= 6 |  |
| WARN | framing: frames with a face, % | 100.0 | 45-68 (Rick 55, range 23-66): about a third of the film belongs to the world and the story object | a face is on screen almost all the time: give beats to the world (a towering wall, the machine, the vehicle, a view from the air) with the character tiny or absent |
| PASS | framing: head width / frame width, median | 0.24 | about 0.25 (Rick 0.25, range 0.16-0.52) |  |
| PASS | framing: head width / frame width, p90 | 0.4 | <= 0.55 |  |
| PASS | framing: whole-body rests: figure height / frame height, median | 0.41 | about 0.45 (his head width of 0.25 at puppet proportions) |  |
| PASS | framing: whole-body rests: feet height (0 = top), median | 0.8 | 0.80-0.95: feet near the bottom, at most a fifth of the frame is empty floor |  |
| PASS | framing: head centre height, median (0 = top) | 0.46 | 0.45 (Rick 0.39-0.51), above the caption band |  |
| PASS | framing: head centres inside the caption band, % of all heads on screen | 0.0 | <= 3 (Rick 2.7) |  |
| PASS | framing: face frames with the head cut by the edge, % | 5.0 | <= 13 (Rick 13) |  |
| PASS | framing: face frames where the whole body fits, % | 81.0 | >= 65 (Rick 68) |  |
| PASS | camera: at rest while a face is on screen, % | 83.0 | >= 40 (Rick 41): rest on faces, move on places and objects |  |
| PASS | framing: shot mix W/M/C/P/O, % of time | 60/30/0/10/0 | whole body 45, medium 20, close <= 7, place 15, object insert <= 15 (Rick) |  |
| WARN | framing: world-led frames (place + object framing), % of time | 10 | 25-40 (Rick: place 15 + object up to 15; his 3D films are about half world-led by eye) | let the world or the story object fill the frame and make the character tiny or leave them out for that beat; then go very close |
| WARN | framing: medium shots, % of time | 30 | about 20 (Rick): the middle size is the dull one | go wide with the whole body small in a big world, or go close; put something big and close behind the character |
| PASS | world: places in the film | 4 | >= 4, aim 5-8 at 55 s or more (Rick's 3D films: 5-8 places) |  |
| PASS | world: share of the film in its most used light, % | 33 | <= 75: 2-3 kinds of light per film (day, golden, morning, night, interior); the light changes at the turn of the story |  |
| WARN | framing: same framing on the same subject in a row (stations) | 4 | <= 3 | change the shot size, or put someone else in the picture |
| PASS | story: sentences whose subject or action is on screen, % | 100.0 | >= 90 (Rick 91) |  |
| PASS | story: named nouns not on screen within 0.5 s of their word | 0 | 0 |  |
| PASS | acting: pose or face changes per 10 s on screen | 20.0 | >= 4 (Rick 4.5 on one figure, range 3-7; this counts every figure on screen) |  |
| PASS | acting: longest fully frozen figure with a resting camera, s | 2.3 | <= 3 unless something else moves |  |
| PASS | acting: held props without a hand | 0 | 0: every held prop is attached to a hand on every frame |  |
| PASS | acting: effects per 10 s | 1.2 | 1-2, on the action noun or verb (Rick) |  |
| PASS | acting: mood (light / colour) changes per minute | 14.8 | >= 12, in-shot on the word (Rick 13.7, range 3.9-15.5) |  |
