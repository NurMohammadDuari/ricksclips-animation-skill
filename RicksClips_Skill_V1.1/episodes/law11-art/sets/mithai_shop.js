// SET: মিষ্টি দোকান — the uncle's sweet shop. MY OWN set for the Law 11 film (artist lead, 2026-11-21).
// Same conventions as sets/platform.js: build(THREE, scene, film, ctx), metres, Z up, Y away from the opening camera.
// Counter runs along X at y = 1.6 (top z = 1.0): the shopkeeper stands BEHIND it (y ~ 2.2), customers in FRONT (y ~ 0.3).
// The hanging balance scale is the film's silent motif: it weighs sweets when the shop thrives, hangs empty when it fails.
export function build(THREE, scene, film, ctx) {
  const { B2T, toon } = ctx, n = {};
  const add = (m, name, role, o = {}) => { n[name] = (n[name] || 0) + 1; m.name = n[name] > 1 ? `${name}_${String(n[name]).padStart(2, '0')}` : name; m.userData.role = role; if (o.mat) m.userData.mat = o.mat; m.castShadow = o.cast ?? true; m.receiveShadow = true; (o.parent || scene).add(m); return m; };
  const box = (name, role, w, d, h, at, col, o = {}) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), toon(col)); m.position.copy(B2T([at[0], at[1], at[2] + h / 2])); if (o.rot) m.rotation.y = o.rot; return add(m, name, role, o); };
  const cyl = (name, role, r, h, at, col, o = {}) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(o.r2 ?? r, r, h, o.seg ?? 16), toon(col)); m.position.copy(B2T([at[0], at[1], at[2] + h / 2])); return add(m, name, role, o); };
  const flat = (name, role, geo, col, at, o = {}) => { const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: col })); if (at) m.position.copy(at); return add(m, name, role, { cast: false, ...o }); };
  // Bangla lettering on a canvas texture (words in the world are allowed: CB 2026-11-11)
  const signTex = (text, bg, fg, edge) => { const c = document.createElement('canvas'); c.width = 512; c.height = 160; const g = c.getContext('2d');
    g.fillStyle = bg; g.fillRect(0, 0, 512, 160); g.strokeStyle = edge; g.lineWidth = 14; g.strokeRect(7, 7, 498, 146);
    g.fillStyle = fg; g.font = '900 74px FreeSans, Arial'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(text, 256, 84);
    const t = new THREE.CanvasTexture(c); t.anisotropy = 4; return t; };
  // ---- floor + street edge (the shop opens toward -Y)
  box('floor', 'stone', 26, 22, .2, [0, 2, -.1], '#cdbfa4', { cast: false, mat: 'plaster' });
  box('street', 'ground', 26, 6, .18, [0, -3.4, -.12], '#9a948a', { cast: false, mat: 'gravel' });
  // worn patch where customers stand (environmental storytelling: years of feet at the counter)
  cyl('worn_patch', 'ground', 1.6, .02, [0, .3, .01], '#b5a98f', { cast: false, seg: 18 });
  // ---- back wall (y = 4.6): door opening (x 1.7..2.8), served window (x -3.4..-1.6)
  box('wall_back', 'plaster', 26, .35, 3.6, [0, 4.6, 1.8], '#e8dcc4', { cast: false });
  box('wall_left', 'plaster', .35, 22, 3.2, [-5.4, 2, 1.6], '#dfcfb2', { cast: false });
  box('door_dark', 'wood', 1.1, .1, 2.45, [2.25, 4.62, 1.22], '#2a2118', { cast: false });
  box('door_jamb_L', 'wood', .12, .4, 2.55, [1.68, 4.5, 1.27], '#7a5a3e'); box('door_jamb_R', 'wood', .12, .4, 2.55, [2.82, 4.5, 1.27], '#7a5a3e'); box('door_lintel', 'wood', 1.3, .45, .14, [2.25, 4.5, 2.48], '#7a5a3e');
  box('window_dark', 'wood', 1.7, .1, 1.15, [-2.5, 4.62, 1.75], '#241d16', { cast: false }); box('window_sill', 'wood', 1.9, .5, .1, [-2.5, 4.35, 1.12], '#8a6a48');
  // ---- the counter (hero furniture): top slab, front panel, kick board, lower shelf with stacked sweet trays
  box('counter_body', 'wood', 4.4, .78, .92, [0, 1.6, .46], '#8a6a48', { mat: 'wood_grain' });
  box('counter_top', 'stone', 4.6, .9, .08, [0, 1.6, .96], '#4a3a2c', { mat: 'wood_grain' });
  box('counter_front', 'wood', 4.4, .06, .8, [0, 1.2, .5], '#a37c52', { mat: 'plywood' });
  box('counter_kick', 'wood', 4.4, .06, .12, [0, 1.6, .04], '#5a4028', { cast: false });
  box('tray_shelf', 'wood', 3.4, .5, .06, [-.3, 1.6, .3], '#6a4a35', { cast: false });
  for (let k = 0; k < 4; k++) box('sweet_tray', 'wood', .72, .42, .1, [-1.55 + k * .85, 1.6, .38], k % 2 ? '#c23d33' : '#2f6a3f', { cast: false });
  // ---- glass sweet jars on the counter: domed mithai under glass (five real Bengali sweets)
  const JARS = [[-1.7, '#f2a13c', 'laddu'], [-1.0, '#f7f3e2', 'roshogolla'], [-.3, '#8a5a34', 'chomchom'], [.4, '#e0453a', 'gulab'], [1.1, '#f7df8a', 'sonpapdi']];
  for (const [x, col] of JARS) {
    cyl('jar_glass', 'glass', .17, .38, [x, 1.6, 1.06], '#d7ecf2', { seg: 12 });
    flat('jar_sweets', 'lamp', new THREE.SphereGeometry(.13, 10, 8), col, B2T([x, 1.6, 1.26]));
    cyl('jar_lid', 'tin', .18, .04, [x, 1.6, 1.44], '#b8b2a4', { seg: 12 });
  }
  // brass bell on the counter + a small tin of loose coins (the world's life)
  flat('bell_dome', 'lamp', new THREE.SphereGeometry(.07, 10, 8, 0, 6.28, 0, 1.9), '#d8b04a', B2T([1.75, 1.6, 1.06]));
  cyl('coin_tin', 'tin', .1, .09, [2.0, 1.6, 1.02], '#7d8696', { seg: 10 });
  // ---- wall shelves: two rows of jars + stacked sweet boxes + the Bangla sign
  for (const z of [1.9, 2.5]) { box('shelf_board', 'wood', 4.6, .4, .07, [0, 4.4, z], '#7a5a3e'); for (let k = 0; k < 5; k++) cyl('shelf_jar', 'glass', .13, .3, [-1.8 + k * .9, 4.4, z + .19], '#d7ecf2', { seg: 10 }); }
  for (let k = 0; k < 3; k++) box('wall_box', 'wood', .55, .3, .3, [1.7, 4.42, 1.62 + k * .34], k % 2 ? '#c23d33' : '#7a3a2e', { cast: false });
  const sign = new THREE.Mesh(new THREE.PlaneGeometry(2.6, .8), new THREE.MeshBasicMaterial({ map: signTex('মিষ্টি দোকান', '#c23d33', '#f7ecd2', '#f2d488') }));
  sign.position.copy(B2T([0, 4.75, 3.06])); add(sign, 'sign_face', 'lamp', { cast: false });
  box('sign_board', 'wood', 2.8, .08, .9, [0, 4.75, 3.02], '#8a2a24', { cast: false });
  // ---- the hanging balance scale (দাঁতরি) — the film's motif, centre beam
  const scaleG = new THREE.Group();
  const beam = new THREE.Mesh(new THREE.BoxGeometry(1.1, .05, .05), toon('#4a3a2c')); scaleG.add(beam);
  for (const s of [-1, 1]) {
    const chainTop = new THREE.Mesh(new THREE.CylinderGeometry(.012, .012, .22, 6), toon('#5a4a3a')); chainTop.position.set(s * .52, -.11, 0); scaleG.add(chainTop);
    const pan = new THREE.Mesh(new THREE.CylinderGeometry(.17, .13, .07, 14), toon('#c9a04a')); pan.position.set(s * .52, -.28, 0); scaleG.add(pan);
    const heap = new THREE.Mesh(new THREE.SphereGeometry(.11, 10, 8), toon('#f2a13c')); heap.scale.y = .5; heap.position.set(s * .52, -.24, 0); scaleG.add(heap);
  }
  scaleG.position.copy(B2T([-3.9, 3.15, 1.5])); add(scaleG, 'balance_scale', 'metal', { cast: false });
  box('scale_hook', 'iron', .04, .04, .5, [-3.9, 3.4, 1.5], '#4a4a52', { cast: false });
  // ---- hanging sweet packets on strings (sway with the set update)
  const packs = [];
  for (let k = 0; k < 5; k++) { const x = -1.3 + k * .8; cyl('pack_string', 'cloth', .012, .5, [x, 3.6, 3.0], '#5a4a3a', { cast: false }); const p = box('sweet_pack', 'cloth', .3, .1, .36, [x, 3.6, 2.28], k % 2 ? '#c23d33' : '#2f6a3f', { cast: false }); packs.push(p); }
  // ---- dressing: sugar sacks, crate stack, tin trunk, oil tin, stool
  for (const [x, y, s] of [[-3.4, 2.2, 1], [-4.1, 1.6, .85], [-3.6, 1.9, .7]]) { const g = new THREE.Mesh(new THREE.SphereGeometry(.42 * s, 10, 8), toon('#d9cfa8')); g.scale.y = .75; g.position.copy(B2T([x, y, .35 * s])); add(g, 'sugar_sack', 'cloth', { mat: 'canvas' }); }
  for (const [x, y, z] of [[3.4, 2.4, 0], [3.5, 2.3, .55], [3.3, 2.2, 1.05]]) box('crate', 'wood', .62, .62, .52, [x, y, z], '#b98a52', { rot: (z * 7) % 1 - .5, mat: 'plywood' });
  box('tin_trunk', 'metal', 1.1, .55, .5, [4.3, 1.2, .25], '#6d7b8a', { mat: 'metal' });
  cyl('oil_tin', 'tin', .16, .34, [4.05, 1.85, 0], '#a8b848', { seg: 10 });
  box('stool', 'wood', .45, .45, .55, [-1.1, 2.9, .275], '#7a5a3e');
  // ---- ceiling beam + lamp + ceiling fan (fan hangs from the beam on a drop rod, 2026-11-21: it used to float in mid-air)
  box('beam', 'wood', 26, .3, .28, [0, 3.2, 3.45], '#6a4a35', { cast: false });
  flat('lamp_globe', 'lamp', new THREE.SphereGeometry(.18, 12, 8), '#fff1c2', B2T([.4, 3.2, 3.08]));
  box('lamp_cap', 'tin', .2, .2, .08, [.4, 3.2, 3.26], '#4a4a52', { cast: false });
  box('fan_rod', 'iron', .05, .05, .26, [1.2, 3.2, 3.06], '#4a4a52', { cast: false });   // beam underside -> hub
  const fan = new THREE.Group(); const hub = new THREE.Mesh(new THREE.SphereGeometry(.09, 10, 8), toon('#3a3a44')); fan.add(hub);
  for (const a of [0, 2.1, 4.2]) { const blade = new THREE.Mesh(new THREE.BoxGeometry(.75, .02, .18), toon('#4a5a6a')); blade.position.set(Math.cos(a) * .42, 0, Math.sin(a) * .42); blade.rotation.y = -a; fan.add(blade); }
  fan.position.copy(B2T([1.2, 3.2, 3.14])); add(fan, 'ceiling_fan', 'metal', { cast: false });   // blades lie flat: a real ceiling fan
  // tube light above the door — the shop's real night lamp: a bright white bar that lifts the dark takes
  flat('tube_bracket', 'tin', new THREE.BoxGeometry(.16, .06, .05), '#3a3a44', B2T([2.25, 4.56, 2.98]), { cast: false });
  flat('tube_light', 'lamp', new THREE.BoxGeometry(1.1, .07, .06), '#fdf6d8', B2T([2.25, 4.55, 3.06]), { cast: false });
  // wall calendar page (the shop's month), pencil marks
  box('calendar', 'cloth', .5, .03, .68, [-3.9, 4.55, 1.6], '#f7ecd2', { cast: false });
  // ---- DEEP DRESSING (ref pass 2026-11-22): the supplier's storeroom corner, wall clock, price board, door-corner life
  // stacked cardboard delivery boxes with tape strips (the supplier's goods, ref frames 2/6)
  const BXT = [[-4.55, 2.15, 0, .04], [-4.5, 2.2, .56, -.03], [-4.42, 2.28, 1.08, .02], [-3.85, 1.45, 0, -.05], [-3.9, 1.5, .54, .03]];
  for (const [x, y, z, r] of BXT) box('dep_box', 'wood', .78, .62, .5, [x, y, z], '#c9a86a', { rot: r, mat: 'plywood' });
  box('dep_box_tape', 'cloth', .1, .64, .52, [-4.55, 2.15, 0], '#8a734d', { rot: .04, cast: false });
  box('dep_box_tape', 'cloth', .1, .64, .52, [-3.85, 1.45, 0], '#8a734d', { rot: -.05, cast: false });
  // wall clock above the served window: rim, face, live hands (update)
  cyl('clock_rim', 'tin', .3, .05, [-2.5, 4.44, 2.86], '#4a4a52', { seg: 18 });
  flat('clock_face', 'cloth', new THREE.CircleGeometry(.26, 18), '#f7ecd2', B2T([-2.5, 4.46, 2.9]), { cast: false });
  const clkH = new THREE.Group(); clkH.position.copy(B2T([-2.5, 4.46, 2.95]));
  const hMin = new THREE.Mesh(new THREE.BoxGeometry(.035, .19, .012), new THREE.MeshBasicMaterial({ color: '#24222c' })); hMin.position.y = .08; clkH.add(hMin);
  const hHr = new THREE.Mesh(new THREE.BoxGeometry(.05, .13, .012), new THREE.MeshBasicMaterial({ color: '#24222c' })); hHr.position.y = .05; hHr.rotation.z = 2.1; clkH.add(hHr);
  add(clkH, 'clock_hands', 'iron', { cast: false });
  // Bangla price board hanging on two strings from the beam, sways in update
  const price = new THREE.Mesh(new THREE.PlaneGeometry(1.15, .44), new THREE.MeshBasicMaterial({ map: signTex('মিষ্টি ৪০০ টাকা/কেজি', '#24522f', '#f7ecd2', '#c23d33') }));
  price.position.copy(B2T([-3.55, 4.35, 3.1])); add(price, 'price_face', 'lamp', { cast: false });
  cyl('price_str_L', 'cloth', .012, .5, [-4.0, 3.95, 3.05], '#5a4a3a', { cast: false });
  cyl('price_str_R', 'cloth', .012, .5, [-3.1, 3.95, 3.05], '#5a4a3a', { cast: false });
  // clay water pot + tray of tumblers at the door corner (the customers' corner)
  cyl('kolshi', 'plaster', .2, .42, [3.05, 4.0, 0], '#a86a44', { seg: 12 });
  cyl('kolshi', 'plaster', .16, .34, [3.3, 4.05, 0], '#a86a44', { seg: 12 });
  cyl('glass_tray', 'tin', .18, .05, [2.75, 3.95, 0], '#c9ccd6', { seg: 12 });
  for (const [x, y] of [[2.68, 3.9], [2.82, 3.98]]) cyl('tumbler', 'glass', .045, .11, [x, y, .05], '#d7ecf2', { cast: false });
  // broom leaning at the counter's right end
  const broom = box('broom_stick', 'wood', .06, .06, 1.3, [2.95, 1.55, 0], '#8a6a48'); broom.rotation.z = .18;
  box('broom_head', 'cloth', .3, .1, .18, [2.78, 1.53, -.02], '#e2c26a', { cast: false });
  // scale weights on the shelf under the balance scale (the দাঁতরি's weights)
  for (const [x, s] of [[-3.7, 1], [-3.55, .7]]) cyl('scale_weight', 'tin', .07 * s, .09 * s, [x, 3.15, 1.5], '#4a4a52', { seg: 10 });
  // ---- the khata (open ledger) on the counter — the film's crown prop
  box('stool_kid', 'wood', .4, .4, .5, [0.3, 1.9, 0], '#7a5a3e');   // the nephew is a kid: he stands on a stool to wear Rafi's spot
  box('khata', 'cloth', .5, .36, .05, [0.9, 1.6, 1.0], '#8a5a3e', { mat: 'canvas' });
  box('khata_page', 'cloth', .46, .32, .02, [0.9, 1.6, 1.03], '#f3e6c4', { cast: false });
  for (let k = 0; k < 4; k++) box('khata_line', 'cloth', .34, .012, .005, [0.9, 1.6, 1.045 + k * .007], '#6a5a48', { cast: false });
  return {
    anchors: { counter: [0, 1.6, 1.02], door: [2.25, 4.3, 0], khata_spot: [.9, 1.6, 1.02], scale: [-3.9, 3.0, 1.5], jars: [-.6, 1.6, 1.1] },
    update: (f, t) => {
      for (let i = 0; i < packs.length; i++) { const p = packs[i]; p.rotation.z = Math.sin(t * .9 + i * 1.7) * .05; }
      scaleG.rotation.z = Math.sin(t * .55) * .035;                                   // the balance breathes with the shop's luck
      fan.rotation.y = t * 1.4;
      clkH.rotation.z = -t * 1.05;                                                    // the shop's day is measured out
      price.rotation.z = Math.sin(t * .7) * .045;                                     // the price board drifts in the fan breeze
    },
  };
}
