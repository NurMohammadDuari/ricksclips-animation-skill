// SET: পাশের দোকান — the neighbour's tea-and-snacks shop. MY OWN set for the Law 11 film (artist lead, 2026-11-21).
// Humble but alive: a kettle steams on the stove, bananas hang, snacks hang in strips, a bench waits for customers.
// This is where Rafi lands at half pay — and where the film ends with him a partner.
export function build(THREE, scene, film, ctx) {
  const { B2T, toon } = ctx, n = {};
  const add = (m, name, role, o = {}) => { n[name] = (n[name] || 0) + 1; m.name = n[name] > 1 ? `${name}_${String(n[name]).padStart(2, '0')}` : name; m.userData.role = role; if (o.mat) m.userData.mat = o.mat; m.castShadow = o.cast ?? true; m.receiveShadow = true; (o.parent || scene).add(m); return m; };
  const box = (name, role, w, d, h, at, col, o = {}) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), toon(col)); m.position.copy(B2T([at[0], at[1], at[2] + h / 2])); if (o.rot) m.rotation.y = o.rot; return add(m, name, role, o); };
  const cyl = (name, role, r, h, at, col, o = {}) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(o.r2 ?? r, r, h, o.seg ?? 16), toon(col)); m.position.copy(B2T([at[0], at[1], at[2] + h / 2])); return add(m, name, role, o); };
  const flat = (name, role, geo, col, at, o = {}) => { const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: col })); if (at) m.position.copy(at); return add(m, name, role, { cast: false, ...o }); };
  const signTex = (text, bg, fg, edge) => { const c = document.createElement('canvas'); c.width = 512; c.height = 160; const g = c.getContext('2d');
    g.fillStyle = bg; g.fillRect(0, 0, 512, 160); g.strokeStyle = edge; g.lineWidth = 14; g.strokeRect(7, 7, 498, 146);
    g.fillStyle = fg; g.font = '900 72px FreeSans, Arial'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(text, 256, 84);
    const t = new THREE.CanvasTexture(c); t.anisotropy = 4; return t; };
  // ---- floor + street edge (opens toward -Y like the big shop: one connected world)
  box('floor', 'stone', 24, 20, .2, [0, 2, -.1], '#c2b294', { cast: false, mat: 'plaster' });
  box('street', 'ground', 24, 6, .18, [0, -3.2, -.12], '#9a948a', { cast: false, mat: 'gravel' });
  cyl('worn_patch', 'ground', 1.4, .02, [-.4, .2, .01], '#ab9f85', { cast: false, seg: 16 });
  // ---- back wall + left wall + awning over the counter
  box('wall_back', 'plaster', 24, .35, 3.4, [0, 4.4, 1.8], '#e0d2b6', { cast: false });
  box('wall_left', 'plaster', .35, 20, 3.2, [-4.6, 2, 1.6], '#d6c6a4', { cast: false });
  box('awning_beam', 'wood', 5.2, .18, .14, [0, 3.1, -.6], '#6a4a35', { cast: false });
  box('awning_arm_L', 'wood', .12, .12, 1.0, [-2.5, 2.6, -.6], '#6a4a35'); box('awning_arm_R', 'wood', .12, .12, 1.0, [2.5, 2.6, -.6], '#6a4a35');
  // striped awning cloth (no words on it, so it may sway: CB micro-motion rule)
  for (let k = 0; k < 9; k++) box('awning_stripe', 'cloth', .58, 1.0, .05, [-2.4 + k * .6, 3.02, -.62], k % 2 ? '#c23d33' : '#f3e7cf', { cast: false, rot: 0 });
  // ---- the counter (smaller than the big shop's) + glass jars + biscuit tins
  box('counter_body', 'wood', 3.6, .7, .88, [-.3, 1.55, .44], '#96703f', { mat: 'wood_grain' });
  box('counter_top', 'stone', 3.8, .82, .08, [-.3, 1.55, .92], '#46362a', { mat: 'wood_grain' });
  box('counter_front', 'wood', 3.6, .06, .76, [-.3, 1.16, .48], '#a87c4a', { mat: 'plywood' });
  const JARS = [[-1.3, '#e0453a'], [-.65, '#f7df8a'], [0, '#f2a13c']];
  for (const [x, col] of JARS) { cyl('jar_glass', 'glass', .15, .34, [x, 1.55, 1.02], '#d7ecf2', { seg: 12 }); flat('jar_sweets', 'lamp', new THREE.SphereGeometry(.115, 10, 8), col, B2T([x, 1.55, 1.2])); }
  for (let k = 0; k < 3; k++) cyl('biscuit_tin', 'tin', .13, .22, [.7 + k * .3, 1.55, 1.0], k % 2 ? '#c9623a' : '#5f8a94', { seg: 10 });
  cyl('kettle', 'tin', .14, .2, [1.5, 1.55, 1.0], '#c9ccd6', { seg: 12 });
  const steam = flat('kettle_steam', 'lamp', new THREE.SphereGeometry(.09, 8, 6), '#ffffff', B2T([1.5, 1.55, 1.26]));
  const stove_box = box('stove_box', 'tin', .5, .4, .3, [1.5, 1.1, .15], '#3a3a44');
  // ---- shelves + the Bangla sign "চা ও নাস্তা" + hanging snacks + banana bunch
  box('shelf_board', 'wood', 3.4, .35, .06, [-.4, 3.6, 1.9], '#7a5a3e');
  for (let k = 0; k < 4; k++) cyl('shelf_jar', 'glass', .11, .26, [-1.5 + k * .7, 3.6, 2.05], '#d7ecf2', { seg: 10 });
  box('radio', 'wood', .42, .22, .26, [1.6, 3.6, 2.0], '#6a4a35');   // the old radio: the shop's life
  flat('radio_grill', 'lamp', new THREE.CircleGeometry(.07, 12), '#2a2118', B2T([1.72, 3.6, 2.08]));
  const sign = new THREE.Mesh(new THREE.PlaneGeometry(2.1, .66), new THREE.MeshBasicMaterial({ map: signTex('চা ও নাস্তা', '#2f6a3f', '#f7ecd2', '#f2d488') }));
  sign.position.copy(B2T([-.4, 4.15, 2.0])); add(sign, 'sign_face', 'lamp', { cast: false });
  box('sign_board', 'wood', 2.3, .07, .74, [-.4, 4.15, 1.96], '#24522f', { cast: false });
  const hangs = [];   // snack strips + bananas (sway in update)
  for (let k = 0; k < 4; k++) { const x = -2.6 + k * .5; cyl('snack_string', 'cloth', .012, .45, [x, 3.0, 1.4], '#5a4a3a', { cast: false }); const p = box('snack_pack', 'cloth', .22, .08, .3, [x, 3.0, 1.0], k % 2 ? '#e2b13c' : '#c23d33', { cast: false }); hangs.push(p); }
  const banch = new THREE.Group();
  for (let k = 0; k < 6; k++) { const bn = new THREE.Mesh(new THREE.SphereGeometry(.06, 8, 6), toon('#f2c94c')); bn.scale.set(1, 2.4, .7); bn.position.set(Math.sin(k * 2.1) * .12, -k * .09, Math.cos(k * 1.7) * .05); banch.add(bn); }
  banch.position.copy(B2T([-3.3, 3.05, 1.4])); add(banch, 'banana_bunch', 'cloth', { cast: false });
  cyl('banana_string', 'cloth', .012, .3, [-3.3, 3.2, 1.4], '#5a4a3a', { cast: false });
  // ---- bench in front, crate stack, water pot, egg basket
  box('bench_seat', 'wood', 1.8, .4, .08, [1.8, -.6, .42], '#8a6a48', { mat: 'wood_grain' });
  for (const dx of [-.7, .7]) { box('bench_leg_L', 'wood', .08, .4, .42, [1.8 + dx, -.6, .21], '#6a4a35'); }
  for (const [x, y, z] of [[-3.6, 2.6, 0], [-3.5, 2.5, .5]]) box('crate', 'wood', .58, .58, .48, [x, y, z], '#b98a52', { rot: (z * 9) % 1 - .5, mat: 'plywood' });
  cyl('water_pot', 'stone', .26, .48, [-4.0, 3.3, 0], '#a5593e', { seg: 12 });
  const basket = cyl('egg_basket', 'cane', .3, .18, [-2.9, 2.5, 0], '#c9a86a', { seg: 12 });
  for (let k = 0; k < 5; k++) { const e = new THREE.Mesh(new THREE.SphereGeometry(.05, 8, 6), toon('#f7f0dc')); e.position.set(-2.9 + Math.sin(k * 3) * .14, 2.5 + .1, Math.cos(k * 2.3) * .1); add(e, 'egg', 'food', { cast: false }); }
  // ---- wall clock + ceiling bulb
  flat('clock_face', 'lamp', new THREE.CircleGeometry(.2, 16), '#f7f3e6', B2T([2.2, 3.9, 1.95]));
  flat('clock_rim', 'lamp', new THREE.RingGeometry(.2, .24, 16), '#24222c', B2T([2.2, 3.9, 1.95]));
  cyl('bulb_cord', 'cloth', .012, .5, [0, 3.9, 1.7], '#3a3a44', { cast: false });
  flat('bulb', 'lamp', new THREE.SphereGeometry(.09, 10, 8), '#fff1c2', B2T([0, 3.4, 1.7]));
  // ---- DEEP DRESSING (ref pass 2026-11-22): the tea row, rate board, news, sacks — the shop that hires Rafi
  // a row of steaming tea glasses + sugar tin + folded newspaper on the counter
  for (let k = 0; k < 4; k++) cyl('tea_glass', 'glass', .048, .1, [-.05 + k * .16, 1.9, .96], '#d7ecf2', { cast: false, r2: .055 });
  flat('tea_glass_tea', 'lamp', new THREE.CircleGeometry(.048, 10), '#b06a3a', B2T([.19, 1.9, 1.07]), { cast: false });
  cyl('sugar_tin', 'tin', .11, .18, [.42, 1.55, .98], '#c9623a', { seg: 10 });
  box('newspaper', 'cloth', .3, .22, .03, [-.75, 1.62, .945], '#e8e2d4', { rot: .12, cast: false });
  // Bangla rate board hanging by the sign (ref: every shop tells its prices)
  const rate = new THREE.Mesh(new THREE.PlaneGeometry(.9, .38), new THREE.MeshBasicMaterial({ map: signTex('চা ৫ টাকা', '#7a2434', '#f7ecd2', '#e2b13c') }));
  rate.position.copy(B2T([1.35, 3.55, 1.55])); add(rate, 'rate_face', 'lamp', { cast: false });
  // rice + dal sacks at the wall, a second crate, hanging chilli string
  for (const [x, y, s] of [[-3.9, 3.6, 1], [-3.35, 3.7, .8]]) { const g = new THREE.Mesh(new THREE.SphereGeometry(.4 * s, 10, 8), toon('#d9cfa8')); g.scale.y = .75; g.position.copy(B2T([x, y, .35 * s])); add(g, 'rice_sack', 'cloth', { mat: 'canvas' }); }
  box('crate', 'wood', .58, .58, .48, [-2.85, 2.55, 0], '#b98a52', { rot: .06, mat: 'plywood' });
  cyl('chilli_string', 'cloth', .012, .38, [2.75, 3.2, 1.5], '#5a4a3a', { cast: false });
  for (let k = 0; k < 4; k++) { const c = new THREE.Mesh(new THREE.SphereGeometry(.035, 8, 6), toon('#c23d33')); c.scale.y = 2.1; c.position.set(2.75 + Math.sin(k * 2.1) * .05, 3.2 - .38 - k * .07, 1.5); add(c, 'chilli', 'food', { cast: false }); }
  // clock hands on the existing wall clock (live time)
  const clkH = new THREE.Group(); clkH.position.copy(B2T([2.2, 3.9, 1.97]));
  const hMin = new THREE.Mesh(new THREE.BoxGeometry(.028, .14, .012), new THREE.MeshBasicMaterial({ color: '#24222c' })); hMin.position.y = .06; clkH.add(hMin);
  const hHr = new THREE.Mesh(new THREE.BoxGeometry(.04, .1, .012), new THREE.MeshBasicMaterial({ color: '#24222c' })); hHr.position.y = .04; hHr.rotation.z = 1.4; clkH.add(hHr);
  add(clkH, 'clock_hands', 'iron', { cast: false });
  // ---- Rafi's own khata on the counter (the partnership ledger)
  box('khata', 'cloth', .46, .34, .05, [-1.0, 1.55, 0.97], '#7a4a3a', { mat: 'canvas' });
  box('khata_page', 'cloth', .42, .3, .02, [-1.0, 1.55, 1.0], '#f3e6c4', { cast: false });
  return {
    anchors: { counter: [-.3, 1.55, .96], bench: [1.8, -.6, .5], kettle: [1.5, 1.55, 1.05], door: [0, 4.2, .6], jars: [-.9, 1.55, 1.05] },
    update: (f, t) => {
      for (let i = 0; i < hangs.length; i++) { const p = hangs[i]; p.rotation.z = Math.sin(t * 1.1 + i * 1.3) * .06; }
      banch.rotation.z = Math.sin(t * .8 + 2) * .04;
      const k = 1 + Math.sin(t * 1.7) * .18; steam.scale.set(k, k * (1 + Math.sin(t * 2.3) * .3), k);   // the kettle breathes
      clkH.rotation.z = -t * 1.05;                                                                    // the day moves on the wall
    },
  };
}
