#!/usr/bin/env python3
"""autofilm.py - any script in, a complete playable episode out.

    python tools/autofilm.py episodes/<slug> --script story.txt
    python tools/autofilm.py episodes/<slug> --script "one line of text" --title "..."
    python tools/autofilm.py episodes/<slug> --script story.txt --words voice/words.json

Nothing here is hard-coded to one episode. For WHATEVER script it is given, the tool:

  1. splits the script into sentences and times every word (real words.json, or a speech-like track)
  2. reads the topic with Bangla + English lexicons: places, characters, props, actions, emotions
  3. BUILDS the sets it needs and SAVES them as normal editable modules in episodes/<slug>/sets/
     (each one is a small data wrapper around the shared templates/threejs_film/sets/place_kit.js)
  4. places the cast on the floor in stage slots, LEVELS a 24 mm camera to each subject's own height
     (whole body / medium / close / place), and writes the camera travels between the beats
  5. writes film.json (takes, stations, acts, moods, fx, sound, sentences) and SCRIPT.md + SETS.md
  6. runs tools/film_plan.py check and repairs the plan until it has NO FAIL (WARNs are reported in CAMERA_NOTE.md)

The result is an ordinary episode: edit film.json or any saved set and use the normal pipeline
(film_plan.py check -> render.mjs --storyboard / --animatic / --frames).
"""
import argparse, json, math, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))     # RicksClips_Skill_V1.1
KIT = os.path.join(ROOT, "templates", "threejs_film")
FPS = 30
HEADS_TALL = 2.8
HEAD_ASPECT = 0.95

# --------------------------------------------------------------------------- lexicons
PLACE_WORDS = [
    (("বন", "জঙ্গল", "মাঠ", "গ্রাম", "বাগান", "খেত", "সমুদ্র", "পাহাড়", "নদী", "ঘাট", "forest", "jungle", "field", "village", "garden", "sea", "mountain", "river", "shore"), "field", "earth"),
    (("দোকান", "বাজার", "হাট", "shop", "market", "store", "bazaar"), "market", "warm"),
    (("ঘর", "বাসা", "বাড়ি", "কামরা", "গুহা", "ঘরে", "home", "house", "room", "cave", "den", "hut"), "room", "warm"),
    (("অফিস", "দফতর", "আদালত", "দরবার", "রাজপ্রাসাদ", "প্রাসাদ", "সভা", "office", "court", "palace", "throne", "chamber"), "office", "royal"),
    (("রান্নাঘর", "রান্না", "হেঁশেল", "kitchen", "cook", "hearth"), "kitchen", "warm"),
    (("স্কুল", "ক্লাস", "শ্রেণি", "মাদ্রাসা", "বিদ্যালয়", "school", "class", "college", "lesson"), "class", "cool"),
    (("রাস্তা", "পথ", "মোড়", "চত্বর", "গলি", "street", "road", "square", "alley", "lane"), "street", "cool"),
    (("স্টেশন", "রেল", "ট্রেন", "প্লাটফর্ম", "station", "train", "platform", "railway"), "station", "cool"),
]

# Only puppets whose sheets carry no baked-in lettering (no "SELL!!" / "BILL" stickers).
CAST_WORDS = [
    (("চাচা", "কাকা", "মামা", "uncle", "father", "বাবা", "আব্বা"), "form:dad", 1.70),
    (("মা", "আম্মা", "মায়ের", "স্ত্রী", "বউ", "মেয়ে", "রানি", "mother", "mom", "wife", "queen", "woman", "lady", "girl"), "form:lady", 1.60),
    (("ভাগ্নে", "ছেলে", "পোলা", "শিশু", "বাচ্চা", "নাতি", "kid", "boy", "child", "son", "nephew", "grandson"), "form:kid", 1.20),
    (("মালিক", "রাজা", "বাদশা", "সাহেব", "বস", "king", "boss", "owner", "master", "lord"), "cast:king", 1.74),
    (("কর্মী", "চাকর", "সৈনিক", "পাহারাদার", "worker", "servant", "soldier", "guard"), "cast:scout", 1.52),
    (("বন্ধু", "সঙ্গী", "সাথী", "friend", "companion", "mate"), "form:standard", 1.70),
    (("শিক্ষক", "গুরু", "পুরোহিত", "বৃদ্ধ", "দাদা", "teacher", "guru", "priest", "elder", "old man"), "form:elder", 1.68),
    (("জেলে", "মাঝি", "নাবিক", "fisher", "fisherman", "sailor", "boatman", "keeper"), "cast:sailor", 1.68),
    (("ডাক্তার", "doctor", "nurse", "সেবিকা"), "form:standard", 1.66),
    (("বৈজ্ঞানিক", "গবেষক", "scientist", "researcher", "professor"), "cast:scientist", 1.70),
    (("শিক্ষার্থী", "ছাত্র", "student", "pupil"), "cast:scholar", 1.64),
    (("যোদ্ধা", "সেনাপতি", "warrior", "fighter", "knight", "samurai"), "cast:samurai", 1.72),
    (("ব্যবসায়ী", "মহাজন", "merchant", "trader", "businessman"), "cast:prospector", 1.72),
    (("নায়ক", "রাফি", "hero", "protagonist"), "form:standard", 1.70),
    (("রobot", "robot", "রোবট"), "cast:robot", 1.70),
]

PROP_WORDS = [
    (("খাতা", "বই", "ডায়েরি", "book", "notebook", "ledger", "diary"), "khata", "notebook"),
    (("টাকা", "পয়সা", "মুদ্রা", "money", "cash", "coin", "gold", "sona", "সোনা"), "coin", "coin"),
    (("চিঠি", "letter", "note", "message"), "letter", "letter"),
    (("বাক্স", "প্যাকেট", "মিষ্টি", "box", "packet", "parcel", "sweet", "chest"), "box", "box"),
    (("ফোন", "phone", "mobile"), "phone", "phone"),
    (("কলম", "pen", "pencil"), "pen", "pen"),
    (("তলোয়ার", "sword", "knife", "ছুরি"), "sword", "sword"),
    (("ওষুধ", "medicine", "bottle", "বোতল"), "bottle", "bottle"),
    (("জাল", "net", "rope", "দড়ি"), "net", "net"),
    (("ভাত", "খাবার", "food", "rice", "bowl"), "bowl", "bowl"),
    (("চা", "tea", "cup"), "tea", "cup"),
    (("মাছ", "fish", "মৎস্য"), "fish", "fish"),
]

