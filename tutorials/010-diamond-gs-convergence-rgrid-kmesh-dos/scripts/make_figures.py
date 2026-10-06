#!/usr/bin/env python3
"""DOS overlays, neighbour differences, and E_total / printed-gap tables for the diamond ground-state ladders.

usage: make_figures.py <dir holding one sub-directory per run> <output figure dir>

Run directories: kcd_gs_r<RR>k<KK> (r ladder at k6: RR = 16..48; k ladder at r32: KK = 06..24).
Each holds *_dos.data (SALMON DOS output, energy relative to the valence-band maximum of the k mesh)
and the standard output (stage_run.log) with the SCF iteration lines
"iter= N Total Energy= ... Gap= ..." and the "#GS converged at N" line.
max_dev  = 100 * max|D_b - D_a| / max(D_b), over the whole window; b = denser rung of the pair.
rel-L1   = 100 * sum|D_b - D_a| / sum(D_b).
Valence = energy <= 0 eV, conduction = energy > 0 eV (VBM origin).
No script decides convergence; the numbers are reference values for reading the overlays.
"""
import glob
import os
import re
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATA = sys.argv[1]
OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)


def dos(run):
    f = glob.glob(os.path.join(DATA, run, "*_dos.data"))[0]
    a = np.loadtxt(f)
    return a[:, 0], a[:, 1]


def scf_info(run):
    txt = open(os.path.join(DATA, run, "stage_run.log")).read()
    it = re.findall(r"iter=\s*(\d+)\s+Total Energy=\s*(\S+)\s+Gap=\s*(\S+)", txt)
    conv = re.findall(r"#GS converged at\s+(\d+)", txt)
    etot = re.findall(r"Total energy \(eV\) =\s*(\S+)", txt)
    return dict(iters=int(conv[0]) if conv else None,
                gap=float(it[-1][2]) if it else None,
                etot=float(etot[-1]) if etot else float(it[-1][1]))


def pair(ra, rb):
    e, da = dos(ra)
    _, db = dos(rb)
    pk = db.max()
    d = np.abs(db - da)
    v = e <= 0
    return (100 * d.max() / pk, e[np.argmax(d)], 100 * d.sum() / db.sum(),
            100 * d[v].max() / pk, 100 * d[~v].max() / pk)


def figure(name, runs, title):
    fig, ax = plt.subplots(2, 1, figsize=(9, 6.6), sharex=True)
    cm = plt.get_cmap("viridis")
    for i, (lab, r) in enumerate(runs):
        e, d = dos(r)
        c = cm(i / max(len(runs) - 1, 1) * 0.9)
        ax[0].plot(e, d, color=c, lw=1.0, label=lab)
    ax[0].set_ylabel("DOS (1/eV)")
    ax[0].set_title(title)
    ax[0].legend(fontsize=8, ncol=2)
    for (la, ra), (lb, rb) in zip(runs, runs[1:]):
        e, da = dos(ra)
        _, db = dos(rb)
        ax[1].plot(e, db - da, lw=0.9, label=la + " to " + lb)
    ax[1].set_xlabel("energy relative to the valence-band maximum of the mesh (eV)")
    ax[1].set_ylabel("neighbour difference")
    ax[1].legend(fontsize=7, ncol=2)
    ax[1].set_xlim(-24, 10)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, name), dpi=130)
    plt.close(fig)


R = [("r%d" % r, "kcd_gs_r%02dk06" % r) for r in (16, 20, 24, 28, 32, 36, 40, 48)]
K = [("k%d" % k, "kcd_gs_r32k%02d" % k) for k in (6, 8, 10, 12, 16, 20, 24)]

figure("dos-rgrid-ladder.png", R, "diamond DOS, r ladder (k6)")
figure("dos-kgrid-ladder.png", K, "diamond DOS, k ladder (r32)")

ks = [int(l[1:]) for l, _ in K]
info = [scf_info(r) for _, r in K]
fig, ax = plt.subplots(1, 2, figsize=(9, 3.6))
ax[0].plot(ks, [i["gap"] for i in info], "o-")
ax[0].set_xlabel("k mesh n (n x n x n)")
ax[0].set_ylabel("printed gap (eV, minimum over mesh points)")
ax[0].set_title("printed gap")
e0 = info[-1]["etot"]
ax[1].plot(ks, [1000 * (i["etot"] - e0) for i in info], "o-")
ax[1].set_xlabel("k mesh n (n x n x n)")
ax[1].set_ylabel("E_total - E_total(k24)  (meV per cell)")
ax[1].set_title("total energy")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "k-gap-and-energy.png"), dpi=130)
plt.close(fig)

for nm, runs in (("r (k6)", R), ("k (r32)", K)):
    print("# " + nm + ": pair, max_dev %, where eV, rel-L1 %, max_dev valence %, max_dev conduction %")
    for (la, ra), (lb, rb) in zip(runs, runs[1:]):
        print("%s->%s  %.2f  %.2f  %.2f  %.2f  %.2f" % ((la, lb) + pair(ra, rb)))
print("# run, SCF iterations, E_total (eV), printed gap at the last iteration (eV)")
for lab, r in R + K[1:]:
    i = scf_info(r)
    print("%s  %s  %.6f  %.4f" % (r, i["iters"], i["etot"], i["gap"]))
