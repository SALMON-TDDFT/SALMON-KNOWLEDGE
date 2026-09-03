# AGENTS.md

This file defines repository-wide instructions for AI coding and writing tools
working in SALMON Knowledge.

## Purpose

Maintain a small, reviewable collection of evidence-backed Markdown knowledge
cards about SALMON development and use. Optimize for technical accuracy,
traceability, and future retrieval rather than document volume.

## Before making changes

- Read `README.md`, `CONTRIBUTING.md`, and the relevant template and cards.
- Run `git status --short --branch` and preserve unrelated user changes.
- Identify whether the requested information belongs here or in SALMON2,
  SALMON-DOCS, or SALMON-inputs.
- Confirm the source version, commit, platform, and verification evidence before
  describing observed behavior.

## Source priority

For behavior tied to a particular version, use the following priority:

1. SALMON2 source code and tests at the referenced commit;
2. the corresponding version of SALMON-DOCS;
3. published examples in SALMON-inputs;
4. reviewed cards in this repository;
5. unreviewed notes or recollection.

Do not resolve a conflict by silently choosing the most convenient source.
State the conflict and narrow the claim to what the evidence supports.

## Creating and editing cards

- Start from `templates/use-case.md` and keep its required front matter. Each
  card is a directory under `cases/<year>/`; its `README.md` is the card body.
  Supporting figures, representative inputs, provenance manifests, and small
  regeneration scripts belong in subdirectories of that card.
- Create one card for one reusable case or conclusion. Split unrelated findings.
- Use `unknown` for facts that cannot be confirmed. Never fabricate a complete
  value for the sake of presentation.
- Separate observations, interpretations, and verified conclusions.
- Preserve exact SALMON input-variable names, commands, units, and error text.
- Prefer concise summaries and stable source links over copied logs or source.
- Mark new cards `draft`. Do not set `reviewed` without human review.
- When a card becomes outdated, mark it `deprecated` and explain the replacement
  or changed behavior instead of deleting useful history.

## Scope boundaries

- Do not add a RAG service, vector database, indexing pipeline, CI workflow, or
  mailing-list ingestion unless a task explicitly requests it.
- Do not duplicate complete inputs from SALMON-inputs, formal documentation from
  SALMON-DOCS, or implementation documentation that belongs in SALMON2. A
  card may include one small, representative input when it is necessary to
  reproduce the card's conclusion; link to SALMON-inputs for published input
  collections and avoid copying multiple variants.
- Do not add large calculation outputs, build directories, binary artifacts, or
  generated caches.
- Small derived figures that support a card are allowed under that card's
  `figures/` directory. Do not commit raw output files or temporary caches.
- Do not include credentials, personal data, unpublished research, restricted
  data, allocation identifiers, or sensitive machine details.

## Verification

- Check Markdown structure, internal links, and the final Git diff.
- Verify cited repository paths, commits, versions, and commands when access is
  available.
- Report what was verified and clearly identify anything not verified.
- Do not commit or push changes unless the user explicitly requests it.
