# CHARACTER ANIMATION REPORT — Law 11 (fresh2)

## The seven characters (cast/sheets/fresh_cast.mjs — drawn for this film)

| id | label | body | signature | fix baked into the drawing |
|---|---|---|---|---|
| kaka | কাকা | dad form | white embroidered taqi cap, silver round specs, teal kabuli vest, prayer beads | specs lens circles at `hy-16` — ON the eye line (the v1 bug hung them on the chin at `hy+8`) |
| rafi | রাফি | standard | tall black quiff, teal gamcha, olive vest, red khata under the arm | quiff bottom edge at `hy-56..-58` — clears the meme eyes (`hy-18..-34`) that the v1 quiff covered |
| bhagne | ভাগ্নে | kid | mustard backwards cap, red-white striped tee, earbud wire | torso widths now derive from shoulder positions (castkit's `B` carries no `w`; the v1 stripes silently drew NaN) |
| ma | মা | lady | green polka-dot sari (plain long cloth), bindi, bun with white streak | gown style corrected from the white lab-coat split to a plain green sari |
| pashi | পাশি | dad | tall white Karaila topi, thin grey moustache, measuring-tape sash | moustache arcs at `hy+18` — at the mouth (v1 drew it at `hy+52`, on the chest); topi re-seated on the head |
| tulu | টুলু | kid | tousled tufts, yellow tee | first act flagged `enter` so he is absent until his scene |
| khoddor | খদ্দের | dad, fat | oiled comb-back, white punjabi, gold chain, jute sweets bag | first act flagged `enter` |

Visual verification: every character rendered in chromium (front/34/side/back views and the
acting faces wail / delight / proudTears / judging / suspicious) — the contact sheets were
inspected during the build, not assumed.

## Facial animation

- Faces come from the locked meme system; act `face` values are strings resolved inside each
  character's own set (elder / female / baby) — e.g. kaka `sweetSmile → suspicious →
  nostalgic`, bhagne `smug → rage`, ma `sassy → judging → mascaraCry`, rafi `standard →
  strain → awkward → soul → wail`, khoddor `proud → delight`.
- Faces swap 0–3 frames BEFORE their word (the kit's random lead), the body pose follows one
  frame later; blinks cover every swap and never run while a character talks.
- Mouths: `say` ranges drive phoneme→viseme mapping (`film_plan.visemes`) — mouths move only
  on quoted words, never on silent characters (gate: held props without a hand = 0; frozen
  figure = 2.1 s, gate ≤ 3).

## Body animation

- Pose vocabulary on the action words: `point_out` (the hook, the lesson), `lean_in` +
  `finger_up` (ma's warning), `grip_shoulder` (the flashback request, the teaching),
  `hand_mouth` (rafi laughing off the warning), `hold_out` (the packet, the pay-off),
  `grip_two` (the begging), `flinch` (হাজির), `shrug`, `write` (the khata work),
  `cheer` (the outro), walk cycles with step frames on every exit/entrance.
- Tween: 6-frame out-ease on every pose/face change (`tween: {frames: 6, ease: 'out'}`) —
  no snap poses; landed poses are dead-still by design (no idle float).
- Acting idles: every on-screen character alternates its face pair every ~2.3 s (generated
  in build_film.py) so nobody freezes while the camera rests — the longest frozen figure
  with a resting camera is 2.1 s (gate ≤ 3).

## Every action has a motivation (examples)

- bhagne ALREADY sits at the till in the opening (the insult the narration states).
- kaka `hold_out` on "প্যাকেট" at both door visits — the script's own packet motif.
- khoddor `hold_out` khata to bhagne (kept, not taught) then `walk` to rafi and pays —
  the film's proof of who is trusted.
- rafi `walk` with `soul` face on "ফিরলো" — the ten-years dismissal is shown as an exit.
- The outro `cheer` is shared by rafi AND tulu — the lesson being passed on.

## Honest limitations

- Walk cycles are the kit's 2-frame step swap (Rick animatic level), not full leg cycles.
- Hands are ink-stick curves; object grips use the kit's pose targets (no finger detail).
- The 10 fps delivery halves the smoothness of the tweens; the 30 fps plan (committed) is
  the full-rate version of exactly this acting.
