---
id: SALMON-TUTORIAL-001
title: Reproducing the official silicon HHG exercise
status: draft
verification_level: tested
learning_stage: foundation
prerequisites: []
next_tutorials: [SALMON-TUTORIAL-002, SALMON-TUTORIAL-003, SALMON-TUTORIAL-005]
estimated_cost: one small node
topics: [silicon, high-harmonic-generation, real-time-tddft, exercise]
salmon_version: 2.3.0
salmon_commit: unknown
platforms: [A64FX]
created_at: 2026-09-03
updated_at: 2026-09-03
contributors: []
reviewed_by: []
---

# Learning objective

Reproduce the official bulk-Si GS-to-RT HHG exercise without changing its
inputs, and confirm the completion markers and essential physical diagnostics.

# Summary

SALMON's official bulk-Si ground-state and pulsed-field samples provide a
small, reproducible starting point for a silicon high-harmonic-generation
(HHG) calculation. This tutorial records how to reproduce the exercise and how
to verify that it completed correctly. The tutorial settings are not claimed
to be converged for publication use; numerical convergence is covered by
[SALMON-TUTORIAL-002](../002-si-hhg-convergence-and-restart-validation/).

## Context and objective

The objective is to reproduce Exercise 6, "Electron dynamics in crystalline
silicon under a pulsed electric field," using the SALMON 2.3.0 sample inputs.
The official structure, functional, pseudopotential, and pulse are retained so
that this tutorial tests reproducibility rather than model choices.

## Conditions

- SALMON version: 2.3.0 sample inputs and executable.
- Ground-state mode: `theory='dft'`.
- Real-time mode: `theory='tddft_pulse'`, initialized from GS
  `data_for_restart`.
- Structure: conventional cubic Si cell with eight atoms and
  `al(1:3)=5.43d0` Angstrom.
- Electronic structure: `xc='PZ'`, `nstate=32`, official `Si_rps.dat`, and
  `nelec=32`.
- Pulse: `ae_shape1='Acos2'`, `I_wcm2_1=1.0d12`, `tw1=10.672d0` fs,
  `omega1=1.55d0` eV, z polarization.
- Baseline discretization: `num_rgrid=12,12,12`, `num_kgrid=4,4,4`,
  `dt=0.002d0` fs, and `nt=6000` (12 fs).
- Frequency output: `de=0.01d0` eV and `nenergy=3000`.
- Parallel configuration: four MPI processes and 12 OpenMP threads per
  process on one node.
- Compiler, optional libraries, and exact build options: unknown.

## Procedure

1. Obtain the GS input and `Si_rps.dat` from the SALMON2 `v.2.3.0` sample
   `samples/exercise_04_bulkSi_gs`.
2. Run SALMON with the GS input and require the `#GS converged` marker.
   Record the final density residual and band gap.
3. Obtain the RT input from
   `samples/exercise_06_bulkSi_rt`. Link or copy the GS
   `data_for_restart` directory as `restart` in the RT run directory.
4. Run SALMON with the RT input. Keep the official input unchanged for this
   reproducibility check.

Minimal execution pattern (from the corresponding run directory):

```text
mpiexec -n 4 salmon < input.dat > out.dat 2> stderr.log
```

The launcher and executable path are platform dependent; use the SALMON 2.3.0
installation available on the target system.

## Observed result

The official GS and RT samples completed successfully in the tested SALMON
2.3.0 environment.

- GS density residual: `8.0961e-10`.
- GS total energy: `-850.76385284 eV` for the eight-atom cell.
- GS fundamental gap: `1.06020364 eV`.
- RT final step and time: 6000 and `12.0 fs`.
- Maximum electron-number deviation in printed RT samples: `2.1e-8`.
- Final electronic excitation energy: `1.17316724 eV`.

## Validation

Treat the run as reproduced only when all of the following are satisfied:

- GS output contains `#GS converged`.
- RT output reaches step 6000 and time `12.0 fs`.
- Standard output contains `end SALMON`.
- Electron number remains close to 32.
- Total and excitation energies are finite.
- `Si_rt.data`, `Si_rt_energy.data`, and `Si_pulse.data` are present.

The pseudopotential summary should be checked for its reported valence count;
do not infer `nelec` only from the element name.

## Lessons learned

- Preserve the official sample inputs when establishing a reproducible
  baseline.
- A successful scheduler status alone does not establish physical validity;
  check the final step, `end SALMON`, electron number, energies, and output
  files.
- This exercise is a baseline, not a convergence recommendation. Use the
  companion convergence tutorial before interpreting a spectrum quantitatively.

## Limitations and applicability

This tutorial covers the official eight-atom Si exercise, PZ-LDA, the official KY
pseudopotential, one pulse condition, SALMON 2.3.0, and one A64FX HPC
environment. It does not establish spatial-grid, time-step, or k-point
convergence, experimental accuracy, or transferability to other systems.

## References

- [SALMON2 v.2.3.0 ground-state Si sample](https://github.com/SALMON-TDDFT/SALMON2/tree/30ba64694ec761cdb6288f01a75b8bcabf05721f/samples/exercise_04_bulkSi_gs)
- [SALMON2 v.2.3.0 pulsed-field Si sample](https://github.com/SALMON-TDDFT/SALMON2/tree/30ba64694ec761cdb6288f01a75b8bcabf05721f/samples/exercise_06_bulkSi_rt)
- [SALMON-DOCS Exercise 6](https://github.com/SALMON-TDDFT/SALMON-DOCS/blob/e4d97e0328a559f5f99c706260d9c63763be0dee/source/exercises.rst)
- Companion tutorial: [Convergence workflow and restart validation](../002-si-hhg-convergence-and-restart-validation/)
