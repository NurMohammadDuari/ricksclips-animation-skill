#!/usr/bin/env python3
"""Debug law11-art: where is the faceless stretch + why are figures small."""
import sys, json, math
sys.path.insert(0, "/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1/tools")
import film_plan as fp

ROOT = "/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1"
F = fp.load(ROOT + "/episodes/law11-art/film.json")
cam, takes = fp.bake_camera(F)
perf = F.get("_perf") or fp.bake_performance(F)
sp = fp.screen_speed(cam)
fps = F["fps"]; n = len(cam)

def head_in(i):
    c = cam[i]; out = []
    for who in perf:
        st = fp.perf_at(perf[who], i)
        if not st["visible"] or st["view"] == "back": continue
        hc, hw, hh, H = fp.head_box(F, who, st); p = fp.project(c, hc)
        if p and 0 <= p[0] <= 1 and 0 <= p[1] <= 1:
            w = hw / p[2] * (0.5 / math.tan(math.radians(c["fov_v"]) / 2)) * fp.PXH / fp.PXW
            out.append((who, round(w, 3), round(p[0], 2), round(p[1], 2)))
    return out

# longest faceless run
run = 0; best = (0, 0, 0)
for i in range(n):
    if not head_in(i):
        run += 1
        if run > best[0]: best = (run, i - run + 1, i)
    else: run = 0
print(f"longest faceless: {best[0]}f = {best[0]/fps:.1f}s  frames {best[1]}-{best[2]} ({best[1]/fps:.1f}s-{best[2]/fps:.1f}s)")
for i in (best[1] + 5, (best[1] + best[2]) // 2, best[2] - 5):
    print(f"  f{i} t={i/fps:.1f}s heads={head_in(i)} place_cam={cam[i].get('place','?')} subj={cam[i].get('subject')}")
# character world positions at a few frames
for who in ("rafi", "chacha", "nephew", "ma", "dokandar"):
    for f in (100, 1800, 2400, 3200):
        stt = fp.perf_at(perf[who], f)
        print(f"  {who}@f{f}: pos={stt['pos']} visible={stt['visible']}")
