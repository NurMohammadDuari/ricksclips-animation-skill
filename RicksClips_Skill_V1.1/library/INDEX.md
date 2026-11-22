# Library index — read before every episode

## Pitfalls
- [dispose-null-breaks-video-renders](pitfall/dispose-null-breaks-video-renders.md) — CRITICAL [adopted]: prototype-call dispose for composer passes
- [stale-camera-nearfar-blurs-subject-in-video-only](pitfall/stale-camera-nearfar-blurs-subject-in-video-only.md) — CRITICAL [adopted]: per-frame uniform sync; sequence-vs-still QA
- [backlight-kills-rim-gate](pitfall/backlight-kills-rim-gate.md) — HIGH: on-axis halo fallback for screen-space rim
- [parallel-chrome-renders-kill-batches](pitfall/parallel-chrome-renders-kill-batches.md) — MED: one Chrome render job at a time; count stills vs request
- [sun-elevation-gates-ground-pools](pitfall/sun-elevation-gates-ground-pools.md) — MED: measure the lit-pool rgb before committing a sun change
- Also binding (kept in SKILL.md Gotchas until migrated): teal Kenney materials; cameras inside houses; ink pass before DOF; px params scale with resolution; Remotion temp fills the drive; backslash paths; silent audio track; scratch .ts in out/; film grain off; SFX peak-align not threshold-align [adopted].

