#!/usr/bin/env python3
"""Patch builder to v7: spaced takes + act prop discipline."""
p = '/home/z/my-project/scripts/build_law11_art.py'
s = open(p).read()
start = s.index('# ---- t1')
end = s.index('F["end"] = 3640')
new_takes = '''# ---- t1 shop_am 0.0-9.6: THE FIRING (cold open). Frame 0 hook: the boss points out the door,
# Rafi stands IN FRONT of the counter with his packed wage bag, the nephew already wears the spot behind it.
T.append({"id": "t1", "place": "shop_am", "stations": [
  st(0.0, [0.15, -2.0, 1.5], [0.4, 2.1, 1.35], "chacha", "W", 24, ["chacha", "rafi", "nephew", "counter", "jars"], 0.55, 0.6),
  st(wtime("রাফি", 1), [0.1, -1.9, 1.3], [0.15, 0.4, 1.3], "rafi", "M", 24, ["rafi", "chacha", "counter", "jars"], 0.5, 0.7, "রাফি"),
  st(wtime("ভাগ্নেরে"), [-2.6, -1.7, 1.25], [0.3, 1.7, 1.15], "counter", "P", 24, ["counter", "chacha", "nephew", "rafi", "jars"], 0.5, 1.1, "ভাগ্নেরে"),
  st(wtime("শিখাইলাম"), [0.4, -2.1, 1.35], [0.3, 0.4, 1.35], "rafi", "C", 26, ["rafi", "chacha"], 0.55, 0.7, "শিখাইলাম"),
]})
# ---- t2 home_night 9.6-16.6: THE TEASER — the knock at night, sweets box held out.
T.append({"id": "t2", "place": "home_night", "stations": [
  st(wtime("কিন্তু"), [1.6, -1.8, 1.35], [2.45, 3.3, 1.3], "chacha", "W", 24, ["chacha", "ma", "door", "box"], 0.5, 0.6, "কিন্তু"),
  st(wtime("মিষ্টির", 1), [2.3, -1.35, 1.2], [2.45, 3.3, 1.25], "chacha", "M", 24, ["chacha", "door", "box"], 0.5, 0.8, "মিষ্টির"),
  st(wtime("বাসায়", 1), [1.7, -1.9, 1.3], [2.45, 3.3, 1.28], "chacha", "M", 24, ["chacha", "ma", "door", "box"], 0.5, 0.7),
  st(wtime("হাজির"), [0.7, -2.1, 1.25], [2.45, 3.3, 1.35], "chacha", "W", 24, ["chacha", "ma", "door"], 0.55, 0.7, "হাজির"),
]})
# ---- t3 home_in 16.7-25.6: THE FLASHBACK — the uncle arrives WITH the khata, handing the nephew over.
T.append({"id": "t3", "place": "home_in", "stations": [
  st(wtime("অথচ"), [1.8, -1.75, 1.35], [2.45, 3.3, 1.3], "chacha", "W", 24, ["chacha", "rafi", "nephew", "ma", "door"], 0.5, 0.6, "অথচ"),
  st(wtime("ভাগ্নেকে"), [2.2, -1.2, 1.2], [2.45, 3.3, 1.25], "chacha", "M", 24, ["chacha", "nephew", "door", "khata"], 0.5, 0.8, "ভাগ্নেকে"),
  st(wtime("রাফি", 2), [1.3, -1.6, 1.3], [1.0, 1.2, 1.3], "chacha", "M", 26, ["chacha", "rafi", "nephew"], 0.5, 0.7, "রাফি"),
  st(wtime("পোলাটারে"), [1.35, -1.5, 1.35], [1.15, 1.25, 1.4], "chacha", "C", 26, ["chacha", "nephew"], 0.55, 0.55, "পোলাটারে"),
]})
# ---- t4 home_in 25.6-32.2: THE MOTHER'S WARNING (the tea glass stays dry on this visit).
T.append({"id": "t4", "place": "home_in", "stations": [
  st(wtime("সব", 3), [-0.7, -1.7, 1.25], [-0.8, 1.05, 1.25], "ma", "M", 24, ["ma", "rafi", "chacha", "nephew", "table"], 0.5, 0.55, "সব"),
  st(wtime("মালিকের", 1), [-0.85, -1.85, 1.35], [-0.85, 1.05, 1.4], "ma", "C", 26, ["ma", "rafi"], 0.5, 0.6, "মালিকের"),
  st(wtime("লোক"), [-0.3, -2.0, 1.2], [-0.35, 0.95, 1.3], "rafi", "M", 24, ["rafi", "ma", "chacha"], 0.55, 0.7, "লোক"),
]})
# ---- t5 shop_day 32.2-49.2: THE TEACHING — khata writing, the flowing montage move, the wage.
T.append({"id": "t5", "place": "shop_day", "stations": [
  st(wtime("মায়ের"), [0.1, -2.1, 1.6], [0.1, 1.3, 1.3], "rafi", "W", 24, ["rafi", "nephew", "chacha", "counter", "jars"], 0.5, 0.6, "মায়ের"),
  st(wtime("খাতা", 1), [-0.75, -1.35, 1.2], [0.3, 1.6, 1.1], "khata", "O", 40, ["khata", "rafi", "nephew"], 0.5, 0.6, "খাতা"),
  st(wtime("খদ্দের", 1), [-3.0, -1.6, 1.3], [0.2, 1.6, 1.12], "counter", "P", 24, ["counter", "rafi", "nephew", "khata", "jars"], 0.5, 0.7, "খদ্দের"),
  st(43.6, [0.2, -2.0, 1.5], [0.4, 2.1, 1.35], "chacha", "W", 24, ["chacha", "rafi", "nephew", "counter"], 0.5, 3.6),
  st(wtime("বেতন"), [0.75, -1.4, 1.3], [0.6, 0.45, 1.25], "wage", "O", 36, ["wage", "rafi", "chacha"], 0.5, 0.6, "বেতন"),
  st(wtime("ফিরলো", 1), [0.2, -2.0, 1.5], [0.3, 2.1, 1.35], "chacha", "W", 24, ["chacha", "rafi", "nephew", "counter", "door"], 0.55, 0.8),
]})
# ---- t6 home_in 49.2-53.3: THE MOTHER'S SECOND WARNING.
T.append({"id": "t6", "place": "home_in", "stations": [
  st(wtime("যার"), [-0.7, -1.75, 1.25], [-0.8, 1.05, 1.25], "ma", "M", 24, ["ma", "rafi", "table", "plate"], 0.5, 0.55, "যার"),
  st(wtime("ভাত", 2), [-0.9, -1.9, 1.35], [-0.85, 1.05, 1.4], "ma", "C", 26, ["ma", "rafi"], 0.55, 0.7, "ভাত"),
]})
# ---- t7 padosi_golden 53.3-62.1: THE NEW JOB — half pay, the secret list kept in his own hand.
T.append({"id": "t7", "place": "padosi_golden", "stations": [
  st(wtime("১", 3), [-0.5, -2.0, 1.7], [-0.3, 1.2, 1.35], "rafi", "W", 24, ["rafi", "dokandar", "counter", "bench", "jars"], 0.5, 0.6),
  st(wtime("বেতনে"), [-0.55, -1.75, 1.3], [-0.4, 1.0, 1.3], "rafi", "M", 24, ["rafi", "dokandar", "counter", "kettle"], 0.5, 0.7, "বেতনে"),
  st(wtime("শিখালো", 2) - 1.7, [1.75, -1.0, 1.25], [1.5, 1.35, 1.15], "kettle", "P", 30, ["kettle", "counter"], 0.5, 0.7),
  st(wtime("শিখালো", 2), [-0.7, -1.85, 1.5], [-0.4, 1.35, 1.3], "rafi", "W", 24, ["rafi", "dokandar", "counter", "bench"], 0.5, 0.7, "শিখালো"),
  st(wtime("হাতে", 2), [-1.3, -1.3, 1.3], [-0.75, 1.0, 1.2], "khata", "O", 36, ["khata", "rafi"], 0.55, 0.6, "হাতে"),
]})
# ---- t8 shop_night 62.1-75.0: THE FAILURE — the nephew alone with the khata nobody honours.
T.append({"id": "t8", "place": "shop_night", "stations": [
  st(wtime("ওদিকে"), [0.1, -2.0, 1.5], [0.15, 1.5, 1.3], "nephew", "W", 24, ["nephew", "chacha", "counter", "jars"], 0.5, 0.6, "ওদিকে"),
  st(64.3, [0.75, -1.4, 1.3], [0.5, 1.4, 1.25], "nephew", "M", 24, ["nephew", "counter", "khata"], 0.5, 0.7),
  st(wtime("চিনতো"), [0.85, -1.65, 1.35], [0.5, 1.45, 1.3], "nephew", "M", 26, ["nephew", "khata", "jars"], 0.5, 0.6, "চিনতো"),
  st(wtime("চোর"), [0.7, -1.6, 1.35], [0.45, 1.35, 1.35], "nephew", "C", 26, ["nephew", "khata"], 0.5, 0.55, "চোর"),
  st(72.8, [-2.7, -1.8, 1.5], [0.0, 1.5, 1.3], "nephew", "W", 24, ["nephew", "counter", "door", "jars"], 0.5, 0.9),
  st(wtime("কাছে"), [0.45, -1.55, 1.3], [0.3, 1.35, 1.3], "nephew", "M", 24, ["nephew", "counter", "khata"], 0.55, 0.7, "কাছে"),
]})
# ---- t9 home_night 75.0-91.6: THE BEGGING + THE REFUSAL — the same door, no khata, only the sweets box.
T.append({"id": "t9", "place": "home_night", "stations": [
  st(wtime("মাসে"), [1.7, -1.85, 1.35], [2.45, 3.3, 1.3], "chacha", "W", 24, ["chacha", "ma", "door", "box"], 0.5, 0.6),
  st(wtime("প্যাকেট", 2), [2.25, -1.15, 1.25], [2.45, 3.3, 1.25], "chacha", "M", 24, ["chacha", "door", "box"], 0.5, 0.7, "প্যাকেট"),
  st(wtime("বললেন", 2), [1.9, -1.5, 1.2], [2.45, 3.3, 1.25], "chacha", "M", 24, ["chacha", "ma", "door", "box"], 0.5, 0.7),
  st(wtime("আবার"), [0.4, -2.1, 1.25], [2.45, 3.3, 1.35], "chacha", "W", 24, ["chacha", "ma", "door"], 0.5, 0.9, "আবার"),
  st(wtime("পারে", 2), [2.2, -1.05, 1.4], [2.45, 3.3, 1.28], "chacha", "C", 26, ["chacha", "box"], 0.5, 0.6, "পারে"),
  st(wtime("চাচা", 5), [0.85, -1.55, 1.3], [0.95, 1.1, 1.3], "rafi", "M", 24, ["rafi", "chacha", "door"], 0.5, 0.55, "চাচা"),
  st(wtime("ভরসাটা"), [0.8, -1.85, 1.35], [1.35, 1.5, 1.35], "rafi", "M", 24, ["rafi", "chacha", "door"], 0.5, 0.7, "ভরসাটা"),
  st(wtime("শিখানো"), [0.35, -2.1, 1.25], [1.7, 2.8, 1.35], "chacha", "W", 24, ["chacha", "rafi", "door"], 0.55, 0.8),
]})
# ---- t10 padosi_day 92.0-98.5: THE PARTNERSHIP — the coin glints, the hand-off lands.
T.append({"id": "t10", "place": "padosi_day", "stations": [
  st(wtime("রাফি", 7), [-0.55, -2.0, 1.7], [-0.4, 1.3, 1.35], "rafi", "W", 24, ["rafi", "dokandar", "counter", "bench", "jars"], 0.5, 0.6),
  st(wtime("মালিক"), [-0.6, -1.65, 1.3], [-0.5, 1.05, 1.3], "dokandar", "M", 24, ["dokandar", "rafi", "counter"], 0.5, 0.8, "মালিক"),
  st(wtime("অংশীদার"), [-1.7, -1.35, 1.3], [-0.8, 1.0, 1.3], "rafi", "C", 26, ["rafi", "dokandar", "coin"], 0.55, 0.6, "অংশীদার"),
]})
# ---- t11 padosi_day 98.5-121.3: THE LESSON + CTA — Rafi's own khata opens on his own counter.
T.append({"id": "t11", "place": "padosi_day", "stations": [
  st(wtime("কাজ", 4), [-0.5, -2.0, 1.6], [-0.4, 1.3, 1.3], "rafi", "W", 24, ["rafi", "dokandar", "counter", "bench", "jars"], 0.5, 0.6, "কাজ"),
  st(wtime("জায়গাটা"), [-0.6, -1.7, 1.3], [-0.45, 1.1, 1.3], "rafi", "M", 26, ["rafi", "dokandar", "counter"], 0.5, 0.7),
  st(wtime("নিয়ম"), [-1.05, -1.4, 1.25], [-0.65, 1.0, 1.15], "khata", "O", 40, ["khata", "rafi"], 0.5, 0.6, "নিয়ম"),
  st(wtime("নাও"), [-0.85, -1.8, 1.4], [-0.55, 1.15, 1.35], "rafi", "C", 26, ["rafi", "dokandar"], 0.5, 0.6, "নাও"),
  st(114.5, [-0.4, -2.0, 1.6], [-0.3, 1.25, 1.3], "rafi", "W", 24, ["rafi", "dokandar", "counter", "bench"], 0.5, 0.9),
  st(wtime("লিখুন"), [-0.75, -1.5, 1.3], [-0.55, 1.05, 1.25], "rafi", "M", 24, ["rafi", "dokandar", "counter", "khata"], 0.5, 0.6, "লিখুন"),
  st(wtime("করুন"), [-0.6, -1.7, 1.35], [-0.45, 1.1, 1.35], "rafi", "C", 26, ["rafi", "dokandar"], 0.55, 0.55, "করুন"),
]})
'''
s = s[:start] + new_takes + s[end:]

