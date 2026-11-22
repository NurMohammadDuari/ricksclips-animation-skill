#!/usr/bin/env python3
"""style_check.py — gate a film plan (and optionally its render) against the
RicksClips3000 Style DNA (library/style/ricksclips-dna/style_params.json).

Usage:
    python tools/style_check.py --film episodes/my-film/film.json
    python tools/style_check.py --film episodes/my-film/film.json --frames out/frames --strict

Advisory by default (exit 0, report only). --strict exits 1 on any WARN.
It complements tools/film_plan.py: film_plan enforces Mode A camera grammar on
the plan; style_check reports DNA conformance and detects the structure mode,
so Mode B films are graded by the Mode B bands instead of failing.
"""
import argparse
import glob
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DNA_PATH = os.path.join(HERE, "..", "library", "style", "ricksclips-dna", "style_params.json")


def load_dna():
    with open(DNA_PATH) as f:
        return json.load(f)


def kmeans_small(pixels, k=6, iters=10, seed=7):
    rng = np.random.default_rng(seed)
    C = pixels[rng.choice(len(pixels), size=min(k, len(pixels)), replace=False)].astype(np.float32)
    for _ in range(iters):
        d = ((pixels[:, None, :] - C[None, :, :]) ** 2).sum(axis=2)
        lab = d.argmin(axis=1)
        for j in range(k):
            m = pixels[lab == j]
            if len(m):
                C[j] = m.mean(axis=0)
    return C


