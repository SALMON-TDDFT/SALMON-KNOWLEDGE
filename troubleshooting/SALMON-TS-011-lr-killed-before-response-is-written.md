---
id: SALMON-TS-011
title: A linear-response run killed at the time limit leaves no spectrum, but the spectrum can be rebuilt from the current
status: draft
verification_level: tested
salmon_version: 2.3.0
salmon_commit: 30ba64694ec761cdb6288f01a75b8bcabf05721f
platforms: [Fugaku (A64FX)]
related_tutorials: [SALMON-TUTORIAL-010]
created_at: 2026-10-06
updated_at: 2026-10-06
contributors: []
reviewed_by: []
---

# A linear-response run killed at the time limit leaves no spectrum, but the spectrum can be rebuilt from the current

## Symptom

A long `theory='tddft_response'` run is killed by the scheduler's elapsed-time
limit shortly before the last step. `<sysname>_response.data` does not exist,
although the run was healthy (electron number constant, no NaN) and 95-99% of
the steps were done.

For diamond (2-atom cell, `num_rgrid=32^3`, 50 fs at `dt` = 5.2e-5 fs,
961600 steps), two runs were killed at 99.0% (k 6^3) and 94.7% (k 8^3) of the
steps.

## Trigger

- `theory='tddft_response'`. SALMON v2.3.0 computes the Fourier transform and
  writes `_response.data` only after the last step (`src/io/write.f90`), so a
  run that does not reach the end writes no spectrum.
- A scheduler limit that is tight for the real speed. Here the speed was
  extrapolated from a probe with 9 k-points per process to production runs
  with 2 k-points per process, assuming the time per step scales with the
  k-points per process. At 2 k-points per process the fixed cost per step
  matters more, and the runs were 1.32-1.38 times slower than assumed, which
  used up the 1.3 margin.

## Evidence

- The induced current is written every step to `<sysname>_rt.data` (column
  `Jm_z`), and every 10 steps to standard output.
- The transform in `src/io/write.f90` was redone offline from the current:
  window `1 - 3 (t/T)^2 + 2 (t/T)^3` over the run length `T`,
  `sigma(omega) = sum_n exp(i omega t_n) J(t_n) w(t_n) dt / E_impulse`,
  `eps = 1 + 4 pi i sigma / omega`. On a run of the same system that did
  finish, it reproduced the written `_response.data` to 4e-5 of the peak.
- Truncating that finished 50 fs run at 47.4 fs changed the spectrum by only
  0.04% of the peak, so a run killed at 95% gives a usable spectrum with
  `T` set to the time actually reached.

## Diagnosis

The spectrum is a post-processing step at the end of the run, not something
accumulated during it. A time-limit kill skips it. Nothing else is lost: the
current that defines the spectrum is already on disk.

## Resolution

- Rebuild the spectrum from `Jm_z` in `<sysname>_rt.data` (or from the
  current printed in standard output) with the formula above, using `T` =
  the last time reached. Check the rebuild against a finished run of the same
  system first.
- Measure the time per step at the production layout (the same number of
  k-points per process) before setting the limit of a long run; do not
  extrapolate from a probe with many more k-points per process.
- For runs of several hours, keep a margin above 1.3, or split the
  propagation so that a kill loses less.

## Applicability

- Observed with SALMON v2.3.0 on Fugaku. The end-of-run transform is the
  behavior of this version; the rebuild applies to any
  `tddft_response` run whose `_rt.data` is complete up to the kill.
- Not tested: the same rebuild for `trans_longi='lo'` (which uses the total
  field instead of the current).
