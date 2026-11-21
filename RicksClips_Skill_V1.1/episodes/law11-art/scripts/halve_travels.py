"""Halve every explicit travel duration in law11-zai (min 0.42 s to stay under the whip
gate) so the hops run ~2x faster and travel p90 rises into its band. Flowing travels
>= 1.5 s and the last station of each take are untouched."""
import json

P = "/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1/episodes/law11-zai/film.json"

film = json.load(open(P))
changed = 0
for take in film["takes"]:
    S = take["stations"]
    at = [s["at"] if isinstance(s["at"], (int, float)) else s["at"].get("s") for s in S]
    for i in range(len(S) - 1):
        nxt = S[i + 1]
        t = nxt.get("travel")
        if t is None or float(t) >= 1.5:
            continue
        gap = at[i + 1] - at[i]
        new = round(max(0.42, float(t) / 2.0), 2)
        if new < float(t):
            nxt["travel"] = new
            # keep the hold cap generous enough that the shorter travel is not clipped
            cap = round(max(0.45, gap - new - 0.05), 2)
            if S[i].get("hold") is not None and S[i]["hold"] > cap:
                S[i]["hold"] = cap
            changed += 1

json.dump(film, open(P, "w"), ensure_ascii=False, indent=1)
print("halved", changed, "travels; saved", P)
