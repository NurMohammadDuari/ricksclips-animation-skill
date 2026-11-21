#!/usr/bin/env python3
"""Probe 2: camera-side fixes (pan aim, truck pos, pull back) per flagged station."""
import sys, math
sys.path.insert(0, '/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1/tools')
import film_plan as fp
from film_plan import PXW, PXH, perf_at, head_box, project

BASE = '/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1'
F = fp.load(BASE + '/episodes/law11-art/film.json')
fps = F['fps']
cam, takes = fp.bake_camera(F)
perf = fp.bake_performance(F)
n = len(cam)

station_frames = {}
for i, c in enumerate(cam):
    station_frames.setdefault((c['take'], c['station']), []).append(i)

TARGETS = [('t8', 2), ('t8', 1), ('t5', 0), ('t5', 1), ('t5', 4), ('t8', 3),
           ('t2', 0), ('t11', 2), ('t7', 2), ('t9', 4), ('t9', 3), ('t4', 0), ('t2', 2),
           ('t5', 3), ('t5', 5), ('t5', 6), ('t8', 0), ('t5', 2), ('t7', 1), ('t11', 1),
           ('t10', 0), ('t10', 2), ('t3', 0), ('t3', 1), ('t6', 0), ('t9', 7)]

def measure_station(key, pan=0.0, truck=0.0, back=0.0):
    cut = 0; total = 0
    for i in station_frames.get(key, []):
        c = cam[i]
        cc = dict(c)
        cc['aim'] = [c['aim'][0] + pan + truck, c['aim'][1], c['aim'][2]]
        cc['pos'] = [c['pos'][0] + truck, c['pos'][1] - back, c['pos'][2]]
        total += 1
        best = None
        for who in perf:
            st = perf_at(perf[who], i)
            if not st['visible'] or st['view'] == 'back':
                continue
            hc, hw, hh, H = head_box(F, who, st)
            p = project(cc, hc)
            if not p:
                continue
            w = hw / p[2] * (0.5 / math.tan(math.radians(cc['fov_v']) / 2)) * PXH / PXW
            h_ = w * PXW / PXH * hh / hw
            if not (-w / 2 < p[0] < 1 + w / 2 and -h_ / 2 < p[1] < 1 + h_ / 2) or w < 0.04:
                continue
            cutf = p[0] - w / 2 < 0 or p[0] + w / 2 > 1 or p[1] - h_ / 2 < 0 or p[1] + h_ / 2 > 1
            if best is None or w > best[0]:
                best = (w, cutf)
        if best and best[1]:
            cut += 1
    return cut, total

print('%-8s %5s %5s | pan: -0.5 -0.3 -0.15 +0.15 +0.3 +0.5 | truck: -0.5 -0.3 +0.3 +0.5 | back: 0.4 0.8' % ('station', 'cut', 'total'))
for k in TARGETS:
    base, tot = measure_station(k)
    pans = [measure_station(k, pan=d)[0] for d in (-0.5, -0.3, -0.15, 0.15, 0.3, 0.5)]
    trks = [measure_station(k, truck=d)[0] for d in (-0.5, -0.3, 0.3, 0.5)]
    backs = [measure_station(k, back=d)[0] for d in (0.4, 0.8)]
    print('%s/s%-3d %5d %5d | ' % (k[0], k[1], base, tot) +
          ' '.join('%4d' % v for v in pans) + ' | ' +
          ' '.join('%4d' % v for v in trks) + ' | ' +
          ' '.join('%3d' % v for v in backs))
