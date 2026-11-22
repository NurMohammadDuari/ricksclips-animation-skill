#!/usr/bin/env python3
"""analyze_video.py — RicksClips3000 DNA analyzer (portable, stdlib + numpy + PIL).

Ingests one video (mp4 via ffmpeg) OR an existing 30 fps frames directory and
produces the same metrics the DNA was built from:

    python library/style/ricksclips-dna/analyze_video.py --video file.mp4 --outdir out/
    python library/style/ricksclips-dna/analyze_video.py --frames frames/My_Video --name My_Video --outdir out/

Outputs (in --outdir):
    metrics_<name>.json   per-frame metrics, cuts, shots, palette, timeline
    sheet_<name>.jpg      12x8 contact sheet (visual reference)
    cap_<name>_*.jpg      caption-band crops (bottom 62-88 %) for typography QA

The cut detector, palette k-means and pacing stats are identical to the ones
that produced style_params.json, so new videos extend the DNA directly.
"""
import argparse
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

FPS = 30.0
SMALL = (72, 128)
PALETTE_SIZE = (56, 100)


def kmeans(pixels, k=6, iters=12, seed=7):
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(pixels), size=min(20000, len(pixels)), replace=False)
    X = pixels[idx]
    C = X[rng.choice(len(X), size=k, replace=False)].astype(np.float32)
    for _ in range(iters):
        d = ((X[:, None, :] - C[None, :, :]) ** 2).sum(axis=2)
        lab = d.argmin(axis=1)
        for j in range(k):
            m = X[lab == j]
            if len(m):
                C[j] = m.mean(axis=0)
    d = ((X[:, None, :] - C[None, :, :]) ** 2).sum(axis=2)
    lab = d.argmin(axis=1)
    counts = np.bincount(lab, minlength=k).astype(np.float64)
    order = counts.argsort()[::-1]
    return [{"hex": "#{:02x}{:02x}{:02x}".format(*[int(round(v)) for v in C[j]]),
             "rgb": [int(round(v)) for v in C[j]],
             "share": round(float(counts[j] / counts.sum()), 4)} for j in order]


def get_frames(video, workdir):
    out = os.path.join(workdir, "f")
    os.makedirs(out, exist_ok=True)
    cmd = ["ffmpeg", "-v", "error", "-i", video, "-vf", "fps=30", "-q:v", "4",
           os.path.join(out, "f_%05d.jpg"), "-nostdin"]
    subprocess.run(cmd, check=True, timeout=900)
    return sorted(glob.glob(os.path.join(out, "*.jpg")))


