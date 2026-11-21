#!/usr/bin/env python3
"""Exact replica of the check() framing gate to bisect the faceless discrepancy."""
import sys, json, math
sys.path.insert(0, "/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1/tools")
import film_plan as fp

ROOT = "/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1"
F = fp.load(ROOT + "/episodes/law11-art/film.json")
fps = F["fps"]
cam, takes = fp.bake_camera(F)
perf = F.get("_perf") or fp.bake_performance(F)
n = len(cam)
CAPTION_BAND = fp.CAPTION_BAND
face = [False] * n
for i, c in enumerate(cam):
    best = None
    for who in perf:
        st = fp.perf_at(perf[who], i)
        if not st["visible"] or st["view"] == "back": continue
        hc, hw, hh, H = fp.head_box(F, who, st); p = fp.project(c, hc)
        if not p: continue
        w = hw / p[2] * (0.5 / math.tan(math.radians(c["fov_v"]) / 2)) * fp.PXH / fp.PXW
        h_ = w * fp.PXW / fp.PXH * hh / hw
        if not (-w / 2 < p[0] < 1 + w / 2 and -h_ / 2 < p[1] < 1 + h_ / 2) or w < 0.04: continue
        if 0 <= p[0] <= 1 and 0 <= p[1] <= 1: face[i] = True
        if best is None or w > best[0]: best = (w, p[1], None, None, None, None)
run = 0; best = (0, 0, 0)
for i in range(n):
    if not face[i]:
        run += 1
        if run > best[0]: best = (run, i - run + 1, i)
    else: run = 0
print(f"faceless longest: {best[0]}f = {best[0]/fps:.1f}s frames {best[1]}-{best[2]}")
print("faces %:", round(100 * sum(face) / n, 1))
# who is visible at frames inside the run
for i in (best[1] + 10, (best[1] + best[2]) // 2):
    vis = [(who, fp.perf_at(perf[who], i)["visible"], [round(x, 2) for x in fp.perf_at(perf[who], i)["pos"]]) for who in perf]
    print(f"f{i} t={i/fps:.1f}s cam.place={cam[i].get('place')} subj={cam[i].get('subject')} pos={[round(x,2) for x in cam[i]['pos']]} aim={[round(x,2) for x in cam[i]['aim']]}")
    print("   vis:", vis)
