// SET: রাফির বাসা — Rafi's modest home. MY OWN set for the Law 11 film (artist lead, 2026-11-21).
// Door opening on the back wall (y = 3.6, x 1.9..3.0): the uncle arrives through it three times (the film's signature).
// The kitchen corner tells the family is poor but kept: brass pots hang, the mat is patched, the plate is steel.
export function build(THREE, scene, film, ctx) {
  const { B2T, toon } = ctx, n = {};
  const add = (m, name, role, o = {}) => { n[name] = (n[name] || 0) + 1; m.name = n[name] > 1 ? `${name}_${String(n[name]).padStart(2, '0')}` : name; m.userData.role = role; if (o.mat) m.userData.mat = o.mat; m.castShadow = o.cast ?? true; m.receiveShadow = true; (o.parent || scene).add(m); return m; };
  const box = (name, role, w, d, h, at, col, o = {}) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), toon(col)); m.position.copy(B2T([at[0], at[1], at[2] + h / 2])); if (o.rot) m.rotation.y = o.rot; return add(m, name, role, o); };
  const cyl = (name, role, r, h, at, col, o = {}) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(o.r2 ?? r, r, h, o.seg ?? 16), toon(col)); m.position.copy(B2T([at[0], at[1], at[2] + h / 2])); return add(m, name, role, o); };
  const flat = (name, role, geo, col, at, o = {}) => { const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: col, transparent: o.opacity != null, opacity: o.opacity ?? 1 })); if (at) m.position.copy(at); return add(m, name, role, { cast: false, ...o }); };
  // ---- floor + walls (back y = 3.6, left x = -4.2)
  box('floor', 'stone', 24, 20, .2, [0, 2, -.1], '#c9a97e', { cast: false, mat: 'plaster' });
  box('wall_back', 'plaster', 24, .35, 3.4, [0, 3.6, 1.7], '#e3d3b4', { cast: false });
  box('wall_left', 'plaster', .35, 20, 3.4, [-4.2, 2, 1.7], '#dcb9a2', { cast: false });
  // ---- door opening with dark inside + frame (x 1.9..3.0) — the film's signature doorway
  box('door_dark', 'wood', 1.1, .1, 2.3, [2.45, 3.62, 1.15], '#2a2118', { cast: false });
  box('door_jamb_L', 'wood', .12, .4, 2.4, [1.88, 3.5, 1.2], '#7a5a3e'); box('door_jamb_R', 'wood', .12, .4, 2.4, [3.02, 3.5, 1.2], '#7a5a3e'); box('door_lintel', 'wood', 1.3, .45, .13, [2.45, 3.5, 2.33], '#7a5a3e');
  // sandals left at the door (life: someone took them off)
  box('sandal_L', 'leather', .09, .26, .04, [1.55, .95, .02], '#8a5a3e', { rot: .3, cast: false }); box('sandal_R', 'leather', .09, .26, .04, [1.75, .8, .02], '#8a5a3e', { rot: -.2, cast: false });
  // ---- window with a light shaft across the floor
  box('window_dark', 'wood', 1.4, .1, 1.0, [-2.2, 3.62, 1.7], '#241d16', { cast: false });
  box('window_frame', 'wood', 1.55, .3, .08, [-2.2, 3.45, 2.24], '#7a5a3e'); box('window_sill', 'wood', 1.7, .4, .09, [-2.2, 3.4, 1.16], '#8a6a48');
  flat('light_shaft', 'lamp', new THREE.PlaneGeometry(1.3, 2.6), '#fff6dd', B2T([-2.2, 1.4, 1.3]), { mat: 'glass', opacity: 0.16 });
  // ---- sleeping mat (patched) + pillow, low table, tin trunk, water pots
  box('mat', 'cloth', 2.3, 1.3, .06, [-2.2, 1.1, .03], '#c94a5f', { cast: false, mat: 'canvas' });
  box('mat_patch', 'cloth', .4, .35, .07, [-1.6, 1.35, .035], '#8a5a6a', { cast: false });
  box('pillow', 'cloth', .55, .35, .14, [-2.9, .75, .07], '#f7ecd2', { mat: 'canvas' });
  box('table_top', 'wood', 1.2, .8, .06, [.3, 1.5, .44], '#8a6a48', { mat: 'wood_grain' });
  for (const [dx, dy] of [[-.5, -.3], [.5, -.3], [-.5, .3], [.5, .3]]) cyl('table_leg', 'wood', .05, .42, [.3 + dx, 1.5 + dy, 0], '#6a4a35');
  box('steel_trunk', 'metal', 1.0, .5, .55, [3.1, .8, .275], '#5f8a94', { mat: 'metal' });
  cyl('water_pot', 'stone', .3, .55, [-3.4, 2.6, 0], '#a5593e', { seg: 14 }); cyl('water_pot', 'stone', .24, .45, [-2.9, 2.7, 0], '#a5593e', { seg: 14 });
  // ---- wall shelf with clock, calendar page, hanging brass pots (kitchen corner), gamcha on a peg
  box('wall_shelf', 'wood', 1.6, .3, .06, [-.4, 3.42, 2.2], '#7a5a3e', { cast: false });
  box('alarm_clock', 'metal', .22, .12, .26, [-.1, 3.42, 2.36], '#c23d33');
  box('calendar', 'cloth', .5, .03, .7, [1.0, 3.55, 2.2], '#f7ecd2', { cast: false });
  flat('calendar_face', 'lamp', new THREE.PlaneGeometry(.42, .6), '#fbf6e8', B2T([1.0, 3.51, 2.2]));
  box('pot_shelf', 'wood', .8, .22, .05, [-2.8, 3.4, 2.45], '#7a5a3e', { cast: false });
  for (const [x, s] of [[-3.0, 1], [-2.6, .85]]) cyl('brass_pot', 'brass', .12 * s, .18, [x, 3.4, 2.5], '#c9a04a', { seg: 12 });
  box('peg_board', 'wood', .6, .06, .1, [-3.6, 3.3, 1.55], '#7a5a3e', { cast: false });
  box('gamcha', 'cloth', .3, .05, .5, [-3.6, 3.3, 1.3], '#f7f3e6', { cast: false, mat: 'canvas' });
  // ---- steel plate + glass + teapot on the table (the tea the mother pours)
  cyl('plate', 'metal', .14, .025, [.1, 1.5, .47], '#d7ecf2', { cast: false, seg: 14 });
  cyl('glass', 'glass', .05, .12, [.55, 1.6, .47], '#d7ecf2', { cast: false });
  cyl('teapot', 'metal', .1, .16, [-.25, 1.5, .47], '#c9ccd6', { seg: 12 });
  // ---- ceiling fan + tin roof beam (rod + flat blades, ref pass fix: it used to stand vertical on nothing)
  box('beam', 'wood', 24, .28, .26, [0, 3.25, 3.35], '#6a4a35', { cast: false });
  box('fan_rod', 'iron', .05, .05, .24, [.2, 3.25, 3.0], '#4a4a52', { cast: false });
  const fan = new THREE.Group(); const hub = new THREE.Mesh(new THREE.SphereGeometry(.09, 10, 8), toon('#3a3a44')); fan.add(hub);
  for (const a of [0, 2.1, 4.2]) { const blade = new THREE.Mesh(new THREE.BoxGeometry(.7, .02, .18), toon('#4a5a6a')); blade.position.set(Math.cos(a) * .4, 0, Math.sin(a) * .4); blade.rotation.y = -a; fan.add(blade); }
  fan.position.copy(B2T([.2, 3.25, 3.08])); add(fan, 'ceiling_fan', 'metal', { cast: false });
  // ---- DEEP DRESSING (ref pass 2026-11-22): the family portrait, potted plants, kitchen string, corner life
  // framed family portrait on the wall above the low table (silhouette busts only: no drawn faces)
  box('portrait_frame', 'wood', .62, .05, .78, [-.5, 3.56, 2.5], '#6a4a35', { cast: false });
  flat('portrait_card', 'cloth', new THREE.PlaneGeometry(.5, .66), '#e8dcc4', B2T([-.5, 3.53, 2.5]), { cast: false });
  flat('portrait_bust_L', 'lamp', new THREE.CircleGeometry(.075, 12), '#5a4a3a', B2T([-.62, 3.55, 2.52]), { cast: false });
  flat('portrait_bust_R', 'lamp', new THREE.CircleGeometry(.06, 12), '#7a5a44', B2T([-.38, 3.56, 2.52]), { cast: false });
  // two potted plants flanking the door (terracotta + leaf clusters)
  for (const px of [1.45, 3.5]) {
    cyl('plant_pot', 'plaster', .17, .3, [px, 3.35, 0], '#a5593e', { seg: 12 });
    const leaves = new THREE.Group();
    for (let k = 0; k < 6; k++) { const lf = new THREE.Mesh(new THREE.SphereGeometry(.1, 8, 6), toon('#2f6a3f')); lf.scale.set(1, 1.9, .5); lf.position.set(Math.sin(k * 2.2) * .1, .34 + k * .045, Math.cos(k * 1.9) * .08); lf.rotation.z = Math.sin(k * 2.6) * .5; leaves.add(lf); }
    leaves.position.copy(B2T([px, 3.35, .28])); add(leaves, 'plant_leaves', 'cloth', { cast: false });
  }
  // kitchen string: onions + dried chillies hanging from the beam by the shelf
  const kerns = [];
  for (const [x, r, col] of [[-1.35, .5, '#a86a44'], [-1.15, .42, '#c23d33']]) {
    cyl('kitchen_string', 'cloth', .012, .42, [x, 3.0, 1.6], '#5a4a3a', { cast: false });
    for (let k = 0; k < 5; k++) { const g = new THREE.Mesh(new THREE.SphereGeometry(.045 * r + .02, 8, 6), toon(col)); g.position.set(x + Math.sin(k * 2.4) * .06, 3.0 - .42 - k * .075, 1.6); kerns.push(g); add(g, 'kitchen_knob', 'food', { cast: false }); }
  }
  // corner life: broom, steel bucket, folded clothes on the trunk, floor cushion
  const broomH = box('broom_stick', 'wood', .06, .06, 1.25, [3.5, 3.2, 0], '#8a6a48'); broomH.rotation.z = .16;
  box('broom_head', 'cloth', .28, .1, .17, [3.39, 3.18, -.01], '#e2c26a', { cast: false });
  cyl('bucket', 'metal', .18, .26, [3.15, 3.25, 0], '#c9ccd6', { seg: 12 });
  box('clothes_L', 'cloth', .5, .4, .14, [3.05, .78, .6], '#8a9ab0', { rot: .2, cast: false });
  box('clothes_R', 'cloth', .44, .36, .12, [3.1, .82, .74], '#c9b8a0', { rot: -.15, cast: false });
  box('cushion', 'cloth', .55, .5, .16, [.9, .7, .08], '#c94a5f', { cast: false, mat: 'canvas' });
  return {
    anchors: { door: [2.45, 3.3, 0], table: [.3, 1.5, .5], mat: [-2.2, 1.1, .05], window: [-2.2, 3.4, 1.2], plant: [1.45, 3.35, .3] },
    update: (f, t) => { fan.rotation.y = t * 1.4; for (let i = 0; i < kerns.length; i++) kerns[i].position.y += Math.sin(t * 1.3 + i) * .0006; },   // something always moves in the set
  };
}
