// SET: পাশের দোকান — the neighbour's general store, day light (my own build for law11-art).
// Rafi's second chance: half salary, big customers kept in his own hands, then the partnership.
export function build(THREE, scene, film, ctx) {
  const { B2T, toon } = ctx, n = {};
  const add = (m, name, role, o = {}) => { n[name] = (n[name] || 0) + 1; m.name = n[name] > 1 ? `${name}_${String(n[name]).padStart(2, '0')}` : name; m.userData.role = role; if (o.mat) m.userData.mat = o.mat; m.castShadow = o.cast ?? true; m.receiveShadow = true; (o.parent || scene).add(m); return m; };
  const box = (name, role, w, d, h, at, col, o = {}) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), toon(col)); m.position.copy(B2T([at[0], at[1], (at[2] || 0) + h / 2])); if (o.rot) m.rotation.y = o.rot; return add(m, name, role, o); };
  const cyl = (name, role, r, h, at, col, o = {}) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(o.r2 ?? r, r, h, o.seg ?? 16), toon(col)); m.position.copy(B2T([at[0], at[1], (at[2] || 0) + h / 2])); return add(m, name, role, o); };
  const flat = (name, role, geo, col, at, o = {}) => { const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: col, transparent: o.opacity != null, opacity: o.opacity ?? 1, side: THREE.DoubleSide })); if (at) m.position.copy(B2T(at)); if (o.rot) m.rotation.set(o.rot[0] || 0, o.rot[1] || 0, o.rot[2] || 0); return add(m, name, role, { cast: false, ...o }); };
  // ground + road (an open-front shop, no back wall shade: bright day)
  box('ground', 'ground', 26, 26, .2, [0, 3, -.2], '#b9a27e', { cast: false, mat: 'gravel' });
  box('road', 'ground', 26, 5, .18, [0, -4.2, -.22], '#8a8478', { cast: false, mat: 'gravel' });
  // shop shell: back wall with a big open front (y = 5), right side wall, tall shed roof
  box('wall_back', 'plaster', 24, .35, 3.6, [0, 5, 1.8], '#dfcfb2', { cast: false });
  box('wall_right', 'plaster', .35, 22, 3.4, [5.2, 3, 1.7], '#d2bf9e', { cast: false });
  box('roof', 'wood', 24, 8, .25, [0, 3.4, 3.4], '#8a4436', { cast: false, rot: 0 });
  for (let k = 0; k < 3; k++) cyl('roof_post', 'wood', .12, 3.2, [-4.5 + k * 4.5, -1.2, 0], '#6e4527');
  // the shop signboard up on the roof edge
  box('sign_board', 'wood', 3.0, .1, .9, [-1.2, -0.8, 3.1], '#2f6a3f', { cast: false });
  flat('sign_face', 'lamp', new THREE.PlaneGeometry(2.8, .7), '#f3e6c8', B2T([-1.2, -0.9, 3.1]));
  // counter + shelves packed with goods (rice sacks, packets, jars)
  box('counter_body', 'wood', 4.2, .8, .95, [-.5, 2.2, .48], '#96724a', { mat: 'wood_grain' });
  box('counter_top', 'stone', 4.4, .9, .08, [-.5, 2.2, .98], '#4a3a2c', { mat: 'wood_grain' });
  for (const z of [2.4, 3.0]) { box('shelf_board', 'wood', 6.0, .45, .08, [0, 4.9, z], '#7a5a3e');
    for (let k = 0; k < 7; k++) box('pack_shelf', 'paper', .34, .3, .42, [-2.6 + k * .85, 4.9, z + .21], k % 3 === 0 ? '#c23d33' : k % 3 === 1 ? '#2f6a3f' : '#e2b13c', { cast: false }); }
  for (const [x, y, s] of [[-3.8, 3.6, 1], [-4.5, 3.1, .85], [-4.0, 3.35, .7]]) { const g = new THREE.Mesh(new THREE.SphereGeometry(.46 * s, 10, 8), toon('#d9c9a0')); g.scale.y = .7; g.position.copy(B2T([x, y, .35 * s])); add(g, 'rice_sack', 'cloth', { mat: 'canvas' }); }
  for (const [x, col] of [[.6, '#f2b13c'], [1.35, '#3fae5a'], [2.1, '#c94a5f']]) { cyl('jar_glass', 'glass', .16, .36, [x, 2.2, 1.05], '#d7ecf2', { seg: 12 }); flat('jar_top', 'lamp', new THREE.SphereGeometry(.12, 10, 8), col, B2T([x, 2.2, 1.23])); }
  // hanging bunches + a hanging scale + a stool + tea cups on the counter (the partnership tea)
  for (let k = 0; k < 4; k++) { cyl('bunch_string', 'cloth', .01, .4, [2.9, 3.9, 3.2 - k * .5], '#5a4a3a', { cast: false }); flat('bunch', 'lamp', new THREE.SphereGeometry(.14, 8, 6), '#e2a13c', B2T([2.9, 3.9, 2.5 - k * .5])); }
  cyl('scale_chain', 'metal', .015, .45, [-2.4, 3.4, 1.6], '#5a6068', { cast: false });
  cyl('scale_pan', 'metal', .26, .05, [-2.4, 2.98, 1.6], '#c9a04a', { seg: 14 }).userData.role = 'lamp';
  box('stool', 'wood', .45, .45, .55, [1.9, 2.9, .275], '#7a5a3e');
  cyl('tea_cup', 'clay', .07, .1, [-.2, 2.2, 1.03], '#f3efe6', { r2: .05, seg: 10 });
  cyl('tea_cup', 'clay', .07, .1, [.35, 2.2, 1.03], '#f3efe6', { r2: .05, seg: 10 });
  // a bicycle leaning by the wall (this shop HAS a life)
  const bike = new THREE.Group();
  for (const dx of [-.55, .55]) { const w = new THREE.Mesh(new THREE.TorusGeometry(.34, .045, 8, 20), toon('#3a3a42')); w.position.set(dx, .34, 0); bike.add(w); }
  bike.add(new THREE.Mesh(new THREE.BoxGeometry(1.1, .06, .04), toon('#c23d33')).translateY(.62));
  bike.add(new THREE.Mesh(new THREE.BoxGeometry(.06, .5, .04), toon('#c23d33')).translateY(.4).translateX(.5));
  const bb = new THREE.Mesh(new THREE.BoxGeometry(.5, .08, .05), toon('#3a3a42')); bb.position.set(0, .55, 0); bike.add(bb);
  bike.position.copy(B2T([4.0, .9, .35])); bike.rotation.y = .9; scene.add(bike); bike.userData.role = 'bike';
  return {
    anchors: { counter: [-.5, 2.2, 1.0], dokandar: [-.5, 3.1, 0], rafi: [.9, 1.6, 0], sign: [-1.2, -.9, 3.1], sacks: [-4.0, 3.4, .5], scale: [-2.4, 3.0, 1.6], door: [3.4, 2.6, 0] },
    update: (f, t) => {},
  };
}
