#!/usr/bin/env python3
"""Deep-dive: why heads cut at specific stations."""
import sys, math
sys.path.insert(0, "/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1/tools")
import film_plan as fp

ROOT = "/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1"
F = fp.load(ROOT + "/episodes/law11-art/film.json")
cam, takes = fp.bake_camera(F)
perf = F.get("_perf") or fp.bake_performance(F)

def head_report(frame, who=None):
    c = cam[frame]
    print(f"--- f{frame} t={frame/30:.1f}s pos={[round(v,2) for v in c['pos']]} aim={[round(v,2) for v in c['aim']]} lens={c['lens']} fov={c['fov_v']}")
    for w in ([who] if who else list(perf.keys())):
        st = fp.perf_at(perf[w], frame)
        if not st["visible"] or st["view"] == "back": continue
        hc, hw, hh, H = fp.head_box(F, w, st); p = fp.project(c, hc)
        if not p: print(f"  {w}: head behind camera"); continue
        wfrac = hw / p[2] * (0.5 / math.tan(math.radians(c["fov_v"]) / 2)) * fp.PXH / fp.PXW
        hfrac = wfrac * fp.PXW / fp.PXH * hh / hw
        cut = p[0] - wfrac / 2 < 0 or p[0] + wfrac / 2 > 1 or p[1] - hfrac / 2 < 0 or p[1] + hfrac / 2 > 1
        print(f"  {w}: head_c=({p[0]:.2f},{p[1]:.2f}) w={wfrac:.2f} h={hfrac:.2f} box=({p[0]-wfrac/2:.2f}-{p[0]+wfrac/2:.2f}, {p[1]-hfrac/2:.2f}-{p[1]+hfrac/2:.2f}) CUT={cut}")

head_report(2850, 'rafi')     # t11 st3 M
head_report(2900, 'rafi')     # t11 st4 W
head_report(1500, 'ma')       # t6 st1 C
head_report(230, 'chacha')    # t9 st0 W? no — t2 area... find t9 st0 frame
head_report(2270, 'chacha')   # t9 st0 W
