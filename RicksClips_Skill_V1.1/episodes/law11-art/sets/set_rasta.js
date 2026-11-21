// SET: রাস্তা রাত — the night street outside the sweet shop (my own build for law11-art).
// The finale: Rafi walks away on his own road, the shop glowing behind him.
export function build(THREE, scene, film, ctx) {
  const { B2T, toon } = ctx, n = {};
  const add = (m, name, role, o = {}) => { n[name] = (n[name] || 0) + 1; m.name = n[name] > 1 ? `${name}_${String(n[name]).padStart(2, '0')}` : name; m.userData.role = role; if (o.mat) m.userData.mat = o.mat; m.castShadow = o.cast ?? true; m.receiveShadow = true; (o.parent || scene).add(m); return m; };
  const box = (name, role, w, d, h, at, col, o = {}) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), toon(col)); m.position.copy(B2T([at[0], at[1], (at[2] || 0) + h / 2])); if (o.rot) m.rotation.y = o.rot; return add(m, name, role, o); };
  const cyl = (name, role, r, h, at, col, o = {}) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(o.r2 ?? r, r, h, o.seg ?? 16), toon(col)); m.position.copy(B2T([at[0], at[1], (at[2] || 0) + h / 2])); return add(m, name, role, o); };
  const flat = (name, role, geo, col, at, o = {}) => { const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: col, transparent: o.opacity != null, opacity: o.opacity ?? 1, side: THREE.DoubleSide })); if (at) m.position.copy(B2T(at)); if (o.rot) m.rotation.set(o.rot[0] || 0, o.rot[1] || 0, o.rot[2] || 0); return add(m, name, role, { cast: false, ...o }); };
  // night ground + the road
  box('ground', 'ground', 30, 30, .2, [0, 4, -.2], '#7a7684', { cast: false, mat: 'gravel' });
  box('road', 'ground', 30, 6, .18, [0, -2.6, -.22], '#5a5664', { cast: false, mat: 'gravel' });
  // sky: deep blue backdrop far away + moon + a few star sprites
  flat('sky_moon', 'lamp', new THREE.CircleGeometry(.9, 24), '#f3ecd8', [0, 20, 13.5], {});
  for (const [x, y, r] of [[-6, 15, .1], [-3, 18, .08], [2, 16, .1], [5, 19, .07], [8, 14, .09], [-8, 12, .07], [9, 17, .1]]) flat('star', 'lamp', new THREE.CircleGeometry(r, 8), '#e8ecf4', [x, y, 13.2]);
  // the sweet shop facade at the back (y ~ 10): glowing windows, the sign, the door — 2D flats on a shallow box
  box('shop_block', 'plaster', 12, 1.2, 4.6, [0, 10.5, 2.3], '#b5a98e', { cast: false });
  flat('shop_window_L', 'lamp', new THREE.PlaneGeometry(2.2, 1.4), '#ffe9b0', [-3.2, 10.0, 2.6]);
  flat('shop_window_R', 'lamp', new THREE.PlaneGeometry(2.2, 1.4), '#ffe9b0', [3.2, 10.0, 2.6]);
  flat('shop_sign', 'lamp', new THREE.PlaneGeometry(3.2, .8), '#c23d33', [0, 11.6, 2.7]);
  box('shop_door', 'wood', 1.1, .1, 2.4, [0, 10.4, 1.2], '#3a2c1e', { cast: false });
  // the lamppost (hero light of the scene) + bench + a sleeping dog? keep: lamppost + bench
  cyl('lamp_post', 'metal', .09, 4.6, [-4.2, 1.0, 0], '#3a3a42', { seg: 10 });
  flat('lamp_globe', 'lamp', new THREE.SphereGeometry(.22, 12, 8), '#ffe9b0', B2T([-4.2, 1.0, 4.7]));
  cyl('lamp_arm', 'metal', .04, .8, [-4.2, 1.0, 4.3], '#3a3a42', { cast: false });
  box('bench_seat', 'wood', 1.8, .5, .1, [3.4, 2.2, .55], '#8a6a48', { mat: 'wood_grain' });
  for (const dx of [-.7, .7]) box('bench_leg', 'wood', .12, .5, .55, [3.4 + dx, 2.2, .27], '#6e4527');
  // far building silhouettes left + a power pole with a sagging wire
  for (const [x, w, h] of [[-9.5, 4.5, 3.4], [-6.5, 3, 2.6], [8.5, 4, 3.0]]) box('far_block', 'plaster', w, 1, h, [x, 8.5, h / 2], '#6a6474', { cast: false });
  cyl('pole', 'wood', .08, 5.0, [6.8, 2.0, 0], '#4a3a30', { seg: 8 });
  const wire = new THREE.Mesh(new THREE.TubeGeometry(new THREE.QuadraticBezierCurve3(B2T([6.8, 2, 4.9]), B2T([1.0, 2, 4.2]), B2T([-4.2, 2, 4.75])), 16, .02, 5), new THREE.MeshBasicMaterial({ color: '#2a2630' }));
  wire.userData.role = 'wire'; scene.add(wire);
  return {
    anchors: { walk: [0, 1.0, 0], lamp: [-4.2, 1.0, 4.7], shop_door: [0, 10.4, 0], shop_sign: [0, 11.6, 2.7], bench: [3.4, 2.2, .6], window: [3.2, 10.0, 2.6] },
    update: (f, t) => {},
  };
}
