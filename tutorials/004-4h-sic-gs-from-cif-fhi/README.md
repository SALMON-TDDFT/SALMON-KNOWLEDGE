---
id: SALMON-TUTORIAL-004
title: 4H-SiC ground state from AFLOW CIF and FHI pseudopotentials
status: draft
verification_level: tested
learning_stage: intermediate
prerequisites: []
next_tutorials: []
estimated_cost: one small node
topics: [silicon-carbide, ground-state, cif, fhi-pseudopotential, electron-density]
salmon_version: 2.3.0
salmon_commit: 30ba64694ec761cdb6288f01a75b8bcabf05721f
platforms: [macOS (arm64)]
created_at: 2026-09-04
updated_at: 2026-09-04
contributors: []
reviewed_by: []
---

# Learning objective

Build and validate a periodic multi-element ground-state calculation from an
external CIF and compatible pseudopotentials.

# Summary

An eight-atom 4H-SiC primitive cell can be converted from the AFLOW hP8 CIF
and used for a SALMON 2.3.0 ground-state calculation with LDA FHI carbon and
silicon pseudopotentials. The recorded `2,2,1` k-point and `12,12,36`
real-space grids completed with four MPI processes and produced an electron
density cube file. This is a functional, low-cost example rather than a
convergence result.

## Context and objective

The purpose is to provide a traceable path from an external 4H-SiC crystal
structure and public FHI pseudopotentials to a small periodic SALMON GS run.
It records the structure conversion, the valence-electron choices, the
representative input, and completion checks needed before using the tutorial as
an example.

## Conditions

- SALMON: v2.3.0, commit `30ba64694ec761cdb6288f01a75b8bcabf05721f`.
- Structure: AFLOW prototype `AB_hP8_186_ab_ab-001` (`C4Si4`, eight atoms),
  with `a=3.080510` Angstrom and `c=10.084800` Angstrom.
- Coordinates: `atomic_red_coor` copied from the CIF conversion output.
- CIF conversion: SALMON2 `cif2salmon.py` at commit
  `b45cd8aa214ece58a30d63ae4c09021b83a1e9cf`, using Gemmi 0.7.5.
- Pseudopotentials: ABINIT LDA FHI `06-C.LDA.fhi` and `14-Si.LDA.fhi`; each
  reports four valence electrons. The input therefore uses `nelec=32` and
  `nstate=32`.
- Functional: `xc='PZ'`.
- Discretization: `num_kgrid=2,2,1` and `num_rgrid=12,12,36`.
- Parallel configuration: four MPI processes, matching the input's
  `nproc_k=4`. The recorded OpenMP and stack settings are in
  [provenance/run.yaml](provenance/run.yaml).
- Platform and build: macOS arm64, GCC/GFortran 16.2.0, OpenMPI 5.0.10, and
  statically linked Netlib LAPACK 3.12.1 and BLAS.

## Procedure

Obtain the exact conversion utility and its Python dependency:

```text
git clone https://github.com/SALMON-TDDFT/SALMON2.git /path/to/SALMON2
git -C /path/to/SALMON2 checkout b45cd8aa214ece58a30d63ae4c09021b83a1e9cf
python3 -m venv .local/004-4h-sic-gs-from-cif-fhi/venv
.local/004-4h-sic-gs-from-cif-fhi/venv/bin/pip install gemmi==0.7.5
export CIF2SALMON=/path/to/SALMON2/utility/cif2salmon/cif2salmon.py
```

Then fetch the external files and convert the CIF with the tracked scripts.
They write downloads and generated structure fragments only below the ignored
local work directory:

```text
tutorials/004-4h-sic-gs-from-cif-fhi/scripts/fetch_sources.sh
tutorials/004-4h-sic-gs-from-cif-fhi/scripts/convert_structure.sh
```

The representative input is
[inputs/4h-sic-gs.inp](inputs/4h-sic-gs.inp). Its lattice vectors and
reduced coordinates are copied directly from the converter's structure
fragment. The run script copies this input to the local GS work directory.

Run the input from the repository root with the Netlib-linked executable:

```text
export SALMON=/path/to/build-netlib/salmon
export NPROCS=4
tutorials/004-4h-sic-gs-from-cif-fhi/scripts/run_gs.sh
```

## Observed result

The recorded run used the representative input unchanged. It enabled the
complex-orbital path, reported `nproc_k=4`, and completed normally.

- GS convergence marker: `#GS converged at 71 : 0.85476349E-09`.
- Final SCF total energy: `-1059.36255618 eV` for the eight-atom cell.
- Final SCF gap: `4.23959072 eV`.
- Electron number at convergence: `32.000000000000028`.
- Completion marker: `end SALMON`; standard error was empty.
- Electron-density output: `4H-SiC_dns.cube`, with an `12 x 12 x 36` voxel
  grid. The raw cube is intentionally retained only in the ignored local run
  directory.

## Validation

The executed input has SHA-256
`e104ffda7395bc70d2ab1435093b90ca2737ec3d4ff02ca5b1008d64fae0cf9a` and
matches the tracked representative input byte-for-byte. The source and
pseudopotential checksums are recorded in
[provenance/sources.yaml](provenance/sources.yaml); runtime details and output
checks are in [provenance/run.yaml](provenance/run.yaml).

The run was validated by checking the complex-orbital and k-point process
configuration, the GS convergence and `end SALMON` markers, empty standard
error, electron number, and presence and header dimensions of the cube file.

## Lessons learned

- A CIF conversion supplies a structure fragment, not a complete DFT input.
  Set pseudopotentials, valence-electron count, orbital count, grids, and SCF
  controls explicitly.
- Retain the lattice-vector representation emitted by the conversion step when
  reproducing this finite-grid example.
- Confirm a cube output by its header and successful GS completion, rather
  than relying on the process exit status alone.

## Limitations and applicability

This tutorial covers one 4H-SiC structure source, PZ-LDA FHI pseudopotentials, one
small grid, and a single macOS arm64 Netlib-linked build. It does not establish
k-point, real-space-grid, pseudopotential, or structural convergence; the
reported energy and gap must not be treated as material reference values. It
does not validate other SALMON versions or architectures.

## References

- [AFLOW 4H-SiC prototype](https://www.aflowlib.org/prototype-encyclopedia/AB_hP8_186_ab_ab-001/)
- [SALMON2 cif2salmon utility at the recorded commit](https://github.com/SALMON-TDDFT/SALMON2/tree/b45cd8aa214ece58a30d63ae4c09021b83a1e9cf/utility/cif2salmon)
- [ABINIT LDA FHI pseudopotential collection](https://www.abinit.org/atomic_data/psps/miscellaneous/ATOMICDATA/LDA_FHI/)
- [Representative input](inputs/4h-sic-gs.inp) and [source provenance](provenance/sources.yaml)
