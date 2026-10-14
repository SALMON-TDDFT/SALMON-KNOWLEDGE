---
id: SALMON-TUTORIAL-008
title: "Converging an alpha-quartz SiO2 ground state: real-space grid and k mesh for the DOS"
status: draft
verification_level: tested
learning_stage: intermediate
prerequisites: [SALMON-TUTORIAL-005]
next_tutorials: []
estimated_cost: 13 runs of 2-54 nodes, each under 12 minutes (about 22 node-hours in total)
topics: [sio2, alpha-quartz, insulator, ground-state, convergence, density-of-states, k-points, real-space-grid, localized-states, hexagonal-cell]
salmon_version: 2.3.0
salmon_commit: 30ba64694ec761cdb6288f01a75b8bcabf05721f
platforms: [Fugaku (A64FX)]
created_at: 2026-10-06
updated_at: 2026-10-06
contributors: []
reviewed_by: []
---

# Learning objective

Choose `num_rgrid` and `num_kgrid` for the ground state of an oxide insulator
with a localized O 2s band, judging convergence from DOS overlays, and learn
which feature of the DOS limits each of the two parameters. Learn also that
the pointwise maximum difference between two DOS curves overstates
convergence trouble when a tall, sharp peak shifts by a few meV, and that
splitting the difference into a rigid shift and a shape difference gives a
usable judgment.

