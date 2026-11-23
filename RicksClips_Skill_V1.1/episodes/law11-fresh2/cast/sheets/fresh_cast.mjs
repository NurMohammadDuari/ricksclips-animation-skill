// fresh_cast.mjs — the seven ORIGINAL characters of Law 11 (fresh2 rebuild, 2026-11-23).
// Built on the locked castkit (castkit.mjs): bodies + meme faces + the head-space hooks.
// Every signature is drawn for THIS film only. Style: ink #2a1a1f outlines, flat fills,
// one light-left gradient, white skin, ink-stick limbs (STYLE_DNA).
//
// FIXES BAKED IN (validated on the previous rebuild, kept verbatim):
//   kaka  specs   : lens circles at cy = hy-16 (ON the eye line; the old hy+8 hung them on the chin)
//   pashi moustache: arcs at hy+18 (at the mouth; the old hy+52 sat on the chest)
//   rafi  quiff   : bottom edge hy-56..-58 (the old -30 covered the meme eyes at hy-18..-34)
//   details width : B carries no `w`, so every details hook derives it from the shoulders.
import { fillPts, poly, rect, circ, hl, cloud, bands, INK, GOLD, SILVER, BLACK, f1 } from '../castkit.mjs';

const TEAL = '#2f6a5f', TEALD = '#22504a', OLIVE = '#6b7340', CREAMS = '#f3efe6', MUSTARD = '#d1a03c',
      MRED = '#c23d33', GREYK = '#8a8f98', JUTE = '#c8a468';
const W = (cx, shL, shR) => Math.max(Math.abs(shR[0] - cx), Math.abs(shL[0] - cx)) + 22;   // half width of the torso

// ---------------------------------------------------------------- kaka — the uncle
const kaka = {
  name: 'kaka', label: 'কাকা', form: 'dad', coat: TEAL, face: ['elder', 'sweetSmile'],
  hat: ({ cx, hy }) =>
    // white embroidered taqi cap — a shallow dome sitting HIGH on the head
    fillPts([[cx - 62, hy - 46], [cx - 52, hy - 84], [cx - 20, hy - 98], [cx + 24, hy - 96], [cx + 54, hy - 80], [cx + 62, hy - 44], [cx + 58, hy - 40], [cx - 58, hy - 40]], CREAMS, 6) +
    `<path d="M${f1(cx - 40)},${f1(hy - 74)} Q${f1(cx)},${f1(hy - 88)} ${f1(cx + 40)},${f1(hy - 74)}" fill="none" stroke="${GOLD}" stroke-width="3.5" stroke-opacity=".8"/>` +
    circ(cx - 18, hy - 62, 3.4, GOLD, 0) + circ(cx + 16, hy - 60, 3.4, GOLD, 0) + circ(cx, hy - 80, 3.4, GOLD, 0),
  faceTop: ({ cx, hy }) =>
    // silver round spectacles ON the eye line (cy = hy-16), bridge + thin temples
    `<circle cx="${f1(cx - 21)}" cy="${f1(hy - 16)}" r="26" fill="#eef3f7" fill-opacity=".26" stroke="${SILVER}" stroke-width="7"/>` +
    `<circle cx="${f1(cx + 21)}" cy="${f1(hy - 16)}" r="26" fill="#eef3f7" fill-opacity=".26" stroke="${SILVER}" stroke-width="7"/>` +
    `<path d="M${f1(cx - 6)},${f1(hy - 18)} Q${f1(cx)},${f1(hy - 22)} ${f1(cx + 6)},${f1(hy - 18)}" fill="none" stroke="${SILVER}" stroke-width="6"/>` +
    `<path d="M${f1(cx - 47)},${f1(hy - 18)} L${f1(cx - 78)},${f1(hy - 26)} M${f1(cx + 47)},${f1(hy - 18)} L${f1(cx + 78)},${f1(hy - 26)}" stroke="${SILVER}" stroke-width="6" fill="none"/>`,
  details: ({ cx, top, bot, shL, shR }) => {
    const w = W(cx, shL, shR);
    // teal kabuli vest: darker front panels + gold frogging over the teal coat
    return rect(cx - w * .62, top + 6, w * .5, (bot - top) * .86, TEALD, 5, 8) +
      rect(cx + w * .12, top + 6, w * .5, (bot - top) * .86, TEALD, 5, 8) +
      `<path d="M${f1(cx - 16)},${f1(top + 14)} L${f1(cx - 6)},${f1(top + (bot - top) * .4)} M${f1(cx + 16)},${f1(top + 14)} L${f1(cx + 6)},${f1(top + (bot - top) * .4)}" stroke="${GOLD}" stroke-width="4" fill="none" stroke-opacity=".85"/>`;
  },
  props: ({ cx, bot }) => {
    // prayer beads loop hanging at the chest
    let out = '';
    for (let k = 0; k < 11; k++) { const a = Math.PI * (.15 + .7 * k / 10); out += circ(cx + 34 - 30 * Math.cos(a), bot - 92 + 26 * Math.sin(a), 4.6, '#8a5a2e', 3); }
    return out;
  },
};

