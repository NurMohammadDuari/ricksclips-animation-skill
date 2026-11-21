#!/usr/bin/env python3
"""Build MY OWN film.json for Law 11 (artist lead, 2026-11-21). v2 — auto-aligned to voice/words.json.

Camera idea: "Who holds the khata holds the shop."
Every act of power is an act of writing or handing: Rafi writes the khata, the uncle hands it
to the nephew, the nephew waves it at customers who do not know him, the uncle arrives at the
door WITHOUT it (only sweets), and Rafi's own khata opens in the last shot. On every power
change the held thing travels TOWARD the lens.
Signature: the home doorway — the uncle crosses it three times (scheming WITH the khata,
begging WITHOUT it); the tea glass is poured on honoured visits, absent when he begs.
Light arc: morning gold (thriving) -> interior warm (warning) -> dusk blue (fired) ->
golden (rising) -> night (failing, begging) -> bright morning (payoff) — full circle.
"""
import json, re

ROOT = "/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1"
EP = f"{ROOT}/episodes/law11-art"
W = [x for x in json.load(open(f"{EP}/voice/words.json")) if re.match(r"[\u0980-\u09FF0-9]", x["w"])]   # skip punctuation tokens

def wtime(text, n=1):
    hits = [x["s"] for x in W if x["w"] == text]
    if len(hits) < n: raise KeyError(f"word {text!r} #{n} not found")
    return round(hits[n - 1], 3)

def S(t): return {"s": round(t, 2)}

import re
def split_words(text):
    # split a Bangla sentence into word tokens matching words.json tokens (strip punctuation)
    return [t for t in re.split(r'[\s।,!?….;:"?-]+', text) if t]

RAW = json.load(open(f"{EP}/voice/words.json"))
CURSOR = 0
def align(text):
    """find the sentence's word run in the RAW words array (film_plan indexes raw); return (i0, i1) raw."""
    toks = split_words(text)
    n = len(toks)
    global CURSOR
    is_tok = lambda t: re.match(r'[\u0980-\u09FF0-9]', t)
    j = CURSOR
    while j < len(RAW) and RAW[j]["w"] != toks[0]: j += 1          # find the first token after the previous sentence
    start = j; k = 0
    while j < len(RAW) and k < n:
        if RAW[j]["w"] == toks[k]: k += 1
        elif k > 0 and is_tok(RAW[j]["w"]): break
        j += 1
    if k == n: CURSOR = j; return start, j - 1
    raise KeyError("sentence not aligned: " + text[:30])

SENTS = [
  ("কাল থেকে আর আসা লাগবে না, রাফি। আমার ভাগ্নে এখন সব পারে।", "chacha", [("ভাগ্নে", "nephew")]),
  ("চাচা, ১০ বছর... আপনার ভাগ্নেরে তো সব আমিই শিখাইলাম!", "rafi", [("ভাগ্নেরে", "nephew")]),
  ("কিন্তু ৩ মাস পর, সেই চাচাই মিষ্টির প্যাকেট হাতে... রাফির বাসায় এসে হাজির!", "chacha", [("মিষ্টির", "box"), ("বাসায়", "door")]),
  ("অথচ ১ বছর আগে, চাচা নিজেই ভাগ্নেকে নিয়ে রাফির বাসায় এসে বলেছিলেন,", "chacha", [("ভাগ্নেকে", "nephew"), ("বাসায়", "door")]),
  ("রাফি, পোলাটারে কাজ শিখায় দাও... তুমি তো আমার নিজের পোলার মতো!", "chacha", [("পোলাটারে", "nephew")]),
  ("সব শিখাইস না, বাবা... মালিকের ভাগ্নে, মালিকেরই লোক!", "ma", [("বাবা", "rafi")]),
  ("মায়ের কথা হেসে উড়িয়ে, রাফি ভাগ্নেকে শিখালো সাপ্লায়ারদের নম্বর, বাকির খাতা... আর চিনিয়ে দিলো সব বাকির খদ্দের। ভাগ্নে সব শিখে ফেলতেই, চাচা বললেন সেই কথা... আর ১০ বছর পর, রাফি মাত্র ১ মাসের বেতন নিয়ে বাসায় ফিরলো।", "rafi", [("খাতা", "khata"), ("খদ্দের", "nephew"), ("বেতন", "wage")]),
  ("যার পাতে ভাত দিলি... সেই তোর ভাত কাড়লো, বাবা!", "ma", [("ভাত", "rafi")]),
  ("১ মাস পর, পাশের দোকানে অর্ধেক বেতনে চাকরি নিয়ে, রাফি এবার সবাইকে কাজ শিখালো... কিন্তু কিছু বড় খদ্দের রাখলো নিজের হাতে। ওদিকে বাকির খাতা ছিলো ভাগ্নের হাতে... কিন্তু বাকির খদ্দেররা চিনতো শুধু রাফিকে। ভাগ্নে বাকির টাকা চাইতে গিয়ে খদ্দেরদের বললো চোর... আর তারা মাল নিতে গেলো রাফির কাছে!", "rafi", [("দোকানে", "counter"), ("হাতে", ("khata", 2)), ("চোর", "nephew")]),
  ("৩ মাসে বিক্রি অর্ধেক হতেই, চাচা মিষ্টির প্যাকেট হাতে রাফির বাসায় এসে বললেন,", "chacha", [("মিষ্টির", "box"), ("বাসায়", "door")]),
  ("রাফি, কাল থেকে আবার আসো, বাবা... ভাগ্নে আমার কিছুই পারে না!", "chacha", [("ভাগ্নে", "nephew")]),
  ("চাচা, কাজ তো সবই শিখাইছিলাম... খালি মানুষের ভরসাটা শিখানো যায় না।", "rafi", [("ভরসাটা", "chacha")]),
  ("রাফি আর ফিরলো না... ৬ মাস পর, পাশের দোকানের মালিক ওকে ৪ আনার অংশীদার বানালেন!", "dokandar", [("মালিক", "dokandar"), ("অংশীদার", "rafi")]),
  ("কাজ সবাইকে শেখান... কিন্তু নিজের জায়গাটা কাউকে শিখিয়ে দিবেন না। রবার্ট গ্রিনের বইয়ের ১১ নম্বর নিয়ম বলে, নিজেকে এমন জায়গায় নাও, যেখানে তোমাকে ছাড়া চলে না।", "rafi", [("নিয়ম", "khata")]),
  ("আপনার চাকরিতেও কি, মালিকের আত্মীয় এসে কারো জায়গা নিয়েছে? কী হয়েছিলো? কমেন্টে লিখুন। এমন আরো গল্প পেতে ফলো করুন।", "rafi", [("লিখুন", "khata")]),
]

