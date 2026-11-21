# exit=True hides a character until an act explicitly sets visible=True

CRITICAL [adopted 2026-11-21, law11-art]. `bake_performance` turns acts into keyframes:
`exit: True` writes `visible=False`, and NOTHING restores visibility except a later act
that carries `visible=True` (the `enter=True` marker alone is decorative). An entry act
with only `pos/pose/face` leaves the character invisible — the plan gates still PASS
because the story gate reads station `shows/subject` lists, not baked visibility, so the
only symptom is missing figures in stills (the storyboard looks "empty" at the stations
whose subject is gone).

## The law
After every `exit=True`, the character's NEXT act in every later scene must carry
`visible=True` (and `enter=True` by convention).

## Audit one-liner
Summarise baked visibility spans per character and eyeball them against the story:

```python
import film_plan as fp
F = fp.load('episodes/<ep>/film.json'); perf = fp.bake_performance(F)
for who, runs in perf.items():
    spans = []; cur = None
    for r in runs:
        v = r['state']['visible']
        if cur is None or cur[2] != v:
            if cur: spans.append(cur)
            cur = [r['f0'], r['f1'], v]
        else: cur[1] = r['f1']
    if cur: spans.append(cur)
    print(who, ' '.join('%.0f-%.0fs=%s' % (a/F['fps'], b/F['fps'], v) for a, b, v in spans if b-a > 30))
```

Every `False` span that overlaps a scene where the character should be on stage = a
missing `visible=True`. Also check the inverse: a background character default-visible
from frame 0 before their entry act (give them an early `visible=False`).

Law 11 hit all three: the nephew was invisible through his own flashback (10-65 s), the
uncle invisible through the begging scene he stars in (69-121 s), and the neighbour
shopkeeper haunted every set from frame 0 until his 53.3 s entry.
