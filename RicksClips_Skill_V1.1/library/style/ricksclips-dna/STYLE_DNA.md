# RicksClips3000 Style DNA — measured from the current viral shorts

Source: 7 uploads of @RicksClips3000 ("Ricks Clips"), verified via YouTube oEmbed,
downloaded 720x1280 mp4, every frame extracted at 30 fps and measured
(**12,761 frames**, per-video JSON in `data/metrics_*.json`, contact sheets in
`data/sheet_*.jpg`). Sampling date: 2026-11.

Videos analyzed (name | duration | cuts | cuts/min | median shot | lum | sat | warmth):

| video | s | cuts | cuts/min | med shot | lum | sat | warm |
|---|---|---|---|---|---|---|---|
| How Mine Salting Worked | 61.1 | 9 | 8.8 | 5.9 s | 100.9 | 0.495 | +56.7 |
| How One Cart Stopped an Entire Army | 66.9 | 1 | 0.9 | 33.4 s | 112.3 | 0.378 | +11.8 |
| The Instinct That Makes You Crash | 59.5 | 7 | 7.1 | 6.8 s | 112.4 | 0.268 | +9.4 |
| The Prisoner Who Tunneled Into a Bank | 55.3 | 1 | 1.1 | 27.7 s | 119.5 | 0.314 | +6.6 |
| Why Astronauts Can't Flush in Space | 61.2 | 7 | 6.9 | 2.9 s | 64.8 | 0.508 | −17.9 |
| Why Drivers Started Filming The Road | 62.3 | 8 | 7.7 | 5.9 s | 102.6 | 0.432 | −22.6 |
| Why Samurai Feared The Flying Thunder | 59.1 | 6 | 6.1 | 6.8 s | 79.2 | 0.349 | +5.6 |

## 1. Format constants (hard)

- Vertical 9:16, published 720x1280, authored 1080x1920 @ 30 fps.
- Duration band **55–67 s** (all seven inside it; plan for 1,650–2,000 frames).
- Everything animates: mean inter-frame motion never drops below 4.7/255 even on
  "still" shots — the camera always creeps. Dead-still reads as broken.

## 2. The two structural modes (this is the big finding)

The channel alternates between two film grammars. Pick one BEFORE boarding.

- **Mode A — one-shot journey** (2 of 7: "One Cart", "Prisoner").
  A single continuous take per act; 1–2 hard cuts in the whole film; median
  shot 27–33 s; the camera travels through the world like a documentary
  operator, resting on faces and following moving things (carts, trains,
  tunnelling). This is the mode the existing `film_plan.py` gates target
  ("cuts per 10 s <= 0.9").
- **Mode B — scene-cut story** (5 of 7). 6–9 cuts in the film (6.1–8.8/min),
  median shot 2.9–6.8 s; each scene is still an animated three.js set with
  travelling camera — cuts land on place/time jumps (interior → exterior,
  day → night, control room → space). Never a cut inside one set's action beat.

Both modes share the same sentence-level grammar: the camera rests on the
noun, travels on the verb, and the caption lands with the rest.

## 3. Colour and light (measured)

- Global luminance leans dark-mid: mean 98.8/255 (per film 64.8–119.5).
- Saturation moderate: 0.27–0.51 (mean 0.39) — never pastel-grey, never neon.
- **Warmth is the scene's identity**, not the film's: −22.6 (asphalt/night
  road) to +56.7 (torch-lit gold mine), film mean only +7.1. Each place owns a
  temperature; the story cuts between temperatures.
- Palette union (k=6 per film, quantised): dark neutrals dominate —
  `#202020` ~10%, `#404040` ~9%, `#c0c0c0` ~6.5%, `#000020` ~6.5%,
  `#606060` ~4%; accents are saturated scene colours — `#4080c0` (sky/void
  blue) ~2%, warm browns `#604020`/`#806020` (wood/torch/gold) ~3%.
- Light is diegetic: torch cones, lamp pools, emissive screens ("OFF COURSE",
  "NO FLUSHING TONIGHT"), sun shafts. Post vignettes stay out of the way.