FACES = [
    ("anger", "angryFist", ("রাগ", "রাগে", "গর্জন", "মারবি", "মারবে", "চোর", "angry", "furious", "roar")),
    ("laugh", "giggle", ("হাসি", "হেসে", "হাসে", "ঠাট্টা", "laugh", "joke", "smile")),
    ("cry", "wail", ("কাঁদ", "কান্না", "কেঁদে", "cry", "weep", "tears")),
    ("fear", "amazed", ("ভয়", "ভীত", "আতঙ্ক", "scared", "afraid", "fear", "terror")),
    ("surprise", "amazed", ("অবাক", "আশ্চর্য", "surprise", "amazed", "sudden")),
    ("greed", "money", ("লোভ", "greed", "profit", "লাভ")),
    ("proud", "proud", ("গর্ব", "গর্বিত", "proud", "victory", "জিত")),
    ("sad", "deadInside", ("দুঃখ", "কষ্ট", "sad", "sorrow", "হারিয়ে")),
    ("smug", "smug", ("চালাক", "ধূর্ত", "smug", "clever", "trick")),
    ("confused", "confused", ("বুঝ", "confused", "puzzle", "কেন")),
]
FACE_CYCLE = ["cool", "proud", "standard", "curious", "sweetSmile", "smug", "judging", "delight"]

POSE_RULES = [
    (("লেখ", "লিখ", "write", "note", "sign"), "write"),
    (("ধর", "ধরে", "grab", "hold", "catch"), "hold_out"),
    (("দেখ", "দেখা", "show", "look", "দেখল", "তাক", "stare", "watch"), "point_up"),
    (("বল", "বলে", "say", "tell", "shout", "চিৎকার", "ডাক"), "point_out"),
    (("হাত", "hands", "pray", "প্রার্থনা"), "hands_hips"),
    (("দৌড়", "ছুট", "run", "chase"), "lean_in"),
    (("খোঁজ", "তালাশ", "search", "find"), "bend_down"),
    (("ঘুম", "sleep", "rest"), "crouch"),
    (("মুক্ত", "free", "release", "জিত", "win", "celebrate"), "cheer"),
    (("কাট", "cut", "break", "ভাঙ", "push", "ঠেল"), "push"),
    (("কাঁদ", "cry", "weep"), "hand_mouth"),
    (("হাস", "laugh", "joke"), "clap"),
    (("শুন", "listen", "hear"), "lean_in"),
]

MOODS = ["warm_up", "spot_hero", "cool_blue", "gold_wash", "flash_red", "warm_glow"]
FX_KINDS = ["glow", "glint", "dust_hit", "paper_flutter", "coin_glint", "dust_puff"]


# --------------------------------------------------------------------------- text
def split_sentences(text):
    t = " ".join(str(text).split())
    parts = re.split(r"(?<=[।!?\.])\s+|\n+", t)
    out = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if out and len(p.split()) < 3:
            out[-1] = out[-1] + " " + p
        else:
            out.append(p)
    return out


WORD_RE = re.compile(r"[0-9\u0980-\u09FFA-Za-z]+(?:['’\-][0-9\u0980-\u09FFA-Za-z]+)*")


def words_of(sentence):
    return WORD_RE.findall(sentence)


def synth_words(sentences):
    """Even, speech-like timing: ~0.19 s + 0.035 s per letter, a breath at every full stop."""
    out, t = [], 0.15
    for s in sentences:
        for w in words_of(s):
            dur = max(0.24, min(0.66, 0.18 + 0.032 * len(w)))
            out.append({"w": w, "s": round(t, 2), "e": round(t + dur, 2)})
            t += dur
        t += 0.34
    if out:
        out[-1]["e"] = round(out[-1]["e"] + 0.25, 2)
    return out


def fit_to_sentences(words, sentences):
    """Real timings but the script may phrase it differently: split the word list by the sentence lengths."""
    counts = [max(1, len(words_of(s))) for s in sentences]
    total = sum(counts)
    n = len(words)
    if total == n:
        bounds, acc = [], 0
        for c in counts:
            bounds.append((acc, acc + c - 1)); acc += c
        return bounds
    bounds, acc = [], 0
    for i, c in enumerate(counts):
        a = min(n - 1, round(acc / total * n)); acc += c
        b = min(n - 1, round(acc / total * n) - 1) if i < len(counts) - 1 else n - 1
        bounds.append((a, max(a, b)))
    return bounds


def has(text, keys):
    low = text.lower()
    return any(k.lower() in low for k in keys)


def find_first(text, table):
    low = text.lower(); best = None
    for row in table:
        for k in row[0]:
            i = low.find(k.lower())
            if i >= 0 and (best is None or i < best[0]):
                best = (i, row)
    return best[1] if best else None


# --------------------------------------------------------------------------- analysis
def analyse(sentences):
    rows = []
    for s in sentences:
        pl = find_first(s, PLACE_WORDS)
        prop = find_first(s, PROP_WORDS)
        cast = find_first(s, CAST_WORDS)
        face = None
        for name, f, keys in FACES:
            if has(s, keys):
                face = (name, f); break
        pose = "stand"
        for keys, p in POSE_RULES:
            if has(s, keys):
                pose = p; break
        rows.append(dict(text=s, place=pl[1] if pl else None, palette=pl[2] if pl else None,
                         prop=(prop[1], prop[2]) if prop else None,
                         cast=(cast[1], cast[2]) if cast else None,
                         face=face, pose=pose))
    return rows


