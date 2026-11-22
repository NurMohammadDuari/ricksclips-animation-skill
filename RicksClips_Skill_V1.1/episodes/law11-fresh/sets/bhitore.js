// SET bhitore — বাসার ভিতরে (inside rafi's home): ma's warning and ma's consolation beats.
// Signature props: clay stove with kettle + steam, low table with two tea cups, wall calendar,
// shelf with radio + lamp, cot edge, window with a light shaft, mat floor.
export function build(THREE, scene, film, ctx) {
  const { B2T, toon } = ctx, n = {};
  const add = (m, name, role, o = {}) => { n[name] = (n[name] || 0) + 1; m.name = n[name] > 1 ? `${name}_${String(n[name]).padStart(2, '0')}` : name; m.userData.role = role; if (o.mat) m.userData.mat = o.mat; m.castShadow = o.cast ?? true; m.receiveShadow = true; (o.parent || scene).add(m); return m; };
  const box = (name, role, w, d, h, at, col, o = {}) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), toon(col)); m.position.copy(B2T([at[0], at[1], at[2] + h / 2])); if (o.rot) m.rotation.y = o.rot; return add(m, name, role, o); };
  const cyl = (name, role, r, h, at, col, o = {}) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(o.r2 ?? r, r, h, o.seg ?? 16), toon(col)); m.position.copy(B2T([at[0], at[1], at[2] + h / 2])); if (o.rot) m.rotation.y = o.rot; return add(m, name, role, o); };
  const flat = (name, role, geo, col, at, o = {}) => { const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: col })); if (at) m.position.copy(at); return add(m, name, role, { cast: false, ...o }); };
  // mat floor + walls of a small room (window on the left wall)
  box('floor', 'cloth', 24, 22, .16, [0, 3, -.08], '#a8845c', { cast: false, mat: 'canvas' });
  box('mat_center', 'cloth', 5.5, 4.0, .05, [0, 2.4, .01], '#8a6a44', { cast: false });
  box('wall_back', 'plaster', 24, .35, 3.4, [0, 5.0, 1.7], '#e3d6bc', { cast: false });
  box('wall_left', 'plaster', .35, 22, 3.4, [-5.0, 3, 1.7], '#d8c9ae', { cast: false });
  // THE WINDOW (left wall) with wooden bars + a light shaft plane (day light reads through)
  box('window_dark', 'wood', 1.6, .12, 1.2, [-4.95, 3.4, 1.7], '#241d16', { cast: false });
  for (let k = 0; k < 3; k++) box('window_bar', 'wood', .1, .2, 1.15, [-4.92, 2.8 + k * .6, 1.7], '#8a6a48', { cast: false });
  flat('light_shaft', 'lamp', new THREE.PlaneGeometry(3.6, 2.2), '#fff2cf', B2T([-3.4, 2.6, 1.5]));
  // THE CLAY STOVE (right rear) + kettle + live coals glow
  box('stove_body', 'clay', .8, .8, .55, [3.2, 4.2, .28], '#8a5a3a', { mat: 'stone' });
  cyl('stove_mouth', 'clay', .16, .18, [3.2, 4.2, .58], '#3a2a1e', { seg: 12 });
  flat('coals', 'lamp', new THREE.CircleGeometry(.12, 10), '#ff9e40', B2T([3.2, 4.2, .68]));
  cyl('kettle', 'metal', .17, .2, [3.2, 4.2, .72], '#5f6a72', { seg: 14, mat: 'metal' });
  cyl('kettle_spout', 'metal', .035, .18, [3.38, 4.2, .82], '#5f6a72', { rot: Math.PI / 2, cast: false });
  box('kettle_grip', 'wood', .22, .05, .04, [3.05, 4.2, .85], '#a37c52', { cast: false });
  // THE LOW TABLE (hero furniture, centre) with two tea cups + a plate of puffed rice
  cyl('table_top', 'wood', .85, .08, [0, 2.4, .3], '#7a5a3e', { seg: 20, mat: 'wood_grain' });
  cyl('table_leg', 'wood', .12, .3, [0, 2.4, .02], '#5f412c', { seg: 10 });
  for (const [x, y] of [[-.3, 2.3], [.35, 2.5]]) {
    cyl('tea_cup', 'clay', .07, .07, [x, y, .38], '#e9dfc8', { seg: 10 });
    flat('tea_surface', 'lamp', new THREE.CircleGeometry(.05, 8), '#c8a86a', B2T([x, y, .42]));
  }
  cyl('muri_plate', 'clay', .16, .04, [0, 2.7, .36], '#d8cfc0', { seg: 12 });
  flat('muri_pile', 'cloth', new THREE.SphereGeometry(.1, 8, 6), '#f2e8ce', B2T([0, 2.7, .42]));
  // THE WALL CALENDAR with Bangla month grid + the shelf with radio and lamp
  box('cal_frame', 'paper', .5, .04, .7, [1.9, 4.95, 1.9], '#f2ead2', { cast: false });
  for (let k = 0; k < 4; k++) flat('cal_line', 'paper', new THREE.PlaneGeometry(.36, .05), '#4a4038', B2T([1.9, 4.93, 2.12 - k * .16]));
  box('shelf_board', 'wood', 2.2, .4, .07, [-.4, 4.85, 2.2], '#7a5a3e');
  box('radio_body', 'wood', .5, .3, .3, [-.7, 4.85, 2.38], '#6e4527', { mat: 'plywood' });
  flat('radio_dial', 'lamp', new THREE.PlaneGeometry(.2, .12), '#e2b13c', B2T([-0.62, 4.7, 2.44]));
  cyl('shelf_lamp', 'glass', .1, .22, [.1, 4.85, 2.35], '#d7ecf2', { seg: 10 });
  flat('shelf_lamp_glow', 'lamp', new THREE.SphereGeometry(.09, 10, 8), '#ffdf9e', B2T([.1, 4.85, 2.5]));
  // THE COT (left front) with a striped blanket folded at the end
  box('cot_frame', 'wood', 2.2, 1.1, .28, [-2.6, 1.2, .14], '#8a6a48', { mat: 'wood_grain' });
  box('cot_blanket', 'cloth', 1.4, 1.0, .1, [-2.9, 1.2, .32], '#2f6a3f', { cast: false });
  for (let k = 0; k < 4; k++) box('cot_leg', 'wood', .1, .1, .14, [-3.5 + k * .5, .8 + (k % 2) * .7, 0], '#5f412c');
  // hanging string with dried chillies (life detail) + a clay water pot in the corner
  cyl('chilli_string', 'cloth', .01, .8, [2.6, 4.85, 2.6], '#5a4a3a', { cast: false });
  for (let k = 0; k < 5; k++) flat('chilli', 'lamp', new THREE.ConeGeometry(.025, .1, 5), '#c23d33', B2T([2.52 + k * .04, 4.85, 2.15 - k * .08]));
  cyl('water_pot', 'clay', .28, .5, [4.1, 1.2, .08], '#b5622e', { seg: 14 });
  return {
    anchors: { table: [0, 2.4, .38], stove: [3.2, 4.2, .6], window: [-4.9, 3.4, 1.7], calendar: [1.9, 4.9, 1.9], cot: [-2.6, 1.2, .3], shelf: [-.4, 4.85, 2.2] },
    update: (f, t) => { const gl = scene.getObjectByName('coals'); if (gl) gl.material.opacity = .8 + Math.sin(t * 9) * .2; },
  };
}
