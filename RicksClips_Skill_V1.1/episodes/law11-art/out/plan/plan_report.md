# Plan check: ৪৮ শক্তির নিয়ম — নিয়ম ১১: খাতা যার, দোকান তার

Camera idea: **Who holds the khata holds the shop**. The credit ledger (বাকির খাতা) is the seat of power: Rafi writes it, the uncle hands it to the nephew, the nephew waves it at customers who only know Rafi, the uncle arrives at the door without it, and Rafi's own khata opens in the last shot. The camera travels toward hands and the book; on every power change the held thing comes toward the lens.

41 gates: 34 pass, 7 warn, 0 fail. 3640 frames, 121.3 s, 11 takes.

| | Gate | Value | Target | Fix |
|-|-|-|-|-|
| PASS | camera: at rest (< 2 px/f), % of frames | 76.6 | >= 30 (Rick median 32, range 6-58) |  |
| PASS | camera: rests per 10 s | 4.29 | 2.2-4.5, aim 3 (Rick 3.1, range 0.9-4.7; the plan reads about 1 higher than the picture). CB 2026-11-10: the scene decides, but the camera must flow like his |  |
| PASS | camera: rest length median, s | 1.43 | >= 0.6 (Rick 0.62); one in ten >= 1.8 |  |
| WARN | camera: longest travel, s | 1.77 | 3-7 in a film of 30 s or more: at least one long flowing move (Rick's long travels: median 3.0, upper quarter 4.8-9.5; Railroads and Roller Coasters 4.7) | every move is a short hop: where the scene has something to follow (a train, a walk, a falling thing, a line of rails) let one move run 4-5 s (station key travel) |
| WARN | camera: speed median px/f | 1.76 | about 4 (Rick 4.1, middle half 2.5-6.1) | too calm: raise the creep on the rests, add a drift, or lengthen the travels |
| WARN | camera: speed p90 px/f | 10.5 | about 23 (Rick 23, range 9.8-33.8) | the travels crawl: cover more distance or take fewer frames (set travel on the station) |
| PASS | camera: dead still (reads under 0.3 px/f when measured), % of frames | 3.2 | <= 21, aim 9 (Rick 9.3, range 1-29) |  |
| PASS | camera: speed peak px/f | 58.4 | <= 60 outside planned whips |  |
| PASS | camera: cuts per 10 s | 0.82 | <= 0.9, aim 0.4 (Rick 0.4; CB: fewer cuts) |  |
| PASS | camera: tilt while resting, deg | 0.0 | level (<= 0.5); tilt only inside a move (Rick: 0 % of holds) |  |
| PASS | camera: roll rate peak deg/f | 0.0 | <= 1.1 (Rick p99 1.08) |  |
| PASS | camera: lens outside 16-55 mm on non-insert frames, % | 0.0 | wide and close: about 24 mm = 73 deg tall (Rick, measured); long lenses only for object inserts |  |
| PASS | camera: travels that swing the view over 120 deg | 0 | 0: lay the places along the travel direction so the camera never turns back |  |
| PASS | camera: word stations not at rest on their word | 0 | 0: key nouns land with the camera at rest, 0-6 f before the word (CB's rule) |  |
| PASS | framing: first face, s | 0.0 | <= 1.5 (Rick median 0.0) |  |
| PASS | framing: face on screen, first 5 s, % | 100.0 | >= 50 (Rick 55-63) |  |
| PASS | framing: face on screen, first 15 s, % | 99.0 | >= 50 (Rick 55-63) |  |
| PASS | framing: longest stretch without a face, s | 0.6 | <= 6 |  |
| WARN | framing: frames with a face, % | 99.0 | 45-68 (Rick 55, range 23-66): about a third of the film belongs to the world and the story object | a face is on screen almost all the time: give beats to the world (a towering wall, the machine, the vehicle, a view from the air) with the character tiny or absent |
| PASS | framing: head width / frame width, median | 0.3 | about 0.25 (Rick 0.25, range 0.16-0.52) |  |
| PASS | framing: head width / frame width, p90 | 0.41 | <= 0.55 |  |
| PASS | framing: whole-body rests: figure height / frame height, median | 0.53 | about 0.45 (his head width of 0.25 at puppet proportions) |  |
| PASS | framing: whole-body rests: feet height (0 = top), median | 0.94 | 0.80-0.95: feet near the bottom, at most a fifth of the frame is empty floor |  |
| PASS | framing: head centre height, median (0 = top) | 0.5 | 0.45 (Rick 0.39-0.51), above the caption band |  |
| WARN | framing: head centres inside the caption band, % of all heads on screen | 4.1 | <= 3 (Rick 2.7) | a face sits under the caption (often the short character): re-aim, raise them on a step, or move them out of the 58-76 % band |
| PASS | framing: face frames with the head cut by the edge, % | 10.0 | <= 13 (Rick 13) |  |
| PASS | framing: face frames where the whole body fits, % | 78.0 | >= 65 (Rick 68) |  |
| PASS | camera: at rest while a face is on screen, % | 76.0 | >= 40 (Rick 41): rest on faces, move on places and objects |  |
| PASS | framing: shot mix W/M/C/P/O, % of time | 53/25/8/6/8 | whole body 45, medium 20, close <= 7, place 15, object insert <= 15 (Rick) |  |
| WARN | framing: world-led frames (place + object framing), % of time | 14 | 25-40 (Rick: place 15 + object up to 15; his 3D films are about half world-led by eye) | let the world or the story object fill the frame and make the character tiny or leave them out for that beat; then go very close |
| PASS | framing: medium shots, % of time | 25 | about 20 (Rick): the middle size is the dull one |  |
| PASS | world: places in the film | 7 | >= 4, aim 5-8 at 55 s or more (Rick's 3D films: 5-8 places) |  |
| PASS | world: share of the film in its most used light, % | 38 | <= 75: 2-3 kinds of light per film (day, golden, morning, night, interior); the light changes at the turn of the story |  |
| PASS | framing: same framing on the same subject in a row (stations) | 2 | <= 3 |  |
| PASS | story: sentences whose subject or action is on screen, % | 100.0 | >= 90 (Rick 91) |  |
| PASS | story: named nouns not on screen within 0.5 s of their word | 0 | 0 |  |
| PASS | acting: pose or face changes per 10 s on screen | 14.3 | >= 4 (Rick 4.5 on one figure, range 3-7; this counts every figure on screen) |  |
| WARN | acting: longest fully frozen figure with a resting camera, s | 3.4 | <= 3 unless something else moves | bepari: add a face change, or let the camera creep / another character act |
| PASS | acting: held props without a hand | 0 | 0: every held prop is attached to a hand on every frame |  |
| PASS | acting: effects per 10 s | 1.2 | 1-2, on the action noun or verb (Rick) |  |
| PASS | acting: mood (light / colour) changes per minute | 15.8 | >= 12, in-shot on the word (Rick 13.7, range 3.9-15.5) |  |
