---
id: SALMON-TS-003
title: Convergence ladder built from the official sample cannot be judged because no DOS is written
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

# Official sample deck writes no DOS, so a convergence ladder cannot be judged

## Symptom

A convergence ladder was built by changing only `num_kgrid` and `num_rgrid`
in the official bulk-Si ground-state sample. Every run converged and
completed, but the outputs could not determine whether the calculation was
converged for the intended use.

- The printed total energy appeared converged in k: at `num_rgrid=12`, the
  values for k4 to k10 differed by only 4.4 meV.
- The printed gap kept decreasing: 0.777, 0.521, 0.424, and 0.377 eV for k4,
  k6, k8, and k10.
- No `<sysname>_dos.data` file had been written, so the DOS could not be
  checked.

All seven runs had to be repeated with DOS output enabled.

## Trigger

- An input derived from SALMON2 `v.2.3.0`
  `samples/exercise_04_bulkSi_gs/Si_gs.inp` without adding an `&analysis`
  block.
- The quantity to be reported, such as the DOS, was not chosen before the
  runs.

## Evidence

- The sample input has no `&analysis` block
  ([sample at v.2.3.0](https://github.com/SALMON-TDDFT/SALMON2/blob/30ba64694ec761cdb6288f01a75b8bcabf05721f/samples/exercise_04_bulkSi_gs/Si_gs.inp)).
- The default is `yn_out_dos = 'n'`
  ([`src/io/inputoutput.f90:925-931` at v.2.3.0](https://github.com/SALMON-TDDFT/SALMON2/blob/30ba64694ec761cdb6288f01a75b8bcabf05721f/src/io/inputoutput.f90#L925-L931)).
  Those defaults also set `out_dos_start` and `out_dos_end` to ±1e10. The
  resulting window is therefore chosen by the code rather than by the input;
  how it is chosen was not checked here.
- In the rerun, only the `&analysis` block was added. Every SCF iteration
  reproduced the original energy and gap exactly. Adding DOS output costs
  nothing physically, but it is unavailable unless requested.

## Diagnosis

The official samples are minimal executable examples and do not request every
available output. The calculation was correct; the missing information was
caused by not deciding the judgment observables before the runs.

## Resolution

Before the first run, decide which observables will be reported and checked
for convergence. Enable each corresponding output. For the DOS, add:

```fortran
&analysis
  yn_out_dos = 'y'
  yn_out_dos_set_fe_origin = 'y'
  out_dos_start = -14.0d0
  out_dos_end = 9.0d0
  out_dos_nenergy = 1841
  out_dos_width = 0.1d0
  out_dos_function = 'gaussian'
/
```

Set `out_dos_start`, `out_dos_end`, and `out_dos_nenergy` explicitly.
In this ladder, all runs then used the same axis: −14 to +9 eV, with 1841
points. Here, energies are in eV
because `unit_system = 'A_eV_fs'`. With `yn_out_dos_set_fe_origin='y'`,
energies are measured from the VBM sampled by the calculation; see
[SALMON-TS-002](SALMON-TS-002-printed-gap-depends-on-k-mesh.md). Also check
that `nstate` covers the energy window. With `nstate=32` in eight-atom Si,
the conduction DOS was complete only below about +6 eV.

## Applicability

The missing DOS output applies to any input derived from a sample without an
`&analysis` block. It was observed with SALMON v2.3.0 and the bulk-Si
ground-state sample. The broader lesson, to decide observables first,
applies to any convergence study. For the full procedure, see
[SALMON-TUTORIAL-005](../tutorials/005-si-gs-convergence-bands-dos/).