- Mood (light/colour) shifts ≥ 12/min inside shots on the word — verified:
  every film re-grades on the story turn, not only at cuts.

## 4. Captions (measured)

- One word (or 1–3 short words) per beat, **synchronised to the voice**, a new
  word roughly every 0.5–1.0 s; the caption changes WITH the narration word.
- White heavy grotesque (bold sans, Montserrat ExtraBold class), lowercase,
  thin dark outline/shadow.
- Position: centred horizontally, **word centre ≈ 75 % frame height**
  (measured band 72–78 % at 720x1280; the 58–76 % band in the gates is the
  keep-clear zone for faces above it).
- Size: cap height ≈ 40 px at 720 wide ≈ **5.6 % of frame width**
  (≈ 60 px at 1080 wide); 1–3 words per line, never a full sentence.
- White pixel share inside the caption band averages 0.7–5.5 % — captions are
  loud but never block the action.

## 5. Character design (verified against all 7 films)

- White round/capsule head, flat white fill, **no outline on the head**;
  two black dot eyes; thick black eyebrows carry all emotion (angle = mood);
  tiny line mouth; anger reads as a red-tinted face.
- Limbs: thin black sticks with simple two-tone clothing/uniform so the ROLE
  reads at thumbnail size (astronaut suit colours, miner hats, samurai armour,
  top hat + moustache for the rich man, red robes for officials).
- Characters are 2D billboards living inside a 3D world — always facing the
  camera; walk cycles are simple; acting beats are pose/brow swaps on content
  words (the acting gate: ≥ 4 changes / 10 s).
- Heads are big: head width ≈ 0.25 × frame width on a whole-body rest.

## 6. World design

- Texture-mapped low-poly three.js sets: stone walls, tiled red roofs, cave
  walls, wooden rails, checkered floors, starfields, Earth-from-space cards.
- ≥ 4 places per film (measured 5–8 views of the world: same set at another
  light counts as a new place).
- **Diegetic signage carries the turn** — the joke or disaster is written on
  an in-world poster/screen ("NO FLUSHING TONIGHT", "OFF COURSE", "SURE THING
  MINE", "MILLIONAIRE DUE TO THE MORNING"). Build the sign into the set.
- Spectacle is literal and POV: arrows flying AT the camera, snow crystals
  hitting the lens, the tunnelling POV, the launch POV. At least one
  first-person thrill shot per film in the last third.
- Props are period/role-honest (shotgun, gold pan, mine cart, samurai banner,
  phone with "no GPS"). Humour lives in props and signs, not in deformation.

## 7. Story grammar (from the contact sheets)

1. **0–3 s hook**: hero + strange act on screen immediately, first caption on
   the first word (first face ≤ 1.5 s — matches the framing gate "Rick median 0.0").
2. **Establish**: walk the world with noun captions; camera introduces the
   machine/place while the hero stays in frame.
3. **Turn**: the diegetic sign/alarm flips the mood look (flash red / cold blue);
   faces react with brow acting.
4. **Payoff**: the literal visual of the claim (arrow storm, gold vein, frozen
   flush cloud) with a POV thrill shot; grade shifts to the place's own light.
5. **Outro/loop**: a closing line that lands back on the title claim.

## 8. Camera constants (cross-checked with `film_plan.py`)

The gates already carry Rick's measured camera numbers; this corpus confirms
them: rests ≥ 30 % of frames, rests 2.2–4.5 per 10 s, hold median ≥ 0.6 s,
one long travel 3–7 s, speed median ~4 px/f (p90 15–27), lens ≈ 24 mm,
no tilt while resting, roll p99 ≤ 1.1 deg/f, cuts/min ≤ 0.9 for Mode A.
Mode B relaxes ONLY the cut gate (see `tools/style_check.py`).

## 9. Audio

Voice-led, music-bed under narration, SFX hit on the action noun
(the toolkit's audio gates). The 2026-11 corpus could not be loudness-probed
in this sandbox (ffmpeg hangs on these mp4s) — treat loudness numbers in
`film_plan.py` as still authoritative.
