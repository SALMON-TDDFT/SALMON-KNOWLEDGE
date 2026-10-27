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
updated_at: 2026-10-27
contributors: []
reviewed_by: []
---

# Learning objective

Reproduce the official bulk-Si GS-to-RT HHG exercise without changing its
inputs, and confirm the completion markers and essential physical diagnostics.
For a first task, complete only the GS milestone and report its output.
RT propagation is an optional later task with separate authorization.

# Summary

SALMON's official bulk-Si ground-state and pulsed-field samples provide a
small, reproducible starting point for a silicon high-harmonic-generation
(HHG) calculation. This tutorial records how to reproduce the exercise and how
to verify that it completed correctly. The tutorial settings are not claimed
to be converged for publication use; numerical convergence is covered by
[SALMON-TUTORIAL-002](../002-si-hhg-convergence-and-restart-validation/).

## Context and objective

Review history: the previous revision recorded `reviewed_by: [MZKC]`; its
review date is unknown. The beginner procedure revised on 2026-10-27 awaits
renewed human review. Historical observations below are preserved;
`verification_level: tested` refers to the recorded calculation, not a new
execution of these revised commands.

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

### Prepare the environment and plan

Start at the repository root in a POSIX-compatible shell. Follow the
[environment route](../../workflows/basic-calculation.md#environment-and-installation-route)
if no usable SALMON executable is available. The source checkout below provides
sample files; cloning it does not build or install SALMON.

Before execution, establish the executable's version/build provenance, MPI
compatibility, and the resource budget. The recorded layout is four MPI
processes with 12 OpenMP threads each (48 threads in total). Do not assume
that layout fits a laptop. If unavailable, propose a different layout and
obtain approval; record it as an environment difference. No runtime estimate
for another machine is established here. On a scheduled system, use its
approved allocation and launcher rather than executing on a login node.

### Obtain and stage the official GS sample

Use a fresh run directory to avoid stale output. Run the following commands
from the repository root; stop if any command fails. Keep the same shell for
the subsequent steps, or restore the variables from this block.

```sh
repo_root="$PWD"
work="$repo_root/.local/001-si-hhg-official-exercise-reproduction/first-run-01"
test ! -e "$work" || { echo "Choose a new run directory; this one exists."; exit 1; }
mkdir -p "$work/gs"
git clone --no-checkout https://github.com/SALMON-TDDFT/SALMON2.git "$work/salmon2"
git -C "$work/salmon2" checkout --detach 30ba64694ec761cdb6288f01a75b8bcabf05721f
git -C "$work/salmon2" rev-parse HEAD
cp "$work/salmon2/samples/exercise_04_bulkSi_gs/Si_gs.inp" "$work/gs/input.inp"
cp "$work/salmon2/samples/exercise_04_bulkSi_gs/Si_rps.dat" "$work/gs/Si_rps.dat"
cmp "$work/gs/input.inp" "$work/salmon2/samples/exercise_04_bulkSi_gs/Si_gs.inp"
```

The pinned source commit identifies the sample. It does not identify the
installed executable's build commit; record that separately, or as `unknown`.
The pseudopotential is next to `input.inp` because the sample specifies
`file_pseudo(1)='./Si_rps.dat'`. Keep both files unchanged.

### Run the GS calculation

After the execution plan is approved, set `SALMON` to the absolute path of the
MPI-enabled SALMON 2.3.0 executable. The placeholder is not a runnable path.
The example below uses the recorded four-process, 12-thread layout and assumes
that `mpiexec` is the compatible, approved launcher on this machine.

```sh
export SALMON="<absolute path to the SALMON executable>"
test -x "$SALMON" || { echo "Set SALMON to an executable file."; exit 1; }
export OMP_NUM_THREADS=12
cd "$work/gs"
if mpiexec -n 4 "$SALMON" < input.inp > stdout.log 2> stderr.log; then
  run_status=0
else
  run_status=$?
fi
printf '%s\n' "$run_status" > exit-status.txt
```

Record a failed launcher or application exit rather than rerunning over these
logs. If your launcher or scheduler differs, the assistant must present the
concrete replacement before execution. An approved different layout must
replace both the launcher process count and the thread setting as appropriate.

### Inspect and report the first milestone

From the GS run directory:

```sh
cat exit-status.txt
rg -ni '#GS converged|end SALMON|Total energy|Fundamental gap' stdout.log
cat stderr.log
test -d data_for_restart
test -s Si_info.data
rg -n 'Total energy' Si_info.data
```

The search command uses `rg` (ripgrep); if unavailable, use
`grep -niE '#GS converged|end SALMON|Total energy|Fundamental gap' stdout.log`
and `grep -n 'Total energy' Si_info.data`.
An absent match or restart directory is evidence to investigate, not a reason
to silently change the sample. Inspect the final SCF values and the
pseudopotential's valence count. Report electron count if printed; otherwise
record it as unavailable rather than assuming it was measured.
`Si_info.data` also records the configured number of electrons; that field is
not an independent measurement of electron-number conservation.

Report the exit status, completion markers, restart directory, warnings, final
residual, energy, gap, and whether the inspected numbers are finite. Compare
with the historical GS observations below, retaining their units. Report
differences without a pass/fail tolerance. **Stop after this GS report for the
first task.** Do not proceed automatically to RT or a convergence study.

### Optional next task: RT propagation

Only after separate authorization, keep the same cell, pseudopotential, grids,
and compatible executable, and stage the official RT sample in a fresh directory.
Run this block from the same shell with `work` and `SALMON` still defined:

```sh
test ! -e "$work/rt" || { echo "RT directory already exists."; exit 1; }
mkdir -p "$work/rt"
cp "$work/salmon2/samples/exercise_06_bulkSi_rt/Si_rt_pulse.inp" "$work/rt/input.inp"
cp "$work/salmon2/samples/exercise_06_bulkSi_rt/Si_rps.dat" "$work/rt/Si_rps.dat"
test -d "$work/gs/data_for_restart"
ln -s ../gs/data_for_restart "$work/rt/restart"
cd "$work/rt"
if mpiexec -n 4 "$SALMON" < input.inp > stdout.log 2> stderr.log; then
  run_status=0
else
  run_status=$?
fi
printf '%s\n' "$run_status" > exit-status.txt
```

Use the approved layout, including `OMP_NUM_THREADS`, in both stages. The
official RT sample's comments specify a `restart` directory containing the GS
`data_for_restart`. Check the GS report before using it; directory existence
alone does not prove compatible or complete restart data. Completing this
stage does not itself validate an HHG spectrum.

## Observed result

The official GS and RT samples completed successfully in the tested SALMON
2.3.0 environment.

- GS density residual: `8.0961e-10`.
- GS total energy: `-850.76385284 eV` for the eight-atom cell.
- GS fundamental gap: `1.06020364 eV`.
- RT final step and time: 6000 and `12.0 fs`.
- Maximum electron-number deviation in printed RT samples: `2.1e-8`.
- Final electronic excitation energy: `1.17316724 eV`.

## Judgment record

| Decision | Adopted scope | Decided by | Evidence or reason |
|---|---|---|---|
| First beginner milestone | Official Si GS only; RT is a later task | the maintainer, explicit instruction in this task (2026-10-27) | A bounded first execution and output report before further calculations |
| Numerical agreement tolerance | Not selected; report measured differences without a verdict | the maintainer, explicit instruction in this task (2026-10-27) | No numerical acceptance tolerance is adopted at this stage |

The official sample's fixed model and numerical settings are retained for
reproduction. They are not newly recommended research settings. Each user's
execution plan still needs approval for their environment and resource budget.

## Validation

For the first GS milestone, check and report:

- the launcher/application exit status and any warnings or errors;
- `#GS converged` and `end SALMON` in GS standard output;
- the presence of `Si_info.data` and `data_for_restart` for an optional later
  RT task;
- finite final SCF residual, total energy, and gap, and electron count where
  available;
- numerical differences from the historical values, with the agreement verdict
  `not judged (no user-approved tolerance)`.

The official GS input sets `threshold=1.0d-9` for its SCF iteration. Retaining
that setting does not establish a tolerance for comparing energies, gaps, or
electron counts between environments. Missing or nonfinite data must be
reported explicitly. No agreement tolerance is chosen in this tutorial revision.

For an authorized RT task, additionally check:

- RT output reaches step 6000 and time `12.0 fs`.
- RT standard output contains `end SALMON`; record its exit status and warnings.
- Report electron-number deviations from 32 without a numerical acceptance verdict.
- Total and excitation energies are finite.
- `Si_rt.data`, `Si_rt_energy.data`, and `Si_pulse.data` are present.

The pseudopotential summary should be checked for its reported valence count;
do not infer `nelec` only from the element name.

The revised commands were checked against the fixed source sample paths and
inputs. They have not been newly validated by a SALMON run on another platform.

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
