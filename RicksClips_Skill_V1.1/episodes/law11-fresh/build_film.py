#!/usr/bin/env python3
"""Build film.json for episodes/law11-fresh — EVERY scene driven by the script line being spoken,
timed against the REAL narration (voice/words.json comes from tools/audio_probe.py, energy-aligned).
Script direction table (see SCRIPT.md): each take states which script line it serves; every station
names the noun that line is about. Author: the artist, 2026-11-22."""
import json

FPS = 30
END_S = 121.3
END = int(END_S * FPS)  # 3639

def S(sec): return {"s": round(sec, 2)}
def st(t, pos, aim, framing, subject, shows=(), word=None, hold=.45, travel=1.0, **kw):
    d = {"at": S(t) if isinstance(t, (int, float)) else t, "pos": pos, "aim": aim, "lens": kw.pop("lens", 24),
         "subject": subject, "framing": framing, "shows": list(shows), "hold": hold, "travel": travel}
    if word: d["word"] = word
    d.update(kw)
    return d
def act(who, t, pos=None, pose=None, face=None, view=None, dir=None, say=None, **kw):
    d = {"who": who, "at": S(t) if isinstance(t, (int, float)) else t}
    if pos is not None: d["pos"] = pos
    if pose: d["pose"] = pose
    if face: d["face"] = face
    if view: d["view"] = view
    if dir is not None: d["dir"] = dir
    if say is not None: d["say"] = say
    d.update(kw)
    return d
def fx(t, kind, on=None, **kw):
    d = {"at": S(t), "kind": kind}
    if on: d["on"] = on
    d.update(kw); return d
def mood(t, look): return {"at": S(t), "look": look}
def snd(t, name): return {"at": S(t), "name": name}
def kick(t, amp=1.3): return {"at": S(t), "amp": amp}

# --- the timecoded script (the SOURCE OF EVERY SCENE); word spans walked against the REAL audio timings ---
_LINES = [
    (0.1, "কাল থেকে আর আসা লাগবে না, রাফি। আমার ভাগ্নে এখন সব পারে।"),
    (4.0, "চাচা, ১০ বছর... আপনার ভাগ্নেরে তো সব আমিই শিখাইলাম!"),
    (9.1, "কিন্তু ৩ মাস পর, সেই চাচাই মিষ্টির প্যাকেট হাতে... রাফির বাসায় এসে হাজির!"),
    (15.1, "অথচ ১ বছর আগে, চাচা নিজেই ভাগ্নেকে নিয়ে রাফির বাসায় এসে বলেছিলেন,"),
    (21.1, "রাফি, পোলাটারে কাজ শিখায় দাও... তুমি তো আমার নিজের পোলার মতো!"),
    (25.1, "সব শিখাইস না, বাবা... মালিকের ভাগ্নে, মালিকেরই লোক!"),
    (31.1, "মায়ের কথা হেসে উড়িয়ে, রাফি ভাগ্নেকে শিখালো সাপ্লায়ারদের নম্বর, বাকির খাতা... আর চিনিয়ে দিলো সব বাকির খদ্দের। ভাগ্নে সব শিখে ফেলতেই, চাচা বললেন সেই কথা... আর ১০ বছর পর, রাফি মাত্র ১ মাসের বেতন নিয়ে বাসায় ফিরলো।"),
    (48.0, "যার পাতে ভাত দিলি... সেই তোর ভাত কাড়লো, বাবা!"),
    (53.0, "১ মাস পর, পাশের দোকানে অর্ধেক বেতনে চাকরি নিয়ে, রাফি এবার সবাইকে কাজ শিখালো... কিন্তু কিছু বড় খদ্দের রাখলো নিজের হাতে। ওদিকে বাকির খাতা ছিলো ভাগ্নের হাতে... কিন্তু বাকির খদ্দেররা চিনতো শুধু রাফিকে। ভাগ্নে বাকির টাকা চাইতে গিয়ে খদ্দেরদের বললো চোর... আর তারা মাল নিতে গেলো রাফির কাছে!"),
    (75.0, "৩ মাসে বিক্রি অর্ধেক হতেই, চাচা মিষ্টির প্যাকেট হাতে রাফির বাসায় এসে বললেন,"),
    (81.0, "রাফি, কাল থেকে আবার আসো, বাবা... ভাগ্নে আমার কিছুই পারে না!"),
    (86.0, "চাচা, কাজ তো সবই শিখাইছিলাম... খালি মানুষের ভরসাটা শিখানো যায় না।"),
    (92.0, "রাফি আর ফিরলো না... ৬ মাস পর, পাশের দোকানের মালিক ওকে ৪ আনার অংশীদার বানালেন!"),
    (99.0, "কাজ সবাইকে শেখান... কিন্তু নিজের জায়গাটা কাউকে শিখিয়ে দিবেন না। রবার্ট গ্রিনের বইয়ের ১১ নম্বর নিয়ম বলে, নিজেকে এমন জায়গায় নাও, যেখানে তোমাকে ছাড়া চলে না।"),
    (112.0, "আপনার চাকরিতেও কি, মালিকের আত্মীয় এসে কারো জায়গা নিয়েছে? কী হয়েছিলো? কমেন্টে লিখুন। এমন আরো গল্প পেতে ফলো করুন।"),
]
_WORDS = json.load(open("voice/words.json"))  # audio-probe: energy-aligned, punctuation dropped
_punct = " .,?!;:-…।!\"'"
_spans, ptr = [], 0
for _s, _t in _LINES:
    _want = [tok for tok in (t.strip(_punct) for t in _t.replace("...", " … ").replace("?", " ? ").replace(",", " , ").replace("।", " । ").replace("!", " ! ").split()) if tok]
    i0 = ptr
    for tok in _want:
        assert ptr < len(_WORDS) and _WORDS[ptr]["w"].strip(_punct) == tok, f"word walk failed at {ptr}: want {tok!r}, got {_WORDS[ptr]['w'] if ptr < len(_WORDS) else 'EOF'!r}"
        ptr += 1
    _spans.append([i0, ptr - 1])
