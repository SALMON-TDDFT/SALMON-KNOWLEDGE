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

The pilot does not include mailing-list ingestion, a RAG implementation, a
vector database, automated indexing, or large collections of raw inputs and
outputs.

## Repository layout

```text
tutorials/              Curated, case-based learning path
faq/                    Short, evidence-backed questions and answers
troubleshooting/        Reproducible symptoms, diagnoses, and resolutions
templates/tutorial.md   Template for a new tutorial
AGENTS.md               Instructions for AI coding tools
CONTRIBUTING.md          Contribution and review rules
```

## Contributing

Create a branch, create a tutorial directory under `tutorials/`, and copy
`templates/tutorial.md` to its `README.md`. Add only small, relevant supporting
figures or one representative input when needed. Complete the tutorial using
evidence from actual work, and submit a pull request. AI tools may help
organize or translate the material, but the contributor remains responsible
for verifying every technical claim and removing sensitive information.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the complete pilot rules.

## License

This repository is licensed under the Apache License 2.0. See [LICENSE](LICENSE).
