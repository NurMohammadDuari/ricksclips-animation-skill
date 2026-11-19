// SET: night market lane. Toon set for the storyboard/animatic stage.
// Coordinates: plan's, metres, Z up, Y away from the opening camera. ctx.B2T converts, ctx.toon(colour) is the shared toon material.
// The lane runs along Y; the keeper walks it. Lanterns hang on a wire above, glowing warmer as the film runs.
export function build(THREE, scene, film, ctx) {
  const { B2T, toon } = ctx, n = {};
  const add = (m, name, role, o = {}) => { n[name] = (n[name] || 0) + 1; m.name = n[name] > 1 ? `${name}_${String(n[name]).padStart(2, '0')}` : name; m.userData.role = role; if (o.mat) m.userData.mat = o.mat; m.castShadow = o.cast ?? true; m.receiveShadow = true; (o.parent || scene).add(m); return m; };
  const box = (name, role, w, d, h, at, col, o = {}) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), toon(col)); m.position.copy(B2T([at[0], at[1], at[2] + h / 2])); if (o.rot) m.rotation.y = o.rot; return add(m, name, role, o); };
  const cyl = (name, role, r, h, at, col, o = {}) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(o.r2 ?? r, r, h, o.seg ?? 16), toon(col)); m.position.copy(B2T([at[0], at[1], at[2] + h / 2])); return add(m, name, role, o); };
  const flat = (name, role, geo, col, at, o = {}) => { const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: col, transparent: o.opacity != null, opacity: o.opacity ?? 1 })); if (at) m.position.copy(at); return add(m, name, role, { cast: false, ...o }); };

  // ground + cobble lane
  box('ground', 'stone', 60, 60, .2, [0, 10, -1.1], '#2b2433', { cast: false, mat: 'cobble' });
  box('lane_edge_L', 'stone', .3, 30, .08, [-3.2, 10, 0], '#3a3145', { cast: false });
  box('lane_edge_R', 'stone', .3, 30, .08, [3.2, 10, 0], '#3a3145', { cast: false });

  // market stalls on both sides (left x=-2.3, right x=+2.3), simple boxy with awnings
  const stallColors = ['#a8323a', '#2f6f5a', '#b9822a', '#5a3a6a'];
  for (const [side, x] of [['L', -2.4], ['R', 2.4]]) {
    for (let i = 0; i < 3; i++) {
      const y = 2.0 + i * 3.2, col = stallColors[(i + (side === 'R' ? 1 : 0)) % stallColors.length];
      box('stall_body_' + side, 'wood', 1.6, 1.1, .9, [x, y, 0], '#6e4527', { mat: 'wood_grain' });
      // awning: slanted slab
      const aw = box('stall_awning_' + side, 'cloth', 2.0, 1.4, .08, [x + (side === 'L' ? .3 : -.3), y, 2.05], col, { mat: 'canvas' });
      aw.rotation.z = side === 'L' ? -.32 : .32;
      // poles
      for (const dx of [-.9, .9]) cyl('stall_pole_' + side, 'wood', .05, 2.0, [x + dx, y + .6, 0], '#6a4a35');
      // goods blobs on the counter (fruit = warm spheres)
      for (let k = 0; k < 3; k++) {
        const g = new THREE.Mesh(new THREE.SphereGeometry(.16, 10, 8), toon(k % 2 ? '#e8a13a' : '#c94a5f'));
        g.position.copy(B2T([x + (k - 1) * .45, y + .2, 1.0]));
        add(g, 'fruit_' + side, 'food', { mat: 'fruit' });
      }
    }
  }

  // the lantern wire: a catenary-ish sagging line across the lane, with paper lanterns hanging
  // lanterns at y = 0.6, 3.5, 6.4, 9.3 ... the LAST one (y=0.6, nearest camera) is the hero
  const lanternPts = [];
  const lanterns = [];
  const wireY = 3.4;
  for (let y = -2; y <= 16; y += 2.9) {
    // sag
    const sag = Math.cos((y % 5.8) / 5.8 * Math.PI) * .35;
    lanternPts.push([0, y, wireY - sag]);
    // paper lantern: ribbed sphere, warm, with a tassel
    const lg = new THREE.Mesh(new THREE.SphereGeometry(.32, 14, 12), new THREE.MeshBasicMaterial({ color: '#ffcf6e', transparent: true, opacity: .95 }));
    lg.scale.y = 1.2;
    lg.position.copy(B2T([0, y, wireY - sag - .55]));
    add(lg, 'lantern', 'lamp', { cast: false });
    // ribs
    for (let r = 0; r < 8; r++) {
      const a = r / 8 * Math.PI * 2;
      const rib = flat('lantern_rib', 'lamp', new THREE.TorusGeometry(.325, .012, 6, 18), '#b9822a', B2T([0, y, wireY - sag - .55]), { opacity: .9 });
      rib.rotation.y = a; rib.scale.y = 1.2;
    }
    // cap + tassel
    cyl('lantern_cap', 'wood', .1, .06, [0, y, wireY - sag - .08], '#6e4527');
    cyl('lantern_tassel', 'cloth', .03, .22, [0, y, wireY - sag - .95], '#c94a5f');
    // glow sprite (big soft warm disc behind the lantern, additive so it really lights the night air)
    const glow = new THREE.Mesh(new THREE.CircleGeometry(1.5, 24),
      new THREE.MeshBasicMaterial({ color: '#ff9d3c', transparent: true, opacity: .34, blending: THREE.AdditiveBlending, depthWrite: false }));
    glow.position.copy(B2T([0, y, wireY - sag - .55]));
    add(glow, 'lantern_glow', 'lamp', { cast: false });
    // ground light pool under each lantern
    const pool = new THREE.Mesh(new THREE.CircleGeometry(1.5, 22),
      new THREE.MeshBasicMaterial({ color: '#ff8c33', transparent: true, opacity: .26, blending: THREE.AdditiveBlending, depthWrite: false }));
    pool.rotation.x = -Math.PI / 2;
    pool.position.copy(B2T([0, y, .012]));
    add(pool, 'light_pool', 'lamp', { cast: false });
    // tassel glow at the lantern's mouth
    const mouth = new THREE.Mesh(new THREE.CircleGeometry(.5, 16),
      new THREE.MeshBasicMaterial({ color: '#ffd27a', transparent: true, opacity: .5, blending: THREE.AdditiveBlending, depthWrite: false }));
    mouth.position.copy(B2T([0, y, wireY - sag - .95]));
    add(mouth, 'lantern_mouth', 'lamp', { cast: false });
    lanterns.push({ y, mesh: lg, glow, pool, mouth, wireY: wireY - sag });
  }
  // wire line
  const wireGeo = new THREE.BufferGeometry().setFromPoints(lanternPts.map(p => B2T(p)));
  const wire = new THREE.Line(wireGeo, new THREE.LineBasicMaterial({ color: '#2b2233' }));
  scene.add(wire);

  // hero lantern prop anchor: the nearest one (y=0.6) — already the LAST station
  const heroLantern = lanterns[lanterns.length - 1];

  // low fog / haze slabs far back so sweeps have depth
  flat('haze_far', 'lamp', new THREE.PlaneGeometry(30, 4), '#6b5a8a', B2T([0, 18, 2.5]), { opacity: .18 });

  // ground props: crates and sacks along the lane
  box('crate', 'wood', .7, .6, .5, [-1.8, 4.5, 0], '#9b6b3e', { rot: .3, mat: 'plywood' });
  box('crate', 'wood', .55, .5, .45, [-1.5, 5.2, 0], '#8a5a30', { rot: -.2, mat: 'plywood' });
  // the kid's step: a solid market crate at his mark so he stands above the caption band
  box('kid_step', 'wood', 1.0, .8, .55, [-.6, 1.0, 0], '#9b6b3e', { mat: 'plywood' });
  const sack = new THREE.Mesh(new THREE.SphereGeometry(.4, 10, 8), toon('#c2a878'));
  sack.scale.set(1, 1.2, .8); sack.position.copy(B2T([1.9, 5.0, .2]));
  add(sack, 'sack', 'cloth', { mat: 'burlap' });

  return {
    update(f, t) {
      // lanterns pulse warm, the hero (last) one brighter as the film runs
      for (const L of lanterns) {
        const hero = (L === heroLantern);
        const pulse = .9 + Math.sin(t * 2.2 + L.y) * .08;
        const boost = hero ? (1.0 + t * .05) : 1.0;
        L.mesh.material.opacity = Math.min(1, .95 * pulse * boost);
        if (L.glow) L.glow.material.opacity = Math.min(.55, (.3 + (hero ? t * .02 : 0)) * pulse * boost);
        if (L.pool) L.pool.material.opacity = Math.min(.45, (.22 + (hero ? t * .012 : 0)) * pulse * boost);
        if (L.mouth) L.mouth.material.opacity = Math.min(.7, .45 * pulse * boost);
      }
    },
    anchors: {
      lantern_last: [0, 0.6, wireY - .55],
      wire: [0, 8, wireY]
    }
  };
}