def build_cast(rows):
    counts = {}
    for r in rows:
        if r["cast"]:
            counts[r["cast"]] = counts.get(r["cast"], 0) + 1
    chosen = []
    for (puppet, height), _n in sorted(counts.items(), key=lambda kv: -kv[1]):
        if all(p != puppet for p, _ in chosen):
            chosen.append((puppet, height))
    defaults = [("form:standard", 1.70), ("form:lady", 1.60), ("form:kid", 1.20), ("form:dad", 1.70)]
    for d in defaults:
        if len(chosen) >= 3:
            break
        if all(p != d[0] for p, _ in chosen):
            chosen.append(d)
    names = ["hero", "partner", "other"]
    cast = {}
    for (puppet, height), nm in zip(chosen[:3], names):
        cast[nm] = {"puppet": puppet, "height": height,
                    "heads_tall": 2.4 if height <= 1.3 else 2.8,
                    "head_aspect": HEAD_ASPECT}
    for r in rows:
        r["who"] = "hero"
        if r["cast"]:
            for nm, c in cast.items():
                if c["puppet"] == r["cast"][0]:
                    r["who"] = nm; break
    return cast


# --------------------------------------------------------------------------- sets (data)
SIZES = {"street": [22, 22], "field": [24, 22], "station": [16, 20], "market": [14, 10]}
OUTDOOR = ("street", "field", "station", "market")


def clear_stage(furniture, kind):
    """Keep the acting area clear: no table/stall/crate may stand between the lens and the cast.
    Steps are the exception - they are deliberately under a short character's feet."""
    out = []
    sy = STAGE_Y.get(kind, 0.65)
    for f in furniture:
        if f["kind"] in ("rug", "step"):
            out.append(f); continue
        x, y = f["at"][0], f["at"][1]
        if abs(x) < 2.5 and y < sy + 1.45:                 # in front of / on top of a stage slot
            x = -3.3 if x <= 0 else 3.3
            y = max(y, sy + 2.25)
            f = dict(f, at=[round(x, 2), round(y, 2)])
        out.append(f)
    return out


def layout_for(kind, palette, seed, variant=0):
    """Everything the set needs, as data. Furniture positions are explicit so Python knows the floor plan."""
    W, D = SIZES.get(kind, [9, 7])
    F = []
    door = "right"
    if kind == "room":
        F = [dict(kind="table", at=[0.4, 2.75], rot=0), dict(kind="chair", at=[-0.5, 3.15], rot=0),
             dict(kind="shelf", at=[-3.0, 2.65], rot=0), dict(kind="plant", at=[3.0, 2.05]),
             dict(kind="lamp", at=[2.85, 1.55]), dict(kind="rug", at=[0.0, 1.15])]
    elif kind in ("shop", "market"):
        F = [dict(kind="counter", at=[0.0, 2.45], rot=0), dict(kind="shelf", at=[0.0, 3.15], rot=0),
             dict(kind="sacks", at=[-3.0, 2.4]), dict(kind="crate", at=[3.0, 2.3])] if kind == "shop" else \
            [dict(kind="stall", at=[-2.7, 2.35], rot=0), dict(kind="stall", at=[2.7, 2.35], rot=0),
             dict(kind="crate", at=[-1.2, 1.85]), dict(kind="sacks", at=[1.15, 2.05])]
    elif kind == "office":
        F = [dict(kind="desk", at=[0.3, 2.85], rot=0), dict(kind="chair", at=[0.3, 3.3], rot=0),
             dict(kind="cupboard", at=[-3.0, 2.75], rot=0), dict(kind="plant", at=[3.0, 2.1]),
             dict(kind="lamp", at=[2.9, 1.6])]
    elif kind == "kitchen":
        F = [dict(kind="stove", at=[-2.4, 2.9], rot=0), dict(kind="counter", at=[1.0, 3.0], rot=0),
             dict(kind="table", at=[1.8, 2.15], rot=0), dict(kind="shelf", at=[-3.2, 2.35], rot=0)]
    elif kind == "class":
        F = [dict(kind="blackboard", at=[0.0, 3.35]), dict(kind="desk", at=[-1.8, 2.65], rot=0),
             dict(kind="chair", at=[-1.8, 3.15], rot=0), dict(kind="bench", at=[1.7, 2.55], rot=0)]
    elif kind == "street":
        F = [dict(kind="lamp", at=[-5.0, 1.45]), dict(kind="bench", at=[4.2, 2.15], rot=0),
             dict(kind="crate", at=[2.4, 2.75])]
    elif kind == "field":
        F = [dict(kind="crate", at=[2.2, 2.4])]
    elif kind == "station":
        F = [dict(kind="bench", at=[3.0, 3.2], rot=0), dict(kind="crate", at=[-4.0, 2.5])]
    if variant:                                    # a second view of the same place: fewer, differently placed props
        F = F[1:] if len(F) > 2 else F
        for i, f in enumerate(F):
            f["at"] = [f["at"][0] * 0.8, f["at"][1] + 0.1 * (i % 2)]
    if kind in ("room", "office", "kitchen", "class", "shop"):
        F.append(dict(kind="rug", at=[0.0, -0.30]))          # something under the camera's feet in a wide shot
    F = clear_stage(F, kind)
    layout = {"kind": kind, "palette": palette, "size": [W, D], "door": door,
              "furniture": F, "seed": seed, "goods": "fruit" if kind == "market" else "jars"}
    return layout


FEATURES = {
    "room": ("window", "back"), "shop": ("counter", "counter"), "market": ("stall", "stall"),
    "office": ("desk", "desk"), "kitchen": ("stove", "stove"), "class": ("board", "board"),
    "street": ("street", "street"), "field": ("field", "field"), "station": ("clock", "clock"),
}


