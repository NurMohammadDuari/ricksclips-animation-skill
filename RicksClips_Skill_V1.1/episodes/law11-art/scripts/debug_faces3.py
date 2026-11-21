#!/usr/bin/env python3
"""Probe law11-art: widest heads, frozen runs, speed stats."""
import sys, json, math
sys.path.insert(0, "/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1/tools")
import film_plan as fp

ROOT = "/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1"
F = fp.load(ROOT + "/episodes/law11-art/film.json")
fps = F["fps"]
cam, takes = fp.bake_camera(F)
perf = F.get("_perf") or fp.bake_performance(F)
sp = fp.screen_speed(cam)
n = len(cam)

# widest heads
tops = []
for i, c in enumerate(cam):
    for who in perf:
        stt = fp.perf_at(perf[who], i)
        if not stt["visible"] or stt["view"] == "back": continue
        hc, hw, hh, H = fp.head_box(F, who, stt); p = fp.project(c, hc)
        if not p: continue
        w = hw / p[2] * (0.5 / math.tan(math.radians(c["fov_v"]) / 2)) * fp.PXH / fp.PXW
        tops.append((w, i, who, round(p[0], 2), round(p[1], 2), c["framing"], c.get("place")))
tops.sort(reverse=True)
print("widest heads:")
for t in tops[:8]: print(f"  w={t[0]:.2f} f{t[1]} t={t[1]/fps:.1f}s {t[2]} px=({t[3]},{t[4]}) {t[5]} {t[6]}")

# frozen runs (visible, same pose, resting camera)
SETT = fp.SETTLED
frozen_run = 0; best = (0, 0, 0, None)
prev_state = {}
for i in range(n):
    moving = sp[i] >= SETT
    any_move = False
    for who in perf:
        stt = fp.perf_at(perf[who], i)
        key = (stt["pose"], stt["face"])
        if stt["visible"] and (prev_state.get(who) != key): any_move = True
        prev_state[who] = key if stt["visible"] else None
    if not moving and not any_move:
        frozen_run += 1
        if frozen_run > best[0]: best = (frozen_run, i - frozen_run + 1, i, None)
    else: frozen_run = 0
print(f"frozen longest: {best[0]}f = {best[0]/fps:.1f}s frames {best[1]}-{best[2]} ({best[1]/fps:.1f}s-{best[2]/fps:.1f}s) place={cam[best[1]+5].get('place') if best[0]>10 else '-'}")

# speed stats
live = [sp[i] for i in range(n) if not cam[i]["cut"]]
v = sorted(live)
print(f"speeds: p50={v[len(v)//2]:.2f} p90={v[int(.9*len(v))]:.2f} max={v[-1]:.1f} | travel frames(>2): {100*sum(1 for x in v if x>2)/len(v):.0f}%")
