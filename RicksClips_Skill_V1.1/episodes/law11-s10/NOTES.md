# law11-s10 — The Firing (Law 11 opening 10 s, script-directed)

**What this episode is:** the from-scratch rebuild demanded after the law11-ai auto-plan drifted off the script
(agents staged invented gags — a knife, a "গোপন রহস্য" sign — instead of the story beats). Every station and act
here is keyed to a word of the real Law 11 script (0–10 s):

| time | script | camera | acting |
|---|---|---|---|
| 0–2.0 s | চাচা: "কাল থেকে আর আসা লাগবে না…" | W, uncle at his shop, proud | k:proud → drift glide |
| 2.0–2.9 s | "…লাগবে না, রাফি।" | M on uncle, at rest before the word | k:annoyed + point_out on "না" (the wave-off) |
| 2.9–5.1 s | "আমার ভাগ্নে এখন সব পারে।" | wide two-shot incl. Rafi (the name lands on him) | k:smug + cool on "ভাগ্নে"; glint on the counter |
| 5.1–7.0 s | রাফি: "চাচা, ১০ বছর…" | W reverse on Rafi, at rest before his word | k:shocked + flinch |
| 7.0–8.4 s | "…আপনার ভাগ্নেরে তো সব…" | M closer | shrug (hands out), k:worried → k:sad |
| 8.4–9.5 s | "…আমিই শিখাইলাম!" | M closer still | show_wrist (hand to chest), sweat fx on the word |
| 9.5–10 s | বর্ণনাকারী: "কিন্তু…" | slow push-in | mood cool_blue — the turn begins |

**Style baseline:** `ricksclips3000` STYLE DNA (12,761 measured frames). Final render measured on the delivered
file: lum 109.7 (DNA mean 98.8, per-video range 64.8–119.5), sat 0.439 (0.268–0.508), warm +43.8 (−22.6…+56.7) —
inside the channel envelope, on its warm end (sweet-shop interior).

**Cast (original):** মালিক চাচা = dad/fat, kurta (maroon #a03a2c / cream / mustard); রাফি = standard, shopAssistant
(honey brown #8a5a2f / cream / red). Bengali visemes: `tools/film_plan.py` now maps Bengali consonants/vowel signs
to mouth shapes (this episode is the first to use it — mouths move on Bengali words).

**Set:** sweet shop from scratch (`sets/set_p1.js`): counter + sweet jars, price board, two shelves, sugar sacks,
crate, lamp, plant; warm cream palette, interior light with a near-neutral `light_over` (the DNA warm target).

**Gates:** 0 FAIL / 2 WARN of 41 (speed p90 12.1 px/f vs Rick 23 — the film is calmer; head-cut-by-edge 14 % vs 13).
Warns accepted: the 10 s is one flowing take (0 cuts) so travel speed sits below the channel's median.

**Learned (registered in library):**
- pitfall/card-tip-sinks-character-behind-geometry.md — the card tip silently culls characters staged behind walls/counters; stage in the open.
- Bengali visemes in film_plan.py (VIS + BENGALI_VIS).

**Render:** 300 frames @30 fps, 720×1280 (channel resolution), `render.mjs --scale 0.6667` in 3 chunks, muxed with
the episode voice (first 10 s of the Law 11 mp3, `-t 10.0`), delivered as `download/law11-s10-script-10s.mp4`.