def feature_point(kind, layout):
    """World point of the set object a place frame is built around."""
    W, D = layout["size"]
    if kind == "room":
        return [-W * 0.28, D / 2 - 1.0, 1.30, "window"]
    if kind in ("shop", "market"):
        f = next((f for f in layout["furniture"] if f["kind"] in ("counter", "stall")), None)
        x, y = (f["at"] if f else (0, 2.4))
        return [x, y, 1.05, "counter" if kind == "shop" else "stall"]
    if kind == "office":
        return [0.3, 2.85, 0.80, "desk"]
    if kind == "kitchen":
        return [-2.4, 2.9, 0.90, "stove"]
    if kind == "class":
        return [0.0, 3.3, 1.65, "board"]
    if kind == "street":
        return [0.0, 4.0, 1.20, "street"]
    if kind == "field":
        return [0.0, 3.0, 0.80, "field"]
    if kind == "station":
        return [-3.0, 3.4, 1.40, "clock"]
    return [0.0, 2.6, 1.20, "table"]


def build_places(rows, slug, cast=None):
    """Four places from the topic: the story's own place, a second one, and two more views/lights of them.
    Short characters get a low step built into every floor plan, so their face is not lost under the captions."""
    counts = {}
    for r in rows:
        if r["place"]:
            counts[r["place"]] = counts.get(r["place"], 0) + 1
    primary = max(counts, key=counts.get) if counts else "room"
    secondary = next((k for k in counts if k != primary), None) or ("street" if primary != "street" else "field")
    first = "morning" if primary in OUTDOOR else "interior"
    lights = [first, "golden", "day", "night"]
    palettes = ["warm", "earth", "cool", "royal" if primary in OUTDOOR else "warm"]
    kinds = [primary, secondary, primary, secondary]
    places = []
    for i in range(4):
        kind = kinds[i]
        lay = layout_for(kind, palettes[i], seed=3 + i, variant=1 if i in (1, 3) else 0)
        places.append(dict(name="p%d" % (i + 1), kind=kind, light=lights[i], palette=palettes[i],
                           layout=lay, feature=feature_point(kind, lay), variant=1 if i in (1, 3) else 0))
    if cast:
        sy0 = STAGE_Y.get(primary, 0.65)
        for who, c in cast.items():
            if c["height"] >= 1.5:
                continue
            x, y = SLOTS[who][0], (sy0 if who == "hero" else sy0 + 0.70)
            for p in places:
                lay = p["layout"]
                yk = (STAGE_Y.get(p["kind"], 0.65) if who == "hero" else STAGE_Y.get(p["kind"], 0.65) + 0.70)
                lay["furniture"].append(dict(kind="step", at=[round(x, 2), round(yk, 2)], rot=0))
    return places, primary


