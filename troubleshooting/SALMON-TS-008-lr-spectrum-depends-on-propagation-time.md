---
id: SALMON-TS-008
title: Linear-response spectrum from an undamped impulse run keeps changing with the propagation time
status: draft
verification_level: tested
salmon_version: 2.3.0
salmon_commit: 30ba64694ec761cdb6288f01a75b8bcabf05721f
platforms: [Fugaku (A64FX)]
related_tutorials: []
created_at: 2026-10-06
updated_at: 2026-10-06
contributors: []
reviewed_by: []
---

# Linear-response spectrum from an undamped impulse run keeps changing with the propagation time

## Symptom

With `theory='tddft_response'` and an impulse field, the dielectric function
written to `<sysname>_response.data` changes when only the propagation time
`T = nt * dt` changes. Lengthening the run makes the absorption peaks taller
and narrower instead of converging. At low photon energy `Im eps` can be
negative and can grow like `1/omega`, and `Re sigma` at the lowest energy
is not zero even for an insulator.

For bulk Si (8-atom cubic cell, FHI98PP LDA, `xc='PZ'`, `num_rgrid=20^3`,
`num_kgrid=8^3`, `dt=0.0005` fs, impulse along z, SALMON defaults for the
analysis):

| quantity | T = 12 fs | T = 48 fs |
|---|---:|---:|
| `Re eps_z` at 0.5 eV | 12.90 | 12.86 |
| main `Im eps_z` peak height | 43.9 | 69.2 |
| main peak position | 3.65 eV | 3.69 eV |
| main peak full width at half maximum | 1.23 eV | 0.25 eV |
| largest point-wise difference of `Im eps_z` (1-10 eV), % of the peak | 37.5 | – |
| lowest `Im eps_z` between 0.2 and 3 eV | -0.38 | -0.83 |

On a coarser k mesh (4^3, T = 12 fs) the same setup gave
`Re sigma_z(0.01 eV) = -0.18` (in the file's units) and
`Im eps_z(0.01 eV) = -4100`, i.e. a spurious `1/omega` divergence.

## Trigger

- `theory='tddft_response'`, `ae_shape1='impulse'`, default analysis
  settings (`yn_lr_w0_correction='n'`).
- Judging convergence of the spectrum from runs that differ in `nt * dt`.

SALMON v2.3.0 always multiplies the current by the polynomial window
`1 - 3 (t/T)^2 + 2 (t/T)^3` before the Fourier transform
(`src/io/write.f90`, subroutine writing `_response.data`). The window is
stretched to the run length `T`, so it does not set a fixed broadening:
its spectral width shrinks as `1/T`. No other damping is applied.

## Evidence

- Same binary, cell, pseudopotential, `xc`, grids, ground state, `dt`, and
  impulse. Only `nt` differs (24000 vs 96000 steps).
- The static limit (`Re eps` well below the gap) agrees to 0.3% between the
  two runs, while the peak height changes by 58% and the peak width by a
  factor of five.
- In the same campaign, changing `dt` from 0.00025 to 0.0015 fs changed the
  spectrum by at most 0.23% of the peak, and changing `nstate` from 16 to 64
  changed nothing (1e-8). The T dependence is not a time-step or band-count
  effect.

## Diagnosis

Without damping the induced current of a finite k-point sample does not
decay: it is a sum of undamped oscillations at the discrete transition
energies of the mesh. The built-in window has a width proportional to `T`,
so each oscillation becomes a peak whose width scales like `hbar / T`, with
side lobes that can be negative. Lengthening `T` resolves the discrete
transitions instead of converging to a smooth spectrum. At energies below
about `2 pi hbar / T` the window-weighted mean of the current is not zero,
which appears as `Re sigma(0) != 0` and `Im eps ~ 1/omega`; with the default
`yn_lr_w0_correction='n'` this mean is not removed.

## Resolution

- Compare spectra only at the same `T`, or after applying the same explicit
  broadening (damping or window) to every run. A spectrum is converged in
  `T` only with respect to a chosen broadening.
- Do not read `eps` below about `2 pi hbar / T` from an undamped run.
  `yn_lr_w0_correction='y'` (periodic systems, fixed occupations) subtracts
  the window-weighted mean current before the transform and is the
  version's own remedy for the low-frequency part. It was checked offline:
  the transform of `src/io/write.f90` was redone from the `Jm_z` column of
  `<sysname>_rt.data` (it reproduces the written `_response.data` to
  3e-7 of the peak), then the mean was subtracted as the option does:

  | run | quantity | as written | with the correction |
  |---|---|---:|---:|
  | k 4^3, T 12 fs | `Im eps_z` at 0.01 eV | -4102 | -0.09 |
  | k 4^3, T 12 fs | `Re eps_z` at 0.01 eV | 237 | 12.5 |
  | k 8^3, T 12 fs | `Re eps_z` at 0.01 eV | 5.1 | 12.4 |
  | k 8^3, T 48 fs | `Re eps_z` at 0.01 eV | -113 | 10.1 |

  The main peak (3.65 eV) is unchanged to 0.01%. The corrected static value
  is close to the known LDA value of Si (about 12-13). Above about
  `2 pi hbar / T` the option changes almost nothing; it does not remove
  the `T` dependence of the peaks.
- The k mesh controls how smooth the undamped spectrum is: in the same
  campaign the point-wise difference of `Im eps_z` between neighbouring k
  meshes fell from 22% (8^3 to 12^3) to 1.2% (20^3 to 24^3) at T = 12 fs.
- Report `T` (and any broadening) together with every spectrum.

## Applicability

- Observed for bulk Si with SALMON v2.3.0 on Fugaku. The mechanism (finite
  window over undamped oscillations) is generic to real-time linear response
  and is expected for any insulator; the size of the effect depends on the
  k mesh and on `T`.
- Not tested: `yn_lr_w0_correction='y'` inside a SALMON run (only the
  offline re-transform above), an explicit damping applied in
  post-processing, and other materials.