- [vertical-frame-narrow-hfov](pitfall/vertical-frame-narrow-hfov.md) — HIGH: 9:16 hfov is ~0.56x; stage in depth, check lateral offsets
- [camera-key-arrive-vs-depart](pitfall/camera-key-arrive-vs-depart.md) — MED: key frame = ARRIVAL; park-creep then move
- [code-colour-is-not-screen-colour](pitfall/code-colour-is-not-screen-colour.md) — MED: measured screen colours are pipeline TARGETS; verify on a render
- [too-many-shots-reads-choppy](pitfall/too-many-shots-reads-choppy.md) — HIGH (CB): ~3-4 shots per 30 s; travel inside a shot, cut only on real jumps
- [captions-required](pitfall/captions-required.md) — HIGH (CB): captions ON, 1 white bold word + black outline at 60-74 % height, word-timed
- [blender-night-pipeline-gotchas](pitfall/blender-night-pipeline-gotchas.md) — HIGH: sRGB->linear, world volume kills sky, Freestyle card borders, absolute render paths, no PIL in Blender
- [density-below-reference](pitfall/density-below-reference.md) — HIGH (CB): measure density per frame (density_check.py G1-G5) and test-render each location before animating
- [floor-zfight-coplanar-surfaces](pitfall/floor-zfight-coplanar-surfaces.md) — CRITICAL (CB, goldrush): floor coplanar with a foundation flickers; 2-3 cm offset; flicker.py + zprobe
- [light-pops-in-one-frame](pitfall/light-pops-in-one-frame.md) — HIGH (CB, goldrush): fast lamp sines, cones/glints/puffs switching in 1 frame; slow curves, fades 10-15 frames
- [body-inside-furniture](pitfall/body-inside-furniture.md) — HIGH (CB, goldrush): marks behind the counter's back edge, only the arm crosses; check.mjs body_in_mesh
- [sliding-walk-linear-glide](pitfall/sliding-walk-linear-glide.md) — HIGH (CB, goldrush): linear move_s glide + leg cycle slides; foot-locked walks, stride matched to distance
- [drawn-face-shading-bands](pitfall/drawn-face-shading-bands.md) — HIGH (CB): card_shade amount/rim/far off in every stretch, forced in the render wrapper
- [shared-plan-folder-serialises-parallel-renders](pitfall/shared-plan-folder-serialises-parallel-renders.md) — HIGH: one shared out/plan + one lock queued 7 builders; never rm -rf a folder with junctions
- [sibling-stretch-folders-copied-sets](pitfall/sibling-stretch-folders-copied-sets.md) — MED: copied sets per stretch folder drift; one episode folder, merged sets with place keys
- [camera-fix-rounds-add-hops](pitfall/camera-fix-rounds-add-hops.md) — HIGH: fix rounds' fly-ins/outs took check_film to 4 FAIL; plan camera flow once per stretch, re-run check_film each round
- [costume-breaks-story-rule](pitfall/costume-breaks-story-rule.md) — MED: a top-hat extra digging read as the hero; costume check against the story's rules, not only the period
- [exit-hides-until-visible-true](pitfall/exit-hides-until-visible-true.md) — CRITICAL [adopted]: exit=True persists until an act sets visible=True; plan gates still pass while the star of the scene is invisible — audit visibility spans per character
- [cast-leaks-across-place-cuts](pitfall/cast-leaks-across-place-cuts.md) — HIGH: one world, many sets — every character without an act AT the place cut keeps its stale position (Ma's sari in the night shop, chacha 428 f into the ending); enter/exit + fresh pos land ON the cut frame, audit per-take on-screen counts

## Solutions
- [far-ink-fades-with-haze](solution/far-ink-fades-with-haze.md) — the reference drops ink on far architecture; fadeNear/Far 90/260, farOpacity 0.7
- [diegetic-vignette-light-pool](solution/diegetic-vignette-light-pool.md) — night vignettes are LIGHT POOLS, not post overlays; post vig stays at corner 0.86
- [flicker-scan-flicker-py](solution/flicker-scan-flicker-py.md) — tools/frame_checks/flicker.py: motion-aligned floor/one-frame flicker scan, FAIL = 2+ pop frames; z-probe for the cause
- [private-render-folder-per-stretch](solution/private-render-folder-per-stretch.md) — render_stretch.sh v2: private sNep/ per stretch, junctions to shared sets/cast/moves/voice
- [one-episode-folder-seeded-merge-proof](solution/one-episode-folder-seeded-merge-proof.md) — merge proven pixel-identical with --seed 1 (Math.random needs a seed for any comparison)

## Recipes / modules
- (grows per episode: hero props in templates/props/, transitions in story.ts TRANSIT, VFX cards)
- solution/render-lock-file-for-parallel-builders.md — lock file serializes only the Chrome render step, builders stay parallel
- pitfall/pale-heat-palette-breaks-sat-bar.md — heat states must stay saturated (ref 0.30-0.47); measure every new palette state before boarding; heads ≥22% frame width on character beats
- pitfall/headwear-eats-brow-acting.md — under a brim, brow-only expressions read identical; vary eye or mouth kind, and strip-test keys before animating
- solution/locked-look-package.md — the approved look is a package plus one check runner; episodes supply only props, staging and preset
- pitfall/old-gates-punish-no-ink.md — score no-outline frames with --style 3d; weave aliasing, grain direction, f/5.6, clamped lamps
- pitfall/materials-before-dense-scene.md — finish Stage A (full Python build in the toon look, polished until the gates pass) before any Stage B work
- solution/short-cast-raised-on-stool.md — a short cast member behind hero furniture reads only raised on a stool: seat under the mark, act z to the seat, W aims at their eyeline, night ai/si +0.2; visibility.json passes while the story doesn't

## Modules (2026-11-21)
- module/law11-sweetshop-world.md — deep-scene pass (2026-11-22): sheet17 bazaar extras (cast:khoddeder/khoddeder2/bepari), PROPS.wage (yellow envelope) + PROPS.khata (open ledger) replace placeholder letter circles, 3 sets dressed to reference density (boxes, clocks, price boards, portrait, plants, tea row). Extras: ~3 m deep on the aim axis, face beat every <=3 s.
- [law11-sweetshop-world](module/law11-sweetshop-world.md) — Bangla bazaar world: 5-cast sheet (sheet16, auto-registered as cast:rafi/chacha/ma/nephew/dokandar) + 3 place_kit sets (mithai_shop/mithai_home/mithai_padosi) + Bangla signTex helper + lineup.mjs renderer

## Style DNA (2026-11-22)
- [style/ricksclips-dna](style/ricksclips-dna/STYLE_DNA.md) — @RicksClips3000 current viral style, measured: 7 shorts, 12,761 frames at 30 fps. Two structure modes (A one-shot journey 1-2 cuts / B scene-cut 6-9 cuts at 6.1-8.8/min), scene-owned warmth (-22.6..+56.7), caption spec (white heavy grotesque, centre ~75 % height, cap height 5.6 % of width), diegetic-sign story turns, one POV thrill shot in the last third. Machine data + per-video metrics + contact sheets in `style/ricksclips-dna/data/`; ingest new videos with `style/ricksclips-dna/analyze_video.py`; gate a plan or a render with `tools/style_check.py`; draft a whole episode from a narration script with `tools/auto_episode.py` (0 FAIL / 8 WARN on a fresh draft, both modes). law11-art validates at 6 PASS / 1 WARN (its 121 s length is outside the 55-67 s corpus band by design).
