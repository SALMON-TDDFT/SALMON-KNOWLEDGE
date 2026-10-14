---
id: SALMON-TS-013
title: A convergence ladder judged by the pointwise difference looks unconverged when a sharp feature shifts by a few meV
status: draft
verification_level: tested
salmon_version: 2.3.0
salmon_commit: 30ba64694ec761cdb6288f01a75b8bcabf05721f
platforms: [Fugaku (A64FX)]
related_tutorials: [SALMON-TUTORIAL-008, SALMON-TUTORIAL-009]
created_at: 2026-10-06
updated_at: 2026-10-06
contributors: []
reviewed_by: []
---

# A convergence ladder judged by the pointwise difference looks unconverged when a sharp feature shifts by a few meV

## Symptom

In a convergence ladder (grid `num_rgrid` or k mesh `num_kgrid`), the
largest pointwise difference between two rungs stays at several percent of
the peak and shrinks slowly. Judged by that number, the ladder suggests a
much finer grid or k mesh than needed.

Examples:

- Bulk Si linear response, `Im eps_z`, k 8^3. Difference from `num_rgrid=32`:
  18.9% at r16, 5.8% at r20, 2.4% at r24.
- alpha-quartz ground-state DOS (Gaussian width 0.1 eV). The O 2s peak at
  about -17 eV (height 23 states/eV) gives the largest difference: 2.6% for
  k 8^3 and 2.0% for k 10^3 against k 12^3, and 7.2% for r36 against r64.

## Trigger

A sharp feature on the compared curve: an absorption edge or peak, or a
narrow DOS peak. On its flank a small shift in energy changes the value at a
fixed energy a lot. The pointwise difference mixes up that shift with a
change of shape.

## Evidence

The difference was split into a rigid shift and a remaining shape difference:

1. Shift one curve by `s` and find the `s` that minimizes the largest
   difference.
2. Report `s` in meV and the remaining difference in percent of the peak.

| system, quantity | rungs | pointwise | shift | shape after shift |
|---|---|---|---|---|
| Si, `Im eps_z`, 1-8 eV | r16 vs r32 | 18.9% | -130 meV | about 5% |
| | r20 vs r32 | 5.8% | +30 meV | 1.2% |
| | r24 vs r32 | 2.4% | -12 meV | 0.4% |
| alpha-quartz DOS, -22 to 12 eV | k 8^3 vs 12^3 | 2.6% | 7 meV | 1.6% |
| | k 10^3 vs 12^3 | 2.0% | 3 meV | 0.7% |
| | r36 vs r64 | 7.2% | 9 meV | 2.3% |
| | r44 vs r64 | 1.8% | 2.5 meV | 0.6% |
| alpha-quartz DOS, -12 to 12 eV (without O 2s) | r36 vs r64 | 1.9% | 0.5 meV | 1.8% |

For Si, most of the r20 difference is a 30 meV shift of the whole spectrum;
the shape agrees to about 1%. At r16 the shape also changes (about 5%, and
`Re eps` at 1 eV is 6% off). For alpha-quartz, the grid moves the O 2s peak
(9 meV at r36) but hardly affects the rest of the DOS.

## Diagnosis

The pointwise difference is not a measure of shape. Near a steep feature it
is about (slope) x (shift), so a few meV look like a few percent. The
convergence of such a feature should be judged by how far it moves, in meV,
and how much the shape changes after that shift.

## Resolution

- Report a shift (meV) and a shape difference (%) for each pair of rungs,
  not only the largest pointwise difference.
- Decide the acceptable shift from the downstream use. A shift of 10-30 meV
  is small next to the band-gap error of LDA (about 0.5 eV for Si) but may
  matter when a laser is tuned to a feature.
- Judge narrow features separately. For alpha-quartz, the parameters depend
  on whether the O 2s level matters downstream: with O 2s, r44 and k 10^3;
  without it, r36 and k 10^3. In both cases k 8^3 is in the caution zone.

## Applicability

- Observed with SALMON v2.3.0 on Fugaku, for bulk Si linear response and
  alpha-quartz ground-state DOS. The issue is in the comparison, not in
  SALMON, and applies to any spectrum or DOS ladder with sharp features.
- The shift search used here was a brute-force scan of +-0.4 eV in 0.5 meV
  steps, with linear interpolation on the output energy grid.