// ---------------------------------------------------------------- rafi — the hero
const rafi = {
  name: 'rafi', label: 'রাফি', form: 'standard', coat: CREAMS, face: 'standard',
  faceTop: ({ cx, hy }) =>
    // tall black quiff swept right — bottom edge hy-56, NEVER over the eyes (fix)
    fillPts([[cx - 50, hy - 58], [cx - 44, hy - 78], [cx - 20, hy - 98], [cx + 12, hy - 106], [cx + 46, hy - 94], [cx + 58, hy - 66], [cx + 44, hy - 56], [cx + 26, hy - 70], [cx + 2, hy - 76], [cx - 24, hy - 70]], BLACK, 5) +
    hl(`M${f1(cx - 30)},${f1(hy - 82)} Q${f1(cx)},${f1(hy - 96)} ${f1(cx + 34)},${f1(hy - 86)}`, 6, .35),
  details: ({ cx, top, bot, shL, shR }) => {
    const w = W(cx, shL, shR);
    // cream kurta + olive vest + teal gamcha at the throat
    return rect(cx - w * .6, top + 8, w * 1.2, (bot - top) * .52, OLIVE, 5, 8) +
      `<path d="M${f1(cx - w * .34)},${f1(top + 2)} q${f1(w * .18)},${f1(26)} ${f1(w * .05)},${f1(34)} l${f1(-w * .3)},0 q${f1(-w * .16)},${f1(-14)} ${f1(-w * .05)},${f1(-34)} Z" fill="#2f6a5f" stroke="${INK}" stroke-width="5"/>` +
      hl(`M${f1(cx - w * .3)},${f1(top + 6)} q${f1(w * .3)},${f1(4)} ${f1(w * .52)},${f1(2)}`, 7, .5);
  },
  props: ({ cx, bot }) =>
    // the red khata (ledger) held under the left arm
    rect(cx - 92, bot - 150, 26, 78, MRED, 5, 3) + `<path d="M${f1(cx - 86)},${f1(bot - 138)} L${f1(cx - 72)},${f1(bot - 138)}" stroke="${CREAMS}" stroke-width="4"/>`,
};

