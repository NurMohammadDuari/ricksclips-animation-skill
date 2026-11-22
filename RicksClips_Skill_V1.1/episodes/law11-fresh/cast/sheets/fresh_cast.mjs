// SHEET law11-fresh — SEVEN ORIGINAL CHARACTERS DRAWN FOR THIS FILM (law11-fresh, 2026-11-22).
// New designs by the artist — no reuse of sheet16/sheet17 signatures:
//   kaka    = white embroidered taqi cap + silver round specs + teal kabuli vest + prayer beads
//   rafi    = tall black quiff + teal gamcha scarf + olive vest + red khata ledger under the arm
//   bhagne  = mustard backwards cap + striped tee + earbud wire + gum bubble
//   ma      = green polka-dot tangail sari + white streak in the bun + brass bangles
//   pashi   = tall white Karaila topi + thin grey moustache + brass specs + measuring tape + tarazu
//   tulu    = tousled tuft hair + yellow half-sleeve + tin tiffin box
//   khoddor = oiled comb-back hair + white punjabi + gold chain + jute sweets bag
import { INK, P, L, ell, f1, smooth, brush, shade, tint, GOLD, GOLDL, STEEL, BRONZE, WOOD, WOODD, CREAM, RED, fillPts, poly, rect, circ, hl, pole, fist, cloud } from '../castkit.mjs';

const TEAL = '#1f5f6b', OLIVE = '#5a6b35', MUST = '#d8a437', SARI = '#2f7a4f', DOTW = '#f2ede0',
      REDK = '#a8322e', TIN = '#9aa5ad', JUTE = '#c8a86a', HAIRB = '#221a12', GREY = '#8d8d90';

export const TITLE = 'Cast sheet law11-fresh: sweet-shop power world';

