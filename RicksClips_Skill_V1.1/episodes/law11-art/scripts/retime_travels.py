"""Give law11-zai travels real speed: short gaps (< 2.5 s) get fast 0.5 s hops into the
next station (speed up -> travel p90 rises), long gaps get flowing ~2 s moves. The bake
renders travel = min(next station's explicit travel, gap - this station's hold), so BOTH
knobs must be set. Keeps plan speed peak under the 60 px/f gate by not going below 0.42 s."""
import json

P = "/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1/episodes/law11-zai/film.json"

film = json.load(open(P))
changed = 0
for take in film["takes"]:
    S = take["stations"]
    at = [s["at"] if isinstance(s["at"], (int, float)) else s["at"].get("s") for s in S]
    for i in range(len(S) - 1):
        gap = at[i + 1] - at[i]
        want = 0.5 if gap < 2.5 else max(1.8, min(2.0, gap - 0.8))
        want = max(want, 0.42)
        nxt = S[i + 1]
        cur_travel = float(nxt.get("travel", 0.9))
        new_travel = min(max(cur_travel, want), max(0.42, gap - 0.45))
        hold_cap = max(0.45, gap - new_travel - 0.05)
        if S[i].get("hold") is not None and S[i]["hold"] > hold_cap:
            S[i]["hold"] = round(hold_cap, 2)
        if new_travel > cur_travel + 0.01 or abs(new_travel - cur_travel) > 0.01:
            if abs(new_travel - want) > 0.01 or new_travel < cur_travel - 0.01:
                nxt["travel"] = round(new_travel, 2)
                changed += 1

json.dump(film, open(P, "w"), ensure_ascii=False, indent=1)
print("retimed", changed, "travels; saved", P)
