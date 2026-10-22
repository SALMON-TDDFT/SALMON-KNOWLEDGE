---
id: SALMON-TS-014
title: On an fcc primitive cell the default even k mesh gives a spurious transverse response; the response along the kick is unaffected
status: reviewed
verification_level: tested
salmon_version: 2.3.0
salmon_commit: 30ba64694ec761cdb6288f01a75b8bcabf05721f
platforms: [Fugaku (A64FX)]
related_tutorials: []
created_at: 2026-10-14
updated_at: 2026-10-21
contributors: []
reviewed_by: [MZKC]
---

# On an fcc primitive cell the default even k mesh gives a spurious transverse response; the response along the kick is unaffected

## Symptom

A `theory='tddft_response'` run on a cubic crystal in its fcc primitive cell,
kicked along z (`epdir_re1 = 0, 0, 1`), writes a current along x and y
(`Jm_x` and `Jm_y` in `<sysname>_rt.data`, equal to each other) and an
`eps_x`, `eps_y` in `<sysname>_response.data` that is far from 1. For a cubic
crystal a z field drives no x or y current, so these columns should be zero
and `eps_x` should be 1.

What this entry establishes, for bulk diamond:

- `eps_z`, the response along the kick, is not biased by this mesh. The
  default even mesh is usable for `eps_z`; converge it in k at the energies
  of interest, as with any mesh.
- `Jm_x`, `Jm_y`, `eps_x` and `eps_y` are a k-sampling artifact, not an
  off-diagonal response. They shrink as k grows, slowly above 8 eV.
- A mesh that contains Gamma makes them smaller at a similar size, by a
  factor that depends on the energy band (up to about 20 above 8 eV). It is
  needed only if you use those components; on a coarse such mesh the
  low-energy `eps_z` is worse, not better.

## Trigger

- The cell is the fcc primitive cell (`al_vec1 = 0, a/2, a/2`, and so on),
  not the cubic conventional cell.
- `num_kgrid` is even in each direction, and `yn_gamma_centered` is left at
  its default `'n'`.

With the default, `init_kvector` in `src/common/lattice.f90` places the k
points at `(i - 0.5)/n - 0.5`, i = 1..n, in reduced coordinates. For even n
this mesh does not contain Gamma; it is offset by half a step.

## Evidence

All runs: bulk diamond, 2-atom fcc primitive cell, 50 fs
`theory='tddft_response'`, `num_rgrid` 20^3 unless stated, one run per
point.

**Symmetry of the k set.** The weighted k set was checked against the 48
operations of the cubic point group, as reduced coordinates modulo the
reciprocal lattice:

| `num_kgrid` | `yn_gamma_centered` | operations that do not map the set onto itself |
|---|---|---|
| 6 | `'n'` | 36 of 48 |
| 8 | `'n'` | 36 of 48 |
| 5 | `'n'` | 0 |
| 6 | `'y'` | 0 |

The offset even mesh keeps only the 12 operations that fix the [111] axis.
With that symmetry the conductivity has the form `sigma = a I + b n n^T` with
`n = (1, 1, 1)/sqrt(3)`. A z field then gives `J = a z + (b/3)(1, 1, 1)`:
`J_x = J_y = b/3`, as observed, and `sigma_zz = a + b/3 = Tr(sigma)/3`, the
cubic average.

**Size of the transverse error in the spectrum.** The table gives the rms of
`|eps_x - 1|` over each energy band, as a percentage of the rms of `|eps_z|`
over the same band:

