// SET: Rafi's home (a modest Bangla living room). Same conventions as sets/platform.js.
// Door opening on the back wall (y = 3.6, x 1.9..3.0): visitors arrive through it.
export function build(THREE, scene, film, ctx) {
  const { B2T, toon } = ctx, n = {};
  const add = (m, name, role, o = {}) => { n[name] = (n[name] || 0) + 1; m.name = n[name] > 1 ? `${name}_${String(n[name]).padStart(2, '0')}` : name; m.userData.role = role; if (o.mat) m.userData.mat = o.mat; m.castShadow = o.cast ?? true; m.receiveShadow = true; (o.parent || scene).add(m); return m; };
  const box = (name, role, w, d, h, at, col, o = {}) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), toon(col)); m.position.copy(B2T([at[0], at[1], at[2] + h / 2])); if (o.rot) m.rotation.y = o.rot; return add(m, name, role, o); };
  const cyl = (name, role, r, h, at, col, o = {}) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(o.r2 ?? r, r, h, o.seg ?? 16), toon(col)); m.position.copy(B2T([at[0], at[1], at[2] + h / 2])); return add(m, name, role, o); };
  const flat = (name, role, geo, col, at, o = {}) => { const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: col, transparent: o.opacity != null, opacity: o.opacity ?? 1 })); if (at) m.position.copy(at); return add(m, name, role, { cast: false, ...o }); };
  // floor + walls (back y = 3.6, left x = -4.2)
  box('floor', 'stone', 24, 20, .2, [0, 2, -.1], '#c9a97e', { cast: false, mat: 'plaster' });
  box('wall_back', 'plaster', 24, .35, 3.4, [0, 3.6, 1.7], '#e3d3b4', { cast: false });
  box('wall_left', 'plaster', .35, 20, 3.4, [-4.2, 2, 1.7], '#dccbA8'.toLowerCase(), { cast: false });
  // door opening with dark inside + frame (x 1.9..3.0)
  box('door_dark', 'wood', 1.1, .1, 2.3, [2.45, 3.62, 1.15], '#2a2118', { cast: false });
  box('door_jamb_L', 'wood', .12, .4, 2.4, [1.88, 3.5, 1.2], '#7a5a3e'); box('door_jamb_R', 'wood', .12, .4, 2.4, [3.02, 3.5, 1.2], '#7a5a3e'); box('door_lintel', 'wood', 1.3, .45, .13, [2.45, 3.5, 2.33], '#7a5a3e');
  // window on the back wall with a light shaft across the floor
  box('window_dark', 'wood', 1.4, .1, 1.0, [-2.2, 3.62, 1.7], '#241d16', { cast: false });
  box('window_frame', 'wood', 1.55, .3, .08, [-2.2, 3.45, 2.24], '#7a5a3e'); box('window_sill', 'wood', 1.7, .4, .09, [-2.2, 3.4, 1.16], '#8a6a48');
  flat('light_shaft', 'lamp', new THREE.PlaneGeometry(1.3, 2.6), '#fff6dd', B2T([-2.2, 1.4, 1.3]), { mat: 'glass', opacity: 0.16 });
  // sleeping mat + pillow, low table, tin trunk, water pots, wall shelf with a clock box
  box('mat', 'cloth', 2.3, 1.3, .06, [-2.2, 1.1, .03], '#c94a5f', { cast: false, mat: 'canvas' });
  box('pillow', 'cloth', .55, .35, .14, [-2.9, .75, .07], '#f7ecd2', { mat: 'canvas' });
  box('table_top', 'wood', 1.2, .8, .06, [.3, 1.5, .44], '#8a6a48', { mat: 'wood_grain' });
  for (const [dx, dy] of [[-.5, -.3], [.5, -.3], [-.5, .3], [.5, .3]]) cyl('table_leg', 'wood', .05, .42, [.3 + dx, 1.5 + dy, 0], '#6a4a35');
  box('steel_trunk', 'metal', 1.0, .5, .55, [3.1, .8, .275], '#5f8a94', { mat: 'metal' });
  cyl('water_pot', 'stone', .3, .55, [-3.4, 2.6, 0], '#a5593e', { seg: 14 }); cyl('water_pot', 'stone', .24, .45, [-2.9, 2.7, 0], '#a5593e', { seg: 14 });
  box('wall_shelf', 'wood', 1.6, .3, .06, [-.4, 3.42, 2.2], '#7a5a3e', { cast: false });
  box('alarm_clock', 'metal', .22, .12, .26, [-.1, 3.42, 2.36], '#c23d33');
  // dressing: a steel plate and glass on the table, a calendar poster on the wall, a ceiling fan above
  cyl('plate', 'metal', .14, .025, [.1, 1.5, .47], '#d7ecf2', { cast: false, seg: 14 });
  cyl('glass', 'glass', .05, .12, [.55, 1.6, .47], '#d7ecf2', { cast: false });
  box('calendar', 'cloth', .5, .03, .7, [1.0, 3.55, 2.2], '#f7ecd2', { cast: false });
  flat('calendar_face', 'lamp', new THREE.PlaneGeometry(.42, .6), '#fbf6e8', B2T([1.0, 3.51, 2.2]));
  const fan = new THREE.Group(); const hub = new THREE.Mesh(new THREE.SphereGeometry(.09, 10, 8), toon('#3a3a44')); fan.add(hub);
  for (const a of [0, 2.1, 4.2]) { const blade = new THREE.Mesh(new THREE.BoxGeometry(.7, .02, .18), toon('#4a5a6a')); blade.position.set(Math.cos(a) * .4, 0, Math.sin(a) * .4); blade.rotation.y = -a; fan.add(blade); }
  fan.position.copy(B2T([.2, 2.2, 3.1])); fan.rotation.x = Math.PI / 2; add(fan, 'ceiling_fan', 'metal', { cast: false });
  return {
    anchors: { door: [2.45, 3.3, 0], table: [.3, 1.5, .5], mat: [-2.2, 1.1, .05] },
    update: (f, t) => { fan.rotation.z = t * 1.4; },   // something always moves in the set
  };
}
