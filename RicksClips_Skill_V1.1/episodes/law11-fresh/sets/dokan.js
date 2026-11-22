// SET dokan — মিষ্টি দোকান (the sweet shop, Law 11's world). Built for law11-fresh, original geometry.
// Same conventions as sets/platform.js: build(THREE, scene, film, ctx), metres, Z up, Y away from the opening camera.
// Layout: counter runs along X at y = 1.9 (top z = 1.05); owner BEHIND it (y ~ 2.6), customers in FRONT (y ~ 0.9).
// Signature props: ceiling fan over the counter, one warm bulb pool, glass mithai jars, hanging packets,
// a mousetrap gag on the counter corner, the khata desk + supplier board on the left wall.
export function build(THREE, scene, film, ctx) {
  const { B2T, toon } = ctx, n = {};
  const add = (m, name, role, o = {}) => { n[name] = (n[name] || 0) + 1; m.name = n[name] > 1 ? `${name}_${String(n[name]).padStart(2, '0')}` : name; m.userData.role = role; if (o.mat) m.userData.mat = o.mat; m.castShadow = o.cast ?? true; m.receiveShadow = true; (o.parent || scene).add(m); return m; };
  const box = (name, role, w, d, h, at, col, o = {}) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), toon(col)); m.position.copy(B2T([at[0], at[1], at[2] + h / 2])); if (o.rot) m.rotation.y = o.rot; return add(m, name, role, o); };
  const cyl = (name, role, r, h, at, col, o = {}) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(o.r2 ?? r, r, h, o.seg ?? 16), toon(col)); m.position.copy(B2T([at[0], at[1], at[2] + h / 2])); if (o.rot) m.rotation.y = o.rot; return add(m, name, role, o); };
  const flat = (name, role, geo, col, at, o = {}) => { const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: col })); if (at) m.position.copy(at); return add(m, name, role, { cast: false, ...o }); };
  // floor + worn doorstep strip + street edge (shop opens toward -Y)
  box('floor', 'stone', 26, 24, .2, [0, 3, -.1], '#cdbfa4', { cast: false, mat: 'plaster' });
  box('worn_strip', 'ground', 8, 2.2, .06, [0, .3, .01], '#b7ab90', { cast: false, mat: 'gravel' });
  box('street', 'ground', 26, 6, .18, [0, -3.6, -.12], '#9a948a', { cast: false, mat: 'gravel' });
  // back wall (y = 4.8) with a door opening left (x -4.4..-3.3) and a served window right (x 2.6..4.2)
  box('wall_back', 'plaster', 26, .35, 3.7, [0, 4.8, 1.85], '#d8ccae', { cast: false });
  box('door_dark', 'wood', 1.1, .1, 2.5, [-3.85, 4.82, 1.25], '#241d16', { cast: false });
  box('door_jamb_L', 'wood', .12, .4, 2.6, [-4.5, 4.7, 1.3], '#7a5a3e'); box('door_jamb_R', 'wood', .12, .4, 2.6, [-3.22, 4.7, 1.3], '#7a5a3e'); box('door_lintel', 'wood', 1.5, .45, .14, [-3.85, 4.7, 2.55], '#7a5a3e');
  box('window_dark', 'wood', 1.7, .1, 1.15, [3.4, 4.82, 1.8], '#241d16', { cast: false }); box('window_sill', 'wood', 1.9, .5, .1, [3.4, 4.55, 1.17], '#8a6a48');
  box('wall_left', 'plaster', .35, 24, 3.3, [-5.6, 3, 1.65], '#d2c2a2', { cast: false });
  // the counter (hero furniture): body, top slab, front lip, lower shelf of sweet trays
  box('counter_body', 'wood', 4.6, .8, .95, [0, 1.9, .47], '#8a6a48', { mat: 'wood_grain' });
  box('counter_top', 'stone', 4.8, .92, .08, [0, 1.9, 1.01], '#4a3a2c', { mat: 'wood_grain' });
  box('counter_front', 'wood', 4.6, .06, .82, [0, 1.5, .52], '#a37c52', { mat: 'plywood' });
  box('counter_shelf', 'wood', 4.4, .5, .06, [0, 2.15, .34], '#6a4a35');
  for (let k = 0; k < 6; k++) cyl('tray_sweets', 'cloth', .19, .1, [-1.7 + k * .68, 2.15, .37], k % 2 ? '#e0453a' : '#f2b13c', { seg: 12 });
  // glass mithai jars on the counter (dome of sweets under glass)
  for (const [x, col] of [[-1.5, '#f2b13c'], [-.7, '#e0453a'], [0, '#f7f3e2'], [.8, '#3fae5a'], [1.6, '#c94a5f']]) {
    cyl('jar_glass', 'glass', .17, .4, [x, 1.9, 1.1], '#d7ecf2', { seg: 12 });
    flat('jar_sweets', 'lamp', new THREE.SphereGeometry(.13, 10, 8), col, B2T([x, 1.9, 1.28]));
  }
  // THE MOUSETRAP GAG ( humour touch, sits by the till): wooden base, red cheese wedge, wire spring
  box('trap_base', 'wood', .34, .2, .04, [2.0, 1.9, 1.05], '#b98a52', { mat: 'plywood' });
  flat('trap_cheese', 'lamp', new THREE.ConeGeometry(.07, .09, 4), '#e2a13c', B2T([2.0, 1.9, 1.12]));
  cyl('trap_spring', 'metal', .015, .18, [2.12, 1.9, 1.08], '#6d7b8a', { rot: Math.PI / 2 });
  // the till: dark cash box with a brass slot at the counter's right end
  box('till', 'metal', .4, .3, .22, [2.02, 2.3, 1.12], '#37414c', { mat: 'metal' });
  flat('till_slot', 'lamp', new THREE.PlaneGeometry(.14, .02), '#e2b13c', B2T([2.1, 2.24, 1.235]));
  // wall shelves with more jars + the shop sign (lettering stays flat and still: CB rule)
  for (const z of [2.05, 2.62]) { box('shelf_board', 'wood', 4.8, .4, .07, [0, 4.6, z], '#7a5a3e'); for (let k = 0; k < 5; k++) cyl('shelf_jar', 'glass', .13, .3, [-1.9 + k * .95, 4.6, z + .19], '#d7ecf2', { seg: 10 }); }
  box('sign_board', 'wood', 2.8, .08, .85, [0, 4.98, 3.1], '#c23d33', { cast: false });
  flat('sign_face', 'lamp', new THREE.PlaneGeometry(2.6, .66), '#f7ecd2', B2T([0, 4.94, 3.1]));
  // hanging sweet packets on strings (sway in update)
  const packs = [];
  for (let k = 0; k < 5; k++) { const x = -1.3 + k * .8; cyl('pack_string', 'cloth', .012, .5, [x, 3.7, 3.1], '#5a4a3a', { cast: false }); const p = box('sweet_pack', 'cloth', .3, .1, .38, [x, 3.7, 2.45], k % 2 ? '#c23d33' : '#2f6a3f', { cast: false }); packs.push(p); }
  // THE CEILING FAN (signature): hub + three blades over the counter, spins in update
  cyl('fan_hub', 'metal', .1, .12, [0, 2.6, 3.0], '#3a4448', { cast: false });
  const fan = new THREE.Group();
  for (let k = 0; k < 3; k++) { const bl = new THREE.Mesh(new THREE.BoxGeometry(1.05, .05, .16), toon('#2f6a3f')); bl.position.set(Math.cos(k * 2.094) * .55, Math.sin(k * 2.094) * .55, 0); bl.rotation.z = k * 2.094; fan.add(bl); }
  fan.position.copy(B2T([0, 2.6, 3.0])); add(fan, 'fan_blades', 'metal', { cast: false });
  // ONE WARM BULB over the counter + its cord
  cyl('bulb_cord', 'cloth', .01, .5, [.4, 3.4, 3.05], '#333', { cast: false });
  flat('lamp_globe', 'lamp', new THREE.SphereGeometry(.17, 12, 8), '#ffdf9e', B2T([.4, 3.4, 2.72]));
  // THE KHATA DESK + SUPPLIER BOARD on the left wall (the teaching corner)
  box('desk_body', 'wood', 1.5, .7, .9, [-4.0, 3.2, .45], '#7a5a3e', { mat: 'wood_grain' });
  box('desk_top', 'wood', 1.6, .8, .06, [-4.0, 3.2, .93], '#5f412c', { mat: 'plywood' });
  flat('khata_book', 'paper', new THREE.BoxGeometry(.5, .36, .1), '#a8322e', B2T([-3.9, 3.15, .99]));
  cyl('ink_pot', 'glass', .05, .1, [-3.55, 3.35, .99], '#22303a', { seg: 10 });
  box('supplier_board', 'paper', 2.0, .06, 1.3, [-5.4, 3.6, 2.1], '#f2ead2', { cast: false });
  for (let k = 0; k < 5; k++) flat('board_line', 'paper', new THREE.PlaneGeometry(.9, .04), '#4a4038', B2T([-5.36, 3.6 - k * .001, 2.5 - k * .2]));
  // dressing: sugar sacks left rear, crate stack right rear, tin trunk, stool, wall clock
  for (const [x, y, s] of [[-4.6, 2.0, 1], [-5.2, 1.4, .85], [-4.8, 1.75, .7]]) { const g = new THREE.Mesh(new THREE.SphereGeometry(.42 * s, 10, 8), toon('#d9cfa8')); g.scale.y = .75; g.position.copy(B2T([x, y, .35 * s])); add(g, 'sugar_sack', 'cloth', { mat: 'canvas' }); }
  for (const [x, y, z] of [[4.5, 2.6, 0], [4.6, 2.5, .55], [4.4, 2.4, 1.05]]) box('crate', 'wood', .62, .62, .52, [x, y, z], '#b98a52', { rot: (z * 7) % 1 - .5, mat: 'plywood' });
  box('tin_trunk', 'metal', 1.1, .55, .5, [5.2, 1.4, .25], '#6d7b8a', { mat: 'metal' });
  box('stool', 'wood', .45, .45, .55, [-1.3, 3.1, .275], '#7a5a3e');
  cyl('clock_face', 'wood', .32, .05, [3.6, 4.75, 2.9], '#f2ead2', { rot: Math.PI / 2, cast: false });
  // the till stool where the NEPHEW sits (the insult): low box behind counter right
  box('till_stool', 'wood', .5, .5, .48, [2.3, 2.75, .24], '#6a4a35');
  return {
    anchors: { counter: [0, 1.9, 1.05], till: [2.0, 2.3, 1.12], door: [-3.85, 4.4, 0], desk: [-4.0, 3.2, .93], board: [-5.4, 3.6, 2.1], stool: [-1.3, 3.1, .55], till_stool: [2.3, 2.75, .48], sign_face: [0, 4.9, 3.1], trap: [2.0, 1.9, 1.05] },
    update: (f, t) => { fan.rotation.z = t * 2.6; for (let i = 0; i < packs.length; i++) { const p = packs[i]; p.rotation.z = Math.sin(t * .9 + i * 1.7) * .05; } },
  };
}
