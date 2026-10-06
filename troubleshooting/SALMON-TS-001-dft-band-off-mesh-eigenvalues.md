---
id: SALMON-TS-001
title: "`theory='dft_band'` gives wrong eigenvalues at k-points off the SCF mesh (v2.3.0)"
status: draft
verification_level: tested
salmon_version: 2.3.0
salmon_commit: 30ba64694ec761cdb6288f01a75b8bcabf05721f
platforms: [Fugaku (A64FX)]
related_tutorials: [SALMON-TUTORIAL-005]
created_at: 2026-10-04
updated_at: 2026-10-04
contributors: []
reviewed_by: []
---

# `theory='dft_band'` gives wrong eigenvalues at k-points off the SCF mesh (v2.3.0)

## Symptom

A periodic band-structure run with `theory='dft_band'` completes normally:
the exit status is zero, it prints `end SALMON`, `band.dat` is written, and
the band CG converges. The band energies are nevertheless wrong:

- At the 66 path points shared with a reference calculation, bands 1–17
  deviate by up to 1.64 eV. The median of the per-point maximum deviation is
  0.76 eV.
- Gamma appears twice on the requested path, at two different k slots. The two
  Gamma entries differ by 0.458 eV.
- The threefold-degenerate valence-band top at Gamma is split by 0.53 eV.
- The gap obtained from `band.dat` is 0.303 eV, compared with 0.522 eV in the
  reference. Its VBM and CBM are also at the wrong k-points.
- Band k-points that coincide with the SCF mesh point of the same index
  (control points) agree with the SCF eigenvalues to 4e-8 eV.

## Trigger

- SALMON v2.3.0, tag `v.2.3.0`, `theory='dft_band'`, `yn_periodic='y'`,
  with a ground-state restart (`yn_restart='y'`).
- Any band k-point that differs from the k-point that occupied the same index
  in the SCF mesh. The error grows with the distance between the two.
- Observed for bulk Si (eight-atom cubic cell, FHI98PP LDA, `num_rgrid=20`,
  SCF `num_kgrid=8`, 512 band k-points, `nref_band=20`, `nproc_k=8`).

## Evidence

Observed in the calculations of
[SALMON-TUTORIAL-005](../tutorials/005-si-gs-convergence-bands-dos/):

| quantity, bands 1–17 | v2.3.0 `dft_band` | v2.3.0 + one-line patch below |
|---|---:|---:|
| max deviation from reference at 66 shared path points | 1.638 eV | 3.3e-6 eV |
| median of the per-point maximum | 0.76 eV | 8.7e-8 eV |
| Gamma at slot 9 versus Gamma at slot 361 | 0.458 eV | 5e-15 eV |
| Gamma triplet (bands 14–16) spread | 0.53 eV | 6e-9 eV |
| gap from `band.dat` | 0.303 eV | 0.5221 eV |

The reference is a `theory='dft'` run on the same density settings with the
same path added as zero-weight `file_kw` points; its gap is 0.5222 eV. The
unpatched deviation increases with the distance d between the band k-point and
the SCF k-point formerly held by the same slot:

| d (2π/a) | typical deviation |
|---:|---:|
| 0.1 | 0.02 eV |
| 0.3–0.6 | median 0.4 eV |
| 0.6–1.0 | median 1.2 eV |

Source inspection at `v.2.3.0`:

