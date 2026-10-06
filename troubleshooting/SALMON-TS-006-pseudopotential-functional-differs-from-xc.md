---
id: SALMON-TS-006
title: "Published input pairs a PBE pseudopotential with `xc='PZ'`"
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

# Published input pairs a PBE pseudopotential with `xc='PZ'`

## Symptom

A published input runs without any warning, but the pseudopotential it uses
was generated with a different exchange-correlation functional from the one
set by `xc` in the deck.

In SALMON-inputs `AYamada2024_PhysRevB109_245130/Al_ms/gs`, the input
`Al.inp` sets `xc ='PZ'` (LDA) and reads `Al.psp8`, whose header line is:

```text
8      11   2     4   600     0    pspcod,pspxc,lmax,lloc,mmax,r2well
```

`pspxc=11` is the ABINIT code for PBE.

## Trigger

- Reusing a published or shared input, or swapping pseudopotential files,
  without checking the functional of the pseudopotential.
- SALMON v2.3.0 ran this combination without a message about the mismatch.
  Whether SALMON checks the functional of any pseudopotential format was not
  examined here.

## Evidence

Measured in [SALMON-TUTORIAL-006](../tutorials/006-al-gs-convergence-rgrid-kmesh-smearing/):
the published input (four-atom cubic cell, `num_kgrid=16,16,44`,
`num_rgrid=24`, 300 K) was run once with the published PBE `Al.psp8` and
once with FHI98PP LDA `13-Al.LDA.fhi`, all other keys equal except
`lloc_ps` (4 to 2).

| quantity | PBE psp8 + `xc='PZ'` | FHI LDA + `xc='PZ'` | difference |
|---|---:|---:|---:|
| occupied bandwidth (eV) | 11.071 | 11.059 | 0.1% |
| DOS(E_F) (states/eV/cell) | 1.730 | 1.718 | 0.7% |
| DOS mean over E_F ± 1 eV | 1.620 | 1.630 | 0.6% |
| bands 9–12 relative to E_F, PBE − LDA (mean over k) | | | +35 to +67 meV |

For Al, the observed effect on the ground-state bandwidth and DOS was small.
Absolute energies and E_F cannot be compared across pseudopotentials.

## Diagnosis

The mismatch is in the input, not in SALMON. A pseudopotential carries the
exchange-correlation functional used to generate it; using it with another
functional is an inconsistent model even when the numbers change little.
The intent of the published input (deliberate choice or oversight) is
unknown.

## Resolution

- Before the first run, compare the pseudopotential's functional with
  `xc`. For ABINIT psp8 files, read `pspxc` on the third line (11 = PBE);
  for FHI98PP files, use the table the file comes from (the ABINIT LDA_FHI
  table is LDA).
- Use a pseudopotential generated with the same functional as `xc`. In the
  tutorial, the FHI98PP LDA file was used with `xc='PZ'`.
- If a published combination must be reproduced exactly, keep it, but state
  the mismatch when reporting.

## Applicability

- Confirmed for the SALMON-inputs Al input at commit
  `e5cf45d7378cc1aec6bb4dd4c3b534cbee8a81b9`, run with SALMON v2.3.0.
- The check applies to every input and pseudopotential format. The size of
  the effect depends on the material and the observable; the small effect
  seen for the Al DOS does not imply a small effect elsewhere.
