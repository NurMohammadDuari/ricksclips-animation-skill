// SET rasta — রাস্তা (the street): the ten-year pay walk and the closing beats.
// Signature props: shop-front row backdrop, tea stall cart with kettle, lampposts, birds on a wire,
// telegraph pole, puddle with reflection, dust bin.
export function build(THREE, scene, film, ctx) {
  const { B2T, toon } = ctx, n = {};
  const add = (m, name, role, o = {}) => { n[name] = (n[name] || 0) + 1; m.name = n[name] > 1 ? `${name}_${String(n[name]).padStart(2, '0')}` : name; m.userData.role = role; if (o.mat) m.userData.mat = o.mat; m.castShadow = o.cast ?? true; m.receiveShadow = true; (o.parent || scene).add(m); return m; };
  const box = (name, role, w, d, h, at, col, o = {}) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), toon(col)); m.position.copy(B2T([at[0], at[1], at[2] + h / 2])); if (o.rot) m.rotation.y = o.rot; return add(m, name, role, o); };
  const cyl = (name, role, r, h, at, col, o = {}) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(o.r2 ?? r, r, h, o.seg ?? 16), toon(col)); m.position.copy(B2T([at[0], at[1], at[2] + h / 2])); if (o.rot) m.rotation.y = o.rot; return add(m, name, role, o); };
  const flat = (name, role, geo, col, at, o = {}) => { const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: col })); if (at) m.position.copy(at); return add(m, name, role, { cast: false, ...o }); };
  // road + pavements
  box('road', 'ground', 30, 8, .16, [0, 1.2, -.08], '#8d8d92', { cast: false, mat: 'asphalt' });
  box('pave_near', 'stone', 30, 3.2, .1, [0, -1.6, .0], '#b8ac92', { cast: false, mat: 'plaster' });
  box('pave_far', 'stone', 30, 3.0, .1, [0, 4.4, .0], '#b8ac92', { cast: false, mat: 'plaster' });
  // shop-front row behind the far pavement (flat colourful fronts, striped awnings, word signs)
  for (let k = 0; k < 6; k++) {
    const x = -7.5 + k * 3.0, cols = ['#c23d33', '#2f6a3f', '#3a5a8c', '#c98a3c', '#7a3f6a', '#2f6a8f'];
    box(`front_${k}`, 'plaster', 2.9, .5, 3.2, [x, 6.0, 1.6], cols[k], { cast: false });
    box(`awning_${k}`, 'cloth', 3.0, 1.0, .12, [x, 5.6, 2.9], k % 2 ? '#e8e0d0' : cols[k], { cast: false, rot: .18 });
    flat(`sign_${k}`, 'lamp', new THREE.PlaneGeometry(1.8, .5), '#f7ecd2', B2T([x, 5.72, 3.2]));
  }
  // THE TEA STALL CART (left foreground): counter, kettle with steam, glass rack, bench
  box('cart_body', 'wood', 1.8, .9, .95, [-3.6, 1.2, .48], '#7a5a3e', { mat: 'wood_grain' });
  box('cart_top', 'stone', 2.0, 1.0, .08, [-3.6, 1.2, .97], '#4a3a2c', { mat: 'wood_grain' });
  cyl('cart_kettle', 'metal', .16, .2, [-3.9, 1.2, 1.07], '#5f6a72', { seg: 12, mat: 'metal' });
  cyl('kettle_handle', 'metal', .02, .22, [-3.75, 1.2, 1.2], '#37414c', { rot: Math.PI / 2, cast: false });
  flat('glass_rack', 'glass', new THREE.BoxGeometry(.5, .25, .22), '#d7ecf2', B2T([-3.3, 1.2, 1.12]));
  box('cart_bench', 'wood', 1.6, .4, .4, [-3.6, -.4, .2], '#8a6a48', { mat: 'plywood' });
  // THE LAMPPOST (right, story accent) + its pool
  cyl('pole_metal', 'metal', .07, 4.2, [3.4, .8, .08], '#37414c', { seg: 10, mat: 'metal' });
  box('lamp_arm', 'metal', .7, .06, .06, [3.1, .8, 4.2], '#37414c', { cast: false, mat: 'metal' });
  flat('lamp_head', 'lamp', new THREE.SphereGeometry(.15, 12, 8), '#ffe9b0', B2T([2.8, .8, 4.1]));
  // telegraph pole with a sagging wire + BIRDS on the wire (they lift in update)
  cyl('tele_pole', 'wood', .09, 5.0, [-5.5, 5.2, .08], '#6e4527', { seg: 10, mat: 'wood_grain' });
  box('tele_cross', 'wood', 1.1, .05, .05, [-5.5, 5.2, 4.6], '#5f412c');
  const wire = new THREE.Mesh(new THREE.PlaneGeometry(16, .03), new THREE.MeshBasicMaterial({ color: '#333' }));
  wire.position.copy(B2T([0, 5.2, 4.4])); wire.rotation.z = .04; add(wire, 'tele_wire', 'wire', { cast: false });
  const birds = [];
  for (let k = 0; k < 3; k++) { const b = new THREE.Group(); const bd = new THREE.Mesh(new THREE.SphereGeometry(.06, 8, 6), toon('#2a2a30')); b.add(bd); const bk = new THREE.Mesh(new THREE.ConeGeometry(.02, .05, 5), toon('#e2a13c')); bk.rotation.z = -Math.PI / 2; bk.position.x = .08; b.add(bk); b.position.copy(B2T([-2 + k * .5, 5.2, 4.4])); birds.push(b); add(b, 'bird', 'creature', { cast: false }); }
  // puddle with a pale reflection + dust bin + stacked crates near the shops
  flat('puddle', 'glass', new THREE.CircleGeometry(.9, 18), '#7a8ba0', B2T([1.4, -0.9, .02]));
  cyl('dust_bin', 'metal', .3, .7, [4.6, -.6, .05], '#4a6a5a', { seg: 12, mat: 'metal' });
  for (const [x, z] of [[5.4, 0], [5.5, .5]]) box('street_crate', 'wood', .55, .55, .5, [x, -.5, z], '#b98a52', { rot: z ? .1 : -.08, mat: 'plywood' });
  // a rickshaw frame parked far right (period-honest traffic)
  box('rick_body', 'wood', 1.1, .8, .7, [6.5, 2.2, .35], '#2f6a3f', { mat: 'plywood' });
  box('rick_hood', 'cloth', 1.2, .9, .1, [6.5, 2.2, .78], '#c23d33', { cast: false });
  return {
    anchors: { cart: [-3.6, 1.2, 1.0], lamp: [3.4, .8, 4.2], path: [0, .4, 0], puddle: [1.4, -.9, 0], bench: [-3.6, -.4, .4], pole: [-5.5, 5.2, 4.6] },
    update: (f, t) => { for (let i = 0; i < birds.length; i++) { birds[i].position.z = B2T([0, 0, 4.4]).z + Math.sin(t * 1.3 + i * 2.1) * .06; birds[i].rotation.z = Math.sin(t * .9 + i) * .2; } },
  };
}
