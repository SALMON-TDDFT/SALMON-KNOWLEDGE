---
id: SALMON-TS-004
title: Metal DOS near E_F converges in k much more slowly than the total energy
status: draft
verification_level: tested
salmon_version: 2.3.0
salmon_commit: 30ba64694ec761cdb6288f01a75b8bcabf05721f
platforms: [Fugaku (A64FX)]
related_tutorials: [SALMON-TUTORIAL-006]
created_at: 2026-10-05
updated_at: 2026-10-05
contributors: []
reviewed_by: []
---

# Metal DOS near E_F converges in k much more slowly than the total energy

## Symptom

In a k-point ladder for a metallic ground state, the total energy and the
Fermi level look converged, but the DOS near E_F keeps changing. The value of
the DOS at the single energy E = E_F scatters from rung to rung without a
trend.

For bulk Al (FHI LDA, `temperature_k=300`, Gaussian DOS width 0.1 eV):

- four-atom cubic cell, anisotropic meshes 8,8,22 to 24,24,66: `E_total`
  within ±2 meV/cell from k12, but DOS(E_F) at a point
  1.631 / 1.635 / 1.718 / 1.544 / 1.673 states/eV/cell (11% spread);
- four-atom cell, isotropic meshes 12^3 to 24^3 without symmetry: E_F scattered
  over 43 meV and DOS(E_F) at a point 1.855 / 1.659 / 1.452 / 1.708 (24%
  spread);
- one-atom primitive cell at `num_rgrid=12`: from k24 to k64 `E_total` moved
  by less than 0.3 meV and E_F by less than 0.6 meV per step, while the DOS
  still changed by 9.5% of its peak at k24 to k32 and 3.6% at k32 to k48.

## Trigger

- `theory='dft'`, a metal, Fermi-Dirac occupations at a low
  `temperature_k` (300 K here), and a narrow DOS broadening
  (`out_dos_width=0.1d0` eV).
- Convergence judged from the total energy, the Fermi level, or the DOS at
  one energy.

## Evidence

Measured in [SALMON-TUTORIAL-006](../tutorials/006-al-gs-convergence-rgrid-kmesh-smearing/)
(primitive cell, r12; max_dev = 100 · max|D_b − D_a| / max D_b over −14 to
+6 eV; numbers are reference values, the judgment was made from overlays):

| pair | max_dev (% of peak) | ΔE_F (meV) | ΔE_total (meV) | change of ±1 eV window mean |
|---|---:|---:|---:|---:|
| k16 to k24 | 19.8 | +20.2 | +0.06 | +0.94% |
| k24 to k32 | 9.50 | +0.02 | −0.22 | −0.36% |
| k32 to k48 | 3.59 | −0.57 | −0.04 | +0.09% |
| k48 to k64 | 1.44 | +0.23 | −0.001 | +0.01% |

- The pair differences oscillate with a period of about 0.3–0.8 eV and are
  not a rigid energy shift: the best rigid shift reduces the L2 difference
  by only 1–13%.
- In the four-atom cell a DOS peak near +2.1 eV and a dip near −0.5 eV
  appeared at some meshes and moved or vanished at others; the dip position
  followed the in-plane mesh number in both mesh families.
- Window means converged first: at k48 and k64 the means over ±0.25, ±0.5,
  ±1, and ±2 eV all lie between 0.405 and 0.409 states/eV/atom.

## Diagnosis

The DOS of a metal near E_F is built from states on and near the Fermi
surface. With a Gaussian width of 0.1 eV, a finite k mesh samples those
states unevenly and produces ripple whose amplitude falls only slowly with
the number of k-points. The total energy and the Fermi level are integrals
over the occupied states and average this ripple out, so they converge much
earlier. The scatter is k-sampling noise, not a lack of SCF convergence and
not a band shift.

## Resolution

- Do not use the total energy, the Fermi level, or DOS(E_F) at a single
  point as the k criterion for a metal DOS.
- Judge from overlays of the DOS and of adjacent-rung differences over the
  whole window, and use window means near E_F as supporting numbers.
- Extend the ladder until the adjacent difference is ripple without a shift
  at the resolution you need. For Al in the primitive cell at σ = 0.1 eV
  this needed `num_kgrid=48,48,48` (confirmed by the maintainer, see the tutorial).
  Use the smallest cell: the primitive cell reaches a given k density with a
  quarter of the four-atom cell's grid points.
- A larger DOS width converges at fewer k-points; choose it as a resolution
  decision, not to hide ripple. Do not quote peaks or dips that move with
  the mesh.

## Applicability

- Confirmed: SALMON v2.3.0, fcc Al, PZ-LDA, FHI98PP, 300 K, Gaussian DOS
  width 0.1 eV, half-shifted meshes up to 64^3 (primitive) and 24^3 / 24,24,66
  (four-atom).
- General mechanism: any metal or system with a Fermi surface. The k mesh
  needed depends on the material, the cell, the smearing, and the DOS width.
  A k mesh converged for the ground-state DOS is not proven to be converged
  for response calculations.
