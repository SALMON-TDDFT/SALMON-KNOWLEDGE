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
updated_at: 2026-10-15
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

An odd mesh was then tested directly: k 5^3 at `num_rgrid` 16^3, otherwise
the same deck. Its k set has the full cubic symmetry, yet rms `Jm_x` / rms
`Jm_z` is still 0.21, against 0.52 at k 6^3. The ratio drops, but the
transverse current does not vanish; 5^3 differs from 6^3 in density as well
as symmetry, so the drop is not assigned to symmetry, and the source of the
remaining current has not been traced. The k 5^3 run used `nproc_ob = 4`.
A control at k 6^3 that changed only `nproc_ob` from 1 to 4 agreed with the
original to 1.8e-7 in the current (2.7e-5 relative) and 1e-5 in `eps_zz`
(2.1e-5 over all components of `eps`), so
that change does not explain the k 5^3 result.

The tested k 5^3 run also showed a second, worse problem. Its `Jm_z` keeps a
constant offset after the kick, about 20 times that of k 6^3. SALMON turns
the current into `sigma(omega)` by a Fourier transform and then
`eps = 1 + 4 pi i sigma / omega`, so a constant current adds a term that
grows like `1/omega^2` at low energy:

| energy | Re `eps_zz`, k 6^3 | Re `eps_zz`, k 5^3 |
|---|---|---|
| 0.5 eV | 1.9 | 117 |
| 1 eV | 5.0 | 33.9 |
| 3 eV | 6.0 | 10.1 |

`Im eps_zz` of the k 5^3 run is negative at 1 eV and 3 eV. The saved current
was postprocessed with the formula of SALMON's `yn_lr_w0_correction = 'y'`,
which subtracts the window-weighted mean of the current before the
transform. That brings Re `eps_zz` at 1 eV down to 6.7, but the negative
`Im eps_zz` and an 8 eV difference remain. The k 5^3 mesh
contains Gamma, and the k 6^3 mesh does not.

## Diagnosis

The offset even k mesh breaks the cubic symmetry of the fcc primitive cell
down to the [111] axis. That explains the form of the transverse current
(`J_x = J_y`) on an even mesh. It is k sampling, not physics. A smaller
transverse current of unknown origin remains on a symmetric odd mesh.

On an even offset mesh the [111] symmetry does not bias `eps_zz` toward one
direction. With `sigma = a I + b n n^T`, `sigma_zz = a + b/3 = Tr(sigma)/3`,
the cubic average, the same quantity a symmetric mesh converges to. This is
a statement about direction only. The spectrum still has to converge in k
in the ordinary way (see
[SALMON-TS-012](SALMON-TS-012-undamped-lr-spectrum-is-spiky-with-coarse-k.md)),
and the low-energy part has to be checked for a constant current (see
Resolution). It does not cover the odd-mesh result above, whose cause is
open.

## Resolution

- On an even offset mesh, for the dielectric function of a cubic crystal,
  use the component along the kick (`Jm_z` for z polarization) and ignore
  `Jm_x` and `Jm_y`. The z component equals the cubic average; converge it
  in k as usual.
- An odd mesh alone is not a verified remedy. The tested diamond k 5^3 run
  still had a transverse current of 0.21 of `Jm_z`, and it exhibited a
  constant current that made `eps` unphysical below a few eV.
- If a run's `Jm` along the kick does not oscillate about zero after the
  kick, the low-energy `eps` is not usable. `yn_lr_w0_correction = 'y'`
  subtracts that offset before the transform and removes the `1/omega^2`
  term, but not the underlying error; treat the result as a diagnostic, not
  a value. SALMON accepts the flag only with `yn_periodic = 'y'`, and it
  takes effect only when `temperature < 0` (fixed occupations, the default).
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
- Odd mesh tested only at k 5^3, `num_rgrid` 16^3. Not tested:
  `yn_gamma_centered = 'y'`, and odd meshes denser than 5^3.
