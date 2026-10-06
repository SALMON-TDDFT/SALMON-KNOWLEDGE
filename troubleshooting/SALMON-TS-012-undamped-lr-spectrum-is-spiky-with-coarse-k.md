---
id: SALMON-TS-012
title: An undamped long linear-response run on a coarse k mesh gives a spiky spectrum
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

# An undamped long linear-response run on a coarse k mesh gives a spiky spectrum

## Symptom

`Im eps(omega)` from a `theory='tddft_response'` run is covered with narrow
spikes instead of a smooth absorption curve. Spectra from two k meshes,
plotted together, are hard to compare because the spikes sit at different
places.

For diamond (2-atom cell, `num_rgrid=32^3`, k 6^3 and 8^3, 47 fs
propagation), the largest second difference of `Im eps` on the 0.01 eV
output grid was 4.4% of the peak height for k 8^3.

## Trigger

- A long propagation time `T` and no damping. SALMON v2.3.0 multiplies the
  current only by the window `1 - 3 (t/T)^2 + 2 (t/T)^3`
  (`src/io/write.f90`), whose width grows with `T`. There is no input
  keyword for an extra damping factor. The energy resolution is about
  `2 pi hbar / T`, i.e. 0.09 eV at 47 fs.
- A coarse k mesh. Each k-point contributes discrete transitions. When the
  resolution is finer than their spacing, they appear one by one as spikes.

## Evidence

The diamond spectra were recomputed from the current `Jm_z` (as in
[SALMON-TS-011](SALMON-TS-011-lr-killed-before-response-is-written.md)), with the same window over the full 47 fs times
`exp(-t/tau)`:

| damping | width hbar/tau | spikiness (k 8^3) | k 6^3 vs 8^3, max difference | dt 75% vs 50% |
|---|---|---|---|---|
| none | - | 4.4% | 49% at 11.6 eV | 0.04% |
| tau = 20 fs | 0.033 eV | 1.8% | 50% at 12.6 eV | 0.05% |
| tau = 10 fs | 0.066 eV | 0.8% | 48% at 12.6 eV | 0.07% |

Spikiness is the largest second difference of `Im eps` relative to the peak.
The damping removes the spikes but leaves the difference between the two k
meshes. So that difference is real k-point non-convergence, not an artifact
of the window.

## Diagnosis

Without damping, a long run resolves the individual transitions of a coarse
k mesh. The spikes are the k sampling made visible, not noise in the time
propagation.

## Resolution

- Apply an exponential damping `exp(-t/tau)` to the current when you do the
  transform yourself. `tau` = 10-20 fs gives a width of 0.03-0.07 eV. The
  current is in `<sysname>_rt.data` (column `Jm_z` for z polarization), and
  the formula is in [SALMON-TS-011](SALMON-TS-011-lr-killed-before-response-is-written.md).
- Compare k meshes, time steps or grids only between spectra with the same
  `T` and the same damping (see [SALMON-TS-008](SALMON-TS-008-lr-spectrum-depends-on-propagation-time.md)).
- Do not use damping to hide k-point non-convergence. A wider damping makes
  the curves smoother, but the k difference stays; converge k separately.

## Applicability

- Observed with SALMON v2.3.0 on Fugaku, for bulk diamond in the 2-atom
  cell. Any periodic `tddft_response` run with a coarse k mesh and a long `T`
  behaves the same way.
- The damping is post-processing only; v2.3.0 writes `_response.data`
  without it.