assert ptr == len(_WORDS), f"span walk: {ptr} vs {len(_WORDS)}"
def widx(word, line):
    lo, hi = _spans[line]
    for i in range(lo, hi + 1):
        if _WORDS[i]["w"].strip(" .,?!;:-…") == word: return i
    raise KeyError(f"word {word!r} not in line {line}")

takes, acts = [], []

# ---------------------------------------------------------------- T1 (lines 1-2, 0.0-9.0) — HOOK: kaka FIRES rafi; bhagne ALREADY at the till
takes.append({"id": "t1", "place": "dokan_night", "stations": [
    st(0.0, [2.5, -1.3, 1.5], [2.7, 1.3, 1.45], "C", "kaka", ["counter", "door"], lead=5, word="কাল", hold=.5, travel=.7, drift=[0.3, 0, 0]),
    st(2.0, [1.2, -2.0, 1.5], [2.2, 2.7, 0.85], "W", "bhagne", ["till", "counter", "kaka", "rafi"], lead=5, word="ভাগ্নে", hold=.45, travel=1.2),
    st(4.3, [-1.4, -1.6, 1.4], [0.3, 0.95, 1.35], "W", "rafi", ["counter", "kaka"], lead=5, word="চাচা", hold=.4, travel=.9),
    st(6.6, [1.3, -0.3, 1.3], [2.0, 2.3, 1.1], "O", "till", ["till", "bhagne", "counter"], lead=5, word="আমিই", hold=.4, travel=.8),
    st(8.0, [-2.4, -2.8, 1.9], [0.4, 2.4, 1.2], "P", "counter", ["counter", "kaka", "rafi", "bhagne"], hold=.35, travel=1.4),
]})
acts += [
    act("kaka", 0.0, [2.7, 1.25, 0], pose="point_out", face="proud", view="front", dir=-1, say=_spans[0]),
    act("bhagne", 0.0, [2.3, 2.75, 0], pose="sit", face="smug", view="34", dir=-1),
    act("rafi", 0.0, [-1.6, 0.9, 0], pose="stand", face="shocked", view="front", dir=1),
    act("kaka", 2.0, pose="hands_hips", face="proud"),
    act("bhagne", 5.4, pose="lean_in", face="smug"),
    act("rafi", 4.0, pose="lean_in", face="pleading", say=_spans[1]),
    act("rafi", 6.6, pose="point_out", face="angryFist"),
    act("kaka", 7.6, pose="shrug", face="cool"),
    act("bhagne", 7.8, face="smug", pose="phone"),
    act("bhagne", 8.9, exit=True), act("rafi", 8.9, exit=True),
]

# ---------------------------------------------------------------- T2 (line 3, 9.0-15.1) — 3 months later: kaka with the sweet packet AT RAFI'S DOOR (night)
takes.append({"id": "t2", "place": "basha_night", "stations": [
    st(9.0, [1.0, -1.2, 1.6], [0.0, 4.2, 1.4], "P", "door", ["door", "step"], lead=5, word="কিন্তু", hold=.5, travel=1.0),
    st(10.6, [0.2, -1.8, 1.4], [0.15, 2.4, 1.3], "W", "kaka", ["door", "bulb"], lead=5, word="পর", hold=.4, travel=1.2),
    st(12.4, [-1.1, 1.0, 1.35], [0.15, 3.35, 1.4], "W", "kaka", ["door", "step"], lead=5, word="প্যাকেট", hold=.45, travel=.8, drift=[0.3, 0, 0]),
    st(13.9, [-0.6, 2.0, 1.5], [0.15, 3.4, 1.5], "C", "kaka", ["door", "bulb"], lead=5, word="হাজির", hold=.35, travel=.6),
]})
acts += [
    act("kaka", 9.0, [0.15, 1.9, 0], pose="m:walk/B", face="nervous", dir=1, walk=True, move_s=1.6),
    act("kaka", 11.2, [0.15, 3.3, 0], pose="knock", face="worried"),
    act("kaka", 12.4, pose="hold_out", face="hopeful", say=_spans[2]),
    act("kaka", 13.9, pose="hold_out", face="scared"),
]