# act prop discipline
s = s.replace(
  'act("ma", 25.65, pos=[-0.85, 1.15, 0], view="34", dir=1, pose="point_out", face="skeptical", say=[57, 64])',
  'act("ma", 25.65, pos=[-0.85, 1.15, 0], view="34", dir=1, pose="point_out", face="skeptical", say=[57, 64])\n'
  'act("chacha", 25.7, pose="stand", face="smug", prop=None)   # the khata stays at Rafi\'s home now')
s = s.replace('act("nephew", 72.6, face="teary")',
              'act("nephew", 72.6, face="teary")\nact("nephew", 74.5, exit=True)')
s = s.replace('act("dokandar", 93.9, pose="hold_out", face="happy", prop="coin")',
              'act("dokandar", 95.5, pose="hold_out", face="happy", prop="coin")')
s = s.replace('act("rafi", 94.7, pose="hold_up", face="excited", prop="coin")',
              'act("rafi", 96.4, pose="hold_up", face="excited", prop="coin")')
s = s.replace('act("rafi", 96.3, pose="cheer", face="excited", prop=None)',
              'act("rafi", 97.7, pose="cheer", face="excited", prop=None)   # the coin pocketed')
s = s.replace('act("dokandar", 98.5, pos=[0.6, 1.8, 0], view="34", dir=-1, pose="stand", face="happy")',
              'act("dokandar", 98.5, pos=[0.6, 1.8, 0], view="34", dir=-1, pose="stand", face="happy", prop=None)')
open(p, 'w').write(s)
print("v7 written")
