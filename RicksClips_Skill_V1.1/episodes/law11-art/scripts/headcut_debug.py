#!/usr/bin/env python3
"""Replicate the film_plan head-cut gate and list every offending station."""
import sys, math, json
sys.path.insert(0, "/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1/tools")
import film_plan as fp

FILM = "/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1/episodes/law11-art/film.json"
F = fp.load(FILM)
cam, takes = fp.bake_camera(F)
perf = F["_perf"]
fps = F["fps"]
n = len(cam)

cut_frames = []; facen = 0
for i, c in enumerate(cam):
    best = None; bestinfo = None
    for who in perf:
        st = fp.perf_at(perf[who], i)
        if not st["visible"] or st["view"] == "back": continue
        hc, hw, hh, H = fp.head_box(F, who, st); p = fp.project(c, hc)
        if not p: continue
        w = hw / p[2] * (0.5 / math.tan(math.radians(c["fov_v"]) / 2)) * fp.PXH / fp.PXW
        h_ = w * fp.PXW / fp.PXH * hh / hw
        if not (-w / 2 < p[0] < 1 + w / 2 and -h_ / 2 < p[1] < 1 + h_ / 2) or w < 0.04: continue
        cut = p[0] - w / 2 < 0 or p[0] + w / 2 > 1 or p[1] - h_ / 2 < 0 or p[1] + h_ / 2 > 1
        if best is None or w > best[0]: best = (w, p[1], cut); bestinfo = (who, p[0], p[1], w, h_)
    if best:
        facen += 1
        if best[2]: cut_frames.append((i, bestinfo))

print("total frames %d, face frames %d, cut frames %d" % (n, facen, len(cut_frames)))
print("ct = %.1f%% (limit 13)" % (100.0 * len(cut_frames) / max(1, facen)))

# map frames back to stations
def station_of(f):
    for ti, tk in enumerate(takes):
        S = tk["_S"]
        for j, s in enumerate(S):
            a = s["_depart"]; b = S[j + 1]["_arrive"] if j + 1 < len(S) else tk["_f1"]
            if a <= f <= b:
                return ti, j, s
    return None, None, None

by_station = {}
for i, info in cut_frames:
    ti, j, s = station_of(i)
    key = (ti, j, s.get("subject") if s else "?", s.get("at") if s else "?")
    by_station.setdefault(key, []).append((i, info))

for (ti, j, subj, at), lst in sorted(by_station.items(), key=lambda kv: -len(kv[1])):
    who, px, py, w, h_ = lst[0][1]
    edges = []
    if px - w / 2 < 0: edges.append("LEFT")
    if px + w / 2 > 1: edges.append("RIGHT")
    if py - h_ / 2 < 0: edges.append("TOP")
    if py + h_ / 2 > 1: edges.append("BOTTOM")
    print("take%d stn%d subj=%-10s at=%-8s frames=%2d (%d..%d) who=%-8s head(%.2f,%.2f) w=%.2f edges=%s" % (
        ti, j, subj, at, len(lst), lst[0][0], lst[-1][0], who, px, py, w, "+".join(edges)))
