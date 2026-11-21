#!/usr/bin/env python3
# DEEP-SCENE PASS (ref: Fahad bhuiyan Law 11, frames analysed 2026-11-22) — dress all 3 sets
# with the reference's scene vocabulary: storeroom boxes, wall clocks, price boards, portrait +
# plants, tea glasses, water pots, brooms. Additions only; every replace is asserted.
import pathlib

BASE = pathlib.Path('/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1/episodes/law11-art/sets')

def patch(fname, pairs):
    p = BASE / fname
    s = p.read_text()
    for old, new in pairs:
        assert s.count(old) == 1, f'{fname}: anchor not unique ({s.count(old)}x): {old[:70]!r}'
        s = s.replace(old, new)
    p.write_text(s)
    print(f'{fname}: {len(pairs)} patches ok')

# ---------------------------------------------------------------- MITHAI_SHOP
shop = []
shop.append((  # dressing block before the khata lines
"""  // ---- the khata (open ledger) on the counter — the film's crown prop
  box('stool_kid',""",
"""  // ---- DEEP DRESSING (ref pass 2026-11-22): the supplier's storeroom corner, wall clock, price board, door-corner life
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
  box('stool_kid',"""))
shop.append((  # update body: clock hand + price board sway
"""    update: (f, t) => {
      for (let i = 0; i < packs.length; i++) { const p = packs[i]; p.rotation.z = Math.sin(t * .9 + i * 1.7) * .05; }
      scaleG.rotation.z = Math.sin(t * .55) * .035;                                   // the balance breathes with the shop's luck
      fan.rotation.y = t * 1.4;
    },""",
"""    update: (f, t) => {
      for (let i = 0; i < packs.length; i++) { const p = packs[i]; p.rotation.z = Math.sin(t * .9 + i * 1.7) * .05; }
      scaleG.rotation.z = Math.sin(t * .55) * .035;                                   // the balance breathes with the shop's luck
      fan.rotation.y = t * 1.4;
      clkH.rotation.z = -t * 1.05;                                                    // the shop's day is measured out
      price.rotation.z = Math.sin(t * .7) * .045;                                     // the price board drifts in the fan breeze
    },"""))
patch('mithai_shop.js', shop)

# ---------------------------------------------------------------- MITHAI_HOME
home = []
home.append((  # fan fix: rod + horizontal blades
"""  // ---- ceiling fan + tin roof beam
  box('beam', 'wood', 24, .28, .26, [0, 3.25, 3.35], '#6a4a35', { cast: false });
  const fan = new THREE.Group(); const hub = new THREE.Mesh(new THREE.SphereGeometry(.09, 10, 8), toon('#3a3a44')); fan.add(hub);
  for (const a of [0, 2.1, 4.2]) { const blade = new THREE.Mesh(new THREE.BoxGeometry(.7, .02, .18), toon('#4a5a6a')); blade.position.set(Math.cos(a) * .4, 0, Math.sin(a) * .4); blade.rotation.y = -a; fan.add(blade); }
  fan.position.copy(B2T([.2, 2.2, 3.1])); fan.rotation.x = Math.PI / 2; add(fan, 'ceiling_fan', 'metal', { cast: false });
  return {""",
"""  // ---- ceiling fan + tin roof beam (rod + flat blades, ref pass fix: it used to stand vertical on nothing)
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
  return {"""))
home.append((  # anchors + update: fan fix + kitchen string sway
"""    anchors: { door: [2.45, 3.3, 0], table: [.3, 1.5, .5], mat: [-2.2, 1.1, .05], window: [-2.2, 3.4, 1.2] },
    update: (f, t) => { fan.rotation.z = t * 1.4; },   // something always moves in the set""",
"""    anchors: { door: [2.45, 3.3, 0], table: [.3, 1.5, .5], mat: [-2.2, 1.1, .05], window: [-2.2, 3.4, 1.2], plant: [1.45, 3.35, .3] },
    update: (f, t) => { fan.rotation.y = t * 1.4; for (let i = 0; i < kerns.length; i++) kerns[i].position.y += Math.sin(t * 1.3 + i) * .0006; },   // something always moves in the set"""))
patch('mithai_home.js', home)

# ---------------------------------------------------------------- MITHAI_PADOSI
padosi = []
padosi.append((  # dressing block before Rafi's khata
"""  // ---- Rafi's own khata on the counter (the partnership ledger)""",
"""  // ---- DEEP DRESSING (ref pass 2026-11-22): the tea row, rate board, news, sacks — the shop that hires Rafi
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
  // ---- Rafi's own khata on the counter (the partnership ledger)"""))
padosi.append((  # update: clock hand
"""      const k = 1 + Math.sin(t * 1.7) * .18; steam.scale.set(k, k * (1 + Math.sin(t * 2.3) * .3), k);   // the kettle breathes
    },""",
"""      const k = 1 + Math.sin(t * 1.7) * .18; steam.scale.set(k, k * (1 + Math.sin(t * 2.3) * .3), k);   // the kettle breathes
      clkH.rotation.z = -t * 1.05;                                                                    // the day moves on the wall
    },"""))
patch('mithai_padosi.js', padosi)
print('ALL SETS DEEPENED')
