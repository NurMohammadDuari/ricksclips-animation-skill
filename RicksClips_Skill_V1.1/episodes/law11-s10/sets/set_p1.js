// SET: the sweet shop (warm) - built from scratch for the Law 11 opening.
// Counter with sweet jars centre-back, price board + shelves on the back wall,
// sugar sacks and crates at the sides. Warm cream walls, honey wood, red accents.
import { buildPlace } from "../../kit/sets/place_kit.js";

export const layout = {
  "kind": "shop",
  "palette": "warm",
  "size": [9, 7],
  "door": "right",
  "goods": "jars",
  "furniture": [
    { "kind": "counter", "at": [0, 2.75], "rot": 0 },
    { "kind": "blackboard", "at": [-1.6, 3.35] },
    { "kind": "shelf", "at": [-3.5, 2.8], "rot": 0.12 },
    { "kind": "shelf", "at": [3.3, 2.75], "rot": -0.15 },
    { "kind": "sacks", "at": [3.5, 1.55] },
    { "kind": "crate", "at": [-3.0, 1.15], "rot": 0.4 },
    { "kind": "lamp", "at": [-3.7, 2.1] },
    { "kind": "plant", "at": [3.9, 2.4] }
  ],
  "seed": 11
};

export function build(THREE, scene, film, ctx) {
  return buildPlace(THREE, scene, film, ctx, layout);
}
