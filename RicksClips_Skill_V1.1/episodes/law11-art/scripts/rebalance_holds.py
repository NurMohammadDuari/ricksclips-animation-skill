"""Rebalance law11-zai holds -> travels: cap every station's hold at (gap - 1.6 s)
so each move into the next station gets >= 1.6 s, matching the skill's 'moving about
68 % of frames' and lifting travel p90. Last station of each take is untouched."""
import json

P = "/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1/episodes/law11-zai/film.json"
TRAVEL_MIN = 1.6
HOLD_MIN = 0.7

film = json.load(open(P))
changed = 0
for take in film["takes"]:
    S = take["stations"]
    at = [s["at"] if isinstance(s["at"], (int, float)) else s["at"].get("s") for s in S]
    for i, s in enumerate(S[:-1]):
        gap = at[i + 1] - at[i]
        cap = max(HOLD_MIN, gap - TRAVEL_MIN)
        if s.get("hold") is not None and s["hold"] > cap:
            s["hold"] = round(cap, 2)
            changed += 1

json.dump(film, open(P, "w"), ensure_ascii=False, indent=1)
print("capped", changed, "holds; saved", P)
