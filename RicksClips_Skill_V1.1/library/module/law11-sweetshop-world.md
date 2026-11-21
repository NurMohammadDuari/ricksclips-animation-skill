# Module: Law 11 "Sweet shop world" — cast + sets (2026-11-21)

**What:** A complete Bangla bazaar world built for the Law 11 film (খাতা যার, দোকান তার):
five original characters, three hand-built sets, one Bangla-sign helper.

**Where:**
- Cast sheet: `templates/vector2d_characters/code/sheets/sheet16_sweetshop.mjs`
  (auto-registered — any episode can use `cast:rafi`, `cast:chacha`, `cast:ma`,
  `cast:nephew`, `cast:dokandar`). Character lineup: `node code/lineup.mjs sheets/sheet16_sweetshop.mjs out.png`.
  Fixes over the first draft: chacha's moustache moved ABOVE the mouth (CB rule), ma's face
  changed from the text-drawing 'sassy' meme to 'sweetSmile', nephew's trollface meme → 'smug'.
- Sets (copy into `episodes/<name>/sets/`): `episodes/law11-art/sets/mithai_shop.js`
  (sweet shop: counter, glass jars with five real mithai, wall shelves, hanging balance scale,
  Bangla sign "মিষ্টি দোকান", ceiling fan, micro-motion on packs/scale/fan),
  `mithai_home.js` (patched mat, low table, brass pots, light shaft, signature doorway),
  `mithai_padosi.js` (tea-and-snacks shop: steaming kettle, hanging snacks, banana bunch,
  Bangla sign "চা ও নাস্তা", bench, radio).
- Extras sheet (deep-scene pass, 2026-11-22): `templates/vector2d_characters/code/sheets/sheet17_bazaar.mjs`
  (cast:khoddeder = bald elder + check lungi + net bag of limes, cast:khoddeder2 = green punjabi
  customer + jhola, cast:bepari = turbaned supplier + rope coil + money pouch). Staging rule: put
  extras ~3 m from the lens near the aim axis (9:16 hfov is only ~46 deg at 24 mm) with a face beat
  every <=3 s, or the head-cut and frozen gates trip.
- Story props drawn in `templates/threejs_film/poses.mjs` PROPS: `wage` = the yellow wage envelope
  (ref: Fahad bhuiyan Law 11) and `khata` = the red open ledger with ruled pages. Before these, any
  prop without a PROPS entry drew as a placeholder letter circle.
- Set deep dressing (ref pass): supplier's cardboard box stacks, wall clocks with live hands, Bangla
  price/rate boards on strings, clay water pots + tumblers, brooms, scale weights, family portrait +
  potted plants + kitchen string (home), tea-glass row + newspaper + rice sacks + chilli string (padosi).
- Bangla signage helper: `signTex(text, bg, fg, edge)` inside each set — a CanvasTexture
  with FreeSans/Arial Black text; Bengali renders correctly in headless Chromium.
- Reference film: `episodes/law11-art/` (film.json with the "who holds the khata holds the
  shop" camera idea; 0 FAIL of 41 gates at birth).

**Why it works:** the sets are data-light toon modules on the place_kit conventions
(build(THREE, scene, film, ctx), B2T coords, anchors, update() micro-motion) and the cast
rides the locked vector-character rig, so both reuse everywhere with zero new tooling.

**Reusable pattern:** for any Bangla/period story, copy the three sets, dress the cast from
the sheet, and keep the two sign helpers for shop fronts.
