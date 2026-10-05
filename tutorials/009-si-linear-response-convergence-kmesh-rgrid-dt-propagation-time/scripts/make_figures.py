#!/usr/bin/env python3
"""Overlay plots and neighbour-difference tables for the Si linear-response ladders.

usage: make_figures.py <dir holding one sub-directory per run> <output figure dir>

Each run sub-directory must contain *_response.data (SALMON tddft_response output).
Column 10 = Re(eps_z), column 13 = Im(eps_z) (1-based, as in the file header).
"max diff" = max over the 1-10 eV window of |Im eps(b) - Im eps(a)|, as a percentage of
the maximum of Im eps(b) in the same window, where b is the denser / longer rung of the pair.
No script decides convergence; the numbers are reference values for reading the overlays.
"""
import glob
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATA = sys.argv[1]
OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)


def load(run):
    f = glob.glob(os.path.join(DATA, run, "*_response.data"))
    a = np.loadtxt(f[0])
    return a[:, 0], a[:, 12]


def pairs(runs):
    rows = []
    for (la, ra), (lb, rb) in zip(runs, runs[1:]):
        xa, ya = load(ra)
        xb, yb = load(rb)
        m = (xa >= 1) & (xa <= 10)
        pk = yb[m].max()
        d = np.abs(yb[m] - ya[m])
        rows.append((la + "->" + lb, 100 * d.max() / pk, xa[m][np.argmax(d)], xb[m][np.argmax(yb[m])], pk))
    return rows


def figure(name, runs, title, xr=(1, 8)):
    fig, ax = plt.subplots(1, 2, figsize=(11, 3.8))
    cm = plt.get_cmap("viridis")
    for i, (lab, r) in enumerate(runs):
        x, y = load(r)
        c = cm(i / max(len(runs) - 1, 1) * 0.9)
        ax[0].plot(x, y, color=c, lw=1.2, label=lab)
    ax[0].set_xlim(*xr)
    # the low-frequency 1/omega artefact (window width ~ T, see the card) would otherwise set the y range
    top = max(load(r)[1][(load(r)[0] >= 1) & (load(r)[0] <= xr[1])].max() for _, r in runs)
    ax[0].set_ylim(-0.1 * top, 1.1 * top)
    ax[0].set_xlabel("photon energy (eV)")
    ax[0].set_ylabel("Im eps_z")
    ax[0].set_title(title)
    ax[0].legend(fontsize=8)
    for i, ((la, ra), (lb, rb)) in enumerate(zip(runs, runs[1:])):
        xa, ya = load(ra)
        xb, yb = load(rb)
        m = (xa >= 1) & (xa <= 10)
        ax[1].plot(xa[m], yb[m] - ya[m], lw=1.0, label=la + " to " + lb)
    ax[1].set_xlim(1, 10)
    ax[1].set_xlabel("photon energy (eV)")
    ax[1].set_ylabel("difference in Im eps_z")
    ax[1].set_title("neighbour differences")
    ax[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, name), dpi=130)
    plt.close(fig)


K = [("k%d" % k, "ksl_lr_r20k%02dn%dd050t12" % (k, 16 if k == 4 else 32)) for k in (4, 8, 12, 16, 20, 24)]
R = [("r%d" % r, "ksl_lr_r%dk08n32d050t12" % r) for r in (16, 20, 24, 28, 32)]
D = [("dt %s fs" % d, "ksl_lr_r20k08n32d%st12" % t) for d, t in (("0.00025", "025"), ("0.0005", "050"), ("0.001", "100"), ("0.0015", "150"))]
T = [("T = 12 fs", "ksl_lr_r20k08n32d050t12"), ("T = 48 fs", "ksl_lr_r20k08n32d050t48")]
N = [("nstate %d" % n, "ksl_lr_r20k04n%dd050t12" % n) for n in (16, 32, 64)]

figure("im-eps-k-ladder.png", K, "k ladder (r20, dt 0.0005 fs, T 12 fs)")
figure("im-eps-r-ladder.png", R, "r ladder (k8, dt 0.0005 fs, T 12 fs)")
figure("im-eps-dt-ladder.png", D, "dt ladder (r20, k8, T 12 fs)")
figure("im-eps-T-ladder.png", T, "propagation time (r20, k8, dt 0.0005 fs)", xr=(0, 8))

for nm, runs in (("k", K), ("r", R), ("dt", D), ("T", T), ("nstate", N)):
    print("# " + nm + ": pair, max diff (% of peak, 1-10 eV), at (eV), peak position (eV), peak value")
    for row in pairs(runs):
        print("%s  %.2f  %.2f  %.2f  %.2f" % row)