F = {
  "title": "৪৮ শক্তির নিয়ম — নিয়ম ১১: খাতা যার, দোকান তার",
  "fps": 30, "size": [1080, 1920], "end": 121.34,
  "words": "voice/words.json",
  "camera_idea": {
    "name": "Who holds the khata holds the shop",
    "why": "The credit ledger (বাকির খাতা) is the seat of power: Rafi writes it, the uncle hands it to the nephew, the nephew waves it at customers who only know Rafi, the uncle arrives at the door without it, and Rafi's own khata opens in the last shot. The camera travels toward hands and the book; on every power change the held thing comes toward the lens.",
    "signature": "The home doorway crossed three times: the uncle brings the nephew IN with the khata (proud), the fired Rafi stands inside (the door opens on him), and the uncle begs at the same door at night WITHOUT the khata — only a sweets box held out flat. Tea is poured on the honoured visit, absent when he begs."
  },
  "cast": {
    "chacha":  {"puppet": "cast:chacha",  "height": 1.68, "heads_tall": 2.7},
    "rafi":    {"puppet": "cast:rafi",    "height": 1.70, "heads_tall": 2.8},
    "nephew":  {"puppet": "cast:nephew",  "height": 1.35, "heads_tall": 2.4},
    "ma":      {"puppet": "cast:ma",      "height": 1.58, "heads_tall": 2.8},
    "dokandar": {"puppet": "cast:dokandar", "height": 1.72, "heads_tall": 2.8},
    "khoddeder":  {"puppet": "cast:khoddeder",  "height": 1.62, "heads_tall": 2.7},
    "khoddeder2": {"puppet": "cast:khoddeder2", "height": 1.66, "heads_tall": 2.8},
    "bepari":     {"puppet": "cast:bepari",     "height": 1.74, "heads_tall": 2.8}
  },
  "places": {
    "shop_am":       {"set": "mithai_shop",   "light": "morning",  "backdrop": 9.0},
    "shop_day":      {"set": "mithai_shop",   "light": "day",      "backdrop": 9.0},
    "shop_night":    {"set": "mithai_shop",   "light": "night",    "backdrop": 8.0,
                      "light_over": {"top": "#141c3c", "hor": "#33447e", "amb": "#4c5e98", "ai": 1.62, "si": 1.62, "tint": "#e2e8ff", "card_gain": 1.22}},
    "home_in":       {"set": "mithai_home",   "light": "interior", "backdrop": 7.0},
    "home_night":    {"set": "mithai_home",   "light": "night",    "backdrop": 8.0,
                      "light_over": {"top": "#131a38", "hor": "#31427a", "amb": "#4a5c94", "ai": 1.4, "si": 1.5, "tint": "#e0e7ff", "card_gain": 1.22}},
    "padosi_golden": {"set": "mithai_padosi", "light": "golden",   "backdrop": 10.0},
    "padosi_day":    {"set": "mithai_padosi", "light": "day",      "backdrop": 10.0}
  },
  "props": { "khata": {"kind": "scroll"}, "box": {"kind": "box"}, "wage": {"kind": "bag"} },
}
F["sentences"] = []
for text, subj, nouns in SENTS:
    i0, i1 = align(text)
    F["sentences"].append({"text": text, "words": [i0, i1], "subject": subj,
                           "nouns": [{"word": w_, "show": sh if not isinstance(sh, tuple) else sh[0], **({"n": sh[1]} if isinstance(sh, tuple) else {})} for w_, sh in nouns]})
print("sentence spans:", [(s["words"][0], s["words"][1]) for s in F["sentences"]])

T = F["takes"] = []
def st(at, pos, aim, subject, framing, lens=24, shows=None, hold=0.4, travel=None, word=None):
    s = {"at": S(at), "pos": pos, "aim": aim, "lens": lens, "subject": subject, "framing": framing,
         "shows": shows if shows is not None else ["chacha", "rafi", "nephew", "ma", "dokandar"], "hold": hold}
    if travel is not None: s["travel"] = travel
    if word is not None: s["word"] = word; s["lead"] = 12; s["hold"] = 0.6
    elif s.get("hold") in (0.5, 0.45): s["hold"] = 0.32
    return s

