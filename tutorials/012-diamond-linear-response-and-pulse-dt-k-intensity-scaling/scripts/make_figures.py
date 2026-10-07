#!/usr/bin/env python3
"""Figures and numbers for the diamond linear-response / real-time-pulse card.

usage: make_figures.py <dir holding one sub-directory per run> <output figure dir>

Run sub-directories expected (names as executed):
  kcd_lr_r32k06_f075   *_response.data (official output), stage_run.log (standard output)
  kcd_lr_r32k06_f050   stdout.1.0 (rank-0 standard output; run killed at the elapse limit, no *_response.data)
  kcd_lr_r32k08_f050   stdout.1.0 (same)
  kcd_rt_r32k06_I1{1,2,3}_f050   *_rt_energy.data (col 3 = Eall - Eall0 [eV]), *_nex.data (time, N_e, N_h)

Rebuilding a spectrum from the printed current
----------------------------------------------
SALMON writes *_response.data only after the last time step. A run that is killed earlier has no such file,
but the standard output prints, every 10th step: step, time [fs], Jm_x, Jm_y, Jm_z (atomic units), electron
number, total energy. The spectrum is rebuilt here with the transform of write_response_3d in
src/io/write.f90 (all quantities in atomic units):
    w(t)    = 1 - 3 x^2 + 2 x^3,  x = t / (dt * nt)         (window over the full planned length)
    sigma_z = dt / e_impulse * sum_n exp(i w t_n) (J_n - jav) w(t_n)
    eps_z   = 1 + 4 pi i sigma_z / w
with e_impulse = 1e-2 a.u. (default) and jav = 0 (yn_lr_w0_correction = 'n', the default) or the
window-weighted mean of J (yn_lr_w0_correction = 'y'). Only every 10th step is printed, so the sum is done
over the printed steps with step 10*dt, plus the Euler-Maclaurin start-point term (10 dt - dt)/2 * f(0), where
f(0) = J(0) is extrapolated from the first two printed values. The rebuild is checked against the official
file of the run that finished (f075); the check is printed. A killed run stops at 99.0 % / 94.7 % of nt, where
the window is 3e-4 / 8e-3: the series is used as it is. The effect of that cut is measured on f075 by cutting
its own series at the same times (printed).
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

FS_AU = 41.341373336    # 1 fs in atomic units of time
HA_EV = 27.211386245988  # 1 hartree in eV
E_IMPULSE = 1.0e-2      # a.u., SALMON default
DT = {"f050": 5.2e-5, "f075": 7.8e-5}        # fs
NT = {"f050": 961600, "f075": 641100}


def parse_stdout(path):
    """step, time[fs], Jm_z[a.u.] from the printed table (7 numeric columns, 6th = electron number)."""
    step, t, jz = [], [], []
    with open(path, errors="replace") as f:
        for line in f:
            p = line.split()
            if len(p) != 7:
                continue
            try:
                n = int(p[0])
                v = [float(x) for x in p[1:]]
            except ValueError:
                continue
            if abs(v[4] - 8.0) > 0.5:      # electron number column (8 electrons)
                continue
            step.append(n)
            t.append(v[0])
            jz.append(v[3])
    return np.array(step), np.array(t), np.array(jz)


def rebuild_eps(step, jz, dt_fs, nt, energies, w0corr=False, tmax=None):
    """Re/Im eps_z from the printed current by the SALMON transform; see the module docstring."""
    if tmax is not None:
        m = step * dt_fs <= tmax + 1e-12
        step, jz = step[m], jz[m]
    h_step = step[1] - step[0]
    tt = dt_fs * nt
    x = step * dt_fs / tt
    win = 1 - 3 * x ** 2 + 2 * x ** 3
    j0 = 2 * jz[0] - jz[1]               # J(0), extrapolated; window = 1 at t = 0
    em = 0.5 * (h_step - 1)              # Euler-Maclaurin start-point weight, in units of one printed step
    jav = 0.0
    if w0corr:
        # window-weighted mean over ALL steps, with the same sampled-sum + start-point estimate as the transform
        jav = (h_step * np.sum(jz * win) + em * j0) / (h_step * np.sum(win) + em)
    f = (jz - jav) * win
    f0 = j0 - jav
    t_au = step * dt_fs * FS_AU
    dt_au = dt_fs * FS_AU
    hw = energies / HA_EV
    zs = np.zeros(len(energies), dtype=complex)
    for i0 in range(0, len(hw), 100):
        w = hw[i0:i0 + 100]
        zs[i0:i0 + 100] = np.exp(1j * np.outer(w, t_au)) @ f
    zs = (zs * h_step + em * f0) * dt_au / E_IMPULSE
    zeps = 1 + 4 * np.pi * 1j * zs / hw
    return zeps.real, zeps.imag


def load_official(run):
    f = glob.glob(os.path.join(DATA, run, "*_response.data"))[0]
    a = np.loadtxt(f)
    return a[:, 0], a[:, 9], a[:, 12]    # energy, Re eps_z (col 10), Im eps_z (col 13)


def maxdiff(e, ya, yb, lo, hi):
    """max |yb - ya| over lo-hi eV as % of the peak of yb over 1-15 eV; and where."""
    m = (e >= lo) & (e <= hi)
    d = np.abs(yb[m] - ya[m])
    pk_ = yb[(e >= 1) & (e <= 15)].max()
    return 100 * d.max() / pk_, e[m][np.argmax(d)]


# ---------------------------------------------------------------- linear response
E, re075, im075 = load_official("kcd_lr_r32k06_f075")
s75, t75, j75 = parse_stdout(os.path.join(DATA, "kcd_lr_r32k06_f075", "stage_run.log"))
s6, t6, j6 = parse_stdout(os.path.join(DATA, "kcd_lr_r32k06_f050", "stdout.1.0"))
s8, t8, j8 = parse_stdout(os.path.join(DATA, "kcd_lr_r32k08_f050", "stdout.1.0"))
print("# printed current: last step / nt, last time [fs]")
print("f075 k6 %d / %d  %.4f" % (s75[-1], NT["f075"], t75[-1]))
print("f050 k6 %d / %d  %.4f   (%.2f %%)" % (s6[-1], NT["f050"], t6[-1], 100.0 * s6[-1] / NT["f050"]))
print("f050 k8 %d / %d  %.4f   (%.2f %%)" % (s8[-1], NT["f050"], t8[-1], 100.0 * s8[-1] / NT["f050"]))

re75r, im75r = rebuild_eps(s75, j75, DT["f075"], NT["f075"], E)
pk = im075[(E >= 1) & (E <= 15)].max()
print("# rebuild check on f075 (all printed steps), 1-15 eV: max |dIm|, |dRe| as %% of the official Im peak (%.4f)" % pk)
m = (E >= 1) & (E <= 15)
print("%.5f  %.5f" % (100 * np.abs(im75r - im075)[m].max() / pk, 100 * np.abs(re75r - re075)[m].max() / pk))

re6, im6 = rebuild_eps(s6, j6, DT["f050"], NT["f050"], E)
re8, im8 = rebuild_eps(s8, j8, DT["f050"], NT["f050"], E)
# like-for-like with the shorter k8 series
re6c, im6c = rebuild_eps(s6, j6, DT["f050"], NT["f050"], E, tmax=t8[-1])
re75c, im75c = rebuild_eps(s75, j75, DT["f075"], NT["f075"], E, tmax=t8[-1])
re75d, im75d = rebuild_eps(s75, j75, DT["f075"], NT["f075"], E, tmax=t6[-1])
print("# effect of cutting the f075 series (rebuilt) at the time the k6 / k8 run stopped, vs official: max |dIm| in % of peak")
print("cut at %.2f fs  %.4f" % (t6[-1], 100 * np.abs(im75d - im075)[m].max() / pk))
print("cut at %.2f fs  %.4f" % (t8[-1], 100 * np.abs(im75c - im075)[m].max() / pk))

print("# peak of Im eps_z (1-15 eV): value, energy [eV]; mean and min..max of Re eps_z over 1-2 eV")
for lab, e, re_, im_ in (("f075 k6 official", E, re075, im075), ("f050 k6 rebuilt", E, re6, im6),
                         ("f050 k8 rebuilt", E, re8, im8)):
    mm = (e >= 1) & (e <= 15)
    i = np.argmax(np.where(mm, im_, -1e9))
    p = (e >= 1) & (e <= 2)
    print("%-18s %.3f  %.2f   %.4f (%.3f..%.3f)" % (lab, im_[i], e[i], re_[p].mean(), re_[p].min(), re_[p].max()))
print("Re eps_z at 1.5 eV (f075 official): %.3f" % re075[np.argmin(np.abs(E - 1.5))])

print("# dt check at k6: f050 rebuilt vs f075 official; max diff in % of the f075 peak (1-15 eV) over a range, and where")
for lo, hi in ((1, 5), (5, 10), (10, 15), (1, 15)):
    print("%2d-%2d eV  %.3f  at %.2f eV" % ((lo, hi) + maxdiff(E, im075, im6, lo, hi)))
print("# same, both rebuilt (f050 k6 cut at the k8 stop time vs f075 rebuilt cut at the same time)")
for lo, hi in ((1, 5), (5, 10), (10, 15), (1, 15)):
    print("%2d-%2d eV  %.3f  at %.2f eV" % ((lo, hi) + maxdiff(E, im75c, im6c, lo, hi)))
print("# k check at f050: k8 vs k6, both rebuilt from the series cut at %.2f fs; max diff in %% of the k8 peak, and where" % t8[-1])
for lo, hi in ((1, 5), (5, 10), (10, 15), (1, 15)):
    print("%2d-%2d eV  %.3f  at %.2f eV" % ((lo, hi) + maxdiff(E, im6c, im8, lo, hi)))

# w0 correction, from the printed f075 current
re75w, im75w = rebuild_eps(s75, j75, DT["f075"], NT["f075"], E, w0corr=True)
print("# yn_lr_w0_correction offline (f075 printed current): value at 0.01 eV, 0.1 eV, and 1-2 eV mean")
for lab, r_, i_ in (("default (n), official", re075, im075), ("w0 correction (y), rebuilt", re75w, im75w)):
    print("%-26s Re %.2f / %.2f / %.4f   Im %.2f / %.2f" % (lab, r_[0], r_[9], r_[(E >= 1) & (E <= 2)].mean(), i_[0], i_[9]))
mm = (E >= 1) & (E <= 15)
print("peak of Im after correction: %.4f (default %.4f); max |dIm| over 1-15 eV in %% of peak: %.4f"
      % (im75w[mm].max(), im075[mm].max(), 100 * np.abs(im75w - im075)[mm].max() / pk))

# ---- figures
C_OFF, C_K6, C_K8 = "#1b6ca8", "#d9822b", "#2a9d5b"
for name, yo, y6, y8, ylab, ylim in (
        ("im-eps-z.png", im075, im6, im8, "Im eps_z", (-3, 60)),
        ("re-eps-z.png", re075, re6, re8, "Re eps_z", (-10, 30))):
    fig, ax = plt.subplots(1, 2, figsize=(11, 3.9))
    for a, xr in zip(ax, ((0, 20), (0, 5))):
        a.plot(E, yo, color=C_OFF, lw=1.3, label="f075, k6: official *_response.data")
        a.plot(E, y6, color=C_K6, lw=1.0, ls="--", label="f050, k6: rebuilt from the printed current (run killed at 99%)")
        a.plot(E, y8, color=C_K8, lw=1.0, label="f050, k8: rebuilt from the printed current (run killed at 95%)")
        a.set_xlim(*xr)
        a.set_xlabel("photon energy (eV)")
        a.set_ylabel(ylab)
    ax[0].set_ylim(*ylim)
    if name.startswith("im"):
        ax[1].set_ylim(-3, 8)
    else:
        ax[1].set_ylim(-5, 12)
    ax[0].set_title("%s, 0-20 eV (y cut)" % ylab)
    ax[1].set_title("low-energy part (y cut)")
    ax[0].legend(fontsize=7, loc="upper right")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, name), dpi=130)
    plt.close(fig)

# ---------------------------------------------------------------- real-time pulse
RT = {}
for tag, I in (("I11", 1e11), ("I12", 1e12), ("I13", 1e13)):
    d = os.path.join(DATA, "kcd_rt_r32k06_%s_f050" % tag)
    en = np.loadtxt(glob.glob(os.path.join(d, "*_rt_energy.data"))[0])
    nx = np.loadtxt(glob.glob(os.path.join(d, "*_nex.data"))[0])
    RT[I] = (en[:, 0], en[:, 2], nx[:, 0], nx[:, 1], nx[:, 2])
print("# RT: I, peak Eall-Eall0 [eV] at t [fs], end Eall-Eall0 [eV], end N_e, end N_h, end dE/N_e [eV], end t")
rows = []
for I, (t, de, tn, ne, nh) in RT.items():
    i = np.argmax(de)
    rows.append((I, de[i], de[-1], ne[-1], nh[-1]))
    print("%.0e  %.4e at %.3f   %.4e   %.4e  %.4e  %.2f  t_end %.3f" % (I, de[i], t[i], de[-1], ne[-1], nh[-1], de[-1] / ne[-1], t[-1]))
Is = np.array([r[0] for r in rows])
print("# exponent p of a power law (ratio over the interval = (I ratio)^p)")
for k, lab in ((1, "peak in-pulse energy"), (2, "residual energy"), (3, "N_e end"), (4, "N_h end")):
    v = np.array([r[k] for r in rows])
    p1 = np.log10(v[1] / v[0])
    p2 = np.log10(v[2] / v[1])
    print("%-22s 1e11-1e12 %.2f   1e12-1e13 %.2f   1e11-1e13 %.2f" % (lab, p1, p2, np.log10(v[2] / v[0]) / 2))

fig, ax = plt.subplots(1, 2, figsize=(11, 3.9))
cols = {1e11: "#1b6ca8", 1e12: "#d9822b", 1e13: "#2a9d5b"}
for I, (t, de, tn, ne, nh) in RT.items():
    pos = de > 0
    ax[0].semilogy(t[pos], de[pos], color=cols[I], lw=1.1, label="I = %.0e W/cm$^2$" % I)
    ax[1].semilogy(t[pos], de[pos] / I, color=cols[I], lw=1.1, label="I = %.0e W/cm$^2$" % I)
for a in ax:
    a.axvline(10.672, color="0.6", lw=0.8, ls=":")
    a.set_xlabel("time (fs)")
    a.set_xlim(0, 20)
ax[0].set_ylim(1e-8, 0.5)          # the first steps (round-off, ~1e-11) are cut
ax[1].set_ylim(1e-20, 1e-13)
ax[0].set_ylabel("Eall - Eall0 (eV)")
ax[1].set_ylabel("(Eall - Eall0) / I (eV per W/cm$^2$)")
ax[0].set_title("excitation energy (dotted: pulse length tw1)")
ax[1].set_title("divided by the peak intensity")
ax[0].legend(fontsize=8, loc="lower right")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "rt-energy-vs-time.png"), dpi=130)
plt.close(fig)

fig, ax = plt.subplots(figsize=(5.8, 4.2))
ax.loglog(Is, [r[1] for r in rows], "o-", color="#7a7a7a", label="peak Eall-Eall0 during the pulse (eV)")
ax.loglog(Is, [r[2] for r in rows], "s-", color="#d9822b", label="residual Eall-Eall0 at 20 fs (eV)")
ax.loglog(Is, [r[3] for r in rows], "^-", color="#1b6ca8", label="N_e at 20 fs")
ax.loglog(Is, [r[4] for r in rows], "v--", color="#1b6ca8", mfc="none", label="N_h at 20 fs (floor-limited at 1e11)")
x = np.array([1e11, 1e13])
ax.loglog(x, rows[0][1] * (x / 1e11), color="0.75", lw=0.8)
ax.loglog(x, rows[0][2] * (x / 1e11) ** 3, color="0.75", lw=0.8)
ax.text(1.2e11, rows[0][1] * 2.5, "slope 1", color="0.5", fontsize=8)
ax.text(2.5e12, rows[0][2] * 2e4, "slope 3", color="0.5", fontsize=8)
ax.set_xlabel("peak intensity (W/cm$^2$)")
ax.set_ylabel("energy (eV) / number of electrons")
ax.legend(fontsize=7, loc="lower right")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "rt-residual-vs-intensity.png"), dpi=130)
plt.close(fig)
