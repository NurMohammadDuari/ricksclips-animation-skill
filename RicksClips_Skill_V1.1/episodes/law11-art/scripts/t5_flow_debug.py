#!/usr/bin/env python3
"""Dump t5 camera speed profile 32-50 s: where does the flowing montage break?"""
import sys
sys.path.insert(0, '/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1/tools')
import film_plan as fp

BASE = '/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1'
F = fp.load(BASE + '/episodes/law11-art/film.json')
fps = F['fps']
cam, takes = fp.bake_camera(F)
sp = fp.screen_speed(cam)
n = len(cam)

f0, f1 = int(31.0 * fps), int(50.5 * fps)
print('frame  t      px/f  state   take/station  framing')
for tk in takes:
    if tk.get('id') != 't5':
        continue
    S = tk['_S']
    marks = {}
    for idx, s in enumerate(S):
        marks[s['_arrive']] = ('arrive', idx, s)
        marks[s['_depart']] = ('depart', idx, s)
    for i in range(f0, min(f1, n)):
        c = cam[i]
        tag = ''
        if i in marks:
            kind, idx, s = marks[i]
            tag = '%s s%d fr=%s word=%s travel=%s hold=%s creep=%s drift=%s' % (
                kind, idx, s.get('framing'), s.get('word'), s.get('travel'), s.get('hold'),
                s.get('creep'), s.get('drift'))
        if tag or i % 10 == 0:
            print('f%4d %6.2f %5.1f  %-6s %s/%s     %s' % (i, i / fps, sp[i], c['state'], c['take'], c['station'], tag))