# ---- t1 shop_am 0.0-9.6: THE FIRING (cold open). Frame 0 hook: the boss points out the door,
# Rafi stands IN FRONT of the counter with his packed wage bag, the nephew already wears the spot behind it.
T.append({"id": "t1", "place": "shop_am", "stations": [
  st(0.0, [0.15, -2.0, 1.5], [0.4, 2.1, 1.35], "chacha", "W", 24, ["chacha", "rafi", "nephew", "counter", "jars"], 0.55, 0.6),
  st(wtime("রাফি", 1), [0.1, -1.9, 1.3], [0.15, 0.4, 1.3], "rafi", "M", 24, ["rafi", "chacha", "nephew", "counter", "jars"], 0.5, 0.7, "রাফি"),
  st(wtime("ভাগ্নেরে"), [-2.6, -1.7, 1.25], [0.3, 1.7, 1.15], "counter", "P", 24, ["counter", "chacha", "nephew", "rafi", "jars"], 0.5, 2.2, "ভাগ্নেরে"),
  st(wtime("শিখাইলাম"), [0.4, -2.1, 1.35], [0.3, 0.4, 1.35], "rafi", "C", 26, ["rafi", "chacha"], 0.55, 0.7, "শিখাইলাম"),
]})
# ---- t2 home_night 9.6-16.6: THE TEASER — the knock at night, sweets box held out.
T.append({"id": "t2", "place": "home_night", "stations": [
  st(wtime("কিন্তু"), [1.6, -1.8, 1.35], [2.45, 3.3, 1.3], "chacha", "W", 24, ["chacha", "ma", "door", "box"], 0.5, 0.6, "কিন্তু"),
  st(wtime("মিষ্টির", 1), [2.38, -0.65, 1.25], [2.42, 3.2, 1.18], "box", "O", 36, ["box", "chacha", "door"], 0.5, 2.6, "মিষ্টির"),
  st(wtime("বাসায়", 1), [1.7, -1.9, 1.3], [2.45, 3.3, 1.28], "chacha", "M", 24, ["chacha", "ma", "door", "box"], 0.5, 0.7),
  st(wtime("হাজির"), [-1.6, -2.6, 1.5], [2.45, 3.3, 1.3], "chacha", "W", 24, ["chacha", "ma", "door"], 0.55, 2.6, "হাজির"),
]})
# ---- t3 home_in 16.7-25.6: THE FLASHBACK — the uncle arrives WITH the khata, handing the nephew over.
T.append({"id": "t3", "place": "home_in", "stations": [
  st(wtime("অথচ"), [1.8, -1.75, 1.35], [2.45, 3.3, 1.3], "chacha", "W", 24, ["chacha", "rafi", "nephew", "ma", "door"], 0.5, 0.6, "অথচ"),
  st(wtime("ভাগ্নেকে"), [2.2, -1.2, 1.2], [2.45, 3.3, 1.25], "chacha", "M", 24, ["chacha", "nephew", "door", "khata"], 0.5, 0.8, "ভাগ্নেকে"),
  st(wtime("পোলাটারে"), [1.5, -2.1, 1.45], [1.0, 1.35, 1.25], "chacha", "W", 24, ["chacha", "nephew", "rafi"], 0.6, 0.7, "পোলাটারে"),
]})
# ---- t4 home_in 25.6-32.2: THE MOTHER'S WARNING (the tea glass stays dry on this visit).
T.append({"id": "t4", "place": "home_in", "stations": [
  st(wtime("সব", 3), [-0.7, -1.7, 1.25], [-0.8, 1.05, 1.25], "ma", "M", 24, ["ma", "rafi", "chacha", "nephew", "table"], 0.5, 0.55, "সব"),
  st(wtime("মালিকের", 1), [-0.85, -1.85, 1.35], [-0.7, 1.0, 1.42], "ma", "C", 26, ["ma", "rafi"], 0.5, 0.6, "মালিকের"),
  st(wtime("লোক"), [-1.7, -2.7, 1.45], [-0.35, 0.95, 1.25], "rafi", "W", 24, ["rafi", "ma", "chacha"], 0.55, 2.6, "লোক"),
]})
# ---- t5 shop_day 32.2-49.2: THE TEACHING — khata writing, the flowing montage move, the wage.
T.append({"id": "t5", "place": "shop_day", "stations": [
  st(wtime("মায়ের"), [0.1, -2.1, 1.6], [0.1, 1.3, 1.3], "rafi", "W", 24, ["rafi", "nephew", "chacha", "counter", "jars"], 0.5, 0.6, "মায়ের"),
  st(wtime("খাতা", 1), [-1.35, -1.75, 1.3], [0.3, 1.6, 1.1], "khata", "O", 40, ["khata", "rafi", "nephew"], 0.5, 2.8, "খাতা"),
  st(38.0, [2.0, -2.0, 1.5], [0.4, 1.6, 1.2], "rafi", "W", 24, ["rafi", "nephew", "counter", "jars"], 0.4, 2.6),
  st(wtime("খদ্দের", 1), [-3.0, -1.6, 1.3], [0.2, 1.6, 1.12], "counter", "P", 24, ["counter", "rafi", "nephew", "khata", "jars"], 0.5, 2.6, "খদ্দের"),
  st(43.6, [0.2, -2.0, 1.5], [0.4, 2.1, 1.35], "chacha", "W", 24, ["chacha", "rafi", "nephew", "counter"], 0.4, 1.7),
  st(wtime("বেতন"), [1.45, -1.2, 1.28], [0.6, 0.45, 1.25], "wage", "O", 36, ["wage", "rafi", "chacha"], 0.5, 2.6, "বেতন"),
  st(wtime("ফিরলো", 1), [0.2, -2.0, 1.5], [0.3, 2.1, 1.35], "chacha", "W", 24, ["chacha", "rafi", "nephew", "counter", "door"], 0.55, 0.8),
]})
# ---- t6 home_in 49.2-53.3: THE MOTHER'S SECOND WARNING.
T.append({"id": "t6", "place": "home_in", "stations": [
  st(wtime("যার"), [-0.7, -2.0, 1.3], [-0.8, 1.05, 1.25], "ma", "W", 24, ["ma", "rafi", "table", "plate"], 0.55, 0.55, "যার"),
  st(wtime("ভাত", 2), [-0.9, -1.9, 1.35], [-0.7, 1.0, 1.42], "ma", "C", 26, ["ma", "rafi"], 0.55, 0.7, "ভাত"),
]})
# ---- t7 padosi_golden 53.3-62.1: THE NEW JOB — half pay, the secret list kept in his own hand.
T.append({"id": "t7", "place": "padosi_golden", "stations": [
  st(wtime("১", 3), [-0.5, -2.0, 1.7], [-0.3, 1.2, 1.35], "rafi", "W", 24, ["rafi", "dokandar", "counter", "bench", "jars"], 0.5, 0.6),
  st(wtime("বেতনে"), [-0.55, -2.1, 1.45], [-0.35, 1.1, 1.25], "rafi", "W", 24, ["rafi", "dokandar", "counter", "kettle"], 0.5, 0.7, "বেতনে"),
  st(wtime("শিখালো", 2) - 1.7, [1.75, -1.0, 1.25], [1.5, 1.35, 1.15], "kettle", "P", 30, ["kettle", "counter"], 0.5, 0.7),
  st(wtime("শিখালো", 2), [-0.7, -1.85, 1.5], [-0.4, 1.35, 1.3], "rafi", "W", 24, ["rafi", "dokandar", "counter", "bench"], 0.5, 0.7, "শিখালো"),
  st(wtime("হাতে", 2), [-1.95, -1.0, 1.32], [-0.75, 1.0, 1.2], "khata", "O", 36, ["khata", "rafi"], 0.55, 2.6, "হাতে"),
]})
# ---- t8 shop_night 62.1-75.0: THE FAILURE — the nephew alone with the khata nobody honours.
T.append({"id": "t8", "place": "shop_night", "stations": [
  st(wtime("ওদিকে"), [0.1, -2.0, 1.5], [0.15, 1.5, 1.3], "nephew", "W", 24, ["nephew", "chacha", "counter", "jars"], 0.5, 0.6, "ওদিকে"),
  st(64.3, [0.55, -2.15, 1.45], [0.4, 1.5, 1.2], "nephew", "W", 24, ["nephew", "counter", "khata"], 0.5, 0.7),
  st(wtime("চিনতো"), [1.35, -1.35, 1.32], [0.5, 1.45, 1.3], "nephew", "M", 26, ["nephew", "khata", "jars"], 0.5, 2.6, "চিনতো"),
  st(wtime("চোর"), [0.85, -1.7, 1.3], [0.45, 1.4, 1.3], "nephew", "M", 24, ["nephew", "khata"], 0.5, 0.55, "চোর"),
  st(72.8, [-2.0, -1.2, 1.45], [0.3, 1.5, 1.35], "nephew", "W", 24, ["nephew", "counter", "door", "jars"], 0.5, 0.9),   # closer + on his eyeline: the teary nephew reads against the lit wall
  st(wtime("কাছে"), [1.35, -2.2, 1.5], [0.35, 1.5, 1.3], "nephew", "W", 24, ["nephew", "counter", "khata"], 0.55, 2.6, "কাছে"),
]})
# ---- t9 home_night 75.0-91.6: THE BEGGING + THE REFUSAL — the same door, no khata, only the sweets box.
T.append({"id": "t9", "place": "home_night", "stations": [
  st(wtime("মাসে"), [1.7, -1.85, 1.35], [2.45, 3.3, 1.3], "chacha", "W", 24, ["chacha", "ma", "door", "box"], 0.5, 0.6),
  st(wtime("প্যাকেট", 2), [2.38, -0.62, 1.25], [2.42, 3.2, 1.18], "box", "O", 36, ["box", "chacha", "door"], 0.5, 2.6, "প্যাকেট"),
  st(wtime("বললেন", 2), [1.9, -1.5, 1.2], [2.45, 3.3, 1.25], "chacha", "M", 24, ["chacha", "ma", "door", "box"], 0.5, 0.7),
  st(wtime("আবার"), [-0.6, -2.5, 1.45], [2.45, 3.3, 1.3], "chacha", "W", 24, ["chacha", "ma", "door"], 0.5, 2.6, "আবার"),
  st(wtime("পারে", 2), [2.2, -1.05, 1.4], [2.45, 3.3, 1.28], "chacha", "C", 26, ["chacha", "box"], 0.5, 0.6, "পারে"),
  st(wtime("চাচা", 5), [1.15, -2.0, 1.4], [1.55, 1.7, 1.25], "rafi", "W", 24, ["rafi", "chacha", "door"], 0.5, 0.6, "চাচা"),
  st(wtime("ভরসাটা"), [1.35, -1.55, 1.3], [1.65, 1.75, 1.35], "rafi", "M", 24, ["rafi", "chacha", "door"], 0.5, 0.7, "ভরসাটা"),
  st(91.1, [-0.9, -2.5, 1.5], [1.85, 2.6, 1.25], "chacha", "W", 24, ["chacha", "rafi", "door"], 0.55, 2.6),
]})
# ---- t10 padosi_day 92.0-98.5: THE PARTNERSHIP — the coin glints, the hand-off lands.
T.append({"id": "t10", "place": "padosi_day", "stations": [
  st(wtime("রাফি", 7), [-0.55, -2.0, 1.7], [-0.4, 1.3, 1.35], "rafi", "W", 24, ["rafi", "dokandar", "counter", "bench", "jars"], 0.5, 0.6),
  st(wtime("মালিক"), [-0.6, -2.1, 1.45], [-0.45, 1.2, 1.25], "dokandar", "W", 24, ["dokandar", "rafi", "counter"], 0.5, 0.8, "মালিক"),
  st(wtime("অংশীদার"), [-1.7, -1.35, 1.3], [-0.8, 1.0, 1.3], "rafi", "C", 26, ["rafi", "dokandar", "coin"], 0.55, 0.6, "অংশীদার"),
]})
# ---- t11 padosi_day 98.5-121.3: THE LESSON + CTA — Rafi's own khata opens on his own counter.
T.append({"id": "t11", "place": "padosi_day", "stations": [
  st(wtime("কাজ", 4), [-0.5, -2.0, 1.6], [-0.4, 1.3, 1.3], "rafi", "W", 24, ["rafi", "dokandar", "counter", "bench", "jars"], 0.5, 0.6, "কাজ"),
  st(wtime("জায়গাটা"), [-0.55, -2.1, 1.5], [-0.4, 1.25, 1.25], "rafi", "W", 24, ["rafi", "dokandar", "counter"], 0.5, 0.7),
  st(wtime("নিয়ম"), [-1.5, -1.05, 1.2], [-0.95, 1.35, 1.08], "khata", "O", 40, ["khata", "rafi"], 0.5, 0.6, "নিয়ম"),
  st(108.2, [1.7, -2.3, 1.5], [0.3, 1.5, 1.25], "rafi", "W", 24, ["rafi", "dokandar", "counter", "bench"], 0.4, 2.6),
  st(wtime("নাও"), [-0.9, -1.7, 1.3], [-0.6, 1.15, 1.3], "rafi", "M", 24, ["rafi", "dokandar"], 0.5, 2.6, "নাও"),
  st(114.5, [-0.4, -2.0, 1.6], [-0.3, 1.25, 1.3], "rafi", "W", 24, ["rafi", "dokandar", "counter", "bench"], 0.5, 0.9),
  st(wtime("লিখুন"), [-1.35, -1.15, 1.3], [-0.55, 1.05, 1.25], "rafi", "M", 24, ["rafi", "dokandar", "counter", "khata"], 0.5, 2.6, "লিখুন"),
  st(wtime("করুন"), [-0.7, -1.8, 1.3], [-0.5, 1.15, 1.3], "rafi", "M", 24, ["rafi", "dokandar"], 0.55, 0.55, "করুন"),
]})
F["end"] = 3640