export const CAST = [
  // ---------------------------------------------------------------- KAKA — the uncle who owns, fires and begs
  { name: 'kaka', label: 'কাকা (মালিক)', form: 'dad', size: 'fat', coat: '#e9dfc8', face: 'proud',
    hat: ({ cx, hy }) => { const o = []; // white taqi cap, gold piped zigzag embroidery
      o.push(`<path d="M${cx - 74},${hy - 62} Q${cx},${hy - 118} ${cx + 74},${hy - 62} L${cx + 74},${hy - 34} Q${cx},${hy - 62} ${cx - 74},${hy - 34} Z" fill="#f7f4ea" stroke="${INK}" stroke-width="5"/>`);
      o.push(`<path d="M${cx - 74},${hy - 34} Q${cx},${hy - 62} ${cx + 74},${hy - 34} L${cx + 74},${hy - 18} Q${cx},${hy - 46} ${cx - 74},${hy - 18} Z" fill="#fbf9f2" stroke="${INK}" stroke-width="5"/>`);
      for (let k = -2; k <= 2; k++) o.push(L(`M${cx + k * 26},${hy - 40 - Math.abs(k) * 6} l14,-12`, 4, GOLD));
      o.push(hl(`M${cx - 44},${hy - 92} Q${cx - 6},${hy - 106} ${cx + 30},${hy - 96}`, 6, .5));
      return o; },
    headBack: ({ cx, hy }) => [ // bald crown, grey side hair
      fillPts([[cx - 92, hy + 10], [cx - 84, hy - 34], [cx - 58, hy - 52], [cx - 46, hy - 18], [cx - 54, hy + 14]], GREY, 5),
      fillPts([[cx + 92, hy + 10], [cx + 84, hy - 34], [cx + 58, hy - 52], [cx + 46, hy - 18], [cx + 54, hy + 14]], GREY, 5)],
    faceTop: ({ cx, hy }) => { const o = []; // silver round specs pushed low on the nose + grey chin-strip beard
      o.push(circ(cx - 34, hy + 6, 25, 'none', 5), circ(cx + 34, hy + 6, 25, 'none', 5));
      o.push(`<circle cx="${cx - 34}" cy="${hy + 6}" r="25" fill="#cfe3ea" fill-opacity=".25"/>`);
      o.push(`<circle cx="${cx + 34}" cy="${hy + 6}" r="25" fill="#cfe3ea" fill-opacity=".25"/>`);
      o.push(L(`M${cx - 9},${hy + 2} Q${cx},${hy - 6} ${cx + 9},${hy + 2}`, 4, STEEL));
      o.push(L(`M${cx - 59},${hy} l-16,-14`, 4, STEEL), L(`M${cx + 59},${hy} l16,-14`, 4, STEEL));
      o.push(hl(`M${cx - 46},${hy - 4} Q${cx - 38},${hy - 14} ${cx - 26},${hy - 12}`, 4, .6));
      o.push(`<path d="M${cx - 44},${hy + 62} Q${cx},${hy + 52} ${cx + 44},${hy + 62} Q${cx},${hy + 96} ${cx - 44},${hy + 62} Z" fill="#b9bcc2" stroke="${INK}" stroke-width="4.5"/>`);
      return o; },
    details: ({ cx, top, bot }) => { const o = [], W = 150; // teal kabuli vest with brass buttons + bead loop
      o.push(poly([[cx - W * .92, top + 8], [cx - W * .5, top], [cx - W * .2, top + 44], [cx - W * .2, bot - 8], [cx - W * .62, bot - 8]], TEAL, 5));
      o.push(poly([[cx + W * .92, top + 8], [cx + W * .5, top], [cx + W * .2, top + 44], [cx + W * .2, bot - 8], [cx + W * .62, bot - 8]], TEAL, 5));
      o.push(rect(cx - W * .62, bot - 16, W * 1.24, 12, shade(TEAL, .75), 4, 2));
      for (const t of [.42, .58, .74]) o.push(circ(cx - W * .2, top + (bot - top) * t, 5.5, BRONZE, 3));
      o.push(`<path d="M${cx - W * .2},${top + 44} L${cx},${top + 72} L${cx + W * .2},${top + 44}" fill="none" stroke="${INK}" stroke-width="4"/>`);
      o.push(`<path d="M${cx - 14},${top + 6} Q${cx},${top + 88} ${cx + 14},${top + 6}" fill="none" stroke="${INK}" stroke-width="3"/>`);
      o.push(`<circle cx="${cx - 16}" cy="${top + 116}" r="17" fill="none" stroke="#8a4a2a" stroke-width="6"/>`);
      for (let k = 0; k < 9; k++) { const a = k / 9 * 6.5; o.push(circ(cx - 16 + Math.cos(a) * 17, top + 116 + Math.sin(a) * 17, 3.2, '#a86038', 2)); }
      return o; },
    props: ({ hdR, top }) => { const [x, y] = hdR; const o = [fist(x, y, 15)]; // prayer beads strand hanging from the fist
      for (let k = 0; k < 6; k++) o.push(circ(x + 2, y + 14 + k * 9, 4.4, '#a86038', 2.4));
      o.push(`<path d="M${x},${y + 10} q6,18 0,${14 + 5 * 9}" fill="none" stroke="${INK}" stroke-width="2"/>`);
      return o; } },

  // ---------------------------------------------------------------- RAFI — the hero who learns everything
  { name: 'rafi', label: 'রাফি', form: 'standard', size: 'thin', coat: '#eef0e6', face: 'standard',
    hat: ({ cx, hy }) => { const o = []; // tall black quiff, sharp side part
      o.push(fillPts([[cx - 98, hy - 8], [cx - 70, hy - 84], [cx + 20, hy - 118], [cx + 78, hy - 74], [cx + 96, hy - 22], [cx + 58, hy - 48], [cx + 6, hy - 60], [cx - 44, hy - 50]], HAIRB, 5));
      o.push(brush(cx - 56, hy - 72, cx - 6, hy - 102, cx + 44, hy - 92, 8, { col: '#4a3d2e', tip: .3 }));
      o.push(`<path d="M${cx - 22},${hy - 112} Q${cx + 4},${hy - 70} ${cx - 10},${hy - 24}" fill="none" stroke="${INK}" stroke-width="4"/>`);
      return o; },
    details: ({ cx, top, bot }) => { const o = [], W = 132; // olive vest + cream shirt + teal gamcha scarf knotted at the neck
      o.push(poly([[cx - W * .86, top + 6], [cx - W * .44, top], [cx - W * .16, top + 42], [cx - W * .16, bot - 4], [cx - W * .6, bot - 4]], OLIVE, 5));
      o.push(poly([[cx + W * .86, top + 6], [cx + W * .44, top], [cx + W * .16, top + 42], [cx + W * .16, bot - 4], [cx + W * .6, bot - 4]], OLIVE, 5));
      for (const t of [.5, .68]) o.push(circ(cx - W * .16, top + (bot - top) * t, 4.5, '#c9c2a8', 3));
      o.push(`<path d="M${cx - 34},${top + 4} q26,18 8,34 q-20,12 -6,26" fill="none" stroke="${TEAL}" stroke-width="13"/>`);
      o.push(`<path d="M${cx + 40},${top + 10} l10,26 l-16,6 Z" fill="${TEAL}" stroke="${INK}" stroke-width="3.5"/>`);
      o.push(`<path d="M${cx - 40},${top + 42} q10,7 22,3" fill="none" stroke="${INK}" stroke-width="3"/>`);
      return o; },
    props: ({ hdL }) => { const [x, y] = hdL, o = []; // red khata ledger always under the left arm
      o.push(rect(x - 20, y + 44, 62, 84, REDK, 5, 6));
      o.push(rect(x - 12, y + 56, 46, 60, '#e8ddc2', 3.5, 3));
      for (let k = 0; k < 4; k++) o.push(L(`M${x - 6},${y + 64 + k * 13} l30,0`, 2.6, '#7a6a4a'));
      o.push(L(`M${x - 20},${y + 60} l14,4`, 5, GOLD));
      o.push(fist(x, y + 62, 13));
      return o; } },

  // ---------------------------------------------------------------- BHAGNE — the nephew who gets everything free
  { name: 'bhagne', label: 'ভাগ্নে', form: 'teen', size: 'thin', coat: '#e8e2d2', face: 'smug',
    hat: ({ cx, hy }) => { const o = []; // mustard backwards cap: dome + snap arc above the forehead, brim edges peeking behind
      o.push(`<path d="M${cx - 78},${hy - 34} Q${cx - 62},${hy - 116} ${cx},${hy - 120} Q${cx + 62},${hy - 116} ${cx + 78},${hy - 34} Q${cx},${hy - 58} ${cx - 78},${hy - 34} Z" fill="${MUST}" stroke="${INK}" stroke-width="5"/>`);
      o.push(`<path d="M${cx - 34},${hy - 108} Q${cx},${hy - 130} ${cx + 34},${hy - 108}" fill="none" stroke="${INK}" stroke-width="5"/>`);
      for (let k = -1; k <= 1; k++) o.push(L(`M${cx + k * 18 - 8},${hy - 100} l16,0`, 3.4, shade(MUST, .7)));
      o.push(`<path d="M${cx - 84},${hy - 40} q-18,6 -22,22" fill="none" stroke="${INK}" stroke-width="5"/>`);
      o.push(`<path d="M${cx + 84},${hy - 40} q18,6 22,22" fill="none" stroke="${INK}" stroke-width="5"/>`);
      return o; },
    faceTop: ({ cx, hy }) => { const o = []; // earbud wires + gum bubble at the mouth corner
      o.push(L(`M${cx - 86},${hy + 16} q-6,44 10,84`, 3, '#e8e8e8'));
      o.push(L(`M${cx + 86},${hy + 16} q6,44 -10,84`, 3, '#e8e8e8'));
      o.push(circ(cx - 86, hy + 10, 7, '#f4f4f4', 3), circ(cx + 86, hy + 10, 7, '#f4f4f4', 3));
      o.push(`<circle cx="${cx + 52}" cy="${hy + 74}" r="17" fill="#f2b8c6" fill-opacity=".85" stroke="${INK}" stroke-width="3"/>`);
      return o; },
    details: ({ cx, top, bot }) => { const o = [], W = 126; // red-white striped tee + brown shorts
      for (let k = 0; k < 5; k++) o.push(rect(cx - W * .84, top + 8 + k * ((bot - top - 14) / 5), W * 1.68, (bot - top - 14) / 5, k % 2 ? REDK : '#f3efe6', 0, 0));
      o.push(rect(cx - W * .84, top + 6, W * 1.68, (bot - top - 10), 'none', 4, 2));
      o.push(rect(cx - W * .7, bot - 10, W * 1.4, 26, '#6e5232', 4, 2));
      o.push(L(`M${cx - 30},${bot + 4} l0,-14`, 4, INK), L(`M${cx + 30},${bot + 4} l0,-14`, 4, INK));
      return o; } },

  // ---------------------------------------------------------------- MA — the mother whose warning was laughed off
  { name: 'ma', label: 'মা', form: 'lady', size: 'standard', coat: SARI, face: ['female', 'worried'],
    headBack: ({ cx, hy }) => { const o = []; // dark bun drawn behind the head + grey side hair
      o.push(circ(cx, hy - 128, 40, '#2b2118', 5));
      o.push(fillPts([[cx - 92, hy + 6], [cx - 84, hy - 44], [cx - 54, hy - 66], [cx - 40, hy - 26], [cx - 50, hy + 10]], '#2b2118', 5));
      o.push(fillPts([[cx + 92, hy + 6], [cx + 84, hy - 44], [cx + 54, hy - 66], [cx + 40, hy - 26], [cx + 50, hy + 10]], '#2b2118', 5));
      return o; },
    faceTop: ({ cx, hy }) => { const o = []; // white streak over the bun + red bindi
      o.push(brush(cx - 10, hy - 148, cx + 16, hy - 118, cx + 26, hy - 92, 6, { col: '#e8e4dc', tip: .35 }));
      o.push(circ(cx, hy + 28, 6, REDK, 2.5));
      return o; },
    details: ({ cx, top, bot }) => { const o = [], W = 158; // green tangail sari: white polka dots + red border
      o.push(rect(cx - W * .82, top + 4, W * 1.64, bot - top - 6, SARI, 4, 4));
      for (let r = 0; r < 6; r++) for (let c = 0; c < 5; c++) o.push(circ(cx - W * .62 + c * W * .3 + (r % 2) * W * .14, top + 26 + r * (bot - top - 30) / 6, 5, DOTW, 0));
      o.push(rect(cx - W * .82, bot - 16, W * 1.64, 14, REDK, 3, 0));
      o.push(`<path d="M${cx + W * .5},${top + 10} Q${cx + W * .2},${top + 120} ${cx - W * .58},${bot - 8}" fill="none" stroke="${shade(SARI, .7)}" stroke-width="10"/>`);
      o.push(rect(cx - W * .2, top - 2, W * .4, 30, '#e9dfc8', 4, 4));
      o.push(circ(cx - W * .74, top + 150, 9, BRONZE, 3), circ(cx + W * .74, top + 150, 9, BRONZE, 3));
      return o; } },

  // ---------------------------------------------------------------- PASHI — the neighbour who pays half and makes a partner
  { name: 'pashi', label: 'পাশের দোকানদার', form: 'dad', size: 'standard', coat: '#f1ece0', face: 'standard',
    hat: ({ cx, hy }) => { const o = []; // tall white Karaila topi
      o.push(rect(cx - 62, hy - 116, 124, 78, '#f6f3ea', 5, 8));
      o.push(rect(cx - 70, hy - 46, 140, 16, '#ece7d8', 4.5, 4));
      for (let k = 0; k < 4; k++) o.push(L(`M${cx - 46 + k * 30},${hy - 108} l0,60`, 2.6, '#d8d2c0'));
      o.push(hl(`M${cx - 40},${hy - 106} Q${cx},${hy - 112} ${cx + 36},${hy - 104}`, 5, .5));
      return o; },
    faceTop: ({ cx, hy }) => { const o = []; // thin grey moustache + small brass round specs on the nose
      o.push(circ(cx - 26, hy + 8, 19, 'none', 4.5), circ(cx + 26, hy + 8, 19, 'none', 4.5), L(`M${cx - 7},${hy + 6} Q${cx},${hy} ${cx + 7},${hy + 6}`, 3.5, BRONZE));
      o.push(`<path d="M${cx - 40},${hy + 52} Q${cx},${hy + 44} ${cx + 40},${hy + 52} Q${cx},${hy + 60} ${cx - 40},${hy + 52} Z" fill="#9b9ea4" stroke="${INK}" stroke-width="3.5"/>`);
      return o; },
    details: ({ cx, top, bot }) => { const o = [], W = 140; // grey sleeveless vest over white kurta + measuring tape over the shoulder
      o.push(rect(cx - W * .8, top + 2, W * 1.6, bot - top - 4, '#f3f0e8', 4, 4));
      o.push(poly([[cx - W * .78, top + 6], [cx - W * .3, top + 2], [cx - W * .3, bot - 6], [cx - W * .74, bot - 6]], '#6f747c', 5));
      o.push(poly([[cx + W * .78, top + 6], [cx + W * .3, top + 2], [cx + W * .3, bot - 6], [cx + W * .74, bot - 6]], '#6f747c', 5));
      for (const t of [.4, .56, .72]) o.push(circ(cx + W * .3, top + (bot - top) * t, 4, '#3a3f46', 2.6));
      o.push(`<path d="M${cx - W * .66},${top + 8} Q${cx - W * .1},${top + 60} ${cx + W * .5},${top + 30}" fill="none" stroke="#e2c25a" stroke-width="7"/>`);
      for (let k = 0; k < 5; k++) o.push(circ(cx - W * .5 + k * W * .22, top + 34 + k * 8, 3, '#3a3f46', 1.6));
      return o; },
    props: ({ hdR }) => { const [x, y] = hdR, o = []; // brass tarazu (hand scale) held up
      o.push(pole(x, y - 10, x, y + 74, WOODD, 8));
      o.push(L(`M${x - 46},${y + 30} Q${x - 30},${y + 44} ${x},${y + 40}`, 4, BRONZE), L(`M${x + 46},${y + 30} Q${x + 30},${y + 44} ${x},${y + 40}`, 4, BRONZE));
      o.push(`<path d="M${x - 52},${y + 30} l-6,10 h12 Z" fill="${BRONZE}" stroke="${INK}" stroke-width="3"/>`);
      o.push(`<path d="M${x + 52},${y + 30} l-6,10 h12 Z" fill="${BRONZE}" stroke="${INK}" stroke-width="3"/>`);
      o.push(circ(x, y - 14, 7, BRONZE, 3));
      o.push(fist(x, y + 6, 13));
      return o; } },

  // ---------------------------------------------------------------- TULU — the boy rafi trains at the new shop
  { name: 'tulu', label: 'টুলু', form: 'teen', size: 'thin', coat: '#e9e4d4', face: 'happy',
    hat: ({ cx, hy }) => { const o = []; // tousled tufts
      for (const [dx, dy, r] of [[-58, -66, 26], [-16, -92, 30], [30, -84, 27], [62, -52, 22]]) o.push(circ(cx + dx, hy + dy, r, HAIRB, 4));
      o.push(hl(`M${cx - 40},${hy - 84} Q${cx},${hy - 100} ${cx + 34},${hy - 88}`, 5, .35));
      return o; },
    details: ({ cx, top, bot }) => { const o = [], W = 118; // yellow half-sleeve + brown half-pants + satchel strap
      o.push(rect(cx - W * .8, top + 2, W * 1.6, (bot - top) * .58, '#e2b93c', 4, 4));
      o.push(rect(cx - W * .72, top + (bot - top) * .58, W * 1.44, (bot - top) * .34, '#7c5a36', 4, 3));
      o.push(L(`M${cx - W * .7},${top + 8} L${cx + W * .3},${bot - 14}`, 8, '#4a3a26'));
      o.push(rect(cx + W * .34, bot - 44, 34, 30, '#8a6a44', 4, 3));
      return o; },
    props: ({ hdL }) => { const [x, y] = hdL, o = []; // tin tiffin box in the left hand
      o.push(rect(x - 26, y + 34, 52, 22, TIN, 4.5, 4));
      o.push(rect(x - 26, y + 12, 52, 24, shade(TIN, .82), 4, 4));
      o.push(L(`M${x - 26},${y + 45} l0,-10`, 4, '#6d757c'));
      o.push(pole(x - 14, y + 12, x + 14, y + 12, '#6d757c', 6));
      o.push(fist(x, y + 6, 12));
      return o; } },

  // ---------------------------------------------------------------- KHODDOR — the big credit customer who follows rafi
  { name: 'khoddor', label: 'বড় খদ্দের', form: 'chad', size: 'fat', coat: '#f4f1e8', face: 'happy',
    hat: ({ cx, hy }) => { const o = []; // oiled comb-back hair with a strong sheen
      o.push(fillPts([[cx - 96, hy + 4], [cx - 86, hy - 70], [cx - 30, hy - 106], [cx + 34, hy - 104], [cx + 88, hy - 64], [cx + 96, hy + 4], [cx + 60, hy - 30], [cx, hy - 44], [cx - 60, hy - 30]], '#2e2016', 5));
      o.push(brush(cx - 60, hy - 66, cx, hy - 96, cx + 58, hy - 66, 9, { col: '#7a5a3a', tip: .4 }));
      return o; },
    faceTop: ({ cx, hy }) => { const o = []; // thick brows + gold tooth glint in the grin
      o.push(L(`M${cx - 44},${hy - 6} l30,-6`, 7, HAIRB), L(`M${cx + 14},${hy - 12} l30,6`, 7, HAIRB));
      o.push(rect(cx - 14, hy + 74, 28, 10, GOLD, 2.5, 2));
      return o; },
    details: ({ cx, top, bot }) => { const o = [], W = 148; // white punjabi + gold chain
      o.push(rect(cx - W * .8, top + 2, W * 1.6, bot - top - 4, '#f6f3ec', 4, 4));
      o.push(L(`M${cx},${top + 2} l0,${(bot - top) * .3}`, 3.4, '#d8d2c2'));
      o.push(`<path d="M${cx - W * .3},${top + 8} Q${cx},${top + 66} ${cx + W * .3},${top + 8}" fill="none" stroke="${GOLD}" stroke-width="6"/>`);
      o.push(circ(cx, top + 66, 8, GOLD, 3));
      o.push(L(`M${cx - W * .8},${top + 44} l0,${(bot - top) * .5}`, 3, '#d8d2c2'), L(`M${cx + W * .8},${top + 44} l0,${(bot - top) * .5}`, 3, '#d8d2c2'));
      return o; },
    props: ({ hdL }) => { const [x, y] = hdL, o = []; // jute bag of sweets
      o.push(poly([[x - 30, y + 30], [x + 30, y + 30], [x + 24, y + 86], [x - 24, y + 86]], JUTE, 5));
      for (let k = 0; k < 3; k++) o.push(L(`M${x - 22 + k * 8},${y + 40} l8,36`, 2.4, shade(JUTE, .7)));
      o.push(circ(x - 8, y + 26, 7, '#e0453a', 3), circ(x + 6, y + 24, 6, '#3fae5a', 3));
      o.push(`<path d="M${x - 14},${y + 30} Q${x - 6},${y + 14} ${x + 14},${y + 26}" fill="none" stroke="${INK}" stroke-width="4"/>`);
      o.push(fist(x, y + 6, 13));
      return o; } },
];
