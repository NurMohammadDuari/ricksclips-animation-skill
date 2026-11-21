// Lineup render for a cast sheet (works with the repo's own node_modules).
// usage: node lineup.mjs <sheet.mjs> <out.png>
import { renderChar } from './castkit.mjs';
import { createRequire } from 'module'; import path from 'path'; import { pathToFileURL } from 'url';
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_DIR || path.resolve(import.meta.url.replace('file://', '').replace(/code\/lineup\.mjs$/, ''), '../threejs_film/node_modules/playwright'));
const mod = await import(pathToFileURL(path.resolve(process.argv[2])).href);
const CAST = mod.CAST, TITLE = mod.TITLE || '';
const SW = 430, TOPPAD = 70;
let defs = '', body = '', labels = '';
CAST.forEach((spec, i) => {
  const cx = i * SW + SW / 2, oy = TOPPAD + 240;
  const r = renderChar(spec, cx);
  const u = t => t.replace(/id="([gc]\d+)"/g, `id="k${i}_$1"`).replace(/url\(#([gc]\d+)\)/g, `url(#k${i}_$1)`);
  defs += u(r.defs);
  body += `<g transform="translate(0,${oy})">${u(r.body)}</g>`;
  labels += `<text x="${cx}" y="${oy + 1030}" font-family="Arial" font-weight="900" font-size="26" text-anchor="middle" fill="#2a1a1f">${spec.label || spec.name}</text>`;
});
const W = SW * CAST.length, H = TOPPAD + 1420;
const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}"><rect width="${W}" height="${H}" fill="#f2ede2"/><defs>${defs}</defs><text x="${W / 2}" y="40" font-family="Arial" font-weight="900" font-size="24" text-anchor="middle" fill="#1d2f6f">${TITLE}</text>${body}${labels}</svg>`;
const b = await chromium.launch(), pg = await b.newPage({ viewport: { width: W, height: H } });
await pg.setContent(`<html><body style="margin:0">${svg}</body></html>`);
await pg.screenshot({ path: process.argv[3] || process.argv[2].replace(/\.mjs$/, '.png') });
await b.close(); console.log('lineup ->', process.argv[3] || process.argv[2].replace(/\.mjs$/, '.png'));
