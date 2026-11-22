# Law 11 (fresh) — কাজ সবাইকে শেখান, জায়গা কাউকে না

**Series:** ৪৮ শক্তির নিয়ম (The 48 Laws of Power, Bangla)
**Episode slug:** `law11-fresh` — built 2026-11-22, every asset drawn/built from scratch for THIS film.
**Source audio:** `The 48 Laws Of Power By Robert Greene Explained In Bangla Law 11.mp3` (121.3 s, the user's own narration).
**Word timings:** `tools/audio_probe.py` on the real audio — 254 energy-aligned words (`voice/words.json`). No time-stretching.
**Render:** `out/animatic.mp4` — 3,639 frames @ 30 fps, 540x960, H.264 + AAC (voice muxed).
**Plan status:** `film_plan.py check` = 0 FAIL / 10 WARN of 41 gates. Measured-film dispositions: `CAMERA_NOTE.md`.

## Cast — seven NEW characters (sheet `cast/sheets/fresh_cast.mjs`)

| character | puppet | height | signature (drawn for this film) | rôle in the script |
|---|---|---|---|---|
| `kaka` | cast:fresh_cast/kaka | 1.68 | white embroidered taqi cap, silver round specs, teal kabuli vest, prayer beads | the uncle — hires, fires, begs |
| `rafi` | cast:fresh_cast/rafi | 1.70 | tall black quiff, teal gamcha scarf, olive vest, red khata ledger under the arm | the hero |
| `bhagne` | cast:fresh_cast/bhagne | 1.38 | mustard backwards cap, red-white striped tee, earbud wire, gum bubble | the nephew handed the counter |
| `ma` | cast:fresh_cast/ma | 1.58 | green polka-dot tangail sari, white streak in the bun, red bindi | Rafi's mother |
| `pashi` | cast:fresh_cast/pashi | 1.72 | tall white Karaila topi, thin grey moustache, brass tarazu, measuring tape | the neighbouring shopkeeper |
| `tulu` | cast:fresh_cast/tulu | 1.30 | tousled tufts, yellow tee, tin tiffin | the boy rafi trains at the new shop |
| `khoddor` | cast:fresh_cast/khoddor | 1.75 | oiled comb-back, white punjabi, gold chain, jute sweets bag | the big credit customer |

## Sets — five NEW sets (sets/*.js), nine place/light combinations

`dokan` (sweet shop: counter, glass mithai jars, ceiling fan, one warm bulb, mousetrap gag, khata desk + supplier board, till) · `basha_door` (blue door, tulsi pot, bicycle, tin roof, porch bulb) · `bhitore` (clay stove + kettle, low table, calendar, radio shelf, cot, light-shaft window) · `pasher` (green roll shutter, brass tarazu, rice sacks, oil tins, partnership desk + ৪-আনা board) · `rasta` (shop-front row, tea cart, lamppost, telegraph birds, puddle).
Lights: night / morning / interior / day / golden — the light changes at every story turn.

## SCRIPT DIRECTION MAP — every scene, driven by the line being spoken

| # | audio time | script line (সময় অনুযায়ী) | take | what the camera shows, exactly when the line says it |
|---|---|---|---|---|
| 1 | 0.1–3.6 | কাল থেকে আর আসা লাগবে না, রাফি। আমার ভাগ্নে এখন সব পারে। | t1 (dokan, night) | HOOK: kaka at the counter's end points rafi out, proud; bhagne ALREADY sits at the till (the insult); "ভাগ্নে" lands on a wide of bhagne at the till |
| 2 | 4.0–8.6 | চাচা, ১০ বছর... আপনার ভাগ্নেরে তো সব আমিই শিখাইলাম! | t1 | rafi pleads (lean_in → point_out); "১০ বছর" lands on rafi; till insert shows what he lost |
| 3 | 9.1–14.6 | কিন্তু ৩ মাস পর, সেই চাচাই মিষ্টির প্যাকেট হাতে... রাফির বাসায় এসে হাজির! | t2 (basha_door, night) | door knock (fx + sound), kaka walks the path, packet held out on "প্যাকেট", close on his scared face on "হাজির" |
| 4 | 15.1–20.6 | অথচ ১ বছর আগে, চাচা নিজেই ভাগ্নেকে নিয়ে রাফির বাসায় এসে বলেছিলেন, | t3 (SAME door, MORNING — the flashback reads by light) | kaka + bhagne walk in together; "ভাগ্নেকে" lands on the two of them at the door |
| 5 | 21.1–24.6 | রাফি, পোলাটারে কাজ শিখায় দাও... তুমি তো আমার নিজের পোলার মতো! | t3 | kaka's hand on rafi's shoulder (grip_shoulder), sweetSmile; rafi shrugs awkwardly |
| 6 | 25.1–30.6 | সব শিখাইস না, বাবা... মালিকের ভাগ্নে, মালিকেরই লোক! | t4 (bhitore, interior) | ma leans in, finger_up on "মালিকের"; rafi laughs it off (hand_mouth) |
| 7 | 31.1–47.6 | মায়ের কথা হেসে উড়িয়ে... সাপ্লায়ারদের নম্বর, বাকির খাতা... খদ্দের। ভাগ্নে সব শিখে ফেলতেই, চাচা বললেন সেই কথা... ১০ বছর পর... বেতন নিয়ে বাসায় ফিরলো। | t5 (dokan, day → golden → cool) | "নম্বর" on the supplier board; "খাতা" on the khata; "খদ্দের" as khoddor walks in; kaka says THE line (spot_hero); light drops cool on "১০ বছর পর"; "বেতন" on the till; "ফিরলো" on rafi walking out the door (m:walk/sad) |
| 8 | 48.0–52.6 | যার পাতে ভাত দিলি... সেই তোর ভাত কাড়লো, বাবা! | t6 (bhitore, golden dusk) | ma grips rafi's shoulder; "ভাত" lands on the tea table; rafi's crying face on "কাড়লো" |
| 9 | 53.0–74.6 | ১ মাস পর, পাশের দোকানে অর্ধেক বেতনে... কাজ শিখালো... বড় খদ্দের রাখলো নিজের হাতে... খাতা ভাগ্নের হাতে... চিনতো শুধু রাফিকে। বললো চোর... মাল নিতে গেলো রাফির কাছে! | t7 + t8 (pasher, day) | "দোকানে" on the brass tarazu; "চাকরি" on pashi paying half; "কাজ" as rafi teaches tulu; "খদ্দের" as khoddor enters; the red khata slides into the DESK (kept, not taught); "খাতা" on bhagne at the desk; "রাফিকে" as khoddor looks past bhagne; "চোর" on bhagne's finger_up (flash_red); "মাল" as khoddor crosses to rafi and pays |
| 10 | 75.0–80.6 | ৩ মাসে বিক্রি অর্ধেক হতেই, চাচা মিষ্টির প্যাকেট হাতে রাফির বাসায় এসে বললেন, | t9 (basha_door, night — the SAME door, again) | kaka walks the path again; "প্যাকেট" held out; "বাসায়" on the door |
| 11 | 81.0–85.6 | রাফি, কাল থেকে আবার আসো, বাবা... ভাগ্নে আমার কিছুই পারে না! | t9 | kaka begs (grip_two, crying); the door opens and RAFI steps out on "রাফি" |
| 12 | 86.0–91.6 | চাচা, কাজ তো সবই শিখাইছিলাম... খালি মানুষের ভরসাটা শিখানো যায় না। | t9 | rafi's calm close-up on "কাজ"; the door between them on "যায়"; kaka wails |
| 13 | 92.0–98.6 | রাফি আর ফিরলো না... ৬ মাস পর, পাশের দোকানের মালিক ওকে ৪ আনার অংশীদার বানালেন! | t10 (rasta, morning) | rafi walks the street toward the shop; "মালিক" on the handshake (grip_two); "আনার"/"অংশীদার" on the desk papers + ৪-আনা board |
| 14 | 99.0–111.6 | কাজ সবাইকে শেখান... নিজের জায়গাটা কাউকে শিখিয়ে দিবেন না। ... ১১ নম্বর নিয়ম... | t11 (pasher, golden) | rafi teaches tulu at HIS counter; "জায়গাটা" on the desk (the red khata stays in it); "নম্বর" on the ৪-আনা board |
| 15 | 112.0–120.9 | আপনার চাকরিতেও কি...? কমেন্টে লিখুন। এমন আরো গল্প পেতে ফলো করুন। | t11 | rafi asks the camera on "চাকরিতেও"; "কমেন্টে" on the shop sign; follow gesture; loop back to frame 0 |

## Why this obeys the script direction

- Every cut lands ONLY on a place/time jump the script names (shop → door, morning flashback, home → new shop → street). Cuts/min measured 0.74 (gate <= 0.9).
- Every named noun is ON SCREEN at its word: the gate "named nouns not on screen within 0.5 s of their word" = **0** (plan) — verified against the real audio timings.
- The repeating door motif (night → morning → night) is the script's own structure (the packet knocks twice); the camera repeats its approach and ends closer each time.
- Sentence gate: "sentences whose subject or action is on screen" = 100 %.

## Reproduce

```bash
python3 episodes/law11-fresh/build_film.py          # film.json from the script + words.json
python3 tools/film_plan.py check episodes/law11-fresh/film.json
node templates/threejs_film/render.mjs episodes/law11-fresh/film.json --storyboard
node templates/threejs_film/render.mjs episodes/law11-fresh/film.json --animatic --scale 0.5
```
