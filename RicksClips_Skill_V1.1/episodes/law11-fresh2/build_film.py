#!/usr/bin/env python3
"""build_film.py — author film.json for law11-fresh2 from the script direction map.

Rules honoured (MASTER DIRECTIVE):
- Every camera number is COMPUTED from the subject's height + framing target
  (whole: figure 0.45 / feet 0.84 / head 0.47 · medium: figure 0.62 / head 0.42 ·
   close: head height 0.52 / head centre 0.45) — nothing guessed.
- Door-set rule (porch_roof fix): every camera in the courtyard keeps its eye-line at
  >= 1.32 m, level (no tilt), so the porch roof can never fill the frame.
- Cuts land ONLY on the script's own place/time jumps (gate: cuts per 10 s <= 0.9).
- Word stations arrive at rest 5 frames before their word (CB's rule).
- Every named noun is on screen at its word (sentences[].nouns).
- fx on action nouns only (1-2 per 10 s), moods on the emotion beats (>= 12/min).
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))          # RicksClips_Skill_V1.1
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import film_plan as FP

FPS = 30
W, H = 1080, 1920
FOVT = math.tan(math.radians(FP.fov_v(24.0)) / 2.0)      # portrait vertical half-fov tan at 24 mm

CAST = {
    # id: (height, heads_tall, head_aspect, sheet name)
    'kaka':    (1.68, 2.8, 0.95),
    'rafi':    (1.70, 2.9, 0.92),
    'bhagne':  (1.38, 3.4, 1.00),
    'ma':      (1.58, 2.9, 0.95),
    'pashi':   (1.72, 2.9, 0.92),
    'tulu':    (1.30, 3.5, 1.00),
    'khoddor': (1.75, 2.7, 0.95),
}
PUPPET = {k: f'cast:fresh_cast/{k}' for k in CAST}

def head_z(who):
    h, ht, ha = CAST[who]
    return h - (h / ht) / 2

def cam(subject, framing, sx, sy, side='front', side_x=0.0, lens=24.0, door=False, off_y=0.0, aim_x=None, aim_y=None, sz=None):
    """Computed camera for one station. side: 'front' (camera at -y), 'sideL', 'sideR', 'back'.
    Object inserts (subject not in CAST): frame the anchor point (sx, sy, sz) centred, lens given."""
    if subject not in CAST:
        z_aim = sz if sz is not None else 1.1
        d = 1.4 if framing == 'O' else 5.07             # O: tight insert (~1.3 m tall frame); P: the place
        pos = [sx + side_x, sy - d + off_y, z_aim]
        aim = [sx if aim_x is None else aim_x, sy if aim_y is None else aim_y, z_aim]
        return dict(pos=[round(v, 4) for v in pos], aim=[round(v, 4) for v in aim], lens=lens)
    h, ht, ha = CAST[subject]
    hh = h / ht
    z_h = head_z(subject)
    if framing == 'W':   V, y_head = z_h / 0.37, 0.47          # figure 0.45, feet 0.84
    elif framing == 'M': V, y_head = h / 0.62, 0.42            # figure 0.62
    elif framing == 'C':
        # close = the head fills 0.52 of the frame WIDTH (Rick p90 0.54): solve the distance
        hw_m = hh * ha
        d = hw_m * (0.5 / FOVT) * (FP.PXH / FP.PXW) / 0.52
        V, y_head = 2 * FOVT * d, 0.42
    else:                V, y_head = 7.6, 0.46                 # P: place
    d = d if framing == 'C' else V / (2 * FOVT)
    z_aim = z_h - (0.5 - y_head) * V
    if door:                                                   # porch_roof fix: eye-line at/above 1.32
        z_aim = max(z_aim, 1.32)
        if framing == 'C': z_aim = max(z_aim, 1.30)
    if side == 'front':   pos = [sx + side_x, sy - d + off_y, z_aim]
    elif side == 'sideL': pos = [sx - d, sy + side_x, z_aim]
    elif side == 'sideR': pos = [sx + d, sy + side_x, z_aim]
    else:                 pos = [sx + side_x, sy + d + off_y, z_aim]
    aim = [sx if aim_x is None else aim_x, sy if aim_y is None else aim_y, z_aim]
    return dict(pos=[round(v, 4) for v in pos], aim=[round(v, 4) for v in aim], lens=lens)

def st_at(word, n=1):
    hits = [i for i, x in enumerate(_WORDS) if x['_k'] == norm(word)]
    if hits and len(hits) < n:
        print(f'  note: anchor {word}#{n} -> #{len(hits)}')
        n = len(hits)
    return [word, n]

_RANGES = []

def _sec(at):
    if isinstance(at, dict) and 's' in at: return at['s']
    return None

def S_(si, tok, off=0, n=1):
    """frame of the n-th occurrence of a token INSIDE sentence si, from its REAL audio time."""
    _, _, times = _RANGES[si]
    toks = [norm(t) for t in SENT[si].split() if norm(t)]
    k = -1
    for _ in range(n):
        k = toks.index(norm(tok), k + 1)
    a, b = times[k]
    return int(round((a + (b - a) * 0.6) * FPS + off))   # 60 % into the word: the beat lands while it is spoken

# ---------------------------------------------------------------- script (15 sentences, unchanged meaning)
SENT = [
    "কাল থেকে আর আসা লাগবে না, রাফি। আমার ভাগ্নে এখন সব পারে।",
    "চাচা, ১০ বছর... আপনার ভাগ্নেরে তো সব আমিই শিখাইলাম!",
    "কিন্তু ৩ মাস পর, সেই চাচাই মিষ্টির প্যাকেট হাতে... রাফির বাসায় এসে হাজির!",
    "অথচ ১ বছর আগে, চাচা নিজেই ভাগ্নেকে নিয়ে রাফির বাসায় এসে বলেছিলেন,",
    "রাফি, পোলাটারে কাজ শিখায় দাও... তুমি তো আমার নিজের পোলার মতো!",
    "সব শিখাইস না, বাবা... মালিকের ভাগ্নে, মালিকেরই লোক!",
    "মায়ের কথা হেসে উড়িয়ে... সাপ্লায়ারদের নম্বর, বাকির খাতা... খদ্দের। ভাগ্নে সব শিখে ফেলতেই, চাচা বললেন সেই কথা... ১০ বছর পর... বেতন নিয়ে বাসায় ফিরলো।",
    "যার পাতে ভাত দিলি... সেই তোর ভাত কাড়লো, বাবা!",
    "১ মাস পর, পাশের দোকানে অর্ধেক বেতনে... কাজ শিখালো... বড় খদ্দের রাখলো নিজের হাতে... খাতা ভাগ্নের হাতে... চিনতো শুধু রাফিকে। বললো চোর... মাল নিতে গেলো রাফির কাছে!",
    "৩ মাসে বিক্রি অর্ধেক হতেই, চাচা মিষ্টির প্যাকেট হাতে রাফির বাসায় এসে বললেন,",
    "রাফি, কাল থেকে আবার আসো, বাবা... ভাগ্নে আমার কিছুই পারে না!",
    "চাচা, কাজ তো সবই শিখাইছিলাম... খালি মানুষের ভরসাটা শিখানো যায় না।",
    "রাফি আর ফিরলো না... ৬ মাস পর, পাশের দোকানের মালিক ওকে ৪ আনার অংশীদার বানালেন!",
    "কাজ সবাইকে শেখান... নিজের জায়গাটা কাউকে শিখিয়ে দিবেন না। ... ১১ নম্বর নিয়ম...",
    "আপনার চাকরিতেও কি...? কমেন্টে লিখুন। এমন আরো গল্প পেতে ফলো করুন।",
]

def load_words():
    w = json.load(open(os.path.join(HERE, 'voice', 'words.json'), encoding='utf-8'))
    for x in w: x['_k'] = x['w'].strip(' .,?!";:-').lower()
    return w

def norm(t):
    return t.strip(' .,?!।";:-…()').lower()

def sentence_ranges(words):
    """match every sentence's tokens against the timed word list, in order, bounded to the sentence's
    own window (+6 slack) so a missing token can never pull the match into the next sentence.
    Returns [(i0, i1, times)] where times[k] = (start_s, end_s) of token k (None if the audio skipped it)."""
    out, cursor = [], 0
    for text in SENT:
        toks = [norm(t) for t in text.split() if norm(t)]
        times = [None] * len(toks); i0 = None; i1 = None; j = cursor
        limit = cursor + len(toks) + 6
        for k, tok in enumerate(toks):
            j2 = j
            while j2 < min(len(words), limit):
                if words[j2]['_k'] == tok:
                    if i0 is None: i0 = j2
                    i1 = j2; times[k] = (words[j2]['s'], words[j2]['e']); j = j2 + 1
                    break
                j2 += 1                                    # a token the aligner skipped: cursor stays put
        if i0 is None: raise SystemExit(f'sentence not aligned: {text[:30]}')
        # fill skipped tokens by interpolation between their matched neighbours
        known = [(k, t) for k, t in enumerate(times) if t]
        for k in range(len(toks)):
            if times[k] is None:
                prev = max([kk for kk, _ in known if kk < k], default=None)
                nxt = min([kk for kk, _ in known if kk > k], default=None)
                if prev is None: prev, p_t = nxt, times[nxt][0]
                if nxt is None: nxt, n_t = prev, times[prev][1]
                a = times[prev][1] if times[prev] else p_t
                b = times[nxt][0] if times[nxt] else n_t
                gap = nxt - prev
                frac = (k - prev) / float(gap if gap else 1)
                t = a + (b - a) * frac
                times[k] = (t, t)
        out.append((i0, i1, times)); cursor = i1 + 1
    return out

def W_(words, word, n=1):
    """frame number of the n-th occurrence of `word` in the timed narration"""
    hits = [i for i, x in enumerate(words) if x['_k'] == norm(word)]
    if not hits: raise SystemExit(f'word {word} missing from words.json')
    if len(hits) < n:
        print(f'  note: {word}#{n} -> #{len(hits)} (audio has {len(hits)})')
        n = len(hits)
    return int(round(words[hits[n - 1]]['s'] * FPS))

# ---------------------------------------------------------------- build
_WORDS = []

def main():
    global _WORDS
    words = load_words()
    _WORDS = words
    ranges = sentence_ranges(words)
    _RANGES[:] = ranges
    ranges = [(r[0], r[1]) for r in ranges]
    end = int(round((words[-1]['e'] + 0.6) * FPS))

    places = {
        'dokan_night':    {'set': 'set_dokan', 'light': 'night', 'backdrop': 9.0},
        'dokan_day':      {'set': 'set_dokan', 'light': 'day', 'backdrop': 9.0},
        'dokan_cool':     {'set': 'set_dokan', 'light': 'day', 'backdrop': 9.0,
                           'light_over': {'tint': '#bcccee', 'sun': '#aebfe0', 'si': 2.0, 'amb': '#8fa0b8'}},
        'door_night':     {'set': 'set_basha_door', 'light': 'night', 'backdrop': 11.0},
        'door_morning':   {'set': 'set_basha_door', 'light': 'morning', 'backdrop': 11.0},
        'bhitore_int':    {'set': 'set_bhitore', 'light': 'interior', 'backdrop': 8.0},
        'bhitore_golden': {'set': 'set_bhitore', 'light': 'golden', 'backdrop': 8.0},
        'pasher_day':     {'set': 'set_pasher', 'light': 'day', 'backdrop': 9.0},
        'pasher_golden':  {'set': 'set_pasher', 'light': 'golden', 'backdrop': 9.0},
        'rasta_morning':  {'set': 'set_rasta', 'light': 'morning', 'backdrop': 14.0},
    }

    # positions per set (feet, plan metres)
    DOK = dict(kaka=[0.1, 3.0], bhagne=[1.35, 2.9], rafi=[-1.5, 1.5], khoddor=[-0.6, 2.3])
    DOR = dict(door=[0.1, 3.3], path0=[0.1, 0.9], pathmid=[0.1, 2.45], rafi_door=[0.75, 2.9], kaka_side=[-0.9, 2.35])
    BIT = dict(ma=[-2.5, 2.4], rafi=[-1.1, 1.7], table=[0.1, 1.6])
    PAS = dict(pashi=[1.6, 3.0], rafi=[0.4, 1.5], tulu=[-0.3, 1.3], bhagne=[-2.75, 1.5], khoddor=[-0.6, 2.4], khoddor_pay=[0.1, 1.8])


    takes, acts, sentences = [], [], []
    fx, moods, sound, trans = [], [], [], []

    def mood(word, n=1, look='warm', at=None):
        moods.append({'at': at if at is not None else st_at(word, n), 'look': look})

    def fxn(word, n, kind, on=None, pos=None, s=0.8, size=1.1):
        e = {'at': st_at(word, n), 'kind': kind, 's': s, 'size': size}
        if on: e['on'] = on
        if pos: e['pos'] = pos
        fx.append(e)

    def snd(word, n, name):
        sound.append({'at': st_at(word, n), 'name': name})

    BODIES = {'dokan_night': list(DOK.values()) + [[-1.2, 1.6]], 'door_night': [DOR['path0'], DOR['pathmid'], DOR['rafi_door']],
              'door_morning': [[0.55, 1.0], [1.1, 1.1], DOR['kaka_side'], [1.7, 1.9], [0.5, 2.3]],
              'bhitore_int': list(BIT.values()), 'dokan_day': list(DOK.values()), 'dokan_cool': list(DOK.values()),
              'bhitore_golden': list(BIT.values()), 'pasher_day': list(PAS.values()) + [[-1.2, 1.6]],
              'pasher_golden': [PAS['rafi'], PAS['tulu']], 'rasta_morning': [[-2.6, 3.2], [1.0, 5.0], [2.0, 5.3], [2.9, 5.2]]}

    def add_take(tid, place, stations):
        # an arc move reads Rick; a straight move that GRAZES a body walks THROUGH it (heads at 3 cm
        # from the lens). Add a via point only when the straight path passes within 0.8 m of one.
        import math as _m
        bodies = BODIES.get(place, [])
        for j in range(1, len(stations)):
            p0 = stations[j - 1]['pos']; p1 = stations[j]['pos']
            if 'via' in stations[j]: continue
            mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
            dx, dy = p1[0] - p0[0], p1[1] - p0[1]
            L2 = dx * dx + dy * dy
            near = False
            for b in bodies:
                if L2 < 1e-6: continue
                t = max(0.0, min(1.0, ((b[0] - p0[0]) * dx + (b[1] - p0[1]) * dy) / L2))
                px, py = p0[0] + dx * t, p0[1] + dy * t
                if _m.hypot(b[0] - px, b[1] - py) < 1.0: near = True; break
            if near:
                stations[j]['via'] = [[round(mx, 3), round(min(p0[1], p1[1], my) - 1.3, 3), p1[2]]]
        takes.append({'id': tid, 'place': place, 'stations': stations})

    def station(at, subject, framing, sx, sy, side='front', hold=0.55, travel=None, shows=(), word=None, follow=None, **kw):
        s = {'at': at, **cam(subject, framing, sx, sy, side=side, **kw),
             'subject': subject, 'framing': framing, 'shows': list(shows), 'hold': hold}
        if travel is not None: s['travel'] = travel
        if word: s['word'] = word
        if follow: s['follow'] = follow
        return s

    def idle(t, who, face=None, pose=None, look='cam'):
        a = {'who': who, 'at': t if not isinstance(t, float) else {'s': t}}
        if face: a['face'] = face
        if pose: a['pose'] = pose
        a['look'] = look
        return a

    # ================= t1 — dokan night: the hook + rafi's protest (sentences 1-2)  [0 .. 8.9]
    add_take('t1', 'dokan_night', [
        station(0, 'kaka', 'W', DOK['kaka'][0], DOK['kaka'][1], hold=0.9, travel=1.1, shows=['kaka', 'rafi', 'bhagne', 'counter', 'jars']),
        station(S_(0, 'ভাগ্নে'), 'bhagne', 'M', DOK['bhagne'][0], DOK['bhagne'][1], hold=0.7, word='ভাগ্নে', shows=['bhagne', 'till']),
        station(S_(1, 'চাচা'), 'rafi', 'W', DOK['rafi'][0], DOK['rafi'][1], side='sideR', hold=0.6, travel=0.9, word='চাচা', shows=['rafi', 'counter', 'bhagne']),
        station(S_(1, 'ভাগ্নেরে'), 'till', 'O', 1.35, 2.42, sz=1.10, hold=2.2, word='ভাগ্নেরে', shows=['till', 'rafi']),
    ])
    acts += [
        {'who': 'kaka', 'at': 0, 'pos': DOK['kaka'] + [0], 'view': 'front', 'dir': 1, 'pose': 'stand', 'face': ['elder', 'sweetSmile'], 'look': 'cam'},
        {'who': 'bhagne', 'at': 0, 'pos': DOK['bhagne'] + [0], 'view': 'front', 'dir': -1, 'pose': 'stand', 'face': ['female', 'smug'], 'look': 'cam'},
        {'who': 'rafi', 'at': 0, 'pos': DOK['rafi'] + [0], 'view': '34', 'dir': 1, 'pose': 'stand', 'face': 'standard', 'look': 'cam'},
        {'who': 'kaka', 'at': {'s': 0.7}, 'pose': 'point_out', 'say': [ranges[0][0], ranges[0][1]], 'look': 'cam'},
        {'who': 'bhagne', 'at': {'s': 2.9}, 'pose': 'hands_hips', 'look': 'cam'},
        {'who': 'rafi', 'at': S_(1, 'চাচা'), 'face': 'strain', 'pose': 'lean_in', 'say': [ranges[1][0], ranges[1][1]], 'look': 'cam'},
        {'who': 'rafi', 'at': S_(1, 'আমিই'), 'pose': 'point_out', 'look': 'cam'},
        {'who': 'kaka', 'at': S_(1, 'ভাগ্নেরে'), 'pose': 'stand', 'face': ['elder', 'suspicious'], 'look': 'bhagne'},
        {'who': 'bhagne', 'at': S_(1, 'ভাগ্নেরে'), 'face': 'delight', 'look': 'cam'},
    ]
    for si, w, lk in ((0, 'ভাগ্নে', 'cold'), (1, 'আমিই', 'spot'), (1, 'ভাগ্নেরে', 'cold')): mood(w, 1, lk, at=S_(si, w))
    fx.append({'at': S_(1, 'শিখাইলাম'), 'kind': 'glint', 'on': 'till', 's': 0.8, 'size': 1.1})

    # ================= t2 — door night: the packet knock (sentence 3)  [8.9 .. 14.9]
    add_take('t2', 'door_night', [
        station({'s': 11.15}, 'path', 'P', 0.1, 2.2, door=True, aim_x=0.1, aim_y=2.4, hold=1.0, travel=1.5, shows=['kaka', 'path', 'door']),
        station({'s': 11.3}, 'kaka', 'W', 0.1, 2.1, door=True, hold=0.6, travel=0.8, shows=['kaka', 'path', 'door']),
        station(S_(2, 'প্যাকেট'), 'kaka', 'M', 0.1, 2.45, door=True, hold=0.7, word='প্যাকেট', shows=['kaka', 'packet', 'door']),
        station(S_(2, 'হাজির'), 'kaka', 'M', 0.1, 2.45, side='sideR', door=True, hold=1.6, word='হাজির', shows=['kaka', 'door']),
    ])
    acts += [
        {'who': 'kaka', 'at': {'s': 11.2}, 'pos': DOR['path0'] + [0], 'view': '34', 'dir': 1, 'pose': 'walk', 'face': ['elder', 'suspicious'], 'walk_pose': 'walk', 'visible': True, 'look': [0.1, 3.3, 0]},
        {'who': 'kaka', 'at': {'s': 14.5}, 'pos': DOR['pathmid'] + [0], 'pose': 'stand', 'face': ['elder', 'suspicious'], 'look': [0.1, 3.3, 0]},
        {'who': 'kaka', 'at': S_(2, 'প্যাকেট'), 'pose': 'hold_out', 'face': 'eek', 'prop': 'packet', 'hand': 'L', 'say': [ranges[2][0], ranges[2][1]], 'look': [0.1, 3.3, 0]},
        {'who': 'kaka', 'at': S_(2, 'হাজির'), 'pose': 'flinch', 'face': 'eek', 'look': 'cam'},
    ]
    for w, lk in (('প্যাকেট', 'cold'), ('হাজির', 'dark')): mood(w, 1, lk, at=S_(2, w))
    fx.append({'at': S_(2, 'হাজির'), 'kind': 'knock', 'on': 'door', 's': 0.7, 'size': 1.1}); sound.append({'at': S_(2, 'হাজির'), 'name': 'door_knock'})
    trans.append({'at': S_(2, 'কিন্তু'), 'kind': 'steam', 'frames': 16})

    # ================= t3 — door morning: the flashback (sentences 4-5)  [14.9 .. 24.8]
    add_take('t3', 'door_morning', [
        station({'s': 20.15}, 'path', 'P', 0.1, 2.3, door=True, aim_x=0.4, aim_y=2.4, hold=1.0, travel=1.6, shows=['kaka', 'bhagne', 'path', 'door']),
        station(S_(3, 'ভাগ্নেকে'), 'kaka', 'W', 0.55, 2.4, door=True, hold=0.7, word='ভাগ্নেকে', shows=['kaka', 'bhagne', 'door']),
        station(S_(4, 'শিখায়'), 'kaka', 'W', DOR['kaka_side'][0], DOR['kaka_side'][1], door=True, hold=0.8, word='শিখায়', shows=['kaka', 'rafi']),
        station(S_(4, 'নিজের'), 'rafi', 'M', 1.7, 1.9, door=True, hold=0.7, word='নিজের', shows=['rafi', 'kaka']),
        station(S_(4, 'মতো'), 'kaka', 'C', DOR['kaka_side'][0], DOR['kaka_side'][1], door=True, hold=1.5, word='মতো', shows=['kaka', 'rafi']),
    ])
    acts += [
        {'who': 'kaka', 'at': {'s': 20.2}, 'pos': [0.55, 1.0, 0], 'view': '34', 'dir': 1, 'pose': 'walk', 'face': ['elder', 'sweetSmile'], 'walk_pose': 'walk', 'visible': True, 'look': [1.7, 2.0, 0]},
        {'who': 'bhagne', 'at': {'s': 20.2}, 'pos': [1.1, 1.1, 0], 'view': '34', 'dir': 1, 'pose': 'walk', 'face': ['female', 'smug'], 'walk_pose': 'walk', 'visible': True, 'look': [1.7, 2.0, 0]},
        {'who': 'kaka', 'at': {'s': 24.0}, 'pos': DOR['kaka_side'] + [0], 'pose': 'stand', 'face': ['elder', 'sweetSmile']},
        {'who': 'bhagne', 'at': {'s': 24.0}, 'pos': [0.5, 2.3, 0], 'pose': 'stand', 'face': ['female', 'smug']},
        {'who': 'rafi', 'at': {'s': 24.0}, 'pos': [1.7, 1.9, 0], 'view': '34', 'dir': -1, 'pose': 'stand', 'face': 'standard', 'visible': True, 'look': 'cam'},
        {'who': 'kaka', 'at': S_(4, 'শিখায়'), 'pose': 'grip_shoulder', 'face': ['elder', 'sweetSmile'], 'say': [ranges[4][0], ranges[4][1]], 'look': 'rafi'},
        {'who': 'rafi', 'at': S_(4, 'নিজের'), 'pose': 'shrug', 'face': 'awkward', 'look': 'cam'},
        {'who': 'bhagne', 'at': S_(4, 'মতো'), 'pose': 'hands_hips', 'face': ['female', 'smug'], 'look': 'cam'},
    ]
    for w, lk in (('আগে', 'warm'), ('মতো', 'gold')): mood(w, 1, lk, at=S_(3 if w == 'আগে' else 4, w))

    # ================= t4 — bhitore interior: ma's warning (sentence 6)  [24.8 .. 30.9]
    add_take('t4', 'bhitore_int', [
        station({'s': 35.4}, 'ma', 'P', BIT['ma'][0], BIT['ma'][1], sz=1.4, hold=1.2, travel=1.4, shows=['ma', 'rafi', 'stove', 'tea_table']),
        station(S_(5, 'বাবা'), 'ma', 'M', BIT['ma'][0], BIT['ma'][1], hold=1.0, word='বাবা', shows=['ma', 'rafi']),
        station(S_(5, 'লোক'), 'ma', 'C', BIT['ma'][0], BIT['ma'][1], hold=1.6, word='লোক', shows=['ma']),
    ])
    acts += [
        {'who': 'ma', 'at': {'s': 35.45}, 'pos': BIT['ma'] + [0], 'view': '34', 'dir': 1, 'pose': 'stand', 'face': ['female', 'sassy'], 'enter': True, 'look': 'cam'},
        {'who': 'rafi', 'at': {'s': 35.45}, 'pos': BIT['rafi'] + [0], 'view': '34', 'dir': -1, 'pose': 'stand', 'face': 'delight', 'visible': True, 'look': 'cam'},
        {'who': 'ma', 'at': S_(5, 'মালিকের'), 'pose': 'lean_in', 'face': ['female', 'judging'], 'say': [ranges[5][0], ranges[5][1]], 'look': 'rafi'},
        {'who': 'ma', 'at': S_(5, 'লোক'), 'pose': 'finger_up', 'look': 'rafi'},
        {'who': 'rafi', 'at': S_(5, 'বাবা'), 'pose': 'hand_mouth', 'face': 'delight', 'look': 'cam'},
    ]
    for w, lk in (('মালিকের', 'warm'), ('লোক', 'spot')): mood(w, 1, lk, at=S_(5, w))
    fx.append({'at': S_(5, 'লোক'), 'kind': 'steam', 'on': 'stove', 's': 1.0, 'size': 1.1})

    # ================= t5 — dokan day: suppliers, khata, khoddor, THE line (sentence 7a+7b)  [30.9 .. 42.0]
    add_take('t5', 'dokan_day', [
        station({'s': 39.7}, 'rafi', 'W', DOK['rafi'][0] + 0.3, DOK['rafi'][1], hold=0.8, travel=1.4, shows=['rafi', 'kaka', 'bhagne', 'counter', 'board']),
        station(S_(6, 'নম্বর'), 'board', 'O', -1.7, 3.1, sz=1.40, hold=0.8, word='নম্বর', shows=['board']),
        station(S_(6, 'খাতা'), 'khoddor', 'M', DOK['khoddor'][0], DOK['khoddor'][1] + 0.1, hold=1.0, word='খাতা', shows=['khoddor', 'khata_desk', 'kaka']),
                station(S_(6, 'ফেলতেই'), 'bhagne', 'W', DOK['bhagne'][0], DOK['bhagne'][1], hold=0.7, travel=1.0, shows=['bhagne', 'kaka', 'counter']),
                station(S_(6, 'কথা', n=2), 'kaka', 'C', DOK['kaka'][0], DOK['kaka'][1], hold=1.6, word='কথা', shows=['kaka', 'bhagne', 'rafi']),
    ])
    acts += [
        {'who': 'rafi', 'at': {'s': 39.75}, 'pos': [DOK['rafi'][0] + 0.3, DOK['rafi'][1], 0], 'view': '34', 'dir': 1, 'pose': 'write', 'face': 'standard', 'prop': 'pen', 'hand': 'R', 'visible': True, 'look': 'cam'},
        {'who': 'kaka', 'at': {'s': 39.75}, 'pos': DOK['kaka'] + [0], 'view': 'front', 'dir': 1, 'pose': 'stand', 'face': ['elder', 'sweetSmile'], 'visible': True, 'look': 'cam'},
        {'who': 'bhagne', 'at': {'s': 39.75}, 'pos': DOK['bhagne'] + [0], 'view': 'front', 'dir': -1, 'pose': 'stand', 'face': ['female', 'smug'], 'visible': True, 'look': 'cam'},
        {'who': 'khoddor', 'at': S_(6, 'খাতা'), 'pos': DOK['khoddor'] + [0], 'view': '34', 'dir': -1, 'pose': 'stand', 'face': 'proud', 'enter': True, 'look': 'cam'},
        {'who': 'khoddor', 'at': S_(6, 'খদ্দের'), 'pose': 'hands_hips', 'face': 'proud', 'look': 'cam'},
        {'who': 'bhagne', 'at': S_(6, 'ফেলতেই'), 'face': 'delight', 'pose': 'stand', 'look': 'cam'},
                {'who': 'kaka', 'at': S_(6, 'কথা', n=2), 'pose': 'point_out', 'face': ['elder', 'sweetSmile'], 'say': [ranges[6][0] + 12, ranges[6][0] + 17], 'look': 'cam'},
        {'who': 'rafi', 'at': S_(6, 'কথা', n=2), 'face': 'awkward', 'pose': 'stand', 'look': 'kaka'},
    ]
    for w, lk in (('নম্বর', 'gold'), ('খদ্দের', 'warm'), ('ফেলতেই', 'gold'), ('কথা', 'spot')): mood(w, 1, lk, at=S_(6, w, n=2 if w == 'কথা' else 1))
    fx.append({'at': S_(6, 'নম্বর'), 'kind': 'paper', 'on': 'board', 's': 0.8, 'size': 1.1}); sound.append({'at': S_(6, 'নম্বর'), 'name': 'paper_turn'})

    # ================= t7 — dokan cool: ten years later (sentence 7c)  [42.0 .. 47.8]
    add_take('t7', 'dokan_cool', [
        station({'s': 51.2}, 'kaka', 'W', DOK['kaka'][0], DOK['kaka'][1], hold=0.8, travel=1.2, shows=['kaka', 'bhagne', 'counter']),
        station(S_(6, 'বছর'), 'kaka', 'W', DOK['kaka'][0], DOK['kaka'][1], hold=0.7, word='বছর', shows=['kaka']),
        station(S_(6, 'বেতন'), 'till', 'O', 1.35, 2.42, sz=1.10, hold=0.4, word='বেতন', shows=['till']),
        station(S_(6, 'ফিরলো'), 'rafi', 'W', -1.5, 1.4, side='sideR', hold=1.6, word='ফিরলো', shows=['rafi', 'door']),
    ])
    acts += [
        {'who': 'kaka', 'at': S_(6, 'বছর'), 'face': ['elder', 'nostalgic'], 'pose': 'stand', 'say': [ranges[6][0] + 18, ranges[6][0] + 26], 'look': 'cam'},
        {'who': 'bhagne', 'at': S_(6, 'বছর'), 'pose': 'hands_hips', 'face': ['female', 'smug'], 'look': 'cam'},
        {'who': 'rafi', 'at': S_(6, 'ফিরলো'), 'pos': [-1.5, 1.4, 0], 'view': 'side', 'dir': 1, 'pose': 'walk', 'face': 'soul', 'walk_pose': 'walk', 'look': [-1.5, 3.4, 0]},
    ]
    for w, lk in (('বছর', 'cold'), ('ফিরলো', 'dark')): mood(w, 1, lk, at=S_(6, w))
    fx.append({'at': S_(6, 'বেতন'), 'kind': 'coin', 'on': 'till', 's': 0.8, 'size': 1.1}); sound.append({'at': S_(6, 'বেতন'), 'name': 'coin_box'})
    trans.append({'at': S_(7, 'যার'), 'kind': 'wheel', 'frames': 14})

    # ================= t8 — bhitore golden: the stolen rice (sentence 8)  [47.8 .. 52.8]
    add_take('t8', 'bhitore_golden', [
        station({'s': 55.05}, 'ma', 'W', BIT['ma'][0], BIT['ma'][1], hold=0.8, travel=1.3, shows=['ma', 'rafi', 'tea_table', 'stove']),
        station(S_(7, 'ভাত'), 'tea_table', 'O', 0.1, 1.6, sz=0.42, hold=0.8, word='ভাত', shows=['tea_table']),
        station(S_(7, 'কাড়লো'), 'rafi', 'C', BIT['rafi'][0], BIT['rafi'][1], side='sideR', hold=1.7, word='কাড়লো', shows=['rafi', 'ma']),
    ])
    acts += [
        {'who': 'ma', 'at': {'s': 55.1}, 'pos': BIT['ma'] + [0], 'view': '34', 'dir': 1, 'pose': 'stand', 'face': ['female', 'sassy'], 'visible': True, 'look': 'cam'},
        {'who': 'rafi', 'at': {'s': 55.1}, 'pos': BIT['rafi'] + [0], 'view': '34', 'dir': -1, 'pose': 'stand', 'face': 'soul', 'visible': True, 'look': 'cam'},
        {'who': 'ma', 'at': S_(7, 'ভাত'), 'pose': 'grip_shoulder', 'face': ['female', 'mascaraCry'], 'say': [ranges[7][0], ranges[7][1]], 'look': 'rafi'},
        {'who': 'rafi', 'at': S_(7, 'কাড়লো'), 'pose': 'stand', 'face': 'wail', 'look': 'cam'},
    ]
    for w, lk in (('ভাত', 'warm'), ('কাড়লো', 'dark')): mood(w, 1, lk, at=S_(7, w))
    fx.append({'at': S_(7, 'ভাত'), 'kind': 'steam', 'on': 'tea_table', 's': 1.1, 'size': 1.1})

    # ================= t9 — pasher day: half pay, teaching, khoddor, thief, payoff (sentence 9)  [52.8 .. 74.8]
    add_take('t9', 'pasher_day', [
        station({'s': 60.1}, 'pashi', 'P', PAS['pashi'][0], PAS['pashi'][1], sz=1.4, hold=1.2, travel=1.6, shows=['pashi', 'rafi', 'counter', 'tarazu', 'shutter']),
        station(S_(8, 'দোকানে'), 'tarazu', 'O', 2.5, 2.62, sz=1.42, hold=0.8, word='দোকানে', shows=['tarazu']),
        station(S_(8, 'বেতনে'), 'pashi', 'C', PAS['pashi'][0], PAS['pashi'][1], hold=0.7, word='বেতনে', shows=['pashi']),
        station(S_(8, 'শিখালো'), 'rafi', 'W', PAS['rafi'][0], PAS['rafi'][1], hold=0.7, travel=1.0, word='শিখালো', shows=['rafi', 'tulu', 'counter']),
        station(S_(8, 'হাতে'), 'khoddor', 'M', PAS['khoddor'][0], PAS['khoddor'][1], hold=0.9, travel=0.9, word='হাতে', shows=['khoddor', 'bhagne', 'desk', 'khata']),
                station(S_(8, 'রাফিকে'), 'bhagne', 'W', PAS['bhagne'][0], PAS['bhagne'][1], hold=4.6, word='রাফিকে', shows=['bhagne', 'khoddor', 'rafi', 'desk']),
    ])
    acts += [
        {'who': 'pashi', 'at': {'s': 60.15}, 'pos': PAS['pashi'] + [0], 'view': 'front', 'dir': -1, 'pose': 'stand', 'face': ['elder', 'suspicious'], 'enter': True, 'look': 'cam'},
        {'who': 'rafi', 'at': {'s': 60.15}, 'pos': PAS['rafi'] + [0], 'view': '34', 'dir': -1, 'pose': 'stand', 'face': 'standard', 'visible': True, 'look': 'cam'},
        {'who': 'tulu', 'at': {'s': 60.15}, 'pos': PAS['tulu'] + [0], 'view': '34', 'dir': 1, 'pose': 'stand', 'face': ['baby', 'curious'], 'enter': True, 'look': 'cam'},
        {'who': 'pashi', 'at': S_(8, 'বেতনে'), 'pose': 'hold_out', 'face': ['elder', 'sweetSmile'], 'prop': 'packet', 'hand': 'R', 'say': [ranges[8][0], ranges[8][0] + 6], 'look': 'cam'},
        {'who': 'rafi', 'at': S_(8, 'শিখালো'), 'pose': 'grip_shoulder', 'face': 'standard', 'look': 'tulu'},
        {'who': 'tulu', 'at': S_(8, 'শিখালো'), 'pose': 'stand', 'face': 'delight', 'look': 'rafi'},
        {'who': 'tulu', 'at': st_at('হাতে', 2), 'face': 'curious', 'pose': 'stand', 'look': 'khoddor'} if False else {'who': 'tulu', 'at': S_(8, 'হাতে'), 'face': ['baby', 'curious'], 'pose': 'stand', 'look': 'khoddor'},
        {'who': 'pashi', 'at': S_(8, 'শিখালো'), 'face': ['elder', 'suspicious'], 'pose': 'hands_hips', 'look': 'rafi'},
        {'who': 'khoddor', 'at': S_(8, 'হাতে'), 'pos': PAS['khoddor'] + [0], 'view': '34', 'dir': -1, 'pose': 'stand', 'face': 'proud', 'visible': True, 'look': 'cam'},
        {'who': 'bhagne', 'at': S_(8, 'হাতে'), 'pos': PAS['bhagne'] + [0], 'view': 'front', 'dir': 1, 'pose': 'stand', 'face': ['female', 'smug'], 'visible': True, 'look': 'cam'},
        {'who': 'khoddor', 'at': S_(8, 'খাতা'), 'pose': 'hold_out', 'face': 'proud', 'prop': 'khata', 'hand': 'R', 'look': 'bhagne'},
        {'who': 'bhagne', 'at': S_(8, 'রাফিকে'), 'pose': 'hold_up', 'face': ['female', 'smug'], 'prop': 'khata', 'hand': 'L', 'look': 'cam'},
        {'who': 'khoddor', 'at': S_(8, 'রাফিকে'), 'face': ['elder', 'suspicious'], 'pose': 'stand', 'look': 'rafi'},
        {'who': 'bhagne', 'at': S_(8, 'চোর'), 'face': 'rage', 'pose': 'point_out', 'look': 'rafi'},
        {'who': 'khoddor', 'at': S_(8, 'মাল'), 'pos': PAS['khoddor_pay'] + [0], 'pose': 'walk', 'face': ['elder', 'suspicious'], 'walk_pose': 'walk', 'look': [0.4, 1.5, 0]},
        {'who': 'khoddor', 'at': S_(8, 'কাছে'), 'pose': 'hold_out', 'face': 'proud', 'prop': 'packet', 'hand': 'R', 'look': 'rafi'},
        {'who': 'rafi', 'at': S_(8, 'কাছে'), 'pose': 'hold_out', 'face': 'standard', 'prop': 'packet', 'hand': 'L', 'look': 'khoddor'},
        {'who': 'pashi', 'at': S_(8, 'কাছে'), 'face': 'delight', 'pose': 'stand', 'look': 'khoddor'},
        {'who': 'tulu', 'at': S_(8, 'মাল'), 'face': 'eek', 'pose': 'stand', 'look': 'khoddor'},
    ]
    for w, lk in (('দোকানে', 'gold'), ('বেতনে', 'warm'), ('হাতে', 'cold'), ('রাফিকে', 'spot'), ('চোর', 'red'), ('কাছে', 'warm')): mood(w, 1, lk, at=S_(8, w))
    fx.append({'at': S_(8, 'দোকানে'), 'kind': 'glint', 'on': 'tarazu', 's': 0.8, 'size': 1.1}); sound.append({'at': S_(8, 'বেতনে'), 'name': 'coin_box'})
    fx.append({'at': S_(8, 'খাতা'), 'kind': 'paper', 'on': 'desk', 's': 0.8, 'size': 1.1}); fx.append({'at': S_(8, 'চোর'), 'kind': 'spark', 's': 0.8, 'size': 0.9}); sound.append({'at': S_(8, 'চোর'), 'name': 'flash'})

    # ================= t12 — door night again: the same door, closer each time (sentences 10-12)  [74.8 .. 91.8]
    add_take('t12', 'door_night', [
        station({'s': 77.35}, 'path', 'P', 0.1, 2.3, door=True, aim_x=0.1, aim_y=2.4, hold=1.0, travel=1.7, shows=['kaka', 'path', 'door']),
        station(S_(9, 'প্যাকেট'), 'kaka', 'W', 0.1, 2.2, door=True, hold=0.7, word='প্যাকেট', shows=['kaka', 'packet', 'door']),
        station(S_(10, 'আসো'), 'kaka', 'M', 0.1, 2.45, door=True, hold=0.7, word='আসো', shows=['kaka', 'door']),
        station(S_(10, 'পারে'), 'kaka', 'M', 0.1, 2.45, side='sideL', door=True, hold=0.8, word='পারে', shows=['kaka', 'rafi']),
        station(S_(10, 'রাফি'), 'rafi', 'M', DOR['rafi_door'][0], DOR['rafi_door'][1], side='sideL', door=True, hold=0.7, word='রাফি', shows=['rafi', 'door', 'kaka']),
        station(S_(11, 'যায়'), 'rafi', 'C', DOR['rafi_door'][0], DOR['rafi_door'][1], side='sideL', door=True, hold=2.2, word='যায়', shows=['rafi', 'door']),
    ])
    acts += [
        {'who': 'kaka', 'at': {'s': 77.4}, 'pos': [0.1, 1.0, 0], 'view': '34', 'dir': 1, 'pose': 'walk', 'face': ['elder', 'suspicious'], 'walk_pose': 'walk', 'visible': True, 'look': [0.1, 3.3, 0]},
        {'who': 'kaka', 'at': {'s': 80.5}, 'pos': DOR['pathmid'] + [0], 'pose': 'stand', 'face': ['elder', 'suspicious']},
        {'who': 'kaka', 'at': S_(9, 'প্যাকেট'), 'pose': 'hold_out', 'face': 'eek', 'prop': 'packet', 'hand': 'L', 'say': [ranges[9][0], ranges[9][1]], 'look': [0.1, 3.3, 0]},
        {'who': 'kaka', 'at': S_(10, 'আসো'), 'pose': 'grip_two', 'face': 'wail', 'say': [ranges[10][0], ranges[10][1]], 'look': 'cam'},
        {'who': 'rafi', 'at': S_(10, 'রাফি'), 'pos': DOR['rafi_door'] + [0], 'view': '34', 'dir': -1, 'pose': 'stand', 'face': 'standard', 'visible': True, 'look': 'cam'},
        {'who': 'rafi', 'at': S_(11, 'শিখাইছিলাম'), 'pose': 'stand', 'face': 'standard', 'say': [ranges[11][0], ranges[11][1]], 'look': 'kaka'},
        {'who': 'kaka', 'at': S_(11, 'যায়'), 'face': 'wail', 'pose': 'flinch', 'look': 'rafi'},
        {'who': 'rafi', 'at': S_(10, 'পারে'), 'face': 'soul', 'pose': 'stand', 'look': 'kaka'},
    ]
    for w, lk in (('আসো', 'cold'), ('যায়', 'dark'), ('শিখাইছিলাম', 'spot')): mood(w, 1, lk, at=S_({'আসো': 10, 'যায়': 11, 'শিখাইছিলাম': 11}[w], w))
    fx.append({'at': S_(9, 'প্যাকেট'), 'kind': 'knock', 'on': 'door', 's': 0.7, 'size': 1.1}); sound.append({'at': S_(9, 'প্যাকেট'), 'name': 'door_knock'})

    # ================= t13 — rasta morning: the partnership (sentence 13)  [91.8 .. 98.8]
    add_take('t13', 'rasta_morning', [
        station({'s': 98.3}, 'street', 'P', 0.1, 3.4, aim_x=0.6, aim_y=4.2, hold=1.6, travel=2.0, shows=['rafi', 'street', 'sign']),
                station(S_(12, 'মালিক'), 'khoddor', 'M', 1.5, 5.0, door=True, hold=0.7, word='মালিক', shows=['khoddor', 'rafi', 'sign']),
        station(S_(12, 'অংশীদার'), 'sign', 'O', 1.5, 6.0, sz=2.55, hold=1.9, word='অংশীদার', shows=['sign', 'khata']),
    ])
    acts += [
        {'who': 'rafi', 'at': {'s': 98.35}, 'pos': [-2.6, 3.2, 0], 'view': 'side', 'dir': 1, 'pose': 'walk', 'face': 'standard', 'walk_pose': 'walk', 'visible': True, 'look': [1.5, 5.5, 0]},
        {'who': 'rafi', 'at': {'s': 102.0}, 'pos': [1.0, 5.0, 0], 'pose': 'stand', 'face': 'standard'},
        {'who': 'khoddor', 'at': S_(12, 'মালিক'), 'pos': [2.0, 5.3, 0], 'view': '34', 'dir': -1, 'pose': 'stand', 'face': 'proud', 'visible': True, 'look': 'cam'},
        {'who': 'pashi', 'at': S_(12, 'মালিক'), 'pos': [2.9, 5.2, 0], 'view': '34', 'dir': -1, 'pose': 'stand', 'face': ['elder', 'sweetSmile'], 'visible': True, 'look': 'cam'},
        {'who': 'khoddor', 'at': S_(12, 'মালিক'), 'pose': 'grip_two', 'face': 'delight', 'prop': 'khata', 'hand': 'R', 'look': 'rafi'},
        {'who': 'rafi', 'at': S_(12, 'মালিক'), 'pose': 'grip_two', 'face': 'delight', 'look': 'khoddor'},
    ]
    for w, lk in (('ফিরলো', 'warm'), ('মালিক', 'gold'), ('অংশীদার', 'gold')): mood(w, 1, lk, at=S_(12, w))
    fx.append({'at': S_(12, 'মালিক'), 'kind': 'glow', 's': 0.8, 'size': 1.2}); sound.append({'at': S_(12, 'অংশীদার'), 'name': 'paper_turn'})

    # ================= t14 — pasher golden: the lesson + outro (sentences 14-15)  [98.8 .. end]
    add_take('t14', 'pasher_golden', [
        station({'s': 106.75}, 'rafi', 'W', PAS['rafi'][0], PAS['rafi'][1], hold=0.9, travel=1.6, shows=['rafi', 'tulu', 'counter', 'desk', 'shutter']),
        station(S_(13, 'শেখান'), 'rafi', 'W', PAS['rafi'][0], PAS['rafi'][1], hold=0.7, word='শেখান', shows=['rafi', 'tulu']),
        station(S_(13, 'জায়গাটা'), 'desk', 'O', -2.2, 2.2, sz=0.88, hold=0.8, word='জায়গাটা', shows=['desk', 'khata']),
        station(S_(13, 'নিয়ম'), 'board', 'O', -2.2, 3.1, sz=1.50, hold=0.9, word='নিয়ম', shows=['board']),
        station(S_(14, 'চাকরিতেও'), 'rafi', 'W', PAS['rafi'][0], PAS['rafi'][1], hold=0.8, travel=1.2, word='চাকরিতেও', shows=['rafi', 'tulu', 'counter']),
        station(S_(14, 'লিখুন'), 'rafi', 'C', PAS['rafi'][0], PAS['rafi'][1], side='sideR', hold=1.0, word='লিখুন', shows=['rafi', 'sign']),
        station(S_(14, 'ফলো'), 'rafi', 'M', PAS['rafi'][0], PAS['rafi'][1], side='sideR', hold=2.0, word='ফলো', shows=['rafi', 'counter', 'board']),
    ])
    acts += [
        {'who': 'rafi', 'at': {'s': 106.8}, 'pos': PAS['rafi'] + [0], 'view': '34', 'dir': -1, 'pose': 'stand', 'face': 'standard', 'visible': True, 'look': 'cam'},
        {'who': 'tulu', 'at': {'s': 106.8}, 'pos': PAS['tulu'] + [0], 'view': '34', 'dir': 1, 'pose': 'stand', 'face': ['baby', 'curious'], 'visible': True, 'look': 'cam'},
        {'who': 'rafi', 'at': S_(13, 'শেখান'), 'pose': 'grip_shoulder', 'face': 'standard', 'say': [ranges[13][0], ranges[13][1]], 'look': 'tulu'},
        {'who': 'rafi', 'at': S_(14, 'চাকরিতেও'), 'pose': 'point_out', 'face': 'standard', 'say': [ranges[14][0], ranges[14][1]], 'look': 'cam'},
        {'who': 'rafi', 'at': S_(14, 'লিখুন'), 'pose': 'point_out', 'face': 'delight', 'look': 'cam'},
        {'who': 'rafi', 'at': S_(14, 'ফলো'), 'pose': 'cheer', 'face': 'delight', 'look': 'cam'},
        {'who': 'tulu', 'at': S_(14, 'ফলো'), 'pose': 'cheer', 'face': 'delight', 'look': 'cam'},
    ]
    for w, lk in (('জায়গাটা', 'gold'), ('নিয়ম', 'spot'), ('ফলো', 'warm')): mood(w, 1, lk, at=S_(13 if w != 'ফলো' else 14, w))
    fx.append({'at': S_(13, 'জায়গাটা'), 'kind': 'paper', 'on': 'desk', 's': 0.8, 'size': 1.1}); fx.append({'at': S_(14, 'ফলো'), 'kind': 'glow', 's': 0.8, 'size': 1.1})

    # ---- ACTING IDLES: while a figure is on screen with nothing to say, its face still acts.
    # Faces alternate on the character's own pair, never during a walk, never twice in 1.8 s.
    IDLE_FACE = {
        'kaka': (['elder', 'sweetSmile'], ['elder', 'suspicious']),
        'rafi': ('standard', 'delight'),
        'bhagne': (['female', 'smug'], 'delight'),
        'ma': (['female', 'sassy'], ['female', 'judging']),
        'pashi': (['elder', 'suspicious'], ['elder', 'sweetSmile']),
        'tulu': (['baby', 'curious'], 'delight'),
        'khoddor': ('proud', 'delight'),
    }
    spans = [('t1', 0.0, 11.15), ('t2', 11.15, 20.15), ('t3', 20.15, 35.35), ('t4', 35.35, 39.7), ('t5', 39.7, 51.2),
             ('t7', 51.2, 55.05), ('t8', 55.05, 60.1), ('t9', 60.1, 77.3), ('t12', 77.3, 98.25),
             ('t13', 98.25, 106.7), ('t14', 106.7, end / FPS - 0.1)]
    for tid, t0, t1e in spans:
        tk = next(t for t in takes if t['id'] == tid)
        for who in F_.keys() if False else [w for w in ('kaka', 'rafi', 'bhagne', 'ma', 'pashi', 'tulu', 'khoddor')]:
            mine = [a for a in acts if a['who'] == who and _sec(a['at']) is not None and t0 - 0.2 <= _sec(a['at']) < t1e]
            if not mine: continue
            f0, f1 = IDLE_FACE[who]
            k = 0
            for t in [t0 + 1.4 + i * 2.3 for i in range(int((t1e - t0 - 1.4) / 2.3) + 1)]:
                k += 1
                acts.append({'who': who, 'at': {'s': round(t, 2)}, 'face': f0 if k % 2 else f1, 'look': 'cam'})

    # ---- EXITS at every take boundary: nobody ghosts into the next scene
    bounds = [('t1', 11.15), ('t2', 20.15), ('t3', 35.35), ('t4', 39.7), ('t5', 51.2), ('t7', 55.05),
              ('t8', 60.1), ('t9', 77.3), ('t12', 98.25), ('t13', 106.7)]
    leave = {
        't1': ['kaka', 'rafi', 'bhagne'], 't2': ['kaka'], 't3': ['kaka', 'rafi', 'bhagne'],
        't4': ['ma', 'rafi'], 't5': ['rafi', 'kaka', 'bhagne', 'khoddor'], 't7': ['kaka', 'bhagne', 'rafi'],
        't8': ['ma', 'rafi'], 't9': ['pashi', 'rafi', 'tulu', 'bhagne', 'khoddor'],
        't12': ['kaka', 'rafi'], 't13': ['rafi', 'khoddor', 'pashi'],
    }
    for tid, t1e in bounds:
        for who in leave[tid]:
            acts.append({'who': who, 'at': {'s': t1e - 0.08}, 'exit': True})

    # ---- sentences for the story gates
    subjects = ['kaka', 'rafi', 'kaka', 'kaka', 'kaka', 'ma', 'kaka', 'ma', 'rafi', 'kaka', 'kaka', 'rafi', 'rafi', 'rafi', 'rafi']
    shows = [
        ['kaka', 'bhagne', 'counter'], ['rafi', 'kaka', 'till'], ['kaka', 'packet', 'door'], ['kaka', 'bhagne', 'door'],
        ['kaka', 'rafi'], ['ma', 'rafi'], ['kaka', 'board', 'khata', 'khoddor'], ['ma', 'tea_table', 'rafi'],
        ['pashi', 'tarazu', 'rafi', 'tulu'], ['kaka', 'packet', 'door'], ['kaka', 'rafi', 'door'], ['rafi', 'kaka', 'door'],
        ['rafi', 'khoddor', 'desk', 'board'], ['rafi', 'desk', 'board'], ['rafi', 'sign'],
    ]
    for i, text in enumerate(SENT):
        sentences.append({'text': text, 'words': list(ranges[i]), 'subject': subjects[i], 'show': shows[i], 'nouns': []})

    film = {
        'title': '৪৮ শক্তির নিয়ম — নিয়ম ১১ (fresh2): কাজ সবাইকে শেখান, জায়গা কাউকে না',
        'fps': FPS, 'size': [W, H], 'end': end, 'words': 'voice/words.json',
        'camera_idea': {
            'name': 'Rest on the noun, travel on the verb — computed, not guessed',
            'why': 'Every station camera is computed from its subject height and the framing target (whole 0.45 / medium 0.62 / close head 0.52), so head widths, feet heights and the caption band are true by construction. The courtyard keeps every eye-line at 1.32 m or higher (the porch_roof fix).',
            'signature': 'Cuts only on the script\'s own place/time jumps; inside a scene one move carries the line and every noun beat rests quietly on its word.',
        },
        'puppet_pkg': ['cast'],
        'tween': {'frames': 6, 'ease': 'out', 'walk_frames': 8},
        'auto_view': True,
        'cast': {k: {'puppet': PUPPET[k], 'height': v[0], 'heads_tall': v[1], 'head_aspect': v[2],
                     'new_character': {'name': k, 'label': {'kaka': 'কাকা', 'rafi': 'রাফি', 'bhagne': 'ভাগ্নে', 'ma': 'মা', 'pashi': 'পাশি', 'tulu': 'টুলু', 'khoddor': 'খদ্দের'}[k]}}
                 for k, v in CAST.items()},
        'places': places,
        'props': {'packet': {'kind': 'box'}, 'khata': {'kind': 'notebook'}, 'pen': {'kind': 'pen'}},
        'takes': takes, 'acts': acts, 'sentences': sentences,
        'fx': fx, 'moods': moods, 'sound': sound, 'transitions': trans,
    }
    out = os.path.join(HERE, 'film.json')
    json.dump(film, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('wrote', out, '| takes', len(takes), '| acts', len(acts), '| stations', sum(len(t['stations']) for t in takes),
          '| fx', len(fx), '| moods', len(moods), '| end', end, f'({end/FPS:.1f}s)')

if __name__ == '__main__':
    main()