// ---------------------------------------------------------------- bhagne — the nephew
const bhagne = {
  name: 'bhagne', label: 'ভাগ্নে', form: 'kid', coat: CREAMS, face: ['female', 'smug'],
  hat: ({ cx, hy }) =>
    // mustard cap worn BACKWARDS: dome high, brim sticking out behind
    fillPts([[cx - 56, hy - 40], [cx - 50, hy - 78], [cx - 18, hy - 94], [cx + 26, hy - 92], [cx + 52, hy - 72], [cx + 56, hy - 38], [cx - 56, hy - 38]], MUSTARD, 6) +
    rect(cx + 50, hy - 74, 40, 14, '#b8873c', 5, 6),
  faceTop: ({ cx, hy }) =>
    // earbud wire down from the left ear (the kid who was handed everything)
    `<path d="M${f1(cx + 62)},${f1(hy - 4)} q6,40 -4,78" fill="none" stroke="${INK}" stroke-width="4" stroke-opacity=".85"/>` + circ(cx + 57, hy + 76, 6, '#2f2f38', 3),
  details: ({ cx, top, bot, shL, shR }) => {
    const w = W(cx, shL, shR);
    // red-white striped tee
    return bands(cx - w * .62, cx + w * .62, top + 10, top + 10 + (bot - top) * .62, [CREAMS, MRED, CREAMS, MRED, CREAMS]) +
      `<path d="M${f1(cx - w * .62)},${f1(top + 10)} h${f1(w * 1.24)}" stroke="${INK}" stroke-width="5"/>` + rect(cx - w * .62, top + 10, w * 1.24, (bot - top) * .62, 'none', 5, 6);
  },
};

// ---------------------------------------------------------------- ma — the mother
const ma = {
  name: 'ma', label: 'মা', form: 'lady', coat: '#3f7a4a', face: ['female', 'sassy'],
  longCloth: { style: 'plain', length: 'ankle', col: '#3f7a4a', hem: '#2f5f3a', folds: 2, flare: 1.15 },
  headBack: ({ cx, hy }) =>
    // bun with the white streak, behind the head
    circ(cx - 52, hy - 66, 27, '#2b2320', 5) + `<path d="M${f1(cx - 62)},${f1(hy - 80)} q10,-6 20,4" stroke="${CREAMS}" stroke-width="5" fill="none" stroke-opacity=".9"/>`,
  faceTop: ({ cx, hy }) =>
    // red bindi on the forehead
    circ(cx, hy - 46, 6.4, MRED, 3),
  details: ({ cx, top, bot, shL, shR }) => {
    const w = W(cx, shL, shR);
    // green polka-dot sari body + pallu over the left shoulder
    let dots = '';
    for (let r = 0; r < 4; r++) for (let c = 0; c < 4; c++) dots += circ(cx - w * .5 + c * w * .33 + (r % 2) * w * .14, top + 26 + r * 34, 5.5, CREAMS, 0);
    return dots + `<path d="M${f1(cx - w * .5)},${f1(bot - 24)} L${f1(cx + w * .3)},${f1(top + 8)}" stroke="#2f5f3a" stroke-width="26" stroke-opacity=".55" fill="none"/>` +
      `<path d="M${f1(cx - w * .5)},${f1(bot - 24)} L${f1(cx + w * .3)},${f1(top + 8)}" stroke="${GOLD}" stroke-width="3" stroke-opacity=".5" fill="none"/>`;
  },
};

// ---------------------------------------------------------------- pashi — the neighbouring shopkeeper
const pashi = {
  name: 'pashi', label: 'পাশি', form: 'dad', coat: GREYK, face: ['elder', 'suspicious'],
  hat: ({ cx, hy }) =>
    // tall white Karaila topi — the silhouette signature (sits ON the head, band at the hairline)
    rect(cx - 32, hy - 124, 64, 74, CREAMS, 6, 8) + rect(cx - 36, hy - 58, 72, 15, '#e4e0d4', 5, 4) +
    `<path d="M${f1(cx - 20)},${f1(hy - 116)} L${f1(cx - 20)},${f1(hy - 62)} M${f1(cx + 2)},${f1(hy - 118)} L${f1(cx + 2)},${f1(hy - 62)} M${f1(cx + 24)},${f1(hy - 114)} L${f1(cx + 24)},${f1(hy - 62)}" stroke="${INK}" stroke-opacity=".22" stroke-width="4" fill="none"/>`,
  faceTop: ({ cx, hy }) =>
    // thin grey moustache AT the mouth (hy+18 — fix), two soft arcs
    `<path d="M${f1(cx - 26)},${f1(hy + 18)} q12,-9 24,0 M${f1(cx + 2)},${f1(hy + 18)} q12,-9 24,0" fill="none" stroke="#9aa0a6" stroke-width="7" stroke-linecap="round"/>`,
  details: ({ cx, top, bot, shL, shR }) => {
    const w = W(cx, shL, shR);
    // measuring tape worn like a sash + grey waistcoat line
    return `<path d="M${f1(cx - w * .55)},${f1(top + (bot - top) * .78)} L${f1(cx + w * .55)},${f1(top + 14)}" stroke="#e0b23c" stroke-width="16" stroke-opacity=".9"/>` +
      `<path d="M${f1(cx - w * .55)},${f1(top + (bot - top) * .78)} L${f1(cx + w * .55)},${f1(top + 14)}" stroke="${INK}" stroke-opacity=".25" stroke-width="3" fill="none"/>` +
      rect(cx - w * .6, top + 10, w * 1.2, (bot - top) * .5, 'none', 5, 8);
  },
};