# ---------------------------------------------------------------- acts (the performance) — valid pose/face names only
A = F["acts"] = []
def act(who, at, **kw): A.append(dict(who=who, at=S(at) if isinstance(at, (int, float)) else at, **kw))

# t1: the firing.  (PLACE DISCIPLINE 2026-11-21: every enter/exit lands on a place cut —
# probe-verified cut frames: 8.67 home, 30.67 shop, 47.67 home, 52.9 padosi, 61.8 shop, 75.07 home, 91.9 padosi.
# Ma lives at home: she is never on stage in shop / padosi takes — her home position no longer leaks
# into the night shop as a cut-off green sari behind the counter.)
act("ma", 0, pos=[-0.35, 0.85, 0], visible=False)   # parked at home, hidden until her first home scene
act("chacha", 0, pos=[0.55, 2.15, 0], view="34", dir=-1, pose="point_out", face="proud", say=[0, 11])
act("rafi", 0, pos=[0.1, 0.4, 0], view="34", dir=1, pose="hold_watch", face="shocked", prop="wage", hand="L")
act("nephew", 0, pos=[1.35, 2.35, 0], view="34", dir=-1, pose="stand", face="smug")
act("rafi", 2.1, pose="flinch", face="sad", prop=None)   # the wage envelope lands on the counter (clank fx)
act("chacha", 2.2, face="cool")
# t1 extras: the loyal old customer witnesses the firing (staged in depth at the left edge: 9:16 hfov is narrow)
act("khoddeder", 0, pos=[-0.1, 0.7, 0], view="34", dir=1, pose="stand", face="worried", enter=True, visible=True)
act("khoddeder", 1.9, face="sad")
act("khoddeder", 4.3, pose="hands_hips", face="tired")
act("khoddeder", 6.6, face="worried")
act("khoddeder", 8.67, exit=True)   # cut hides it
act("chacha", 4.7, pose="hands_hips", face="smug")
act("nephew", 5.2, pose="cheer", face="excited")
act("rafi", 6.2, pose="stand", face="sad")
act("chacha", 7.4, face="smug")
act("nephew", 8.67, exit=True)   # cut hides it (was 9.5: 25 leaked frames inside the night home)
# t2: the teaser knock at night.
act("chacha", 8.67, pos=[2.3, 3.2, 0], view="front", dir=1, pose="knock", face="smug", say=[21, 33])
act("ma", 8.67, pos=[-0.35, 0.85, 0], view="front", dir=1, pose="stand", face="worried", enter=True, visible=True)
act("chacha", 10.5, face="cool")   # the tease softens mid-knock (kills the 3.3 s frozen stretch)
act("chacha", 12.0, pose="hold_out", face="smug", prop="box", hand="R")
act("ma", 14.2, pose="flinch", face="worried")
act("chacha", 16.0, pose="hold_out", face="cool")   # still offering the box at the door
act("ma", 11.4, face="worried")
act("ma", 13.4, pose="tiltL", face="skeptical")
# t3: the flashback — the uncle hands over the nephew, WITH the khata.
act("chacha", 14.67, pos=[2.3, 3.1, 0], view="front", dir=1, pose="hold_watch", face="proud", prop="khata", hand="L", say=[34, 45])
act("nephew", 16.7, pos=[2.0, 2.6, 0], view="34", dir=1, pose="stand", face="excited", enter=True, visible=True)
act("rafi", 14.67, pos=[0.45, 0.6, 0], view="34", dir=1, pose="stand", face="surprised")
act("rafi", 19.0, face="worried")
act("ma", 14.67, pos=[-0.75, 0.85, 0], view="34", dir=1, pose="stand", face="worried")
act("ma", 22.5, pose="tiltL", face="worried")
act("ma", 24.0, face="sad")
act("chacha", 19.4, pose="hold_out", face="proud", prop="khata", hand="R")
act("chacha", 21.0, face="smug")   # the hand-over beat
act("nephew", 18.4, face="smug")   # watching Rafi's home with hungry eyes
act("nephew", 20.0, pose="cheer", face="excited")
act("rafi", 20.6, face="happy")
act("chacha", 22.4, pos=[0.95, 1.35, 0], view="34", dir=1, pose="hold_watch", face="smug", hand="L", say=[46, 56])   # keeps the khata in hand
act("nephew", 23.4, pos=[1.45, 1.65, 0], view="34", dir=1, pose="stand", face="smug")
act("chacha", 24.6, face="cool")
# t4: the mother's warning.
act("ma", 25.65, pos=[-0.85, 1.15, 0], view="34", dir=1, pose="point_out", face="skeptical", say=[57, 64])
act("chacha", 25.55, pose="stand", face="smug", prop=None)   # the khata stays at Rafi's home now
act("rafi", 25.65, pos=[-0.25, 0.6, 0], view="34", dir=-1, pose="stand", face="happy")
act("chacha", 25.65, pos=[0.95, 1.35, 0], view="34", dir=1, pose="stand", face="smug")
act("nephew", 25.65, pos=[1.45, 1.65, 0], view="34", dir=-1, pose="stand", face="annoyed")
act("ma", 28.6, face="worried")
act("rafi", 29.6, pose="shrug", face="laugh")
act("chacha", 30.6, pose="clap", face="happy")
act("ma", 30.67, exit=True)   # cut hides it — she stays home; the shop is Rafi's world
# t5: the teaching montage + the firing + the wage.
act("chacha", 30.67, pos=[0.7, 2.35, 0], view="34", dir=-1, pose="hands_hips", face="smug")
act("rafi", 30.67, pos=[0.4, 1.75, 0], view="34", dir=-1, pose="write", face="concentrate", say=[65, 101])
act("nephew", 30.67, pos=[-0.35, 1.15, 0], view="34", dir=1, pose="stand", face="confused")
# t5 extras: the supplier waits at the counter's far end; a customer at the front-left edge
act("bepari", 30.67, pos=[1.25, 2.35, 0], view="34", dir=-1, pose="stand", face="cool", enter=True, visible=True)
act("bepari", 33.6, pose="hold_watch", face="think")
act("bepari", 36.5, pose="hands_hips", face="happy")
act("bepari", 39.4, face="cool")
act("bepari", 42.4, pose="hold_watch", face="concentrate")
act("bepari", 45.4, face="worried")
act("bepari", 47.67, exit=True)   # cut hides it
act("khoddeder", 30.67, pos=[-0.3, 0.75, 0], view="34", dir=1, pose="stand", face="cool", enter=True, visible=True)
act("khoddeder", 33.0, face="happy")   # smiles as the boy writes
act("khoddeder", 34.2, face="think")
act("khoddeder", 37.2, pose="hands_hips", face="concentrate")
act("khoddeder", 40.2, face="tired")
act("khoddeder", 43.2, face="cool")
act("khoddeder", 47.67, exit=True)   # cut hides it
act("nephew", 35.6, face="surprised")
act("nephew", 32.8, face="think")   # the lesson lands slowly
act("chacha", 33.5, face="happy")   # beams as the boy writes
act("chacha", 36.0, face="proud")   # nods along to his own system
act("rafi", 38.0, pose="point_out", face="think")
act("nephew", 40.0, pose="write", face="concentrate")
act("rafi", 43.0, face="happy")
act("chacha", 44.4, face="cool")
act("rafi", 45.3, pose="hold_watch", face="sad", prop="wage", hand="L")
act("nephew", 45.3, prop="khata", pose="hold_watch", face="proud", hand="L")
act("chacha", 47.6, pose="point_out", face="smug")
act("chacha", 47.67, exit=True)   # cut hides it (was leaking 45 frames into the home)
act("nephew", 47.67, exit=True)   # cut hides it (was 49.0: 40 leaked frames inside the home)
# t6: the mother's second warning.
act("ma", 47.67, pos=[-0.85, 1.15, 0], view="34", dir=1, pose="finger_up", face="skeptical", say=[102, 110], enter=True, visible=True)
act("rafi", 49.2 - 1.53, pos=[-0.25, 0.6, 0], view="34", dir=-1, pose="hold_watch", face="sad")   # the wage bag still in his hand at home
act("rafi", 51.15, pose="flinch", face="shocked", prop=None)   # the bag hits the floor in shock
act("ma", 52.4, pose="hands_hips", face="angry")
act("ma", 52.9, exit=True)   # cut hides it — home again before the padosi scene
# t7: the new job.
act("rafi", 52.9, pos=[-0.35, 1.35, 0], view="34", dir=1, pose="stand", face="tired", prop=None, say=[111, 130])   # the bag left at home
act("dokandar", 0.2, pos=[0.55, 1.95, 0], visible=False)   # the neighbour shopkeeper stays off stage until his own shop
act("dokandar", 52.9, pos=[0.55, 1.95, 0], view="34", dir=-1, pose="stand", face="sweetSmile", enter=True, visible=True)
# t7 extra: a tea customer by the counter's front edge (golden hour life)
act("khoddeder2", 52.9, pos=[-0.1, 0.7, 0], view="34", dir=1, pose="stand", face="cool", enter=True, visible=True)
act("khoddeder2", 55.4, face="happy")
act("khoddeder2", 58.0, pose="hands_hips", face="laugh")
act("khoddeder2", 60.4, face="cool")
act("khoddeder2", 61.8, exit=True)   # cut hides it
act("rafi", 55.9, face="cool")
act("dokandar", 57.4, pose="point_out", face="happy")
act("dokandar", 61.8, exit=True)   # cut hides it
act("rafi", 59.0, pose="clap", face="happy")
act("rafi", 61.5, face="concentrate")
act("rafi", 61.8, exit=True)   # cut hides it (was 62.1: 9 leaked frames in the night shop)
# t8: the failure at night. The cast arrives with the cut (was 64.7: a 3 s empty shop, then a mid-travel pop-in);
# the nephew stands on his stool so his head clears the counter in the wide shots.
act("nephew", 61.8, pos=[0.3, 1.9, 0.5], view="34", dir=1, pose="hold_watch", face="proud", prop="khata", hand="L", enter=True, visible=True, say=[131, 148])
act("chacha", 61.8, pos=[1.6, 2.5, 0], view="34", dir=-1, pose="hands_hips", face="grumpy", enter=True, visible=True)
act("chacha", 67.6, face="angry")
act("chacha", 70.4, face="worried")
act("nephew", 67.0, pose="hold_out", face="confused")
act("chacha", 69.0, exit=True)
act("nephew", 69.6, face="sad")
act("nephew", 71.0, pose="hold_out", face="confused")   # offers the khata nobody takes
act("nephew", 72.6, face="teary")
act("nephew", 74.5, exit=True)
# (PLACE DISCIPLINE: ma's t7/t8 "watching" beats removed — she stood in the shop's customer
#  zone as a cut-off dark sari; the night failure belongs to the nephew and chacha alone.)
# t9: the begging + the refusal.
act("chacha", 75.07, pos=[2.3, 3.15, 0], view="front", dir=1, pose="knock", face="worried", enter=True, visible=True, say=[149, 164])
act("ma", 75.07, pos=[-1.3, 0.5, 0], view="front", dir=1, pose="stand", face="cool", enter=True, visible=True)
act("ma", 77.2, pose="hands_hips", face="skeptical")
act("chacha", 76.9, pose="hold_out", face="worried", prop="box", hand="R")
act("chacha", 79.5, face="sad")   # the begging deepens (kills the 5.1 s frozen stretch)
act("ma", 79.3, pose="tiltR", face="skeptical")
act("ma", 81.3, face="sad")
act("ma", 83.6, face="worried")
act("ma", 85.1, face="tired")
act("ma", 86.8, face="skeptical")
act("ma", 89.3, face="proud")
act("ma", 91.9, exit=True)   # cut hides it
act("chacha", 82.0, pose="hold_out", face="nervous")
act("chacha", 83.5, pose="hold_out", face="teary")   # the plea cracks
act("rafi", 82.1, pos=[1.35, 1.05, 0], view="34", dir=-1, pose="stand", face="cool", enter=True, visible=True)   # rafi opens the door
act("rafi", 86.0, view="34", dir=-1, pose="stand", face="cool", say=[165, 176])
act("chacha", 86.0, pos=[2.3, 3.1, 0], view="front", dir=1, pose="stand", face="worried", prop=None)   # the box comes down, refused
act("rafi", 88.1, face="cool")
act("chacha", 87.8, face="teary")   # one last plead before the refusal lands
act("chacha", 89.6, pose="flinch", face="deadInside")
act("chacha", 91.9, exit=True)   # cut hides it — the door closes on him for good (was on stage 428 frames of the padosi ending)
act("rafi", 90.8, pose="hands_hips", face="cool")
# t10: the partnership.
act("rafi", 91.9, pos=[-0.55, 0.45, 0], view="34", dir=1, pose="stand", face="proud", say=[177, 188])
act("dokandar", 91.9, pos=[0.35, 1.7, 0], view="34", dir=-1, pose="stand", face="happy", enter=True, visible=True)
# t10+t11 extras: the big customers who only know Rafi, and the supplier now delivering to HIS counter
act("khoddeder", 91.9, pos=[0.05, 0.95, 0], view="34", dir=-1, pose="stand", face="happy", enter=True, visible=True)
act("khoddeder", 94.4, pose="hands_hips", face="excited")
act("khoddeder", 97.0, face="happy")
act("khoddeder", 100.0, pose="hold_watch", face="concentrate")
act("khoddeder", 103.0, face="think")
act("khoddeder", 106.0, pose="hands_hips", face="cool")
act("khoddeder", 109.0, face="proud")
act("khoddeder", 112.0, face="happy")
act("khoddeder", 115.0, pose="hold_watch", face="laugh")
act("khoddeder", 118.0, face="proud")
act("bepari", 91.9, pos=[0.9, 2.3, 0], view="34", dir=-1, pose="stand", face="concentrate", enter=True, visible=True)
act("bepari", 94.0, face="cool")
act("bepari", 97.5, pose="hold_watch", face="think")
act("bepari", 101.0, pose="hands_hips", face="cool")
act("bepari", 104.5, face="concentrate")
act("bepari", 108.0, pose="hold_watch", face="cool")
act("bepari", 111.5, face="think")
act("bepari", 115.0, pose="hands_hips", face="concentrate")
act("bepari", 118.5, face="happy")
act("dokandar", 95.5, pose="hold_out", face="happy", prop="coin", hand="R")
act("rafi", 96.4, pose="hold_up", face="excited", prop="coin", hand="R")
act("rafi", 97.7, pose="cheer", face="excited", prop=None)   # the coin pocketed   # the coin pocketed
# t11: the lesson + CTA.
act("dokandar", 98.5, pos=[0.25, 1.6, 0], view="34", dir=-1, pose="stand", face="happy", prop=None)
act("rafi", 98.5, pos=[-0.4, 1.4, 0], view="34", dir=-1, pose="write", face="proud", say=[189, 208])
act("rafi", 102.3, face="think")
act("rafi", 104.3, face="concentrate")
act("rafi", 105.8, pose="point_out", face="think")
act("dokandar", 103.4, face="happy")
act("dokandar", 107.2, pose="clap", face="happy")
act("dokandar", 110.6, face="sweetSmile")
act("dokandar", 114.8, pose="tiltL", face="happy")
act("dokandar", 117.9, face="proud")
act("rafi", 110.8, pose="hands_hips", face="proud")
act("rafi", 112.5, pose="stand", face="happy")
act("rafi", 116.6, pose="point_out", face="happy")
act("rafi", 118.7, pose="hold_up", face="sweetSmile", prop="khata", hand="R")

