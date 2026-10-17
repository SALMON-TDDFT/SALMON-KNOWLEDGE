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
updated_at: 2026-10-17
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

On the even ladder at `num_rgrid` 20^3 the ratio stays large and falls only
slowly with k: 0.53 (k 6^3), 0.57 (8^3), 0.61 (10^3, 12^3), 0.53 (16^3),
0.42 (20^3), 0.37 (24^3).

Odd meshes were then run with the same deck except for `num_kgrid` and the
process grid (`nproc_ob = 4` and the matching `nproc_k`, because an odd k
count has no factor 4):

| `num_rgrid` | k mesh | rms `Jm_x` / rms `Jm_z` |
|---|---|---|
| 16^3 | 5^3, 7^3, 9^3 | 0.21, 0.22, 0.18 |
| 20^3 | 7^3, 9^3, 11^3, 13^3, 15^3 | 0.049, 0.042, 0.033, 0.045, 0.040 |

At 20^3 the odd meshes reduce the transverse current by about a factor of
ten against every even mesh, but do not remove it. The residual is about 0.2
at 16^3 and about 0.04 at 20^3 for the same odd k. Those two sets also differ
in the time step (`dt` scales with the grid spacing, so `nt` grows from
161300 to 250000 for the same 50 fs), so the drop is an observation; its
cause has not been isolated. A control at 16^3, k 6^3 that changed only
`nproc_ob` from 1 to 4 agreed with the original to 1.8e-7 in the current
(2.7e-5 relative) and 1e-5 in `eps_zz` (2.1e-5 over all components of
`eps`); the process grid made no visible difference in that case.

The coarsest odd meshes showed a second problem: Re `eps_zz` far too large
below the gap, together with a `Jm_z` whose late-time mean is clearly
nonzero. SALMON turns the current into `sigma(omega)` by a Fourier transform
and then `eps = 1 + 4 pi i sigma / omega`, so a nonzero mean current would add
a term that grows like `1/omega^2` at low energy. The mean of `Jm_z` over the
last 20% of the run, as a fraction of its rms, and Re `eps_zz` at 1 eV:

| `num_rgrid` | k mesh | tail mean / rms `Jm_z` | Re `eps_zz` (1 eV) |
|---|---|---|---|
| 16^3 | 5^3 | -0.30 | 33.9 |
| 16^3 | 7^3 | -0.07 | 9.5 |
| 16^3 | 9^3 | 0.003 | 5.7 |
| 20^3 | 7^3 | -0.07 | 10.0 |
| 20^3 | 9^3 | -0.008 | 6.2 |
| 20^3 | 11^3, 13^3, 15^3 | 0.005 to 0.012 | 5.72, 5.64, 5.54 |
| 20^3 | even 6^3 to 24^3 | 0.003 to 0.018 | 5.54 to 5.64 (5.56 at 24^3) |

Subtracting the window-weighted mean of the saved current before the
transform (the formula of SALMON's `yn_lr_w0_correction = 'y'`) brings the
16^3, 5^3 value at 1 eV from 33.9 down to 6.7, so the mean current accounts
for most of the low-energy excess. The tail mean falls with k and is at the
level of the even meshes from 9^3 on, so it behaves as a k-sampling error.
Recovery at low energy is gradual, not complete at 9^3: the same subtraction
still moves the 20^3, 9^3 run from 6.24 to 5.85 at 1 eV and from 7.45 to 5.89
at 0.5 eV. Re `eps_zz` at 1 eV of the odd 15^3
run (3375 k-points) is within 0.02 of the even 24^3 run (13824 k-points).
That agreement is at 1 eV only; at 8 eV neither ladder has converged (odd
15^3 `8.94 + 4.64i`, even 20^3 `9.71 + 3.46i`, even 24^3 `8.45 + 3.08i`).

`Im eps_zz` is slightly negative at 1 eV and 3 eV on most meshes, even and
odd (about -0.03 to -0.4), so a negative value there is not a sign of this
problem.

## Diagnosis

The offset even k mesh breaks the cubic symmetry of the fcc primitive cell
down to the [111] axis. That gives the transverse current (`J_x = J_y`) on an
even mesh. It is k sampling, not physics, and it decays only slowly with k.

On an even offset mesh the [111] symmetry does not bias `eps_zz` toward one
direction. With `sigma = a I + b n n^T`, `sigma_zz = a + b/3 = Tr(sigma)/3`,
the cubic average, the same quantity a symmetric mesh converges to. This is a
statement about direction only; the spectrum still has to converge in k in
the ordinary way (see
[SALMON-TS-012](SALMON-TS-012-undamped-lr-spectrum-is-spiky-with-coarse-k.md)).

A symmetric odd mesh reduces the transverse current by about a factor of ten
at 20^3; a residual of unidentified origin remains, smaller on the finer grid.
On a very coarse odd mesh (5^3, 7^3 for diamond) the current along the kick
also keeps a nonzero late-time mean, and `eps` is spoiled at low energy;
removing the mean removes most of that error. The mean falls to the
even-mesh level by 9^3.

## Resolution

- For the dielectric function of a cubic crystal on an even offset mesh, use
  the component along the kick (`Jm_z` for z polarization) and ignore `Jm_x`
  and `Jm_y`. The z component equals the cubic average; converge it in k as
  usual.
- To reduce the transverse current itself, use an odd `num_kgrid`. Then
  check:
  - `Jm` along the kick oscillates about zero after the kick (for diamond the
    mean fell to the even-mesh level at 9^3), and `eps` is converged in k at
    the energies you use;
  - the remaining transverse current is small enough for your purpose (for
    diamond 0.18 to 0.22 of `Jm_z` at 16^3 and 0.03 to 0.05 at 20^3).
- Judge the low-energy `eps` by its convergence in k at the energies you
  use, against the accuracy you need. A late-time mean of `Jm` along the kick
  far above that of other meshes (here 7% to 30% of the rms, against 0.3% to
  2% on converged meshes) is a warning sign; raise k.
  `yn_lr_w0_correction = 'y'` subtracts the mean before the transform and
  removes the `1/omega^2` term, but not the underlying error; treat its
  result as a diagnostic, not a value. SALMON accepts the flag only
  with `yn_periodic = 'y'`, and it takes effect only when `temperature < 0`
  (fixed occupations, the default).
- Do not use the transverse current as a sign that the run went wrong, and do
  not take it as a physical off-diagonal response.

## Applicability

- Observed with SALMON v2.3.0 on Fugaku for bulk diamond in the 2-atom fcc
  primitive cell, 50 fs `theory='tddft_response'` runs: even meshes 6^3 to
  24^3 and odd meshes 5^3 to 15^3, `num_rgrid` 16^3, 20^3 and 32^3.
- The k-set symmetry check applies to any fcc primitive cell with an even
  offset mesh: Si, C, Ge, GaAs, Al, Cu. The k at which the mean current falls
  to the even-mesh level, and the residual of the odd mesh, are for diamond
  only.
- A cubic conventional cell (as in the official Si linear-response sample)
  has a simple cubic reciprocal lattice, whose offset meshes keep the cubic
  symmetry. This was reasoned from the k-set symmetry, not run.
- Not tested: `yn_gamma_centered = 'y'` on an even mesh.
