---
id: SALMON-TS-014
title: On an fcc primitive cell an even, offset k mesh gives a transverse current that cubic symmetry forbids
status: draft
verification_level: tested
salmon_version: 2.3.0
salmon_commit: 30ba64694ec761cdb6288f01a75b8bcabf05721f
platforms: [Fugaku (A64FX)]
related_tutorials: []
created_at: 2026-10-14
updated_at: 2026-10-14
contributors: []
reviewed_by: []
---

# On an fcc primitive cell an even, offset k mesh gives a transverse current that cubic symmetry forbids

## Symptom

A `theory='tddft_response'` run on a cubic crystal in its fcc primitive cell,
kicked along z (`epdir_re1 = 0, 0, 1`), writes a large current along x and y
in `<sysname>_rt.data`. The columns `Jm_x` and `Jm_y` are equal to each
other, and after the kick their rms is about half that of `Jm_z`. For a
cubic crystal the conductivity tensor is a multiple of the identity, so a z
field should drive no x or y current at all.

For diamond (2-atom cell, k 6^3 and 8^3, 50 fs propagation):

| `num_rgrid` | k mesh | rms `Jm_x` / rms `Jm_z` (t > 1 fs) |
|---|---|---|
| 16^3 | 6^3 | 0.52 |
| 32^3 | 6^3 | 0.53 |
| 32^3 | 8^3 | 0.57 |

Right after the kick (t < 0.01 fs) `Jm_x` is 10^-5 of `Jm_z`. The transverse
current builds up afterwards, so it is a response, not a mislabelled column.

## Trigger

- The cell is the fcc primitive cell (`al_vec1 = 0, a/2, a/2`, and so on),
  not the cubic conventional cell.
- `num_kgrid` is even in each direction, and `yn_gamma_centered` is left at
  its default `'n'`.

With the default, `init_kvector` in `src/common/lattice.f90` places the k
points at `(i - 0.5)/n - 0.5`, i = 1..n, in reduced coordinates. For even n
this mesh does not contain Gamma; it is offset by half a step.

## Evidence

The weighted k set was checked against the 48 operations of the cubic point
group, as reduced coordinates modulo the reciprocal lattice:

| `num_kgrid` | `yn_gamma_centered` | operations that do not map the set onto itself |
|---|---|---|
| 6 | `'n'` | 36 of 48 |
| 8 | `'n'` | 36 of 48 |
| 5 | `'n'` | 0 |
| 6 | `'y'` | 0 |

The offset even mesh keeps only the 12 operations that fix the [111] axis.
With that symmetry the conductivity has the form `sigma = a I + b n n^T` with
`n = (1, 1, 1)/sqrt(3)`. A z field then gives `J = a z + (b/3)(1, 1, 1)`:
`J_x = J_y = b/3`, as observed.

The same ratio at `num_rgrid` 16^3 and 32^3 rules out the real-space grid as
the cause. In the transformed spectrum `|eps_xz|` reaches 0.34 of the peak of
`Im eps_zz` at k 6^3 and at k 8^3, with or without a 10 fs damping.

## Diagnosis

The offset even k mesh breaks the cubic symmetry of the fcc primitive cell
down to the [111] axis. The transverse current is k sampling, not physics.

It does not spoil `eps_zz`. With `sigma = a I + b n n^T`,
`sigma_zz = a + b/3 = Tr(sigma)/3`. That is the cubic average, the same
quantity a symmetric mesh converges to. So the z spectrum is still a valid k
ladder point. It is unconverged in k in the ordinary way (see
[SALMON-TS-012](SALMON-TS-012-undamped-lr-spectrum-is-spiky-with-coarse-k.md)),
but it is not biased toward one direction.

## Resolution

- For the dielectric function of a cubic crystal, use the component along
  the kick (`Jm_z` for z polarization) and ignore `Jm_x` and `Jm_y`. The z
  component already equals the cubic average.
- To get a k set with the full cubic symmetry, use an odd `num_kgrid`, or
  set `yn_gamma_centered = 'y'`. For even n the Gamma-centered mesh has
  (n+1)^3 points with halved weights on the zone faces, so plan
  `nproc_k` for that count.
- Do not use the transverse current as a sign that the run went wrong, and
  do not take it as a physical off-diagonal response.

## Applicability

- Observed with SALMON v2.3.0 on Fugaku for bulk diamond in the 2-atom fcc
  primitive cell, `num_kgrid` 6^3 and 8^3, `num_rgrid` 16^3 and 32^3.
- The k-set symmetry check applies to any fcc primitive cell with an even
  offset mesh: Si, C, Ge, GaAs, Al, Cu.
- A cubic conventional cell (as in the official Si linear-response sample)
  has a simple cubic reciprocal lattice, whose offset meshes keep the cubic
  symmetry.
- Not tested: a run with `yn_gamma_centered = 'y'` or an odd mesh, to show
  directly that the transverse current vanishes.
