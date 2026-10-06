---
id: SALMON-TS-009
title: Multiscale Maxwell-TDDFT with a coarse k mesh can leave a spurious static field and a negative absorbed energy
status: draft
verification_level: tested
salmon_version: 2.3.0
salmon_commit: 30ba64694ec761cdb6288f01a75b8bcabf05721f
platforms: [Fugaku (A64FX)]
related_tutorials: []
created_at: 2026-10-06
updated_at: 2026-10-06
contributors: []
reviewed_by: []
---

# Multiscale Maxwell-TDDFT with a coarse k mesh can leave a spurious static field and a negative absorbed energy

## Symptom

In a `theory='multi_scale_maxwell_tddft'` run of a thin film, the
macroscopic vector potential `Ac_tot` does not return to zero after the
pulse. It ramps up while a nearly constant electric field remains inside the
film, and ends at the same value at every macro point. At the front macro
points the electronic energy `Eall - Eall0` in `<sysname>_rt_energy.data`
becomes negative, i.e. the medium ends below its ground state. The job
itself finishes normally: the electron number is conserved, nothing becomes
NaN, and nothing grows.

For a 400 Angstrom Si film (the official `exercise_07_bulkSi_ms` setup:
8 macro points of 50 Angstrom, `Acos2` pulse at 1.55 eV, 1e12 W/cm^2,
`tw1 = 10.672` fs, 16 fs; FHI98PP LDA instead of the sample's pseudopotential,
`nstate = 32`):

| microscopic grid | k mesh | dt (fs) | `Ac_tot_z` at 16 fs, macro 1 / 4 / 8 | mean `E_tot_z` 10-15 fs, macro 1 (V/Angstrom) | `Eall - Eall0` at 16 fs, macro 1 (eV) | R / T |
|---|---|---|---|---|---|---|
| 20^3 | 4^3 | 0.001 | 0.0933 / 0.0933 / 0.0933 | -1.5e-2 | **-0.0147** | 0.781 / 0.204 |
| 20^3 | 4^3 | 0.0005 | 0.0933 / 0.0933 / 0.0933 | -1.5e-2 | **-0.0147** | 0.781 / 0.204 |
| 20^3 | 8^3 | 0.001 | 0.0015 / 0.0016 / 0.0018 | -1.0e-3 | +0.0051 | 0.720 / 0.227 |
| 12^3 | 4^3 | 0.002 | -0.0009 / +0.0020 / +0.0056 | +1.4e-3 | +0.125 | 0.699 / 0.140 |
| 12^3 | 8^3 | 0.002 | 0.0007 / 0.0008 / 0.0002 | -2.1e-3 | +0.041 | 0.692 / 0.172 |

(`Ac` in fs V/Angstrom; R and T are the time integrals of the squared
reflected and transmitted fields over that of the incident field, up to
16 fs.)

## Trigger

- Multiscale Maxwell-TDDFT of an insulator with a coarse microscopic k mesh
  (here 4^3 for the 8-atom Si cell, as in the official sample).
- It appeared for one microscopic grid (20^3) and not for the coarser one
  (12^3) at the same k mesh, so it cannot be ruled out just because a
  previous run with the same k mesh looked clean.

## Evidence

- The decks differ only in the stated variable (checked by diff of the full
  input and job script).
- Halving `dt` reproduces every quantity of the 20^3/4^3 run to 2e-4
  (relative): the effect is not a time-step artifact.
- Going from 4^3 to 8^3 k-points at 20^3 removes it: `Ac` relaxes to about
  0 after the pulse, as in the 12^3 runs, the residual field drops by a
  factor of 15 to 30, and `Eall - Eall0` stays positive at every macro point.
- Single-cell `theory='tddft_pulse'` runs with the same pulse and no Maxwell
  coupling never went below the ground state (20^3/4^3 at two `dt`, 20^3/8^3,
  12^3/4^3). The negative energy needs the coupling to the macroscopic field.
- A single-cell linear-response run at 20^3/4^3 already showed a non-zero
  conductivity at the lowest frequency in the written spectrum (see
  [SALMON-TS-008](SALMON-TS-008-lr-spectrum-depends-on-propagation-time.md)
  for the part of that which is a window effect).

## Diagnosis

Established: the effect is set by the k mesh, not by the time step or the
macroscopic grid, and it needs the Maxwell coupling.

Probable mechanism (from reading the v2.3.0 source, not proven by
instrumenting it): on a coarse mesh a uniform vector potential is not a pure
gauge, because the Brillouin-zone sum over the shifted points `k + A` is not
invariant. The electrons then carry a small spurious low-frequency current.
In the one-dimensional Maxwell solver the spatially uniform mode is not
damped by the absorbing boundaries; it integrates that current into a
uniform `Ac` and keeps it. The electronic energy at `k + A` on a coarse mesh
also differs from that at `A = 0`, so `Eall - Eall0` can become negative.

## Resolution

Microscopic k mesh for this Si film (8-atom cell), as zones rather than one
value, because the choice is a trade-off with cost:

| zone | k mesh | what was seen |
|---|---|---|
| safe | 8^3 and above | R and T within 1% of 12^3; `Ac` back near zero; energy positive everywhere |
| caution | 4^3 to 6^3 | R and T off by several percent; a spurious static field can appear (above) |

(6^3 was not run; it is placed in the caution zone by interpolation.)

- Check `Ac_tot` at the end of the run at every macro point. After the pulse
  has left, it should oscillate around zero. A uniform offset or a steady
  ramp means the microscopic k mesh is too coarse.
- Check `Eall - Eall0` at every macro point for negative values.
- Raise the microscopic k mesh. Here 8^3 removed the effect at 20^3.
- Treat the official sample's 4^3 k mesh (and its 12^3 grid) as a quick
  functional test, not as converged settings: in the same study the
  absorbed energy of a single cell at 12^3 was 1.9 times that at 20^3, and
  R and T changed with both the grid and the k mesh.
- Converge R and T separately in k; 16 fs was also not long enough for the
  reflected and transmitted fields to die out (3-6% of the incident peak
  remained at 32 fs in a 12^3 run).

## Applicability

- Observed for bulk Si films with SALMON v2.3.0 on Fugaku, one pulse
  (1.55 eV, 1e12 W/cm^2). Not tested: other materials, other intensities,
  k meshes between 4^3 and 8^3, and whether 8^3 is converged for R and T.
