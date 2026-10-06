---
id: SALMON-TS-002
title: Printed "Fundamental gap" keeps changing with the k mesh while the total energy is converged
status: draft
verification_level: tested
salmon_version: 2.3.0
salmon_commit: 30ba64694ec761cdb6288f01a75b8bcabf05721f
platforms: [Fugaku (A64FX)]
related_tutorials: [SALMON-TUTORIAL-005]
created_at: 2026-10-04
updated_at: 2026-10-04
contributors: []
reviewed_by: []
---

# Printed "Fundamental gap" keeps changing with the k mesh while the total energy is converged

## Symptom

In a k-point convergence ladder of a periodic ground state, the total energy
is converged, but the printed `Fundamental gap[eV]` keeps decreasing
steadily. The gap therefore appears not to be k-converged.

For bulk Si at `num_rgrid=20`, `num_kgrid` values of 6, 8, 10, 12, 14, 16,
20, and 24 printed gaps of 0.867, 0.766, 0.687, 0.645, 0.616, 0.592, 0.570,
and 0.555 eV. Over the same ladder, `E_total` varied by only 0.26 meV per
eight-atom cell, and each step from k8 onward was below 0.04 meV.

## Trigger

- `theory='dft'`, `yn_periodic='y'`, with SALMON's default shifted k mesh
  (`yn_gamma_centered='n'`).
- The valence-band maximum (VBM) and/or conduction-band minimum (CBM) lie at
  k-points that the mesh does not contain. In the eight-atom cubic Si cell,
  the VBM is at Gamma and the CBM is on Gamma-X near (0.16, 0, 0)·2π/a. An even
  shifted mesh contains neither point.

## Evidence

The printed gap is computed at the end of the SCF as the minimum
conduction-band energy minus the maximum valence-band energy over the
k-points of the calculation only
([`src/io/write.f90:1898-1919` at v.2.3.0](https://github.com/SALMON-TDDFT/SALMON2/blob/30ba64694ec761cdb6288f01a75b8bcabf05721f/src/io/write.f90#L1898-L1919)).

The following was measured in
[SALMON-TUTORIAL-005](../tutorials/005-si-gs-convergence-bands-dos/) at
`num_rgrid=20`:

| calculation | printed or derived gap (eV) |
|---|---:|
| shifted 8^3 mesh, printed | 0.766 |
| same SCF plus 128 zero-weight path points, path-resolved | 0.522 |
| Gamma-centered 8^3 mesh (`yn_gamma_centered='y'`, 729 points), printed | 0.528 |
| path-resolved gap with SCF k6 / k8 / k12 | 0.52218 / 0.52221 / 0.52221 |

At k8, the 0.244 eV excess of the mesh gap has two parts. The mesh VBM is
0.084 eV below Gamma, and the mesh CBM is 0.160 eV above the true CBM. Adding the
path changed `E_total` by only 1.2e-7 eV and did not change the mesh-only gap.

## Diagnosis

The changing printed gap is a sampling artifact of the band edges. It is not
a lack of k convergence in the SCF density or Hamiltonian. The path-resolved
gap was already converged in SCF k at k6, while the printed mesh gap was
still changing by 15 meV per step at k24.

## Resolution

- Do not use the printed `Fundamental gap` as a k-convergence criterion.
- Obtain the gap from eigenvalues at the band-edge k-points. Use a band path,
  for example zero-weight `file_kw` points as in
  [SALMON-TUTORIAL-005](../tutorials/005-si-gs-convergence-bands-dos/). In
  v2.3.0, do not use `theory='dft_band'`; see
  [SALMON-TS-001](SALMON-TS-001-dft-band-off-mesh-eigenvalues.md).
  Alternatively, use a mesh that contains the band edges, such as a Gamma-centered
  mesh for a VBM at Gamma. With an 8^3 Gamma-centered mesh, the gap was within 6 meV
  of the path-resolved gap because the CBM still lay between mesh points.
- When comparing DOS files with `yn_out_dos_set_fe_origin='y'`, remember
  that the origin is the sampled VBM. It moves when path points or a different
  mesh are added: by 84 meV at k8 and 10 meV at k24.

## Applicability

- Confirmed: SALMON v2.3.0, bulk Si, PZ-LDA, FHI98PP, shifted meshes 6^3 to
  24^3, `num_rgrid` 16–28.
- General mechanism: any insulator or semiconductor whose band edges are not
  on the k mesh. The size of the artifact depends on the material and mesh.
  The printed `BG between same k-point[eV]` is also sampled on the same mesh.
