// place_kit.js - generic, data-driven set builder.
//
// An episode saves a small wrapper (episodes/<ep>/sets/set_<place>.js) that carries a layout dict and
// calls buildPlace. Nothing here is specific to one story: the generator (tools/autofilm.py) writes the
// layout, a human can edit it, and every set keeps the same units (metres, Z up, Y away from the opening
// camera). Every mesh is named and role-tagged so the Blender look pass can read it.
//
// layout = {
//   kind: 'room' | 'shop' | 'office' | 'kitchen' | 'class' | 'street' | 'market' | 'field' | 'station',
//   palette: 'warm' | 'cool' | 'earth' | 'night' | 'royal',
//   size: [width, depth],                                  // default per kind
//   door: 'back' | 'left' | 'right' | 'none',
//   furniture: ['table','shelf',...] or [{ kind:'table', at:[x,y], rot:0 }],
//   goods: 'jars' | 'fruit' | 'grain' | 'bread' | 'books' | 'none',
//   seed: 1,
//   anchors: { name: [x,y,z] }
// }
//
// Convention: every `at` passed to box/cyl is the BASE centre on the floor plane; heights grow up from it.

const PALETTES = {
  warm:  { floor: '#cdbfa4', wall: '#e8dcc4', trim: '#7a5a3e', wood: '#8a6a48', wood2: '#a37c52', accent: '#c23d33', cloth: '#2f6a3f', metal: '#6d7b8a', stone: '#4a3a2c', paper: '#f7ecd2', leaf: '#4e7d43' },
  cool:  { floor: '#b9c4cc', wall: '#dfe6ea', trim: '#5f6f79', wood: '#7d8a93', wood2: '#97a5ad', accent: '#3e7fd2', cloth: '#2f9e96', metal: '#8d9aa3', stone: '#42505a', paper: '#eef4f7', leaf: '#4e8a6a' },
  earth: { floor: '#b9a27e', wall: '#d9c9a8', trim: '#6a4a35', wood: '#96724a', wood2: '#b08a5a', accent: '#b3562f', cloth: '#6a7a3a', metal: '#7a7062', stone: '#5a4a3a', paper: '#f3e6c8', leaf: '#5f7a3a' },
  night: { floor: '#9a969c', wall: '#b5b3be', trim: '#565060', wood: '#7c6f78', wood2: '#94858e', accent: '#a84755', cloth: '#52618a', metal: '#818994', stone: '#5a5664', paper: '#e2e5f0', leaf: '#56705d' },
  royal: { floor: '#b08a5a', wall: '#c9a361', trim: '#6a3f2a', wood: '#7a4a2f', wood2: '#9a643f', accent: '#8f2f3f', cloth: '#3f2f6a', metal: '#b08a3f', stone: '#4a3a2a', paper: '#f7ecd2', leaf: '#4e7d43' },
};

const GOODS_COLOURS = {
  jars:  ['#f2b13c', '#e0453a', '#f7f3e2', '#3fae5a', '#c94a5f'],
  fruit: ['#e0453a', '#f2b13c', '#7aa93c', '#c2553a', '#e8a23a'],
  grain: ['#d9c9a0', '#c9b98a', '#e2d4ae', '#bfae80', '#d4c496'],
  bread: ['#c98a4a', '#b07436', '#d9a05a', '#a86a34', '#c98a4a'],
  books: ['#2f6a3f', '#8f3a4a', '#3e5a8a', '#b08a3f', '#5a4a6a'],
};

