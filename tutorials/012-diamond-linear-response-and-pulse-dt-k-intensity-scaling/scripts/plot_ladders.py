#!/usr/bin/env python3
"""Figures and comparison numbers for the r ladder and the k ladder of the diamond linear response.

usage: plot_ladders.py <data dir> <figure dir>

<data dir> holds one sub-directory per run (names as executed), each with eps_tau<tau>.npz written by
rebuild_damped_spectrum.py (fields w_eV, eps (complex), tau):
  r ladder at k 6^3:   kcd_lr_r{16,20,24,28,32}k06_f075     (reference r32)
  k ladder at r 20:    kcd_lr_r20k{06,08,10,12,16,20,24}_f075 (reference k24, also k20)
Figures: Im eps_z with the 10 fs damping, 4-26 eV. Printed: for each rung against the reference,
the largest pointwise difference of Im eps_z over 5-25 eV (% of the reference peak), the rigid shift of
Im eps_z (+-0.4 eV, 0.5 meV steps) that minimizes that difference, the difference left after the shift
("shape", % of the reference peak), and Re eps_z at 1 eV relative to the reference (%).
"""
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATA = sys.argv[1]
OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)

BAND = (5.0, 25.0)
SHIFT = 0.4  # eV, range of the rigid-shift search
R_KEYS = [(r, "kcd_lr_r%02dk06_f075" % r) for r in (16, 20, 24, 28, 32)]
K_KEYS = [(k, "kcd_lr_r20k%02d_f075" % k) for k in (6, 8, 10, 12, 16, 20, 24)]


def load(key, tau=10):
    d = np.load(os.path.join(DATA, key, "eps_tau%g.npz" % tau))
    return d["w_eV"], d["eps"]


def metrics(w, e, wr, er):
    """pointwise %, shift meV, shape %, Re eps(1 eV) % of (w, e) against the reference (wr, er)."""
    for x, name in ((wr, "reference"), (w, "rung")):
        if x.min() > min(1.0, BAND[0] - SHIFT) or x.max() < BAND[1] + SHIFT:
            raise SystemExit("%s spectrum covers %.2f-%.2f eV; need 1 eV and %g-%g eV +- %g eV"
                             % (name, x.min(), x.max(), BAND[0], BAND[1], SHIFT))
    m = (wr >= BAND[0]) & (wr <= BAND[1])
    peak = np.max(er.imag[m])
    pw = np.max(np.abs(np.interp(wr, w, e.imag) - er.imag)[m])
    best, shift = np.inf, 0.0
    for s in np.arange(-SHIFT, SHIFT + 1e-12, 0.0005):
        r = np.max(np.abs(np.interp(wr, w + s, e.imag) - er.imag)[m])
        if r < best:
            best, shift = r, s
    re1 = np.interp(1.0, w, e.real) / np.interp(1.0, wr, er.real) - 1
    return 100 * pw / peak, 1000 * shift, 100 * best / peak, 100 * re1


def table(title, rungs, ref, tau=10):
    print("\n%s (tau = %g fs, %g-%g eV)" % (title, tau, *BAND))
    print("%-8s %12s %10s %8s %14s" % ("rung", "pointwise %", "shift meV", "shape %", "Re eps 1 eV %"))
    wr, er = load(ref, tau)
    for name, key in rungs:
        pw, sh, shp, re1 = metrics(*load(key, tau), wr, er)
        print("%-8s %12.2f %10.1f %8.2f %14.2f" % (name, pw, sh, shp, re1))


def overlay(rungs, ref_name, label, fname, title):
    """Top: Im eps_z of every rung. Bottom: difference from the reference, % of the reference peak."""
    fig, (ax, bx) = plt.subplots(2, 1, figsize=(8.0, 6.4), sharex=True, gridspec_kw={"height_ratios": [3, 2]})
    cols = plt.cm.Blues(np.linspace(0.35, 0.95, len(rungs) - 1))
    wr, er = load(dict(rungs)[ref_name])
    m = (wr >= BAND[0]) & (wr <= BAND[1])
    peak = np.max(er.imag[m])
    win = (wr >= 4) & (wr <= 26)
    ymax = 0.0
    i = 0
    for name, key in rungs:
        w, e = load(key)
        ymax = max(ymax, np.max(e.imag[(w >= 4) & (w <= 26)]))
        if name == ref_name:
            ax.plot(w, e.imag, color="black", lw=1.6, ls="--", label="%s %s (reference)" % (label, name), zorder=5)
        else:
            ax.plot(w, e.imag, color=cols[i], lw=1.3, label="%s %s" % (label, name))
            bx.plot(wr[win], 100 * (np.interp(wr, w, e.imag) - er.imag)[win] / peak, color=cols[i], lw=1.1)
            i += 1
    ax.set_xlim(4, 26)
    ax.set_ylim(-1, 1.08 * ymax)
    ax.set_ylabel("Im eps_z (damped, tau = 10 fs)")
    ax.set_title(title, fontsize=10)
    ax.legend(fontsize=8, frameon=False)
    bx.axhline(0, color="0.5", lw=0.6)
    bx.set_xlabel("photon energy (eV)")
    bx.set_ylabel("minus reference (% of its peak)")
    for a in (ax, bx):
        a.grid(color="0.9", lw=0.6)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, fname), dpi=130)
    plt.close(fig)


overlay([("%d" % r, k) for r, k in R_KEYS], "32", "r", "r-ladder-im-eps-z-tau10.png",
        "r ladder at k 6^3 (dt = 75 % of the estimated limit at each r)")
overlay([("%d" % k, key) for k, key in K_KEYS], "24", "k", "k-ladder-im-eps-z-tau10.png",
        "k ladder at r 20 (dt = 2.0e-4 fs)")

r_ref = R_KEYS[-1][1]
table("r ladder at k 6^3, reference r32", [("r%d" % r, k) for r, k in R_KEYS[:-1]], r_ref)
for tau in (10, 5, 20):
    table("k ladder at r 20, reference k24", [("k%d" % k, key) for k, key in K_KEYS[:-1]], K_KEYS[-1][1], tau)
table("k ladder at r 20, reference k20", [("k%d" % k, key) for k, key in K_KEYS[:-2]], K_KEYS[-2][1])
table("k6 against k8 at r 20", [("k6", K_KEYS[0][1])], K_KEYS[1][1])

print("\nRe eps_z at 1 eV and the Im eps_z peak (5-25 eV), tau = 10 fs")
for key in [k for _, k in R_KEYS] + [k for _, k in K_KEYS[1:]]:
    w, e = load(key)
    m = (w >= BAND[0]) & (w <= BAND[1])
    i = np.argmax(e.imag[m])
    print("%-22s Re eps(1 eV) = %.3f   peak = %.2f at %.2f eV" % (key, np.interp(1.0, w, e.real), e.imag[m][i], w[m][i]))
