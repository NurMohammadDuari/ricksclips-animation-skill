// SET pasher — পাশের দোকান (the neighbour's shop): rafi's round-2 world and the partnership payoff.
// Different colour family from the sweet shop (green shutters, checkered floor) so the cuts read as a new place.
// Signature props: brass tarazu on the counter, rice sacks, oil tins, hanging packets,
// the owner's desk that becomes the partnership desk (papers + 4-anna sign).
export function build(THREE, scene, film, ctx) {
  const { B2T, toon } = ctx, n = {};
  const add = (m, name, role, o = {}) => { n[name] = (n[name] || 0) + 1; m.name = n[name] > 1 ? `${name}_${String(n[name]).padStart(2, '0')}` : name; m.userData.role = role; if (o.mat) m.userData.mat = o.mat; m.castShadow = o.cast ?? true; m.receiveShadow = true; (o.parent || scene).add(m); return m; };
  const box = (name, role, w, d, h, at, col, o = {}) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), toon(col)); m.position.copy(B2T([at[0], at[1], at[2] + h / 2])); if (o.rot) m.rotation.y = o.rot; return add(m, name, role, o); };
  const cyl = (name, role, r, h, at, col, o = {}) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(o.r2 ?? r, r, h, o.seg ?? 16), toon(col)); m.position.copy(B2T([at[0], at[1], at[2] + h / 2])); if (o.rot) m.rotation.y = o.rot; return add(m, name, role, o); };
  const flat = (name, role, geo, col, at, o = {}) => { const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: col })); if (at) m.position.copy(at); return add(m, name, role, { cast: false, ...o }); };
  // checkered floor + street edge
  box('floor', 'stone', 26, 24, .2, [0, 3, -.1], '#cbbfa6', { cast: false, mat: 'plaster' });
  for (let r = 0; r < 6; r++) for (let c = 0; c < 8; c++) if ((r + c) % 2) box('tile_dark', 'stone', 1.4, 1.4, .04, [-4.9 + c * 1.4, .4 + r * 1.4, .005], '#5f5648', { cast: false });
  box('street', 'ground', 26, 6, .18, [0, -3.6, -.12], '#96908a', { cast: false, mat: 'gravel' });
  // back wall + green roll shutter with ribs + shop sign
  box('wall_back', 'plaster', 26, .35, 3.7, [0, 4.8, 1.85], '#d6ccb2', { cast: false });
  box('shutter', 'metal', 7.5, .12, 3.0, [2.4, 4.72, 1.5], '#3f7a4a', { cast: false, mat: 'metal' });
  for (let k = 0; k < 12; k++) box('shutter_rib', 'metal', 7.4, .04, .08, [2.4, 4.66, .3 + k * .24], '#356a3f', { cast: false, mat: 'metal' });
  box('sign_board', 'wood', 3.0, .08, .8, [2.4, 4.98, 3.15], '#2f5a3a', { cast: false });
  flat('sign_face', 'lamp', new THREE.PlaneGeometry(2.8, .62), '#f2ecd8', B2T([2.4, 4.94, 3.15]));
  // the counter along the right (owner behind at y ~ 2.6)
  box('counter_body', 'wood', 4.2, .78, .95, [1.6, 1.9, .47], '#7a5a3e', { mat: 'wood_grain' });
  box('counter_top', 'stone', 4.4, .9, .08, [1.6, 1.9, 1.01], '#4a3a2c', { mat: 'wood_grain' });
  // THE BRASS TARAZU standing on the counter + weight set
  cyl('tarazu_post', 'brass', .03, .5, [1.0, 1.9, 1.09], '#c9963c', { seg: 8 });
  box('tarazu_beam', 'brass', .7, .03, .03, [1.0, 1.9, 1.62], '#c9963c');
  flat('pan_L', 'brass', new THREE.CylinderGeometry(.08, .05, .05, 10), '#c9963c', B2T([.72, 1.9, 1.56]));
  flat('pan_R', 'brass', new THREE.CylinderGeometry(.08, .05, .05, 10), '#c9963c', B2T([1.28, 1.9, 1.56]));
  cyl('weight_set', 'brass', .05, .08, [1.9, 1.9, 1.09], '#a8763a', { seg: 8 });
  // rice sacks row + oil tins behind the counter
  for (const [x, s] of [[2.9, 1], [3.6, .85], [4.2, .7]]) { const g = new THREE.Mesh(new THREE.SphereGeometry(.4 * s, 10, 8), toon('#d9cfa8')); g.scale.y = .7; g.position.copy(B2T([x, 2.6, .34 * s])); add(g, 'rice_sack', 'cloth', { mat: 'canvas' }); }
  for (const [x, z] of [[2.6, 0], [2.75, .42], [2.6, .84]]) cyl('oil_tin', 'metal', .18, .4, [4.7, 2.4, z], '#4a6a8f', { seg: 12, mat: 'metal' });
  // hanging plastic packets on a rail (sway in update)
  const packs = [];
  for (let k = 0; k < 4; k++) { const x = .2 + k * .75; cyl('pack_string', 'cloth', .012, .45, [x, 3.4, 3.0], '#5a4a3a', { cast: false }); const p = box('hanging_pack', 'cloth', .26, .1, .34, [x, 3.4, 2.4], k % 2 ? '#c98a3c' : '#2f6a3f', { cast: false }); packs.push(p); }
  // THE OWNER'S DESK (left, becomes the partnership desk): papers, ink, coin tray, the 4-anna board above
  box('desk_body', 'wood', 1.6, .8, .88, [-3.4, 3.0, .44], '#6a4a35', { mat: 'wood_grain' });
  box('desk_top', 'wood', 1.7, .9, .06, [-3.4, 3.0, .91], '#54381f', { mat: 'plywood' });
  flat('paper_stack', 'paper', new THREE.BoxGeometry(.4, .3, .06), '#f2ead2', B2T([-3.2, 2.95, .97]));
  flat('paper_2', 'paper', new THREE.PlaneGeometry(.34, .26), '#e8e0c8', B2T([-3.55, 3.05, .945]));
  cyl('ink_bottle', 'glass', .05, .1, [-3.0, 3.15, .97], '#22303a', { seg: 10 });
  flat('coin_tray', 'brass', new THREE.CylinderGeometry(.12, .1, .04, 12), '#c9963c', B2T([-3.75, 2.8, .96]));
  flat('anna_board', 'paper', new THREE.PlaneGeometry(1.5, .5), '#f2ead2', B2T([-3.4, 4.9, 2.5]));
  box('anna_frame', 'wood', 1.6, .05, .56, [-3.4, 4.9, 2.5], '#7a5a3e', { cast: false });
  // stool behind the counter + a tin trunk + hanging scale lamp
  box('stool', 'wood', .45, .45, .55, [1.2, 2.8, .275], '#6a4a35');
  box('tin_trunk', 'metal', 1.0, .55, .5, [-4.6, 1.6, .25], '#6d7b8a', { mat: 'metal' });
  cyl('lamp_cord', 'cloth', .01, .5, [-1.2, 3.2, 3.05], '#333', { cast: false });
  flat('lamp_globe', 'lamp', new THREE.SphereGeometry(.16, 12, 8), '#ffdf9e', B2T([-1.2, 3.2, 2.72]));
  return {
    anchors: { counter: [1.6, 1.9, 1.05], desk: [-3.4, 3.0, .94], anna_board: [-3.4, 4.9, 2.5], stool: [1.2, 2.8, .55], sign_face: [2.4, 4.9, 3.15], tarazu: [1.0, 1.9, 1.6] },
    update: (f, t) => { for (let i = 0; i < packs.length; i++) packs[i].rotation.z = Math.sin(t * .8 + i * 1.4) * .06; },
  };
}
