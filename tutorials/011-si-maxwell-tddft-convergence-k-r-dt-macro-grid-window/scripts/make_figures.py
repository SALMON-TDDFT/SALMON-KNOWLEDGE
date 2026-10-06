#!/usr/bin/env python3
"""Figures and tables for the Si thin-film Maxwell-TDDFT convergence card.

usage: make_figures.py <data dir> <output figure dir>

<data dir> holds one sub-directory per run (the run name is the sysname):
  multiscale runs   <run>/<run>_wave.data
                    <run>/<run>_m/m00000i/<run>_rt.data         (col 10 = Ac_tot_z, col 13 = E_tot_z)
                    <run>/<run>_m/m00000i/<run>_rt_energy.data  (col 3 = Eall - Eall0)
  single-cell runs  <run>/<run>_rt_energy.data                  (tddft_pulse, col 3 = Eall - Eall0)
All columns are 1-based as in the file headers.

Definitions used for the numbers:
  R = integral(E_ref_z^2 dt) / integral(E_inc_z^2 dt), T likewise with E_tra_z, over the window [0, t_end].
  Eabs(film mean) = mean over the macro points inside the film of (Eall - Eall0) at the last time step.
No script decides convergence; the numbers are reference values for reading the figures.
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


def wave(run):
    return np.loadtxt(os.path.join(DATA, run, run + "_wave.data"))


def RT(run, tmax=None):
    a = wave(run)
    t = a[:, 0]
    if tmax is not None:
        m = t <= tmax + 1e-9
        a = a[m]
        t = t[m]
    einc, eref, etra = a[:, 3], a[:, 6], a[:, 9]
    n = np.trapz(einc ** 2, t)
    return np.trapz(eref ** 2, t) / n, np.trapz(etra ** 2, t) / n


def macro_files(run, kind):
    # the layout is <run>/<run>_m/m00000i/ for most runs; the first smoke run keeps m00000i directly in <run>/
    for sub in (os.path.join(run + "_m", "m*"), "m*"):
        files = sorted(glob.glob(os.path.join(DATA, run, sub, run + "_" + kind + ".data")))
        if files:
            return files
    return []


def rt(run, point=1):
    f = macro_files(run, "rt")[point - 1]
    a = np.loadtxt(f)
    return a[:, 0], a[:, 9], a[:, 12]  # t, Ac_tot_z, E_tot_z


def erg(run, point=1):
    f = macro_files(run, "rt_energy")[point - 1]
    a = np.loadtxt(f)
    return a[:, 0], a[:, 2]


def eabs_points(run):
    return np.array([np.loadtxt(f)[-1, 2] for f in macro_files(run, "rt_energy")])


def pulse_eabs(run):
    a = np.loadtxt(os.path.join(DATA, run, run + "_rt_energy.data"))
    return a[-1, 2]


# ---- run names -------------------------------------------------------------------------------
OFFICIAL = "ksl_ms_r12k04_m8h50_d002"           # official exercise_07 grid (r12, k4, dt 0.002 fs)
R20 = {4: "ksl_ms_r20k04_m8h50_d001", 8: "ksl_ms_r20k08_m8h50_d001", 12: "ksl_ms_r20k12_m8h50_d001"}

# ---- Figure 1 and 2: Ac_tot_z(t) and Eall-Eall0(t) at macro point 1 ----------------------------
curves = [("r20 k4", R20[4], "#c0392b", "-"), ("r20 k8 (dashed, nearly on top of k12)", R20[8], "#1f6fb4", "--"),
          ("r20 k12", R20[12], "#2e8b57", "-"), ("r12 k4 (official grid, dt 0.002 fs)", OFFICIAL, "#7f7f7f", "-")]

fig, ax = plt.subplots(figsize=(6.4, 3.8))
for lab, run, c, ls in curves:
    t, ac, _ = rt(run)
    ax.plot(t, ac, color=c, ls=ls, lw=1.5, label=lab)
ax.axhline(0, color="k", lw=0.5)
ax.set_xlabel("time (fs)")
ax.set_ylabel("Ac_tot_z at macro point 1 (fs V/Angstrom)")
ax.set_title("Total vector potential, first macro point of the film")
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "ac-tot-z-macro1.png"), dpi=130)
plt.close(fig)

fig, ax = plt.subplots(figsize=(6.4, 3.8))
for lab, run, c, ls in curves:
    t, de = erg(run)
    ax.plot(t, de * 1e3, color=c, ls=ls, lw=1.5, label=lab)
ax.axhline(0, color="k", lw=0.5)
ax.set_xlabel("time (fs)")
ax.set_ylabel("Eall - Eall0 per cell, macro point 1 (meV)")
ax.set_title("Energy relative to the ground state, first macro point")
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "eall-minus-eall0-macro1.png"), dpi=130)
plt.close(fig)

# ---- Figure 3: R and T versus k -----------------------------------------------------------------
ks = [4, 8, 12]
RTk = [RT(R20[k]) for k in ks]
fig, ax = plt.subplots(1, 2, figsize=(8.0, 3.4))
for i, (nm, j) in enumerate((("R", 0), ("T", 1))):
    vals = [x[j] for x in RTk]
    cols = ["#c0392b", "#1f6fb4", "#1f6fb4"]
    ax[i].bar([str(k) for k in ks], vals, color=cols)
    for x, v in enumerate(vals):
        ax[i].text(x, v, "%.3f" % v, ha="center", va="bottom", fontsize=8)
    ax[i].set_ylim(0, max(vals) * 1.18)
    ax[i].set_xlabel("num_kgrid (k x k x k), r = 20^3, 16 fs window")
    ax[i].set_ylabel(nm + " (fraction of incident energy)")
    ax[i].set_title(nm + " versus k (red = caution zone)")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "rt-vs-k.png"), dpi=130)
plt.close(fig)

# ---- Figure 4: single-cell absorbed energy versus r ---------------------------------------------
k8 = [(20, "ksl_pu_r20k08_d001", "dt 0.001 fs"), (24, "ksl_pu_r24k08_d0005", "dt 0.0005 fs"),
      (28, "ksl_pu_r28k08_d0005", "dt 0.0005 fs"), (32, "ksl_pu_r32k08_d0005", "dt 0.0005 fs")]
fig, ax = plt.subplots(figsize=(6.0, 3.8))
ax.plot([r for r, _, _ in k8], [pulse_eabs(n) for _, n, _ in k8], "o-", color="#1f6fb4", label="k8")
k4 = [(12, "ksl_pu_r12k04_d001"), (20, "ksl_pu_r20k04_d001")]
ax.plot([r for r, _ in k4], [pulse_eabs(n) for _, n in k4], "s", color="#c0392b", label="k4 (caution zone)")
ax.set_xlabel("num_rgrid (r x r x r)")
ax.set_ylabel("Eall - Eall0 at 16 fs, one cell (eV)")
ax.set_title("Single-cell absorbed energy (no Maxwell coupling)")
ax.set_ylim(0, 2.8)
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "single-cell-eabs-vs-r.png"), dpi=130)
plt.close(fig)

# ---- Tables ---------------------------------------------------------------------------------------
print("# R, T over 16 fs (int E^2 dt / int E_inc^2 dt), R+T")
for lab, run in (("r20 k4 d001", "ksl_ms_r20k04_m8h50_d001"), ("r20 k4 d0005", "ksl_ms_r20k04_m8h50_d0005"),
                 ("r20 k8 d001", R20[8]), ("r20 k12 d001", R20[12]),
                 ("r12 k4 d002 (official grid)", OFFICIAL), ("r12 k4 d001", "ksl_ms_r12k04_m8h50_d001"),
                 ("r12 k8 d002", "ksl_ms_r12k08_m8h50_d002")):
    r, t = RT(run, 16.0)
    print("%-30s R %.4f  T %.4f  R+T %.4f" % (lab, r, t, r + t))
print("# window: r20 k8 d001 over 16 fs and over 32 fs (32 fs run), and r12 k4 d002 16 fs vs 32 fs")
for lab, run in (("r20 k8 d001_t32", "ksl_ms_r20k08_m8h50_d001_t32"), ("r12 k4 d002_t32", "ksl_ms_r12k04_m8h50_d002_t32")):
    for tm in (16.0, 32.0):
        r, t = RT(run, tm)
        print("%-30s window %4.0f fs  R %.5f  T %.5f" % (lab, tm, r, t))
print("# film-mean and per-point Eall-Eall0 at 16 fs (eV)")
for lab, run in (("r20 k4 d001", "ksl_ms_r20k04_m8h50_d001"), ("r20 k8 d001", R20[8]), ("r20 k12 d001", R20[12])):
    e = eabs_points(run)
    print("%-14s mean %.4f  points %s" % (lab, e.mean(), " ".join("%.4f" % x for x in e)))
e8, e12 = eabs_points(R20[8]), eabs_points(R20[12])
print("# k8 -> k12 change per macro point (%):", " ".join("%.1f" % x for x in 100 * (e12 / e8 - 1)))
print("# dt check: r20 k4 d001 vs d0005 and r12 k4 d002 vs d001, film-mean Eabs")
for a, b in (("ksl_ms_r20k04_m8h50_d001", "ksl_ms_r20k04_m8h50_d0005"), ("ksl_ms_r12k04_m8h50_d002", "ksl_ms_r12k04_m8h50_d001")):
    ea, eb = eabs_points(a).mean(), eabs_points(b).mean()
    print("%s -> %s : %.5f -> %.5f (%.3f %%)" % (a, b, ea, eb, 100 * (eb / ea - 1)))
print("# macro grid (r12 k4 d002): film-mean Eabs (m16, m32 block-averaged to 8 points not needed for the mean)")
for lab, run in (("m8 h50", OFFICIAL), ("m16 h25", "ksl_ms_r12k04_m16h25_d002"), ("m32 h12.5", "ksl_ms_r12k04_m32h125_d002")):
    e = eabs_points(run)
    r, t = RT(run, 16.0)
    print("%-10s npts %2d  film mean %.5f  R %.4f  T %.4f" % (lab, len(e), e.mean(), r, t))
print("# Ac_tot_z at 16 fs, macro point 1 / last-2-fs mean, and minimum of Eall-Eall0 at point 1")
for lab, run in (("r20 k4 d001", "ksl_ms_r20k04_m8h50_d001"), ("r20 k4 d0005", "ksl_ms_r20k04_m8h50_d0005"), ("r20 k8", R20[8]), ("r20 k12", R20[12]), ("r12 k4 d002", OFFICIAL)):
    t, ac, ez = rt(run)
    t2, de = erg(run)
    print("%-14s Ac(end) %.4f  E_tot_z mean 10-15 fs %.4e  dE(end) %.5f  dE min %.5f eV" % (lab, ac[-1], ez[(t >= 10) & (t <= 15)].mean(), de[-1], de.min()))
print("# single-cell Eall-Eall0 at 16 fs (eV)")
for run in ("ksl_pu_r12k04_d001", "ksl_pu_r20k04_d001", "ksl_pu_r20k04_d0005", "ksl_pu_r20k08_d001", "ksl_pu_r24k08_d001",
            "ksl_pu_r24k08_d0005", "ksl_pu_r28k08_d0005", "ksl_pu_r32k08_d0005"):
    print("%-24s %.5f" % (run, pulse_eabs(run)))