# ---------------------------------------------------------------- T3 (lines 4-5, 15.1-25.1) — FLASHBACK, morning: kaka HIMSELF brings bhagne to rafi's home
takes.append({"id": "t3", "place": "basha_morn", "stations": [
    st(15.1, [1.8, -1.2, 1.55], [0.5, 2.4, 1.3], "W", "kaka", ["door", "bike", "tulsi"], lead=5, word="অথচ", hold=.45, travel=1.4),
    st(17.8, [-1.0, 0.4, 1.4], [0.5, 3.2, 1.3], "W", "kaka", ["door", "bhagne", "step"], lead=5, word="ভাগ্নেকে", hold=.4, travel=.9),
    st(20.9, [-0.9, 1.6, 1.45], [0.2, 3.35, 1.45], "M", "kaka", ["door", "bhagne", "rafi"], lead=5, word="রাফি", hold=.4, travel=.7),
    st(23.0, [-1.6, 0.6, 1.4], [-0.3, 3.6, 1.35], "W", "rafi", ["door", "kaka", "bhagne"], lead=5, word="শিখায়", hold=.4, travel=1.0),
]})
acts += [
    act("kaka", 15.1, [0.4, 1.6, 0], pose="m:walk/B", face="delight", dir=1, walk=True, move_s=1.6),
    act("bhagne", 15.1, [1.2, 1.8, 0], pose="m:walk/C", face="bored", dir=1, walk=True, move_s=1.6, visible=True),
    act("kaka", 17.3, [0.2, 3.3, 0], pose="hold_out", face="delight"),
    act("bhagne", 17.6, [0.9, 3.0, 0], pose="stand", face="smug", dir=-1),
    act("rafi", 18.5, [-0.5, 3.6, 0], pose="stand", face="surprised", dir=-1, visible=True),
    act("kaka", 20.9, pose="grip_shoulder", face="sweetSmile", say=_spans[4]),
    act("rafi", 22.0, pose="shrug", face="awkward"),
    act("kaka", 25.0, exit=True), act("bhagne", 25.0, exit=True),
]

# ---------------------------------------------------------------- T4 (line 6, 25.1-31.1) — inside home: MA warns, rafi laughs it off (day)
takes.append({"id": "t4", "place": "bhitore_day", "stations": [
    st(25.1, [-1.2, -0.6, 1.35], [-0.7, 2.0, 1.3], "W", "ma", ["table_top", "tea_cup", "rafi"], lead=5, word="সব", hold=.45, travel=.8),
    st(27.0, [-1.4, -0.2, 1.5], [-0.75, 2.0, 1.45], "M", "ma", ["table_top", "rafi"], lead=5, word="মালিকের", hold=.4, travel=.6),
    st(28.7, [-0.6, 0.0, 1.4], [0.55, 1.9, 1.3], "W", "rafi", ["table_top", "ma", "stove"], lead=5, word="লোক", hold=.4, travel=.8),
    st(30.0, [-1.9, -1.4, 1.7], [0.6, 2.8, 1.0], "P", "table_top", ["table_top", "ma", "rafi", "stove", "calendar"], hold=.35, travel=1.3),
]})
acts += [
    act("ma", 25.1, [-0.8, 2.0, 0], pose="lean_in", face="worried", view="34", dir=1, say=_spans[5], enter=True),
    act("rafi", 25.1, [0.6, 1.9, 0], pose="sit", face="happy", dir=-1),
    act("ma", 27.0, pose="finger_up", face="serious"),
    act("rafi", 28.7, pose="hand_mouth", face="giggle"),
    act("ma", 29.6, pose="hands_hips", face="grumpy"),
    act("ma", 31.0, exit=True),
]

# ---------------------------------------------------------------- T5 (line 7, 31.1-49.2) — THE TEACHING: numbers, khata, customers -> kaka says THE line -> ten years, rafi walks out with 1 month's pay
takes.append({"id": "t5", "place": "dokan_day", "stations": [
    st(31.1, [-3.1, -0.4, 1.6], [-4.1, 2.55, 1.3], "W", "rafi", ["desk", "khata_book"], hold=.45, travel=.9, drift=[0.3, 0, 0]),
    st(33.4, [-3.4, 1.2, 1.4], [-3.6, 3.2, 1.5], "M", "rafi", ["desk", "khata_book", "bhagne"], hold=.4, travel=.7),
    st(35.3, [-4.5, 1.2, 1.75], [-5.35, 3.6, 2.05], "O", "board", ["board", "desk", "bhagne", "khata_book"], lead=5, word="নম্বর", hold=.4, travel=.9),
    st(36.5, [-2.6, 1.4, 1.3], [-3.25, 3.4, 1.3], "M", "bhagne", ["desk", "khata_book", "rafi"], lead=5, word="খাতা", hold=.4, travel=.7),
    st(38.6, [0.4, -1.4, 1.45], [0.35, 1.0, 1.3], "W", "khoddor", ["counter", "rafi", "bhagne", "khoddor"], lead=5, word="খদ্দের", hold=.4, travel=1.2),
    st(41.0, [1.1, -0.6, 1.5], [0.25, 2.6, 1.5], "M", "kaka", ["counter"], lead=5, word="চাচা", hold=.35, travel=.6),
    st(44.8, [-2.4, -2.6, 1.9], [0.0, 2.4, 1.2], "P", "counter", ["counter", "kaka", "bhagne"], hold=.5, travel=3.4),
    st(46.4, [0.9, -0.4, 1.3], [1.6, 2.0, 1.1], "O", "counter", ["counter", "till", "rafi"], lead=5, word="বেতন", hold=.4, travel=.9),
    st(48.0, [-2.6, -1.4, 1.5], [-3.85, 4.0, 1.4], "P", "door", ["door", "rafi"], lead=5, word="ফিরলো", hold=.35, travel=1.0),
]})
acts += [
    act("rafi", 31.1, [-4.15, 2.5, 0], pose="khata", face="serious", view="34", dir=-1),
    act("bhagne", 31.1, [-3.3, 2.5, 0], pose="lean_in", face="curious", view="34", dir=1, visible=True),
    act("rafi", 33.4, pose="point_out", dir=-1, face="serious"),
    act("rafi", 35.3, pose="point_up", face="serious"),
    act("bhagne", 34.4, pose="notebook", face="curious"),
    act("bhagne", 36.5, pose="write", face="happy"),
    act("bhagne", 38.2, [-3.3, 2.5, 0], pose="write", face="happy"),
    act("khoddor", 38.4, [0.6, 0.6, 0], pose="m:walk/B", face="money", dir=1, walk=True, move_s=1.0, enter=True),
    act("khoddor", 39.4, [0.3, 0.9, 0], pose="stand", face="money"),
    act("rafi", 37.6, pose="grip_two", face="sweetSmile", dir=1),
    act("kaka", 40.4, [0.2, 2.6, 0], pose="stand", face="cool", view="front", dir=-1, visible=True),
    act("kaka", 41.0, pose="point_out", face="smug"),
    act("rafi", 42.6, [0.3, 0.9, 0], pose="coin", face="sad", dir=-1),
    act("rafi", 45.2, [-0.5, 1.2, 0], pose="m:walk/sad", face="deadInside", dir=-1, walk=True, move_s=2.0),
    act("rafi", 47.4, [-3.85, 3.6, 0], pose="stand", face="deadInside", dir=-1),
    act("kaka", 49.1, exit=True), act("bhagne", 49.1, exit=True), act("khoddor", 49.1, exit=True),
]

