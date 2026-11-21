#!/usr/bin/env python3
"""Find which station travel causes the camera speed peak in law11-ai."""
import sys, os, json
sys.path.insert(0, "/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1/tools")
import film_plan as fp

F = json.load(open("/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1/episodes/law11-ai/film.json"))
F = fp.load("/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1/episodes/law11-ai/film.json")
cam, takes = fp.bake_camera(F)
sp = fp.screen_speed(cam)
fps = F["fps"]

# peak overall
pk_i = max(range(len(sp)), key=lambda i: sp[i])
print(f"PEAK: frame {pk_i}  t={pk_i/fps:.2f}s  speed={sp[pk_i]:.1f} px/f")

# top 12 peaks
order = sorted(range(len(sp)), key=lambda i: -sp[i])[:12]
for i in order:
    print(f"  f{i:5d} t={i/fps:6.2f}s speed={sp[i]:6.1f} cut={cam[i].get('cut')} take={cam[i].get('take')}")

# station times per take
print("\n--- stations near peaks ---")
for tk in takes:
    sid = tk["id"]
    sts = tk["stations"]
    for k, s in enumerate(sts):
        at = s["at"] if isinstance(s["at"], (int, float)) else s["at"].get("s", 0)
        tsec = at if isinstance(at, (int, float)) else at
        tframe = tsec * fps if tsec < 10000 else tsec
        print(f"{sid} st{k:02d} at={tframe:.0f}f ({tframe/fps:.2f}s) travel={s.get('travel','-')} hold={s.get('hold','-')} subj={s.get('subject')} framing={s.get('framing')} lens={s.get('lens')}")
