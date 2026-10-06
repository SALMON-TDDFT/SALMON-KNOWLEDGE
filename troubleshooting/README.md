# Troubleshooting

This directory contains reproducible SALMON problems and their evidence-backed
resolutions. Each entry should state the observed symptom, trigger, diagnosis,
resolution, and applicability. Link to a tutorial when it already contains the
relevant procedure or evidence.

## Entries

Each entry is a Markdown file named `SALMON-TS-NNN-short-title.md`. Its front
matter mirrors the tutorial front matter. Its sections are Symptom, Trigger,
Evidence, Diagnosis, Resolution, and Applicability.

- [SALMON-TS-001: `theory='dft_band'` gives wrong eigenvalues at k-points off the SCF mesh (v2.3.0)](SALMON-TS-001-dft-band-off-mesh-eigenvalues.md)
- [SALMON-TS-002: Printed "Fundamental gap" keeps changing with the k mesh while the total energy is converged](SALMON-TS-002-printed-gap-depends-on-k-mesh.md)
- [SALMON-TS-003: Official sample deck writes no DOS, so a convergence ladder cannot be judged](SALMON-TS-003-sample-deck-has-no-dos-output.md)
- [SALMON-TS-004: Metal DOS near E_F converges in k much more slowly than the total energy](SALMON-TS-004-metal-dos-near-ef-converges-slowly-in-k.md)
- [SALMON-TS-005: With `temperature_k`, the printed "Total energy" rises with temperature because it is not a free energy](SALMON-TS-005-total-energy-with-temperature-is-not-free-energy.md)
- [SALMON-TS-006: Published input pairs a PBE pseudopotential with `xc='PZ'`](SALMON-TS-006-pseudopotential-functional-differs-from-xc.md)
- [SALMON-TS-007: Ground-state SCF with `nstate` equal to the number of occupied states converges very slowly](SALMON-TS-007-gs-with-only-occupied-states-converges-slowly.md)
- [SALMON-TS-008: Linear-response spectrum from an undamped impulse run keeps changing with the propagation time](SALMON-TS-008-lr-spectrum-depends-on-propagation-time.md)
- [SALMON-TS-009: Multiscale Maxwell-TDDFT with a coarse k mesh can leave a spurious static field and a negative absorbed energy](SALMON-TS-009-multiscale-coarse-k-spurious-static-field.md)
- [SALMON-TS-010: On Fugaku a ground-state run is killed in its first seconds when too many k-points sit on one node](SALMON-TS-010-fugaku-gs-killed-too-many-k-points-per-node.md)
- [SALMON-TS-011: A linear-response run killed at the time limit leaves no spectrum, but the spectrum can be rebuilt from the current](SALMON-TS-011-lr-killed-before-response-is-written.md)
