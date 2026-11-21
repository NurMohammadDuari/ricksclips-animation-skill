#!/usr/bin/env python3
"""Patch v8: rafi prop continuity + shot mix rebalance (W 45 / M 20 / C 7 / P+O world-led)."""
p = '/home/z/my-project/scripts/build_law11_art.py'
s = open(p).read()

# ---- A. rafi prop continuity: keeps the wage bag at home, leaves it there
s = s.replace(
  'st(wtime("যার"), [-0.7, -1.75, 1.25], [-0.8, 1.05, 1.25], "ma", "M", 24, ["ma", "rafi", "table", "plate"], 0.5, 0.55, "যার"),',
  'st(wtime("যার"), [-0.7, -2.0, 1.3], [-0.8, 1.05, 1.25], "ma", "W", 24, ["ma", "rafi", "table", "plate"], 0.55, 0.55, "যার"),')
s = s.replace('act("rafi", 49.2, pos=[0.1, 0.5, 0], view="34", dir=-1, pose="stand", face="sad")',
              'act("rafi", 49.2, pos=[0.1, 0.5, 0], view="34", dir=-1, pose="hold_watch", face="sad")   # the wage bag still in his hand at home')
s = s.replace('act("rafi", 53.3, pos=[-0.35, 1.35, 0], view="34", dir=1, pose="stand", face="tired", say=[111, 130])',
              'act("rafi", 53.3, pos=[-0.35, 1.35, 0], view="34", dir=1, pose="stand", face="tired", prop=None, say=[111, 130])   # the bag left at home')