# ---------------------------------------------------------------- T6 (line 8, 49.2-53.5) — inside home, dusk: MA consoles rafi
takes.append({"id": "t6", "place": "bhitore_dusk", "stations": [
    st(49.4, [-1.3, -0.4, 1.35], [-0.55, 1.95, 1.3], "M", "ma", ["table_top", "tea_cup", "rafi"], lead=5, word="ভাত", hold=.45, travel=.8),
    st(51.6, [-0.4, 0.2, 1.5], [0.45, 1.85, 1.45], "C", "rafi", ["table_top", "ma", "rafi"], lead=5, word="ভাত", hold=.4, travel=.6),
    st(52.8, [-2.0, -1.2, 1.7], [0.8, 3.0, 1.1], "P", "table_top", ["table_top", "ma", "rafi", "stove", "window"], lead=5, word="বাবা", hold=.35, travel=1.2),
]})
acts += [
    act("ma", 49.4, [-0.6, 2.0, 0], pose="grip_shoulder", face="sad", view="34", dir=1, say=_spans[7], visible=True),
    act("rafi", 49.4, [0.4, 1.8, 0], pose="sit", face="crying", dir=-1),
    act("rafi", 51.6, pose="stand", face="sad"),
    act("ma", 52.4, pose="hold_out", face="worried"),
    act("ma", 53.4, exit=True),
]

# ---------------------------------------------------------------- T7 (line 9a, 53.5-66.5) — ROUND 2: half pay at the neighbour's; teaches everyone; keeps the big customers; the khata is bhagne's
takes.append({"id": "t7", "place": "pasher_day", "stations": [
    st(53.5, [1.1, -0.7, 2.2], [1.0, 1.9, 1.15], "O", "tarazu", ["tarazu", "counter"], lead=5, word="দোকানে", hold=.45, travel=.9, drift=[0.3, 0, 0]),
    st(55.5, [0.6, -1.8, 1.5], [1.6, 2.0, 1.3], "W", "pashi", ["counter", "pashi", "rafi", "tulu"], lead=5, word="চাকরি", hold=.4, travel=1.1),
    st(57.8, [0.8, -0.8, 1.35], [1.5, 1.2, 1.3], "W", "rafi", ["counter", "tulu", "pashi"], lead=5, word="কাজ", hold=.4, travel=.8),
    st(60.0, [-2.5, 1.1, 2.05], [-3.4, 3.05, 0.95], "O", "desk", ["desk", "paper_stack", "rafi", "khoddor"], lead=5, word="খদ্দের", hold=.4, travel=.8),
    st(62.0, [-2.0, 0.2, 1.4], [-3.0, 2.5, 1.3], "W", "rafi", ["desk"], lead=5, word="হাতে", hold=.35, travel=.5),
    st(63.5, [-2.6, 0.6, 1.3], [-3.3, 2.85, 1.15], "M", "bhagne", ["desk", "paper_stack"], lead=5, word="খাতা", hold=.4, travel=.7),
    st(65.2, [0.8, -1.6, 1.5], [1.0, 1.4, 1.3], "W", "khoddor", ["counter", "khoddor", "pashi", "rafi"], lead=5, word="রাফিকে", hold=.4, travel=1.0),
]})
acts += [
    act("pashi", 53.5, [1.6, 2.6, 0], pose="stand", face="proud", view="front", dir=-1, enter=True),
    act("rafi", 53.5, [1.4, 0.9, 0], pose="stand", face="serious", dir=1),
    act("tulu", 53.5, [2.4, 1.0, 0], pose="stand", face="happy", dir=-1, enter=True),
    act("rafi", 55.5, pose="coin", face="money"),
    act("rafi", 57.8, pose="point_out", face="serious"),
    act("tulu", 58.2, pose="lean_in", face="curious"),
    act("khoddor", 59.8, [0.6, 0.6, 0], pose="m:walk/B", face="money", dir=1, walk=True, move_s=1.0, visible=True),
    act("khoddor", 60.8, [0.4, 0.9, 0], pose="stand", face="money"),
    act("rafi", 61.8, [-3.0, 2.2, 0], pose="grip_box", face="sneaky", view="34", dir=1),
    act("rafi", 63.0, pose="stand", face="sneaky"),
    act("bhagne", 63.3, [-3.3, 2.3, 0], pose="hold_out", face="money", view="front", dir=1, visible=True),
    act("bhagne", 65.0, pose="stand", face="confused"),
    act("khoddor", 63.4, pose="stand", face="happy"),
    act("khoddor", 65.4, pose="hands_hips", face="sus"),
]

