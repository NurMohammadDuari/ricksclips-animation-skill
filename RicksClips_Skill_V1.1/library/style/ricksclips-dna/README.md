# ricksclips-dna — the analyze → think → create loop

This module turns @RicksClips3000's current viral shorts into machine-checked
rules, and gives the AI a full loop: **ingest any new video, extend the DNA,
then plan a film that conforms to it.**

## Files

- `STYLE_DNA.md` — the measured style bible (read before boarding any episode).
- `style_params.json` — the same DNA as data; consumed by `tools/style_check.py`
  and `tools/auto_episode.py`.
- `analyze_video.py` — ingest a new video (mp4 or frames dir) → metrics JSON +
  contact sheet + caption crops, identical method to the corpus below.
- `data/` — the 2026-11 corpus evidence: 7 per-video metrics JSONs
  (12,761 frames measured), cross-video `summary.json`, caption-band stats,
  one 12x8 contact sheet per video (the visual reference), caption zoom crop.

## The loop (how the AI makes a video like @RicksClips3000)

1. **ANALYZE** — new reference material in?
   `python library/style/ricksclips-dna/analyze_video.py --video new.mp4 --outdir library/style/ricksclips-dna/data/`
   Compare the printed metrics against `style_params.json`: if the new video
   shifts a band (cuts/min, warmth, caption), update the DNA and say so.
2. **THINK** — pick the structure mode:
   - Mode A (one-shot journey): slow-burn world stories, 1-2 cuts.
   - Mode B (scene-cut story): 6-9 scenes, cuts on place/time jumps.
   Choose the scene recipes (`scene_recipes`) so every place owns a warmth
   identity, write the diegetic sign that carries the turn, and place one POV
   thrill shot in the last third.
3. **CREATE** — draft the plan without hardcoding anything:
   `python tools/auto_episode.py --script story.txt --title "My Film" --mode B --words voice/words.json --out episodes/my-film/film.json`
   produces a first-pass `film.json` (sentences, word-timed stations, moods on
   the DNA recipes, acting/fx/sound/kicks beats) plus `out/plan/auto_draft.md`
   staging notes. The AI artist then builds real sets/cast and refines.
4. **CHECK** —
   `python tools/film_plan.py check episodes/my-film/film.json` (the 41 gates)
   `python tools/style_check.py --film episodes/my-film/film.json` (DNA gate,
   add `--frames rendered/` to grade the RENDER, not just the plan)
5. **ITERATE** — fix until both checkers are green, render chunk-wise with
   `templates/threejs_film/_render_chunk.mjs`, mux the voice, ship.

## Provenance

Every number in `STYLE_DNA.md` traces to `data/metrics_*.json`. The frames
themselves (1.2 GB, 12,761 jpg) stay out of git on purpose — the sheets and
metrics carry the evidence.
