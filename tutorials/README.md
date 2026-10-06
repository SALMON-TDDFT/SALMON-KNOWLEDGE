# Tutorials

This directory is a curated, case-based learning path for SALMON calculations.
Each tutorial teaches one reusable skill using an actual, evidence-backed
calculation or development activity. The directory number is a stable catalog
identifier, not a year or a strict reading order.

## Learning paths

### Silicon HHG

1. [001: Reproduce the official Si HHG exercise](001-si-hhg-official-exercise-reproduction/)
2. [003: Build Si HHG from external CIF and UPF data](003-si-hhg-from-cif-upf/)
3. [002: Validate convergence and restart data for Si HHG](002-si-hhg-convergence-and-restart-validation/)

Tutorial 002 is an advanced calculation that uses substantial parallel
resources. Complete 001 and 003 before applying its convergence workflow.

### New-material ground states

1. [004: Build and run a 4H-SiC ground state from CIF and FHI pseudopotentials](004-4h-sic-gs-from-cif-fhi/)

### Ground-state convergence

1. [005: Converge bulk-Si ground state for total energy, band structure, and DOS](005-si-gs-convergence-bands-dos/)

Tutorial 005 starts from the official Si ground-state sample used in 001 and
applies the per-observable convergence approach of 002 to ground-state
observables. Related troubleshooting entries:
[SALMON-TS-001](../troubleshooting/SALMON-TS-001-dft-band-off-mesh-eigenvalues.md),
[SALMON-TS-002](../troubleshooting/SALMON-TS-002-printed-gap-depends-on-k-mesh.md),
[SALMON-TS-003](../troubleshooting/SALMON-TS-003-sample-deck-has-no-dos-output.md).

2. [006: Converge the Al ground state: real-space grid, k mesh, and smearing for the DOS](006-al-gs-convergence-rgrid-kmesh-smearing/)

Tutorial 006 applies the same approach to a metal, starting from a published
SALMON-inputs Al input, and records the reason for each convergence judgment.
Its k mesh judgment is provisional, pending author confirmation. Related
troubleshooting entries:
[SALMON-TS-004](../troubleshooting/SALMON-TS-004-metal-dos-near-ef-converges-slowly-in-k.md),
[SALMON-TS-005](../troubleshooting/SALMON-TS-005-total-energy-with-temperature-is-not-free-energy.md),
[SALMON-TS-006](../troubleshooting/SALMON-TS-006-pseudopotential-functional-differs-from-xc.md).

## Adding a tutorial

Create `tutorials/NNN-short-title/README.md` from
`templates/tutorial.md`. Use lowercase ASCII words separated by hyphens in the
directory name. Record the tutorial's learning stage, prerequisites, next
tutorials, and estimated computational cost in its front matter.

Do not create a tutorial merely to populate this directory. Add one only when
it teaches a distinct skill and is based on an actual calculation,
implementation, diagnosis, or validation activity.