def analyze(name, files, outdir):
    n = len(files)
    lum = np.zeros(n, dtype=np.float32)
    sat = np.zeros(n, dtype=np.float32)
    warm = np.zeros(n, dtype=np.float32)
    edge = np.zeros(n, dtype=np.float32)
    diff = np.zeros(max(0, n - 1), dtype=np.float32)
    prev = None
    pal_px = []
    cap_ratios, cap_white = [], []

    for i, fp in enumerate(files):
        im = Image.open(fp).convert("RGB")
        a = np.asarray(im.resize(SMALL), dtype=np.float32)
        r, g, b = a[..., 0], a[..., 1], a[..., 2]
        lum[i] = (0.299 * r + 0.587 * g + 0.114 * b).mean()
        mx = a.max(axis=2); mn = a.min(axis=2)
        sat[i] = ((mx - mn) / (mx + 1e-5)).mean()
        warm[i] = (r - b).mean()
        gg = a.mean(axis=2)
        edge[i] = np.abs(np.diff(gg, axis=1)).mean() + np.abs(np.diff(gg, axis=0)).mean()
        if prev is not None:
            diff[i - 1] = np.abs(a - prev).mean()
        prev = a
        if i % 10 == 0:
            pal_px.append(np.asarray(im.resize(PALETTE_SIZE), dtype=np.float32).reshape(-1, 3))
        h = SMALL[1]
        cap = gg[int(h * 0.62):int(h * 0.88), :]
        mid = gg[int(h * 0.30):int(h * 0.50), :]
        ec = np.abs(np.diff(cap, axis=1)).mean() + np.abs(np.diff(cap, axis=0)).mean()
        em = np.abs(np.diff(mid, axis=1)).mean() + np.abs(np.diff(mid, axis=0)).mean()
        cap_ratios.append(ec / (em + 1e-5))
        cap_white.append((cap > 225).sum() / cap.size)

    cuts = []
    if len(diff) > 8:
        mu, sd = float(diff.mean()), float(diff.std())
        thr = mu + 4.5 * sd + 6.0
        last = -10
        for c in np.where(diff > thr)[0]:
            if c - last >= 5:
                cuts.append(int(c) + 1)
                last = int(c)
    bounds = [0] + cuts + [n]
    shots = [(bounds[k + 1] - bounds[k]) / FPS for k in range(len(bounds) - 1)]
    dur = n / FPS
    thirds = {}
    for label, lo, hi in (("hook_0_3s", 0.0, 3.0), ("first_third", 0.0, 1 / 3),
                          ("mid_third", 1 / 3, 2 / 3), ("last_third", 2 / 3, 1.0)):
        lo_f, hi_f = int(lo * n), min(n, max(1, int(hi * n)))
        thirds[label] = {
            "lum": round(float(np.mean(lum[lo_f:hi_f])), 2),
            "sat": round(float(np.mean(sat[lo_f:hi_f])), 4),
            "warm": round(float(np.mean(warm[lo_f:hi_f])), 2),
            "cuts_per_min": round(float(len([c for c in cuts if lo_f <= c < hi_f]) / max(0.01, (hi_f - lo_f) / FPS) * 60), 1),
        }
    m = {
        "video": name, "frames": n, "duration_s": round(dur, 2), "fps": FPS,
        "cuts": cuts, "cut_count": len(cuts),
        "cuts_per_min": round(len(cuts) / dur * 60, 1),
        "median_shot_s": round(float(np.median(shots)), 2),
        "mean_shot_s": round(float(np.mean(shots)), 2),
        "longest_shot_s": round(max(shots), 2),
        "lum_mean": round(float(lum.mean()), 2), "lum_std": round(float(lum.std()), 2),
        "sat_mean": round(float(sat.mean()), 4),
        "warm_mean": round(float(warm.mean()), 2),
        "edge_mean": round(float(edge.mean()), 2),
        "motion_mean": round(float(diff.mean()), 3),
        "caption_band_edge_ratio_62_88": round(float(np.mean(cap_ratios)), 3),
        "caption_band_white_share": round(float(np.mean(cap_white)), 4),
        "timeline": thirds,
        "palette": kmeans(np.concatenate(pal_px), k=6),
        "per_frame_sampled_6hz": {
            "lum": [round(float(v), 2) for v in lum.tolist()[::5]],
            "diff": [round(float(v), 3) for v in diff.tolist()[::5]],
        },
    }
    with open(os.path.join(outdir, f"metrics_{name}.json"), "w") as f:
        json.dump(m, f)

    # contact sheet
    COLS, ROWS, TW, TH = 12, 8, 100, 178
    step = max(1, n // (COLS * ROWS))
    picks = files[::step][:COLS * ROWS]
    canvas = Image.new("RGB", (COLS * TW + (COLS + 1) * 2, ROWS * TH + (ROWS + 1) * 2), (18, 18, 18))
    for i, fp in enumerate(picks):
        canvas.paste(Image.open(fp).resize((TW, TH)),
                     (2 + (i % COLS) * (TW + 2), 2 + (i // COLS) * (TH + 2)))
    canvas.save(os.path.join(outdir, f"sheet_{name}.jpg"), quality=88)

    # caption crops
    for tag, idx in (("a", n // 10), ("b", n // 2), ("c", (n * 9) // 10)):
        im = Image.open(files[min(idx, n - 1)])
        w, h = im.size
        im.crop((0, int(h * 0.62), w, int(h * 0.88))).save(
            os.path.join(outdir, f"cap_{name}_{tag}.jpg"), quality=90)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", help="mp4 file (needs ffmpeg)")
    ap.add_argument("--frames", help="existing frames directory (f_%05d.jpg)")
    ap.add_argument("--name", help="video name (default: file/dir base)")
    ap.add_argument("--outdir", required=True)
    a = ap.parse_args()
    if not (a.video or a.frames):
        sys.exit("give --video or --frames")
    name = a.name or (os.path.splitext(os.path.basename(a.video))[0] if a.video
                      else os.path.basename(os.path.normpath(a.frames)))
    os.makedirs(a.outdir, exist_ok=True)
    tmp = None
    if a.video:
        tmp = tempfile.mkdtemp(prefix="rcdna_")
        files = get_frames(a.video, tmp)
    else:
        files = sorted(glob.glob(os.path.join(a.frames, "*.jpg")))
    m = analyze(name, files, a.outdir)
    if tmp:
        shutil.rmtree(tmp, ignore_errors=True)
    print(json.dumps({k: v for k, v in m.items() if k != "per_frame_sampled_6hz"}, indent=1))


if __name__ == "__main__":
    main()
