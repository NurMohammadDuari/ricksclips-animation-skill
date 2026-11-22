# SCRIPT CORRECTIONS — Law 11

Rule honored: the narration's meaning was never changed. Every correction below is a DIRECTION correction (what the picture does while the line plays), documented as ORIGINAL → PROBLEM → CORRECTION → REASON → VISUAL DIRECTION.

---

## S-1 — Sunglasses contradicting calm narration (CRITICAL, fixed + verified)

**ORIGINAL DIRECTION (in data, not text):** 49 acting acts assigned the `cool` face (dark sunglasses) to chacha, rafi, ma, helper, neighbor during ordinary conversation, pleading and crying beats — e.g. act 119/120 @ 77.0–77.7 s (rafi begging scene), act 134 @ 90.0 s (rafi's calm refusal close-up on "ভরসাটা শিখানো যায় না"), act 162 @ 110.4 s (rafi teaching).

**IDENTIFIED PROBLEM:** the sunglasses face on the hero during the film's most sincere line ("মানুষের ভরসাটা শিখানো যায় না") turns sincerity into a meme; the audience reads sarcasm. This was the "not following the script direction" error class.

**CORRECTED DIRECTION:** `cool` → `standard` (calm) on 41 acts; on 8 nephew acts → `smug` (the nephew's smugness IS the story point — the uncle's mistake).

**DIRECTOR'S REASON:** facial expression must serve the line being spoken at that second; the calm refusal is the thesis of Law 11.

**VISUAL DIRECTION:** rafi's face calm and level at the door; the nephew visibly smug at the till so the audience understands why the shop dies.

**VERIFICATION:** re-baked plan 0 FAIL / 4 WARN; final render beats at 77 s and 110 s show calm faces (16-beat sheet, frames v_11, v_15).

## S-2 — Insert rests that cut faces off (HIGH, recipe fixed on the parallel rebuild)

**ORIGINAL:** till/board object inserts framed from beside a standing character — that character's head crossed the frame edge (measured 95–100 % cut on those rests).

**CORRECTED (recipe):** straight-on centering of the noun: camera on the object's axis (e.g. till at `[-0.62, 2.95, 1.14]` ← camera `[-0.78, 0.9, 1.25]`), no character between lens and noun; in the surviving production the edge-cut gate already passes at 9.0 %.

**DIRECTOR'S REASON:** an insert exists to show a THING; a half-cut face at the edge steals the read.

**VERIFICATION:** parallel rebuild probe f_0290/f_03510 showed centered nouns; surviving production gate value 9.0 % (≤ 13).

## S-3 — Furniture crossing the actor (HIGH, recipe fixed)

**ORIGINAL:** t9 medium on the nephew at the partnership desk — the desk's near corner crossed his body (the "slab through the face" frames).

**CORRECTED (recipe):** raise camera above the desktop plane (camera z 1.06, aim z 1.0) and move the viewpoint past the desk's open end (`pos [4.62, 0.78]`, aim the character), so the desk reads as furniture below the chest, not a wall.

**REASON:** the audience must see WHO acts; furniture may frame, never occlude.

**VERIFICATION:** probe f_02130 after fix: character clear, desk edge only in the lower-left as context.

## S-4 — Doors shot from below the porch (HIGH, recipe fixed)

**ORIGINAL:** all door-set medium/close stations at camera z 0.76–0.94 aiming up at z 1.13 — the porch roof underside filled the upper frame (raycast-verified).

**CORRECTED (recipe):** eye-level coverage: camera z 1.42 / aim z 1.32 on 10 door M stations, close-ups at z 1.30.

**REASON:** the door motif must repeat CLEANLY three times (night → morning → night); a looming roof turns the knock into a haunted-house beat.

**VERIFICATION:** parallel rebuild probe f_02360 clean blue door + warm porch light; surviving production door beats read clean at f_2280/f_2565 equivalents.

## S-5 — Set nouns that could not be read (MEDIUM–HIGH, recipe preserved)

**ORIGINAL:** night shop inserts unreadable (dark-wood till; navy "papers" reading as lit windows; pale glass jars as gray boxes; no warm pools).

**CORRECTED (recipe, kept for the next rebuild):** brass till `#c9a23c/#e8c063` + slot; dark green boards `#3d5c48` with cream papers `#f7f0dd` + red marks `#b03a2e`; translucent glass jars (`opacity .45`, `#cfe9f2`) with brass lids + scaled mithai; two warm PointLights at bulb positions; door set: porch PointLight, central trees moved out of the walk lane, fence moved behind the house wall.

**REASON:** every named noun must be recognizable in half a second at Shorts size.

**VERIFICATION:** parallel rebuild probes f_0290/f_1210/f_3510 warm and readable.

## Not changed (documented so nobody "fixes" them later)
- Sentence order, all Bangla wording, 15-sentence structure, the door motif, the mother's thesis line placement, the CTA ending.
- The author's set compositions and the shop's counter-forward staging.