def assign_places(rows, places):
    """Story into quarters: each quarter gets its own set, so a long film has four places even in one location.
    A very short film uses two of them (fewer cuts, and the world gate is relaxed under 30 s)."""
    n = len(rows)
    if n <= 8:
        return [places[0] if i * 2 < n else places[2] for i in range(n)]
    return [places[min(3, i * 4 // max(1, n))] for i in range(n)]


# --------------------------------------------------------------------------- sets (files)
SET_TEMPLATE = """// SET: {kind} ({palette}) - GENERATED by tools/autofilm.py, then yours to edit.
// This is a normal set module: build(THREE, scene, film, ctx). The floor plan is plain data below;
// the geometry comes from the shared kit, so every generated set speaks the same metres / Z-up language.
import {{ buildPlace }} from "../../kit/sets/place_kit.js";

export const layout = {layout};

export function build(THREE, scene, film, ctx) {{
  return buildPlace(THREE, scene, film, ctx, layout);
}}
"""


def write_sets(ep, places):
    sd = os.path.join(ep, "sets")
    os.makedirs(sd, exist_ok=True)
    written = []
    for p in places:
        path = os.path.join(sd, "set_%s.js" % p["name"])
        with open(path, "w", encoding="utf-8") as f:
            f.write(SET_TEMPLATE.format(kind=p["kind"], palette=p["palette"],
                                        layout=json.dumps(p["layout"], ensure_ascii=False, indent=1)))
        written.append(path)
    return written


# --------------------------------------------------------------------------- camera (levelled to the subject)
def cam_for(framing, subject, height, feature=None, deep=False, side=None):
    """24 mm, portrait. Distances/aims solved against film_plan's own projection so the measured gates agree:
    W = whole body in the world, M = medium, C = close, P = place, O = object insert."""
    sx, sy = subject[0], subject[1]
    if framing == "P" and feature:
        fx, fy, fz, _ = feature
        pos = [round(fx * 0.30 + 0.25, 3), round(fy - 5.2, 3), 1.45]
        aim = [round(fx, 3), round(fy, 3), round(fz, 3)]
        return pos, aim
    if framing == "O" and feature:
        fx, fy, fz, _ = feature
        pos = [round(fx - 0.75, 3), round(fy - 1.55, 3), round(fz + 0.18, 3)]
        aim = [round(fx, 3), round(fy, 3), round(fz, 3)]
        return pos, aim
    if side is None:
        side = 0.10 if abs(sx) < 0.15 else (0.36 if sx > 0 else -0.36)
    H = max(0.95, height)
    if framing == "C":
        d, cz, az = 0.885 * H, 0.92 * H, 0.75 * H
    elif framing == "M":
        d, cz, az = 1.32 * H, 0.55 * H, 0.72 * H
    else:                                                    # W
        d, cz, az = (1.70 * H if not deep else 1.86 * H), 0.30 * H, 0.71 * H
    pos = [round(sx + side, 3), round(sy - d, 3), round(cz, 3)]
    aim = [round(sx, 3), round(sy, 3), round(az, 3)]
    return pos, aim


STAGE_Y = {"street": 1.30, "field": 1.10, "market": 1.15, "station": 1.10}
SLOTS = {"hero": [0.00, 0.65], "partner": [-1.55, 1.30], "other": [1.55, 1.30]}


# --------------------------------------------------------------------------- film
def build_film(rows, places, cast, words, title, all_places=None):
    words = [dict(w=w["w"], s=float(w["s"]), e=float(w["e"])) for w in words]
    n_words = len(words)
    n = len(rows)
    # sentence -> word span
    wi, spans = 0, []
    for r in rows:
        k = len(words_of(r["text"]))
        a, b = wi, min(n_words - 1, wi + k - 1)
        spans.append((a, b)); wi = b + 1
    end_f = int(math.ceil((words[-1]["e"] + 0.7) * FPS))
    mouthy = {}

    # ---- takes: one per run of the same place (i keeps the sentence's index)
    takes, cur = [], []
    for i, (r, p) in enumerate(zip(rows, places)):
        if cur and cur[0][2] is not p:
            takes.append(cur); cur = []
        cur.append((i, r, p))
    if cur:
        takes.append(cur)
    if len(takes) == 1 and len(rows) > 6:                       # a one-location story still earns more views of it
        half = len(rows) // 2
        takes = [[(i, rows[i], places[0]) for i in range(half)],
                 [(i, rows[i], places[2]) for i in range(half, len(rows))]]

    # ---- stage: fixed slots, so nobody walks through anybody; short characters stand on a step
    lift = {who: (0.24 if c["height"] < 1.5 else 0.0) for who, c in cast.items()}
    stage = {}
    for who, (x, y) in SLOTS.items():
        if who in cast:
            stage[who] = [x, y, lift[who]]
    for t in takes:
        kind = t[0][2]["kind"]
        sy = STAGE_Y.get(kind, 0.65)
        for who, p in stage.items():
            p[1] = sy if who == "hero" else sy + 0.70

    # ---- framing plan (quotas by time), one station per sentence
    p_quota = max(1, int(round(n * (0.35 if n <= 6 else 0.22))))
    plan = []; p_left = p_quota
    for i, r in enumerate(rows):
        lead = r["who"] == "hero"
        short = n <= 6
        if ((i % 2 == 1) if short else (i % max(2, round(n / max(1, p_quota))) == 1)) and p_left > 0 and (short or i < n - 1):
            f = "P"; p_left -= 1
        elif r["face"] and i % 12 == 3:
            f = "C"
        elif i % 6 == 4:
            f = "M"
        else:
            f = "W" if lead else "W2"
        plan.append(f)
    if "P" not in plan and n > 1:
        plan[min(n - 1, max(1, n // 2))] = "P"

    # ---- stations (one per sentence, plus a second beat inside longer sentences)
    takes_out, meta = [], {}
    take_i = 0
    for t in takes:
        stations = []
        for gi, (i, r, p) in enumerate(t):
            a, b = spans[i]
            t0, t1 = words[a]["s"], words[b]["e"]
            who = r["who"]; H = cast[who]["height"] + lift[who]
            f = plan[i]
            deep = who != "hero" or f == "W2"
            if f == "W2":
                f = "W"
            shows = [x for x in cast] + [p["feature"][3]]
            if r["prop"]:
                shows.append(r["prop"][0])
            shows = list(dict.fromkeys(shows))

            def make(at, framing, subject, pos, aim, lens=24):
                st = {"at": at, "pos": pos, "aim": aim, "lens": lens, "subject": subject,
                      "framing": framing, "shows": list(shows), "hold": 0.5, "travel": 0.9}
                stations.append(st); meta[id(st)] = (stage[who], H, p, who)
                return st

            if f == "P":
                pos, aim = cam_for("P", stage[who], H, feature=p["feature"])
                first = make(0 if gi == 0 and take_i == 0 else {"s": round(max(0.0, t0 - 0.13), 2)},
                             "P", p["feature"][3], pos, aim, lens=21)
            else:
                pos, aim = cam_for(f, stage[who], H, deep=deep)
                first = make(0 if gi == 0 and take_i == 0 else {"s": round(max(0.0, t0 - 0.13), 2)},
                             f, who, pos, aim)

            # the beat: inside a long sentence the camera closes or opens, so the film is not a slideshow
            last_beat = n > 2 and take_i == len(takes) - 1 and gi == len(t) - 1
            if not last_beat and ((t1 - t0) > 1.55 or n <= 6):
                bsub = who
                if n <= 2:                                  # one-line scripts still need a real camera move
                    bf, lens = "M", 30
                    bpos, baim = cam_for("M", stage[who], H, side=1.15)
                elif f in ("P", "C"):
                    bf, lens = "W", 24
                    bpos, baim = cam_for("W", stage[who], H, deep=deep)
                else:
                    bf, lens = "M", 30
                    bpos, baim = cam_for("M", stage[who], H)
                make({"s": round(t0 + (t1 - t0) * 0.55, 2)}, bf, bsub, bpos, baim, lens=lens)
        # travel/hold from the real gaps (the arriving station owns its travel)
        for j, st in enumerate(stations):
            if j == 0:
                st.pop("travel", None); st["hold"] = 0.7
                continue
            prev_t = _station_time(stations[j - 1])
            cur_t = _station_time(st)
            gap = max(0.5, cur_t - prev_t)
            tv = min(0.48, max(0.28, gap * 0.18))
            tv = min(tv, max(0.25, gap - 0.45))
            st["travel"] = round(tv, 2)
            st["hold"] = round(max(0.40, gap - tv - 0.05), 2)
        takes_out.append({"id": "t%d" % (take_i + 1), "place": t[0][2]["name"], "stations": stations})
        take_i += 1

    # one signature long move: the middle take's second station
    if takes_out:
        mid = takes_out[len(takes_out) // 2]
        if len(mid["stations"]) > 1:
            st = mid["stations"][1]
            prev_t = _station_time(mid["stations"][0]); cur_t = _station_time(st)
            gap = max(0.6, cur_t - prev_t)
            st["travel"] = round(min(3.2, max(1.0, gap - 0.55)), 2)
            st["hold"] = round(max(0.45, gap - st["travel"] - 0.05), 2)
            st["_signature"] = True

    # ---- acts
    acts = []
    for t in takes:
        start = words[spans[t[0][0]][0]]["s"]
        for who in cast:
            acts.append({"who": who, "at": {"s": max(0.02, start)}, "pos": list(stage[who]),
                         "view": "front" if who == "hero" else "34", "dir": 1,
                         "pose": "stand", "face": "standard", "look": "cam"})
    acts[0]["at"] = 0
    for i, r in enumerate(rows):
        a, b = spans[i]
        who = r["who"]; t0 = words[a]["s"]
        face = r["face"][1] if r["face"] else FACE_CYCLE[i % len(FACE_CYCLE)]
        pose = r["pose"]
        if r["prop"] and pose == "stand":
            pose = "grip_box" if r["prop"][1] == "box" else "hold_out"
        act = {"who": who, "at": {"s": round(max(0.02, t0 - 0.06), 2)}, "pose": pose, "face": face,
               "say": [a, b], "look": "cam"}
        if r["prop"]:
            act["prop"] = r["prop"][0]; act["hand"] = "R"
        acts.append(act)
        # a reaction on another face, and a second beat for the speaker
        other = "partner" if who != "partner" else "hero"
        if other in cast:
            acts.append({"who": other, "at": {"s": round(min(words[b]["e"], t0 + 0.6 * (words[b]["e"] - t0)), 2)},
                         "face": "curious" if i % 2 else "proud"})
        acts.append({"who": who, "at": {"s": round(max(t0 + 0.5, words[b]["e"] - 0.25), 2)},
                     "face": FACE_CYCLE[(i + 3) % len(FACE_CYCLE)]})
    acts.sort(key=lambda a: a["at"]["s"] if isinstance(a["at"], dict) else a["at"])

    # ---- places / sentences / props
    places_out = {}
    for p in (all_places or places):
        places_out[p["name"]] = {"set": "set_" + p["name"], "light": p["light"], "backdrop": 9.0 if p["kind"] != "field" else 24.0}
    sentences = []
    for i, r in enumerate(rows):
        a, b = spans[i]
        p = places[i]
        row = {"text": r["text"], "words": [a, b], "subject": r["who"],
               "show": list(dict.fromkeys(list(cast) + [p["feature"][3]] + ([r["prop"][0]] if r["prop"] else [])))}
        nouns = []
        if r["prop"]:
            t0, t1 = words[a]["s"], words[b]["e"]
            nouns.append({"word": words[a]["w"], "at": {"s": round(t0 + (t1 - t0) * 0.5, 2)}, "show": r["prop"][0]})
        row["nouns"] = nouns
        sentences.append(row)

    # ---- moods / fx / sound / kicks
    moods, fx, sound, kicks = [], [], [], []
    for i, r in enumerate(rows):
        a, b = spans[i]; t0, t1 = words[a]["s"], words[b]["e"]
        moods.append({"at": {"s": round(max(0.05, t0), 2)}, "look": MOODS[i % len(MOODS)]})
        moods.append({"at": {"s": round(min(t1, t0 + (t1 - t0) * 0.55), 2)}, "look": MOODS[(i + 2) % len(MOODS)]})
        on = r["prop"][0] if r["prop"] else (places[i]["feature"][3] if i % 3 == 0 else r["who"])
        if i % 4 == 0:
            fx.append({"at": {"s": round(t0 + 0.2, 2)}, "kind": FX_KINDS[i % len(FX_KINDS)], "on": on})
        if i % 2 == 0:
            sound.append({"at": {"s": round(t0 + 0.12, 2)},
                          "name": ["door_knock", "paper_flutter", "coin_chink", "arrival_hit"][i % 4]})
        if i % 3 == 1:
            kicks.append({"at": {"s": round(t0, 2)}, "amp": 1.1})

    film = {
        "title": title, "fps": FPS, "size": [1080, 1920], "end": end_f,
        "words": "voice/words.json",
        "camera_idea": {
            "name": "Level the camera to each subject",
            "why": "Every set is generated from the story, so the floor plan is known: the cast stands on it in stage slots and each beat gets a 24 mm camera levelled to that subject's own height - whole body to show the world, medium to squeeze two people, place and object frames when the beat belongs to the room or the thing.",
            "signature": "One long flowing move at the middle of the film, from the establishing framing into the turn.",
        },
        "cast": cast, "places": places_out,
        "props": {r["prop"][0]: {"kind": r["prop"][1]} for r in rows if r["prop"]},
        "takes": takes_out, "acts": acts, "sentences": sentences,
        "fx": fx, "moods": moods, "sound": sound, "kicks": kicks,
    }
    return film, meta


def _station_time(st):
    a = st["at"]
    return a if isinstance(a, (int, float)) else a["s"]


# --------------------------------------------------------------------------- gates + repair
def run_check(ep):
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "film_plan.py"), "check",
                        os.path.join(ep, "film.json")], cwd=ROOT, capture_output=True, text=True)
    out = (r.stdout or "") + (r.stderr or "")
    result = next((l for l in out.splitlines() if l.strip().startswith("RESULT")), "")
    return out, result


def read_gates(ep):
    p = os.path.join(ep, "out", "plan", "plan_report.json")
    try:
        return {g["name"]: g for g in json.load(open(p, encoding="utf-8"))["gates"]}
    except Exception:
        return {}


def save(ep, film):
    json.dump(film, open(os.path.join(ep, "film.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def speed_repair(ep, film, tries=4):
    """Measure the baked plan and give the fast travels more frames until no single frame whips past ~40 px/f.
    A move out of a close-up into a place frame covers metres; the fix is frames, not a different camera."""
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import film_plan as fp
    for _ in range(tries):
        save(ep, film)
        F = fp.load(os.path.join(ep, "film.json"))
        cam, tks = fp.bake_camera(F)
        sp = fp.screen_speed(cam)
        touched = False
        for ti, tk in enumerate(tks):
            S = tk["_S"]
            for si, (s0, s1) in enumerate(zip(S, S[1:])):
                a, b = s0["_depart"], s1["_arrive"]
                if b <= a + 1:
                    continue
                peak = max(sp[a:b + 1])
                if peak <= 40:
                    continue
                if ti >= len(film["takes"]) or si + 1 >= len(film["takes"][ti]["stations"]):
                    continue
                st = film["takes"][ti]["stations"][si + 1]
                gap_s = max(0.4, (s1["_at"] - s0["_at"]) / float(FPS))
                cur = float(st.get("travel", 0.9))
                want = max(cur, cur * peak / 34.0)
                new = round(min(max(cur + 0.05, want), max(cur, gap_s - 0.42)), 2)
                if new > cur + 0.01:
                    st["travel"] = new
                    st["hold"] = round(max(0.30, gap_s - new - 0.02), 2)
                    touched = True
        if not touched:
            return


def repair(ep, film, meta, rounds=4):
    """Read the measured gates and fix the cheap knobs until there is no FAIL. Returns the last report."""
    for _ in range(rounds):
        out, result = run_check(ep)
        gates = read_gates(ep)
        fails = [g for g in gates.values() if g["status"] == "FAIL"]
        pk = (gates.get("speed peak px/f") or {}).get("value")
        if isinstance(pk, (int, float)) and pk > 45:
            speed_repair(ep, film, tries=3)
            out, result = run_check(ep)
            gates = read_gates(ep)
            fails = [g for g in gates.values() if g["status"] == "FAIL"]
        if not fails:
            return out, result, gates
        by = {g["name"]: g for g in fails}
        stations = [s for t in film["takes"] for s in t["stations"]]

        def each(fn):
            for t in film["takes"]:
                for s in t["stations"]:
                    fn(t, s)

        if any(k in by for k in ("frames with a face, %", "shot mix W/M/C/P/O, % of time", "medium shots, % of time")):
            face = (by.get("frames with a face, %") or {}).get("value", 60)
            wshare = (by.get("shot mix W/M/C/P/O, % of time") or {}).get("value")
            if isinstance(wshare, str):
                try:
                    wshare = float(wshare.split("/")[0])
                except Exception:
                    wshare = 60
            if face < 45 or (isinstance(wshare, float) and wshare < 35):
                for s in stations:
                    if s["framing"] in ("P", "O"):
                        m = meta.get(id(s))
                        if not m:
                            continue
                        sub, H, p, who = m
                        s["pos"], s["aim"] = cam_for("W", sub, H, deep=who != "hero")
                        s["framing"] = "W"; s["subject"] = who
            elif face > 68:
                k = 0
                for s in stations:
                    m = meta.get(id(s))
                    if not m or s["framing"] in ("P", "O"):
                        continue
                    k += 1
                    if k % 4 == 2:
                        sub, H, p, who = m
                        s["pos"], s["aim"] = cam_for("P", sub, H, feature=p["feature"])
                        s["framing"] = "P"; s["subject"] = p["feature"][3]
        head = (by.get("face frames with the head cut by the edge, %") or {}).get("value")
        if head is not None and head > 13:
            for s in stations:
                m = meta.get(id(s))
                if not m or s["framing"] == "P":
                    continue
                sub, H, p, who = m
                f = s["framing"] if s["framing"] in ("W", "M", "C") else "W"
                if f == "C":
                    f = "M"
                s["pos"], s["aim"] = cam_for(f, sub, H, deep=True)
                s["framing"] = f
        if "longest travel, s" in by:
            v = by["longest travel, s"]["value"]
            mid = film["takes"][len(film["takes"]) // 2]
            if len(mid["stations"]) > 1:
                st = mid["stations"][1]
                if v < 3.0:
                    prev_t = _station_time(mid["stations"][0]); cur_t = _station_time(st)
                    st["travel"] = round(min(3.2, max(1.0, cur_t - prev_t - 0.5)), 2)
                    st["hold"] = round(max(0.45, cur_t - prev_t - st["travel"] - 0.05), 2)
                else:
                    st["travel"] = 2.0
                    st["hold"] = round(max(0.5, _station_time(st) - _station_time(mid["stations"][0]) - 2.4), 2)
        if "speed median px/f" in by and by["speed median px/f"]["value"] < 2.0:
            for s in stations:
                s["drift"] = [0.30, 0.0, 0.0]
        still = (by.get("dead still (reads under 0.3 px/f when measured), % of frames") or {}).get("value")
        if still is not None and still > 21:
            for s in stations:
                s["drift"] = [max(0.25, (s.get("drift") or [0.25])[0]), 0.0, 0.0]
        if "at rest (< 2 px/f), % of frames" in by:
            each(lambda t, s: s.__setitem__("hold", round(max(0.9, s.get("hold", 0.7)), 2)))
        p90 = (by.get("speed p90 px/f") or {}).get("value")
        if p90 is not None and p90 < 10:
            # few moving frames: spread each existing move over more frames (~0.5 s) so 10 % of the film reads as motion
            for t in film["takes"]:
                S = t["stations"]
                for j, s in enumerate(S):
                    if j == 0:
                        continue
                    tv = float(s.get("travel", 0.9))
                    if tv > 0.7:
                        continue
                    gap = max(0.4, _station_time(s) - _station_time(S[j - 1]))
                    new = round(min(0.55, max(tv, gap * 0.42)), 2)
                    s["travel"] = new
                    s["hold"] = round(max(0.30, gap - new - 0.02), 2)
        elif p90 is not None and p90 < 15:
            for s in stations:
                if s.get("travel", 0) > 0.6:
                    s["travel"] = round(s["travel"] * 0.8, 2)
        if "word stations not at rest on their word" in by:
            for s in stations:
                s["travel"] = max(0.7, s.get("travel", 0.9))
                s["hold"] = max(0.6, s.get("hold", 0.6))
        if "speed peak px/f" in by:
            speed_repair(ep, film)
        save(ep, film)
    g = read_gates(ep)
    pk = (g.get("speed peak px/f") or {}).get("value")
    if isinstance(pk, (int, float)) and pk > 60:
        speed_repair(ep, film, tries=3)
        out, result = run_check(ep)
        return out, result, read_gates(ep)
    out, result = run_check(ep)
    return out, result, g


# --------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description="Any script -> a complete film: sets saved, cast staged, camera levelled, gates repaired.")
    ap.add_argument("episode", help="episodes/<slug> (created if missing)")
    ap.add_argument("--script", required=True, help="script file, or the script text itself")
    ap.add_argument("--words", help="real word timings (voice/words.json); synthetic speech timing otherwise")
    ap.add_argument("--title", default=None)
    ap.add_argument("--lang", default="bn")
    ap.add_argument("--force", action="store_true", help="overwrite an existing film.json")
    a = ap.parse_args()

    ep = os.path.abspath(a.episode)
    os.makedirs(ep, exist_ok=True)
    if os.path.exists(os.path.join(ep, "film.json")) and not a.force:
        sys.exit("film.json already exists - pass --force to overwrite")

    text = a.script
    if os.path.exists(text):
        text = open(text, encoding="utf-8").read()
    sents = split_sentences(text)
    if not sents:
        sys.exit("no sentences found in the script")

    wpath = a.words or os.path.join(ep, "voice", "words.json")
    if wpath and os.path.exists(wpath):
        words = json.load(open(wpath, encoding="utf-8"))
        if not words:
            words = synth_words(sents)
    else:
        words = synth_words(sents)
    os.makedirs(os.path.join(ep, "voice"), exist_ok=True)
    json.dump(words, open(os.path.join(ep, "voice", "words.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    rows = analyse(sents)
    cast = build_cast(rows)
    all_places, primary = build_places(rows, os.path.basename(ep), cast)
    places = assign_places(rows, all_places)          # one place per sentence
    title = a.title or (sents[0][:58] + ("..." if len(sents[0]) > 58 else ""))
    film, meta = build_film(rows, places, cast, words, title, all_places)

    sets = write_sets(ep, all_places)
    save(ep, film)
    out, result, gates = repair(ep, film, meta)
    film = json.load(open(os.path.join(ep, "film.json"), encoding="utf-8"))

    # ---- SCRIPT.md
    final_words = json.load(open(os.path.join(ep, "voice", "words.json"), encoding="utf-8"))
    with open(os.path.join(ep, "SCRIPT.md"), "w", encoding="utf-8") as f:
        f.write("# %s\n\nGenerated by `tools/autofilm.py` from the supplied script - edit this file freely.\n\n" % film["title"])
        f.write("| # | time | line |\n|---|---|---|\n")
        wi = 0
        for i, s in enumerate(sents, 1):
            k = len(words_of(s))
            t0 = final_words[min(wi, len(final_words) - 1)]["s"]; wi += k
            f.write("| %d | %.1f s | %s |\n" % (i, t0, s))
        f.write("\n**Cast:** %s\n\n" % ", ".join("`%s` = %s (%.2f m)" % (k, v["puppet"], v["height"]) for k, v in film["cast"].items()))
        f.write("**Places:** %s\n" % ", ".join("`%s` = %s / %s light" % (k, v["set"], v["light"]) for k, v in film["places"].items()))

    # ---- SETS.md (what was generated, and how to change it)
    with open(os.path.join(ep, "SETS.md"), "w", encoding="utf-8") as f:
        f.write("# Sets for %s\n\n" % film["title"])
        f.write("`tools/autofilm.py` generated these from the script and saved them as ordinary set modules.\n")
        f.write("Edit the `layout` dict in any file - kind, palette, furniture, size - then re-run the pipeline.\n\n")
        f.write("| place | file | kind | light | furniture |\n|---|---|---|---|---|\n")
        for p in all_places:
            f.write("| `%s` | `sets/set_%s.js` | %s | %s | %s |\n" % (
                p["name"], p["name"], p["kind"], p["light"],
                ", ".join(x["kind"] for x in p["layout"]["furniture"])))

    # ---- CAMERA_NOTE.md (measured state, accepted warnings)
    warns = [g for g in gates.values() if g["status"] == "WARN"]
    with open(os.path.join(ep, "CAMERA_NOTE.md"), "w", encoding="utf-8") as f:
        f.write("# Camera / gate note - %s\n\n" % film["title"])
        f.write("Gate state: **%s**. " % (result.replace("RESULT ", "") or "see out/plan/plan_report.md"))
        f.write("%d gates, %d accepted WARN.\n\n" % (len(gates), len(warns)))
        if warns:
            f.write("## Accepted warnings\n\n| gate | value | target | why accepted |\n|---|---|---|---|\n")
            for g in warns:
                f.write("| %s | %s | %s | %s |\n" % (g["name"], g["value"], g["target"],
                        "within the skill's WARN band; the plan pass is kept and the episode stays editable"))
        f.write("\n## Camera idea\n\n%s\n\n" % film["camera_idea"]["why"])
        f.write("Signature move: %s\n" % film["camera_idea"]["signature"])
        f.write("\n## Re-bake after any edit\n\n```bash\npython tools/film_plan.py check episodes/%s/film.json\n```\n" % os.path.basename(ep))
        f.write("Renders read the **baked** plan in `out/plan/`, never `film.json` directly.\n")

    print(out[-2200:])
    print("saved: film.json, voice/words.json, %d sets, SCRIPT.md, SETS.md, CAMERA_NOTE.md -> %s" % (len(sets), ep))
    print(result)
    if "0 FAIL" not in result:
        print("\nNOTE: still >0 FAIL - the plan and every set are saved; open film.json and adjust, or run with a longer script.")
        sys.exit(1)


if __name__ == "__main__":
    main()
