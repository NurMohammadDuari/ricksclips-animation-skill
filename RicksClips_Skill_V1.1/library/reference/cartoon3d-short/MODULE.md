# cartoon3d-short — vendored reference module (claude-animated-shorts)

**Source:** https://github.com/mromidev/claude-animated-shorts (vendored 2026-11-22, `rsync -a --exclude .git`; issues/pulls API capture in `library/reference/claude-animated-shorts-api/`)
**What it is:** a measurement-driven Cartoon-3D-Short skill: Remotion + three.js bridge render pipeline, 20 reference shorts measured into 7 quantised style reports (colour / motion / lighting / outlines / textures …), a multi-agent look-matching loop, STYLE_BIBLE.md, and a programmatic audio stack (`audio/timeline.py` + sfx/music/mix/dsp/instruments/sfx_gen).

## Module map

| area | files | what it gives us |
|---|---|---|
| bridge | `templates/bridge/{story,toon,cast,ink,grade,lensblur,lights,shade,paint,cardshade,world,build}.ts`, `Bridge.tsx` | camera-grammar DSL (story.ts), toon shading + ink pass ordering, grade/lensblur stacks |
| scripts | `scripts/{short_qa,sbs_sheet,bridge_merge,bridge_shots}.py`, `bridge-stills.mjs` | QA gate + side-by-side sheet tooling |
| audio | `audio/{timeline,sfx,music,mix,dsp,instruments,sfx_gen}.py`, `cues.md` | fully programmatic narration-lead audio, no external assets |
| reports | 7 quantised style reports + STYLE_BIBLE.md | measured colour/motion/lighting targets for the same white-capsule-head cartoon-3D family |
| examples | `SCRIPT_example.md`, reference sheets | shot-table format reference |

## Relationship to ricksclips-dna (complementary, not competing)

- **ricksclips-dna** = *inverse* direction: measured 7 real @RicksClips3000 films (12,761 frames) → STYLE_DNA.md targets + film_plan gates.
- **cartoon3d-short** = *forward* direction: from a STYLE_BIBLE → render a new film (Remotion/three.js) that matches the same visual family (white capsule-head 3D cartoon shorts; confirmed visually against its `references/sheets/short01_sheet.jpg`).
- The toolkit already absorbed two of its gotchas before vendoring (Kenney teal palette, ink pass before DOF — see `library/README.md` provenance line).

## Community intel (issues + pulls capture, 2026-11-22)

`library/reference/claude-animated-shorts-api/` holds the repo's issues and comments as captured from the GitHub API (`iss_<n>.json` + `iss_<n>_comments.json`, plus `repo_meta.json`). Pattern across them: users reproduce the pipeline on other machines, ask for style-transfer of the same white-capsule-head family, and hit SwiftShader/software-GL rendering limits — the same limits our sandbox renders under. No merged PRs changed the core bridge at capture time; the value of this capture is the recurring gotcha list, which our own gates already encode.

## Integration roadmap (what we take from it)

1. **QA cross-check:** port `scripts/short_qa.py` as a second opinion next to `tools/measure/density_check.py` for episode stills.
2. **Side-by-side sheets:** port `scripts/sbs_sheet.py` → `tools/` for Rick-vs-ours frame comparison pages (the CB RULES No.1 test).
3. **Camera grammar:** `templates/bridge/story.ts` encodes the same "rest on the noun, travel on the verb" grammar as our CINEMATOGRAPHY.md — keep as reference when evolving film_plan station fields.
4. **Programmatic audio:** its audio stack is the fallback plan if Fish Audio TTS stays unavailable in the sandbox.

## Provenance

Vendored by the RicksClips Animation Skill toolkit. Upstream: mromidev/claude-animated-shorts. Its README credits the measurement methodology on 20 reference shorts.