| k mesh | k-points | 1 to 4 eV | 4 to 8 eV | 8 to 14 eV |
|---|---|---|---|---|
| offset even 6^3 | 216 | 31.5% | 17.6% | 38.3% |
| offset even 8^3 | 512 | 5.3% | 12.6% | 36.1% |
| offset even 12^3 | 1728 | 0.7% | 6.4% | 29.5% |
| offset even 16^3 | 4096 | 0.5% | 4.1% | 22.8% |
| offset even 24^3 | 13824 | 0.4% | 2.1% | 13.0% |
| offset even 32^3 | 32768 | 0.5% | 1.1% | 7.5% |
| gamma-centered 6^3 | 343 | 0.3% | 1.3% | 2.7% |
| odd 7^3 | 343 | 0.3% | 1.2% | 1.9% |
| odd 15^3 | 3375 | 0.4% | 0.5% | 1.1% |

On the offset even mesh the error generally decreases with k (monotonically
in the two higher bands), so it is a k-sampling error, and it is largest
above 8 eV. A mesh that contains Gamma is smaller at a similar size: odd
15^3 against offset 16^3 by factors of about 1.3, 8 and 21 in the three
bands. The gamma-centered 6^3 mesh (the only one tested) is at the level of
odd 7^3, against 38.3% for offset 6^3 above 8 eV; what matters is whether the
mesh contains Gamma, not whether n is odd. At 6^3 the
same numbers come out at `num_rgrid` 16^3, 24^3, 28^3 and 32^3 (38.2% to
38.4% at 8 to 14 eV), which rules out the real-space grid as the cause.

**In the time domain.** Right after the kick (t < 0.01 fs) `Jm_x` is 10^-5
of `Jm_z`, so it is a response, not a mislabelled column. On the 6^3 offset
mesh it reaches 0.34 of `Jm_z` (rms over the first 2 fs). At 32^3 it is
below 0.01 of `Jm_z` over the first 2 fs and grows to 0.3 to 0.75 of it
later, when `Jm_z` has decayed (its rms over the last 15 fs is 1/35 of that
over the first 2 fs). The ratio rms(`Jm_x`) / rms(`Jm_z`) after the kick
(0.53 at 6^3, 0.37 at 24^3, 0.25 at 32^3, 0.04 for odd 15^3) therefore
depends on the time window and does not map directly onto the error in
`eps`; judge by the spectrum.

**The response along the kick.** Re `eps_z` at 0.5, 1 and 3 eV, complex
`eps_z` at 8 eV (no `yn_lr_w0_correction`):

| k mesh | 0.5 eV | 1 eV | 3 eV | 8 eV |
|---|---|---|---|---|
| offset even 24^3 | 4.89 | 5.56 | 6.18 | 8.45 + 3.08i |
| offset even 32^3 | 4.84 | 5.57 | 6.19 | 8.20 + 3.74i |
| odd 15^3 | 4.93 | 5.54 | 6.17 | 8.94 + 4.64i |
| offset even 6^3 | 4.39 | 5.64 | 6.11 | 7.29 - 0.02i |
| gamma-centered 6^3 | 49.9 | 16.7 | 7.75 | 9.72 + 0.68i |
| odd 7^3 | 22.4 | 10.0 | 6.78 | 9.18 + 5.38i |

From 24^3 to 32^3 Re `eps_z` changes by -1.0%, +0.2% and +0.2% at 0.5, 1 and
3 eV; at 8 eV no mesh has converged. Up to 3 eV the offset mesh converges
like any other.

On the coarse meshes that contain Gamma (gamma-centered 6^3, odd 7^3, and odd
5^3 at `num_rgrid` 16^3) Re `eps_z` is far too large below 2 eV, while the
offset 6^3 mesh is close to the converged value there. The coarse
Gamma-containing meshes leave a nonzero late-time mean in `Jm_z` (-14% of its
rms for gamma-centered 6^3, -7% for odd 7^3, against 0.3% to 2.3% on
converged meshes). SALMON turns the current into `sigma(omega)` by a Fourier
transform and then `eps = 1 + 4 pi i sigma / omega`, so a nonzero mean adds a
term that grows like `1/omega^2` at low energy. Subtracting the
window-weighted mean before the transform (the formula of SALMON's
`yn_lr_w0_correction = 'y'`) brings the odd 5^3, `num_rgrid` 16^3 value at
1 eV from 33.9 down to 6.7. The mean falls to the level of the converged
meshes by 9^3 (odd).

