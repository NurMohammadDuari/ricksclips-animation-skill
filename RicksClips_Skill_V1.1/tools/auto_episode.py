#!/usr/bin/env python3
"""auto_episode.py — first-pass DIRECTOR: narration text -> film.json draft
that follows the RicksClips3000 Style DNA, ready for `film_plan.py check` and
for the AI artist to refine with real sets/cast.

    python tools/auto_episode.py --script story.txt --title "My Film" \
        [--mode A|B] [--words voice/words.json] [--out episodes/my-film/film.json]

What it does
  1. sentences: one row per script line, word indices, nouns picked by a
     stopword filter (subject defaults to "hero" for the artist to rename).
  2. words.json: reuses --words when given, else estimates timing at ~2.8
     words/s (inside the DNA 1.6-4.0 band).
  3. structure: Mode A (one-shot journey) or Mode B (scene-cut story, default
     for 6+ sentences). Mode B groups 2-3 sentences per scene/place; cuts land
     ONLY on scene boundaries.
  4. scenes: each scene picks a DNA grade recipe by keyword (fire/mine/gold ->
     warm, night/road/storm -> cool, space/star -> dark, else bright day) and
     gets its own place key + mood look.
  5. stations: word-timed, lens 24, hold 0.6-0.9 s, travel 0.4-0.5 s, framing
     cycling W/M/P/C/O toward the DNA shot mix; whole-body rests sit 2.4 m
     from the subject at head height (the gates' own convention).
  6. acting/fx/sound/kicks: beat on every content word (>= 4 acting changes
     per 10 s), an fx + sound + kick on the sentence-final action word.
  7. writes out/plan/auto_draft.md: per-scene staging questions for the artist.

The draft is a STARTING PLAN, not a finished episode: coordinates are generic
staging around the subject; the artist replaces them with the real set layout,
cast names and props, then re-runs film_plan.py check until 0 FAIL.
"""
import argparse
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DNA_PATH = os.path.join(HERE, "..", "library", "style", "ricksclips-dna", "style_params.json")

STOP = set("the a an of to in on at for with and or but so then that this those these is are was were be been "
           "it its as by from into out up down over under his her their they he she you i we my your our them "
           "one two not no did do does done had has have will would can could just very really when what which "
           "who whom how why where all any some more most about after before between during if because".split())

WARM_KW = ("mine fire gold torch forge sun desert dawn volcano lava oven kitchen forge")
COOL_KW = ("night road storm rain snow ice sea ocean cold asphalt city dusk")
DARK_KW = ("space star planet astronaut void cosmic moon")
LOOKS = {"warm": "torch_warm", "cool": "cold_blue", "dark": "deep_void", "day": "bright_day"}


def load_dna():
    with open(DNA_PATH) as f:
        return json.load(f)


def recipe_for(text):
    t = text.lower()
    if any(k in t for k in DARK_KW.split()):
        return "dark", LOOKS["dark"]
    if any(k in t for k in COOL_KW.split()):
        return "cool", LOOKS["cool"]
    if any(k in t for k in WARM_KW.split()):
        return "warm", LOOKS["warm"]
    return "day", LOOKS["day"]


def estimate_words(lines):
    out, i = [], 0
    for ln in lines:
        for w in ln.split():
            dur = 0.30 + (0.10 if len(w) > 7 else 0.0)
            out.append({"w": w, "s": round(i, 2), "e": round(i + dur, 2)})
            i += dur + 0.14
        i += 0.45
    return out


def content(ws):
    return [w for w in ws if re.sub(r"[^a-z0-9']", "", w.lower()) not in STOP and len(w) > 1]