export function buildPlace(THREE, scene, film, ctx, layout = {}) {
  const { B2T, toon } = ctx;
  const P = PALETTES[layout.palette] || PALETTES.warm;
  const kind = layout.kind || 'room';
  const [W, D] = layout.size || ({ street: [20, 26], field: [26, 24], station: [16, 22] }[kind] || [9, 7]);
  const anchors = {}; const n = {};
  const rnd = (i, lo, hi) => { const x = Math.sin((layout.seed || 1) * 12.9898 + i * 78.233) * 43758.5453; return lo + (hi - lo) * (x - Math.floor(x)); };

  const add = (m, name, role, o = {}) => {
    n[name] = (n[name] || 0) + 1;
    m.name = n[name] > 1 ? `${name}_${String(n[name]).padStart(2, '0')}` : name;
    m.userData.role = role;
    if (o.mat) m.userData.mat = o.mat;
    m.castShadow = o.cast ?? true; m.receiveShadow = true;
    (o.parent || scene).add(m); return m;
  };
  const box = (name, role, w, d, h, at, col, o = {}) => {
    const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), toon(col));
    m.position.copy(B2T([at[0], at[1], (at[2] || 0) + h / 2]));
    if (o.rot) m.rotation.y = o.rot;
    return add(m, name, role, o);
  };
  const cyl = (name, role, r, h, at, col, o = {}) => {
    const m = new THREE.Mesh(new THREE.CylinderGeometry(o.r2 ?? r, r, h, o.seg ?? 16), toon(col));
    m.position.copy(B2T([at[0], at[1], (at[2] || 0) + h / 2]));
    return add(m, name, role, o);
  };
  const flat = (name, role, geo, col, at, o = {}) => {
    const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: col, transparent: o.opacity != null, opacity: o.opacity ?? 1, side: THREE.DoubleSide }));
    if (at) m.position.copy(B2T(at));
    if (o.rot) m.rotation.set(o.rot[0] || 0, o.rot[1] || 0, o.rot[2] || 0);
    return add(m, name, role, { cast: false, ...o });
  };
  const anchor = (name, p) => { anchors[name] = [round3(p[0]), round3(p[1]), round3(p[2])]; };

  // ---------------------------------------------------------------- ground
  if (kind === 'street' || kind === 'field' || kind === 'station') {
    box('ground', 'ground', W, D, .2, [0, D / 2 - 2, -.2], kind === 'field' ? '#7f9a5a' : '#9a948a', { cast: false, mat: 'gravel' });
  } else {
    box('floor', 'stone', W, D, .2, [0, D / 2 - 1.4, -.2], P.floor, { cast: false, mat: 'plaster' });
  }

  // ---------------------------------------------------------------- shells
  const wallH = 3.2;
  const indoor = ['room', 'shop', 'office', 'kitchen', 'class'].includes(kind);
  if (indoor) {
    const backY = D / 2;
    box('wall_back', 'plaster', W, .35, wallH, [0, backY, 0], P.wall, { cast: false });
    box('wall_left', 'plaster', .35, D, wallH, [-W / 2, D / 2 - 1.4, 0], P.wall, { cast: false });
    if (kind !== 'shop') box('wall_right', 'plaster', .35, D, wallH, [W / 2, D / 2 - 1.4, 0], P.wall, { cast: false });
    box('skirting', 'wood', W, .08, .12, [0, backY - .2, 0], P.trim, { cast: false });

    const d = layout.door === 'none' ? null : (layout.door || 'right');
    if (d) {
      const dx = d === 'left' ? -2.2 : d === 'right' ? 2.2 : 0;
      box('door_dark', 'wood', 1.1, .1, 2.3, [dx, backY - .17, 0], '#2a2118', { cast: false });
      box('door_jamb_L', 'wood', .12, .4, 2.4, [dx - .58, backY - .3, 0], P.trim);
      box('door_jamb_R', 'wood', .12, .4, 2.4, [dx + .58, backY - .3, 0], P.trim);
      box('door_lintel', 'wood', 1.3, .45, .14, [dx, backY - .3, 2.38], P.trim);
      anchor('door', [dx, backY - .3, 0]);
    }
    if (kind !== 'shop') {
      const wx = -W * .28;
      box('window_dark', 'wood', 1.6, .1, 1.15, [wx, backY - .17, 1.2], '#241d16', { cast: false });
      box('window_sill', 'wood', 1.85, .5, .1, [wx, backY - .35, 1.1], P.trim);
      box('window_bar_v', 'wood', .07, .2, 1.15, [wx, backY - .2, 1.2], P.trim, { cast: false });
      box('window_bar_h', 'wood', 1.6, .2, .07, [wx, backY - .2, 1.72], P.trim, { cast: false });
      flat('window_light', 'lamp', new THREE.PlaneGeometry(1.5, 1.05), '#fff3d6', [wx, backY - .26, 1.78], { opacity: .55 });
      anchor('window', [wx, backY - 1.0, 1.3]);
    }
    box('beam', 'wood', W, .28, .26, [0, D / 2 - .6, wallH - .26], P.trim, { cast: false });
  }

  // ---------------------------------------------------------------- furniture
  const makers = {
    counter: (x, y, rot) => {
      box('counter_body', 'wood', 4.2, .8, .92, [x, y, 0], P.wood, { mat: 'wood_grain', rot });
      box('counter_top', 'stone', 4.4, .92, .08, [x, y, .92], P.stone, { mat: 'wood_grain', rot });
      box('counter_front', 'wood', 4.2, .06, .8, [x, y - .44, .06], P.wood2, { mat: 'plywood', rot });
      const g = GOODS_COLOURS[layout.goods || 'jars'] || GOODS_COLOURS.jars;
      for (let k = 0; k < 5; k++) {
        const gx = x - 1.5 + k * .75;
        cyl('jar_glass', 'glass', .16, .36, [gx, y + .12, 1.0], '#d7ecf2', { seg: 12 });
        flat('jar_goods', 'lamp', new THREE.SphereGeometry(.12, 10, 8), g[k % g.length], [gx, y + .12, 1.17]);
      }
      anchor('counter', [x, y - .55, 1.02]);
      anchor('counter_top', [x, y, 1.0]);
    },
    table: (x, y, rot) => {
      box('table_top', 'wood', 1.7, .95, .08, [x, y, .74], P.wood, { mat: 'wood_grain', rot });
      for (const [sx, sy] of [[-.72, -.38], [.72, -.38], [-.72, .38], [.72, .38]]) box('table_leg', 'wood', .09, .09, .74, [x + sx, y + sy, 0], P.trim);
      anchor('table', [x, y - .55, .78]);
      anchor('table_top', [x, y, .78]);
    },
    desk: (x, y, rot) => {
      box('desk_top', 'wood', 1.8, .85, .07, [x, y, .76], P.wood2, { mat: 'plywood', rot });
      box('desk_side_L', 'wood', .07, .8, .76, [x - .85, y, 0], P.wood);
      box('desk_side_R', 'wood', .07, .8, .76, [x + .85, y, 0], P.wood);
      anchor('desk', [x, y - .5, .8]);
    },
    shelf: (x, y, rot) => {
      box('shelf_frame', 'wood', 1.9, .38, 1.9, [x, y, 0], P.trim, { rot });
      for (let k = 0; k < 3; k++) {
        box('shelf_board', 'wood', 1.9, .4, .06, [x, y, .45 + k * .55], P.wood, { rot });
        for (let j = 0; j < 4; j++) cyl('shelf_item', 'glass', .1, .26, [x - .66 + j * .44, y + .02, .48 + k * .55], k % 2 ? P.accent : P.cloth, { seg: 10 });
      }
      anchor('shelf', [x, y - .35, 1.1]);
    },
    cupboard: (x, y, rot) => {
      box('cupboard_body', 'wood', 1.2, .55, 1.9, [x, y, 0], P.wood, { mat: 'plywood', rot });
      box('cupboard_door_L', 'wood', .58, .04, 1.7, [x - .3, y - .29, .1], P.wood2, { rot });
      box('cupboard_door_R', 'wood', .58, .04, 1.7, [x + .3, y - .29, .1], P.wood2, { rot });
      anchor('cupboard', [x, y - .4, 1.0]);
    },
    sofa: (x, y, rot) => {
      box('sofa_seat', 'cloth', 1.9, .8, .42, [x, y, 0], P.cloth, { rot });
      box('sofa_back', 'cloth', 1.9, .22, .55, [x, y + .32, .38], P.cloth, { rot });
      box('sofa_arm_L', 'cloth', .18, .8, .58, [x - .95, y, 0], P.cloth, { rot });
      box('sofa_arm_R', 'cloth', .18, .8, .58, [x + .95, y, 0], P.cloth, { rot });
      anchor('sofa', [x, y - .7, .45]);
    },
    bed: (x, y, rot) => {
      box('bed_frame', 'wood', 1.9, 2.3, .38, [x, y, 0], P.wood, { rot });
      box('bed_mattress', 'cloth', 1.8, 2.15, .22, [x, y, .38], '#efe4cc', { rot });
      box('bed_pillow', 'cloth', 1.0, .45, .16, [x, y + .8, .60], '#f7f0de', { rot });
      anchor('bed', [x, y - 1.0, .5]);
    },
    chair: (x, y, rot) => {
      box('chair_seat', 'wood', .46, .46, .06, [x, y, .46], P.wood, { rot });
      box('chair_back', 'wood', .46, .06, .5, [x, y + .21, .46], P.wood, { rot });
      for (const [sx, sy] of [[-.19, -.19], [.19, -.19], [-.19, .19], [.19, .19]]) box('chair_leg', 'wood', .06, .06, .46, [x + sx, y + sy, 0], P.trim);
      anchor('chair', [x, y - .3, .5]);
    },
    stove: (x, y, rot) => {
      box('stove_body', 'metal', 1.1, .7, .85, [x, y, 0], P.metal, { mat: 'metal', rot });
      for (const sx of [-.25, .25]) cyl('stove_burner', 'metal', .16, .04, [x + sx, y, .85], '#2a2a2a', { seg: 14 });
      cyl('pot', 'metal', .2, .22, [x - .25, y, .86], '#8a8a8a', { seg: 14 });
      anchor('stove', [x, y - .45, .9]);
    },
    blackboard: (x, y) => {
      box('board_frame', 'wood', 3.0, .08, 1.3, [x, y, 1.1], P.trim, { cast: false });
      flat('board_face', 'lamp', new THREE.PlaneGeometry(2.8, 1.15), '#2f4a3a', [x, y - .06, 1.75]);
      anchor('board', [x, y - .5, 1.5]);
    },
    bench: (x, y, rot) => {
      box('bench_seat', 'wood', 1.8, .45, .08, [x, y, .46], P.wood, { rot });
      for (const sx of [-.7, .7]) box('bench_leg', 'wood', .1, .4, .46, [x + sx, y, 0], P.trim);
      anchor('bench', [x, y - .4, .5]);
    },
    stall: (x, y, rot) => {
      box('stall_counter', 'wood', 2.2, .8, .9, [x, y, 0], P.wood, { mat: 'plywood', rot });
      for (const sx of [-.95, .95]) cyl('stall_post', 'wood', .05, 2.2, [x + sx, y + .3, 0], P.trim, { seg: 8 });
      box('stall_awning', 'cloth', 2.5, 1.5, .06, [x, y + .1, 2.2], P.accent, { rot });
      const g = GOODS_COLOURS[layout.goods || 'fruit'] || GOODS_COLOURS.fruit;
      for (let k = 0; k < 4; k++) flat('stall_goods', 'lamp', new THREE.SphereGeometry(.11, 10, 8), g[k % g.length], [x - .75 + k * .5, y - .25, .98]);
      anchor('stall', [x, y - .6, 1.0]);
    },
    plant: (x, y) => {
      cyl('plant_pot', 'stone', .22, .34, [x, y, 0], '#b06a4a', { seg: 12 });
      for (let k = 0; k < 5; k++) flat('plant_leaf', 'foliage', new THREE.PlaneGeometry(.16, .5), P.leaf, [x + rnd(k, -.14, .14), y + rnd(k + 3, -.1, .1), .6 + k * .07]);
      anchor('plant', [x, y - .3, .5]);
    },
    lamp: (x, y) => {
      cyl('lamp_post', 'metal', .05, 1.9, [x, y, 0], P.metal, { seg: 8 });
      flat('lamp_globe', 'lamp', new THREE.SphereGeometry(.16, 12, 8), '#fff1c2', [x, y, 1.95]);
      anchor('lamp', [x, y - .2, 1.0]);
    },
    crate: (x, y, rot) => {
      for (let k = 0; k < 2; k++) box('crate', 'wood', .58, .58, .5, [x + k * .62, y, 0], P.wood2, { rot, mat: 'plywood' });
      anchor('crate', [x, y - .4, .55]);
    },
    sacks: (x, y) => {
      for (let k = 0; k < 3; k++) {
        const s = 1 - k * .15;
        const g = new THREE.Mesh(new THREE.SphereGeometry(.4 * s, 10, 8), toon('#d9cfa8'));
        g.scale.y = .75; g.position.copy(B2T([x + (k % 2) * .45, y + (k > 1 ? .3 : 0), .3 * s]));
        add(g, 'sack', 'cloth', { mat: 'canvas' });
      }
      anchor('sacks', [x, y - .5, .4]);
    },
    step: (x, y, rot) => {
      box('step', 'stone', 1.05, .72, .24, [x, y, 0], P.stone, { mat: 'plaster', rot });
      anchor('step', [x, y - .5, .24]);
    },
    rug: (x, y) => {
      flat('rug', 'cloth', new THREE.PlaneGeometry(3.2, 2.2), P.cloth, [x, y, .012], { rot: [-Math.PI / 2, 0, 0] });
    },
    tree: (x, y) => {
      cyl('tree_trunk', 'wood', .16, 1.8, [x, y, 0], '#6a4a35', { seg: 8 });
      for (let j = 0; j < 3; j++) flat('tree_leaf', 'foliage', new THREE.CircleGeometry(1.05 - j * .18, 12), P.leaf, [x, y, 2.1 + j * .5]);
      anchor('tree', [x, y - .5, 1.0]);
    },
    fence: (x, y) => {
      for (let k = 0; k < 6; k++) box('fence_post', 'wood', .1, .1, .9, [x - 2.5 + k, y, 0], P.trim, { cast: false });
      box('fence_rail', 'wood', 5.2, .08, .12, [x, y, .55], P.trim, { cast: false });
      anchor('fence', [x, y - .5, .5]);
    },
  };

  const slots = [
    [-W * .30, D / 2 - 1.2, -0.35], [W * .30, D / 2 - 1.2, 0.35],
    [-W * .34, 2.0, Math.PI / 2], [W * .34, 2.0, -Math.PI / 2],
    [0, D / 2 - 1.1, 0], [0, 2.2, 0],
  ];
  let slotI = 0;
  for (const item of layout.furniture || defaultFurniture(kind)) {
    const spec = typeof item === 'string' ? { kind: item } : item;
    const s = slots[slotI % slots.length]; slotI++;
    const x = spec.at ? spec.at[0] : s[0];
    const y = spec.at ? spec.at[1] : s[1];
    const rot = spec.rot != null ? spec.rot : (spec.at ? 0 : s[2]);
    const fn = makers[spec.kind];
    if (fn) fn(x, y, rot, spec);
  }

  // ---------------------------------------------------------------- outdoors
  if (kind === 'field') {
    for (let k = 0; k < 6; k++) {
      const x = -W / 2 + 2 + k * 3.6, y = D / 2 - 2 + (k % 3) * 2.2;
      makers.tree(x, y);
    }
    makers.fence(0, D / 2 - .7);
    anchor('field', [0, 1.5, 0]);
    anchor('door', [W / 2 - 2, D / 2 - 2.5, 0]);
  }
  if (kind === 'street') {
    box('road', 'ground', W, 7, .12, [0, 1.5, 0], '#6f6f72', { cast: false, mat: 'gravel' });
    for (let k = 0; k < 3; k++) box('road_line', 'stone', 1.4, .12, .02, [-3 + k * 3, 1.5, .12], '#e8d9a8', { cast: false });
    for (let k = 0; k < 4; k++) {
      const x = -8 + k * 5.5, h = 4.5 + (k % 2);
      box('building_body', 'plaster', 4.2, 3.2, h, [x, D / 2 - 1, 0], k % 2 ? P.wall : '#d8c7a8', { cast: false });
      for (let j = 0; j < 3; j++) for (let i = 0; i < 2; i++) flat('building_window', 'lamp', new THREE.PlaneGeometry(.8, 1.0), j % 2 ? '#ffe6a8' : '#cfe4f2', [x - 1 + i * 2, D / 2 - 2.62, 2.2 + j * 1.1], { opacity: i ? .8 : 1 });
      box('building_door', 'wood', .9, .12, 1.9, [x + 1.3, D / 2 - 2.6, 0], '#3a2c22', { cast: false });
    }
    for (let k = 0; k < 3; k++) {
      const x = -6 + k * 6;
      cyl('lamp_post', 'metal', .06, 2.6, [x, .2, 0], P.metal, { seg: 8 });
      flat('lamp_globe', 'lamp', new THREE.SphereGeometry(.17, 12, 8), '#ffeec0', [x, .2, 2.7]);
    }
    anchor('street', [0, 1.5, 0]);
    anchor('door', [4.2, D / 2 - 2.6, 0]);
  }
  if (kind === 'station') {
    box('platform', 'stone', 12, 5.5, .35, [0, 2, 0], '#b9a98a', { cast: false, mat: 'plaster' });
    for (const yy of [5.4, 6.3]) box('rail', 'metal', 24, .1, .12, [0, yy, .12], '#6a6a6e', { cast: false, mat: 'metal' });
    for (let k = 0; k < 9; k++) box('sleeper', 'wood', .22, 1.6, .12, [-8 + k * 2, 5.85, .06], '#5a4a3a', { cast: false });
    cyl('clock_post', 'metal', .06, 2.4, [-3, 3.4, 0], P.metal, { seg: 8 });
    cyl('clock_face', 'metal', .38, .08, [-3, 3.4, 2.42], '#f5f0e2', { seg: 18, cast: false });
    box('bench_seat', 'wood', 1.9, .45, .08, [3, 3.2, .5], '#8a6a48');
    for (const sx of [-.75, .75]) box('bench_leg', 'wood', .1, .4, .5, [3 + sx, 3.2, 0], '#7a5a3e');
    anchor('clock', [-3, 3.0, 1.4]);
    anchor('bench', [3, 2.8, .55]);
    anchor('door', [0, 4.6, 0]);
  }

  // ---------------------------------------------------------------- anchors
  anchor('center', [0, .6, 0]);
  anchor('back', [0, D / 2 - 1.6, 0]);
  anchor('front', [0, -.6, 0]);
  for (const [k, v] of Object.entries(layout.anchors || {})) anchors[k] = v;
  return { anchors, update: () => {} };
}

function defaultFurniture(kind) {
  return {
    room: ['table', 'chair', 'shelf', 'plant', 'rug', 'lamp'],
    shop: ['counter', 'shelf', 'sacks', 'crate'],
    office: ['desk', 'chair', 'cupboard', 'plant', 'lamp'],
    kitchen: ['stove', 'counter', 'table', 'shelf', 'crate'],
    class: ['blackboard', 'desk', 'chair', 'bench'],
    street: ['lamp', 'bench', 'crate'],
    market: ['stall', 'stall', 'crate', 'sacks'],
    field: ['tree', 'fence'],
    station: ['bench', 'clock'],
  }[kind] || ['table', 'chair', 'shelf'];
}

function round3(v) { return Math.round(v * 1000) / 1000; }

export const KINDS = ['room', 'shop', 'office', 'kitchen', 'class', 'street', 'market', 'field', 'station'];
