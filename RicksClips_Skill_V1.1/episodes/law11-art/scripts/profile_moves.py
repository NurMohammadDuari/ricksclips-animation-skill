#!/usr/bin/env python3
"""Dump speed profile inside the two long moves, base vs via."""
import sys, json, copy
sys.path.insert(0, "/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1/tools")
import film_plan as fp

ROOT = "/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1"
F0 = fp.load(ROOT + "/episodes/law11-ai/film.json")

def profile(F, lo, hi, label):
    cam, takes = fp.bake_camera(F)
    sp = fp.screen_speed(cam)
    seg = sp[lo:hi]
    print(f"{label}: f{lo}-{hi} min={min(seg):.1f} max={max(seg):.1f} avg={sum(seg)/len(seg):.1f}")
    print("  " + " ".join(f"{x:.0f}" for x in seg[::4]))

F = copy.deepcopy(F0)
profile(F, 1360, 1475, "t2 st11 move base")
F2 = copy.deepcopy(F0); F2["takes"][1]["stations"][11]["via"] = [[-1.4, -2.4, 1.15]]
profile(F2, 1360, 1475, "t2 st11 move via ")
F3 = copy.deepcopy(F0)
profile(F3, 1665, 1775, "t3 st01 move base ")
F4 = copy.deepcopy(F0); F4["takes"][2]["stations"][1]["via"] = [[1.7, -1.55, 0.75]]
profile(F4, 1665, 1775, "t3 st01 move via  ")
