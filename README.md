# SALMON Knowledge

SALMON Knowledge is a curated collection of practical knowledge for developing
and using [SALMON](https://salmon-tddft.jp/). Its primary entry point is a
curated, case-based learning path for SALMON calculations. It also records
concise answers, troubleshooting lessons, and implementation context that do
not naturally belong in the source code, the formal manuals, or the
published-input database.

This repository is initially a small, private pilot. Its Markdown files are
written so that developers can read and review them directly and so that they
can later serve as a source for retrieval-augmented generation (RAG).

## Relationship to other SALMON repositories

- [SALMON2](https://github.com/SALMON-TDDFT/SALMON2) is the authoritative source
  for implementation, tests, build configuration, and coding rules.
- [SALMON-DOCS](https://github.com/SALMON-TDDFT/SALMON-DOCS) is the authoritative
  source for the public user and developer documentation.
- [SALMON-inputs](https://github.com/SALMON-TDDFT/SALMON-inputs) contains input
  files associated with published work.
- SALMON Knowledge contains reviewed experience and context derived from actual
  development and use.

A tutorial, FAQ entry, or troubleshooting note is not a replacement for source code, tests, or formal
documentation. If a resource conflicts with the relevant version of SALMON2 or
SALMON-DOCS, those repositories take precedence. Stable knowledge that becomes
part of the supported interface should be promoted to the appropriate formal
repository, with the original resource updated or deprecated.

## Initial scope

The pilot accepts Markdown tutorials describing:

- a calculation or development objective;
- the relevant SALMON version or commit and execution environment;
- the procedure and observed result;
- how the result was validated;
- reusable lessons, limitations, and links to supporting evidence.

It also accepts troubleshooting entries under `troubleshooting/`, each
recording one reproducible symptom with its trigger, evidence, diagnosis,
resolution, and applicability, and short FAQ entries under `faq/`.

The pilot does not include mailing-list ingestion, a RAG implementation, a
vector database, automated indexing, or large collections of raw inputs and
outputs.

## Repository layout

```text
tutorials/              Curated, case-based learning path
faq/                    Short, evidence-backed questions and answers
troubleshooting/        Reproducible symptoms, diagnoses, and resolutions
templates/tutorial.md   Template for a new tutorial
templates/troubleshooting.md
                        Template for a new troubleshooting entry
STYLE.md                Naming, front matter, section, link, and notation rules
AGENTS.md               Instructions for AI coding tools
CONTRIBUTING.md         Contribution and review rules
workflows/              Shared calculation and reporting procedures
templates/knowledge-proposal.md
                        Proposal for user approval before adding knowledge
```

## Start a calculation with an AI assistant

Read this README, [AGENTS.md](AGENTS.md), and
[CONTRIBUTING.md](CONTRIBUTING.md), then follow
[the basic calculation workflow](workflows/basic-calculation.md) and choose a
relevant resource from [the learning paths](tutorials/README.md).
Read [STYLE.md](STYLE.md) before drafting or editing knowledge resources.

For a first calculation, start with **the official silicon ground state only**
in [tutorial 001](tutorials/001-si-hhg-official-exercise-reproduction/).
The maintainer reviewed the revised beginner procedure on 2026-10-27.
The first goal is to run one fixed sample, inspect its completion and main
outputs, and report numerical differences without an acceptance tolerance.
Real-time propagation and HHG are a later, separately authorized step.

If SALMON is not installed, first follow the
[environment and installation route](workflows/basic-calculation.md#environment-and-installation-route).
This repository links to the official build instructions; it does not promise
a working build on every platform. A command-line environment, access to the
sample sources, and an executable with a compatible launcher are needed.

Example request to an AI assistant:

```text
Read README.md, AGENTS.md, and workflows/basic-calculation.md in this repository.
Help me start with the official silicon GS sample in tutorial 001, without
changing its scientific settings. Check my environment and propose the
commands, MPI/thread layout, and execution budget before running anything.
If SALMON is missing, guide me through the official installation instructions.
Report completion checks and measured differences; do not choose numerical
acceptance tolerances or declare scientific validity. Stop after the GS report.
Do not add knowledge items, commit, or push without a separate instruction.
```

The assistant should explain unfamiliar terms using the
[short glossary](workflows/basic-calculation.md#short-glossary) and distinguish
questions about the user's machine from scientific decisions.

The assistant may execute a user-approved plan and report evidence. Scientific
choices and interpretations remain proposals until the user adopts them.
Tutorial settings are examples within their recorded conditions, not automatic
approval for a new research calculation. The user also decides whether a
finding should become a repository item; running a calculation does not grant
that permission.

## Contributing

After the user approves an item's topic and scope, create a branch, create a
tutorial directory under `tutorials/`, and copy
`templates/tutorial.md` to its `README.md`; for a troubleshooting entry, copy
`templates/troubleshooting.md` to `troubleshooting/SALMON-TS-NNN-short-title.md`.
Follow [STYLE.md](STYLE.md). Add only small, relevant supporting
figures and the small representative inputs needed to reproduce its procedure
or comparisons. Complete the tutorial using
evidence from actual work, and submit a pull request. AI tools may help
organize or translate the material, but the contributor remains responsible
for verifying every technical claim and removing sensitive information.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the complete pilot rules.

## License

This repository is licensed under the Apache License 2.0. See [LICENSE](LICENSE).