# ---------------------------------------------------------------- moods (light chapter changes on the beat)
F["moods"] = [{"at": S(t), "look": look} for t, look in [
  (0.2, "warm_morning"), (2.4, "flash_red"), (4.4, "cold_blue"), (6.8, "dim_plead"), (9.7, "night_arrival"),
  (12.2, "flash_gold"), (16.8, "warm_home"), (19.5, "gold_request"), (22.5, "flash_gold"), (25.7, "spot_ma"),
  (30.9, "bright_day"), (33.5, "gold_wash"), (39.6, "teach_warm"), (43.5, "cold_dusk"), (45.9, "dim_blue"),
  (49.3, "warm_home"), (53.4, "golden_new"), (58.5, "kettle_warm"), (61.5, "glow_khata"), (64.8, "night_fail"),
  (69.0, "lamp_pool"), (72.0, "cold_blue"), (75.1, "night_knock"), (82.1, "dim_plead"), (86.1, "steady_night"),
  (92.1, "bright_day"), (94.6, "flash_gold"), (96.9, "coin_glint"), (98.6, "golden_end"), (105.9, "teach_warm"),
  (111.4, "warm_sunset"), (116.7, "spot_raficontent"),
]]
# ---------------------------------------------------------------- fx (on the action word)
F["fx"] = [
  {"at": S(2.3), "kind": "clank", "on": "counter"},
  {"at": S(9.9), "kind": "knock_x2", "on": "door"},
  {"at": S(13.8), "kind": "dust_hit", "on": "door"},
  {"at": S(17.1), "kind": "knock_x2", "on": "door"},
  {"at": S(wtime("খাতা", 1)), "kind": "glow", "on": "khata"},
  {"at": S(41.0), "kind": "glint", "on": "jars"},
  {"at": S(45.5), "kind": "dust_hit", "on": "counter"},
  {"at": S(wtime("হাতে", 2)), "kind": "glow", "on": "khata"},
  {"at": S(wtime("চোর")), "kind": "sweat", "on": "nephew"},
  {"at": S(76.6), "kind": "knock_x2", "on": "door"},
  {"at": S(83.6), "kind": "dust", "on": "door"},
  {"at": S(wtime("অংশীদার")), "kind": "glint", "on": "coin"},
  {"at": S(wtime("নিয়ম")), "kind": "glow", "on": "khata"},
  {"at": S(119.9), "kind": "glint", "on": "bulb"},
]
# ---------------------------------------------------------------- sound
F["sound"] = [
  {"at": S(2.3), "name": "bag_land"}, {"at": S(9.9), "name": "door_knock"},
  {"at": S(13.8), "name": "arrival_hit"}, {"at": S(17.1), "name": "door_knock"},
  {"at": S(wtime("খাতা", 1)), "name": "khata_flip"}, {"at": S(45.5), "name": "bag_land"},
  {"at": S(58.6), "name": "kettle_steam"}, {"at": S(76.6), "name": "door_knock"},
  {"at": S(wtime("অংশীদার")), "name": "coin_chink"}, {"at": S(119.9), "name": "follow_pop"},
]
# ---------------------------------------------------------------- kicks
F["kicks"] = [{"at": S(t), "amp": a} for t, a in [
  (2.3, 1.3), (9.9, 1.2), (13.8, 1.4), (17.2, 1.2), (45.5, 1.4), (51.3, 1.2),
  (58.6, 1.0), (67.1, 1.2), (76.6, 1.3), (83.6, 1.2), (90.8, 1.4), (96.9, 1.3), (119.9, 1.1)
]]

