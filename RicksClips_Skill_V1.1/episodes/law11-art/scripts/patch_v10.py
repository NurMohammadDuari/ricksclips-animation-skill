#!/usr/bin/env python3
"""Patch v10: tight scene blocking + noun fix + hold trim (match-verified)."""
p = '/home/z/my-project/scripts/build_law11_art.py'
s = open(p).read()

# ---- 1. noun fix: ভাগ্নে@2.39 (L1) needs nephew visible in t1 st1
a = 'st(wtime("রাফি", 1), [0.1, -1.9, 1.3], [0.15, 0.4, 1.3], "rafi", "M", 24, ["rafi", "chacha", "counter", "jars"], 0.5, 0.7, "রাফি"),'
b = 'st(wtime("রাফি", 1), [0.1, -1.9, 1.3], [0.15, 0.4, 1.3], "rafi", "M", 24, ["rafi", "chacha", "nephew", "counter", "jars"], 0.5, 0.7, "রাফি"),'
assert a in s; s = s.replace(a, b)

# ---- 2. scene blocking
blocks = [
  ('act("chacha", 0, pos=[0.5, 2.2, 0]', 'act("chacha", 0, pos=[0.55, 2.15, 0]'),
  ('act("nephew", 0, pos=[1.6, 2.3, 0], view="34", dir=-1, pose="stand", face="smug")',
   'act("nephew", 0, pos=[1.35, 2.35, 0], view="34", dir=-1, pose="stand", face="smug")'),
  ('act("ma", 9.6, pos=[-1.3, 0.5, 0], view="front", dir=1, pose="stand", face="worried")',
   'act("ma", 9.6, pos=[-0.35, 0.85, 0], view="front", dir=1, pose="stand", face="worried")'),
  ('act("ma", 16.7, pos=[-1.3, 0.5, 0], view="34", dir=1, pose="stand", face="worried")',
   'act("ma", 16.7, pos=[-0.75, 0.85, 0], view="34", dir=1, pose="stand", face="worried")'),
  ('act("rafi", 16.7, pos=[0.1, 0.5, 0], view="34", dir=1, pose="stand", face="surprised")',
   'act("rafi", 16.7, pos=[0.15, 0.55, 0], view="34", dir=1, pose="stand", face="surprised")'),
  ('act("chacha", 22.4, pos=[1.05, 0.7, 0], view="34", dir=1, pose="hold_watch", face="smug", say=[46, 56])',
   'act("chacha", 22.4, pos=[0.95, 1.35, 0], view="34", dir=1, pose="hold_watch", face="smug", say=[46, 56])'),
  ('act("nephew", 23.4, pos=[1.5, 0.45, 0], view="34", dir=1, pose="stand", face="smug")',
   'act("nephew", 23.4, pos=[1.45, 1.65, 0], view="34", dir=1, pose="stand", face="smug")'),
  ('act("chacha", 25.65, pos=[1.5, 0.6, 0], view="34", dir=1, pose="stand", face="smug")',
   'act("chacha", 25.65, pos=[0.95, 1.35, 0], view="34", dir=1, pose="stand", face="smug")'),
  ('act("nephew", 25.65, pos=[2.0, 1.6, 0], view="34", dir=-1, pose="stand", face="annoyed")',
   'act("nephew", 25.65, pos=[1.45, 1.65, 0], view="34", dir=-1, pose="stand", face="annoyed")'),
  ('act("chacha", 32.2, pos=[0.6, 2.3, 0], view="34", dir=-1, pose="hands_hips", face="smug")',
   'act("chacha", 32.2, pos=[0.7, 2.35, 0], view="34", dir=-1, pose="hands_hips", face="smug")'),
  ('act("nephew", 32.2, pos=[-0.25, 1.15, 0], view="34", dir=1, pose="stand", face="confused")',
   'act("nephew", 32.2, pos=[-0.35, 1.15, 0], view="34", dir=1, pose="stand", face="confused")'),
  ('act("rafi", 86.0, pos=[0.55, 0.5, 0], view="34", dir=-1, pose="stand", face="cool", say=[165, 176])',
   'act("rafi", 86.0, pos=[1.35, 1.05, 0], view="34", dir=-1, pose="stand", face="cool", say=[165, 176])'),
  ('act("dokandar", 53.3, pos=[0.6, 2.0, 0], view="34", dir=-1, pose="stand", face="sweetSmile")',
   'act("dokandar", 53.3, pos=[0.55, 1.95, 0], view="34", dir=-1, pose="stand", face="sweetSmile")'),
  ('act("dokandar", 92.0, pos=[0.6, 1.7, 0], view="34", dir=-1, pose="stand", face="happy")',
   'act("dokandar", 92.0, pos=[0.55, 1.75, 0], view="34", dir=-1, pose="stand", face="happy")'),
  ('act("dokandar", 98.5, pos=[0.6, 1.8, 0], view="34", dir=-1, pose="stand", face="happy", prop=None)',
   'act("dokandar", 98.5, pos=[0.55, 1.75, 0], view="34", dir=-1, pose="stand", face="happy", prop=None)'),
]
for a, b in blocks:
    assert a in s, "block missing: " + a[:70]
    s = s.replace(a, b)

# ---- 3. t9 stations re-aim at the clustered doorway confrontation
s = s.replace(
  'st(wtime("চাচা", 5), [0.8, -2.15, 1.45], [1.0, 1.3, 1.25], "rafi", "W", 24, ["rafi", "chacha", "door"], 0.5, 0.6, "চাচা"),',
  'st(wtime("চাচা", 5), [1.15, -2.0, 1.4], [1.55, 1.7, 1.25], "rafi", "W", 24, ["rafi", "chacha", "door"], 0.5, 0.6, "চাচা"),')
s = s.replace(
  'st(wtime("ভরসাটা"), [0.8, -1.85, 1.35], [1.35, 1.5, 1.35], "rafi", "M", 24, ["rafi", "chacha", "door"], 0.5, 0.7, "ভরসাটা"),',
  'st(wtime("ভরসাটা"), [1.35, -1.55, 1.3], [1.65, 1.75, 1.35], "rafi", "M", 24, ["rafi", "chacha", "door"], 0.5, 0.7, "ভরসাটা"),')
s = s.replace(
  'st(wtime("শিখানো"), [0.35, -2.1, 1.25], [1.7, 2.8, 1.35], "chacha", "W", 24, ["chacha", "rafi", "door"], 0.55, 0.8),',
  'st(wtime("শিখানো"), [1.05, -2.15, 1.3], [1.85, 2.6, 1.3], "chacha", "W", 24, ["chacha", "rafi", "door"], 0.55, 0.8),')

# ---- 4. t11 khata O insert: keep rafi's head out of the insert frame
s = s.replace(
  'st(wtime("নিয়ম"), [-1.05, -1.4, 1.25], [-0.65, 1.0, 1.15], "khata", "O", 40, ["khata", "rafi"], 0.5, 0.6, "নিয়ম"),',
  'st(wtime("নিয়ম"), [-1.5, -1.05, 1.2], [-0.95, 1.35, 1.08], "khata", "O", 40, ["khata", "rafi"], 0.5, 0.6, "নিয়ম"),')

# ---- 5. holds 0.5 -> 0.45 on non-word stations
s = s.replace(
  'if word is not None: s["word"] = word; s["lead"] = 12; s["hold"] = 0.6',
  'if word is not None: s["word"] = word; s["lead"] = 12; s["hold"] = 0.6\n    elif s.get("hold") == 0.5: s["hold"] = 0.45')
open(p, 'w').write(s)
print("v10 written")
