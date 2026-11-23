// SET: dokan — kaka's sweet shop (fresh2). Layout base + the story furniture, all fixes baked in:
//   jar glass readable (opacity .45, pale glass + copper lids), brass till with a slot,
//   supplier board DARK green with BRIGHT paper + red stripe, two warm practical bulbs,
//   ceiling fan, khata desk. Anchors name every story noun.
import { buildPlace } from '../../kit/sets/place_kit.js';

export const layout = {
  kind: 'shop', palette: 'warm', size: [10, 7], door: 'back', goods: 'jars', seed: 7,
  furniture: [
    { kind: 'counter', at: [0.1, 2.6], rot: 0 },
    { kind: 'shelf', at: [-3.6, 2.4], rot: 0 },
    { kind: 'sacks', at: [3.6, 2.5], rot: 0 },
    { kind: 'crate', at: [3.2, 1.0], rot: 0 },
    { kind: 'plant', at: [-4.2, 1.2] },
  ],
};

export function build(THREE, scene, film, ctx) {
  const { B2T, toon } = ctx;
  const base = buildPlace(THREE, scene, film, ctx, layout);
  const anchor = (name, p) => { base.anchors[name] = p; };

  const box = (name, role, w, d, h, at, col, o = {}) => {
    const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), toon(col));
    m.position.copy(B2T([at[0], at[1], (at[2] || 0) + h / 2]));
    if (o.rot) m.rotation.y = o.rot;
    m.name = name; m.userData.role = role; scene.add(m); return m;
  };
  const cyl = (name, role, r, h, at, col, o = {}) => {
    const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r * (o.taper || 1), h, o.seg || 10), toon(col));
    m.position.copy(B2T([at[0], at[1], (at[2] || 0) + h / 2]));
    m.name = name; m.userData.role = role; scene.add(m); return m;
  };

  // ---- brass till (fix: readable brass, not a dark box; slot on top)
  box('till_body', 'metal', .34, .3, .22, [1.35, 2.42, .92], '#c9a23c');
  box('till_lid', 'metal', .36, .32, .05, [1.35, 2.42, 1.14], '#e8c063');
  box('till_slot', 'metal', .18, .02, .02, [1.35, 2.5, 1.2], '#6a5a35');
  anchor('till', [1.35, 2.42, 1.1]);

  // ---- supplier board on the back wall (fix: DARK board, BRIGHT paper, red stripe)
  box('supplier_board', 'wood', 1.7, .06, .95, [-1.7, 3.28, 1.35], '#3d5c48');
  const paper = new THREE.Mesh(new THREE.PlaneGeometry(1.42, .62), new THREE.MeshBasicMaterial({ color: '#f7f0dd' }));
  paper.position.copy(B2T([-1.7, 3.24, 1.38])); paper.name = 'supplier_paper'; paper.userData.role = 'paper'; scene.add(paper);
  const stripe = new THREE.Mesh(new THREE.PlaneGeometry(1.42, .1), new THREE.MeshBasicMaterial({ color: '#b03a2e' }));
  stripe.position.copy(B2T([-1.7, 3.23, 1.62])); stripe.name = 'supplier_stripe'; scene.add(stripe);
  anchor('board', [-1.7, 3.1, 1.38]);

  // ---- khata desk by the wall (the red ledger lives here until the story moves it)
  box('khata_desk', 'wood', 1.1, .7, .8, [-2.6, 1.15, 0], '#8a6a48');
  box('khata_desk_top', 'stone', 1.2, .8, .06, [-2.6, 1.15, .8], '#a37c52');
  anchor('khata_desk', [-2.6, 1.15, .86]);

  // ---- glass jar dressing fix: pale glass, copper lids, bigger goods
  scene.traverse(o => {
    if (/jar_glass/.test(o.name || '')) {
      if (o.material) { o.material.transparent = true; o.material.opacity = .45; if (o.material.color) o.material.color.set('#cfe9f2'); }
    }
    if (/counter_body|counter_top/.test(o.name || '')) { /* keep */ }
  });
  for (const gx of [-1.1, -0.55, 0, 0.55, 1.1]) {
    cyl('jar_lid', 'metal', .17, .05, [gx, 2.68, 1.12], '#b0703a', { seg: 12 });
    const knob = new THREE.Mesh(new THREE.SphereGeometry(.05, 8, 6), toon('#8a5426'));
    knob.position.copy(B2T([gx, 2.68, 1.2])); knob.name = 'jar_knob'; knob.userData.role = 'metal'; scene.add(knob);
  }
  anchor('jars', [0.1, 2.7, 1.05]);
  anchor('counter', [0.1, 2.0, 1.0]);

  // ---- ceiling fan (three flat blades, slow spin is done by the layout's lamp flicker; static here)
  cyl('fan_rod', 'metal', .025, .5, [2.3, 2.6, 3.0], '#5a5a5f');
  for (let k = 0; k < 3; k++) {
    const b = new THREE.Mesh(new THREE.BoxGeometry(1.1, .03, .16), toon('#6a6a70'));
    b.position.copy(B2T([2.3, 2.6, 2.72]));
    b.rotation.y = k * Math.PI * 2 / 3; b.name = 'fan_blade'; b.userData.role = 'metal'; scene.add(b);
  }

  // ---- two warm practical bulbs (fix: night interiors read warm, not club-dark)
  for (const [lx, ly] of [[-1.6, 2.3], [1.9, 2.3]]) {
    cyl('bulb_wire', 'metal', .012, .45, [lx, ly, 2.85], '#3a3a3a');
    const globe = new THREE.Mesh(new THREE.SphereGeometry(.09, 10, 8), new THREE.MeshBasicMaterial({ color: '#fff1c2' }));
    globe.position.copy(B2T([lx, ly, 2.36])); globe.name = 'bulb_globe'; globe.userData.role = 'lamp'; scene.add(globe);
    const warm = new THREE.PointLight('#ffd9a0', 2.4, 9.5, 1.6);
    warm.position.copy(B2T([lx, ly, 2.3])); warm.name = 'warm_pool'; scene.add(warm);
  }
  scene.traverse(o => { o.castShadow = false; o.receiveShadow = false; });   // noshadow: animatic speed, the Blender look pass owns the real look
  anchor('door', [0.1, 3.4, 0]);
  return base;
}
