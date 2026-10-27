# AGENTS.md

This file defines repository-wide instructions for AI coding and writing tools
working in SALMON Knowledge.

## Purpose

Maintain a small, reviewable collection of evidence-backed Markdown learning
resources about SALMON development and use. Optimize for technical accuracy,
traceability, educational value, and future retrieval rather than document
volume.

## Human decision authority

- The AI assistant may propose scientific choices and interpretations with
  evidence, alternatives, and uncertainty. Only the user decides whether to
  adopt them. An AI proposal is not an adopted conclusion.
- Scientific choices include the research objective, physical model, structure,
  functional, pseudopotentials, convergence criteria, adopted settings,
  applicability, and suitability for publication.
- Within a user-approved plan, prepare inputs, run calculations, extract
  observations, and compare them with approved criteria without asking for the
  same approval again. Approval must cover the settings, parameter ranges,
  evaluation criteria, and computational budget relevant to the task.
- When a new scientific choice or an expansion of that scope is needed, present
  a concrete proposal and wait for the user's decision before dependent work.
  Continue independent work within the approved scope.
- Execution success, SCF convergence, or passing a numerical threshold alone
  does not establish physical validity or suitability for research use.
- Never infer approval from silence, calculation success, a previous tutorial's
  settings, or another AI's assessment. Never invent a human approval record.

## Starting a calculation

- Read `workflows/basic-calculation.md` and select the relevant learning path
  in `tutorials/README.md` before preparing a calculation.
- Treat tutorial settings and judgments as evidence within their stated scope,
  not automatic approval to adopt them for a new research task.

## Knowledge admission

- A request to run or analyze a calculation does not authorize adding a
  tutorial, FAQ, or troubleshooting entry.
- Before creating an item, present a proposal using
  `templates/knowledge-proposal.md` and obtain explicit user approval for the
  topic, destination, and scope. Apply the same rule to substantive changes to
  existing conclusions, recommendations, or applicability, and to deprecation.
- Before approval, keep proposals in the conversation or the ignored
  `.local/<work-id>/` workspace. Do not assign a permanent catalog identifier,
  create a resource in the curated directories, or update their indexes.
- After approval, prepare a reviewable draft within that scope. Admission
  approval does not confirm scientific claims or authorize `reviewed` status.
- Pure spelling, formatting, and broken-link fixes that do not change technical
  meaning may proceed within an authorized maintenance task.
- Record a scientific proposal as `provisional (AI assistant)` and unadopted
  until the user explicitly accepts it. Preserve superseded judgments and
  distinguish approval to add an item from approval of its scientific content.
- Follow `CONTRIBUTING.md` for human review. Do not independently promote an
  item to `reviewed` or extend an earlier review to changed scientific content.

## Before making changes

- Read `README.md`, `CONTRIBUTING.md`, and the relevant template and resources.
- Read `STYLE.md` before writing or editing any tutorial, troubleshooting
  entry, or FAQ entry. It is mandatory: naming, front matter, section order,
  links, notation, and the content that must never appear are defined there.
- Run `git status --short --branch` and preserve unrelated user changes.
- Identify whether the requested information belongs here or in SALMON2,
  SALMON-DOCS, or SALMON-inputs.
- Confirm the source version, commit, platform, and verification evidence before
  describing observed behavior.

## Local working convention

- Perform per-user downloads, CIF conversions, temporary inputs, calculation
  runs, and raw outputs under `.local/<tutorial-directory-name>/` at the
  repository root, for example `.local/004-4h-sic-gs-from-cif-fhi/` (the same
  name as the tutorial directory). The repository ignores `/.local/`; do not
  stage its contents.
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
- Mark new tutorials `draft`. Keep substantively revised resources `draft`
  pending renewed human review; preserve prior review history in the text and
  do not present earlier reviewers as having reviewed the revision. An explicitly
  approved deprecation uses `deprecated` instead.
- When a tutorial becomes outdated, mark it `deprecated` and explain the replacement
  or changed behavior instead of deleting useful history.

## Scope boundaries

- Do not add a RAG service, vector database, indexing pipeline, CI workflow, or
  mailing-list ingestion unless a task explicitly requests it.
- Do not duplicate complete inputs from SALMON-inputs, formal documentation from
  SALMON-DOCS, or implementation documentation that belongs in SALMON2. A
  tutorial may include multiple small, representative inputs when necessary to
  reproduce its procedure, comparisons, or conclusion. Include only the needed
  cases; link to SALMON-inputs for published input collections.
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
- Add a troubleshooting entry only for an observed, reproducible symptom. Start
  from `templates/troubleshooting.md`; state the symptom, trigger, evidence,
  diagnosis, resolution, and applicability; do not turn a hypothesis into a
  documented fix. Keep the H1 equal to the front-matter title and list the
  entry in `troubleshooting/README.md`.
- Keep shared evidence and procedures in one resource and link from the other
  categories rather than duplicating content.

## Verification

- Check Markdown structure, internal links, learning-path links, the rules in
  `STYLE.md`, and the final Git diff.
- Verify cited repository paths, commits, versions, and commands when access is
  available.
- Report what was verified and clearly identify anything not verified.
- Do not commit or push changes unless the user explicitly requests it.
