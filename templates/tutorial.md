---
id: SALMON-TUTORIAL-NNN
title: Replace with a concise descriptive title
status: draft
verification_level: reported
learning_stage: unknown
prerequisites: []
next_tutorials: []
estimated_cost: unknown
topics: []
salmon_version: unknown
salmon_commit: unknown
platforms: []
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
contributors: []
reviewed_by: []
---

<!-- Follow STYLE.md at the repository root (naming, front matter, section
order, links, notation). Obtain user approval of the topic and scope using
knowledge-proposal.md before creating this resource. Delete this comment. -->

# Learning objective

State the skill or conclusion that this tutorial teaches.

# Summary

State the reusable conclusion in a few sentences. Distinguish an observation in
this tutorial from behavior that is documented or verified to be general.

## Context and objective

Describe what was being calculated, implemented, diagnosed, or evaluated and
why the tutorial may be useful to another SALMON developer or user.

## Conditions

- SALMON version or commit:
- Calculation mode and relevant input variables:
- Operating system and architecture:
- Compiler and version:
- MPI and process/thread configuration:
- Optional libraries and build options:
- Other relevant constraints:

Use `unknown` for information that cannot be confirmed.

## Procedure

Describe the essential reproducible steps. Include only short commands or input
excerpts that are necessary to understand the tutorial.

## Observed result

Record what actually happened, including the relevant output, error, numerical
behavior, or performance observation. Do not replace observations with an
expected result.

For a tutorial that records convergence, use the layout of STYLE.md
("Observed result of a convergence tutorial") with these subsections.

### Convergence by observable

One table: rows are the observables that were examined, columns are the varied
parameters, each cell is where the observable converged and one number (for
example `k24 (0.3 meV/atom)`), but only when this tutorial already holds that
judgment; quote it. Otherwise give the measured difference and write `not judged`
(never strengthen or extrapolate a verdict). Leave out what
was not examined. Add a short note on which observables converge early and
which late.

### Ladder: name of the varied parameter

Repeat for each ladder, in this order.

1. One figure: top, overlay for all rungs; bottom, difference between
   neighboring rungs.
2. One table: rows are neighbor pairs (`r16 to r20`); columns are the difference
   of each examined observable, then the difference of each rung to the densest
   rung where available. DOS and spectra as maximum difference in % of the peak,
   scalars as absolute differences, energies in meV/atom.
3. One judgment line: the pair where the change became small, the member taken,
   and who judged it (link to the Judgment record row if the tutorial has one;
   otherwise say the judge is not recorded). If no judgment exists, say so.

### Recommended settings by use

A table: use, setting, measure, evidence. The adopted point is one row.

## Judgment record

Required when the tutorial records convergence judgments or scientific
parameter choices; otherwise optional. Keep it directly after Observed result.
One table row per
decision: what was judged, the conclusion, who judged it (the maintainer, or
the AI assistant marked "provisional (AI assistant)" and unadopted until the
user explicitly accepts the proposal), what was
looked at, and the reason including rejected alternatives. A superseded
judgment stays in the table, marked as superseded. Record the date and a
traceable, non-sensitive reference to explicit user acceptance when available;
write `unknown` for unavailable details. Admission approval or a `reviewed`
label alone must not be used to infer acceptance of an individual proposal.

## Assumptions made by the assistant

Required when an AI assistant made assumptions; otherwise optional. List every
setting that was fixed and not varied, so that it is not mistaken for a
convergence result. Distinguish approved settings from unaccepted proposals;
do not execute a new scientific choice before user approval.

## Validation

Explain how the result or diagnosis was checked. Identify builds, tests,
comparisons, independent reproductions, or source-code inspection. Ensure that
the front-matter `verification_level` matches this evidence.

## Surprises and failures recorded

Optional; keep it directly after Validation. Record failed runs, misread
outputs, and unexpected behavior, each with what was learned from it.

## Lessons learned

Summarize the reusable guidance, including common mistakes or checks that can
shorten future development and diagnosis.

## Limitations and applicability

State which versions, platforms, calculation modes, or parameter ranges are
covered and which have not been tested.

## References

- SALMON2 source, commit, issue, pull request, sample, or testsuite:
- SALMON-DOCS page or commit:
- SALMON-inputs example or publication:
- Other evidence:
