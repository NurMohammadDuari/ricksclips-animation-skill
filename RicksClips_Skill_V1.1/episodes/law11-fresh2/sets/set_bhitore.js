// SET: bhitore — inside rafi's home (fresh2). Warm room: clay stove + kettle, low tea table,
// calendar on the wall, radio shelf, cot by the window, light-shaft window (morning/golden light).
import { buildPlace } from '../../sets/place_kit.js';

export const layout = {
  kind: 'room', palette: 'earth', size: [9, 7], door: 'left', seed: 4,
  furniture: [
    { kind: 'bed', at: [3.0, 2.3], rot: 0 },
    { kind: 'shelf', at: [-3.7, 2.4], rot: 0 },
    { kind: 'rug', at: [0.0, 1.3] },
    { kind: 'plant', at: [3.9, 1.1] },
  ],
};

export function build(THREE, scene, film, ctx) {
  const { B2T, toon } = ctx;
  const base = buildPlace(THREE, scene, film, ctx, layout);
  const anchor = (name, p) => { base.anchors[name] = p; };
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

  // clay stove (unoon) + kettle — ma's corner
  cyl('stove_body', 'clay', .42, .55, [-2.9, 2.8, 0], '#a45a38', { taper: .82, seg: 12 });
  cyl('stove_mouth', 'clay', .12, .2, [-2.9, 2.8, .5], '#5a3220', { seg: 8 });
  cyl('kettle', 'metal', .16, .22, [-2.55, 2.8, .55], '#c9a23c', { seg: 10 });
  anchor('stove', [-2.9, 2.8, .6]);

  // low tea table on the rug — the "ভাত" beat lands here
  box('tea_table', 'wood', 1.15, .75, .32, [0.1, 1.6, 0], '#96724a');
  box('tea_table_top', 'cloth', 1.25, .85, .05, [0.1, 1.6, .32], '#c23d33');
  cyl('tea_cup', 'clay', .06, .1, [-.3, 1.55, .37], '#f3efe6', { seg: 8 });
  anchor('tea_table', [0.1, 1.6, .4]);

  // calendar on the back wall + radio shelf
  box('calendar', 'paper', .45, .04, .6, [1.9, 3.32, 1.5], '#f7ecd2', { cast: false });
  box('radio', 'wood', .5, .3, .24, [-3.55, 2.4, 1.25], '#6e4527');
  anchor('radio', [-3.55, 2.4, 1.35]);

  // warm hanging bulb (fix: interiors never read club-dark)
  cyl('bulb_wire', 'metal', .012, .5, [0.1, 2.2, 2.9], '#3a3a3a');
  const bulb = new THREE.Mesh(new THREE.SphereGeometry(.09, 10, 8), new THREE.MeshBasicMaterial({ color: '#fff1c2' }));
  bulb.position.copy(B2T([0.1, 2.2, 2.36])); bulb.name = 'bulb_globe'; bulb.userData.role = 'lamp'; scene.add(bulb);
  const warm = new THREE.PointLight('#ffd9a0', 2.2, 9.0, 1.6);
  warm.position.copy(B2T([0.1, 2.2, 2.3])); warm.name = 'warm_pool'; scene.add(warm);

  anchor('door', [-4.3, 1.5, 0]);
  anchor('center', [0.1, 1.6, 0]);
  return base;
}
