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
- [SALMON-TS-008: Linear-response spectrum from an undamped impulse run keeps changing with the propagation time](SALMON-TS-008-lr-spectrum-depends-on-propagation-time.md)