# ---------------------------------------------------------------- T8 (line 9b, 66.5-75.0) — customers only know RAFI; bhagne calls him a THIEF; they cross to rafi and take their goods from him
takes.append({"id": "t8", "place": "pasher_day", "stations": [
    st(66.5, [0.8, -1.6, 1.5], [1.0, 1.4, 1.3], "W", "khoddor", ["counter", "khoddor", "rafi", "bhagne"], lead=5, word="রাফিকে", hold=.45, travel=.9, drift=[0.3, 0, 0]),
    st(71.6, [-2.4, 0.4, 1.5], [-3.2, 2.8, 1.3], "M", "bhagne", ["desk"], lead=5, word="চোর", hold=.45, travel=.6),
    st(72.9, [0.2, -2.0, 1.55], [0.9, 1.0, 1.25], "W", "khoddor", ["counter", "khoddor", "rafi", "bhagne"], lead=5, word="মাল", hold=.35, travel=1.0),
    st(73.9, [1.6, -0.4, 1.4], [2.55, 2.45, 1.4], "M", "rafi", ["counter", "khoddor"], lead=5, word="কাছে", hold=.35, travel=.5),
]})
acts += [
    act("khoddor", 68.4, pose="shrug", face="confused"),
    act("khoddor", 70.6, pose="flinch", face="offended"),
    act("bhagne", 71.6, [-3.3, 2.3, 0], pose="finger_up", face="angryFist", view="front", dir=1, say=[widx("চোর", 8), widx("চোর", 8)]),
    act("khoddor", 72.6, [0.9, 0.8, 0], pose="m:walk/A", face="angry", dir=1, walk=True, move_s=1.0),
    act("khoddor", 73.6, [1.3, 0.9, 0], pose="coin", face="money"),
    act("rafi", 73.9, [2.6, 2.6, 0], pose="hold_out", face="sweetSmile", view="front", dir=-1),
    act("tulu", 74.0, pose="clap", face="excited"),
    act("rafi", 74.9, exit=True), act("khoddor", 74.9, exit=True), act("tulu", 74.9, exit=True),
    act("bhagne", 74.9, exit=True), act("pashi", 74.9, exit=True),
]

# ---------------------------------------------------------------- T9 (lines 10-12, 75.0-92.0) — sales halve; kaka begs AT NIGHT again; rafi comes out; his answer: trust cannot be taught
takes.append({"id": "t9", "place": "basha_night", "stations": [
    st(75.4, [0.2, -1.8, 1.5], [0.15, 2.2, 1.3], "W", "kaka", ["door", "bulb"], lead=5, word="বিক্রি", hold=.45, travel=1.2, drift=[0.3, 0, 0]),
    st(78.5, [-1.0, 1.4, 1.4], [0.15, 3.35, 1.4], "M", "kaka", ["door", "step"], lead=5, word="প্যাকেট", hold=.4, travel=.8),
    st(81.2, [0.9, 1.0, 1.5], [0.3, 4.0, 1.45], "W", "rafi", ["door", "kaka", "bulb"], lead=5, word="রাফি", hold=.4, travel=.8),
    st(83.5, [-0.7, 1.9, 1.5], [0.1, 3.5, 1.5], "M", "kaka", ["door", "bulb"], lead=5, word="আসো", hold=.4, travel=.5),
    st(84.9, [-1.5, 0.6, 1.55], [0.2, 3.9, 1.45], "W", "kaka", ["door", "kaka", "rafi"], lead=5, word="ভাগ্নে", hold=.4, travel=.8),
    st(87.2, [0.35, 2.0, 1.5], [0.3, 4.3, 1.5], "C", "rafi", ["door", "kaka"], lead=5, word="কাজ", hold=.45, travel=.5),
    st(89.6, [-1.9, -0.8, 1.7], [0.2, 4.0, 1.4], "P", "door", ["door", "kaka", "rafi", "bulb"], lead=5, word="যায়", hold=.45, travel=1.3),
    st(91.0, [0.7, 0.4, 1.4], [0.0, 4.4, 1.4], "W", "door", ["door", "rafi"], hold=.3, travel=1.0),
]})
acts += [
    act("kaka", 75.4, [0.2, 1.0, 0], pose="m:walk/C", face="worried", dir=1, walk=True, move_s=1.8, visible=True),
    act("kaka", 77.4, [0.15, 3.3, 0], pose="hold_out", face="scared"),
    act("kaka", 81.0, pose="hold_out", face="crying", say=_spans[10]),
    act("rafi", 81.4, [0.1, 4.1, 0], pose="stand", face="calm", dir=-1, walk=True, move_s=0.8),
    act("rafi", 82.2, [0.1, 4.3, 0], pose="stand", face="calm"),
    act("kaka", 83.5, pose="grip_two", face="pleading"),
    act("rafi", 87.2, pose="hands_hips", face="serious", say=_spans[11]),
    act("rafi", 89.0, pose="stand", face="sad"),
    act("kaka", 90.0, pose="hand_mouth", face="wail"),
    act("kaka", 91.9, exit=True),
]

