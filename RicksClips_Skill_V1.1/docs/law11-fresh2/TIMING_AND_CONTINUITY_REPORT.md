# TIMING, MOTION & TRANSITION REPORT — Law 11 (fresh2)

## The timing foundation

- Delivery frame rate of the plan: 30 fps (the kit's native rate; the delivered animatic
  samples every 3rd frame at 10 fps — see the honest note at the end).
- Narration: 121.3 s MP3 → 198 energy-aligned words (`voice/words.json`). Nothing was
  time-stretched; the plan's `end` = last word + 0.6 s = 3,621 frames = 120.7 s.
- Sentence spans measured from the audio; take boundaries = the script's own place/time
  jumps at those measured spans (11 takes, 10 cuts, 0.83 cuts/10 s).

## Motion rules applied

1. **Word-first acting:** face swaps lead their word by 0–3 frames (kit random lead), body
   follows one frame later — reactions read as reactions, not as machine timing.
2. **Tweening:** 6-frame out-ease between poses/faces; walk cycles get 8-frame blends.
   No snap changes anywhere.
3. **Ease:** camera travels use smootherstep (zero speed and acceleration at both ends);
   character moves use fast-in/slow-settle with no overshoot; walks move at a steady
   1.1 m/s with a step every ~8 frames.
4. **Arrival rule:** word stations rest 0–6 frames before their word — the noun is on
   screen, still, when it is spoken (gate: 0 violations).
5. **No frozen acting:** generated face idles every ~2.3 s per visible character; longest
   frozen figure with a resting camera = 2.1 s (gate ≤ 3).
6. **No speed spikes:** camera peak 55 px/f (gate ≤ 60); travels that would sweep past a
   body get an arc via point; colliding word beats were merged (the t9 drama plays in one
   wide rather than six teleporting stations).

## Transitions (drawn, used only where the script jumps)

| at | kind | purpose |
|---|---|---|
| "কিন্তু ৩ মাস পর" (t2) | steam, 16 f | the ৩ মাস jump — a boil-up clears over the cut |
| "যার পাতে ভাত" (t7→t8) | wheel, 14 f | the shop → home jump closes on the door, opens on the kettle |

All other scene changes are straight cuts ON the named jumps (courtyard → courtyard
flashback by morning light, shop → neighbour shop → street → shop). No transition decorates
a jump the script does not make.

## Continuity ledger (verified)

- Same sets reused by construction (10 place entries over 5 set modules); the door motif
  night → morning → night; the red khata stays in the desk from t9 to t14.
- Exit/re-enter acts at every cut — no character ghosts into a scene they are not part of
  (this was the 46-second no-face failure of the first draft; the acting and noun gates now
  hold at 100 % / 0).
- Sound cues (`out/plan/sound_events.json`): door_knock ×2, coin_box ×2, paper_turn ×3,
  flash — placed on the action nouns; the mix carries narration + these cue marks.

## Honest note on the delivered rate

The delivered animatic is 10 fps (every 3rd frame at 432×768). Tween blends therefore read
simpler than designed, and the walk cycles show their 2-frame step at a slower cadence.
The plan, the baked camera/performance files and the resumable render script for the full
30 fps / 540×960 version are committed — rendering it is pure compute, no authoring left.
