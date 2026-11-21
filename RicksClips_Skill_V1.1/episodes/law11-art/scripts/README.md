# law11-art working scripts

Kept for archaeology: the throwaway-but-real scripts used to build, tune and debug this
episode's film plan. The reproducible builder is `../build_film.py` (portable version of
`build_law11_art.py`, byte-identical output).

## What each group does

- `build_law11_art.py` — original film.json builder (v2 → v8 evolution, absolute-path version)
- `patch_v7.py / patch_v8.py / patch_v9.py / patch_v10.py / patch_deep.py` — ordered plan
  evolution patches (anchor spacing, prop continuity, shot-mix rebalance, deep dressing)
- `diag_gates.py / diag_heads.py / headcut_probe.py / headcut_probe2.py / headcut_debug.py /
  t5_flow_debug.py` — gate diagnostics: head-cut math, word stations, camera flow
- `fast_travels.py / halve_travels.py / retime_travels.py / rebalance_holds.py /
  merge_stations.py / search_travel.py / search_via.py / search_via2.py / find_cam_peak.py /
  profile_moves.py / tune_law11.py` — travel-peak, hold and via-point tuning passes
- `debug_faces.py / debug_faces2.py / debug_faces3.py / castsheet_local.mjs` — cast sheet
  face rendering debugging (led to the ma/nephew/chacha fixes in sheet16)
- `render_chunk.sh / render_chunk_pair.sh / mux_seg.sh / mux_seg2.sh` — chunked animatic
  rendering + voice muxing helpers

Run order that produced the committed `../film.json`: `build_law11_art.py` → patches →
`tools/film_plan.py check` (42 gates) → diag/tune loop → `../build_film.py` final.
