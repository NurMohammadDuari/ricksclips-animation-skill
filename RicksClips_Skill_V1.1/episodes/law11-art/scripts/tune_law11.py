#!/usr/bin/env python3
"""Final tuner for law11-art: iterate bake->measure->patch until 0 FAIL."""
import sys, json, math
sys.path.insert(0, "/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1/tools")
import film_plan as fp

ROOT = "/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1"
PATH = ROOT + "/episodes/law11-art/film.json"
FPS = 30
WORDS = json.load(open(ROOT + "/episodes/law11-art/voice/words.json"))

def measure(F):
    cam, takes = fp.bake_camera(F)
    sp = fp.screen_speed(cam)
    perf = F.get("_perf") or fp.bake_performance(F)
    n = len(cam)
    live = [i for i in range(n) if not cam[i]["cut"]]
    v = sorted(sp[i] for i in live)
    pk_i = max(range(n), key=lambda i: sp[i])
    tops = []
    for i, c in enumerate(cam):
        for who in perf:
            stt = fp.perf_at(perf[who], i)
            if not stt["visible"] or stt["view"] == "back": continue
            hc, hw, hh, H = fp.head_box(F, who, stt); p = fp.project(c, hc)
            if not p: continue
            w = hw / p[2] * (0.5 / math.tan(math.radians(c["fov_v"]) / 2)) * fp.PXH / fp.PXW
            if -w / 2 < p[0] < 1 + w / 2 and -w * 16 / 9 / 2 < p[1] < 1 + w / 2: tops.append((w, i, who, p[0], p[1]))
    tops.sort(reverse=True)
    prev = {}; fr = 0; runs = []
    for i in range(n):
        moving = sp[i] >= fp.SETTLED; ch = False
        for who in perf:
            stt = fp.perf_at(perf[who], i); key = (stt["pose"], stt["face"])
            if stt["visible"] and prev.get(who) != key: ch = True
            prev[who] = key if stt["visible"] else None
        if not moving and not ch:
            fr += 1
        else:
            if fr > 3 * FPS: runs.append((fr, i - fr, i))
            fr = 0
    if fr > 3 * FPS: runs.append((fr, n - fr, n))
    return dict(p50=v[len(v) // 2], p90=v[int(.9 * len(v))], pk=sp[pk_i], pk_i=pk_i,
                head=tops[0] if tops else None, runs=runs, cam=cam, takes=takes, sp=sp, perf=perf)

def travel_of(takes, f):
    for ti, tk in enumerate(takes):
        S = tk["_S"]
        for j in range(1, len(S)):
            if S[j - 1]["_depart"] <= f <= S[j]["_arrive"]: return ti, j
    return None

def find_station(F, ti, j):
    return F["takes"][ti]["stations"][j]

def who_visible_at(perf, f):
    return [w for w in perf if fp.perf_at(perf[w], f)["visible"]]

F = fp.load(PATH)
fx_added = 0
for it in range(22):
    M = measure(F)
    hw, hw_i, hw_who = M["head"][0], M["head"][1], M["head"][2] if M["head"] else (0, 0, "?")
    print(f"pass {it}: p90={M['p90']:.1f} pk={M['pk']:.0f}@f{M['pk_i']} head90={hw:.2f}@f{hw_i}({hw_who}) frozen_runs={[(round(a/30,1)) for a,_,_ in M['runs']]}")
    changed = False
    # peak: lengthen the offending travel (cap 2.4s)
    if M["pk"] > 58:
        hit = travel_of(M["takes"], M["pk_i"])
        if hit:
            ti, j = hit; st = find_station(F, ti, j)
            cur = st.get("travel", 1.0)
            if cur < 2.4:
                st["travel"] = round(min(2.4, cur * M["pk"] / 50.0), 2); changed = True
                print(f"  peak: t{ti} st{j} ({st.get('subject')}) travel {cur}->{st['travel']}")
            else:  # travel capped: shrink the distance instead (move pos 15% closer to aim)
                px, ax = st["pos"], st["aim"]
                st["pos"] = [round(ax[0] + (px[0] - ax[0]) * .85, 3), round(ax[1] + (px[1] - ax[1]) * .85, 3), round(ax[2] + (px[2] - ax[2]) * .85, 3)]
                changed = True; print(f"  peak: t{ti} st{j} distance -15%")
    # head90: the widest head is usually a bystander near the lens; angle the station away
    if hw > 0.55:
        print(f"  head90 {hw:.2f}@f{hw_i} ({hw_who}) left to design fixes")
    # frozen runs: inject face changes for visible characters mid-run
    for flen, f0, f1 in M["runs"]:
        mid_s = round((f0 + flen // 2) / FPS, 2)
        vis = who_visible_at(M["perf"], f0 + flen // 2)
        for who in vis[:2]:
            faces = ["confused", "standard", "proud", "delight", "cool", "sideeye", "sus", "troll", "standard"]
            cur = None
            for a in sorted(F["acts"], key=lambda a: a["at"].get("s", 0) if isinstance(a["at"], dict) else a["at"] / 30):
                if a["who"] == who and "face" in a: cur = a["face"]
            pick = next((f for f in faces if f != cur), None)
            dup = any(a["who"] == who and isinstance(a["at"], dict) and abs(a["at"].get("s", -1) - mid_s) < .3 and a.get("face") == pick for a in F["acts"])
            if pick and not dup:
                F["acts"].append({"who": who, "at": {"s": mid_s}, "face": pick}); changed = True
        if vis: print(f"  frozen {flen/30:.1f}s@{f0/30:.1f}s: faces at {mid_s}s for {vis[:2]}")
    # p90: scale travels down while peak ok
    if M["p90"] < 10.2 and M["pk"] <= 55:
        for tk in F["takes"]:
            for st in tk["stations"]:
                if "travel" in st: st["travel"] = round(st["travel"] * .85, 2)
        changed = True; print("  p90: travels x0.85")
    if not changed: break
    F.pop("_perf", None)
    json.dump(F, open(PATH, "w"), ensure_ascii=False, indent=1)
    F = fp.load(PATH)
print("tuner done")
