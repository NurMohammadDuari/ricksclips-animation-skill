// SHEET 17 — BAZAAR EXTRAS (Law 11 world: the people around the sweet shop)
// Three original characters drawn for the deep-scene pass. Signatures:
// khoddeder = bald elder + white stubble + checked lungi + net bag of limes (the loyal customer);
// khoddeder2 = younger customer, green punjabi, cloth shoulder bag;
// bepari = supplier/creditor, turban headwrap + blue kurta + rope coil on the shoulder.
import { INK, GOLD, CREAM, fillPts, poly, rect, circ, hl, fist } from '../castkit.mjs';

const c23 = '#c23d33', SKIN = '#c8a27a', SKIND = '#b08a5e';

export const TITLE = 'Cast sheet 17: Bazaar extras (Law 11)';

export const CAST = [
  // ------------------------------------------------ KHODDEDER — the loyal old customer
  { name: 'khoddeder', label: 'খদ্দের দাদু', form: 'standard', size: 'fat', coat: SKIN, face: 'standard',
    faceTop: ({ cx, hy }) => { const o = []; // bald crown, white hair rim, white stubble beard
      o.push(fillPts([[cx - 92, hy + 18], [cx - 86, hy - 30], [cx - 58, hy - 58], [cx - 44, hy - 24], [cx - 56, hy + 14]], '#e8e2d4', 5));
      o.push(fillPts([[cx + 92, hy + 18], [cx + 86, hy - 30], [cx + 58, hy - 58], [cx + 44, hy - 24], [cx + 56, hy + 14]], '#e8e2d4', 5));
      o.push(`<path d="M${cx - 56},${hy + 22} Q${cx - 44},${hy + 66} ${cx},${hy + 70} Q${cx + 44},${hy + 66} ${cx + 56},${hy + 22} Q${cx + 44},${hy + 52} ${cx},${hy + 55} Q${cx - 44},${hy + 52} ${cx - 56},${hy + 22} Z" fill="#e8e2d4" stroke="${INK}" stroke-width="4" opacity=".95"/>`);
      o.push(`<path d="M${cx - 40},${hy + 30} Q${cx - 26},${hy + 44} ${cx - 8},${hy + 46} M${cx + 40},${hy + 30} Q${cx + 26},${hy + 44} ${cx + 8},${hy + 46}" stroke="#e8e2d4" stroke-width="3" fill="none" opacity=".8"/>`);
      return o; },
    longCloth: { style: 'plain', length: 'ankle', col: '#3a6a5f', hem: '#24443c', hemW: 14, folds: 3,
      pattern: ({ cx, y0, side, view }) => { const o = []; if (side || view === 'back') return o; // green checks
        for (let i = -3; i <= 3; i++) o.push(`<rect x="${cx + i * 64 - 7}" y="${y0}" width="14" height="520" fill="#24443c" opacity=".4"/>`);
        for (let j = 0; j < 6; j++) o.push(`<rect x="${cx - 240}" y="${y0 + 44 + j * 84}" width="480" height="13" fill="#24443c" opacity=".4"/>`);
        return o; } },
    details: ({ cx, top, bot }) => { const o = []; // bare chest: collarbones + a gamcha strip over the left shoulder
      const W = 104;
      o.push(`<path d="M${cx - W * .3},${top + 26} L${cx - W * .12},${top + 44} M${cx + W * .3},${top + 26} L${cx + W * .12},${top + 44}" fill="none" stroke="${SKIND}" stroke-width="4"/>`);
      o.push(`<path d="M${cx - W * .52},${top + 70} Q${cx - W * .2},${top + 96} ${cx - W * .05},${top + 120}" fill="none" stroke="${SKIND}" stroke-width="3.5" opacity=".7"/>`);
      o.push(rect(cx - W * .78, top + 4, W * .3, 120, '#f7f3e6', 4, 4)); // gamcha over the shoulder
      o.push(`<path d="M${cx - W * .78},${top + 104} L${cx - W * .48},${top + 104}" stroke="${c23}" stroke-width="6"/>`);
      return o; },
    props: ({ hdL }) => { const o = []; // his signature: the net bag of limes (বাজারের থলে)
      const bx = hdL[0] - 8, by = hdL[1] + 56;
      o.push(`<path d="M${hdL[0] - 2},${hdL[1] - 4} L${bx - 34},${by - 34} M${hdL[0] + 2},${hdL[1] - 2} L${bx + 34},${by - 30}" stroke="${INK}" stroke-width="5"/>`);
      o.push(`<ellipse cx="${bx}" cy="${by}" rx="40" ry="34" fill="#bfe3ef" fill-opacity=".3" stroke="${INK}" stroke-width="5"/>`);
      for (const [dx, dy, r] of [[-14, -6, 12], [10, -10, 11], [0, 10, 12], [20, 6, 10], [-22, 8, 9]]) o.push(circ(bx + dx, by + dy, r, '#e2c23c', 4));
      o.push(`<path d="M${bx - 30},${by - 16} L${bx + 8},${by + 22} M${bx - 10},${by - 24} L${bx + 26},${by + 12}" stroke="${INK}" stroke-opacity=".5" stroke-width="3"/>`);
      o.push(fist(hdL[0], hdL[1], 13));
      return o; } },
  // ------------------------------------------------ KHODDEDER 2 — the younger customer
  { name: 'khoddeder2', label: 'খদ্দের তরুণ', form: 'standard', size: 'standard', coat: '#3f7a4f', face: 'standard',
    faceTop: ({ cx, hy }) => { const o = []; // neat black hair, thin moustache
      o.push(fillPts([[cx - 94, hy - 8], [cx - 70, hy - 88], [cx + 10, hy - 94], [cx + 88, hy - 34], [cx + 62, hy - 48], [cx + 4, hy - 60], [cx - 44, hy - 54]], '#241d16', 5));
      o.push(`<path d="M${cx - 30},${hy + 34} Q${cx},${hy + 42} ${cx + 30},${hy + 34}" fill="none" stroke="#241d16" stroke-width="6"/>`);
      return o; },
    details: ({ cx, top, bot }) => { const o = []; // green punjabi placket + white pajama hint
      const W = 104;
      o.push(`<path d="M${cx - W * .16},${top + 8} L${cx - W * .16},${bot - 40}" stroke="${INK}" stroke-width="3.5" opacity=".5"/>`);
      for (const t of [.3, .5, .7]) o.push(`<circle cx="${cx - W * .16}" cy="${top + (bot - top) * t}" r="4" fill="${GOLD}" stroke="${INK}" stroke-width="2.5"/>`);
      o.push(`<path d="M${cx - W * .3},${top + 30} Q${cx},${top + 56} ${cx + W * .3},${top + 30}" fill="none" stroke="${INK}" stroke-width="4"/>`);
      return o; },
    props: ({ hdR }) => { const o = []; // cloth shoulder bag (ঝোলা) hanging from the right hand
      const bx = hdR[0] - 6, by = hdL_dummy(hdR, 58);
      o.push(`<path d="M${hdR[0]},${hdR[1]} L${bx - 6},${by - 30} M${hdR[0]},${hdR[1]} L${bx + 34},${by - 26}" stroke="${INK}" stroke-width="4"/>`);
      o.push(poly([[bx - 30, by - 28], [bx + 36, by - 24], [bx + 30, by + 44], [bx - 24, by + 40]], '#c9a86a', 5));
      o.push(`<path d="M${bx - 20},${by - 6} L${bx + 24},${by - 4}" stroke="${INK}" stroke-opacity=".5" stroke-width="3.5"/>`);
      o.push(fist(hdR[0], hdR[1], 12));
      return o; } },
  // ------------------------------------------------ BEPARI — the supplier / creditor
  { name: 'bepari', label: 'সরবরাহকারী', form: 'standard', size: 'fat', coat: '#4a6a8f', face: 'standard',
    faceTop: ({ cx, hy }) => { const o = []; // turban headwrap + thick moustache
      o.push(`<path d="M${cx - 96},${hy + 2} Q${cx - 102},${hy - 64} ${cx - 44},${hy - 84} Q${cx},${hy - 98} ${cx + 46},${hy - 82} Q${cx + 100},${hy - 62} ${cx + 94},${hy + 4} L${cx + 70},${hy - 2} Q${cx + 78},${hy - 48} ${cx + 30},${hy - 62} Q${cx - 20},${hy - 72} ${cx - 48},${hy - 56} Q${cx - 78},${hy - 40} ${cx - 72},${hy + 2} Z" fill="#e8e2d4" stroke="${INK}" stroke-width="5"/>`);
      o.push(`<path d="M${cx - 78},${hy - 22} Q${cx},${hy - 44} ${cx + 78},${hy - 22}" fill="none" stroke="${INK}" stroke-width="4" opacity=".45"/>`);
      o.push(`<path d="M${cx - 70},${hy - 38} Q${cx},${hy - 58} ${cx + 70},${hy - 38}" fill="none" stroke="${INK}" stroke-width="4" opacity=".35"/>`);
      o.push(`<circle cx="${cx + 74}" cy="${hy + 2}" r="10" fill="#c9a86a" stroke="${INK}" stroke-width="4"/>`);
      o.push(`<path d="M${cx - 34},${hy + 30} Q${cx - 10},${hy + 20} ${cx + 4},${hy + 28} Q${cx + 24},${hy + 36} ${cx + 38},${hy + 28} Q${cx + 20},${hy + 46} ${cx - 6},${hy + 42} Q${cx - 28},${hy + 40} ${cx - 34},${hy + 30} Z" fill="#241d16" stroke="${INK}" stroke-width="4"/>`);
      return o; },
    details: ({ cx, top, bot }) => { const o = []; // blue kurta + money pouch on the waist string
      const W = 104;
      o.push(`<path d="M${cx - W * .18},${top + 6} L${cx - W * .18},${bot - 30}" stroke="${INK}" stroke-width="3.5" opacity=".5"/>`);
      o.push(`<path d="M${cx - W * .3},${top + 26} Q${cx},${top + 52} ${cx + W * .3},${top + 26}" fill="none" stroke="${INK}" stroke-width="4"/>`);
      o.push(`<path d="M${cx - W * .5},${top + 148} Q${cx},${top + 170} ${cx + W * .5},${top + 148}" fill="none" stroke="${CREAM}" stroke-width="5"/>`);
      o.push(poly([[cx + W * .34, top + 168], [cx + W * .62, top + 176], [cx + W * .58, top + 236], [cx + W * .3, top + 226]], '#b08a3f', 5)); // the pouch of taka
      o.push(`<circle cx="${cx + W * .46}" cy="${top + 200}" r="5" fill="${GOLD}" stroke="${INK}" stroke-width="2.5"/>`);
      return o; },
    props: ({ hdR, shR, top }) => { const o = []; // rope coil over the right shoulder + fist
      const sx = shR[0], sy = top + 6;
      o.push(`<circle cx="${sx + 26}" cy="${sy - 6}" r="34" fill="none" stroke="#a8804a" stroke-width="9"/>`);
      o.push(`<circle cx="${sx + 26}" cy="${sy - 6}" r="20" fill="none" stroke="#a8804a" stroke-width="7"/>`);
      o.push(`<path d="M${sx + 44},${sy + 20} Q${sx + 60},${sy + 80} ${sx + 30},${sy + 130}" fill="none" stroke="#a8804a" stroke-width="7"/>`);
      o.push(fist(hdR[0], hdR[1], 13));
      return o; } },
];

function hdL_dummy(hdR, dy) { return hdR[1] + dy; }   // the bag hangs straight below the holding hand