# ---- B. mix rebalance: M -> W, C -> M, two box O-inserts
mix = [
  # t3 st3 রাফি M -> W
  ('st(wtime("রাফি", 2), [1.3, -1.6, 1.3], [1.0, 1.2, 1.3], "chacha", "M", 26, ["chacha", "rafi", "nephew"], 0.5, 0.7, "রাফি"),',
   'st(wtime("রাফি", 2), [1.1, -2.15, 1.45], [0.9, 1.3, 1.25], "chacha", "W", 24, ["chacha", "rafi", "nephew"], 0.5, 0.8, "রাফি"),'),
  # t3 st4 পোলাটারে C -> M
  ('st(wtime("পোলাটারে"), [1.35, -1.5, 1.35], [1.15, 1.25, 1.4], "chacha", "C", 26, ["chacha", "nephew"], 0.55, 0.55, "পোলাটারে"),',
   'st(wtime("পোলাটারে"), [1.5, -1.6, 1.3], [1.15, 1.25, 1.4], "chacha", "M", 24, ["chacha", "nephew"], 0.55, 0.55, "পোলাটারে"),'),
  # t4 st3 লোক M -> W
  ('st(wtime("লোক"), [-0.3, -2.0, 1.2], [-0.35, 0.95, 1.3], "rafi", "M", 24, ["rafi", "ma", "chacha"], 0.55, 0.7, "লোক"),',
   'st(wtime("লোক"), [-0.45, -2.35, 1.4], [-0.35, 0.95, 1.25], "rafi", "W", 24, ["rafi", "ma", "chacha"], 0.55, 0.7, "লোক"),'),
  # t8 st2 M -> W (keep one M)
  ('st(64.3, [0.75, -1.4, 1.3], [0.5, 1.4, 1.25], "nephew", "M", 24, ["nephew", "counter", "khata"], 0.5, 0.7),',
   'st(64.3, [0.55, -2.15, 1.45], [0.4, 1.5, 1.2], "nephew", "W", 24, ["nephew", "counter", "khata"], 0.5, 0.7),'),
  # t8 চোর C -> M
  ('st(wtime("চোর"), [0.7, -1.6, 1.35], [0.45, 1.35, 1.35], "nephew", "C", 26, ["nephew", "khata"], 0.5, 0.55, "চোর"),',
   'st(wtime("চোর"), [0.85, -1.7, 1.3], [0.45, 1.4, 1.3], "nephew", "M", 24, ["nephew", "khata"], 0.5, 0.55, "চোর"),'),
  # t8 কাছে M -> W
  ('st(wtime("কাছে"), [0.45, -1.55, 1.3], [0.3, 1.35, 1.3], "nephew", "M", 24, ["nephew", "counter", "khata"], 0.55, 0.7, "কাছে"),',
   'st(wtime("কাছে"), [0.4, -2.2, 1.45], [0.25, 1.4, 1.25], "nephew", "W", 24, ["nephew", "counter", "khata"], 0.55, 0.7, "কাছে"),'),
  # t9 প্যাকেট M -> O insert on the held sweets box
  ('st(wtime("প্যাকেট", 2), [2.25, -1.15, 1.25], [2.45, 3.3, 1.25], "chacha", "M", 24, ["chacha", "door", "box"], 0.5, 0.7, "প্যাকেট"),',
   'st(wtime("প্যাকেট", 2), [2.28, -1.0, 1.22], [2.42, 3.2, 1.18], "box", "O", 36, ["box", "chacha", "door"], 0.5, 0.7, "প্যাকেট"),'),
  # t9 চাচা M -> W
  ('st(wtime("চাচা", 5), [0.85, -1.55, 1.3], [0.95, 1.1, 1.3], "rafi", "M", 24, ["rafi", "chacha", "door"], 0.5, 0.55, "চাচা"),',
   'st(wtime("চাচা", 5), [0.8, -2.15, 1.45], [1.0, 1.3, 1.25], "rafi", "W", 24, ["rafi", "chacha", "door"], 0.5, 0.6, "চাচা"),'),
  # t10 মালিক M -> W
  ('st(wtime("মালিক"), [-0.6, -1.65, 1.3], [-0.5, 1.05, 1.3], "dokandar", "M", 24, ["dokandar", "rafi", "counter"], 0.5, 0.8, "মালিক"),',
   'st(wtime("মালিক"), [-0.6, -2.1, 1.45], [-0.45, 1.2, 1.25], "dokandar", "W", 24, ["dokandar", "rafi", "counter"], 0.5, 0.8, "মালিক"),'),
  # t11 জায়গাটা M -> W
  ('st(wtime("জায়গাটা"), [-0.6, -1.7, 1.3], [-0.45, 1.1, 1.3], "rafi", "M", 26, ["rafi", "dokandar", "counter"], 0.5, 0.7),',
   'st(wtime("জায়গাটা"), [-0.55, -2.1, 1.5], [-0.4, 1.25, 1.25], "rafi", "W", 24, ["rafi", "dokandar", "counter"], 0.5, 0.7),'),
  # t11 নাও C -> M
  ('st(wtime("নাও"), [-0.85, -1.8, 1.4], [-0.55, 1.15, 1.35], "rafi", "C", 26, ["rafi", "dokandar"], 0.5, 0.6, "নাও"),',
   'st(wtime("নাও"), [-0.9, -1.7, 1.3], [-0.6, 1.15, 1.3], "rafi", "M", 24, ["rafi", "dokandar"], 0.5, 0.6, "নাও"),'),
  # t11 করুন C -> M
  ('st(wtime("করুন"), [-0.6, -1.7, 1.35], [-0.45, 1.1, 1.35], "rafi", "C", 26, ["rafi", "dokandar"], 0.55, 0.55, "করুন"),',
   'st(wtime("করুন"), [-0.7, -1.8, 1.3], [-0.5, 1.15, 1.3], "rafi", "M", 24, ["rafi", "dokandar"], 0.55, 0.55, "করুন"),'),
  # t2 মিষ্টির M -> O insert on the held box
  ('st(wtime("মিষ্টির", 1), [2.3, -1.35, 1.2], [2.45, 3.3, 1.25], "chacha", "M", 24, ["chacha", "door", "box"], 0.5, 0.8, "মিষ্টির"),',
   'st(wtime("মিষ্টির", 1), [2.28, -1.0, 1.22], [2.42, 3.2, 1.18], "box", "O", 36, ["box", "chacha", "door"], 0.5, 0.8, "মিষ্টির"),'),
  # t7 বেতনে M -> W
  ('st(wtime("বেতনে"), [-0.55, -1.75, 1.3], [-0.4, 1.0, 1.3], "rafi", "M", 24, ["rafi", "dokandar", "counter", "kettle"], 0.5, 0.7, "বেতনে"),',
   'st(wtime("বেতনে"), [-0.55, -2.1, 1.45], [-0.35, 1.1, 1.25], "rafi", "W", 24, ["rafi", "dokandar", "counter", "kettle"], 0.5, 0.7, "বেতনে"),'),
]
for a, b in mix:
    assert a in s, "mix missing: " + a[:80]
    s = s.replace(a, b)
open(p, 'w').write(s)
print("v8 written")
