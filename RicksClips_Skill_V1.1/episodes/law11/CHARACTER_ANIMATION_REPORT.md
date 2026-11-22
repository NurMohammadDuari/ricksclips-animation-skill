# CHARACTER ANIMATION REPORT — Law 11

Cast: chacha (owner), rafi (hero), nephew (the mistake), ma (the warning), neighbor, helper — toolkit builtin forms with per-character face states from `film.json` acts. All checks below were run against `out/plan/performance_baked.json` (per-frame states) and rendered frames.

## Character consistency
- Proportions are rig-owned (form definitions), constant across all 3,645 frames — no drift possible by construction (one SVG card per state, cached by key).
- Costumes: farmer-outfit chacha, sari ma, three-piece rafi — colors constant; verified across beats.
- No missing-head / floating-feet cases found in the 16-beat final-video check (contact shadow + feet-on-ground are rig-enforced: `S.dy = CARD.GY - ground`).

## Facial animation — the one CRITICAL error and its repair
- **Found:** the auto-acting layer had assigned the `cool` meme face (dark sunglasses) to 49 acts across ALL characters for ordinary conversation, pleading and crying — the "sunglasses at a funeral" class of error. Verified in the pre-repair probe sheets.
- **Repaired:** 41 acts → `standard` (calm kit face, blinks automatically when nothing happens), 8 nephew acts → `smug` (motivated).
- **After repair:** faces match the line at every checked beat: proud at the firing, sweetSmile during the ask, wail only at the begging door (once per film), calm standard on the thesis line at 86–91.6 s.
- Blink policy (CB rule): calm faces blink on idle — no frozen stares found in the beat sheet.
- Mouth: talking characters use visemes from the narration's word timing (`visemes(word)`); silent listeners have closed mouths — verified (no random flapping; the acting gate "pose or face changes per 10 s" = 16.8 ≥ 4).

## Body animation
- Walks: `m:walk/B` move library entries with foot targets; no sliding feet observed at the checked street/door beats; travel speeds match the character's walk_speed 1.0.
- Held props: gate `held props without a hand = 0` — every held packet/box/teacup is attached to a hand on every frame.
- Poses used at the right beats: point_out (firing), grip_shoulder (the ask), finger_up (ma's warning + nephew's rage), hands_hips, hold_out (serving), write (teaching).
- Frozen-figure limit: longest fully frozen figure with a resting camera = 2.9 s (gate ≤ 3) — passes.
- Anticipation/follow-through: pose changes are tweened (`film.json "tween"`), 6-frame ease-out; visible as eased gestures in the beat frames (no snap poses).

## Acting direction (per-character)
- **chacha:** proud → begging arc; his sweetSmile during the ask is the manipulation beat; his single wail at t9 is the emotional floor.
- **rafi:** the still center of the film; his calm face at the door is the thesis; never grins except the partnership handshake.
- **nephew:** smug at the till, rage finger-up when the customer bypasses him — his expressions carry the lesson without a single spoken line.
- **ma:** one scene, one warning, finger-up on the key word — minimal and loud.

## Known residual (LOW)
- The toolkit's builtin forms limit silhouette variety; the lost parallel rebuild's 7 original drawn characters (fresh_cast recipe, documented in SCRIPT_CORRECTIONS.md S-5) would lift this to full signature silhouettes next round.
