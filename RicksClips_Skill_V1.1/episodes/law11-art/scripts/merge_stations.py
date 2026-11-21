"""Merge station-hopping runs in law11-zai/film.json: consecutive stations with the
same framing + subject and no word anchor become one station (keep the first, union
the shows lists, drop the rest). The next kept station's `at` stays, so the travel
into it automatically lengthens (the bake derives travel = gap - hold)."""
import json

P = "/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1/episodes/law11-zai/film.json"

RUNS = {  # take id -> list of maximal runs [i..j] to merge (keep i)
    "t1": [[5, 6, 7], [13, 14, 15]],
    "t2": [[0, 1], [12, 13, 14]],
    "t3": [[5, 6, 7], [8, 9], [13, 14, 15]],
    "t4": [[5, 6, 7]],
}

film = json.load(open(P))
dropped = 0
for take in film["takes"]:
    runs = RUNS.get(take["id"], [])
    if not runs:
        continue
    kill = set()
    for run in runs:
        keeper = take["stations"][run[0]]
        for idx in run[1:]:
            gone = take["stations"][idx]
            for s in gone.get("shows", []):
                if s not in keeper.get("shows", []):
                    keeper.setdefault("shows", []).append(s)
            kill.add(idx)
        # the keeper's hold may need to stretch: cap it at the whole run span so the
        # bake leaves room for a flowing travel into the next kept station
        nxt = run[-1] + 1
        if nxt < len(take["stations"]):
            at_of = lambda s: s["at"] if isinstance(s["at"], (int, float)) else s["at"].get("s")
            span = at_of(take["stations"][nxt]) - at_of(keeper)
            if keeper.get("hold", 0) is not None and keeper["hold"] > span - 0.9:
                keeper["hold"] = round(max(0.6, span - 0.9), 2)
    take["stations"] = [s for i, s in enumerate(take["stations"]) if i not in kill]
    dropped += len(kill)

json.dump(film, open(P, "w"), ensure_ascii=False, indent=1)
print("dropped", dropped, "stations; saved", P)
