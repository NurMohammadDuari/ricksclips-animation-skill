// SET basha_door — রাফির বাসার দরজা (the doorway where chacha arrives with the sweet packet).
// Works at night (round 1 + round 3) and morning (the flashback) via the place's light.
// Signature props: blue wooden door with a curtain, tulsi pot on the step, bicycle, tin roof edge,
// house number plate "৪ নং", the step where the packet is handed over.
export function build(THREE, scene, film, ctx) {
  const { B2T, toon } = ctx, n = {};
  const add = (m, name, role, o = {}) => { n[name] = (n[name] || 0) + 1; m.name = n[name] > 1 ? `${name}_${String(n[name]).padStart(2, '0')}` : name; m.userData.role = role; if (o.mat) m.userData.mat = o.mat; m.castShadow = o.cast ?? true; m.receiveShadow = true; (o.parent || scene).add(m); return m; };
  const box = (name, role, w, d, h, at, col, o = {}) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), toon(col)); m.position.copy(B2T([at[0], at[1], at[2] + h / 2])); if (o.rot) m.rotation.y = o.rot; return add(m, name, role, o); };
  const cyl = (name, role, r, h, at, col, o = {}) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(o.r2 ?? r, r, h, o.seg ?? 16), toon(col)); m.position.copy(B2T([at[0], at[1], at[2] + h / 2])); return add(m, name, role, o); };
  const flat = (name, role, geo, col, at, o = {}) => { const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: col })); if (at) m.position.copy(at); return add(m, name, role, { cast: false, ...o }); };
  // ground + path + low yard wall behind
  box('floor', 'ground', 26, 24, .2, [0, 3, -.1], '#b0a48c', { cast: false, mat: 'gravel' });
  box('path', 'stone', 3.4, 5.5, .06, [0, 1.8, .01], '#c9bfa6', { cast: false, mat: 'plaster' });
  // the house facade wall (y = 4.6) in warm brick banding with plaster edges
  box('wall_main', 'plaster', 16, .4, 3.5, [0, 4.6, 1.75], '#d8b98a', { cast: false, mat: 'brick' });
  box('wall_edge_L', 'plaster', .3, .5, 3.5, [-3.2, 4.6, 1.75], '#efe3cc', { cast: false });
  box('wall_edge_R', 'plaster', .3, .5, 3.5, [3.2, 4.6, 1.75], '#efe3cc', { cast: false });
  // tin roof edge with ribs + a hanging bulb by the door (warm pool at night)
  box('roof_edge', 'metal', 12, 1.1, .16, [0, 4.7, 3.42], '#5f6a72', { cast: false, mat: 'metal' });
  for (let k = 0; k < 9; k++) box('roof_rib', 'metal', .08, 1.0, .1, [-5 + k * 1.25, 4.68, 3.3], '#4a545c', { cast: false, mat: 'metal' });
  cyl('porch_cord', 'cloth', .01, .55, [1.5, 3.9, 3.1], '#333', { cast: false });
  flat('porch_bulb', 'lamp', new THREE.SphereGeometry(.14, 12, 8), '#ffdf9e', B2T([1.5, 3.9, 2.8]));
  // THE BLUE DOOR (x = 0), half-open toward -Y, with a dark doorway and a folded curtain
  box('doorway_dark', 'wood', 1.3, .12, 2.5, [0, 4.66, 1.25], '#221c15', { cast: false });
  box('door_leaf', 'wood', 1.05, .12, 2.4, [.52, 4.45, 1.2], '#2f6a8f', { rot: -.5, mat: 'plywood' });
  for (let k = 0; k < 3; k++) box('door_panel', 'wood', .78, .05, .5, [.52, 4.4, .55 + k * .62], '#3f7aa0', { rot: -.5 });
  box('door_jamb_L', 'wood', .14, .45, 2.6, [-.7, 4.55, 1.3], '#8a6a48'); box('door_jamb_R', 'wood', .14, .45, 2.6, [.7, 4.55, 1.3], '#8a6a48'); box('door_lintel', 'wood', 1.7, .5, .16, [0, 4.55, 2.62], '#8a6a48');
  const curt = box('door_curtain', 'cloth', .8, .06, 1.7, [-.35, 4.5, .75], '#c23d33', { cast: false, mat: 'canvas' });
  // THE STEP (the packet lands here) + tulsi pot left + bicycle right
  box('step', 'stone', 2.0, .9, .18, [0, 3.55, .09], '#cbb27f', { mat: 'stone' });
  cyl('tulsi_pot', 'clay', .22, .5, [-1.7, 3.7, .1], '#b5622e', { seg: 12 });
  const tulsi = new THREE.Group();
  for (let k = 0; k < 7; k++) { const lf = new THREE.Mesh(new THREE.ConeGeometry(.06, .3, 5), toon('#3f8a4a')); const a = k / 7 * 6.28; lf.position.set(Math.cos(a) * .12, .32 + (k % 3) * .1, Math.sin(a) * .12); tulsi.add(lf); }
  tulsi.position.copy(B2T([-1.7, 3.7, .6])); add(tulsi, 'tulsi_leaves', 'leaf', { cast: false });
  // bicycle leaning on the right wall: frame tubes + two spoked wheels
  const wheel = (x, y) => { const g = new THREE.Group(); const rim = new THREE.Mesh(new THREE.TorusGeometry(.34, .045, 8, 20), toon('#37414c')); rim.rotation.x = Math.PI / 2; g.add(rim); for (let k = 0; k < 6; k++) { const sp = new THREE.Mesh(new THREE.BoxGeometry(.02, .62, .02), toon('#6d7b8a')); sp.rotation.y = k / 6 * Math.PI; g.add(sp); } g.position.copy(B2T([x, y, .36])); return g; };
  add(wheel(2.6, 3.5), 'bike_wheel', 'metal'); add(wheel(2.05, 3.35), 'bike_wheel', 'metal');
  box('bike_frame', 'metal', .12, 1.0, .08, [2.3, 3.42, .62], '#c23d33', { rot: .2, mat: 'metal' });
  box('bike_seat', 'leather', .3, .12, .06, [2.5, 3.3, .88], '#37302a');
  cyl('bike_bar', 'metal', .025, .5, [2.1, 3.5, .95], '#6d7b8a', { rot: Math.PI / 2 });
  // house number plate "৪ নং" (flat lettering board) + a wall calendar beside the door
  flat('num_plate', 'lamp', new THREE.PlaneGeometry(.5, .3), '#f7ecd2', B2T([-1.0, 4.54, 2.5]));
  box('num_frame', 'wood', .56, .05, .36, [-1.0, 4.55, 2.5], '#7a5a3e', { cast: false });
  flat('cal_board', 'paper', new THREE.PlaneGeometry(.46, .62), '#f2ead2', B2T([1.35, 4.54, 2.3]));
  // dressing: water drum, broom against the wall, string with drying cloth, clay jug
  cyl('water_drum', 'metal', .38, .85, [-2.6, 2.3, .1], '#4a6a5a', { seg: 14, mat: 'metal' });
  box('broom_handle', 'wood', .05, .05, 1.5, [2.9, 4.35, .75], '#a37c52', { rot: .18 });
  flat('dry_cloth', 'cloth', new THREE.PlaneGeometry(.7, .55), '#d8cfc0', B2T([-2.5, 2.2, 1.9]));
  cyl('clay_jug', 'clay', .16, .34, [2.05, 3.75, .18], '#b5622e', { seg: 10 });
  return {
    anchors: { door: [0, 3.9, 0], step: [0, 3.55, .18], tulsi: [-1.7, 3.7, 0], bike: [2.4, 3.4, 0], bulb: [1.5, 3.9, 2.8], wall: [0, 4.5, 0] },
    update: (f, t) => { curt.rotation.x = Math.sin(t * .7) * .04; },
  };
}
