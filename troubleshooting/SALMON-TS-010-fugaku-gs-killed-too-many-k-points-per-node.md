---
id: SALMON-TS-010
title: On Fugaku a ground-state run is killed in its first seconds when too many k-points sit on one node
status: draft
verification_level: tested
salmon_version: 2.3.0
salmon_commit: 30ba64694ec761cdb6288f01a75b8bcabf05721f
platforms: [Fugaku (A64FX)]
related_tutorials: [SALMON-TUTORIAL-009, SALMON-TUTORIAL-011]
created_at: 2026-10-06
updated_at: 2026-10-06
contributors: []
reviewed_by: []
---

# On Fugaku a ground-state run is killed in its first seconds when too many k-points sit on one node

## Symptom

A `theory='dft'` run with many k-points ends after a few seconds. SALMON
prints no error message: standard output stops right after the
initialization lines (here, after the Ewald setup) and contains no SCF
iteration. The scheduler's standard error has a line like

```
[WARN] PLE 0610 plexec The process terminated with the signal.(rank=2)(...)(sig=9)
```

and the job statistics show a maximum memory per node at the node's usable
limit (about 27.7 GB of the 32 GB HBM2 of an A64FX node). `data_for_restart/`
is created but empty.

## Trigger

- k-point parallelization (`nproc_k` = number of MPI processes,
  `nproc_ob = 1`, `nproc_rgrid = 1,1,1`), so each process holds the
  orbitals of all its k-points on the full real-space grid.
- Many k-points per node relative to the grid and `nstate`. Here: bulk Si,
  8-atom cell, `num_rgrid = 28^3`, `nstate = 32`, 20^3 = 8000 k-points on
  20 nodes with 4 processes per node = 400 k-points per node.

## Evidence

| nodes | k-points per node | predicted memory per node | result | measured maximum memory per node |
|---:|---:|---:|---|---:|
| 20 | 400 | 28.0 GiB | killed by signal 9 after 11 s | 27.7 GiB (at the limit) |
| 40 | 200 | 14.6 GiB | converged in 97 iterations, 19.6 min | 15.1 GiB |

Same deck apart from the process count. The prediction is a fit to earlier
ground-state runs of the same cell on the same machine:

`memory per node ~ 1.2 GiB + 25 MiB x (nstate / 32) x (num_rgrid / 20)^3 x (k-points per node)`

It reproduced the measured 15.1 GiB to 3%. The memory grows linearly with
the k-points per node, with a per-k-point cost about six times the orbitals
themselves (`nstate x num_rgrid^3 x 16 bytes`, complex double): the
orbitals of this run total 84 GiB (`wfn.bin` = 8000 x 32 x 28^3 x 16 B),
i.e. 2.1 GiB per node on 40 nodes, and the rest is work arrays that scale
the same way. So the restart-file size alone underestimates the need.

## Diagnosis

The run exceeded the memory of a node while allocating the orbitals and
work arrays, and the operating system killed it (signal 9). SALMON did not
check the available memory before allocating, so the only signs are the
signal in the scheduler's error stream and the memory statistics.

## Resolution

- Estimate the memory per node before submitting, from a smaller run of the
  same system: scale the measured memory per k-point with `nstate` and with
  `num_rgrid^3`, and multiply by the k-points per node.
- Keep the estimate well below the usable node memory (about 28 GB on
  Fugaku); here 24 GiB was used as the working limit.
- Reduce the k-points per node by using more nodes (here 40 instead of 20).
- If a killed run left an empty `data_for_restart/` and a job script refuses
  to reuse such a directory, rerun in a fresh directory, and point any later
  run that reads the restart (for example `directory_read_data` of a
  real-time run) at the new directory.

## Applicability

- Observed with SALMON v2.3.0 on Fugaku (A64FX, 32 GB per node, 4 MPI
  processes per node). The numbers of the fit are specific to this cell and
  pseudopotential; the scaling with `nstate`, `num_rgrid^3`, and k-points
  per node is general for k-point parallel ground-state runs.
- Not tested: other parallelization layouts (`nproc_ob`, `nproc_rgrid`),
  which distribute the orbitals differently.
