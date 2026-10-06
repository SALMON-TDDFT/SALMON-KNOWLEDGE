# Troubleshooting

This directory contains reproducible SALMON problems and their evidence-backed
resolutions. Each entry should state the observed symptom, trigger, diagnosis,
resolution, and applicability. Link to a tutorial when it already contains the
relevant procedure or evidence.

## Entries

Each entry is a Markdown file named `SALMON-TS-NNN-short-title.md`. Its front
matter mirrors the tutorial front matter. Its sections are Symptom, Trigger,
Evidence, Diagnosis, Resolution, and Applicability.

- [SALMON-TS-001: `theory='dft_band'` gives wrong eigenvalues off the SCF mesh (v2.3.0)](SALMON-TS-001-dft-band-off-mesh-eigenvalues.md)
- [SALMON-TS-002: Printed "Fundamental gap" depends on k-mesh sampling](SALMON-TS-002-printed-gap-depends-on-k-mesh.md)
- [SALMON-TS-003: Official sample deck writes no DOS, so a convergence ladder cannot be judged](SALMON-TS-003-sample-deck-has-no-dos-output.md)
- [SALMON-TS-004: Metal DOS near E_F converges in k much more slowly than the total energy](SALMON-TS-004-metal-dos-near-ef-converges-slowly-in-k.md)
- [SALMON-TS-005: With `temperature_k`, the printed "Total energy" is not a free energy](SALMON-TS-005-total-energy-with-temperature-is-not-free-energy.md)
- [SALMON-TS-006: Pseudopotential functional differs from the deck's `xc`](SALMON-TS-006-pseudopotential-functional-differs-from-xc.md)
- [SALMON-TS-010: On Fugaku a ground-state run is killed in its first seconds when too many k-points sit on one node](SALMON-TS-010-fugaku-gs-killed-too-many-k-points-per-node.md)