**Residual on meshes that contain Gamma.** For odd 15^3 the 8 to 14 eV error
is 1.1% at `num_rgrid` 20^3 and 0.3% at 24^3. `dt` changes with the grid
(0.0002 and 0.00014 fs), so whether the grid or the time step causes the
drop is not separated.

**Process grid.** Odd k counts have no factor 4, so the odd runs used
`nproc_ob = 4`. A control at `num_rgrid` 16^3, k 6^3 that changed only
`nproc_ob` from 1 to 4 agreed with the original to 1.8e-7 in the current
(2.7e-5 relative) and 2.1e-5 over all components of `eps`.

`Im eps_z` is slightly negative at 1 eV and 3 eV on most meshes (about -0.03
to -0.4), so a negative value there is not a sign of this problem.

## Diagnosis

The offset even k mesh breaks the cubic symmetry of the fcc primitive cell
down to the [111] axis. That produces the transverse current
(`J_x = J_y`) and a non-unit `eps_x`, `eps_y`. It is k sampling, not
physics; it decays with k, slowly above 8 eV.

The same symmetry does not bias the response along the kick:
`sigma_zz = Tr(sigma)/3`, the cubic average that a symmetric mesh also
converges to. `eps_z` still has to converge in k in the ordinary way (see
[SALMON-TS-012](SALMON-TS-012-undamped-lr-spectrum-is-spiky-with-coarse-k.md)).

A mesh that contains Gamma keeps the cubic symmetry and gives a much smaller
transverse error, by a factor that depends on the band and the mesh size. A small residual remains and falls with the
real-space grid (or `dt`). Very coarse Gamma-containing meshes have a
separate k-sampling error: a nonzero late-time mean of the current along the
kick that spoils `eps_z` below about 2 eV.

## Resolution

- For the dielectric function of a cubic crystal, use the component along the
  kick (`eps_z` for a z kick) and converge it in k as usual. The default even
  mesh is fine for this.
- Do not read `Jm_x`, `Jm_y`, `eps_x` or `eps_y` from such a run as an
  off-diagonal response, and do not take them as a sign that the run went
  wrong.
- If you need those components small, use a mesh that contains Gamma: an odd
  `num_kgrid`, or an even one with `yn_gamma_centered = 'y'`. Then check that
  `Jm` along the kick oscillates about zero after the kick and that `eps` is
  converged in k at the energies you use; raise k if the late-time mean of
  `Jm` is far above a few percent of its rms. `yn_lr_w0_correction = 'y'`
  removes the `1/omega^2` term but not the underlying error; use its result
  as a diagnostic, not a value. SALMON accepts the flag only with
  `yn_periodic = 'y'`, and it takes effect only when `temperature < 0` (fixed
  occupations, the default).

## Applicability

- Observed with SALMON v2.3.0 on Fugaku for bulk diamond in the 2-atom fcc
  primitive cell, 50 fs `theory='tddft_response'` runs: offset even meshes
  6^3 to 32^3, odd meshes 5^3 to 15^3 and one gamma-centered 6^3 mesh,
  `num_rgrid` 16^3 to 32^3. Each point is a single run.
- The k-set symmetry check applies to any fcc primitive cell with an even
  offset mesh: Si, C, Ge, GaAs, Al, Cu. The sizes of the errors and the k at
  which they become small are for diamond only.
- A cubic conventional cell (as in the official Si linear-response sample)
  has a simple cubic reciprocal lattice, whose offset meshes keep the cubic
  symmetry. This was reasoned from the k-set symmetry, not run.
- Not tested: gamma-centered meshes other than 6^3; nonlinear response;
  a kick along a direction other than a cubic axis.
