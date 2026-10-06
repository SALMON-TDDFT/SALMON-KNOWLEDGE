# Style guide

Conventions for every file in this repository. Read this before writing or
editing a tutorial, a troubleshooting entry, or an FAQ entry. One line per
rule; the files in `templates/` already follow it.

## Files and directories

- Tutorial: `tutorials/NNN-short-title/README.md`; `NNN` is a globally unique three-digit number and the slug is lowercase ASCII words joined by hyphens.
- Tutorial subdirectories: `figures/` (small derived PNGs), `inputs/` (one representative input, or the few the conclusion needs), `scripts/` (regeneration scripts, executable), `provenance/` (`run.yaml`, `sources.yaml`).
- Troubleshooting entry: `troubleshooting/SALMON-TS-NNN-short-title.md`, one file per entry, same slug rules.
- Reserved numbers: a number taken by a tutorial or entry in review stays reserved (none at present); do not reuse it. Record reservations in `tutorials/README.md`.
- Per-user work goes under `.local/<tutorial-directory-name>/` at the repository root (ignored by Git); a tutorial must not depend on it.
- Identifiers (`SALMON-TUTORIAL-NNN`, `SALMON-TS-NNN`) stay stable after review even if a directory is renamed.

## Front matter

- Tutorial keys, in this order: `id`, `title`, `status`, `verification_level`, `learning_stage`, `prerequisites`, `next_tutorials`, `estimated_cost`, `topics`, `salmon_version`, `salmon_commit`, `platforms`, `created_at`, `updated_at`, `contributors`, `reviewed_by`.
- Troubleshooting keys, in this order: `id`, `title`, `status`, `verification_level`, `salmon_version`, `salmon_commit`, `platforms`, `related_tutorials`, `created_at`, `updated_at`, `contributors`, `reviewed_by`.
- `status`: `draft`, `reviewed`, or `deprecated`; only a reviewer sets `reviewed`.
- `verification_level`: `reported`, `reproduced`, `code-reviewed`, or `tested`; the Validation section must support it.
- `learning_stage`: `foundation`, `intermediate`, `advanced`, or `unknown`.
- `platforms`: a list of `Name (arch)` strings, for example `Fugaku (A64FX)`, `Wisteria/BDEC-01 (A64FX)`, `macOS (arm64)`; `A64FX` alone when the text does not name the machine.
- Dates: `YYYY-MM-DD`.
- `salmon_commit`: the full 40-character SHA or `unknown`; `salmon_version`: the release, for example `2.3.0`.
- `topics`: lowercase ASCII words and hyphens (`mos2`, `density-of-states`).
- Graph symmetry: tutorial A lists B in `next_tutorials` if and only if B lists A in `prerequisites`; a troubleshooting entry lists in `related_tutorials` every tutorial that cites it.
- Quote a `title` in YAML when it contains a colon, starts with a backtick, or contains both quote characters.

## Headings and sections

- Troubleshooting entry: the H1 equals the front-matter `title` character for character, backticks included.
- Tutorial: the title lives in the front matter only; the body starts with `# Learning objective` and `# Summary`, followed by the H2 sections below.
- Tutorial H2 sections, in this order: Context and objective; Conditions; Procedure; Observed result; Judgment record (optional); Assumptions made by the assistant (optional); Validation; Surprises and failures recorded (optional); Lessons learned; Limitations and applicability; References.
- Troubleshooting sections, in this order: Symptom; Trigger; Evidence; Diagnosis; Resolution; Applicability.
- A short status banner (a blockquote after the Learning objective) is allowed; it must say the same thing as the Judgment record.

## Links

- Link every `SALMON-TUTORIAL-NNN` or `SALMON-TS-NNN` that exists on `main` with a relative link (`../../troubleshooting/SALMON-TS-NNN-slug.md` from a tutorial, `../tutorials/NNN-slug/` from an entry); never leave a bare id.
- Name work that is not on `main` (in review, on a branch) in plain words without an id, for example "a separate linear-response tutorial (in review)".
- Link figures, inputs, scripts, and provenance by relative path inside the tutorial directory.
- Link SALMON2 source and SALMON-DOCS at a commit or tag, not at a moving branch.
- Index link text in `troubleshooting/README.md` is `SALMON-TS-NNN: <title>`.

## Notation and wording

- Cubic meshes and grids as `20^3`; non-cubic ones as written (`12 x 12 x 1`, `24,24,144`).
- ASCII in prose: `Angstrom`, `Gamma`, `E_F`; no Angstrom sign, Greek capital gamma, superscript digits, or arrow characters.
- Ranges and transitions in prose use "to" (`r24 to r28`, `k8 to k12`); arrows stay only inside code blocks and formulas.
- US spelling: artifact, behavior, center, neighbor, polarized, parallelization, gray, aluminum.
- `k-points` (noun, hyphenated), `k mesh` (no hyphen), `k-point` as an adjective (`k-point parallelization`).
- SALMON keywords in backticks in prose and headings: `num_rgrid`, `num_kgrid`, `dt`, `xc`, `nstate`, `theory='dft'`.
- Self-reference is "this tutorial" or "this entry", never "card".
- The human reviewer is "the maintainer"; an AI tool is "the AI assistant" (or "the assistant"), never a product name.
- A judgment the maintainer has not confirmed is marked "provisional (AI assistant)"; a confirmed one is recorded as the maintainer's in the Judgment record and wherever the status is repeated.
- Separate observation, interpretation, and verified conclusion; write `unknown` rather than a guessed value.
- English only.

## Content that must never appear

- Allocation or project identifiers, group names, and budget codes.
- Login names, user names, e-mail addresses, and personal contact details.
- Absolute cluster or home paths (volume, `/home` or user-home prefixes); use relative paths or placeholders such as `<data dir>`.
- Scheduler job IDs, and job scripts copied with machine-specific settings.
- Private repository names, internal hostnames, credentials, and tokens.
- Unpublished results and restricted data.
