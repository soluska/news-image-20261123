// Entry for make.fun news-image-20261123: "Sum up 23 November's world
// news in one image" (Node, standard library only, no network).
//
// The picture is entry.png, stored next to this file. It was painted
// entirely with code (see draw.py, Python + PIL primitives) as a
// newspaper front page for Monday 23 November 2026: Nvidia reinstating
// Jensen Huang as CEO and jumping 33%, the COP31 climate summit ending
// with no deal in Antalya, Ukraine sinking the Russian corvette Merkury
// off Benghazi, the Dymer death toll rising to 11, India pledging $1.6bn
// to rebuild flood-hit Nepal, the Democrats taking their biggest House
// majority since 1992, and Brentford beating Everton 4-0.
//
// This program does a single deterministic job: it places that exact
// image at $MAKEFUN_OUTPUT_DIR/entry.png (or /output/entry.png by
// default), byte for byte, so every run shows the judge the same
// picture the repository holds. No network, no state, no randomness:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const here = new URL("./entry.png", import.meta.url);
copyFileSync(here, join(outDir, "entry.png"));