def main():
    dna = load_dna()
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--script", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--mode", choices=["A", "B"], default=None)
    p.add_argument("--words", default=None)
    p.add_argument("--out", required=True)
    args = p.parse_args()

    lines = [ln.strip() for ln in open(args.script, encoding="utf-8") if ln.strip()]
    mode = args.mode or ("B" if len(lines) >= 6 else "A")
    outdir = os.path.dirname(os.path.abspath(args.out))
    os.makedirs(outdir, exist_ok=True)
    os.makedirs(os.path.join(outdir, "out", "plan"), exist_ok=True)

    # words
    if args.words and os.path.exists(args.words):
        words = json.load(open(args.words, encoding="utf-8"))
        wsrc = os.path.relpath(args.words, outdir)
    else:
        words = estimate_words(lines)
        wsrc = "voice/words.json"
        os.makedirs(os.path.join(outdir, "voice"), exist_ok=True)
        json.dump(words, open(os.path.join(outdir, "voice", "words.json"), "w"))

    # word index lookup per line
    flat = [w["w"] for w in words]
    fi = 0
    sents = []
    for ln in lines:
        toks = ln.split()
        found = None
        for j in range(fi, len(flat) - len(toks) + 1):
            if [x.strip(" .,?!").lower() for x in flat[j:j + len(toks)]] == [x.strip(" .,?!").lower() for x in toks]:
                found = j
                break
        if found is None:
            found = fi
        fi = found + len(toks)
        cw = content(toks)
        sents.append({"text": ln, "words": [found, fi - 1], "subject": "hero",
                      "nouns": [{"word": re.sub(r"[^a-z0-9']", "", w.lower()), "show": "hero"}
                                for w in cw[:2]]})

    end_s = words[-1]["e"] + 0.8
    fps = 30
    end = int(round(end_s * fps))

    # scenes
    scenes = []
    if mode == "A":
        scenes = [{"lines": list(range(len(lines))), "place": "world_day"}]
        # mode A still re-grades: split into 3 acts on one place entry each
        third = max(1, len(lines) // 3)
        scenes = []
        for k in range(3):
            lo = k * third
            hi = len(lines) if k == 2 else (k + 1) * third
            kind, look = recipe_for(" ".join(lines[lo:hi]))
            scenes.append({"lines": list(range(lo, hi)), "place": f"world_act{k+1}", "kind": kind, "look": look})
    else:
        k = 0
        while k < len(lines):
            grp = lines[k:k + 2]
            if k + 2 < len(lines) and len(lines) - (k + 2) >= 2:
                grp = lines[k:k + 3]
            kind, look = recipe_for(" ".join(grp))
            scenes.append({"lines": list(range(k, k + len(grp))), "place": f"scene_{k//3+1}",
                           "kind": kind, "look": look})
            k += len(grp)

    places, moods, takes, acts, fx, sound, kicks, props = {}, [], [], [], [], [], [], {}
    FR = ["W", "M", "P", "W", "C", "W", "O", "M", "W", "P"]  # -> W40 M20 P20 C10 O10, DNA shot mix
    FPOS = {"W": 2.4, "M": 1.6, "C": 1.0, "P": 3.6, "O": 0.9}
    POSES = ["stand", "point_out", "hold_watch", "hands_hips", "hold_out", "flinch"]
    FACES = ["cool", "k:happy", "k:shocked", "k:skeptical", "k:excited", "k:worried", "k:concentrate"]
    act_i = 0
    fidx = 0

    for si, sc in enumerate(scenes):
        places[sc["place"]] = {"look": sc["look"], "recipe": dna["grade"]["scene_recipes"].get(
            {"warm": "fire_or_mine_warm", "cool": "night_or_road_cool", "dark": "space_dark"}.get(sc["kind"], "bright_day"))}
        first_word_s = float(words[sents[sc["lines"][0]]["words"][0]]["s"])
        moods.append({"at": {"s": round(first_word_s, 2)}, "look": sc["look"]})
        st = []
        for li in sc["lines"]:
            sent = sents[li]
            w0, w1 = sent["words"]
            cws = [words[j] for j in range(w0, w1 + 1) if words[j]["w"].strip(" .,?!").lower() not in STOP]
            beats = cws or [words[w0]]
            for bi, bw in enumerate(beats):
                fr = FR[fidx % len(FR)]
                fidx += 1
                dist = FPOS[fr]
                ang = (bi * 0.6 + si) % 3.14 - 1.57
                st.append({
                    "at": {"s": round(float(bw["s"]), 2)},
                    "pos": [round(0.5 * (1 if fr in "CW" else -1) + 0.3 * bi, 2), round(dist, 2), round(1.25 if fr == "C" else 1.5, 2)],
                    "aim": [0.0, 0.0, 1.42 if fr != "P" else 1.0],
                    "lens": 24, "subject": "hero",
                    "framing": fr,
                    "shows": [n["show"] for n in sent["nouns"][:2]] or ["hero"],
                    "hold": round(0.75 + 0.3 * ((bi + si) % 2), 2),
                    "travel": 0.75,
                })
                acts.append({"who": "hero", "at": {"s": round(float(bw["s"]), 2)},
                             "pos": [0.0, 0.0, 0.0], "visible": True,
                             "pose": POSES[act_i % len(POSES)], "face": FACES[act_i % len(FACES)]})
                act_i += 1
            # acting beat: brow change + fx/sound on sentence-final content word
            last = beats[-1]
            fx.append({"at": {"s": round(float(last["e"]), 2)}, "kind": "glint", "on": "hero"})
            sound.append({"at": {"s": round(float(last["e"]), 2)}, "name": "beat"})
            kicks.append({"at": {"s": round(float(last["e"]), 2)}, "amp": 1.2})
        takes.append({"id": f"t{si+1}", "place": sc["place"], "stations": st})

    film = {
        "title": args.title, "fps": fps, "size": [1080, 1920], "end": end,
        "words": wsrc, "sentences": sents, "takes": takes, "acts": acts,
        "moods": moods, "fx": fx, "sound": sound, "kicks": kicks,
        "places": places,
        "cast": {"hero": {"puppet": "cast:hero", "height": 1.68, "heads_tall": 2.7}}, "props": props,
        "camera_idea": {"name": "dna-draft",
                        "why": f"auto_episode draft, mode {mode}: rest on the noun, travel on the verb",
                        "signature": "one long flowing move per act (mode A) / scene-cut travel (mode B)"},
    }

    json.dump(film, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # staging notes
    md = [f"# auto_draft — {args.title}", "",
          f"- mode: **{mode}** ({'one-shot journey' if mode == 'A' else 'scene-cut story'})",
          f"- scenes: {len(scenes)} | sentences: {len(sents)} | words: {len(words)} | end: {end} f ({end_s:.1f} s)",
          "- grades follow DNA scene_recipes; replace generic staging with the real set.", ""]
    for si, sc in enumerate(scenes):
        md += [f"## take t{si+1} — place `{sc['place']}` look `{sc['look']}`",
               f"- lines: {' / '.join(lines[i] for i in sc['lines'])}",
               "- artist questions: what real set? who is on screen? what diegetic sign carries the turn here?",
               "- replace station pos/aim with real set coordinates; rename subject from `hero`.", ""]
    open(os.path.join(outdir, "out", "plan", "auto_draft.md"), "w", encoding="utf-8").write("\n".join(md))

    print(f"wrote {args.out}")
    print(f"mode {mode}, {len(scenes)} scenes, {len(takes)} takes, {len(sents)} sentences, "
          f"{sum(len(t['stations']) for t in takes)} stations, end {end} f")
    print("next: python tools/film_plan.py check " + args.out)
    print("      python tools/style_check.py --film " + args.out)


if __name__ == "__main__":
    main()
