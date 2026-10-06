---
id: SALMON-TS-007
title: "Ground-state SCF with `nstate` equal to the number of occupied states converges very slowly"
status: draft
verification_level: tested
salmon_version: 2.3.0
salmon_commit: 30ba64694ec761cdb6288f01a75b8bcabf05721f
platforms: [Fugaku (A64FX)]
related_tutorials: []
created_at: 2026-10-05
updated_at: 2026-10-05
contributors: []
reviewed_by: []
---

# Ground-state SCF with `nstate` equal to the number of occupied states converges very slowly

## Symptom

A ground-state run of an insulator with `nstate` set to exactly the number of
occupied orbitals (`nelec/2`, no empty states) needs several times more SCF
iterations than the same run with empty states, and at denser k meshes or
finer real-space grids it stops at the `nscf` cap without reaching
`threshold`. The density residual is still falling slowly when the cap is
hit.

For bulk Si (8-atom cubic cell, `a = 5.43` Angstrom, FHI98PP LDA, `xc='PZ'`,
`threshold=1.0d-9`, `nscf=300`, `nelec=32`):

| r grid | k mesh | `nstate=16` (occupied only) | `nstate=32` | `nstate=64` |
|---|---|---|---|---|
| 20^3 | 4^3 | converged at 258 iterations | 59 | 43 |
| 16^3 | 8^3 | converged at 210 | 43 | – |
| 20^3 | 8^3 | **cap at 300**, residual 6.2e-8 | 56 | – |
| 20^3 | 12^3 | **cap at 300**, residual 1.1e-8 | 63 | – |
| 20^3 | 16^3 | **cap at 300**, residual 1.1e-8 | (queued) | – |
| 24^3 | 8^3 | **cap at 300**, residual 3.2e-7 | 73 | – |

## Trigger

- `theory='dft'` for an insulator or semiconductor.
- `nstate` equal to the number of doubly occupied orbitals. This is a
  natural choice when the ground state is only a starting point for a
  real-time run (`theory='tddft_response'` or `tddft_pulse`), because the
  real-time propagation only needs the occupied orbitals and costs less with
  fewer states.
- Denser k meshes and finer `num_rgrid` make it worse.

## Evidence

- All runs above use the same binary, cell, pseudopotential, `xc`, mixing,
  `threshold`, and `nscf`. Only `nstate`, `num_rgrid`, and `num_kgrid`
  differ. The 20^3/4^3 row changes only `nstate`.
- The capped `nstate=16` runs reached the same total energy as the converged
  `nstate=32` runs to within a few μeV per cell (for example 20^3/8^3:
  −864.43078 eV vs −864.43078 eV). Their residuals had not reached the
  threshold, and in the 20^3/16^3 run the residual was noisy from about
  iteration 100 onward.
- The orbitals that do converge do not depend on `nstate` in the subsequent
  linear-response run. Three `tddft_response` runs (20^3/4^3, impulse, 12 fs)
  started from the `nstate=16`, `32`, and `64` ground states gave current
  densities and dielectric functions that agree to about 1e-8. Their cost
  per time step was also the same (18.8–19.6 ms per step on 4 nodes).

## Diagnosis

Observed behavior, not traced in the SALMON source. With no empty states
the highest computed band is the top valence band, and the iterative
eigensolver has no buffer above it. The separation that governs how fast the
top bands converge is then the band gap at each k-point, which is small in
LDA Si (about 0.5 eV) and smaller still at k-points near the conduction-band
minimum. Adding empty states moves that separation up into the conduction
bands. This is the usual explanation for block eigensolvers, and it is
consistent with the iteration counts above, but it was not verified by
instrumenting the solver.

## Resolution

- Run the ground state with empty states. For Si, `nstate=32` (16 occupied
  + 16 empty) converged in 43–73 iterations at every grid tested.
- The real-time run that restarts from this ground state should use the same
  `nstate` as the ground state. With this binary the extra empty states
  changed neither the linear-response result nor the cost per step.
- A capped run is not automatically useless: here its total energy already
  agreed with the converged run. Whether to accept it is a judgment call. In
  this campaign the job script required a converged ground state before any
  real-time run, so the capped runs were repeated with `nstate=32`.

## Applicability

- Tested only on bulk Si with a norm-conserving pseudopotential and SALMON
  v2.3.0 on Fugaku. Other insulators were run with empty states from the
  start (SiO2: 24 occupied + 24 empty; diamond: 4 occupied + 4 empty) and
  converged within the cap, so they do not test this trigger.
- Metals need empty states for the Fermi-Dirac occupations anyway and are
  outside this entry.
