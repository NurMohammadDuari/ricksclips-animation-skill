#!/usr/bin/env python3
"""Round 2: push p90 toward 15. hop scaling + big S-detours + travel trims."""
import sys, copy
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
    return pct(50), pct(90), max(v), at_rest, (max(tl) if tl else 0.0)

def apply(F, hop, v2, v3, t2s11, t3s01, extra=None):
    F["takes"][1]["stations"][11]["travel"] = t2s11
    F["takes"][2]["stations"][1]["travel"] = t3s01
    if v2: F["takes"][1]["stations"][11]["via"] = v2
    if v3: F["takes"][2]["stations"][1]["via"] = v3
    for tk in F["takes"]:
        for s in tk["stations"]:
            if abs(s.get("travel", 0) - 0.28) < 0.02:
                s["travel"] = round(0.28 * hop, 3)
    if extra: extra(F)

print(f"{'cfg':>26} | {'p50':>5} {'p90':>5} {'peak':>5} {'rest%':>6} {'longT':>5}")
V2B = [[-1.4, -2.4, 1.15]]
V3B = [[1.7, -1.55, 0.75]]
V3S = [[1.3, -1.5, 0.7], [-0.9, -1.7, 0.6]]

def hold_cut(F):  # trim a few long holds so their squeezed moves get more frames (fast frames at sane speed)
    F["takes"][2]["stations"][2]["hold"] = 3.6   # t3 st02 5.14 -> 3.6 (gap 170f, hold 108f -> tv 62f, peak drops 44.7->~12)
def hop_and_insert(F):
    for tk in F["takes"]:
        for s in tk["stations"]:
            if abs(s.get("travel", 0) - 0.48) < 0.02: s["travel"] = 0.38

cfgs = [
    ("h.55+v2+v3S",        0.55, V2B, V3S, 3.71, 3.2, None),
    ("h.45+v2+v3S",        0.45, V2B, V3S, 3.71, 3.2, None),
    ("h.45+v2+v3S+trim",   0.45, V2B, V3S, 3.71, 3.2, hold_cut),
    ("h.55+v2+v3S+ins",    0.55, V2B, V3S, 3.71, 3.2, hop_and_insert),
    ("h.45+v2+v3S+ins",    0.45, V2B, V3S, 3.71, 3.2, hop_and_insert),
    ("h.35+v2+v3S+ins",    0.35, V2B, V3S, 3.71, 3.2, hop_and_insert),
]
for name, hop, v2, v3, a, b, extra in cfgs:
    F = copy.deepcopy(F0)
    apply(F, hop, v2, v3, a, b, extra)
    p50, p90, pk, rest, tp = measure(F)
    mark = " <== FULL PASS" if (p90 >= 15 and pk <= 55 and rest >= 30) else (" <== NO FAIL" if p90 >= 10.2 and pk <= 55 else "")
    print(f"{name:>26} | {p50:5.2f} {p90:5.1f} {pk:5.1f} {rest:6.1f} {tp:5.2f}{mark}")