# ---------------------------------------------------------------- T10 (line 13, 92.0-99.6) — PAYOFF: rafi never returned; six months later the neighbour makes him a 4-anna PARTNER
takes.append({"id": "t10", "place": "rasta_morn", "stations": [
    st(92.0, [0.2, -2.6, 1.5], [0.0, 1.8, 1.35], "W", "rafi", ["cart", "lamp", "puddle"], lead=5, word="ফিরলো", hold=.45, travel=1.3, drift=[0.3, 0, 0]),
    st(94.4, [-0.6, -1.4, 1.45], [-1.6, 1.6, 1.35], "W", "rafi", ["cart", "pashi", "rafi"], lead=5, word="মাস", hold=.4, travel=1.1),
    st(96.8, [-1.8, -0.2, 1.4], [-2.9, 2.4, 1.35], "M", "pashi", ["cart", "pashi", "rafi"], lead=5, word="মালিক", hold=.4, travel=.8),
    st(98.2, [-2.7, 1.2, 2.05], [-3.4, 3.05, 0.95], "O", "desk", ["desk", "paper_stack", "coin_tray", "anna_board"], lead=5, word="আনার", hold=.4, travel=.7),
]})
acts += [
    act("rafi", 92.0, [0.0, 2.6, 0], pose="m:walk/B", face="happy", dir=1, walk=True, move_s=2.0, visible=True),
    act("rafi", 94.2, [-2.0, 1.4, 0], pose="stand", face="happy", dir=1),
    act("pashi", 93.0, [-3.0, 2.6, 0], pose="hold_out", face="delight", view="34", dir=1, visible=True),
    act("rafi", 96.8, pose="grip_two", face="excited"),
    act("pashi", 96.8, pose="grip_two", face="delight"),
    act("rafi", 98.4, pose="cheer", face="starstruck"),
    act("pashi", 99.5, exit=True),
]

# ---------------------------------------------------------------- T11 (lines 14-15, 99.6-121.3) — THE LAW stated at rafi's own counter; the CTA; loop to frame 0
takes.append({"id": "t11", "place": "pasher_gold", "stations": [
    st(99.6, [0.2, -2.0, 1.5], [1.5, 1.7, 1.3], "W", "rafi", ["counter", "rafi", "tulu", "desk"], lead=5, word="শেখান", hold=.45, travel=1.2, drift=[0.3, 0, 0]),
    st(102.2, [-2.6, 1.1, 2.05], [-3.4, 3.05, 0.95], "O", "desk", ["desk", "paper_stack", "ink_bottle"], lead=5, word="জায়গাটা", hold=.45, travel=.8),
    st(104.8, [-1.6, -0.4, 1.5], [-2.6, 2.2, 1.45], "M", "rafi", ["desk", "tulu"], lead=5, word="শিখিয়ে", hold=.4, travel=.5),
    st(106.0, [-2.6, 1.6, 1.6], [-3.4, 4.9, 2.5], "O", "anna_board", ["anna_board", "desk"], lead=5, word="নম্বর", hold=.4, travel=.9),
    st(112.0, [0.0, -1.0, 1.5], [1.4, 1.75, 1.45], "M", "rafi", ["counter", "tulu"], lead=5, word="চাকরিতেও", hold=.45, travel=.7),
    st(116.4, [0.2, -1.8, 1.55], [1.5, 1.8, 1.35], "W", "rafi", ["counter", "sign_face", "tarazu"], lead=5, word="কমেন্টে", hold=.4, travel=1.0),
    st(118.9, [0.8, -0.6, 1.5], [1.4, 1.7, 1.4], "M", "rafi", ["counter", "tulu"], lead=5, word="ফলো", hold=.4, travel=.7),
    st(120.4, [0.2, -2.2, 1.7], [1.6, 1.8, 1.2], "P", "counter", ["counter", "rafi", "tulu", "sign_face"], hold=.35, travel=2.6, loop=True),
]})
acts += [
    act("rafi", 99.6, [1.3, 1.7, 0], pose="point_out", face="serious", view="front", dir=-1),
    act("tulu", 99.6, [2.4, 1.0, 0], pose="lean_in", face="curious", dir=-1, visible=True),
    act("rafi", 101.2, pose="khata", face="serious"),
    act("rafi", 102.2, [-2.9, 2.4, 0], pose="grip_box", face="serious", view="34", dir=1),
    act("rafi", 104.8, pose="hands_hips", face="cool"),
    act("rafi", 106.0, pose="point_up", face="serious"),
    act("rafi", 108.6, pose="hold_out", face="sweetSmile"),
    act("rafi", 112.0, [1.3, 1.7, 0], pose="point_out", face="happy", view="front", dir=-1, say=_spans[14]),
    act("tulu", 112.6, pose="clap", face="excited"),
    act("rafi", 118.9, pose="cheer", face="excited"),
]

