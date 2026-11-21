#!/usr/bin/env python3
"""Search travel-duration tweaks for law11-ai to lift p90 speed above the FAIL floor
while keeping peak <= 55 and at-rest >= 30. Uses film_plan's own bake + measure."""
import sys, json, copy, math
sys.path.insert(0, "/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1/tools")
import film_plan as fp

ROOT = "/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1"
F0 = fp.load(ROOT + "/episodes/law11-ai/film.json")

def measure(F):
    cam, takes = fp.bake_camera(F)
    sp = fp.screen_speed(cam)
    live = [i for i in range(len(cam)) if not cam[i]["cut"]]
    v = [sp[i] for i in live]
    n = len(cam); dur = n / F["fps"]
    at_rest = 100.0 * sum(1 for x in v if x < fp.SETTLED) / max(1, len(v))
    # longest travel from baked stations
    tl = []
    for tk in takes:
        S = tk["_S"]
        for j in range(len(S) - 1):
            a, b = S[j]["_depart"], S[j + 1]["_arrive"]
            if b > a: tl.append((b - a) / F["fps"])
    tp = max(tl) if tl else 0.0
    pk = max(v)
    v_sorted = sorted(v)
    def pct(p):
        return v_sorted[min(len(v_sorted) - 1, int(p / 100.0 * len(v_sorted)))]
    return pct(50), pct(90), pk, at_rest, tp, dur

def apply(F, a, b, hop):
    # a: t2 st11 travel, b: t3 st01 travel, hop: scale factor for 0.28s hop travels
    F["takes"][1]["stations"][11]["travel"] = a
    F["takes"][2]["stations"][1]["travel"] = b
    if hop != 1.0:
        for tk in F["takes"]:
            for s in tk["stations"]:
                if abs(s.get("travel", 0) - 0.28) < 0.02:
                    s["travel"] = round(0.28 * hop, 3)

print(f"{'t2s11':>6} {'t3s01':>6} {'hop':>5} | {'p50':>5} {'p90':>5} {'peak':>5} {'rest%':>6} {'longT':>5}")
for a in (3.71, 2.4, 2.0, 1.6):
    for b in (3.2, 2.2):
        for hop in (1.0, 0.8):
            F = copy.deepcopy(F0)
            apply(F, a, b, hop)
            p50, p90, pk, rest, tp, dur = measure(F)
            flag = " <== " if (p90 >= 12 and pk <= 55 and rest >= 30) else ""
            print(f"{a:6.2f} {b:6.2f} {hop:5.2f} | {p50:5.2f} {p90:5.1f} {pk:5.1f} {rest:6.1f} {tp:5.2f}{flag}")
