---
id: SALMON-TS-005
title: With temperature_k, the printed Total energy rises with temperature because it is not a free energy
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

# With temperature_k, the printed "Total energy" is not a free energy

## Symptom

In a ground-state calculation of a metal with Fermi-Dirac occupations, the
printed `Total energy` increases when `temperature_k` is raised. Total
energies of runs at different temperatures differ by tens to hundreds of meV
even though the DOS is unchanged.

For four-atom cubic Al (FHI LDA, `num_kgrid=16,16,44`, `num_rgrid=24`), the
printed `Total energy` relative to 100 K was +0.0019, +0.020, +0.079, and
+0.178 eV per cell at 300, 1000, 2000, and 3000 K.

## Trigger

- `theory='dft'` with `temperature_k` set (Fermi-Dirac occupations).
- Comparing the printed total energy between runs with different
  `temperature_k`, or reading it as a free energy.

## Evidence

Measured in [SALMON-TUTORIAL-006](../tutorials/006-al-gs-convergence-rgrid-kmesh-smearing/):

| T (K) | E(T) − E(100 K) printed (meV/cell) | Sommerfeld estimate (meV/cell) | ratio |
|---:|---:|---:|---:|
| 300 | +1.9 | +1.7 | — |
| 1000 | +20.2 | +20.8 | 0.97 |
| 2000 | +79.0 | +83.7 | 0.94 |
| 3000 | +177.7 | +188.7 | 0.94 |

The estimate is (π²/6) g(E_F) [(k_B T)² − (k_B · 100 K)²] with
g(E_F) = 1.718 states/eV/cell from the same run. The 300 K increment is
only 2 meV and is not used for the ratio.

- The logs of these runs contain one energy line, `Total energy`; there is
  no entropy, −TS, or free-energy line.
- The DOS did not change with T (relative L1 to 300 K at most 0.07%), and
  E_F moved by at most 4 meV.
- A free energy E − TS would decrease with T. The printed value increases
  and follows the electronic thermal (internal) energy within 3–6%.

## Diagnosis

With `temperature_k`, the printed `Total energy` is the energy of the
thermally occupied Kohn-Sham system without an electronic-entropy term. It
contains the thermal excitation energy of the electrons, so it rises
approximately as T². This conclusion is from the observed output and the
Sommerfeld comparison; the SALMON source was not inspected for this entry.

## Resolution

- Compare total energies only between runs at the same `temperature_k`.
- Do not interpret the printed value as a free energy. If a free energy or a
  T → 0 extrapolation is needed, compute the entropy term from the
  occupations yourself; this was not done here.
- For convergence ladders of a metal, keep `temperature_k` fixed across all
  rungs.

## Applicability

- Confirmed: SALMON v2.3.0, fcc Al, PZ-LDA, FHI98PP, Fermi-Dirac smearing at
  100–3000 K, `unit_system='A_eV_fs'`.
- Expected for any system with partially occupied states at the chosen
  temperature. For an insulator with a gap much larger than k_B T, the effect
  is negligible. Other smearing schemes, if any, were not tested.
