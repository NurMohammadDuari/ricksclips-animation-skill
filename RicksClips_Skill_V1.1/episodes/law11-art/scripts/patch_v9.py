#!/usr/bin/env python3
"""Patch v9: aim M/C stations at head height + rafi wage-bag continuity."""
p = '/home/z/my-project/scripts/build_law11_art.py'
s = open(p).read()

# ---- 1. rafi wage-bag continuity (the bag floats from t6 through t11 today)
s = s.replace(
  'act("rafi", 49.2, pos=[0.1, 0.5, 0], view="34", dir=-1, pose="stand", face="sad")',
  'act("rafi", 49.2, pos=[0.1, 0.5, 0], view="34", dir=-1, pose="hold_watch", face="sad")   # the wage bag still in his hand at home')
assert 'pose="hold_watch", face="sad")   # the wage bag still in his hand at home' in s
s = s.replace(
  'act("rafi", 53.3, pos=[-0.35, 1.35, 0], view="34", dir=1, pose="stand", face="tired", say=[111, 130])',
  'act("rafi", 53.3, pos=[-0.35, 1.35, 0], view="34", dir=1, pose="stand", face="tired", prop=None, say=[111, 130])   # the bag left at home')
assert 'the bag left at home' in s

# ---- 2. M/C stations: aim at the subject's head, not the chest (heads were cut by the frame edge)
aim_fix = '''# aim M/C stations at the subject's head height (heads were cut by the frame edge)
HEAD_Z = {"chacha": 1.56, "rafi": 1.58, "ma": 1.47, "nephew": 1.26, "dokandar": 1.60}
for tk in F["takes"]:
    for stn in tk["stations"]:
        if stn.get("framing") in ("M", "C") and stn.get("subject") in HEAD_Z:
            stn["aim"][2] = round(max(stn["aim"][2], HEAD_Z[stn["subject"]] + (0.02 if stn["framing"] == "C" else -0.06)), 2)

for tk in F["takes"]:'''
s = s.replace('''for tk in F["takes"]:
    for stn in tk["stations"]:
        if "travel" in stn and stn["travel"] < 3: stn["travel"] = round(max(0.5, stn["travel"] * 0.6), 2)''', aim_fix + '''
    for stn in tk["stations"]:
        if "travel" in stn and stn["travel"] < 3: stn["travel"] = round(max(0.5, stn["travel"] * 0.6), 2)''')
open(p, 'w').write(s)
print("v9 written")