sentences = [
    {"text": _LINES[0][1], "words": _spans[0], "subject": "kaka",
     "nouns": [{"word": "ভাগ্নে", "n": 1, "show": "bhagne"}]},
    {"text": _LINES[1][1], "words": _spans[1], "subject": "rafi",
     "nouns": [{"word": "বছর", "n": 1, "show": "rafi"}]},
    {"text": _LINES[2][1], "words": _spans[2], "subject": "kaka",
     "nouns": [{"word": "বাসায়", "n": 1, "show": "door"}, {"word": "চাচাই", "n": 1, "show": "kaka"}]},
    {"text": _LINES[3][1], "words": _spans[3], "subject": "kaka",
     "nouns": [{"word": "ভাগ্নেকে", "n": 1, "show": "bhagne"}, {"word": "চাচা", "n": 2, "show": "kaka"}]},
    {"text": _LINES[4][1], "words": _spans[4], "subject": "kaka",
     "nouns": [{"word": "পোলাটারে", "n": 1, "show": "bhagne"}, {"word": "রাফি", "n": 2, "show": "rafi"}, {"word": "কাজ", "n": 1, "show": "rafi"}]},
    {"text": _LINES[5][1], "words": _spans[5], "subject": "ma",
     "nouns": [{"word": "বাবা", "n": 1, "show": "rafi"}]},
    {"text": _LINES[6][1], "words": _spans[6], "subject": "rafi",
     "nouns": [{"word": "নম্বর", "n": 1, "show": "board"}, {"word": "খাতা", "n": 1, "show": "khata_book"}, {"word": "খদ্দের", "n": 1, "show": "khoddor"}, {"word": "বেতন", "n": 1, "show": "rafi"}, {"word": "ফিরলো", "n": 1, "show": "door"}]},
    {"text": _LINES[7][1], "words": _spans[7], "subject": "ma",
     "nouns": [{"word": "ভাত", "n": 1, "show": "tea_cup"}, {"word": "বাবা", "n": 2, "show": "rafi"}]},
    {"text": _LINES[8][1], "words": _spans[8], "subject": "rafi",
     "nouns": [{"word": "দোকানে", "n": 1, "show": "counter"}, {"word": "চাকরি", "n": 1, "show": "pashi"}, {"word": "হাতে", "n": 2, "show": "desk"}, {"word": "খাতা", "n": 2, "show": "bhagne"}, {"word": "খদ্দের", "n": 2, "show": "khoddor"}, {"word": "রাফিকে", "n": 1, "show": "rafi"}, {"word": "চোর", "n": 1, "show": "bhagne"}, {"word": "মাল", "n": 1, "show": "khoddor"}]},
    {"text": _LINES[9][1], "words": _spans[9], "subject": "kaka",
     "nouns": [{"word": "বিক্রি", "n": 1, "show": "kaka"}, {"word": "প্যাকেট", "n": 2, "show": "kaka"}, {"word": "বাসায়", "n": 4, "show": "door"}]},
    {"text": _LINES[10][1], "words": _spans[10], "subject": "kaka",
     "nouns": [{"word": "আসো", "n": 1, "show": "door"}, {"word": "রাফি", "n": 6, "show": "rafi"}]},
    {"text": _LINES[11][1], "words": _spans[11], "subject": "rafi",
     "nouns": [{"word": "কাজ", "n": 3, "show": "rafi"}, {"word": "চাচা", "n": 5, "show": "kaka"}]},
    {"text": _LINES[12][1], "words": _spans[12], "subject": "pashi",
     "nouns": [{"word": "মালিক", "n": 1, "show": "pashi"}, {"word": "আনার", "n": 1, "show": "anna_board"}, {"word": "অংশীদার", "n": 1, "show": "paper_stack"}]},
    {"text": _LINES[13][1], "words": _spans[13], "subject": "rafi",
     "nouns": [{"word": "শেখান", "n": 1, "show": "tulu"}, {"word": "জায়গাটা", "n": 1, "show": "desk"}, {"word": "নম্বর", "n": 2, "show": "anna_board"}]},
    {"text": _LINES[14][1], "words": _spans[14], "subject": "rafi",
     "nouns": [{"word": "চাকরিতেও", "n": 1, "show": "rafi"}, {"word": "কমেন্টে", "n": 1, "show": "sign_face"}, {"word": "ফলো", "n": 1, "show": "rafi"}]},
]

