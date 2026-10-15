#!/usr/bin/env python3
"""Damped dielectric function eps_z(omega) from the current of a SALMON v2.3.0 impulse response run.

usage: rebuild_damped_spectrum.py <run dir> [--tau 10] [--out <file.npz>] [--wmax 30] [--calib <factor>]

<run dir> holds <sysname>_rt.data and, if the run finished, <sysname>_response.data.

SALMON writes eps in <sysname>_response.data with the window w(t) = 1 - 3 x^2 + 2 x^3 (x = t / T, T = the
last time) and no damping (write_response_3d, src/io/write.f90). This script redoes that transform from the
column Jm_z of <sysname>_rt.data,
    S(omega) = sum_n exp(i omega t_n) Jm_z(t_n) w(t_n) dt,      eps_z = 1 + C i S(omega) / omega,
and fits the one complex factor C (units, sign, impulse strength) against SALMON's own undamped eps_z
over 2-25 eV, so nothing about units is assumed. It prints the largest relative difference between the
undamped rebuild and SALMON's file over 2-25 eV as the check of the rebuild. It then repeats the
transform with w(t) exp(-t / tau) (width hbar / tau; tau = 10 fs gives 0.066 eV).
For a run without <sysname>_response.data (killed before the end), pass --calib with the real part of C
from a finished run with the same cell and the same impulse; C depends on those only.

Output (npz): w_eV, eps (damped, complex), eps_undamped_rebuilt, eps_salmon (NaN without a file), calib,
resid, tau, T.
"""
import argparse
import glob
import os

import numpy as np

HBAR_EVFS = 0.6582119569  # eV fs


def columns(path, first_unit):
    """Map 'name' -> 0-based column from the last '# 1:Time[fs] 2:...' header line of a SALMON data file.
    The first column must carry first_unit: the transform assumes fs and eV (unit_system = 'A_eV_fs')."""
    hdr = [l for l in open(path) if l.startswith("#")][-1]
    fields = [c for c in hdr.lstrip("#").split() if ":" in c]
    if not fields or ("[%s]" % first_unit) not in fields[0]:
        raise SystemExit("%s: first column is %r, expected unit [%s] (run with unit_system = 'A_eV_fs')"
                         % (path, fields[0] if fields else None, first_unit))
    return {c.split(":", 1)[1].split("[")[0]: int(c.split(":", 1)[0]) - 1 for c in fields}


def load(run_dir, tmax=None):
    rt = glob.glob(os.path.join(run_dir, "*_rt.data"))
    rs = glob.glob(os.path.join(run_dir, "*_response.data"))
    if len(rt) != 1:
        raise SystemExit("expected one *_rt.data in %s, found %d" % (run_dir, len(rt)))
    d = np.atleast_2d(np.loadtxt(rt[0], usecols=(0, columns(rt[0], "fs")["Jm_z"])))
    if tmax is not None:
        d = d[d[:, 0] <= tmax + 1e-9]
    t = d[:, 0]
    if len(t) < 2 or not np.all(np.isfinite(d)):
        raise SystemExit("%s: need at least two finite rows" % rt[0])
    step = np.diff(t)
    if np.any(step <= 0) or np.max(np.abs(step - step[0])) > 1e-3 * step[0]:
        raise SystemExit("%s: time column is not increasing with a uniform step" % rt[0])
    if len(rs) != 1:
        return t, d[:, 1], None, None
    s = np.loadtxt(rs[0])
    c = columns(rs[0], "eV")
    return t, d[:, 1], s[:, 0], s[:, c["Re(eps_z)"]] + 1j * s[:, c["Im(eps_z)"]]


def transform(t, j, w_eV, tau=None):
    x = t / t[-1]
    win = 1 - 3 * x ** 2 + 2 * x ** 3
    if tau is not None:
        win = win * np.exp(-t / tau)
    dt = t[1] - t[0]
    om = w_eV / HBAR_EVFS  # 1/fs
    out = np.empty(len(om), complex)
    for i in range(0, len(om), 200):  # blocks of omega bound the memory
        out[i:i + 200] = (np.exp(1j * np.outer(om[i:i + 200], t)) * (j * win)).sum(axis=1) * dt
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("--tau", type=float, default=10.0, help="damping time [fs]")
    ap.add_argument("--out", default=None)
    ap.add_argument("--wmax", type=float, default=30.0, help="highest photon energy [eV]")
    ap.add_argument("--calib", type=float, default=None, help="real factor C from a finished run (no fit)")
    ap.add_argument("--tmax", type=float, default=None,
                    help="cut the current at this time [fs] to compare runs at a common length (needs --calib)")
    a = ap.parse_args()
    if not (np.isfinite(a.tau) and a.tau > 0):
        raise SystemExit("--tau must be a positive time in fs")
    if a.tmax is not None and a.calib is None:
        raise SystemExit("--tmax changes the window, so SALMON's file no longer matches: pass --calib")

    t, j, w_s, eps_s = load(a.run_dir, a.tmax)
    if eps_s is None or a.tmax is not None:
        if a.calib is None:
            raise SystemExit("no *_response.data in %s: pass --calib from a finished run" % a.run_dir)
        w = np.arange(0.01, a.wmax + 1e-9, 0.01)
        eps_ref = np.full(len(w), np.nan + 0j)
    else:
        sel = (w_s > 0) & (w_s <= a.wmax)
        w, eps_ref = w_s[sel], eps_s[sel]

    S0 = transform(t, j, w)
    fit = (w >= 2) & (w <= min(25.0, a.wmax))
    if a.calib is not None:
        C = complex(a.calib)
    else:
        A = (1j * S0 / w)[fit]
        norm = np.vdot(A, A).real
        if not fit.any() or not norm > 0:
            raise SystemExit("cannot fit C: no data or zero current in 2-25 eV (check --wmax and Jm_z)")
        C = np.vdot(A, (eps_ref - 1)[fit]) / norm  # least squares for eps - 1 = C i S / omega
    eps_u = 1 + C * 1j * S0 / w
    if np.all(np.isnan(eps_ref)) or not fit.any():
        resid = np.nan
    else:
        resid = np.max(np.abs(eps_u - eps_ref)[fit]) / np.max(np.abs(eps_ref[fit]))

    eps_d = 1 + C * 1j * transform(t, j, w, tau=a.tau) / w
    out = a.out or os.path.join(a.run_dir, "eps_tau%g.npz" % a.tau)
    np.savez(out, w_eV=w, eps=eps_d, eps_undamped_rebuilt=eps_u, eps_salmon=eps_ref,
             calib=C, resid=resid, tau=a.tau, T=t[-1])
    print("T = %.3f fs, %d steps, C = %.6g%+.3gi, undamped rebuild vs SALMON (2-25 eV) max rel diff = %.2e,"
          " tau = %g fs -> %s" % (t[-1], len(t), C.real, C.imag, resid, a.tau, out))


if __name__ == "__main__":
    main()