def frames_grade(frames_dir):
    import PIL.Image as Image
    files = sorted(glob.glob(os.path.join(frames_dir, "*.jpg"))) or \
            sorted(glob.glob(os.path.join(frames_dir, "*.png")))
    if not files:
        return None
    step = max(1, len(files) // 400)
    files = files[::step]
    lum, sat, warm, pal = [], [], [], []
    for fp in files:
        a = np.asarray(Image.open(fp).convert("RGB").resize((72, 128)), dtype=np.float32)
        r, g, b = a[..., 0], a[..., 1], a[..., 2]
        lum.append((0.299 * r + 0.587 * g + 0.114 * b).mean())
        mx = a.max(axis=2); mn = a.min(axis=2)
        sat.append(((mx - mn) / (mx + 1e-5)).mean())
        warm.append((r - b).mean())
        pal.append(a.reshape(-1, 3))
    P = np.concatenate(pal)
    C = kmeans_small(P[:: max(1, len(P) // 20000)], k=6)
    return {"lum": float(np.mean(lum)), "sat": float(np.mean(sat)), "warm": float(np.mean(warm)),
            "palette": ["#{:02x}{:02x}{:02x}".format(*[int(round(v)) for v in c]) for c in C]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--film", required=True)
    ap.add_argument("--frames", help="rendered frames dir (jpg/png) to grade the RENDER")
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    dna = load_dna()
    with open(a.film) as f:
        film = json.load(f)

    R = []

    def row(group, name, val, ok, target, fix=""):
        R.append((group, name, val, "PASS" if ok else "WARN", target, fix))

    fps = float(film.get("fps", 30))
    end = float(film.get("end", 0))
    dur = end / fps if fps else 0.0
    lo, hi = dna["format"]["duration_band_s"]
    row("format", "duration s", round(dur, 1), lo - 8 <= dur <= hi + 8,
        f"{lo}-{hi} (+/-8 tolerated)", "re-time the script: the corpus sits in this band")

    takes = film.get("takes", [])
    n_cuts = max(0, len(takes) - 1)
    cpm = n_cuts / dur * 60 if dur else 0
    A, B = dna["modes"]["A_one_shot_journey"], dna["modes"]["B_scene_cut_story"]
    if n_cuts <= A["cuts_total"][1]:
        mode = "A (one-shot journey)"
        row("structure", "mode", mode, True, "A or B")
        row("structure", "cuts total", n_cuts, n_cuts <= A["cuts_total"][1],
            f"<= {A['cuts_total'][1]} for mode A")
    else:
        mode = "B (scene-cut story)"
        row("structure", "mode", mode, True, "A or B")
        ok = B["cuts_total"][0] <= n_cuts <= B["cuts_total"][1] + 3
        row("structure", "cuts total", n_cuts, ok,
            f"{B['cuts_total'][0]}-{B['cuts_total'][1]}(+3) for mode B",
            "mode B wants 6-9 scenes; merge or split takes on place/time jumps only")
    med = None
    if takes:
        lens = []
        for i, t in enumerate(takes):
            st = t.get("stations") or []
            if not st:
                continue
            s0 = st[0].get("at", {}).get("s", 0)
            s1 = st[-1].get("at", {}).get("s", dur)
            lens.append(max(0.1, float(s1) - float(s0)))
        if lens:
            med = sorted(lens)[len(lens) // 2]
            band = A["median_shot_s"] if mode.startswith("A") else B["median_shot_s"]
            row("structure", "median take s", round(med, 2),
                band[0] * 0.5 <= med <= band[1] * 1.6, f"~{band[0]}-{band[1]} for {mode[:1]}")

    # mood re-grades on the story turn
    moods = film.get("moods", [])
    mm = len(moods) / dur * 60 if dur else 0
    row("grade", "mood changes/min", round(mm, 1),
        mm >= dna["grade"]["mood_changes_per_min_min"] * 0.5,
        f">= {dna['grade']['mood_changes_per_min_min']} (advisory half-band)",
        "re-grade on the turn: warm_morning -> flash_red -> cold_blue style looks")

    # word cadence
    words_file = film.get("words")
    if words_file and os.path.exists(os.path.join(os.path.dirname(a.film), words_file)):
        with open(os.path.join(os.path.dirname(a.film), words_file)) as f:
            words = json.load(f)
        if words:
            span = words[-1].get("e", 0) - words[0].get("s", 0)
            wps = len(words) / span if span else 0
            row("voice", "words/s narrated", round(wps, 2), 1.6 <= wps <= 4.0,
                "1.6-4.0 (corpus caption cadence 0.5-1.0 s/beat)")
            # stations on nouns: stations timed near word starts
            stimes = []
            for t in takes:
                for s in t.get("stations", []):
                    stimes.append(float(s.get("at", {}).get("s", -1)))
            stimes = [x for x in stimes if x >= 0]
            if stimes and words:
                starts = [w["s"] for w in words]
                import bisect
                near = sum(1 for x in stimes if
                           (lambda i: abs(x - starts[i]) if 0 <= i < len(starts) else 9)(
                               bisect.bisect_left(starts, x) if bisect.bisect_left(starts, x) < len(starts)
                               else bisect.bisect_left(starts, x) - 1) <= 0.35)
                share = near / len(stimes)
                row("voice", "stations landing on/near a word", f"{round(share * 100)}%",
                    share >= 0.55, ">= 55% of stations sit on a word start",
                    "snap station 'at.s' to the nearest narration word")

    # caption block if the plan carries one
    cap = film.get("captions") or film.get("caption")
    if isinstance(cap, dict):
        h = cap.get("height_pct", cap.get("centre_height_pct"))
        if h is not None:
            row("captions", "centre height %", h,
                dna["captions"]["band_pct"][0] - 2 <= h <= dna["captions"]["band_pct"][1] + 2,
                f"{dna['captions']['band_pct']} (corpus centre ~75)")

    # grade the RENDER if frames exist
    if a.frames:
        g = frames_grade(a.frames)
        if g:
            gb = dna["grade"]
            row("render", "luminance", round(g["lum"], 1),
                gb["luminance_mean_band"][0] - 15 <= g["lum"] <= gb["luminance_mean_band"][1] + 15,
                f"{gb['luminance_mean_band']} (+/-15)")
            row("render", "saturation", round(g["sat"], 3),
                gb["saturation_band"][0] - 0.05 <= g["sat"] <= gb["saturation_band"][1] + 0.05,
                f"{gb['saturation_band']} (+/-0.05)")
            row("render", "warmth", round(g["warm"], 1),
                gb["warmth_scene_band"][0] - 10 <= g["warm"] <= gb["warmth_scene_band"][1] + 10,
                f"{gb['warmth_scene_band']} (+/-10): each place owns its temperature")

    w = sum(1 for r in R if r[3] == "WARN")
    print(f"== style_check vs {dna['name']} v{dna['version']} — film: {a.film}")
    for group, name, val, status, target, fix in R:
        mark = "PASS" if status == "PASS" else "WARN"
        print(f"[{mark}] {group:9s} {name:38s} = {val}   target: {target}" + (f"   fix: {fix}" if fix and status == "WARN" else ""))
    print(f"== {len(R) - w} PASS / {w} WARN  mode: {mode}")
    if a.strict and w:
        sys.exit(1)


if __name__ == "__main__":
    main()
