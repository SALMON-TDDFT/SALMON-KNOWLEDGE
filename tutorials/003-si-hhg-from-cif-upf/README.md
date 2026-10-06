---
id: SALMON-TUTORIAL-003
title: Preparing a silicon HHG calculation from COD CIF and PseudoDojo UPF data
status: draft
verification_level: tested
learning_stage: intermediate
prerequisites: [SALMON-TUTORIAL-001]
next_tutorials: [SALMON-TUTORIAL-002]
estimated_cost: one small node
topics: [silicon, high-harmonic-generation, real-time-tddft, cif, pseudopotential]
salmon_version: 2.3.0
salmon_commit: unknown
platforms: [Wisteria/BDEC-01 (A64FX)]
created_at: 2026-09-04
updated_at: 2026-09-04
contributors: []
reviewed_by: []
---

# Learning objective

Build and validate a Si HHG calculation from externally obtained CIF and UPF
data, recording enough provenance to reproduce the construction.

# Summary

This tutorial prepares and test-runs ground-state (GS) and real-time (RT) SALMON inputs for
bulk-Si high-harmonic generation (HHG) without copying the crystal structure
or pseudopotential from a SALMON sample. The structure is derived from COD CIF
entry 9013102 with SALMON2's `utility/cif2salmon`, and the Si UPF is the same
file downloaded by SALMON2 testsuite 195. The inputs completed a GS calculation
and a 12-fs RT propagation on Wisteria/BDEC-01.

## Context and objective

The exercise records a traceable path from publicly available external data to
a conventional eight-atom diamond-Si SALMON model. It is intended to practice
checking the generated cell and coordinates, pseudopotential valence count,
and GS/RT consistency before interpreting an HHG result.

## Conditions

- SALMON executable and platform: version 2.3.0 on Wisteria/BDEC-01.
- Parallel configuration: one node, four MPI processes, and 12 OpenMP threads
  per process.
- CIF conversion utility: SALMON2 commit
  `b45cd8aa214ece58a30d63ae4c09021b83a1e9cf`,
  `utility/cif2salmon/cif2salmon.py`.
- CIF parser: Gemmi 0.7.5.
- Structure: COD 9013102, conventional cubic `Fd-3m` Si cell at 298.15 K,
  `al=5.4304,5.4304,5.4304` Angstrom and eight Si atoms.
- Pseudopotential: `Si.upf` obtained from the same URL as SALMON2 testsuite
  `195_bulk_Si_pseudo_upf`; its UPF header reports `z_valence="4.00"`.
- Functional: `xc='PZ'`, matching the functional used by that testsuite and
  the UPF header's Slater--Perdew--Wang LDA designation.
- HHG pulse: `ae_shape1='Acos2'`, `I_wcm2_1=1.0d12`,
  `tw1=10.672d0` fs, `omega1=1.55d0` eV, and z polarization.
- Discretization: `num_rgrid=16,16,16`, `num_kgrid=2,2,2`,
  `dt=0.002d0` fs, and `nt=6000`.

## Procedure

Use the tracked scripts from the repository root. They write only to the
ignored local work directory:

```text
tutorials/003-si-hhg-from-cif-upf/scripts/fetch_sources.sh
SALMON2_ROOT=/path/to/SALMON2 \
  tutorials/003-si-hhg-from-cif-upf/scripts/convert_structure.sh
```

Copy the representative inputs to `.local/003-si-hhg-from-cif-upf/gs/` and
`.local/003-si-hhg-from-cif-upf/rt/` as `input.inp`. The included relative
`file_pseudo` path expects `Si.upf` in `../downloads/`. Run the GS calculation
first, then provide its matching `data_for_restart` directory to the RT run as
`rt/restart/`.

## Observed result

`cif2salmon` expanded COD entry 9013102 into an eight-atom conventional Si
cell and wrote the cell and reduced coordinates used in both representative
inputs. The downloaded UPF header identifies Si with atomic number 14 and
four valence electrons.

The Wisteria/BDEC-01 test run produced the following results:

- GS converged at iteration 223 with a printed density residual of
  `8.6246312e-10` and printed `end SALMON`.
- RT reached step 6000 at `12.0 fs`, printed `end SALMON`, and had a final
  printed electron count of `31.99999964`.
- The RT run produced `Si_rt.data`, `Si_rt_energy.data`, and `Si_pulse.data`.
- Both GS and RT standard-error logs were empty.

## Validation

The source-file SHA-256 checksums and conversion tool version are recorded in
[provenance/sources.yaml](provenance/sources.yaml). The test run verified that:

- the generated structure has `natom=8` and the COD lattice constant;
- both GS and RT use the same cell, coordinates, pseudopotential, `nelec`,
  `nstate`, real-space grid, and `2,2,2` k-point grid;
- GS output contains `#GS converged` and `end SALMON`;
- RT reaches step 6000 and `12.0 fs`, prints `end SALMON`, conserves the
  electron count to the printed precision, and writes its three expected data
  files.

## Lessons learned

- `cif2salmon` produces a structure fragment. Pseudopotential, valence
  electron count, orbital count, discretization, and field parameters require
  explicit user choices.
- A conventional cell obtained from a CIF must be used consistently in both
  GS and RT; an RT restart cannot safely be reused after changing the grid or
  structure.
- The PseudoDojo file is external input data. Record its URL and checksum
  instead of committing the downloaded UPF.

## Limitations and applicability

The calculation is a single successful test run, not a numerical-convergence
study. The PZ functional and the specified PseudoDojo UPF differ from the
official Si HHG exercise's KY pseudopotential, so this tutorial does not imply
matching energies or HHG spectra. It covers only the COD conventional
diamond-Si cell, the stated external files, and one Wisteria/BDEC-01 run.

## References

- [COD entry 9013102](https://www.crystallography.net/cod/9013102.html)
- [SALMON2 cif2salmon utility at the recorded commit](https://github.com/SALMON-TDDFT/SALMON2/tree/b45cd8aa214ece58a30d63ae4c09021b83a1e9cf/utility/cif2salmon)
- [SALMON2 testsuite 195 at the recorded commit](https://github.com/SALMON-TDDFT/SALMON2/tree/b45cd8aa214ece58a30d63ae4c09021b83a1e9cf/testsuites/195_bulk_Si_pseudo_upf)
- [PseudoDojo UPF source](http://www.pseudo-dojo.org/pseudos/nc-sr_pw_standard/Si.upf.gz)
- Companion tutorials: [official Si HHG exercise](../001-si-hhg-official-exercise-reproduction/) and [convergence workflow](../002-si-hhg-convergence-and-restart-validation/)