> **Draft.** Both convergence judgments are the maintainer's. The maintainer
> adopted **two parameter sets**, depending on whether the O 2s level (about
> -17 eV below the valence-band maximum) matters downstream: **r44, k10** when
> it does and **r36, k10** when it does not; k8 is the caution zone in both
> cases. Convergence was judged by splitting the difference between two DOS
> curves into a rigid shift (meV) and the shape difference that remains after
> the shift (% of the peak), not by the pointwise maximum difference, which
> overstates a few-meV shift of the tall O 2s peak. The AI assistant's first
> reading (r48, from the pointwise difference) and an earlier maintainer
> comment based on the same pointwise numbers are kept as superseded entries
> in the [Judgment record](#judgment-record). The structure, pseudopotentials,
> and every setting that was not varied were assumptions of the assistant;
> see [Assumptions](#assumptions-made-by-the-assistant).

# Summary

We ran a real-space-grid ladder at a thin k mesh and then a k ladder at the
grid the assistant first chose, for the 9-atom primitive cell of alpha-quartz
(LDA, FHI98PP Si and O, SALMON v2.3.0). The results were as follows.

- **Real-space grid.** The localized O 2s peak at -16.8 eV below the
  valence-band maximum dominates the DOS difference between neighboring grids
  at every rung. Judged pointwise, its maximum change falls from 5.35%
  (r36 to r44) to 1.01% (r44 to r48) and 0.66% (r48 to r56). Judged as a rigid
  shift plus a remaining shape difference against r64, with the O 2s band in
  the window (-22 to +12 eV), r36 is a 9 meV shift plus 2.3% of the peak,
  r44 a 2.5 meV shift plus 0.6%, and r48 a 1 meV shift plus 0.3%. Without the
  O 2s band (-12 to +12 eV) r36 is a 0.5 meV shift plus 1.8%, r44 no shift
  plus 0.45%, and r48 no shift plus 0.27%. Maintainer's judgment:
  **`num_rgrid` = 44,44,50 (r44) if the O 2s band is used downstream, and
  `num_rgrid` = 36,36,41 (r36) if only the upper valence and the conduction
  bands are used.**
- **k mesh.** The conduction-band DOS converges steadily with the mesh
  (pointwise 3.3%, 2.0%, 0.87% for k6 to k8, k8 to k10, k10 to k12). The
  valence-band DOS reaches a pointwise plateau of about 2% of the peak that
  does not fall from k8 to k12; it sits on the O 2s peak and at -7.3 eV.
  Against k12, k10 is a 3 meV shift plus 0.7% of the peak with the O 2s band
  and 3 meV plus 1.8% without it; k8 is 7 meV plus 1.6% and 12 meV plus 3.8%.
  The total energy is flat from k6 (0.3 meV per cell between k6 and k12).
  Maintainer's judgment: **10 x 10 x 10** (Gamma-centered, 1000 k-points, no
  symmetry) for both sets; **k8 is the caution zone**.
- **Cost.** The (r48, k10) run needs 50 nodes for 7 minutes; k12 needs 54 nodes
  for 12 minutes. The two adopted sets were not run as such: r44 and r36 were
  run at k2, and k10 at r48.

These are observations for one model: experimental alpha-quartz geometry,
PZ-LDA, FHI98PP pseudopotentials, `nstate = 48`, a Gaussian DOS width of
0.1 eV, and SALMON v2.3.0. They must not be transferred to other oxides
without repeating the ladders. Forces and stress are different quantities and
were not checked.

## Context and objective

alpha-quartz is a wide-gap insulator whose oxygen 2s states form a narrow,
localized band far below the valence band. It is a good test of how a
localized band and a set of dispersive bands pull the real-space grid and the
k mesh in different directions. We wanted a ground state whose DOS over the
whole range from the O 2s band to about 14 eV above the valence-band maximum
could be reported. Tutorial [005](../005-si-gs-convergence-bands-dos/) showed
for bulk Si that each observable needs its own convergence check; this
tutorial applies the approach to a two-species oxide in a hexagonal cell.

**Judgment rule used in this tutorial.** Convergence is judged from overlays
of the DOS and of the differences between rungs. The numbers below are
reference values. No script decides convergence. For each judgment, the
reasons and rejected alternatives are written in the
[Judgment record](#judgment-record). The definitions are:

- `max_dev` = 100 * max|D_b - D_a| / max(D_b) over the whole DOS window, where
  b is the denser rung of the pair (the "pointwise" difference); "valence" and
  "conduction" values use the part of the window below and above the
  valence-band maximum;
- `rel-L1` = 100 * sum|D_b - D_a| / sum(D_b) over the same window;
- **shift and shape**: the difference between a rung and the finest rung is
  split into a rigid shift of the energy axis (in meV) and the shape
  difference that remains after that shift (in % of the peak). This is the
  measure the maintainer judged by, because a few-meV shift of the tall, sharp
  O 2s peak produces a large pointwise difference without any change of shape
  ([SALMON-TS-013](../../troubleshooting/SALMON-TS-013-pointwise-difference-overstates-a-small-shift.md)). It is evaluated in two windows: -22 to +12 eV
  (with the O 2s band) and -12 to +12 eV (without it);
- a rule "two consecutive pairs below a tolerance" is used only as a reference.
  It names the first rung from which the next two neighbor differences are
  both below the tolerance.

## Conditions

- SALMON: v2.3.0, tag `v.2.3.0`, commit
  `30ba64694ec761cdb6288f01a75b8bcabf05721f`, unmodified for every run.
- Platform: Fugaku (A64FX), Fujitsu compiler (`mpifrtpx`), `-Kfast`, SSL2.
  Four MPI processes per node and 12 OpenMP threads per process.
  `nproc_k` equals the number of MPI processes, `nproc_ob = 1`,
  `nproc_rgrid = 1,1,1`. The number of k-points is divisible by `nproc_k` in
  every run. Runs used 2 to 54 nodes.
- Structure: 9-atom primitive hexagonal cell. The lattice constants
  (a = 4.913357 Angstrom, c = 5.405155 Angstrom) and the internal parameters
  (Si u = 0.4701; O at 0.1460, 0.4136, 0.1191 in the orthorhombic setting)
  are those of the published SALMON-inputs SiO2 ground-state input
  ([`AYamada2024_PhysRevB109_245130/SiO2_ms/gs`](https://github.com/SALMON-TDDFT/SALMON-inputs/tree/e5cf45d7378cc1aec6bb4dd4c3b534cbee8a81b9/inputfiles/AYamada2024_PhysRevB109_245130/SiO2_ms/gs)),
  which uses the 18-atom orthorhombic cell (a x a sqrt(3) x c, exactly two
  primitive cells). We rewrote it for the primitive cell with
  a1 = (a/2, -a sqrt(3)/2, 0), a2 = (a/2, a sqrt(3)/2, 0), a3 = (0, 0, c).
  Every Si has four O neighbors at 1.608-1.610 Angstrom, every O has two Si
  neighbors at 1.608 and 1.610 Angstrom, and the O-O distance is
  2.615 Angstrom. The published input itself uses `psp8` pseudopotentials
  and the TB-mBJ potential; we used neither.
- Pseudopotentials: ABINIT FHI98PP LDA, Si `14-Si.LDA.fhi` (4 valence
  electrons, `lloc_ps = 2`) and O `08-O.LDA.fhi` (6 valence electrons,
  `lloc_ps = 2`); no nonlinear core correction. `xc = 'PZ'`. Checksums are in
  [provenance/run.yaml](provenance/run.yaml).
- Electronic structure: `theory = 'dft'`, spin-unpolarized, fixed occupations
  (`temperature_k = -1`), `yn_symmetry = 'n'` (all k-points kept, no
  `sym.dat`), `nelec = 48`, `nstate = 48` (24 occupied and 24 empty bands).
- SCF: `ncg = 4`, `nscf = 600`, `threshold = 1d-9`, Broyden mixing with the
  v2.3.0 defaults, default initial orbitals. All 13 runs converged.
- DOS: `yn_out_dos = 'y'`, `yn_out_dos_set_fe_origin = 'y'` (origin at the
  valence-band maximum), Gaussian width 0.1 eV, window -22 to +14 eV, 2881
  points (0.0125 eV).
- k meshes: n x n x n on the reciprocal primitive axes with
  `dk_shift = 0.5, 0.5, 0.5`, which is Gamma-centered for even n. (The Si and Al
  tutorials use the default half-shifted mesh, which has no Gamma point. We
  expected the band edges of quartz to lie at Gamma, from earlier
  calculations that we did not repeat here, so we kept Gamma on the mesh.)

## Procedure

1. **Decide what will be judged.** The DOS over the whole window, with the
   total energy and the printed gap as side information.
2. **r ladder at a thin k mesh.** `num_rgrid` = n,n,round(9n/8) with
   n = 24, 28, 32, 36, 44, 48, 56, 64 and a 2 x 2 x 2 k mesh (8 k-points). The
   ratio 9/8 keeps the ratio of the three grid spacings of the primitive
   cell (n = 48 gives 0.1024 Angstrom along a1 and a2 and 0.1001 Angstrom
   along z). A thin mesh is used for the r ladder because the cost of a rung
   scales with the grid and the number of k-points; the pairs compare the same
   sampling. A rung at n = 40 was prepared but not run.
3. **Choose r from the r ladder.** (See the judgment below. The assistant's
   first reading was r48, at which the k ladder was then run; the
   maintainer's judgment, made later from the same data, is r44 or r36.)
4. **k ladder at the chosen r.** n x n x n with n = 4, 6, 8, 10, 12 at
   `num_rgrid` = 48,48,54; the k2 point is the r48 rung of the r ladder.
   Only even n were used, so that the mesh stays Gamma-centered.
5. **Compare rungs on overlays and differences**, look at where the largest
   difference sits in energy, and split the difference against the finest
   rung into a rigid shift and a remaining shape difference, with and without
   the O 2s band in the window.

The adopted inputs are
[inputs/sio2-gs-adopted-with-o2s.inp](inputs/sio2-gs-adopted-with-o2s.inp)
(r44, k10; for use when the O 2s band matters downstream) and
[inputs/sio2-gs-adopted-valence.inp](inputs/sio2-gs-adopted-valence.inp)
(r36, k10; upper valence and conduction bands only). They differ from each
other only in `num_rgrid`, `sysname` and the comments. Both are the deck of
the executed (r48, k10) run with `num_rgrid` set to the executed r44 or r36
value of the r ladder; only `sysname`, the pseudopotential paths, and
comments differ otherwise from the executed decks. Neither (r44, k10) nor
(r36, k10) was run as such.

## Observed result

All 13 runs reached `#GS converged`, wrote nothing to standard error,
finished with `end SALMON`, and printed a DOS whose energy axis equals the
requested window (no clamping). The DOS integral up to the valence-band
maximum was 48.000 electrons in the k10 run.

### 1. r ladder (k2)

![r ladder: DOS overlay and neighbor differences](figures/dos-rgrid-ladder-k2.png)

| pair | max_dev (% of peak) | where | max_dev valence / conduction | rel-L1 valence / conduction | ΔE_total (meV/atom) | Δgap (meV) |
|---|---:|---|---|---|---:|---:|
| r24 to r28 | 18.9 | -16.85 eV | 18.9 / 5.5 | 13.7% / 8.2% | -93.5 | +21.1 |
| r28 to r32 | 15.6 | -16.81 eV | 15.6 / 2.9 | 7.8% / 3.4% | -72.9 | +16.3 |
| r32 to r36 | 10.1 | -16.79 eV | 10.1 / 1.9 | 4.3% / 2.1% | -40.0 | +9.7 |
| r36 to r44 | 5.35 | -16.77 eV | 5.35 / 0.90 | 2.4% / 1.3% | -27.6 | +5.2 |
| r44 to r48 | 1.01 | -16.77 eV | 1.01 / 0.62 | 0.38% / 0.31% | -4.8 | +0.83 |
| r48 to r56 | 0.66 | -16.77 eV | 0.66 / 0.44 | 0.30% / 0.35% | -3.6 | +0.62 |
| r56 to r64 | 0.86 | +13.1 eV | 0.16 / 0.86 | 0.08% / 0.48% | -1.0 | +0.17 |

- In every pair, the largest valence difference is at the O 2s peak (about
  -16.8 eV). The peak moves toward the valence-band maximum as the grid is
  refined (maximum at -16.975, -16.9375, -16.9125, -16.8875, -16.8875,
  -16.875, -16.875, -16.875 eV for r24 to r64, in steps of the 0.0125 eV
  output grid) and stops moving from r44 on. Its height rises from 22.87 to
  23.09 states/eV/cell at r28 and stays between 23.06 and 23.10 afterwards.
- The conduction-band DOS differences are at most 0.9% from r36 to r44 on. The
  largest conduction difference in r56 to r64 is at +13.1 eV, near the upper
  edge of the window; we did not examine it further.
- The total energy keeps falling with r: -4.8, -3.6, and -1.0 meV/atom for
  r44 to r48, r48 to r56, and r56 to r64. It is not converged to 1 meV/atom at
  r48, and it was not used as a criterion.
- The number of SCF iterations grows with r (66 at r24 to 280 at r64).

### 2. k ladder (r48)

![k ladder: DOS overlay and neighbor differences](figures/dos-kgrid-ladder-r48.png)

| pair | max_dev (% of peak) | where | max_dev valence / conduction | rel-L1 valence / conduction | ΔE_total (meV/atom) | printed gap (eV) at the denser rung |
|---|---:|---|---|---|---:|---:|
| k2 to k4 | 36.1 | +9.5 eV | 18.9 / 36.1 | 22.8% / 52.7% | -0.887 | 5.7775 |
| k4 to k6 | 14.5 | -17.0 eV | 14.5 / 9.4 | 13.0% / 19.7% | -0.053 | 5.7526 |
| k6 to k8 | 3.31 | +10.5 eV | 2.68 / 3.31 | 2.7% / 7.1% | -0.019 | 5.7571 |
| k8 to k10 | 2.11 | -7.3 eV | 2.11 / 2.00 | 1.1% / 3.5% | -0.009 | 5.7561 |
| k10 to k12 | 2.01 | -16.8 eV | 2.01 / 0.87 | 1.2% / 1.6% | -0.005 | 5.7526 |

- **Conduction band.** The maximum deviation falls from 3.31% to 2.00% to
  0.87%, and the rel-L1 from 7.1% to 3.5% to 1.6%.
- **Valence band.** The maximum deviation is 2.68%, 2.11%, and 2.01% for
  k6 to k8, k8 to k10, and k10 to k12. It does not fall from k8 on. It is
  located at the O 2s peak (-17.0 and -16.8 eV) and at -7.3 eV. The rel-L1
  over the valence band is about 1.1-1.2% for the last two pairs.
- **O 2s peak.** Its maximum height is 22.76, 22.84, 22.88, 22.87, and 22.84
  states/eV/cell for k4 to k12, that is, a change of at most 0.2% of the
  height. The 2% difference of k10 to k12 lies on the flanks of the peak, not
  at the apex, as the zoom in the right-hand panels shows. We did not measure
  what changes in the band: the flank difference could be a small change of
  the sampled band width.
- **Total energy.** It changes by 0.05 meV/atom from k4 to k6, and by 0.03
  meV/atom (0.29 meV per cell) between k6 and k12.
- **Printed gap.** The printed gap is a minimum over the mesh points. For k6 to
  k12 it stays within 5.7526-5.7571 eV; a mesh that includes Gamma was used
  throughout. We did not track the 4 meV spread to its cause.
- **Cost.** k8 needs 16 nodes (21 GiB per node, 693 s), k10 needs 50 nodes (14 GiB,
  408 s), and k12 needs 54 nodes (21 GiB, 698 s).

![Height of the O 2s peak against r and against k](figures/o2s-peak-height.png)

### 3. Rigid shift and remaining shape difference

The pointwise numbers above are dominated by the O 2s peak: it is tall and
sharp, so a shift of a few meV along the energy axis produces a pointwise
difference of several percent of the peak although the shape of the DOS has
not changed. The maintainer therefore judged each rung against the finest
rung (r64 for the r ladder at k2, k12 for the k ladder at r48) by a rigid
shift plus the shape difference that remains after the shift, in two windows.
The pointwise maximum difference against the same finest rung is given in
brackets for comparison.

| comparison | with the O 2s band (-22 to +12 eV): shift / shape after shift [pointwise] | without the O 2s band (-12 to +12 eV): shift / shape after shift [pointwise] |
|---|---|---|
| k8 vs k12 (r48) | 7 meV / 1.6% [2.6%] | 12 meV / 3.8% [3.9%] |
| k10 vs k12 (r48) | 3 meV / 0.7% [2.0%] | 3 meV / 1.8% [2.1%] |
| r36 vs r64 (k2) | 9 meV / 2.3% [7.2%] | 0.5 meV / 1.8% [1.9%] |
| r44 vs r64 (k2) | 2.5 meV / 0.6% [1.8%] | 0 / 0.45% |
| r48 vs r64 (k2) | 1 meV / 0.3% [0.8%] | 0 / 0.27% |

(For r44 and r48 without the O 2s band no shift was found and the pointwise
value was not recorded separately.)

- **r.** With the O 2s band in the window, r36 differs from r64 by 7.2%
  pointwise but only by a 9 meV shift plus 2.3% of shape; r44 is a 2.5 meV
  shift plus 0.6%. Without the O 2s band, r36 is already within 1.8% of r64
  with a negligible shift, and r44 within 0.45%.
- **k.** k10 is within 0.7% (with O 2s) and 1.8% (without) of k12 after a
  3 meV shift. k8 is a 7 meV or 12 meV shift plus 1.6% or 3.8%.

### 4. Adopted sets

Two sets were adopted by the maintainer, depending on the later use of the
ground state.

| later use | `num_rgrid` | `num_kgrid` | safe zone | caution zone | deciding observation | judged by |
|---|---|---|---|---|---|---|
| the O 2s band is used downstream (a later response or real-time run excites it) | 44,44,50 (r44) | 10,10,10, Gamma-centered (1000 k-points) | r44 and finer; k10 and denser | k8 | r44 vs r64: 2.5 meV shift plus 0.6% (with O 2s); k10 vs k12: 3 meV plus 0.7% | maintainer |
| only the upper valence and the conduction bands are used | 36,36,41 (r36) | 10,10,10, Gamma-centered (1000 k-points) | r36 and finer; k10 and denser | k8 | r36 vs r64: 0.5 meV shift plus 1.8% (without O 2s); k10 vs k12: 3 meV plus 1.8% | maintainer |

| parameter | value | deciding observation | judged by |
|---|---|---|---|
| structure | alpha-quartz, 9-atom primitive cell, published lattice and internal parameters | not varied | assumed by the AI assistant |
| pseudopotentials / `xc` | FHI LDA Si (4e), O (6e) / `'PZ'` | not varied | assumed by the AI assistant |
| `nstate` | 48 | DOS window checked to be complete up to its end (+14 eV) | not varied |
| DOS | Gaussian, 0.1 eV, window -22 to +14 eV | convention carried over from tutorials 005 and 006 | not varied |

Neither adopted set was run at its own intersection: r44 and r36 were run at
k2 (the r ladder), and k10 at r48 (the k ladder). The (r48, k10) run, the
assistant's first adopted point, converged in 150 iterations
(residual 2.8e-10) with `E_total = -2949.178496` eV and a printed gap of
5.7561 eV, and took 408 s on 50 nodes with 14.1 GiB per node. On the 2-node k2
rungs, r44 took 58 s and r36 31 s against 97 s for r48.

### 5. All runs

| run | nodes | k-points | iterations | E_total (eV) | printed gap (eV) | calc. time (s) | memory (GiB/node) |
|---|---:|---:|---:|---:|---:|---:|---:|
| r24 k2 | 2 | 8 | 66 | -2947.020210 | 5.732682 | 6 | 1.6 |
| r28 k2 | 2 | 8 | 74 | -2947.861639 | 5.753815 | 10 | 2.0 |
| r32 k2 | 2 | 8 | 95 | -2948.517968 | 5.770135 | 17 | 2.3 |
| r36 k2 | 2 | 8 | 127 | -2948.877628 | 5.779864 | 31 | 2.8 |
| r44 k2 | 2 | 8 | 132 | -2949.126377 | 5.785042 | 58 | 4.3 |
| r48 k2 | 2 | 8 | 171 | -2949.169784 | 5.785876 | 97 | 5.2 |
| r56 k2 | 2 | 8 | 224 | -2949.202063 | 5.786492 | 212 | 7.7 |
| r64 k2 | 2 | 8 | 280 | -2949.211259 | 5.786664 | 427 | 10.9 |
| r48 k4 | 16 | 64 | 163 | -2949.177769 | 5.777514 | 93 | 5.3 |
| r48 k6 | 9 | 216 | 170 | -2949.178249 | 5.752631 | 544 | 16.4 |
| r48 k8 | 16 | 512 | 163 | -2949.178417 | 5.757116 | 693 | 20.8 |
| r48 k10 | 50 | 1000 | 150 | -2949.178496 | 5.756122 | 408 | 14.1 |
| r48 k12 | 54 | 1728 | 161 | -2949.178539 | 5.752626 | 698 | 20.8 |

The iteration column is the number printed after `#GS converged at`.

## Judgment record

| # | object | conclusion | judged by | what was looked at | reason, including rejected alternatives |
|---|---|---|---|---|---|
| 1a | r | two sets by later use: r44 (44,44,50) if the O 2s band is used downstream, r36 (36,36,41) if not; the safe zone is r44 and finer, or r36 and finer | maintainer (2026-10-06) | each rung against r64 at k2, split into a rigid shift and the remaining shape difference, with the O 2s band in the window (-22 to +12 eV) and without it (-12 to +12 eV) | With the O 2s band: r36 is a 9 meV shift plus 2.3% of the peak (7.2% pointwise), r44 a 2.5 meV shift plus 0.6% (1.8% pointwise), r48 a 1 meV shift plus 0.3% (0.8%). Without it: r36 is 0.5 meV plus 1.8% (1.9%), r44 no shift plus 0.45%, r48 no shift plus 0.27%. The pointwise difference that drove the earlier readings (1 and 1b) is dominated by a few-meV shift of the tall O 2s peak and overstates the remaining difference ([SALMON-TS-013](../../troubleshooting/SALMON-TS-013-pointwise-difference-overstates-a-small-shift.md)). r48 is therefore not needed for either use; r44 keeps the O 2s band within 0.6% after a 2.5 meV shift, and r36 keeps the rest of the DOS within 1.8%. Forces and stress were not checked. |
| 1b | r | r44 or r48, depending on whether the O 2s level is probed later | maintainer's earlier comment on the pointwise numbers, superseded by 1a | the pointwise r44 to r48 (1.01%) and r48 to r56 (0.66%) differences at the O 2s peak | Between r44 and r48 the only visible pointwise change was the height of the localized O 2s peak; r48 or finer was suggested if a later run excites the O 2s level, r44 (about 1.7 times cheaper) otherwise. Superseded because the shift and shape split shows that r44 is enough even with the O 2s band and that r36 is enough without it. |
| 1 | r | r48 | AI assistant's first reading (pointwise), superseded by 1a | r24 to r64 overlays at k2 and neighbor differences (DOS, ΔE_total, Δgap) | The largest difference of every pair is at the localized O 2s peak (-16.8 eV) and falls monotonically with r: 5.35%, 1.01%, 0.66% for r36 to r44, r44 to r48, r48 to r56; the conduction band is at most 0.9% from r44. The peak position stops moving at r44 and the gap at r48 is within 0.6 meV of r56. A rule "two consecutive pairs below the tolerance" gives r44 at 5% and at 3%, and r48 at 1% (r44 to r48 is 1.01%, then 0.66% and 0.86%). r48 was taken because it is the 1% lock and because the k ladder was prepared at r48; r40 was not run (r36 to r44 is 5.35%, so r40 would not have been usable). r44 was named as the alternative (58 s against 97 s on 2 nodes at k2), and r56 if the O 2s peak had to be accurate to below 1%. |
| 2a | k | 10 x 10 x 10 for both sets; k8 is the caution zone | maintainer (2026-10-06) | k8 and k10 against k12 at r48, split into a rigid shift and the remaining shape difference, in both windows | k10 vs k12: 3 meV shift plus 0.7% (with O 2s), 3 meV plus 1.8% (without). k8 vs k12: 7 meV plus 1.6% (with), 12 meV plus 3.8% (without). k10 is adopted; k8 is usable with caution (its 12 meV shift and 3.8% shape difference are in the part of the DOS without the O 2s band). |
| 2 | k | 10 x 10 x 10 | AI assistant's first reading (pointwise); the value is kept by 2a | k4 to k12 overlays and neighbor differences, split into valence and conduction; O 2s peak height; ΔE_total and printed gap | Conduction DOS converges monotonically (3.31%, 2.00%, 0.87%). Valence DOS stays at 2.7%, 2.1%, 2.0%, located on the O 2s peak and at -7.3 eV; the peak height changes by only 0.2%, so the plateau is a flank effect that does not shrink with k in this range. The total energy is flat from k6. The rule gives k6 at 5% and k8 at 3%, and no lock at 1%. k10 was taken because the conduction side is still at 2% between k8 and k10, and beyond k10 the only difference above 1% is the valence plateau that k12 does not remove. k8 was named as the alternative if a conduction DOS accurate to 2% is enough (it uses 16 nodes instead of 50); k12 if the conduction DOS must be below 1%, at about 1.9 times the node-time of k10 (698 s on 54 nodes against 408 s on 50). |
| 3 | structure, pseudopotentials, `nstate`, DOS settings | not varied | assumed by the AI assistant | | see [Assumptions](#assumptions-made-by-the-assistant) |

## Assumptions made by the assistant

These were fixed by the drafting assistant, not varied, and are not
convergence results.

- The geometry is the published (experimental) structure of the SALMON-inputs
  input, not an LDA-relaxed one. The LDA equilibrium geometry was not
  computed.
- FHI98PP LDA pseudopotentials for Si and O were used without checking against
  another pseudopotential set. The gap printed here must not be quoted as the
  SiO2 gap without such a check.
- Fixed occupations (`temperature_k = -1`) with the origin at the
  valence-band maximum. For an insulator this does not change the DOS shape,
  the energy, or the bands. A Fermi-level origin at 300 K would put the origin
  inside the gap.
- `nstate = 48`, `ncg = 4`, `nscf = 600`, Gaussian width 0.1 eV, and the DOS
  window -22 to +14 eV (the valence-band bottom is at about -19 eV).
- The r ladder was run at k2 because it is cheap. k2 is not a converged
  sampling; the pairs compare the same sampling.
- The k ladder was run at r48, the assistant's first choice of r, before the
  maintainer's judgment; it was not repeated at r44 or r36.

## Validation

- Each run was checked for `#GS converged`, an empty standard error, no NaN,
  the namelists read without error, `nelec` equal to the sum of the valence
  charges of the atoms (3 x 4 + 6 x 6 = 48), the `num_rgrid` echoed by SALMON,
  the number of k-points, and the DOS energy axis equal to the requested
  window. The DOS integral up to the valence-band maximum is 48.000.
- Controlled comparisons: every deck was checked before submission against
  one plan manifest that pins all keys except the ladder variables and
  `nproc_k`.
- The maintainer judged both ladders from the shift and shape split of
  section 3 and adopted the two sets of section 4.
- **Not validated:** neither adopted set was run at its own intersection
  (r44 or r36 with k10). The r ladder was run at k2 only, so the r judgment
  has not been repeated at the adopted k mesh, and the k ladder was run at
  r48, not at r44 or r36. The conduction-band difference at +13 eV in r56 to
  r64 was not examined. No pseudopotential set other than FHI98PP LDA, and no
  other functional, was tried. A response calculation (linear-response or
  real-time) was not run. Forces and stress were not checked; see
  Limitations.

## Surprises and failures recorded

- **The localized band, not the dispersive bands, sets the grid.** The
  differences between grids were largest at the O 2s band at every rung, and
  the conduction band converged faster. The printed gap follows the same
  trend as the O 2s peak (5.2, 0.83, 0.62 meV for r36 to r44, r44 to r48,
  r48 to r56).
- **The pointwise difference overstated the grid convergence.** Against r64,
  r36 is 7.2% pointwise with the O 2s band in the window but only a 9 meV
  shift plus 2.3% of shape; r44 is 1.8% pointwise but a 2.5 meV shift plus
  0.6%. The assistant's first reading (r48) and the earlier "r44 or r48"
  comment were both based on the pointwise numbers (SALMON-TS-013 (in
  review)).
- **The total energy was the slowest quantity in r.** It is still moving by
  1.0 meV/atom at r56 to r64, long after the DOS differences are below 1% of
  the peak.
- **The valence DOS did not converge in k beyond a 2% pointwise plateau**,
  while the total energy was flat from k6 and the conduction DOS kept
  converging. The plateau is on the flanks of the O 2s peak. After a 3 meV
  shift, k10 is within 0.7% of k12 with the O 2s band in the window. We do
  not know whether the plateau would fall at a much denser mesh; k12 is the
  densest we ran.
- **The printed gap varies by a few meV with k** even on a Gamma-centered mesh
  (5.7526, 5.7571, 5.7561, 5.7526 eV for k6 to k12); it is a minimum over mesh
  points (see [SALMON-TS-002](../../troubleshooting/SALMON-TS-002-printed-gap-depends-on-k-mesh.md)).
  We did not run a band path to find the band edges.
- **The number of SCF iterations rises steeply with r** (66 at r24, 280 at r64),
  and a k ladder at fixed r changes it only a little (150 to 171).

## Lessons learned

- **Look at where the largest DOS difference is.** Here it was always the
  localized O 2s peak for the grid, and the valence O 2s peak and conduction
  bands for the k mesh. The location tells you what to look at next.
- **When a tall, sharp peak dominates the difference, split it into a shift
  and a shape difference.** A few-meV shift of the O 2s peak made the
  pointwise difference several times larger than the remaining shape
  difference; judged pointwise, the ladder looked less converged than it is.
- **Decide what the ground state is for before choosing the grid.** Whether
  the O 2s band must be reproduced changes the adopted grid from r36 to r44.
- **Do not use the total energy as a convergence criterion for the grid.** It
  falls with r long after the DOS has stopped changing.
- **Judge the k ladder on separate parts of the DOS.** The conduction side and
  the valence side behaved differently, and a single number would have hidden
  that.
- **Keep Gamma on the mesh when the band edges are at Gamma**, and use
  `dk_shift = 0.5` for even n.
- **Thin-k r ladders are cheap but compare equal sampling only.** Repeat the
  chosen r at the chosen k if the answer matters.

## Limitations and applicability

This tutorial covers alpha-quartz in the published geometry, PZ-LDA, FHI98PP
Si and O, fixed occupations, a Gaussian DOS broadening of 0.1 eV, and SALMON
v2.3.0 on Fugaku (A64FX).

- The two adopted sets are for the DOS. Forces and stress are different
  quantities and were not checked; do not carry the DOS-based choice over to
  them without their own ladders.
- The k mesh needed for a ground-state DOS is a necessary condition for a
  response calculation, not a sufficient one.
- A broader DOS width would converge at a coarser mesh; only 0.1 eV was studied.
- The O 2s peak is the demanding feature of this study; which set applies
  depends on whether a later calculation reaches the O 2s level.
- Neither adopted set was run at its own intersection; the r ladder was run
  at k2 and the k ladder at r48.
- The absolute total energy was not shown to be converged in r.

## References

- [SALMON-inputs `AYamada2024_PhysRevB109_245130/SiO2_ms/gs`](https://github.com/SALMON-TDDFT/SALMON-inputs/tree/e5cf45d7378cc1aec6bb4dd4c3b534cbee8a81b9/inputfiles/AYamada2024_PhysRevB109_245130/SiO2_ms/gs) (structure)
- [ABINIT LDA FHI pseudopotential collection](https://www.abinit.org/atomic_data/psps/miscellaneous/ATOMICDATA/LDA_FHI/)
- Related tutorial: [005 Si ground-state convergence](../005-si-gs-convergence-bands-dos/)
- Troubleshooting: [SALMON-TS-002](../../troubleshooting/SALMON-TS-002-printed-gap-depends-on-k-mesh.md),
  [SALMON-TS-003](../../troubleshooting/SALMON-TS-003-sample-deck-has-no-dos-output.md);
  [SALMON-TS-013](../../troubleshooting/SALMON-TS-013-pointwise-difference-overstates-a-small-shift.md)
  (pointwise difference overstates a few-meV shift of a sharp feature).
- Run provenance: [provenance/run.yaml](provenance/run.yaml). Raw outputs are not committed.
