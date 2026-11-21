#!/usr/bin/env python3
"""Surgical diagnostics for the 5 remaining FAILs."""
import sys, json
sys.path.insert(0, "/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1/tools")
import film_plan as fp

ROOT = "/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1"
F = fp.load(ROOT + "/episodes/law11-art/film.json")
cam, takes = fp.bake_camera(F)
sp = fp.screen_speed(cam)
perf = F.get("_perf") or fp.bake_performance(F)
n = len(cam); fps = F["fps"]

# (a) which stations cut heads (station rest windows with cut)
cut_by_station = {}
for tk in takes:
    S = tk["_S"]
    for j, s in enumerate(S):
        a = s["_arrive"]; b = (S[j+1]["_depart"] if j+1 < len(S) else tk["_f1"])
        # count cut frames in the rest window
        cut = 0; tot = 0
        for f in range(max(0, a), min(n, b+1)):
            st = None
            best_w, best_cut = None, False
            import film_plan
            # replicate the gate's head test cheaply: reuse gate vars? just sample 5 frames
            pass
        pass
# simpler: per-frame cut flags via the same math
import math
from film_plan import project, head_box, perf_at
cutf = []
for i, c in enumerate(cam):
    best = None
    for who in perf:
        st = perf_at(perf[who], i)
        if not st["visible"] or st["view"] == "back": continue
        hc, hw, hh, H = head_box(F, who, st); p = project(c, hc)
        if not p: continue
        w = hw / p[2] * (0.5 / math.tan(math.radians(c["fov_v"]) / 2)) * fp.PXH / fp.PXW; h_ = w * fp.PXW / fp.PXH * hh / hw
        if not (-w / 2 < p[0] < 1 + w / 2 and -h_ / 2 < p[1] < 1 + h_ / 2) or w < 0.04: continue
        cut = p[0] - w / 2 < 0 or p[0] + w / 2 > 1 or p[1] - h_ / 2 < 0 or p[1] + h_ / 2 > 1
        if best is None or w > best[0]: best = (w, cut)
    if best and best[1]: cutf.append(i)
print("cut frames:", len(cutf), "of face frames")
# group cut frames by active station
from film_plan import camera_segments
stn_of = {}
for tk in takes:
    S = tk["_S"]
    for f in range(tk["_f0"], tk["_f1"] + 1):
        j = max(i for i, s in enumerate(S) if s["_arrive"] <= f)
        stn_of[f] = (tk["id"], j, S[j].get("subject"), S[j].get("framing"), round(S[j]["pos"][1], 1), round(S[j]["aim"][1], 1))
groups = {}
for f in cutf:
    key = stn_of.get(f)
    if key: groups[key] = groups.get(key, 0) + 1
for k, v in sorted(groups.items(), key=lambda x: -x[1])[:12]:
    print("cut", k, v)

# (b) nouns
fps = F["fps"]
for snt in F["sentences"]:
    for noun in snt.get("nouns", []):
        hits = [w["s"] for w in F["_words"] if w["_k"] == noun["word"].lower()]
        nf = int(round(hits[noun.get("n", 1) - 1] * fps))
        what = noun.get("show")
        near = range(max(0, nf - 15), min(n, nf + 15))
        ok = any(what == cam[i]["subject"] or what in cam[i]["shows"] for i in near)
        if not ok: print("NOUN FAIL:", noun["word"], what, "frame", nf, "shows near:", [cam[i]["shows"] for i in range(nf-5, nf+5, 3)])

# (c) floating props
SLOT = {'hold_watch','press_watch','hold_up','hold_out','grip_pole','grip_point','grip_raise','grip_swing','grip_hang','grip_shield','grip_two','grip_sign','grip_box','grip_shoulder','grip_push'}
tot = {}
for who, runs in perf.items():
    for r in runs:
        st = r["state"]
        if st.get("prop") and st.get("pose") not in SLOT:
            key = (who, st.get("pose"), st.get("prop"))
            tot[key] = tot.get(key, 0) + r["f1"] - r["f0"] + 1
for k, v in tot.items(): print("FLOAT:", k, v, "frames", f"{k[0] and round(k and None) or ''}")

# (d) word stations not settled
for tk in takes:
    for s in tk["_S"]:
        if s.get("word"):
            a = s["_at"]
            seg = " ".join(f"{sp[f]:.0f}" for f in range(a-1, min(n, a+3)))
            bad = not all(sp[f] < 2.0 for f in range(max(0, a-1), min(n, a+3)))
            if bad: print("WORD STN BAD:", s.get("word"), "at f", a, "speeds", seg, "arrive", s["_arrive"], "depart", s["_depart"])
