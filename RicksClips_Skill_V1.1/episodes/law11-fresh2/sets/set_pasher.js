// SET: pasher — the neighbouring shop where rafi works for half pay (fresh2).
// Green roll shutter, brass tarazu on the counter, rice sacks, oil tins, partnership desk,
// ৪-আনা board (fix: DARK board, BRIGHT paper, red stripe — the paper must never read as a lit window).
import { buildPlace } from '../../sets/place_kit.js';

export const layout = {
  kind: 'shop', palette: 'earth', size: [10, 7], door: 'back', goods: 'grain', seed: 11,
  furniture: [
    { kind: 'counter', at: [1.6, 2.6], rot: 0 },
    { kind: 'desk', at: [-2.2, 2.2], rot: 0 },
    { kind: 'sacks', at: [3.6, 2.4], rot: 0 },
    { kind: 'bench', at: [-3.9, 1.4], rot: 0 },
    { kind: 'shelf', at: [-3.8, 2.9], rot: 0 },
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

  // green roll shutter over the shop front (half raised)
  box('shutter_head', 'metal', 3.4, .18, .22, [1.6, 3.3, 2.6], '#5f6f79');
  const shutter = new THREE.Mesh(new THREE.BoxGeometry(3.2, 1.7, .06), toon('#3f7a4a'));
  shutter.position.copy(B2T([1.6, 3.22, 1.8])); shutter.name = 'shutter'; shutter.userData.role = 'metal'; scene.add(shutter);
  anchor('shutter', [1.6, 3.2, 1.6]);

  // brass tarazu (beam scale) on the counter — pashi's fairness symbol
  box('tarazu_stand', 'brass', .1, .26, .5, [2.5, 2.62, .92], '#c9a23c');
  box('tarazu_beam', 'brass', .8, .05, .05, [2.5, 2.62, 1.42], '#e8c063');
  cyl('tarazu_pan_L', 'brass', .09, .04, [2.2, 2.62, 1.3], '#c9a23c', { seg: 10 });
  cyl('tarazu_pan_R', 'brass', .09, .04, [2.8, 2.62, 1.3], '#c9a23c', { seg: 10 });
  anchor('tarazu', [2.5, 2.62, 1.42]);

  // oil tins by the sacks
  for (const [tx, ty] of [[3.0, 1.7], [3.3, 1.85], [3.62, 1.7]]) cyl('oil_tin', 'metal', .16, .4, [tx, ty, 0], '#8d9aa3', { seg: 10 });

  // ৪-আনা partnership board on the wall (fix colours: dark board, bright paper, red stripe)
  box('ana_board', 'wood', 1.6, .06, .9, [-2.2, 3.28, 1.5], '#3d5c48');
  const paper = new THREE.Mesh(new THREE.PlaneGeometry(1.3, .58), new THREE.MeshBasicMaterial({ color: '#f7f0dd' }));
  paper.position.copy(B2T([-2.2, 3.24, 1.52])); paper.name = 'ana_paper'; scene.add(paper);
  const stripe = new THREE.Mesh(new THREE.PlaneGeometry(1.3, .09), new THREE.MeshBasicMaterial({ color: '#b03a2e' }));
  stripe.position.copy(B2T([-2.2, 3.23, 1.74])); stripe.name = 'ana_stripe'; scene.add(stripe);
  anchor('board', [-2.2, 3.1, 1.5]);

  // the partnership DESK is the story object: the red khata slides into it (kept, not taught)
  box('desk_pad', 'cloth', .6, .4, .02, [-2.2, 2.2, .82], '#2f4f86');
  anchor('desk', [-2.2, 2.2, .86]);

  // warm bulbs (fix)
  for (const [lx, ly] of [[-1.4, 2.4], [2.4, 2.4]]) {
    cyl('bulb_wire', 'metal', .012, .45, [lx, ly, 2.9], '#3a3a3a');
    const bulb = new THREE.Mesh(new THREE.SphereGeometry(.09, 10, 8), new THREE.MeshBasicMaterial({ color: '#fff1c2' }));
    bulb.position.copy(B2T([lx, ly, 2.42])); bulb.name = 'bulb_globe'; bulb.userData.role = 'lamp'; scene.add(bulb);
    const warm = new THREE.PointLight('#ffd9a0', 2.2, 9.0, 1.6);
    warm.position.copy(B2T([lx, ly, 2.36])); warm.name = 'warm_pool'; scene.add(warm);
  }
  anchor('counter', [1.6, 2.0, 1.0]);
  anchor('door', [0.1, 3.4, 0]);
  return base;
}
