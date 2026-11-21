// SHEET 16 — SWEET SHOP WORLD (Law 11: "Learn to make people depend on you")
// Five original characters drawn for THIS film. Signatures: rafi = apron + sweet box;
// chacha = moustache + belly + maroon waistcoat; ma = sari + bun; nephew = backwards cap + phone;
// dokandar = white banyan + lungi + gamcha.
import { INK, P, L, ell, f1, smooth, brush, shade, tint, GOLD, GOLDL, STEEL, BRONZE, WOOD, WOODD, CREAM, RED, fillPts, poly, rect, circ, hl, pole, fist, cloud } from '../castkit.mjs';

const MAROON = '#7a2434', GREEN = '#2f6a3f', SKYB = '#3a5a8c', TURM = '#e2a13c', c23 = '#c23d33';

export const TITLE = 'Cast sheet 16: Sweet shop world (Law 11)';

export const CAST = [
  // ---------------------------------------------------------------- RAFI — the apprentice hero
  { name: 'rafi', label: 'রাফি', form: 'standard', size: 'thin', coat: '#eef2f4', face: 'standard',
    outfit: 'baker', outfitPal: { a: '#f7f3e8', b: SKYB, c: MAROON },
    hat: ({ cx, hy }) => { const o = []; // neat side-parted black hair
      o.push(fillPts([[cx - 100, hy - 12], [cx - 60, hy - 92], [cx + 40, hy - 96], [cx + 98, hy - 30], [cx + 74, hy - 44], [cx + 10, hy - 58], [cx - 40, hy - 52]], '#1d1712', 5));
      o.push(hl(`M${cx - 58},${hy - 74} Q${cx - 20},${hy - 88} ${cx + 30},${hy - 84}`, 5, .3));
      o.push(`<path d="M${cx - 8},${hy - 92} Q${cx + 6},${hy - 60} ${cx - 2},${hy - 20}" fill="none" stroke="${INK}" stroke-width="4"/>`);
      return o; },
    props: ({ hdL }) => { const o = []; // his signature: a stack of two sweet boxes in the left hand
      const bx = hdL[0] - 34, by = hdL[1] - 46;
      o.push(rect(bx - 44, by, 88, 34, MAROON, 5, 3));
      o.push(rect(bx - 44, by - 30, 88, 30, c23, 5, 3));
      o.push(rect(bx - 44, by - 12, 88, 12, GOLD, 3, 0));
      o.push(hl(`M${bx - 36},${by + 5} L${bx - 36},${by + 26}`, 4, .5));
      o.push(fist(hdL[0], hdL[1], 13));
      return o; },
    details: ({ cx, top, bot }) => [ // pencil in the bib pocket (the baker outfit draws the apron)
      rect(cx + 52, top + 150, 12, 34, TURM, 3.5, 3),
    ] },
  // ---------------------------------------------------------------- CHACHA — the sweet shop owner
  { name: 'chacha', label: 'মালিক চাচা', form: 'standard', size: 'fat', coat: '#efe6d2', face: 'proud',
    faceTop: ({ cx, hy }) => { const o = []; // the big swept moustache — his signature (sits ABOVE the mouth: CB rule)
      o.push(`<path d="M${cx - 58},${hy + 34} Q${cx - 28},${hy + 18} ${cx},${hy + 28} Q${cx + 28},${hy + 18} ${cx + 58},${hy + 34} Q${cx + 28},${hy + 44} ${cx},${hy + 38} Q${cx - 28},${hy + 44} ${cx - 58},${hy + 34} Z" fill="#241d16" stroke="${INK}" stroke-width="5"/>`);
      o.push(`<path d="M${cx - 36},${hy + 29} Q${cx - 16},${hy + 23} ${cx - 2},${hy + 30}" fill="none" stroke="#4a4038" stroke-width="3"/>`);
      return o; },
    headBack: ({ cx, hy }) => { const o = []; // bald top, thick side + back hair
      o.push(fillPts([[cx - 96, hy + 6], [cx - 88, hy - 40], [cx - 62, hy - 62], [cx - 40, hy - 30], [cx - 52, hy + 10]], '#241d16', 5));
      o.push(fillPts([[cx + 96, hy + 6], [cx + 88, hy - 40], [cx + 62, hy - 62], [cx + 40, hy - 30], [cx + 52, hy + 10]], '#241d16', 5));
      o.push(fillPts([[cx - 70, hy + 4], [cx + 70, hy + 4], [cx + 66, hy + 58], [cx - 66, hy + 58]], '#241d16', 5));
      return o; },
    dress: S => { const d0 = S.details; S.details = c => { const o = d0 ? d0(c) : []; // cream kurta + maroon waistcoat, drawn on the raw rig ctx
      const cx = c.cx, top = c.bodyTop ?? 333, bot = c.bodyBot ?? 640, W = c.wB || c.w || 150;
      o.push(`<path d="M${cx - W * .3},${top + 4} L${cx - W * .3},${bot - 6} M${cx + W * .3},${top + 4} L${cx + W * .3},${bot - 6}" stroke="${INK}" stroke-width="3.5" opacity=".5"/>`); // kurta placket seams
      o.push(poly([[cx - W * .96, top + 10], [cx - W * .56, top], [cx - W * .2, top + 46], [cx - W * .2, bot - 10], [cx - W * .64, bot - 10]], MAROON, 5)); // waistcoat left panel
      o.push(poly([[cx + W * .96, top + 10], [cx + W * .56, top], [cx + W * .2, top + 46], [cx + W * .2, bot - 10], [cx + W * .64, bot - 10]], MAROON, 5)); // right panel
      o.push(rect(cx - W * .64, bot - 16, W * 1.28, 12, MAROON, 4, 2)); // hem band
      o.push(`<path d="M${cx - W * .2},${top + 46} L${cx},${top + 76} L${cx + W * .2},${top + 46}" fill="none" stroke="${INK}" stroke-width="4"/>`); // V neck
      for (const t of [.4, .58, .76]) o.push(`<circle cx="${cx - W * .2}" cy="${top + (bot - top) * t}" r="5" fill="${GOLD}" stroke="${INK}" stroke-width="3"/>`);
      o.push(`<path d="M${cx - W * .58},${top + 40} Q${cx},${top + 132} ${cx + W * .58},${top + 40}" fill="none" stroke="${GOLD}" stroke-width="6"/><circle cx="${cx - W * .58}" cy="${top + 40}" r="7" fill="${GOLD}" stroke="${INK}" stroke-width="3"/><circle cx="${cx + W * .58}" cy="${top + 40}" r="7" fill="${GOLD}" stroke="${INK}" stroke-width="3"/>`); // gold chain
      o.push(hl(`M${cx - W * .9},${top + 16} L${cx - W * .66},${top + 88}`, 5, .3));
      return o; }; },
    props: ({ hdR }) => [pole(hdR[0] - 8, hdR[1] + 4, hdR[0] + 18, hdR[1] - 116, WOODD, 9), fist(hdR[0], hdR[1], 14)], // walking stick at rest
  },
  // ---------------------------------------------------------------- MA — Rafi's mother
  { name: 'ma', label: 'রাফির মা', form: 'lady', size: 'standard', coat: GREEN, face: ['female', 'sweetSmile'],   // calm wise mother; the old 'sassy' meme drew text on the face (CB: no drawn text)
    outfit: 'sari', outfitPal: { a: GREEN, b: '#c23d33', c: GOLD },
    faceTop: ({ cx, hy }) => { const o = []; // centre-parted hair + bindi
      o.push(fillPts([[cx - 98, hy - 6], [cx - 76, hy - 84], [cx - 6, hy - 96], [cx + 78, hy - 84], [cx + 98, hy - 6], [cx + 74, hy - 30], [cx + 8, hy - 44], [cx - 8, hy - 44], [cx - 74, hy - 30]], '#241d16', 5));
      o.push(`<path d="M${cx},${hy - 96} L${cx},${hy - 44}" stroke="${INK}" stroke-width="4"/>`);
      o.push(`<circle cx="${cx}" cy="${hy - 34}" r="6" fill="${MAROON}"/>`);
      return o; },
    headBack: ({ cx, hy }) => [ // the bun behind, with a maroon flower
      circ(cx, hy - 116, 34, '#241d16', 5), circ(cx + 30, hy - 96, 13, MAROON, 4), circ(cx - 22, hy - 130, 9, c23, 3),
      fillPts([[cx - 88, hy - 10], [cx - 84, hy - 60], [cx - 60, hy - 100], [cx - 34, hy - 118], [cx - 44, hy - 70], [cx - 52, hy - 20]], '#241d16', 5),
      fillPts([[cx + 88, hy - 10], [cx + 84, hy - 60], [cx + 60, hy - 100], [cx + 34, hy - 118], [cx + 44, hy - 70], [cx + 52, hy - 20]], '#241d16', 5)],
    props: ({ hdR }) => [ // her brass ladle at rest
      pole(hdR[0] - 4, hdR[1] + 6, hdR[0] + 22, hdR[1] - 78, '#b08a3f', 8),
      `<path d="M${hdR[0] + 10},${hdR[1] - 78} q14,-16 26,0 q-4,22 -26,14 Z" fill="#c9a04a" stroke="${INK}" stroke-width="4"/>`,
      fist(hdR[0], hdR[1], 13)] },
  // ---------------------------------------------------------------- NEPHEW — the owner's spoiled nephew
  { name: 'nephew', label: 'ভাগ্নে', form: 'kid', size: 'standard', coat: '#e2b13c', face: 'smug',   // spoiled smirk, not the troll meme (generic internet face)
    outfit: 'poloClassic', outfitPal: { a: '#e2b13c', b: SKYB, c: MAROON },
    hat: ({ cx, hy }) => { const o = []; // backwards cap — his signature
      o.push(fillPts([[cx - 88, hy - 34], [cx - 60, hy - 92], [cx + 20, hy - 96], [cx + 84, hy - 48], [cx + 88, hy - 26], [cx + 44, hy - 34], [cx - 40, hy - 30]], c23, 5));
      o.push(rect(cx + 62, hy - 44, 44, 16, '#a82820', 5, 6));
      o.push(`<circle cx="${cx + 6}" cy="${hy - 78}" r="9" fill="${GOLD}" stroke="${INK}" stroke-width="4"/>`);
      o.push(hl(`M${cx - 66},${hy - 58} Q${cx - 30},${hy - 88} ${cx + 14},${hy - 86}`, 5, .4));
      return o; },
    props: ({ hdR }) => { const o = []; // the phone he never puts down
      o.push(rect(hdR[0] - 16, hdR[1] - 44, 32, 52, '#24222c', 5, 5));
      o.push(rect(hdR[0] - 11, hdR[1] - 39, 22, 38, '#7ec8e8', 2.5, 3));
      o.push(hl(`M${hdR[0] - 8},${hdR[1] - 34} L${hdR[0] - 8},${hdR[1] - 12}`, 3, .6));
      o.push(fist(hdR[0], hdR[1], 12));
      return o; } },
  // ---------------------------------------------------------------- DOKANDAR — the neighbour shop owner
  { name: 'dokandar', label: 'পাশের দোকানের মালিক', form: 'standard', size: 'standard', coat: '#c9bda8', face: 'standard',
    faceTop: ({ cx, hy }) => { const o = []; // thick black side hair + hairline (a fit 45-year-old)
      o.push(fillPts([[cx - 96, hy + 10], [cx - 90, hy - 44], [cx - 58, hy - 84], [cx - 20, hy - 96], [cx - 34, hy - 52], [cx - 44, hy - 8]], '#241d16', 5));
      o.push(fillPts([[cx + 96, hy + 10], [cx + 90, hy - 44], [cx + 58, hy - 84], [cx + 20, hy - 96], [cx + 34, hy - 52], [cx + 44, hy - 8]], '#241d16', 5));
      o.push(`<path d="M${cx - 44},${hy - 74} Q${cx},${hy - 88} ${cx + 44},${hy - 74}" fill="none" stroke="#241d16" stroke-width="10"/>`);
      return o; },
    longCloth: { style: 'plain', length: 'ankle', col: '#3a6a8f', hem: '#24425a', hemW: 16, folds: 3,
      pattern: ({ cx, y0, side, view }) => { const o = []; if (side || view === 'back') return o; // lungi checks
        for (let i = -3; i <= 3; i++) o.push(`<rect x="${cx + i * 64 - 8}" y="${y0}" width="16" height="520" fill="#24425a" opacity=".42"/>`);
        for (let j = 0; j < 6; j++) o.push(`<rect x="${cx - 240}" y="${y0 + 40 + j * 84}" width="480" height="14" fill="#24425a" opacity=".42"/>`);
        return o; } },
    details: ({ cx, top, bot }) => { const o = []; // white banyan vest on the earth-toned kurta (standard body: half width ~104)
      const W = 104, hem = bot - 8, sh = top + 8, nk = top + 40;
      o.push(poly([[cx - W * .96, sh], [cx - W * .58, sh - 6], [cx - W * .17, nk], [cx - W * .17, hem], [cx - W * .64, hem]], '#f6f4ee', 5));
      o.push(poly([[cx + W * .96, sh], [cx + W * .58, sh - 6], [cx + W * .17, nk], [cx + W * .17, hem], [cx + W * .64, hem]], '#f6f4ee', 5));
      o.push(rect(cx - W * .64, hem - 5, W * 1.28, 10, '#f6f4ee', 4, 2));
      o.push(`<path d="M${cx - W * .17},${nk} L${cx},${top + 68} L${cx + W * .17},${nk}" fill="none" stroke="${INK}" stroke-width="4"/>`);
      for (const t of [.42, .6, .78]) o.push(`<circle cx="${cx}" cy="${top + (bot - top) * t}" r="4.5" fill="${STEEL}" stroke="${INK}" stroke-width="2.5"/>`);
      o.push(hl(`M${cx - W * .9},${sh + 8} L${cx - W * .68},${top + 86}`, 5, .4));
      return o; },
    props: ({ cx, top, bot, shR }) => { const o = []; // gamcha: white towel over the right shoulder, thin red border, red checks
      const sx = shR[0], sy = top + 8;
      o.push(fillPts([[sx - 14, sy - 6], [sx + 78, sy + 26], [sx + 62, sy + 96], [sx - 24, sy + 66]], '#f7f3e6', 5));
      o.push(`<path d="M${sx + 40},${sy + 40} L${sx + 74},${sy + 150} L${sx + 30},${sy + 168} L${sx + 12},${sy + 52} Z" fill="#f7f3e6" stroke="${INK}" stroke-width="5"/>`);
      o.push(`<path d="M${sx + 30},${sy + 168} L${sx + 74},${sy + 150}" stroke="${c23}" stroke-width="7" fill="none"/>`);
      for (let j = 0; j < 4; j++) for (let i = 0; i < 3; i++) o.push(`<rect x="${sx - 8 + i * 26}" y="${sy + 14 + j * 16}" width="13" height="7" fill="${c23}" opacity=".75"/>`);
      for (let j = 0; j < 5; j++) o.push(`<rect x="${sx + 22 + (j % 2) * 18}" y="${sy + 70 + j * 18}" width="16" height="8" fill="${c23}" opacity=".75"/>`);
      o.push(hl(`M${sx - 6},${sy - 2} L${sx - 14},${sy + 54}`, 4, .45));
      return o; } },
];