# aim M/C stations at the subject's head height (heads were cut by the frame edge)
HEAD_Z = {"chacha": 1.56, "rafi": 1.58, "ma": 1.47, "nephew": 1.26, "dokandar": 1.60}
for tk in F["takes"]:
    for stn in tk["stations"]:
        if stn.get("framing") in ("M", "C") and stn.get("subject") in HEAD_Z:
            stn["aim"][2] = round(max(stn["aim"][2], HEAD_Z[stn["subject"]] + (0.02 if stn["framing"] == "C" else -0.06)), 2)

# travel shaping: big hops get ~1.1 s (mid-speed 12-20 px/f, many frames above the p90 line), small hops stay snappy
import math as _m
prev_pos = None
for tk in F["takes"]:
    for stn in tk["stations"]:
        if "travel" not in stn:
            prev_pos = stn["pos"]; continue
        if stn["travel"] < 3:
            d = _m.dist(stn["pos"], prev_pos) if prev_pos else 0
            if d > 1.5: stn["travel"] = max(stn["travel"], 1.8)
            else: stn["travel"] = round(max(0.4, stn["travel"] * 0.70), 2)
        prev_pos = stn["pos"]

# ---- face vocabulary: the renderer resolves cast faces from the MEMES registry (plain
# names) or the calm char2d kit faces ("k:" prefix). Map our script faces accordingly.
_CHAR2D_FACES = {"happy", "smug", "proud", "sad", "skeptical", "excited", "concentrate", "think",
                 "confused", "surprised", "shocked", "nervous", "angry", "teary", "laugh", "annoyed", "worried"}
