// SET: a Bangla sweet shop (mithai dokan). Simple toon set for the storyboard / animatic stage.
// Same conventions as sets/platform.js: build(THREE, scene, film, ctx), metres, Z up, Y away from the opening camera.
// Counter runs along X at y = 1.5 (top at z = 1.0): the shopkeeper stands BEHIND it (y ~ 2.1), customers in FRONT (y ~ 0.3).
export function build(THREE, scene, film, ctx) {
  const { B2T, toon } = ctx, n = {};
  const add = (m, name, role, o = {}) => { n[name] = (n[name] || 0) + 1; m.name = n[name] > 1 ? `${name}_${String(n[name]).padStart(2, '0')}` : name; m.userData.role = role; if (o.mat) m.userData.mat = o.mat; m.castShadow = o.cast ?? true; m.receiveShadow = true; (o.parent || scene).add(m); return m; };
  const box = (name, role, w, d, h, at, col, o = {}) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), toon(col)); m.position.copy(B2T([at[0], at[1], at[2] + h / 2])); if (o.rot) m.rotation.y = o.rot; return add(m, name, role, o); };
  const cyl = (name, role, r, h, at, col, o = {}) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(o.r2 ?? r, r, h, o.seg ?? 16), toon(col)); m.position.copy(B2T([at[0], at[1], at[2] + h / 2])); return add(m, name, role, o); };
  const flat = (name, role, geo, col, at, o = {}) => { const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: col })); if (at) m.position.copy(at); return add(m, name, role, { cast: false, ...o }); };
  // floor + street edge in front (the shop opens toward -Y)
  box('floor', 'stone', 26, 22, .2, [0, 2, -.1], '#cdbfa4', { cast: false, mat: 'plaster' });
  box('street', 'ground', 26, 6, .18, [0, -3.4, -.12], '#9a948a', { cast: false, mat: 'gravel' });
  // back wall (y = 4.6) with a door opening (x 1.7..2.8) and a served window (x -3.4..-1.6)
  box('wall_back', 'plaster', 26, .35, 3.6, [0, 4.6, 1.8], '#e8dcc4', { cast: false });
  box('door_dark', 'wood', 1.1, .1, 2.45, [2.25, 4.62, 1.22], '#2a2118', { cast: false });
  box('door_jamb_L', 'wood', .12, .4, 2.55, [1.68, 4.5, 1.27], '#7a5a3e'); box('door_jamb_R', 'wood', .12, .4, 2.55, [2.82, 4.5, 1.27], '#7a5a3e'); box('door_lintel', 'wood', 1.3, .45, .14, [2.25, 4.5, 2.48], '#7a5a3e');
  box('window_dark', 'wood', 1.7, .1, 1.15, [-2.5, 4.62, 1.75], '#241d16', { cast: false }); box('window_sill', 'wood', 1.9, .5, .1, [-2.5, 4.35, 1.12], '#8a6a48');
  box('wall_left', 'plaster', .35, 22, 3.2, [-5.4, 2, 1.6], '#dfcfb2', { cast: false });
  // the counter (hero furniture): top slab, front panel, and a lower shelf of stacked sweet trays
  box('counter_body', 'wood', 4.4, .78, .92, [0, 1.5, .46], '#8a6a48', { mat: 'wood_grain' });
  box('counter_top', 'stone', 4.6, .9, .08, [0, 1.5, .96], '#4a3a2c', { mat: 'wood_grain' });
  box('counter_front', 'wood', 4.4, .06, .8, [0, 1.12, .5], '#a37c52', { mat: 'plywood' });
  // glass sweet jars on the counter: dome of mithai under glass
  for (const [x, col] of [[-1.6, '#f2b13c'], [-.9, '#e0453a'], [-.2, '#f7f3e2'], [.5, '#3fae5a'], [1.2, '#c94a5f']]) {
    cyl('jar_glass', 'glass', .17, .38, [x, 1.5, 1.06], '#d7ecf2', { seg: 12 });
    flat('jar_sweets', 'lamp', new THREE.SphereGeometry(.13, 10, 8), col, B2T([x, 1.5, 1.24]));
  }
  cyl('jar_glass', 'glass', .17, .38, [1.7, 1.5, 1.06], '#d7ecf2', { seg: 12 });
  // wall shelves with more jars + a hanging sign (lettering stays flat and still: CB rule)
  for (const z of [1.9, 2.5]) { box('shelf_board', 'wood', 4.6, .4, .07, [0, 4.4, z], '#7a5a3e'); for (let k = 0; k < 5; k++) cyl('shelf_jar', 'glass', .13, .3, [-1.8 + k * .9, 4.4, z + .19], '#d7ecf2', { seg: 10 }); }
  box('sign_board', 'wood', 2.6, .08, .8, [0, 4.75, 3.0], '#c23d33', { cast: false });
  flat('sign_face', 'lamp', new THREE.PlaneGeometry(2.4, .62), '#f7ecd2', B2T([0, 4.7, 3.0]));
  // hanging sweet packets on strings (sway with the set update)
  const packs = [];
  for (let k = 0; k < 5; k++) { const x = -1.4 + k * .8; cyl('pack_string', 'cloth', .012, .55, [x, 3.6, 3.0], '#5a4a3a', { cast: false }); const p = box('sweet_pack', 'cloth', .3, .1, .38, [x, 3.6, 2.3], k % 2 ? '#c23d33' : '#2f6a3f', { cast: false }); packs.push(p); }
  // dressing: sugar sacks left, crate stack right, a hanging scale, a standing fan? keep to sacks + crates + a tin trunk
  for (const [x, y, s] of [[-3.4, 2.2, 1], [-4.1, 1.6, .85], [-3.6, 1.9, .7]]) { const g = new THREE.Mesh(new THREE.SphereGeometry(.42 * s, 10, 8), toon('#d9cfa8')); g.scale.y = .75; g.position.copy(B2T([x, y, .35 * s])); add(g, 'sugar_sack', 'cloth', { mat: 'canvas' }); }
  for (const [x, y, z] of [[3.4, 2.4, 0], [3.5, 2.3, .55], [3.3, 2.2, 1.05]]) box('crate', 'wood', .62, .62, .52, [x, y, z], '#b98a52', { rot: (z * 7) % 1 - .5, mat: 'plywood' });
  box('tin_trunk', 'metal', 1.1, .55, .5, [4.3, 1.2, .25], '#6d7b8a', { mat: 'metal' });
  // a stool behind the counter and a ceiling beam with a lamp
  box('stool', 'wood', .45, .45, .55, [-1.1, 2.9, .275], '#7a5a3e');
  box('beam', 'wood', 26, .3, .28, [0, 3.2, 3.45], '#6a4a35', { cast: false });
  flat('lamp_globe', 'lamp', new THREE.SphereGeometry(.18, 12, 8), '#fff1c2', B2T([.4, 3.2, 3.1]));
  return {
    anchors: { counter: [0, 1.5, 1.02], door: [2.25, 4.3, 0], khata_spot: [.9, 1.5, 1.02] },
    update: (f, t) => { for (let i = 0; i < packs.length; i++) { const p = packs[i]; p.rotation.z = Math.sin(t * .9 + i * 1.7) * .05; p.position.x = B2T([-1.4 + i * .8, 3.6, 2.3]).x + Math.sin(t * .7 + i) * .01; } },
  };
}
