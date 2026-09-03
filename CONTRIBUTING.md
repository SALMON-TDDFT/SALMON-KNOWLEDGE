# Contributing to SALMON Knowledge

## Contribution workflow

1. Create a topic branch from the latest `main`.
2. Create `cases/<year>/<number>-<short-title>/README.md` from
   `templates/use-case.md`. Keep card-specific figures, representative inputs,
   and provenance under that directory.
3. Replace every placeholder. Use `unknown` when a fact cannot be established;
   do not infer a value merely to complete the template.
4. Check all technical claims against the recorded SALMON version or commit.
5. Remove confidential, personal, and machine-sensitive information.
6. Submit a pull request and request review from another SALMON developer.

Use a three-digit number within each year, for example:
`cases/2026/001-building-with-libxc.md`. Resolve number collisions during pull
request review. Keep the `id` in the front matter stable after merge, even if
the file is later renamed.

## Card status

- `draft`: incomplete or awaiting technical review;
- `reviewed`: reviewed by another developer and suitable for normal use;
- `deprecated`: no longer applicable; the card must explain why and link to a
  replacement when one exists.

Only a reviewer should change a card from `draft` to `reviewed`.

`status` describes editorial review, while `verification_level` describes the
strength of the technical evidence:

- `reported`: the result was recorded by the contributor but not independently
  checked;
- `reproduced`: the behavior was reproduced in a recorded environment;
- `code-reviewed`: the explanation was checked against the relevant source;
- `tested`: a build, test, or calculation explicitly verified the claim.

Choose the strongest level actually supported by the card. Do not treat a
developer's expectation as an observed result.

## Evidence and references

- Record a SALMON release version, Git commit, or both.
- Prefer links fixed to a commit or release over links to a moving branch.
- Link formal behavior to SALMON-DOCS and implementation details to SALMON2.
- Link reusable published inputs to SALMON-inputs instead of copying them.
- Distinguish general SALMON behavior from an observation made in one
  environment.
- Include only short, relevant excerpts of input or output. Do not commit large
  result files, complete build trees, or generated binary files.

## Use of AI tools

AI coding and writing tools may create a first draft, organize work logs, check
the template, or translate a contributor's text into English. They must not:

- invent missing versions, commands, results, citations, or explanations;
- present a hypothesis as a confirmed cause;
- silently generalize a result beyond its tested configuration;
- copy third-party text without an appropriate license and attribution;
- determine that a card is technically verified without human review.

The contributor must read the final diff and is accountable for its accuracy.

## Language

English is the primary language for cards and repository documentation. A
contributor may prepare a draft in another language and use an AI tool for
translation, but technical meaning, variable names, commands, and units must be
checked after translation. A second full-language copy is not required for the
pilot.

## Information that must not be committed

Do not include credentials, access tokens, private keys, personal contact
details, unpublished research results, restricted source code, confidential
input data, allocation or project identifiers, internal hostnames, or local
absolute paths that reveal private information. Treat copied terminal output
and scheduler scripts as potentially sensitive.

Although the pilot repository is private, write each card so that it could be
published later after an explicit review.

Mailing-list collection and automated conversion of messages are outside the
scope of the initial pilot.