_FACE_MAP = {"sweetSmile": "k:happy", "grumpy": "k:annoyed"}
for _a in A:
    _f = _a.get("face")
    if not _f:
        continue
    if _f in _FACE_MAP:
        _a["face"] = _FACE_MAP[_f]
    elif _f in _CHAR2D_FACES:
        _a["face"] = "k:" + _f
# 'cool', 'tired', 'deadInside' are MEMES names and stay as they are.

# ---- travel overrides: the slow long hops (peak < 20 px/f) carry hundreds of mid-speed
# frames; shortening them lifts the whole speed distribution (p90) without touching the
# gap-capped fast hops that own the 58 px/f peak. Applied after shaping, by (take, station).
TRAVEL_OVERRIDE = {
    ("t5", 1): 1.5,    # into khata insert: 84f -> 45f (peak 14 -> 31)
    ("t5", 4): 1.35,   # into chacha W: 54f -> 40f
    ("t2", 1): 1.0,    # into misti box insert: 40f -> 30f
    ("t7", 2): 0.7,    # into s2: 30f @ 7.7 -> 21f @ ~11
    ("t7", 3): 0.7,    # into s3: 34f @ 6.4 -> 21f @ ~10.4
    ("t7", 4): 1.3,    # into s4: 78f @ 6.4 -> 39f @ ~12.8
    ("t1", 1): 0.53,   # into s1: 24f @ 7.5 -> 16f @ ~11.3
    ("t1", 2): 1.0,    # into s2: 66f @ 6.8 -> 30f @ ~15
    ("t4", 1): 0.6,    # into s1: 27f @ 7.1 -> 18f @ ~10.7
    ("t4", 2): 0.9,    # into s2: 55f @ 5.4 -> 27f @ ~11
    ("t9", 1): 1.1,    # into s1: 55f @ 6.7 -> 33f @ ~11.2
    ("t9", 3): 0.7,    # into s3: 48f @ 4.6 -> 21f @ ~10.5
    ("t11", 6): 1.2,   # into s6: 55f @ 9.5 -> 36f @ ~14.5
}
for tk in F["takes"]:
    for idx, stn in enumerate(tk["stations"]):
        v = TRAVEL_OVERRIDE.get((tk["id"], idx))
        if v and "travel" in stn:
            stn["travel"] = v

