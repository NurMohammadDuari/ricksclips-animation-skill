#!/usr/bin/env python3
"""gen_cast.py - draw NEW characters from the script, not from a fixed list of 150 names.

    python tools/gen_cast.py episodes/<slug> < film_analysis.json

autofilm.py calls `write_cast_sheet(ep, cast, rows, title)` after it has read the script.
The result is an ordinary cast sheet at `episodes/<slug>/cast/sheets/story_cast.mjs` plus a
`CAST.md` that a human can edit. `film.json` then points at that sheet through `puppet_pkg`
and references each new puppet as `cast:story_cast/<role>`.

The sheet uses only spec fields castkit.mjs already understands (form / coat / face / outfit /
outfitPal / hair), so no SVG is written by hand and every character still animates with the kit.
"""
import json, os, re
from collections import Counter

# role word -> (form, size, outfit, coat, hair, face)
ROLES = [
    (("চাচা", "কাকা", "মামা", "uncle", "father", "dad", "বাবা", "মালিক", "boss", "king", "owner"),
     "dad", "fat", "farmer", "#6b7340", None, "proud"),
    (("মা", "আম্মা", "mother", "mom", "wife", "woman", "lady", "girl", "রানি", "queen"),
     "lady", "standard", "sundress", "#3f7a4a", "bob", ["female", "sassy"]),
    (("ছেলে", "বাচ্চা", "শিশু", "kid", "boy", "child", "son", "ভাগ্নে", "nephew"),
     "kid", "standard", "schoolGirl", "#d2a02a", None, "delight"),
    (("বৃদ্ধ", "দাদা", "শিক্ষক", "গুরু", "elder", "teacher", "professor", "বর্ণনাকারী", "narrator"),
     "elder", "standard", "threePiece", "#3a3f8a", "gramps", ["elder", "sweetSmile"]),
    (("জেলে", "মাঝি", "fisherman", "sailor", "নাবিক"),
     "standard", "standard", "sailor", "#2f6fd0", None, "cool"),
    (("ডাক্তার", "doctor", "nurse"),
     "standard", "standard", "doctor", "#efe6cf", None, "standard"),
    (("বৈজ্ঞানিক", "scientist", "researcher"),
     "noodle", "thin", "scientist", "#c9ced6", None, "confused"),
    (("যোদ্ধা", "warrior", "soldier", "সৈনিক"),
     "chad", "fat", "ww2Soldier", "#6b7340", None, "strain"),
    (("মহাজন", "ব্যবসায়ী", "merchant", "trader", "businessman"),
     "standard", "fat", "threePiece", "#7a2434", None, "money"),
    (("রোবট", "robot"),
     "standard", "standard", "robot", "#8e96a4", None, "standard"),
]
COATS = ["#2f6fd0", "#c98a3c", "#3f7a4a", "#7a2434", "#6b3fa0", "#2f8f8a"]


def _has(text, keys):
    low = (text or "").lower()
    return any(k.lower() in low for k in keys)


def role_spec(label, speaker, texts, index, base_form=None):
    """Turn what the script says about a character into a castkit spec."""
    primary = str(speaker or label or "")
    form, size, outfit, coat, hair, face = "standard", "standard", "threePiece", COATS[index % len(COATS)], None, "standard"
    chosen = None
    if base_form and base_form != "standard":       # the body autofilm picked for this slot is the strongest clue
        chosen = next((r for r in ROLES if r[1] == base_form), None)
    if chosen is None:
        chosen = next((r for r in ROLES if _has(primary, r[0])), None)
    if chosen is None and not base_form:
        chosen = next((r for r in ROLES if _has(" ".join(texts[:1]), r[0])), None)
    if chosen:
        _keys, form, size, outfit, coat, hair, face = chosen
    joined = " ".join(texts).lower()
    if _has(joined, ("রাগ", "angry", "গর্জন")):
        face = "rage"
    elif _has(joined, ("কাঁদ", "cry", "কান্না")):
        face = ["female", "mascaraCry"] if form == "lady" else "wail"
    elif _has(joined, ("হাস", "laugh", "হেসে")):
        face = "delight"
    elif _has(joined, ("অবাক", "surprise", "আশ্চর্য")):
        face = "jawdrop"
    elif _has(joined, ("ভয়", "scared", "fear")):
        face = "terrified"
    return {"form": form, "size": size, "outfit": outfit,
            "outfitPal": {"a": coat, "b": "#efe6cf", "c": "#b4542a"},
            "coat": coat, "face": face, **({"hair": hair} if hair else {})}


def js(v):
    return json.dumps(v, ensure_ascii=False)


def write_cast_sheet(ep, cast, rows, title="Generated cast"):
    """Save the characters as an editable module and return the puppet strings for film.json."""
    sheet_dir = os.path.join(ep, "cast", "sheets")
    os.makedirs(sheet_dir, exist_ok=True)
    sheet_path = os.path.join(sheet_dir, "story_cast.mjs")
    role_texts = {who: [] for who in cast}
    speakers = {who: Counter() for who in cast}
    for r in rows:
        who = r.get("who")
        if who in role_texts:
            role_texts[who].append(r.get("text", ""))
            if r.get("speaker"):
                speakers[who][r["speaker"]] += 1
    specs, lines = [], []
    for i, who in enumerate(cast):
        named = [(k, v) for k, v in speakers[who].items()
                 if not any(x in k.lower() for x in ("বর্ণনাকারী", "narrator", "voiceover"))]
        label = (max(named, key=lambda kv: kv[1])[0] if named else
                 (speakers[who].most_common(1)[0][0] if speakers[who] else who))
        puppet = str(cast[who].get("puppet", ""))
        bf = puppet.split(":")[1] if puppet.startswith("form:") else None
        spec = role_spec(label, label, role_texts[who], i, bf)
        spec.update({"name": who, "label": label})
        specs.append(spec)
        lines.append("  " + js(spec) + ",")
    body = ("// GENERATED by tools/gen_cast.py from the script - edit freely, then re-check the film.\n"
            "export const TITLE = %s;\n\nexport const CAST = [\n%s\n];\n"
            % (js(title), "\n".join(lines)))
    with open(sheet_path, "w", encoding="utf-8") as f:
        f.write(body)
    for i, who in enumerate(cast):
        cast[who]["puppet"] = "cast:story_cast/" + who
        cast[who]["new_character"] = specs[i]
    with open(os.path.join(ep, "CAST.md"), "w", encoding="utf-8") as f:
        f.write("# New characters for %s\n\n" % title)
        f.write("`tools/gen_cast.py` read the script's speakers and role words and wrote "
                "`cast/sheets/story_cast.mjs`. These are ordinary castkit specs — change any "
                "`form`, `outfit`, `coat`, `face` or `hair` and re-run the check.\n\n")
        f.write("| role | speaker in script | form | outfit | face |\n|---|---|---|---|---|\n")
        for s in specs:
            face = s["face"]
            if isinstance(face, list):
                face = "/".join(face)
            f.write("| `%s` | %s | %s | %s | %s |\n" %
                    (s["name"], s["label"], s["form"], s["outfit"], face))
    return ["cast:story_cast/" + who for who in cast]


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Create a new cast sheet from a script analysis JSON.")
    ap.add_argument("episode")
    ap.add_argument("analysis", help="JSON with cast, rows and title")
    a = ap.parse_args()
    d = json.load(open(a.analysis, encoding="utf-8"))
    write_cast_sheet(a.episode, d["cast"], d["rows"], d.get("title", "Generated cast"))
    print("saved %s" % os.path.join(a.episode, "cast", "sheets", "story_cast.mjs"))


if __name__ == "__main__":
    main()
