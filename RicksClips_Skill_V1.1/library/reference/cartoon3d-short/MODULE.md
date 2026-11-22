# cartoon3d-short — vendored reference (upstream: mromidev/claude-animated-shorts)

- **Upstream:** https://github.com/mromidev/claude-animated-shorts (skill name `cartoon-3d-short`)
- **Snapshot:** upstream commit `e3b817b` "Add 20 reference contact sheets (1,200 frames)", 2026-11-01. Repo has exactly 2 commits (one-shot publish); all later activity lives in 13 PRs + 11 issues (analysed below).
- **Popularity at snapshot time:** 4,503 stars / 935 forks / 21 open items. Featured in third-party creator guides.
- **License:** MIT (code + docs). The `references/frames/` + `references/sheets/` JPEGs are upstream's private style study of *their* reference channel — study only, never publish them, never copy their characters/shots (upstream rule, we honour it).
- **Provenance chain:** our library already carried `[adopted]` notes "taken from CB's production library (claude-animated-shorts)" (see `library/README.md` and the INDEX "Also binding" gotcha line). This vendor completes the chain: the full source those notes came from is now in-tree.

## What it is (one paragraph)

A complete, proven Claude skill that produces **55–70 s vertical animated story shorts in the "2D characters in a 3D world" genre** — the same genre as our @RicksClips3000 DNA, but measured on a *different reference channel* (peach superellipse heads with plum ink outlines, bean bodies, saturated painted 3D town; not RicksClips' white capsule heads). The proven film: **"The Bridge That Fell for a Song"** (67 s, 1831 Broughton bridge resonance disaster, 74 marching soldiers). Stack: **Remotion + @remotion/three + postprocessing** compositing over **three.js**, Canvas2D-drawn character billboards, procedural painted textures, a fully synthesized numpy/scipy soundtrack, and frame-exact QA tooling. The repo's biggest asset is not the code — it is the **method**: measure the reference with numbers, split the look into 5 owned sandboxes, merge, verify with a fresh reviewer, repeat 4 rounds until scores go 5/3/4/5/4/7/4/6 → 7/5-6/6/5-6/7/6-7/6-7.

## Repo anatomy

| Path | Content | Size |
|---|---|---|
| `SKILL.md` | The full pipeline (11 steps), final look values, look-match loop, gotchas, readability traps | 15 KB |
| `references/STYLE_BIBLE.md` | Script formula + picture/camera/effects formula from 20 reference shorts | 4 KB |
| `references/reports/*.md` | 7 measured reports + shared brief (4,359 lines): motion (32,337 frames), depth (539 frames), textures (978 lines), characters (38 head fits), lighting (67 study frames), outlines (66 edge scans), grade — each with scripts + data + crops | 296 KB |
| `references/frames/` | 38 full-size reference frames 540x960 | 2.2 MB |
| `references/sheets/` | 20 contact sheets, 60 frames each (1,200 frames @ 30 fps) | 16 MB |
| `templates/bridge/*.ts` | World/story/characters/post source of the proven short (13 files, 4,783 lines): `story.ts` (shots, physics, camera keys, kicks, DOF table, foreground props), `world.ts` (sky/fog/river/town posing), `build.ts` (merged batches, Kenney CC0 kit, sight-line culler), `paint.ts` (procedural Canvas2D textures), `lights.ts` (day/golden presets, camera-relative sun), `shade.ts` (two-tone world lighting via lights_fragment_begin patch), `toon.ts` (900-line character drawing API, 600x1000 design space), `cast.ts` (canvas-pool billboards, crowds, fx cards), `cardshade.ts` (scene-lit cards), `ink.ts` (world ink outline pass), `lensblur.ts` (thin-lens DOF, 2-pass Vogel disc), `grade.ts` (6-knot tone curve + split-tone + vignette), `Bridge.tsx` (composer: ink → lens pre → lens main → bloom → NEUTRAL tone map → grade, MSAA 4) | 540 KB |
| `templates/audio/*.py` | Synthesized soundtrack kit (7 files, 2,471 lines): `timeline.py` (picture mirrored into Python), `sfx.py` (cue list, SFX_DB −6), `sfx_gen.py` (570 lines of numpy SFX synthesis), `music.py` (original march, score follows picture sections), `instruments.py` (additive/modal synth instruments), `dsp.py` (filters, reverb IRs, BS.1770-4 loudness, WAV I/O), `mix.py` (ducking, −15 LUFS master, look-ahead limiter), `cues.md` (cue sheet) | — |
| `templates/scripts/` (180 lines) | `bridge-stills.mjs` (still renders via Remotion), `sbs_sheet.py` (side-by-side vs reference), `bridge_merge.py` (sandbox merge by owned files), `bridge_shots.py` (shots.json extractor), `short_qa.py` (per-frame QA) | — |

## The corrected camera grammar (the single most valuable finding)

`STYLE_BIBLE.md` claimed the reference camera moves in **ease-out bursts** (peak speed on frame 1, decay ~8–10 f). The dedicated `reports/motion.md` study later **proved the bible wrong**: integer phase correlation cannot see motion below ~4 px/f, which faked the burst shape. Re-measured with 9-tile sub-pixel phase correlation (32,337 frames):

- Moves are **symmetric ease-in-out (smootherstep) glides, ~23 f total, ~10 f in / ~10 f out**, median peak **14–16 px/f @720p** (25 px/f cap).
- 65 % of frames move; **every hold creeps** 0.14–0.35 %/f (0.6 %/f ~35 f on punch words). No static hold ≥ 4 f — flat holds read as freezes in QA.
- **No hand-held float.** Impacts are **7-frame kicks that flip sign every frame** (±3 px @720p per unit, decay (1−n/7)^1.5, ±0.23° roll per unit) — see `kickAt()` in `story.ts`.
- Hard cuts only on big reframes (≥ ~half a frame width or 40 % zoom); everything else glides; glides are **centred on the old key frame** (key frame = move mid-point, so a glide key starts dur/2 earlier than the beat).
- Rolls 4–8° over ≥ 18 f; camera height median 0.79 × character height (82 % eye level).

**Method lesson (this is the permanent rule):** a measurement method with a blind spot writes fiction into the style bible. Any camera-grammar claim made from integer-pixel frame differencing must be re-validated sub-pixel before it becomes a gate. Our `film_plan.py` speed numbers (median ~4 px/f, p90 15–27) live in the same risk class — cross-check with the glide model before hard-gating.

## Cross-validation vs our ricksclips-dna (two channels, one genre)

| Dimension | @RicksClips3000 (our DNA, 7 shorts) | their reference channel (20 shorts) | Read |
|---|---|---|---|
| Duration | 55–67 s | 31–78 s, median ~60 s | same band |
| Voice rate | ~2.8 wps (law11 build) | 3.5–4.1 wps (median 3.7), gaps >0.25 s total <1 s | theirs is faster; our 10s/121s builds don't conflict |
| Captions | white heavy grotesque, centre ≈75 % height, cap ≈5.6 % of width, 1–3 words | white bold sans + thin black outline, 60–74 % height band, 1 word mostly | same convention, ours sits slightly lower and larger |
| Structure | Mode A one-shot journey (1–2 cuts) / Mode B scene-cut (6–9 cuts) | hard cuts almost never (0–1 in 12/20), transitions = continuous moves, 6–8 f crossfades at place changes | their channel is almost pure Mode A; our Mode B is the RicksClips-specific grammar |
| Characters | white capsule head, no head outline, dot eyes + thick brows, 2-tone uniforms | peach superellipse head (H/W .93, pointed crown/jaw), plum ink #241726 thick-thin outline, bean torso, 3.5 head-heights, ink-dot hands, 14 expressions | **two distinct character systems** — do not mix in one film |
| Colour | lum 98.8/255 mean, sat 0.27–0.51, dark neutrals + scene accents | day lum median ~.57 (0.43–0.54 raw), sat 0.38–0.65, lit C* p90 ~55 | theirs is brighter and more saturated |
| Warmth | scene-owned (−22.6…+56.7), film mean +7.1 | lighting follows story beats (noon → sunset → night-blue) | same principle, both scene-driven |
| Story turns | diegetic signage carries the turn | props carry the joke; every sentence illustrated literally | compatible |
| Thrill | ≥1 POV thrill shot per film in last third | foreground props in ~1/3 of shots, follow-the-object transitions | compatible |

Conclusion for the library: the two studies triangulate the genre's invariants (word-locked captions at ~2/3–3/4 height, 55–70 s, scene-driven light, creep-only holds) and isolate the channel-specific variables (head construction, palette brightness, cut density). A new film must declare **one** character system up front.

## Community analysis: 13 PRs + 11 issues (fetched via API, snapshot 2026-11-22)

### Substantive PRs (what the community fixed)

| PR | Content | Our verdict |
|---|---|---|
| **#3** | `short_qa.py` bug: the SPECS line's conditional binds to the whole `R.append(...)`, so a **silent render** (no audio stream) loses the SPECS line entirely (report starts with `NONE`). 3-line fix, byte-identical output otherwise. | **ADOPTED** into `tools/short_qa.py` (our renders are often muted animatics — we hit this bug class directly) |
| **#21** (fixes **#13**) | `short_qa.py` misses a **frozen span that runs to the last frame** (the loop only records a span when motion resumes). Flush the open run at `len(diff)` with the same ≥12 f threshold; PR ships 3 end-to-end regression tests. | **ADOPTED** into `tools/short_qa.py` |
| **#15** (fixes **#14**) | Fresh-install blank renders: npm now resolves `@react-three/postprocessing` ≥3.0.5, where `EffectComposer` builds in `useEffect`+`setState`; under Remotion `frameloop="never"` the first `advance()` runs before the composer exists → every frame is the flat `#cfe3f2` background, exit 0, no warning. Fix: **pin 3.0.4** (composer built in `useMemo`) + wrap composer children in one fragment (3.0.4 types reject `null` children). Also: Windows-only Chrome path, `TEMP`/`TMP` vs `TMPDIR`, hardcoded composition id, placeholder ROOT in `bridge_merge.py`, undocumented 26 Kenney GLBs silently skipped by `loadKit()`. | Pin **documented** in MODULE (we do not run Remotion, but our own sandbox lesson `stale-camera-nearfar-blurs-subject-in-video-only` is the same disease: per-frame uniform sync vs still-vs-video divergence). If we ever adopt Remotion: pin 3.0.4 first. |
| **#6** | Every Remotion bundle copies `public/` (~1.3 GB) into TEMP and never deletes → 60+ GB ENOSPC death mid-render (matches the SKILL.md gotcha). Adds self-cleanup + a dry-run cleaner with `--yes`. | Worth porting into our render wrapper if we ever bundle; our `_render_chunk.mjs` does not bundle (plain three.js), so no action now |
| **#11** | ElevenLabs narration step: one clip per script beat via the with-timestamps endpoint → `voice.wav` + `words.json` straight from the API (no STT pass) + `beats.json`; `--only`/`--voice`/`--starts`/`--min-frames` revision options; stdlib + ffmpeg only; key from `ELEVENLABS_API_KEY` env only. | **Candidate**: our `voice/words.json` pipeline currently depends on manual/STT timings; their direct-from-API timings + beat grouping is a cleaner contract. Evaluate against `voice_prep.py` |
| **#17** | "Caption-channel modules" from a real second production (Spanish zombie short, 1080x1920): pause-gap (>0.3 s) sentence split because **ElevenLabs stores `...` ellipses as commas**; scene windows derived from word timings (`start = words[0].ini − 0.25`, monotonic) so scenes re-derive when timings change; word-synced caption recipe (grey→white lerp ~90 ms, keyword recolour, selection box on last spoken word only) including the **hex channel-shift lerp trap** (`[0,8,16]` shifts turn white→red into white→blue; correct order `[16,8,0]`); SFX-only mix (`amix normalize=0` or the voice gets squashed, `adelay:all=1`, mux with `apad`, volumedetect window check); thumbnail with a code-constant `SIN_SUBS` flag because **`process.env` does not reach Remotion render workers from PowerShell**; mandatory frame-review loop (re-extract with a new prefix each pass); Windows/PowerShell translation table. | The reusable lessons are **recorded below** and two became library pitfall candidates. The hex-lerp trap also applies to our own `mix()` helpers in JS/CSS tooling |
| **#9, #10, #20** | Doc typos (adverb, duplicated parenthetical, wrong shared-brief path) | no action |
| **#16** | Rename README → skill install path (body is unrelated spam text) | no action |
| **#4** | Adds a "Pig War video delivery + voice credits" (delivery example, not pipeline) | no action |
| **#12, #24** | Junk ("Ccr …") | no action |

### Substantive issues

| Issue | Content | Verdict |
|---|---|---|
| **#14** | Fresh install → blank frames (root cause analysis of the 3.0.5 composer/`advance()` race, isolation steps) | merged with PR#15 above |
| **#13** | Frozen-span-at-end miss with synthetic diff tables | fixed by PR#21, ADOPTED |
| **#5** | Third-party feature post (WaveWeaver guide; note the "probably a virus" reply and the author's clarification — treat external skill aggregators with the same caution) | no action |
| #1, #2, #7, #8, #18, #19, #22, #23 | Spam/test/foreign-language noise ("K", "Delete my message", "kurd nation", "Balochistan", "аввп") | no action |

**Tracker hygiene lesson:** of 24 items, 5 carry real engineering value (3 code fixes, 1 pin guide, 1 add-on module set). For our own repo: keep the tracker in the same discipline — a PR that changes behaviour ships a reproduction table.

## What we adopt (map to our pipeline)

| Their asset | Our integration | Status |
|---|---|---|
| `short_qa.py` per-frame QA (black/white/frozen/pop + loudness + per-shot stats + 2 s contact sheets with burned frame numbers) | `tools/short_qa.py` (fixed with PR#3 + PR#21) — run it on every muxed deliverable, not just law11 | **adopted now** |
| `sbs_sheet.py` side-by-side rows (ours vs reference) | `tools/sbs_sheet.py` — look-match reviews against `style/ricksclips-dna/data/sheet_*.jpg` | **adopted now** |
| Camera grammar (glide model, kicks, creep holds) | cross-check input for `film_plan.py` speed gates; `story.ts` `glide()/pushK()/kickAt()` are the reference formulas | **read + cross-check** |
| Character construction v2 (superellipse heads, thick-thin outline weighted away from light, 3.5 HH, ink-dot hands) | our `gen_cast.py`/sheet16 cast is the RicksClips capsule system; theirs is a second, fully specified system if a film ever calls for the "peach-ink" look | **reference** |
| Look tech (`ink.ts` world ink pass before DOF, `lensblur.ts` thin-lens CoC, `grade.ts` 6-knot curve + split tone, `cardshade.ts` scene-lit cards, `lights.ts` camera-relative frozen sun) | our `look3d.mjs`/`lie_cam.mjs` already implement cousin techniques (learned via the earlier [adopted] gotchas); the vendored source is now the full-formula reference | **reference** |
| Audio kit (`timeline.py` mirror + cue-list SFX + BS.1770-4 + ducking mix) | our audio today is voice-only (fish_tts + mux). A synthesized music/SFX bed timed to words.json is the missing piece; `dsp.py`'s own loudness meter also bypasses our sandbox's `volumedetect` hang | **candidate (next audio work)** |
| Look-match loop (measure → 5 owned sandboxes → merge by owned files → fresh verifier → re-sync) | our episode loop already does measure+gates; the owned-file merge discipline is worth adopting when two agents touch one episode | **process note** |
| Script formula (hook paradox → setting → escalation → mystery → "You see," pivot → analogy → ironic payoff) | our `auto_episode.py` narration intake; the formula is genre-compatible with our story grammar §7 | **reference** |
| Remotion stack | NOT adopted — we render with `templates/threejs_film/_render_chunk.mjs` (no bundler, no TEMP growth, ~876 ms/frame at 540x960). Keep Remotion as the fallback if we ever need DOM overlays/Rive | **rejected (for now)** |
| Their reference frames/sheets | style-study ground truth for sbs_sheet comparisons of the peach-ink character system only — never ours | **reference, private** |

## Readability traps (from SKILL.md + PR#17) not yet in our pitfall files

1. Swing drawn as one rope that disappears behind the kid reads as a **hanging** — always two ropes to a wide plank.
2. Props closer than ~2 m to a lens become **huge cut-off blobs**; re-check every prop near a moved camera.
3. A foreground bush cut by the frame edge reads as a **green ball** — recognisable or gone.
4. Flags: red + yellow star reads as **Vietnam**; use a period-correct flag.
5. Side-lit painted signs go grey-blue — give the **sign face an unlit material**.
6. Golden rim as an offset outer copy turns hats into **picture frames** — inner rim only.
7. Rails at chest height through torsos — put the lens ~2.5 m up so rails cross **legs**.
8. **Close-up "half a face"** (PR#17): features drawn past the head circle's edge read as the face sliding off; every feature inside ~0.9 r of head centre.
9. **Hex channel-shift lerp** (PR#17): channel order in a JS colour lerp must be `[16,8,0]`; `[0,8,16]` turns white→red into white→blue.
10. Frozen holds read as freezes in QA (span ≥ 12 f) — every hold creeps.

## Rules imported from upstream (binding, same as their user rules)

- Story, characters and voice are always OURS; the references are for the LOOK, never for content.
- Never upload/publish the reference frames or sheets; never name the reference channel in a voice-over or description.
- No captions unless the channel spec asks for them (our channels DO — RicksClips DNA requires them).
- Lock the picture's time constants before sound is made; any later timing change re-runs the sound.
- Every pixel-sized post parameter scales with output height / 1920.