1. **The non-local projector phase is not updated for band k-points.**
   `ppg%zekr_uV` (`exp(-ik·r)` times the projector) is built for the SCF
   mesh by `update_kvector_nonlocalpt` in
   [`src/atom/pp/prep_pp.f90:184-185`](https://github.com/SALMON-TDDFT/SALMON2/blob/30ba64694ec761cdb6288f01a75b8bcabf05721f/src/atom/pp/prep_pp.f90#L184-L185).
   The band loop in
   [`src/gs/main_dft.f90:168-199`](https://github.com/SALMON-TDDFT/SALMON2/blob/30ba64694ec761cdb6288f01a75b8bcabf05721f/src/gs/main_dft.f90#L168-L199)
   changes `system%vec_k` through `calc_band_write` but does not call it
   again. The kinetic term therefore uses the new k-point, while the
   non-local term keeps the old one.
2. **`primitive_b` is applied twice.** The band k-points are multiplied by
   `system%primitive_b` in
   [`src/gs/band_dft.f90:202-205`](https://github.com/SALMON-TDDFT/SALMON2/blob/30ba64694ec761cdb6288f01a75b8bcabf05721f/src/gs/band_dft.f90#L202-L205)
   and again in
   [`src/gs/band_dft.f90:62`](https://github.com/SALMON-TDDFT/SALMON2/blob/30ba64694ec761cdb6288f01a75b8bcabf05721f/src/gs/band_dft.f90#L62).
   The output confirmed this: `kpt` values were multiplied by b twice.
3. **Default `nref_band=0` performs no band CG.** `check_conv_esp` then has
   zero length, so `all(...)` is true, and the iteration is skipped with
   `cycle` before any orbital update
   ([`src/gs/scf_iteration_dft.f90:159-164`](https://github.com/SALMON-TDDFT/SALMON2/blob/30ba64694ec761cdb6288f01a75b8bcabf05721f/src/gs/scf_iteration_dft.f90#L159-L164);
   default in
   [`src/io/inputoutput.f90:1020`](https://github.com/SALMON-TDDFT/SALMON2/blob/30ba64694ec761cdb6288f01a75b8bcabf05721f/src/io/inputoutput.f90#L1020)).
   `nref_band` must be set explicitly.
4. **The explicit path drops its final endpoint.** `kpt` is allocated with
   `num_of_segments+1` columns, but only `num_of_segments` are copied from
   the namelist
   ([`band_dft.f90:133-140`](https://github.com/SALMON-TDDFT/SALMON2/blob/30ba64694ec761cdb6288f01a75b8bcabf05721f/src/gs/band_dft.f90#L133-L140)).
   The last segment is then interpolated towards zero
   ([`:293-298`](https://github.com/SALMON-TDDFT/SALMON2/blob/30ba64694ec761cdb6288f01a75b8bcabf05721f/src/gs/band_dft.f90#L293-L298)).
5. **`if_real_orbital` is set only for `calc_mode` `'RT'` and `'GS'`**
   ([`src/common/initialization.f90:162-176`](https://github.com/SALMON-TDDFT/SALMON2/blob/30ba64694ec761cdb6288f01a75b8bcabf05721f/src/common/initialization.f90#L162-L176)).
   In the observed run it printed `F` (complex orbitals) and was harmless.
6. **Restart file paths are stored in `character(100)`** in the density
   readers
   ([`src/io/checkpoint_restart.f90:1458-1465`](https://github.com/SALMON-TDDFT/SALMON2/blob/30ba64694ec761cdb6288f01a75b8bcabf05721f/src/io/checkpoint_restart.f90#L1458-L1465),
   [`:1582-1588`](https://github.com/SALMON-TDDFT/SALMON2/blob/30ba64694ec761cdb6288f01a75b8bcabf05721f/src/io/checkpoint_restart.f90#L1582-L1588)).
   A long `directory_read_data` can be silently truncated. This was found by
   reading the source only; it was not triggered here.

An additional output problem was observed but its source was not examined.
With `nproc_k=8`, the `vec_k` columns (columns 5–7) of `band.dat` contained
the applied band k-point only for slots 1–64, which belong to the first
process. For slots 65–512, they repeated the SCF-mesh k-point for that slot.
Use the reduced-coordinate columns (2–4) to identify band k-points.

Items 2–6 are findings from the source code. The observed run worked around
items 2 and 4 in the input, as described below. Items 5 and 6 were not
exercised.

## Diagnosis

Item 1, the stale non-local phase, is the cause of the wrong eigenvalues. A
controlled test changed only the executable. The v2.3.0 source received one
added line, taken from the public upstream commit
[`685462cf`](https://github.com/SALMON-TDDFT/SALMON2/commit/685462cff9461404130ab0b264532eed64893d65)
on the SALMON2 `band` branch. The line was inserted in the `dft_band` branch
of `main_dft.f90` immediately after `calc_band_write`:

```fortran
call update_kvector_nonlocalpt(info%ik_s,info%ik_e,system,ppg)
```

The same restart, input, and path were used. With the patch, all symptoms
disappeared: maximum deviation 3.3e-6 eV, Gamma duplicates equal to 5e-15 eV, and
the Gamma triplet degenerate to 6e-9 eV. The gap was 0.5221 eV with the VBM at Gamma
and the CBM on Gamma-X, matching the reference.

This result was obtained with the doubled `primitive_b` compensated in the
input. All path coordinates in `&band` `kpt` were divided by
b = 0.612323844378641. The trailing-endpoint defect was avoided with a
duplicated final point. The one-line patch does not fix either item. The
upstream commit `685462cf` rewrites `band_dft.f90` more extensively; it was
not tested as a whole.

The diagnosis was cross-checked by an independent reading of the v2.3.0
source. The control points agree because, at those points, the stale phase
equals the correct phase.

## Resolution

Workaround with unmodified v2.3.0, used in
[SALMON-TUTORIAL-005](../tutorials/005-si-gs-convergence-bands-dos/): do not use
`theory='dft_band'`. Run `theory='dft'` with `file_kw` containing the SCF
mesh plus the path k-points at weight about 1e-9. SALMON renormalizes the
weights. The path eigenvalues agreed with true-weight k-points to 4e-6 eV,
and `E_total` changed by 1.2e-7 eV.

Source fix: call `update_kvector_nonlocalpt` after `calc_band_write` in the
band loop, as in upstream commit `685462cf`. Also correct the doubled
`primitive_b` and the path copy. Until a release contains these fixes, treat
`dft_band` eigenvalues away from the SCF mesh as invalid. Checking only the
on-mesh control points cannot detect this defect.

This is a candidate for an upstream SALMON2 issue: release v2.3.0 does not
contain the fix.

## Applicability

- Confirmed: SALMON v2.3.0, tag `v.2.3.0`, periodic `dft_band`,
  norm-conserving pseudopotential with non-local projectors, bulk Si, and
  Fugaku (A64FX).
- Expected, but not tested: any periodic `dft_band` calculation with
  non-local projectors, because the missing call does not depend on the
  material.
- Not tested: later releases, the full upstream `band` branch, PAW, and
  spin-orbit calculations.
