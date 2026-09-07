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

## Adding a tutorial

Create `tutorials/NNN-short-title/README.md` from
`templates/tutorial.md`. Use lowercase ASCII words separated by hyphens in the
directory name. Record the tutorial's learning stage, prerequisites, next
tutorials, and estimated computational cost in its front matter.

Do not create a tutorial merely to populate this directory. Add one only when
it teaches a distinct skill and is based on an actual calculation,
implementation, diagnosis, or validation activity.
