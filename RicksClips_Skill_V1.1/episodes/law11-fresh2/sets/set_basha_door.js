// SET: basha_door — the courtyard in front of rafi's home (fresh2). Fully custom outdoor.
// THE DOOR MOTIF: night → morning → night, the packet knocks twice. Camera discipline (fix):
//   the porch roof is REAL and low, so every camera here keeps an eye-line at/above 1.32 m
//   (build_film.py clamps it) — no shot may aim up from below the porch.
// Tree/fence discipline (fix): trunks stand OUTSIDE the walking corridor (|x| >= 4.4),
//   the fence sits 2.6 m behind the house line, never crossing the door path.
export function build(THREE, scene, film, ctx) {
  const { B2T, toon } = ctx;
  const anchor = (name, p) => { ctx._anchors = ctx._anchors || {}; ctx._anchors[name] = p; };
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

  // ground: packed-earth courtyard + a stone path to the door
  const ground = new THREE.Mesh(new THREE.BoxGeometry(16, .12, 14), toon('#b9a27e'));
  ground.position.copy(B2T([0, 2.0, -.06])); ground.name = 'yard_ground'; ground.userData.role = 'ground';
  ground.receiveShadow = true; scene.add(ground);
  for (let k = 0; k < 7; k++) box('path_stone', 'stone', .5, .34, .05, [Math.sin(k * 1.7) * .35, 2.55 - k * .38, 0], '#cbb48c', { cast: false });

  // house front: plaster wall, tin roof, BLUE door (fresh signature), warm window
  box('house_wall', 'plaster', 8.4, .3, 3.4, [0, 3.5, 0], '#d9c9a8', { cast: false });
  box('house_roof', 'metal', 9.2, 1.5, .16, [0, 3.6, 3.45], '#7a8a93');
  box('house_door', 'wood', 1.1, .12, 2.05, [0.1, 3.38, 0], '#3e6ea8');
  box('door_frame', 'wood', 1.3, .1, 2.15, [0.1, 3.34, 0], '#6e4527', { cast: false });
  cyl('door_knob', 'metal', .045, .05, [0.42, 3.3, 1.05], '#c9a23c', { seg: 8 });
  const win = new THREE.Mesh(new THREE.PlaneGeometry(.9, .8), new THREE.MeshBasicMaterial({ color: '#ffd9a0' }));
  win.position.copy(B2T([2.6, 3.32, 1.75])); win.name = 'house_window'; win.userData.role = 'lamp'; scene.add(win);
  box('win_frame', 'wood', 1.0, .08, .9, [2.6, 3.34, 1.75], '#6e4527', { cast: false });

  // porch: slab, two posts, THE low roof (named porch_roof — the raycast culprit of the old bug)
  box('porch_slab', 'stone', 3.0, 1.5, .18, [0.1, 2.62, 0], '#a5987e');
  cyl('porch_post_L', 'wood', .07, 2.3, [-1.35, 2.5, 0], '#6e4527');
  cyl('porch_post_R', 'wood', .07, 2.3, [1.55, 2.5, 0], '#6e4527');
  box('porch_roof', 'metal', 3.4, 1.8, .12, [0.1, 2.55, 2.42], '#7a8a93');
  // warm porch bulb hanging from the porch roof (fix: warm practical, not cold night)
  cyl('porch_wire', 'metal', .012, .4, [0.1, 2.62, 2.36], '#3a3a3a');
  const bulb = new THREE.Mesh(new THREE.SphereGeometry(.09, 10, 8), new THREE.MeshBasicMaterial({ color: '#fff1c2' }));
  bulb.position.copy(B2T([0.1, 2.62, 1.9])); bulb.name = 'porch_bulb_globe'; bulb.userData.role = 'lamp'; scene.add(bulb);
  const warm = new THREE.PointLight('#ffd9a0', 2.2, 8.5, 1.6);
  warm.position.copy(B2T([0.1, 2.62, 1.85])); warm.name = 'porch_pool'; scene.add(warm);

  // tulsi pot beside the door + bicycle against the wall (far side, never in the door corridor)
  cyl('tulsi_pot', 'clay', .22, .42, [-.85, 2.85, 0], '#b3562f', { taper: .7 });
  box('tulsi_plant', 'leaf', .3, .3, .3, [-.85, 2.85, .42], '#4e7d43');
  box('bike_frame', 'metal', 1.5, .12, .5, [3.1, 3.1, .3], '#3e7fd2', { rot: .12 });
  const wheel = (x) => { const m = new THREE.Mesh(new THREE.TorusGeometry(.34, .05, 8, 18), toon('#2f2f38')); m.position.copy(B2T([x, 3.08, .36])); m.name = 'bike_wheel'; m.userData.role = 'metal'; scene.add(m); };
  wheel(2.5); wheel(3.7);

  // TREES outside the corridor (fix: |x| >= 4.4) + FENCE far behind the house line (fix)
  for (const tx of [-4.6, 4.8]) {
    cyl('tree_trunk', 'wood', .16, 2.6, [tx, 4.6, 0], '#6e4527');
    const crown = new THREE.Mesh(new THREE.SphereGeometry(1.1, 10, 8), toon('#4e7d43'));
    crown.position.copy(B2T([tx, 4.6, 3.1])); crown.name = 'tree_crown'; crown.userData.role = 'leaf'; scene.add(crown);
  }
  for (let k = 0; k < 8; k++) box('fence_post', 'wood', .12, .12, 1.0, [-5.2 + k * 1.5, 6.4, 0], '#8a6a48', { cast: false });
  box('fence_rail', 'wood', 12.0, .1, .1, [0, 6.4, .78], '#8a6a48', { cast: false });

  anchor('door', [0.1, 3.3, 0]);
  anchor('step', [0.1, 2.5, .18]);
  anchor('path', [0.1, 1.2, 0]);
  anchor('porch', [0.1, 2.6, .2]);
  anchor('tulsi', [-.85, 2.85, .3]);
  return { anchors: ctx._anchors, update: () => {} };
}
