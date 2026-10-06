# AGENTS.md

This file defines repository-wide instructions for AI coding and writing tools
working in SALMON Knowledge.

## Purpose

Maintain a small, reviewable collection of evidence-backed Markdown learning
resources about SALMON development and use. Optimize for technical accuracy,
traceability, educational value, and future retrieval rather than document
volume.

## Before making changes

- Read `README.md`, `CONTRIBUTING.md`, and the relevant template and resources.
- Run `git status --short --branch` and preserve unrelated user changes.
- Identify whether the requested information belongs here or in SALMON2,
  SALMON-DOCS, or SALMON-inputs.
- Confirm the source version, commit, platform, and verification evidence before
  describing observed behavior.

## Local working convention

- Perform per-user downloads, CIF conversions, temporary inputs, calculation
  runs, and raw outputs under `/.local/<tutorial-id>/`. The repository ignores
  `/.local/`; do not stage its contents.
- Use the ignored root-level `LOCAL_ENV.md` for non-sensitive notes about a
  local working environment, such as available executables or module names.
  Do not record credentials, allocation identifiers, internal hostnames, or
  other sensitive details there.
- Keep reproducible scripts, provenance manifests, representative inputs, and
  small derived figures in the relevant tutorial directory. A tutorial must not depend
  on unrecorded files in `/.local/` to explain or regenerate its conclusion.

## Source priority

For behavior tied to a particular version, use the following priority:

1. SALMON2 source code and tests at the referenced commit;
2. the corresponding version of SALMON-DOCS;
3. published examples in SALMON-inputs;
4. reviewed resources in this repository;
5. unreviewed notes or recollection.

Do not resolve a conflict by silently choosing the most convenient source.
State the conflict and narrow the claim to what the evidence supports.

## Creating and editing tutorials

- Start from `templates/tutorial.md` and keep its required front matter. Each
  tutorial is a directory under `tutorials/`; its `README.md` is the tutorial
  body.
  Supporting figures, representative inputs, provenance manifests, and small
  regeneration scripts belong in subdirectories of that tutorial.
- Create one tutorial for one reusable learning objective or conclusion. Split
  unrelated findings.
- Use a globally unique three-digit `SALMON-TUTORIAL-NNN` identifier and a
  matching `NNN-short-title` directory. Set the learning stage, prerequisites,
  and next tutorials in the front matter.
- Use `unknown` for facts that cannot be confirmed. Never fabricate a complete
  value for the sake of presentation.
- Separate observations, interpretations, and verified conclusions.
- Preserve exact SALMON input-variable names, commands, units, and error text.
- Prefer concise summaries and stable source links over copied logs or source.
- Mark new tutorials `draft`. Do not set `reviewed` without human review.
- When a tutorial becomes outdated, mark it `deprecated` and explain the replacement
  or changed behavior instead of deleting useful history.

## Scope boundaries

- Do not add a RAG service, vector database, indexing pipeline, CI workflow, or
  mailing-list ingestion unless a task explicitly requests it.
- Do not duplicate complete inputs from SALMON-inputs, formal documentation from
  SALMON-DOCS, or implementation documentation that belongs in SALMON2. A
  tutorial may include one small, representative input when it is necessary to
  reproduce the tutorial's conclusion; link to SALMON-inputs for published input
  collections and avoid copying multiple variants.
- Do not add large calculation outputs, build directories, binary artifacts, or
  generated caches.
- Small derived figures that support a tutorial are allowed under that tutorial's
  `figures/` directory. Do not commit raw output files or temporary caches.
- Do not include credentials, personal data, unpublished research, restricted
  data, allocation identifiers, or sensitive machine details.

## FAQ and troubleshooting

- Add an FAQ entry only for a short, stable question whose answer is supported
  by the source priority above. Link to a tutorial when the answer requires a
  reproducible procedure.
- Add a troubleshooting entry only for an observed, reproducible symptom. State
  the trigger, evidence, diagnosis, resolution, and applicability; do not turn
  a hypothesis into a documented fix.
- Keep shared evidence and procedures in one resource and link from the other
  categories rather than duplicating content.

## Verification

- Check Markdown structure, internal links, learning-path links, and the final
  Git diff.
- Verify cited repository paths, commits, versions, and commands when access is
  available.
- Report what was verified and clearly identify anything not verified.
- Do not commit or push changes unless the user explicitly requests it.
