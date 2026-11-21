#!/usr/bin/env python3
"""Probe: shift a character's position per take and measure head-cut frames.
Tests candidate x-shifts for ma (t5, t8), chacha (t8), rafi (t9 C/W, t11, t4, t10),
dokandar (t2), against the exact framing-gate math."""
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

# station ranges of interest -> (take, station index) is on cam frames; build frame mask per station
station_frames = {}
for i, c in enumerate(cam):
    station_frames.setdefault((c['take'], c['station']), []).append(i)

TARGETS = [('t8', 2), ('t8', 1), ('t5', 0), ('t5', 1), ('t5', 4), ('t8', 3),
           ('t2', 0), ('t11', 2), ('t7', 2), ('t9', 4), ('t9', 3), ('t4', 0), ('t2', 2)]

SHIFTS = {  # who -> candidate [dx, dz] shifts to try
    'ma':      [[0, 0], [-1.2, 0], [-2.0, 0], [0.6, 0], [1.2, 0]],
    'chacha':  [[0, 0], [0.8, 0], [1.5, 0], [-1.5, 0]],
    'rafi':    [[0, 0], [-0.5, 0], [0.5, 0], [-1.0, 0]],
    'dokandar':[[0, 0], [-0.8, 0], [0.5, 0]],
}

def measure(shifts):
    """shifts: dict who -> [dx, dz] applied to every run position; returns cut set per station."""
    res = {}
    for key in TARGETS:
        cut = 0
        for i in station_frames.get(key, []):
            c = cam[i]
            best = None
            for who in perf:
                st = perf_at(perf[who], i)
                if not st['visible'] or st['view'] == 'back':
                    continue
                hc, hw, hh, H = head_box(F, who, st)
                if who in shifts:
                    dx, dz = shifts[who]
                    hc = [hc[0] + dx, hc[1], hc[2] + dz]
                p = project(c, hc)
                if not p:
                    continue
                w = hw / p[2] * (0.5 / math.tan(math.radians(c['fov_v']) / 2)) * PXH / PXW
                h_ = w * PXW / PXH * hh / hw
                if not (-w / 2 < p[0] < 1 + w / 2 and -h_ / 2 < p[1] < 1 + h_ / 2) or w < 0.04:
                    continue
                cutf = p[0] - w / 2 < 0 or p[0] + w / 2 > 1 or p[1] - h_ / 2 < 0 or p[1] + h_ / 2 > 1
                if best is None or w > best[0]:
                    best = (w, cutf)
            if best and best[1]:
                cut += 1
        res[key] = cut
    return res

# current positions of each who during target stations (for reference)
print('current head-cut per target station:')
base = measure({})
for k in TARGETS:
    print('  %s/s%s: %d' % (k[0], k[1], base[k]))

# find who is present per target station
print('\npresent characters per station:')
for k in TARGETS:
    f0 = station_frames[k][len(station_frames[k]) // 2]
    present = []
    for who in perf:
        st = perf_at(perf[who], f0)
        if st['visible'] and st['view'] != 'back':
            hc, hw, hh, H = head_box(F, who, st)
            present.append('%s@[%s] view=%s' % (who, ','.join('%.1f' % v for v in hc), st['view']))
    print('  %s/s%s: %s' % (k[0], k[1], ' | '.join(present)))

# try shifting each who individually (t5/t8 = ma domain; others listed per station)
print('\nshift trials (cut frames per station):')
cands = [('ma', SHIFTS['ma']), ('chacha', SHIFTS['chacha']), ('rafi', SHIFTS['rafi']), ('dokandar', SHIFTS['dokandar'])]
hdr = 'shift            ' + ' '.join('%s/s%-2s' % (a, b) for a, b in TARGETS)
print(hdr)
for who, shifts in cands:
    for s in shifts:
        r = measure({who: s})
        print('%-4s dx=%-5.1f dz=%-4.1f ' % (who, s[0], s[1]) + ' '.join('%5d' % r[k] for k in TARGETS))
