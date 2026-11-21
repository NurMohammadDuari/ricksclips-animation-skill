#!/usr/bin/env python3
"""Search via-detour + travel tweaks for law11-ai: lift p90 >= 15, keep peak <= 55."""
import sys, json, copy
sys.path.insert(0, "/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1/tools")
import film_plan as fp

ROOT = "/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1"
F0 = fp.load(ROOT + "/episodes/law11-ai/film.json")

def measure(F):
    cam, takes = fp.bake_camera(F)
    sp = fp.screen_speed(cam)
    live = [i for i in range(len(cam)) if not cam[i]["cut"]]
    v = [sp[i] for i in live]
    at_rest = 100.0 * sum(1 for x in v if x < fp.SETTLED) / max(1, len(v))
    tl = []
    for tk in takes:
        S = tk["_S"]
        for j in range(len(S) - 1):
            a, b = S[j]["_depart"], S[j + 1]["_arrive"]
            if b > a: tl.append((b - a) / F["fps"])
    v_sorted = sorted(v)
    pct = lambda p: v_sorted[min(len(v_sorted) - 1, int(p / 100.0 * len(v_sorted)))]
    over15 = 100.0 * sum(1 for x in v if x >= 15) / max(1, len(v))
    return pct(50), pct(90), max(v), at_rest, (max(tl) if tl else 0.0), over15

def apply(F, via2, via3, hop, t2s11, t3s01):
    F["takes"][1]["stations"][11]["travel"] = t2s11
    F["takes"][2]["stations"][1]["travel"] = t3s01
    if via2: F["takes"][1]["stations"][11]["via"] = via2
    if via3: F["takes"][2]["stations"][1]["via"] = via3
    if hop != 1.0:
        for tk in F["takes"]:
            for s in tk["stations"]:
                if abs(s.get("travel", 0) - 0.28) < 0.02:
                    s["travel"] = round(0.28 * hop, 3)

print(f"{'cfg':>22} | {'p50':>5} {'p90':>5} {'peak':>5} {'rest%':>6} {'longT':>5} {'>=15px':>6}")
cfgs = [
    ("base",               None, None, 1.0, 3.71, 3.2),
    ("via2+via3",          [[-1.0, -2.2, 1.1]], [[1.2, -1.5, 0.7]], 1.0, 3.71, 3.2),
    ("via2big+via3big",    [[-1.4, -2.4, 1.15]], [[1.7, -1.55, 0.75]], 1.0, 3.71, 3.2),
    ("via2big+via3big+h",  [[-1.4, -2.4, 1.15]], [[1.7, -1.55, 0.75]], 0.8, 3.71, 3.2),
    ("via2big+via3big+h+t",[[-1.4, -2.4, 1.15]], [[1.7, -1.55, 0.75]], 0.8, 2.6, 2.8),
    ("via2big+via3big+t",  [[-1.4, -2.4, 1.15]], [[1.7, -1.55, 0.75]], 1.0, 2.6, 2.8),
]
for name, v2, v3, hop, a, b in cfgs:
    F = copy.deepcopy(F0)
    apply(F, v2, v3, hop, a, b)
    p50, p90, pk, rest, tp, o15 = measure(F)
    mark = " <== WINNER" if (p90 >= 15 and pk <= 55 and rest >= 30) else ""
    print(f"{name:>22} | {p50:5.2f} {p90:5.1f} {pk:5.1f} {rest:6.1f} {tp:5.2f} {o15:6.1f}{mark}")
