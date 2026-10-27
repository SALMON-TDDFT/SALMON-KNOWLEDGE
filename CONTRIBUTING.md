# Contributing to SALMON Knowledge

## Contribution workflow

Before creating a tutorial, FAQ, or troubleshooting entry, obtain the user's
explicit decision to add it. Use [the knowledge proposal
template](templates/knowledge-proposal.md) to present the topic, evidence,
alternatives, destination, and scope. Keep unapproved proposals in the
conversation or ignored `.local/<work-id>/` workspace, without a permanent
identifier or catalog entry. A calculation request does not grant admission
approval. The same gate applies to substantive changes to conclusions,
recommendations, applicability, and deprecation of existing items.

After admission approval:

1. Create a topic branch from the latest `main`.
2. Create `tutorials/<number>-<short-title>/README.md` from
   `templates/tutorial.md`. Keep tutorial-specific figures, representative inputs,
   and provenance under that directory. For a troubleshooting entry, create
   `troubleshooting/SALMON-TS-NNN-short-title.md` from
   `templates/troubleshooting.md`.
3. Replace every placeholder and follow [STYLE.md](STYLE.md) for naming, front
   matter, section order, links, and notation. Use `unknown` when a fact cannot
   be established; do not infer a value merely to complete the template.
4. Check all technical claims against the recorded SALMON version or commit.
5. Remove confidential, personal, and machine-sensitive information.
6. Submit a pull request and request review from another SALMON developer.

Use a globally unique three-digit number, for example:
`tutorials/001-building-with-libxc/`. The front-matter identifier is
`SALMON-TUTORIAL-001`. Resolve number collisions during pull-request review.
Keep the identifier stable after a tutorial is reviewed or published, even if
the directory is later renamed.

## Tutorial status

- `draft`: incomplete or awaiting technical review;
- `reviewed`: reviewed by another developer and suitable for normal use;
- `deprecated`: no longer applicable; the tutorial must explain why and link to a
  replacement when one exists.

Only a human reviewer may authorize a change from `draft` to `reviewed`.
The AI assistant may apply that change only on explicit instruction after human
review of the relevant revision. Record the reviewer and the review date and
scope in a review note or a linked review record; never fabricate them.
Admission approval is separate from scientific acceptance and final review.
These status rules also apply to troubleshooting and FAQ entries.

Substantive revisions return an item to `draft` pending renewed human review.
Preserve the previous review history in a note, and clear `reviewed_by` for the
new draft so it does not imply that earlier reviewers approved the revision.
Formatting-only changes and corrections to navigation links or learning-path
metadata that do not change technical meaning do not require a status change.
An explicitly approved deprecation uses `deprecated`, with the reason and
replacement recorded, rather than returning the item to `draft`.

`status` describes editorial review, while `verification_level` describes the
strength of the technical evidence:

- `reported`: the result was recorded by the contributor but not independently
  checked;
- `reproduced`: the behavior was reproduced in a recorded environment;
- `code-reviewed`: the explanation was checked against the relevant source;
- `tested`: a build, test, or calculation explicitly verified the claim.

Choose the strongest level actually supported by the tutorial. Do not treat a
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

## FAQ and troubleshooting entries

FAQ entries answer one concise, stable question and should link to the
authoritative source or a tutorial. Troubleshooting entries record a reproducible
symptom, its evidence, diagnosis, resolution, and applicability. Start them
from `templates/troubleshooting.md`, keep the H1 equal to the front-matter
title, and list each entry in `troubleshooting/README.md`. Do not repeat
the full procedure or evidence of a tutorial; link to it instead.

## Use of AI tools

AI coding and writing tools may create a first draft, organize work logs, check
the template, or translate a contributor's text into English within the
user-authorized scope. Scientific choices and interpretations are proposals
only; the user decides whether to adopt them. The assistant may apply approved
criteria and report measured comparisons, but must not choose new acceptance
criteria or adopt settings on the user's behalf. Record unaccepted proposals
as `provisional (AI assistant)` and unadopted; attribute an accepted decision to
the user only when explicit confirmation exists. They must not:

- invent missing versions, commands, results, citations, or explanations;
- present a hypothesis as a confirmed cause;
- silently generalize a result beyond its tested configuration;
- copy third-party text without an appropriate license and attribution;
- determine that a tutorial is technically verified without human review.

The contributor must read the final diff and is accountable for its accuracy.
Permission to add an item, acceptance of a scientific proposal, approval of a
reviewed revision, and permission to commit or push are separate decisions.

## Language

English is the primary language for tutorials and repository documentation. A
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

Although the pilot repository is private, write each tutorial so that it could be
published later after an explicit review.

Mailing-list collection and automated conversion of messages are outside the
scope of the initial pilot.
