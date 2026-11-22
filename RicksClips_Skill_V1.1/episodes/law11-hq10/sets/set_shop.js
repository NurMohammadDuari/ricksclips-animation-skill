// SET: Rafi's sweet shop (mithai shop) — hand-built from scratch 2026-11-22 for law11-hq10.
// Rebuilt to Rick's measured DNA (library/style/ricksclips-dna/STYLE_DNA.md):
//   texture-mapped low-poly world (relief wood / plaster / tile), warm diegetic light pools
//   (hanging lamp + window shaft), PBR brass trays, rail and scale, dense props in clusters,
//   diegetic signage carrying the joke ("নতুন মালিক" tag on the till), and everything animates
//   (ceiling fan, hanging scale sway, lamp flicker, mood re-grade on the story turn).
// Plan coords: metres, Z up, Y away from the opening camera (B2T: (x,y,z) -> (x,z,-y)).
// Back wall y = 4.2, side walls x = ±5, ceiling 3.3. Counter across the frame at y = 1.6.
// Door to the street right (x ≈ 3.7), window shaft left (x ≈ -3.7), hanging lamp over the counter.
export function build(THREE, scene, film, ctx) {
  const { B2T, toon, relief, pbr } = ctx;
  const anchors = {};
  const n = {};
  const add = (m, name, role, o = {}) => { n[name] = (n[name] || 0) + 1; m.name = n[name] > 1 ? `${name}_${String(n[name]).padStart(2, '0')}` : name; m.userData.role = role; if (o.mat) m.userData.mat = o.mat; m.castShadow = o.cast ?? true; m.receiveShadow = true; (o.parent || scene).add(m); return m; };
  const box = (name, role, w, d, h, at, col, o = {}) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), o.mat || toon(col)); m.position.copy(B2T([at[0], at[1], at[2] + h / 2])); if (o.rot) m.rotation.y = o.rot; return add(m, name, role, o); };
  const cyl = (name, role, r, h, at, col, o = {}) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(o.r2 ?? r, r, h, o.seg ?? 16), o.mat || toon(col)); m.position.copy(B2T([at[0], at[1], at[2] + h / 2])); m.rotation.set(o.rx || 0, o.rot || 0, o.rz || 0); return add(m, name, role, o); };
  const flat = (name, role, geo, mat, at, o = {}) => { const m = new THREE.Mesh(geo, mat || new THREE.MeshBasicMaterial({ color: o.col || '#ffffff', transparent: o.opacity != null, opacity: o.opacity ?? 1, side: THREE.DoubleSide, blending: o.add ? THREE.AdditiveBlending : THREE.NormalBlending, depthWrite: !o.add })); if (at) m.position.copy(B2T(at)); if (o.rot) m.rotation.set(o.rot[0] || 0, o.rot[1] || 0, o.rot[2] || 0); return add(m, name, role, { cast: false, ...o }); };
  const anchor = (name, p) => { anchors[name] = [Math.round(p[0] * 1000) / 1000, Math.round(p[1] * 1000) / 1000, Math.round(p[2] * 1000) / 1000]; };
  // Bangla painted-board text (shop sign, price board, calendar, till tag)
  const paintTex = (lines, opts = {}) => {
    const c = document.createElement('canvas'); c.width = 512; c.height = Math.round(512 / (opts.ar || 3));
    const g = c.getContext('2d');
    g.fillStyle = opts.bg || '#f4e3bf'; g.fillRect(0, 0, c.width, c.height);
    if (opts.frame !== 'none') { g.strokeStyle = opts.frame || '#7a3b22'; g.lineWidth = 14; g.strokeRect(8, 8, c.width - 16, c.height - 16); }
    g.fillStyle = opts.ink || '#8a2f1e'; g.textAlign = 'center'; g.textBaseline = 'middle';
    g.font = `700 ${opts.px || 90}px "Noto Sans Bengali", sans-serif`;
    const ys = lines.length === 1 ? [c.height / 2] : lines.map((_, i) => c.height * (i + 1) / (lines.length + 1));
    lines.forEach((t, i) => g.fillText(t, c.width / 2, ys[i]));
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t;
  };
  const texPlane = (name, role, w, h, tex, at, o = {}) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: tex, side: THREE.DoubleSide })); m.position.copy(B2T(at)); if (o.rot) m.rotation.set(o.rot[0] || 0, o.rot[1] || 0, o.rot[2] || 0); return add(m, name, role, { cast: false, ...o }); };

  // ---------------------------------------------------------------- shell (all relief, no flat fills)
  const mFloor = relief('wood', '#8a5636', { seed: 7, scale: 1.15 });
  box('floor', 'wood', 11, 9, .2, [0, 2.2, -.2], 0, { cast: false, mat: mFloor });
  const mWall = relief('plaster', '#e6d2a8', { seed: 4 });
  box('wall_back', 'plaster', 11, .4, 3.3, [0, 4.2, 0], 0, { cast: false, mat: mWall });
  box('wall_left', 'plaster', .4, 9, 3.3, [-5, 2.2, 0], 0, { cast: false, mat: mWall });
  box('wall_right', 'plaster', .4, 9, 3.3, [5, 2.2, 0], 0, { cast: false, mat: mWall });
  box('ceiling', 'wood', 11, 9, .18, [0, 2.2, 3.3], '#4a3626', { cast: false });
  const mWain = relief('wood', '#6e4628', { seed: 11, scale: 1.6 });
  box('wainscot_back', 'wood', 11, .1, 1.0, [0, 3.95, 0], 0, { cast: false, mat: mWain });
  box('wainscot_left', 'wood', .1, 9, 1.0, [-4.75, 2.2, 0], 0, { cast: false, mat: mWain });
  box('beam_A', 'wood', 11, .3, .3, [0, 2.8, 3.0], '#5c3f28', { cast: false });
  box('beam_B', 'wood', .3, 9, .3, [0, 2.2, 3.0], '#5c3f28', { cast: false });

  // ---------------------------------------------------------------- door (street, right) with spill + curtains
  box('door_dark', 'wood', 1.15, .12, 2.4, [3.7, 4.18, 0], '#241a12', { cast: false });
  box('door_jamb_L', 'wood', .14, .44, 2.5, [3.05, 4.2, 0], '#5c3f28'); box('door_jamb_R', 'wood', .14, .44, 2.5, [4.35, 4.2, 0], '#5c3f28');
  box('door_lintel', 'wood', 1.5, .5, .16, [3.7, 4.2, 2.45], '#5c3f28');
  flat('door_spill', 'lamp', new THREE.PlaneGeometry(1.3, 2.3), null, [3.7, 4.0, 1.18], { col: '#ffdf9e', opacity: .16, add: true });
  box('door_curtain_L', 'cloth', .5, .06, 2.1, [3.35, 3.98, .28], '#a83a2c');
  box('door_curtain_R', 'cloth', .55, .06, 2.1, [4.05, 3.98, .28], '#a83a2c');
  anchor('door', [3.7, 3.8, 0]);

  // ---------------------------------------------------------------- window (left) + light shaft
  box('window_dark', 'wood', 1.5, .12, 1.2, [-4.95, 1.6, 1.35], '#1c140d', { cast: false });
  box('window_sill', 'wood', 1.9, .5, .12, [-4.7, 1.6, 1.28], '#5c3f28');
  box('window_bar', 'wood', .08, .2, 1.2, [-4.9, 1.6, 1.35], '#5c3f28', { cast: false });
  flat('window_glow', 'lamp', new THREE.PlaneGeometry(1.4, 1.1), null, [-4.86, 1.6, 1.95], { col: '#fff3d0', opacity: .5 });
  flat('shaft', 'lamp', new THREE.PlaneGeometry(2.8, 1.5), null, [-3.5, 1.6, 1.55], { col: '#ffe9b8', opacity: .10, add: true, rot: [0, -1.15, .45] });
  anchor('window', [-4.5, 1.6, 1.4]);
  const winLight = new THREE.PointLight('#ffdf9e', 12, 9, 2); winLight.position.copy(B2T([-4.3, 1.6, 1.9])); scene.add(winLight);

  // ---------------------------------------------------------------- counter (relief wood + tile top + brass rail)
  const mBrass = pbr ? pbr.metal('brass', { finish: 'brushed', seed: 3 }) : toon('#c9a24a');
  const mCounter = relief('wood', '#9a6238', { seed: 5, scale: 1.3 });
  box('counter_body', 'wood', 4.6, .9, .95, [-.2, 1.6, 0], 0, { mat: mCounter });
  const mTop = relief('tile', '#ddd2bc', { seed: 9, scale: 1.4 });
  box('counter_top', 'stone', 4.8, 1.0, .07, [-.2, 1.6, .95], 0, { mat: mTop });
  box('counter_front', 'wood', 4.6, .05, .82, [-.2, 1.12, .06], 0, { mat: mWain });
  cyl('counter_rail', 'metal', .035, 4.6, [-.2, 1.02, 1.0], 0, { mat: mBrass, rz: Math.PI / 2 });
  cyl('rail_post_L', 'metal', .035, 1.05, [-2.35, 1.16, 0], 0, { mat: mBrass });
  cyl('rail_post_R', 'metal', .035, 1.05, [1.95, 1.16, 0], 0, { mat: mBrass });
  anchor('counter', [-.2, 1.0, 1.02]);
  anchor('counter_top', [-.2, 1.6, 1.02]);

  // ---------------------------------------------------------------- sweet display (brass trays + mounds + glass dome)
  const sweetCols = ['#e8912a', '#f2e7d8', '#b06a34', '#d9a840', '#f7ead0', '#c2553a', '#7aa93c', '#c98a4a'];
  const trayAt = [-1.7, -.6, .5, 1.55];
  trayAt.forEach((tx, i) => {
    const mTray = pbr ? pbr.metal('brass', { finish: 'cast', seed: 8 + i }) : toon('#c9a24a');
    cyl(`tray_${i}`, 'metal', .34, .05, [tx, 1.58, 1.02], 0, { seg: 24, mat: mTray });
    const kind = [1, 0, 2, 3][i]; // tray order: rosho, laddu (front of rafi), chomchom, sonpapdi
    for (let k = 0; k < 7; k++) {
      const ang = k * 2.39, rr = .1 + (k % 3) * .08;
      const px = tx + Math.cos(ang) * rr, py = 1.58 + Math.sin(ang) * rr * .55;
      if (kind === 2) cyl(`sweet_${i}_${k}`, 'sweet', .055, .17, [px, py, 1.07], sweetCols[2], { rz: Math.PI / 2, rot: ang, seg: 10 });
      else if (kind === 3) box(`sweet_${i}_${k}`, 'sweet', .1, .1, .07, [px, py, 1.07], sweetCols[3], { rot: ang });
      else { const s = new THREE.Mesh(new THREE.SphereGeometry(.075, 10, 8), toon(kind === 0 ? sweetCols[0] : sweetCols[1])); s.position.copy(B2T([px, py, 1.14])); s.scale.y = .72; add(s, `sweet_${i}_${k}`, 'sweet'); }
    }
    if (i === 0) anchor('tray1', [tx, 1.58, 1.12]);
    if (i === 3) anchor('tray4', [tx, 1.58, 1.12]);
  });
  if (pbr) { const dome = new THREE.Mesh(new THREE.SphereGeometry(.34, 18, 12, 0, Math.PI * 2, 0, Math.PI / 2), pbr.metal('wet', { color: '#cfe0e6', rough: .06, coat: 1, coatRough: .1, seed: 2 })); dome.position.copy(B2T([.5, 1.58, 1.07])); add(dome, 'dome', 'glass', { cast: false }); }
  anchor('trays', [-.6, 1.58, 1.1]);

  // ---------------------------------------------------------------- till + khata + the joke tag (diegetic sign)
  box('till_body', 'wood', .55, .45, .5, [1.62, 2.0, .95], '#5c3f28');
  box('till_lid', 'wood', .55, .45, .06, [1.62, 2.0, 1.45], '#6e4628', { rot: .06 });
  const mCoin = pbr ? pbr.metal('gold', { finish: 'cast', seed: 6 }) : toon('#d9b13c');
  for (let k = 0; k < 4; k++) cyl('coin', 'metal', .05, .02, [1.52 + (k % 2) * .12, 1.95 + Math.floor(k / 2) * .1, 1.51], 0, { seg: 12, mat: mCoin });
  box('khata', 'paper', .42, .3, .09, [2.35, 2.42, 1.01], '#a8322a', { rot: .35 });
  flat('khata_page', 'paper', new THREE.PlaneGeometry(.36, .26), null, [2.35, 2.42, 1.107], { col: '#f7f1de', rot: [0, 0, .35] });
  texPlane('till_tag', 'paper', .44, .13, paintTex(['নতুন মালিক'], { px: 110, ar: 3.4, bg: '#fbf3dc', ink: '#2f2a22', frame: '#8a8272' }), [1.62, 1.76, 1.52], { rot: [0, 0, -.08] });
  anchor('till', [1.62, 2.0, 1.5]);
  anchor('khata', [2.35, 2.42, 1.1]);

  // ---------------------------------------------------------------- back wall: two shelf rows of jars + tins + sign
  const mShelf = relief('wood', '#7c4f2c', { seed: 13, scale: 1.2 });
  for (let row = 0; row < 2; row++) {
    const z = 1.35 + row * .85, y = 3.95;
    box(`shelf_board_${row}`, 'wood', 6.4, .42, .07, [-2.4, y, z], 0, { mat: mShelf });
    for (const bx of [-5.45, .65]) box(`shelf_bracket_${row}_${bx}`, 'wood', .1, .5, .1, [bx, y, z - .12], '#5c3f28', { cast: false });
    for (let j = 0; j < 8; j++) {
      const jx = -5.3 + j * .72;
      cyl(`jar_${row}_${j}`, 'glass', .2, .55, [jx, y - .18, z + .05], '#bccfd4', { seg: 14, cast: false });
      cyl(`jar_sweet_${row}_${j}`, 'sweet', .14, .22, [jx, y - .18, z + .05], sweetCols[(j + row * 3) % 8], { seg: 12, cast: false });
      cyl(`jar_lid_${row}_${j}`, 'metal', .21, .06, [jx, y - .18, z + .6], 0, { seg: 14, mat: mBrass });
    }
    for (let k = 0; k < 3; k++) cyl(`tin_${row}_${k}`, 'metal', .16, .3, [-.35 + k * .45, y - .16, z + .16], '#b8b4ac', { seg: 12 });
  }
  anchor('jars', [-2.4, 3.7, 1.9]);
  const sign = texPlane('shop_sign', 'sign', 3.4, .81, paintTex(['রাফি মিষ্টি ঘর'], { px: 104, ar: 4.2 }), [-2.4, 3.95, 3.0]);
  const signBoard = new THREE.Mesh(new THREE.BoxGeometry(3.6, .06, .95), toon('#5c3f28')); signBoard.position.copy(B2T([-2.4, 3.99, 3.0])); add(signBoard, 'sign_board', 'wood', { cast: false });
  anchor('sign', [-2.4, 3.8, 2.9]);
  cyl('clock_rim', 'metal', .3, .06, [2.6, 4.05, 2.35], 0, { seg: 24, mat: mBrass, rx: Math.PI / 2 });
  cyl('clock_face', 'stone', .26, .03, [2.6, 4.02, 2.35], '#f5efe0', { seg: 24, rx: Math.PI / 2, cast: false });
  texPlane('clock_hand', 'metal', .03, .2, null, [2.6, 4.0, 2.36], { col: '#2a241c', rot: [0, 0, .8] });
  texPlane('calendar', 'paper', .5, .34, paintTex(['নভেম্বর', 'চৈত্র'], { px: 88, ar: 1.5, bg: '#f7f0dc' }), [-4.35, 4.05, 2.3]);

  // ---------------------------------------------------------------- right wall price board + stove corner
  texPlane('price_board', 'sign', 1.15, .44, paintTex(['আজকের দাম', '১০ টাকা'], { px: 92, ar: 2.6 }), [4.82, 2.6, 2.0], { rot: [0, -Math.PI / 2, 0] });
  box('stove_body', 'metal', .9, .6, .75, [-3.6, 3.3, 0], '#5a5450');
  cyl('pot', 'metal', .22, .26, [-3.55, 3.3, .75], '#8f8a84', { seg: 16 });
  cyl('kettle', 'metal', .14, .2, [-3.0, 3.35, .78], '#7d7871', { seg: 12 });

  // ---------------------------------------------------------------- sacks + crates cluster (right of counter)
  for (let k = 0; k < 3; k++) { const s = new THREE.Mesh(new THREE.SphereGeometry(.42 - k * .05, 10, 8), toon('#d9cfa0')); s.scale.y = .72; s.position.copy(B2T([3.3 + (k % 2) * .7, 2.9 + Math.floor(k / 2) * .5, .3 - k * .04])); add(s, 'sack', 'cloth', { mat: 'canvas' }); }
  const mCrate = relief('wood', '#8a6a44', { seed: 17, scale: 1.1 });
  box('crate_A', 'wood', .62, .62, .5, [3.9, 1.15, 0], 0, { mat: mCrate });
  box('crate_B', 'wood', .58, .58, .45, [4.4, 1.5, 0], 0, { rot: .5, mat: mCrate });
  box('crate_C', 'wood', .55, .55, .42, [4.05, 1.3, .5], 0, { rot: .12, mat: mCrate });

  // ---------------------------------------------------------------- foreground mass: barrel + big sweet jar (left near)
  const barrel = new THREE.Mesh(new THREE.CylinderGeometry(.32, .36, .8, 16), mCrate); barrel.position.copy(B2T([-3.3, .55, 0])); barrel.position.y = .4; add(barrel, 'barrel', 'wood');
  cyl('big_jar', 'glass', .3, .8, [-3.3, .55, .78], '#bccfd4', { seg: 18, cast: false });
  cyl('big_jar_sweets', 'sweet', .22, .34, [-3.3, .55, .83], '#e8912a', { seg: 14, cast: false });
  cyl('big_jar_lid', 'metal', .31, .07, [-3.3, .55, 1.58], 0, { seg: 18, mat: mBrass });

  // ---------------------------------------------------------------- hanging lamp + bloom globe + floor pool
  const lamp = new THREE.Group();
  const cord = new THREE.Mesh(new THREE.CylinderGeometry(.012, .012, .7, 6), toon('#2a221a')); cord.position.y = -.35; lamp.add(cord);
  const holder = new THREE.Mesh(new THREE.CylinderGeometry(.05, .09, .12, 10), mBrass); holder.position.y = -.74; lamp.add(holder);
  const globe = new THREE.Mesh(new THREE.SphereGeometry(.11, 14, 10), new THREE.MeshBasicMaterial({ color: '#ffdf9e' }));
  globe.position.y = -.84; globe.name = 'lamp_globe'; globe.userData.role = 'lamp'; lamp.add(globe);
  const shade = new THREE.Mesh(new THREE.ConeGeometry(.22, .16, 14, 1, true), toon('#3f6a3a')); shade.position.y = -.76; lamp.add(shade);
  lamp.position.copy(B2T([-.2, 2.1, 2.6])); scene.add(lamp);
  const lampLight = new THREE.PointLight('#ffd9a0', 26, 11, 2); lampLight.position.copy(B2T([-.2, 2.1, 1.72])); scene.add(lampLight);
  flat('lamp_pool', 'lamp', new THREE.CircleGeometry(1.6, 24), null, [-.2, 2.1, .012], { col: '#ffdf9e', opacity: .10, add: true, rot: [-Math.PI / 2, 0, 0] });
  anchor('lamp', [-.2, 2.1, 1.8]);

  // hanging brass scale (sways) + sweet-box garland
  const scaleG = new THREE.Group();
  const sCord = new THREE.Mesh(new THREE.CylinderGeometry(.008, .008, .5, 6), toon('#2a221a')); sCord.position.y = -.25; scaleG.add(sCord);
  const sBar = new THREE.Mesh(new THREE.BoxGeometry(.6, .02, .02), mBrass); sBar.position.y = -.52; scaleG.add(sBar);
  const sPanL = new THREE.Mesh(new THREE.CylinderGeometry(.09, .07, .04, 12), mBrass); sPanL.position.set(-.28, -.6, 0); scaleG.add(sPanL);
  const sPanR = new THREE.Mesh(new THREE.CylinderGeometry(.09, .07, .04, 12), mBrass); sPanR.position.set(.28, -.6, 0); scaleG.add(sPanR);
  scaleG.position.copy(B2T([1.0, 2.9, 2.55])); scene.add(scaleG);
  for (let k = 0; k < 4; k++) box(`box_string_${k}`, 'paper', .3, .22, .12, [-3.2 + k * .38, 3.7, 2.45 - Math.sin(k) * .05], ['#c23d33', '#2f6a3f', '#c23d33', '#2f6a3f'][k], { cast: false });

  // ---------------------------------------------------------------- ceiling fan (turns in update)
  const fan = new THREE.Group();
  const fanHub = new THREE.Mesh(new THREE.CylinderGeometry(.06, .06, .1, 10), toon('#3a3428')); fan.add(fanHub);
  const fanCord = new THREE.Mesh(new THREE.CylinderGeometry(.01, .01, .25, 6), toon('#2a221a')); fanCord.position.y = .17; fan.add(fanCord);
  for (let k = 0; k < 3; k++) {
    const bl = new THREE.Mesh(new THREE.BoxGeometry(.85, .02, .16), toon('#5a5148'));
    bl.position.x = .5; const pivot = new THREE.Group(); pivot.rotation.y = k * (Math.PI * 2 / 3); pivot.rotation.x = .12; pivot.add(bl); fan.add(pivot);
  }
  fan.position.copy(B2T([.9, 3.0, 3.05])); scene.add(fan);

  // ---------------------------------------------------------------- stool + pitha basket behind counter
  box('stool_seat', 'wood', .38, .38, .05, [1.62, 2.95, .48], '#6e4628');
  for (const [sx, sy] of [[-.14, -.14], [.14, -.14], [-.14, .14], [.14, .14]]) box('stool_leg', 'wood', .05, .05, .48, [1.62 + sx, 2.95 + sy, 0], '#5c3f28');


  // ---------------------------------------------------------------- density pass (2026-11-22): festoons, posters, box tower, high shelf
  const mDark = toon('#3a2c1e');
  const flags = ['#c23d33', '#2f6a3f', '#e8b13c', '#3e6a9f', '#c2553a', '#2f6a3f', '#e8b13c', '#c23d33'];
  for (let k = 0; k < 8; k++) { const u = k / 7, sag = Math.sin(u * Math.PI) * .35;
    box(`pennant_${k}`, 'cloth', .16, .02, .22, [-3.9 + u * 5.6, 2.2, 2.9 - sag], flags[k], { cast: false }); }
  box('festoon_cord', 'cloth', 5.6, .02, .02, [-1.1, 2.2, 3.06], mDark, { cast: false });
  for (let k = 0; k < 6; k++) { const u = k / 5, sag = Math.sin(u * Math.PI) * .3;
    box(`pennant2_${k}`, 'cloth', .14, .02, .2, [-2.6 + u * 4.2, 3.4, 2.95 - sag], flags[(k + 3) % 8], { cast: false }); }
  box('festoon_cord2', 'cloth', 4.2, .02, .02, [-0.5, 3.4, 3.0], mDark, { cast: false });
  // framed posters on the back wall (strong edges + this place's paper)
  const post1 = texPlane('poster_1', 'paper', .7, .95, paintTex(['আজ', '৩০% ছাড়'], { px: 82, ar: .74, bg: '#f2e2c4', ink: '#a03020' }), [3.6, 4.05, 2.2]);
  box('poster_1_frame', 'wood', .8, .05, 1.05, [3.6, 4.03, 1.7], '#4a3626', { cast: false });
  const post2 = texPlane('poster_2', 'paper', .55, .7, paintTex(['চা', '৫ টাকা'], { px: 84, ar: .78, bg: '#e8e2d0', ink: '#2f4a3a' }), [4.5, 4.05, 1.6]);
  box('poster_2_frame', 'wood', .65, .05, .8, [4.5, 4.03, 1.2], '#4a3626', { cast: false });
  // sweet-box tower on the counter left end (big near shape)
  const boxCols = ['#c23d33', '#2f6a3f', '#e8b13c'];
  for (let k = 0; k < 3; k++) box(`box_tower_${k}`, 'paper', .5 - k * .04, .42 - k * .04, .28, [-2.05, 1.62, 1.02 + k * .3], boxCols[k % 3], { rot: k * .12 });
  // ladle pot + spoons (right counter end)
  cyl('ladle_pot', 'metal', .16, .26, [-.05, 1.6, 1.02], '#8f8a84', { seg: 14 });
  for (let k = 0; k < 3; k++) box(`ladle_${k}`, 'metal', .04, .04, .4, [-.05 + (k - 1) * .05, 1.58, 1.26], '#7d7871', { rot: (k - 1) * .1, cast: false });
  // third high shelf with jars (fills the top band)
  const z3 = 2.75;
  box('shelf_board_3', 'wood', 5.2, .36, .06, [-2.6, 3.95, z3], 0, { mat: mShelf });
  for (let j = 0; j < 5; j++) {
    const jx = -4.4 + j * .9;
    cyl(`jar_3_${j}`, 'glass', .17, .48, [jx, 3.9, z3 + .04], '#bccfd4', { seg: 14, cast: false });
    cyl(`jar3_sweet_${j}`, 'sweet', .12, .2, [jx, 3.9, z3 + .04], sweetCols[(j * 2) % 8], { seg: 12, cast: false });
    cyl(`jar3_lid_${j}`, 'metal', .18, .05, [jx, 3.9, z3 + .52], 0, { seg: 14, mat: mBrass });
  }
  // coin scatter near the till (fine detail)
  for (let k = 0; k < 3; k++) cyl('coin', 'metal', .04, .015, [1.3 + k * .07, 2.15 + k * .05, 1.02], 0, { seg: 10, mat: mCoin });

  anchor('center', [0, .8, 0]); anchor('back', [0, 3.4, 0]); anchor('front', [0, -.4, 0]);

  // ---------------------------------------------------------------- mood + motion (update): Rick re-grades on the turn
  // warm shop while chacha declares (t < 4.05); the lamp dips cool while Rafi cannot believe it
  // (t 4.05-7.5); back to warm with a soft flicker for the indignant payoff. Fan turns, scale sways.
  const warm = { c: new THREE.Color('#ffd9a0'), i: 26 }, cool = { c: new THREE.Color('#a9c4e8'), i: 14 };
  let warmT = 1;
  function update(f, t) {
    if (t == null) t = (f || 0) / (film.fps || 30);
    fan.rotation.y = t * 16.4;
    scaleG.rotation.z = Math.sin(t * 1.7) * .05; scaleG.rotation.x = Math.sin(t * 1.13 + 1) * .03;
    const flick = 1 + Math.sin(t * 13.7) * .022 + Math.sin(t * 7.3) * .016;
    let target = 1; if (t >= 4.05 && t < 7.5) target = 0;
    warmT += (target - warmT) * ((t > 3.9 && t < 4.3) || (t > 7.4 && t < 7.8) ? .16 : .03);
    lampLight.color.copy(cool.c).lerp(warm.c, warmT);
    lampLight.intensity = (cool.i + (warm.i - cool.i) * warmT) * flick;
    winLight.intensity = 12 * (.7 + .3 * warmT) * flick;
    return { warmT };
  }
  return { anchors, update };
}
