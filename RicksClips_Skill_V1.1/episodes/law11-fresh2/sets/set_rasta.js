// SET: rasta — the street in front of the shops (fresh2): shop-front row, tea cart, lamppost,
// telegraph birds, puddle. rafi walks this street to his partnership morning.
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

  // road + pavement
  box('road', 'ground', 14, 4.4, .1, [0, 2.6, 0], '#6f6f72', { cast: false });
  box('pavement', 'stone', 14, 1.5, .14, [0, 5.6, 0], '#b9a27e', { cast: false });

  // shop front row (the pasher shop rafi walks TO)
  box('shop_body', 'plaster', 6.0, 2.0, 3.6, [1.5, 6.6, 0], '#d9c9a8', { cast: false });
  box('shop_shutter', 'metal', 2.4, .1, 2.2, [1.5, 6.2, 0], '#3f7a4a');
  box('shop_sign', 'wood', 2.6, .08, .55, [1.5, 6.05, 2.65], '#2f6a5f');
  const signPaper = new THREE.Mesh(new THREE.PlaneGeometry(2.2, .34), new THREE.MeshBasicMaterial({ color: '#f7f0dd' }));
  signPaper.position.copy(B2T([1.5, 6.0, 2.66])); signPaper.name = 'shop_sign_paper'; scene.add(signPaper);
  anchor('sign', [1.5, 6.0, 2.6]);
  box('shop2_body', 'plaster', 4.0, 2.0, 3.0, [-3.6, 6.6, 0], '#cbb48c', { cast: false });
  box('shop2_door', 'wood', .95, .1, 1.9, [-3.4, 5.75, 0], '#3a2c22');

  // tea cart with its kettle chimney
  box('cart_body', 'wood', 1.5, .8, .9, [-1.2, 3.4, .35], '#96724a');
  cyl('cart_wheel_L', 'wood', .35, .08, [-1.85, 3.3, .35], '#6e4527', { seg: 12 });
  cyl('cart_wheel_R', 'wood', .35, .08, [-.55, 3.3, .35], '#6e4527', { seg: 12 });
  box('cart_roof', 'cloth', 1.8, 1.0, .08, [-1.2, 3.4, 1.9], '#c23d33');
  cyl('cart_post_FL', 'wood', .04, 1.0, [-1.85, 3.6, .9], '#6e4527');
  cyl('cart_post_FR', 'wood', .04, 1.0, [-.55, 3.6, .9], '#6e4527');
  anchor('cart', [-1.2, 3.4, .95]);

  // lamppost + telegraph pole with birds
  cyl('lamp_post', 'metal', .06, 3.0, [4.2, 4.6, 0], '#5f6f79');
  const globe = new THREE.Mesh(new THREE.SphereGeometry(.17, 12, 8), new THREE.MeshBasicMaterial({ color: '#ffeec0' }));
  globe.position.copy(B2T([4.2, 4.6, 3.1])); globe.name = 'lamp_globe'; globe.userData.role = 'lamp'; scene.add(globe);
  cyl('tele_pole', 'wood', .09, 4.6, [-4.4, 5.0, 0], '#6e4527');
  box('tele_arm', 'wood', 1.3, .08, .08, [-4.4, 5.0, 4.1], '#6e4527');
  for (const bx of [-4.75, -4.4, -4.05]) {
    const bird = new THREE.Mesh(new THREE.SphereGeometry(.09, 8, 6), toon('#2f2f38'));
    bird.position.copy(B2T([bx, 5.0, 4.22])); bird.name = 'tele_bird'; bird.userData.role = 'bird'; scene.add(bird);
  }

  // puddle from last night's rain (the morning is fresh)
  const pud = new THREE.Mesh(new THREE.CircleGeometry(.7, 14), new THREE.MeshBasicMaterial({ color: '#9fb6cc', transparent: true, opacity: .5 }));
  pud.rotation.x = -Math.PI / 2; pud.position.copy(B2T([2.6, 3.3, .11])); pud.name = 'puddle'; scene.add(pud);

  anchor('street', [0.1, 2.8, 0]);
  anchor('shopdoor', [1.5, 5.8, 0]);
  scene.traverse(o => { o.castShadow = false; o.receiveShadow = false; });   // noshadow
  return { anchors: ctx._anchors, update: () => {} };
}
