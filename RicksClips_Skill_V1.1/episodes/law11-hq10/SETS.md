# SETS — law11-hq10

One place: `shop` (`sets/set_shop.js`), hand-built 2026-11-22, no place_kit.

## set_shop — Rafi's sweet shop (interior, warm)

- **Shell:** relief wood plank floor, relief plaster walls (+ wood wainscot), relief wood ceiling with 2 beams. 11 x 9 m, walls 3.3 m.
- **Counter (y 1.6):** relief wood body, relief tile top, PBR brass rail + posts, front wainscot panel.
- **Display:** 4 brass trays with sweet mounds (rosho white / laddu orange / chomchom rolls / sonpapdi squares), glass dome (`pbr wet`) over the middle tray, box tower, ladle pot + spoons, coin scatter.
- **Till:** wood till + lid + gold PBR coins + khata (red ledger, open page) + the diegetic joke tag **"নতুন মালিক"** (painted canvas texture) on the till front.
- **Back wall:** 2 shelf rows (8 glass jars each + lids + coloured sweets) + 1 high shelf (5 jars), 3 tins per row, painted shop sign **"রাফি মিষ্টি ঘর"**, wall clock (brass rim), calendar, 2 framed posters, price board on the right wall.
- **Left:** window + sill + bar, warm glow plane, additive light shaft, stove corner (pot + kettle).
- **Right:** street door (dark opening + jambs + lintel + cloth curtains + spill), sacks + crate cluster.
- **Overhead:** hanging lamp (cord, brass holder, bloom globe, green shade) + PointLight, festoon cords with 14 coloured pennants, hanging brass scale (sways), ceiling fan (turns ~2.6 rev/s), sweet-box garland.
- **Foreground mass:** barrel + big sweet jar (left near), crates (right).
- **Motion in update():** fan rotation, scale sway, lamp flicker ±2 %, mood re-grade (warm → cool s 4.05–7.5 → warm), window light follows the grade.
- **Anchors:** counter, counter_top, trays, tray1, tray4, till, khata, jars, sign, lamp, door, window, center, back, front.

## Light

`interior` preset + `light_over.tint #ffeedd`; practicals: hanging lamp PointLight (#ffd9a0, 26 → dips to #a9c4e8 14 during the disbelief beat), window PointLight (#ffdf9e, 12), door/window glow planes, floor pool, bloom globes on `role: lamp` meshes (film.js auto-halo).
