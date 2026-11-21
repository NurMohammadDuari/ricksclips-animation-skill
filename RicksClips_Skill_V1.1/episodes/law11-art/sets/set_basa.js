// SET: রাফির বাসা — Rafi's home (my own build for law11-art). Mother's stove, rice pot, the door the uncle knocks on.
export function build(THREE, scene, film, ctx) {
  const { B2T, toon } = ctx, n = {};
  const add = (m, name, role, o = {}) => { n[name] = (n[name] || 0) + 1; m.name = n[name] > 1 ? `${name}_${String(n[name]).padStart(2, '0')}` : name; m.userData.role = role; if (o.mat) m.userData.mat = o.mat; m.castShadow = o.cast ?? true; m.receiveShadow = true; (o.parent || scene).add(m); return m; };
  const box = (name, role, w, d, h, at, col, o = {}) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), toon(col)); m.position.copy(B2T([at[0], at[1], (at[2] || 0) + h / 2])); if (o.rot) m.rotation.y = o.rot; return add(m, name, role, o); };
  const cyl = (name, role, r, h, at, col, o = {}) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(o.r2 ?? r, r, h, o.seg ?? 16), toon(col)); m.position.copy(B2T([at[0], at[1], (at[2] || 0) + h / 2])); return add(m, name, role, o); };
  const flat = (name, role, geo, col, at, o = {}) => { const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: col, transparent: o.opacity != null, opacity: o.opacity ?? 1, side: THREE.DoubleSide })); if (at) m.position.copy(B2T(at)); if (o.rot) m.rotation.set(o.rot[0] || 0, o.rot[1] || 0, o.rot[2] || 0); return add(m, name, role, { cast: false, ...o }); };
  // mud floor + front yard strip (the home faces -Y)
  box('floor', 'stone', 24, 20, .2, [0, 2, -.1], '#c2a67e', { cast: false, mat: 'plaster' });
  box('yard', 'ground', 24, 5, .18, [0, -3, -.12], '#a89472', { cast: false, mat: 'gravel' });
  // back wall: door right (x 1.6..2.7), barred window left (-2.6..-1.4)
  box('wall_back', 'plaster', 24, .35, 3.4, [0, 4.2, 1.8], '#d9c9a8', { cast: false });
  box('door_dark', 'wood', 1.1, .1, 2.3, [2.15, 4.22, 1.15], '#3a2c1e', { cast: false });
  box('door_jamb_L', 'wood', .12, .4, 2.4, [1.58, 4.1, 1.2], '#6e4527'); box('door_jamb_R', 'wood', .12, .4, 2.4, [2.72, 4.1, 1.2], '#6e4527'); box('door_lintel', 'wood', 1.3, .45, .14, [2.15, 4.1, 2.33], '#6e4527');
  box('window_dark', 'wood', 1.3, .1, 1.0, [-2.0, 4.22, 1.7], '#241d16', { cast: false });
  for (let k = 0; k < 4; k++) cyl('window_bar', 'metal', .03, 1.0, [-2.44 + k * .3, 4.22, 1.7], '#3a3a42', { cast: false });
  box('wall_left', 'plaster', .35, 20, 3.0, [-4.8, 2, 1.5], '#cdbb98', { cast: false });
  // mother's clay stove (চুলা) + the rice pot on it + steam puff
  cyl('stove_body', 'clay', .55, .5, [-1.6, 1.3, 0], '#9a5c3a', { r2: .42, seg: 14 });
  cyl('stove_mouth', 'clay', .2, .12, [-1.6, 1.3, .5], '#4a2c1a', { seg: 12 });
  cyl('rice_pot', 'clay', .4, .42, [-1.6, 1.3, .62], '#8a4436', { r2: .3, seg: 14 });
  flat('steam', 'lamp', new THREE.SphereGeometry(.22, 8, 6), '#ffffff', B2T([-1.6, 1.3, 1.2]), { opacity: .55 });
  box('wood_pile', 'wood', .7, .3, .3, [-2.6, 1.2, .15], '#7a5232');
  // brass water pot (কলস) by the wall + plate stack + stool
  cyl('kolos', 'clay', .26, .55, [1.0, 3.6, 0], '#c98a3c', { r2: .18, seg: 12 });
  for (let k = 0; k < 4; k++) cyl('plate', 'metal', .18, .03, [-.6, 2.2, .02 + k * .045], '#c9ccd6', { seg: 14 });
  box('stool', 'wood', .48, .48, .5, [.6, 1.7, .25], '#8a6a48');
  // mat on the floor + shelf with utensils
  box('mat', 'cloth', 1.8, 1.2, .04, [-.4, .8, 0], '#b3562f', { cast: false, mat: 'canvas' });
  box('shelf_board', 'wood', 2.2, .35, .07, [-.6, 4.05, 2.1], '#7a5a3e');
  for (let k = 0; k < 3; k++) cyl('utensil', 'metal', .1, .22, [-1.3 + k * .5, 4.05, 2.2], '#b9c0cc', { seg: 10 });
  flat('lamp_globe', 'lamp', new THREE.SphereGeometry(.16, 12, 8), '#fff1c2', B2T([1.2, 3.0, 3.0]));
  // a hanging cloth line across the corner
  cyl('line_rope', 'cloth', .012, 2.2, [-4.0, 3.0, 2.6], '#c9bda8', { cast: false }); void 0;
  const cloth = box('hanging_cloth', 'cloth', .7, .06, .9, [-3.2, 3.0, 2.6], '#3f7a4a', { cast: false });
  cloth.rotation.y = .3;
  return {
    anchors: { stove: [-1.6, 1.3, .8], ma: [-.9, 1.5, 0], rafi: [.5, 1.4, 0], door: [2.15, 4.0, 0], window: [-2.0, 4.0, 1.7], mat: [-.4, .8, 0], pot: [-1.6, 1.3, 1.0] },
    update: (f, t) => { const s = scene.getObjectByName('steam'); if (s) { s.scale.setScalar(1 + Math.sin(t * 2.2) * .18); s.position.y = B2T([-1.6, 1.3, 1.2 + Math.sin(t * 1.4) * .06]).y; } },
  };
}