// ---------------------------------------------------------------- tulu — the boy rafi trains
const tulu = {
  name: 'tulu', label: 'টুলু', form: 'kid', coat: '#e0b23c', face: ['baby', 'curious'],
  headBack: ({ cx, hy }) =>
    // tousled tufts
    cloud([[cx - 44, hy - 74, 20], [cx - 12, hy - 90, 22], [cx + 24, hy - 84, 21], [cx + 48, hy - 64, 17]], BLACK, 4.5),
  details: ({ cx, top, bot, shL, shR }) => {
    const w = W(cx, shL, shR);
    // yellow tee, white collar band
    return rect(cx - w * .62, top + 10, w * 1.24, (bot - top) * .58, '#e0b23c', 5, 6) +
      `<path d="M${f1(cx - w * .4)},${f1(top + 10)} q${f1(w * .4)},${f1(16)} ${f1(w * .8)},0" fill="none" stroke="${CREAMS}" stroke-width="9"/>`;
  },
};

// ---------------------------------------------------------------- khoddor — the big credit customer
const khoddor = {
  name: 'khoddor', label: 'খদ্দের', form: 'dad', size: 'fat', coat: CREAMS, face: 'proud',
  faceTop: ({ cx, hy }) =>
    // oiled comb-back hair, hard shine
    fillPts([[cx - 60, hy - 34], [cx - 56, hy - 72], [cx - 26, hy - 96], [cx + 18, hy - 98], [cx + 50, hy - 80], [cx + 58, hy - 48], [cx + 40, hy - 56], [cx - 10, hy - 62], [cx - 42, hy - 50]], BLACK, 5) +
    hl(`M${f1(cx - 34)},${f1(hy - 86)} Q${f1(cx + 6)},${f1(hy - 92)} ${f1(cx + 40)},${f1(hy - 72)}`, 7, .5),
  details: ({ cx, top, bot, shL, shR }) => {
    const w = W(cx, shL, shR);
    // white punjabi + gold chain
    let chain = '';
    for (let k = 0; k < 9; k++) { const a = Math.PI * (.2 + .6 * k / 8); chain += circ(cx + 26 * Math.cos(a), top + 16 + 20 * Math.sin(a), 5, GOLD, 3); }
    return rect(cx - w * .62, top + 8, w * 1.24, (bot - top) * .9, CREAMS, 5, 8) + `<path d="M${f1(cx)},${f1(top + 8)} v${f1((bot - top) * .9)}" stroke="${INK}" stroke-opacity=".3" stroke-width="3"/>` + chain;
  },
  props: ({ cx, bot }) =>
    // jute sweets bag in the left fist
    poly([[cx - 86, bot - 160], [cx - 40, bot - 160], [cx - 34, bot - 96], [cx - 92, bot - 96]], JUTE, 5) + `<path d="M${f1(cx - 78)},${f1(bot - 160)} l6,-14 M${f1(cx - 50)},${f1(bot - 160)} l-6,-14" stroke="${INK}" stroke-width="5" fill="none"/>`,
};

export const CAST = [kaka, rafi, bhagne, ma, pashi, tulu, khoddor];
export const TITLE = '৪৮ শক্তির নিয়ম — নিয়ম ১১ (fresh2)';
