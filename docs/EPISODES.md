# Episodes

One folder per film. Each is rebuildable from `film.json` + `sets/` + `voice/`.

| episode | title | length | takes / stations | language | gate | status |
|---|---|---|---|---|---|---|
| [`law11`](../../RicksClips_Skill_V1.1/episodes/law11) | ৪৮ শক্তির নিয়ম — নিয়ম ১১ | 121.5 s (3645 f) | 11 / 45 | Bangla | 0 FAIL, 4 WARN of 41 | storyboard + stills done; animatic render pending |
| `lantern` | The Lantern Keeper (10 s demo) | 10 s | 1 / 9 | English | — | animatic rendered (1.7 MB) |
| `railway-time` | Railway Time (10 s silent test) | 10 s (300 f) | 1 / 7 | English | documented WARNs | animatic rendered (1.2 MB) |

## law11 — full breakdown

- **Story:** Law 11 of *The 48 Laws of Power* — learn to keep people dependent on you.
- **Source audio:** the user's Bangla narration, 121.3 s, 302 words (see `SCRIPT.md`).
- **Looks:** two sets (`shop.js`, `home.js`), four light states (morning, interior, night, golden).
- **Cast:** chacha (`cast:bbqdad`), rafi (`cast:barista`), nephew (`cast:backpack`), ma (`form:lady`),
  neighbour (`cast:business`), helper (`cast:scout`).
- **Camera idea:** "the counter that changes hands" — the film is told by who stands behind the counter.
- **Shot mix:** W 23 · P 13 · M 6 · C 2 · O 1.
- **Accepted WARNs:** see `episodes/law11/CAMERA_NOTE.md` (speed median/p90, face %, caption band).
- **Artifacts:** `out/plan/` (baked + `plan_report.md`), `out/storyboard.png/.html`, `out/stills/`.

## Adding an episode

1. `mkdir episodes/<name>/{sets,voice}` and copy a `film.json` from the closest episode.
2. Write `voice/words.json` (+ `voice.wav` when you have narration).
3. Build/point at sets, fill takes/stations/acts, run `python tools/film_plan.py check …` to 0 FAIL.
4. Render the storyboard, review it, then render the animatic.
5. Write `SCRIPT.md`, `CAMERA_NOTE.md` and `NOTES.md` in the episode folder.