# ---- whole-body rests: come closer (a dolly in, not a zoom) and raise the aim a touch,
# so figures read ~0.45 of frame height and the floor stops filling the bottom quarter.
for tk in F["takes"]:
    for stn in tk["stations"]:
        if stn.get("framing") == "W" and isinstance(stn["pos"], list) and isinstance(stn["aim"], list):
            k = 0.25
            stn["pos"] = [round(stn["pos"][0] + (stn["aim"][0] - stn["pos"][0]) * k, 2),
                          round(stn["pos"][1] + (stn["aim"][1] - stn["pos"][1]) * k, 2),
                          stn["pos"][2]]
            stn["aim"][2] = round(stn["aim"][2] + 0.05, 2)

# ---- head-cut fixes (probe-verified): tiny pans (aim) and trucks (pos+aim) so the
# biggest visible head never straddles the frame edge. Applied by (take id, station index).
CAM_FIX = {
    ("t8", 2): {"pan": -0.5},   ("t8", 1): {"truck": 0.5},  ("t5", 0): {"truck": -0.5},
    ("t5", 1): {"pan": 0.3},    ("t5", 4): {"pan": 0.5},    ("t8", 3): {"pan": -0.5},
    ("t2", 0): {"truck": 0.3},  ("t11", 2): {"pan": 0.3},   ("t7", 2): {"pan": -0.15},
    ("t9", 4): {"truck": 0.3},  ("t9", 3): {"truck": 0.5},  ("t2", 2): {"truck": -0.5},
    ("t5", 3): {"pan": -0.3},   ("t5", 5): {"truck": 0.5},  ("t5", 6): {"truck": 0.5},
    ("t8", 0): {"pan": -0.3},   ("t5", 2): {"pan": -0.3},   ("t7", 1): {"pan": -0.15},
    ("t11", 1): {"pan": 0.15},  ("t10", 2): {"pan": 0.15},  ("t3", 0): {"pan": 0.15},
    ("t6", 0): {"pan": 0.15},   ("t9", 7): {"pan": 0.15},
}
_applied = 0
for tk in F["takes"]:
    for idx, stn in enumerate(tk["stations"]):
        fx = CAM_FIX.get((tk["id"], idx))
        if not fx:
            continue
        if not isinstance(stn["aim"], list) or not isinstance(stn["pos"], list):
            print("WARN: CAM_FIX skipped for %s/s%d (non-literal pos/aim)" % (tk["id"], idx)); continue
        if "pan" in fx:
            stn["aim"][0] = round(stn["aim"][0] + fx["pan"], 2)
        if "truck" in fx:
            stn["pos"][0] = round(stn["pos"][0] + fx["truck"], 2)
            stn["aim"][0] = round(stn["aim"][0] + fx["truck"], 2)
        _applied += 1
print("CAM_FIX applied:", _applied, "of", len(CAM_FIX))

# ---- the flowing montage move: the two wordless W stations inside the t5 montage keep
# sliding (explicit drift ~0.5 m/s sideways) so the camera never settles between hops and
# the whole montage reads as one continuous 3.5-4.5 s travelling shot.
_t5 = next(tk for tk in F["takes"] if tk["id"] == "t5")
_t5["stations"][2]["drift"] = [0.66, 0.34, 0.0]
_t5["stations"][4]["drift"] = [0.81, -0.14, 0.0]

json.dump(F, open(f"{EP}/film.json", "w"), ensure_ascii=False, indent=1)
print("film.json written:", len(F["takes"]), "takes,", sum(len(t["stations"]) for t in F["takes"]), "stations,", len(A), "acts,", len(F["moods"]), "moods,", len(F["fx"]), "fx")
