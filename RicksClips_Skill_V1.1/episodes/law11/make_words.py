#!/usr/bin/env python3
"""Build voice/words.json for Law 11: word timings distributed across each script
line's real audio span (line starts come from the script's own timecodes; the
span of a line ends at the next line's start minus a small pause)."""
import json, os

LINES = [
 ("chacha",  0.0,  "কাল থেকে আর আসা লাগবে না, রাফি। আমার ভাগ্নে এখন সব পারে।"),
 ("rafi",    4.0,  "চাচা, ১০ বছর... আপনার ভাগ্নেরে তো সব আমিই শিখাইলাম!"),
 ("narr",    9.0,  "কিন্তু ৩ মাস পর, সেই চাচাই মিষ্টির প্যাকেট হাতে... রাফির বাসায় এসে হাজির!"),
 ("narr",   15.0,  "অথচ ১ বছর আগে, চাচা নিজেই ভাগ্নেকে নিয়ে রাফির বাসায় এসে বলেছিলেন,"),
 ("chacha", 21.0,  "রাফি, পোলাটারে কাজ শিখায় দাও... তুমি তো আমার নিজের পোলার মতো!"),
 ("ma",     25.0,  "সব শিখাইস না, বাবা... মালিকের ভাগ্নে, মালিকেরই লোক!"),
 ("narr",   31.0,  "মায়ের কথা হেসে উড়িয়ে, রাফি ভাগ্নেকে শিখালো সাপ্লায়ারদের নম্বর, বাকির খাতা... আর চিনিয়ে দিলো সব বাকির খদ্দের। ভাগ্নে সব শিখে ফেলতেই, চাচা বললেন সেই কথা... আর ১০ বছর পর, রাফি মাত্র ১ মাসের বেতন নিয়ে বাসায় ফিরলো।"),
 ("ma",     48.0,  "যার পাতে ভাত দিলি... সেই তোর ভাত কাড়লো, বাবা!"),
 ("narr",   53.0,  "১ মাস পর, পাশের দোকানে অর্ধেক বেতনে চাকরি নিয়ে, রাফি এবার সবাইকে কাজ শিখালো... কিন্তু কিছু বড় খদ্দের রাখলো নিজের হাতে। ওদিকে বাকির খাতা ছিলো ভাগ্নের হাতে... কিন্তু বাকির খদ্দেররা চিনতো শুধু রাফিকে। ভাগ্নে বাকির টাকা চাইতে গিয়ে খদ্দেরদের বললো চোর... আর তারা মাল নিতে গেলো রাফির কাছে!"),
 ("narr",   75.0,  "৩ মাসে বিক্রি অর্ধেক হতেই, চাচা মিষ্টির প্যাকেট হাতে রাফির বাসায় এসে বললেন,"),
 ("chacha", 81.0,  "রাফি, কাল থেকে আবার আসো, বাবা... ভাগ্নে আমার কিছুই পারে না!"),
 ("rafi",   86.0,  "চাচা, কাজ তো সবই শিখাইছিলাম... খালি মানুষের ভরসাটা শিখানো যায় না।"),
 ("narr",   92.0,  "রাফি আর ফিরলো না... ৬ মাস পর, পাশের দোকানের মালিক ওকে ৪ আনার অংশীদার বানালেন!"),
 ("narr",   99.0,  "কাজ সবাইকে শেখান... কিন্তু নিজের জায়গাটা কাউকে শিখিয়ে দিবেন না। রবার্ট গ্রিনের বইয়ের ১১ নম্বর নিয়ম বলে, নিজেকে এমন জায়গায় নাও, যেখানে তোমাকে ছাড়া চলে না।"),
 ("narr",  112.0,  "আপনার চাকরিতেও কি, মালিকের আত্মীয় এসে কারো জায়গা নিয়েছে? কী হয়েছিলো? কমেন্টে লিখুন। এমন আরো গল্প পেতে ফলো করুন।"),
]
END = 121.3

words, index = [], 0
sentences = []
for li, (who, start, text) in enumerate(LINES):
    nxt = LINES[li + 1][1] if li + 1 < len(LINES) else END
    span = max(1.0, nxt - start - 0.45)
    ws = [w for w in text.replace("...", " ... ").replace("।", " ").replace(",", " , ").replace("?", " ? ").replace("!", " ! ").split() if w not in (" ",)]
    # re-join ellipses/punct as part of flow but keep keys clean
    clean = [w.strip("।") for w in ws]
    weight = [max(2, len(w)) for w in clean]
    tot = sum(weight)
    t = start + 0.05
    i0 = index
    for w, wt in zip(clean, weight):
        dur = span * wt / tot
        e = min(t + dur, nxt - 0.15)
        words.append({"w": w, "s": round(t, 2), "e": round(e, 2)})
        t = e
        index += 1
    sentences.append({"who": who, "i0": i0, "i1": index - 1,
                      "start": start, "end": nxt})

json.dump(words, open(os.path.join(os.path.dirname(__file__), "voice", "words.json"), "w"), ensure_ascii=False, indent=1)
print(f"{len(words)} words; lines:")
for s in sentences:
    a, b = words[s["i0"]], words[s["i1"]]
    n = s["i1"] - s["i0"] + 1
    pace = n / max(0.1, b["e"] - a["s"])
    print(f"  [{s['i0']:3d}-{s['i1']:3d}] {s['who']:6s} {s['start']:6.1f}s  '{a['w']}…{b['w']}'  {n:2d}w  {pace:.1f} w/s")
print(f"last word ends {words[-1]['e']} s -> film end frame {round((words[-1]['e'] + 0.6) * 30)}")
