"""Fast-travel pass for law11-zai: on transitions with gap >= 1.2 s and hold > 0.9 s,
set the next station's explicit travel to 0.40 s and shrink this station's hold to
gap - 0.45, so the bake renders 12-frame fast hops (speed p90 rises toward the 15-27
target). Transitions already carrying a flowing travel >= 1.5 s are left alone."""
import json

P = "/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1/episodes/law11-zai/film.json"

film = json.load(open(P))
changed = 0
for take in film["takes"]:
    S = take["stations"]
    at = [s["at"] if isinstance(s["at"], (int, float)) else s["at"].get("s") for s in S]
    for i in range(len(S) - 1):
        gap = at[i + 1] - at[i]
        nxt, cur = S[i + 1], S[i]
        if gap < 1.2 or cur.get("hold", 0) is None or cur["hold"] <= 0.9:
            continue
        if float(nxt.get("travel", 0)) >= 1.5:      # keep the flowing moves flowing
            continue
        cur["hold"] = round(gap - 0.45, 2)
        nxt["travel"] = 0.40
        changed += 1

json.dump(film, open(P, "w"), ensure_ascii=False, indent=1)
print("fast-traveled", changed, "transitions; saved", P)