film = {
    "title": "৪৮ শক্তির নিয়ম — নিয়ম ১১ (বাংলা): কাজ সবাইকে শেখান, জায়গা কাউকে না",
    "fps": FPS, "size": [1080, 1920], "end": END, "words": "voice/words.json",
    "puppet_pkg": ["cast", "../../templates/vector2d_characters/code"],
    "camera_idea": {
        "name": "Rest on the noun, travel on the verb",
        "why": "Mode B scene-cut story: cuts land only on the script's place/time jumps (shop -> door -> flashback -> home -> new shop -> street). Inside every scene one slow move carries the line: push on the talker, travel 3-7 s on the walk/knock/handshake, close on the face that owns the moral word. Every station time comes from the real narration's word timings.",
        "signature": "The sweet packet knocks at the same blue door three times, at three lights (night, morning, night) — the camera repeats its approach but ends closer each time, until the door closes on it.",
    },
    "cast": {
        "kaka": {"puppet": "cast:fresh_cast/kaka", "height": 1.68, "heads_tall": 2.7},
        "rafi": {"puppet": "cast:fresh_cast/rafi", "height": 1.70, "heads_tall": 2.8},
        "bhagne": {"puppet": "cast:fresh_cast/bhagne", "height": 1.38, "heads_tall": 2.6},
        "ma": {"puppet": "cast:fresh_cast/ma", "height": 1.58, "heads_tall": 2.6},
        "pashi": {"puppet": "cast:fresh_cast/pashi", "height": 1.72, "heads_tall": 2.8},
        "tulu": {"puppet": "cast:fresh_cast/tulu", "height": 1.30, "heads_tall": 2.5},
        "khoddor": {"puppet": "cast:fresh_cast/khoddor", "height": 1.75, "heads_tall": 2.8},
    },
    "places": {
        "dokan_night": {"set": "dokan", "light": "night", "backdrop": 9.0},
        "basha_night": {"set": "basha_door", "light": "night", "backdrop": 9.0},
        "basha_morn": {"set": "basha_door", "light": "morning", "backdrop": 9.0},
        "bhitore_day": {"set": "bhitore", "light": "interior", "backdrop": 9.0},
        "dokan_day": {"set": "dokan", "light": "day", "backdrop": 9.0},
        "bhitore_dusk": {"set": "bhitore", "light": "golden", "backdrop": 9.0},
        "pasher_day": {"set": "pasher", "light": "day", "backdrop": 9.0},
        "pasher_gold": {"set": "pasher", "light": "golden", "backdrop": 9.0},
        "rasta_morn": {"set": "rasta", "light": "morning", "backdrop": 12.0},
    },
    "props": {"khata_book": {"kind": "notebook"}, "coin": {"kind": "coin"}},
    "takes": takes,
    "kicks": [kick(0.1, 1.4), kick(9.4, 1.3), kick(12.6, 1.3), kick(15.3, 1.2), kick(35.5, 1.2), kick(46.9, 1.4),
              kick(50.0, 1.2), kick(72.3, 1.5), kick(73.4, 1.3), kick(76.0, 1.3), kick(97.2, 1.4), kick(99.8, 1.3)],
    "acts": sorted(acts, key=lambda a: a["at"]["s"] if isinstance(a["at"], dict) else a["at"]),
    "sentences": sentences,
    "fx": [
        fx(9.8, "door_knock", on="door"), fx(11.2, "door_knock", on="door"),
        fx(36.8, "khata_flip", on="khata_book"), fx(63.9, "khata_flip", on="desk"),
        fx(46.9, "coin_glint", on="till"), fx(44.0, "glow", on="lamp_globe"),
        fx(50.3, "glow", on="coals"), fx(56.3, "coin_glint", on="counter"),
        fx(62.5, "khata_flip", on="desk"), fx(72.2, "glint", on="bhagne"),
        fx(73.0, "dust_puff", on="khoddor"), fx(73.5, "coin_glint", on="counter"),
        fx(76.2, "door_knock", on="door"), fx(77.8, "door_knock", on="door"),
        fx(89.8, "glow", on="bulb"), fx(98.3, "paper_flutter", on="paper_stack"),
        fx(99.8, "glow", on="lamp_globe"), fx(102.5, "paper_flutter", on="paper_stack"),
    ],
    "moods": [
        mood(0.1, "cool_blue"), mood(1.8, "warm_glow"), mood(4.2, "cool_blue"), mood(6.6, "flash_red"),
        mood(8.0, "warm_glow"), mood(9.0, "cool_blue"), mood(12.4, "warm_glow"), mood(14.0, "spot_hero"),
        mood(15.1, "warm_up"), mood(18.0, "gold_wash"), mood(21.0, "warm_glow"), mood(23.0, "gold_wash"),
        mood(25.1, "warm_up"), mood(27.0, "cool_blue"), mood(28.7, "warm_glow"), mood(30.0, "gold_wash"),
        mood(31.1, "warm_up"), mood(33.0, "gold_wash"), mood(38.6, "warm_glow"), mood(41.0, "spot_hero"),
        mood(43.8, "cool_blue"), mood(46.4, "gold_wash"), mood(48.0, "cool_blue"),
        mood(49.4, "gold_wash"), mood(51.6, "cool_blue"), mood(52.8, "warm_glow"),
        mood(53.5, "warm_up"), mood(55.5, "gold_wash"), mood(57.8, "warm_glow"), mood(61.8, "spot_hero"),
        mood(63.5, "cool_blue"), mood(66.5, "warm_up"), mood(70.6, "gold_wash"), mood(72.0, "flash_red"),
        mood(73.0, "cool_blue"), mood(73.9, "gold_wash"),
        mood(75.4, "cool_blue"), mood(78.5, "warm_glow"), mood(83.5, "spot_hero"),
        mood(85.5, "cool_blue"), mood(87.2, "spot_hero"), mood(89.6, "cool_blue"), mood(91.0, "flash_red"),
        mood(92.0, "warm_up"), mood(96.8, "gold_wash"), mood(98.2, "warm_glow"),
        mood(99.6, "gold_wash"), mood(102.2, "spot_hero"), mood(105.0, "cool_blue"), mood(106.0, "gold_wash"),
        mood(108.6, "warm_glow"), mood(112.0, "gold_wash"), mood(116.4, "warm_glow"), mood(118.9, "gold_wash"), mood(120.4, "warm_glow"),
    ],
    "sound": [
        snd(0.1, "arrival_hit"), snd(9.8, "door_knock"), snd(11.2, "door_knock"), snd(36.8, "khata_flip"),
        snd(63.9, "khata_flip"), snd(46.9, "coin_chink"), snd(56.3, "coin_chink"), snd(72.3, "follow_pop"),
        snd(73.5, "coin_chink"), snd(76.2, "door_knock"), snd(77.8, "door_knock"),
        snd(98.3, "paper_flutter"), snd(102.5, "paper_flutter"), snd(119.4, "follow_pop"),
    ],
}

json.dump(film, open("film.json", "w"), ensure_ascii=False, indent=1)
n_st = sum(len(t["stations"]) for t in takes)
print(f"film.json: {len(takes)} takes, {n_st} stations, {len(acts)} acts, {len(sentences)} sentences, {END} frames ({END/FPS:.1f} s)")
