---
id: SALMON-CASE-YYYY-NNN
title: Replace with a concise descriptive title
status: draft
verification_level: reported
topics: []
salmon_version: unknown
salmon_commit: unknown
platforms: []
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
contributors: []
reviewed_by: []
---

# Summary

State the reusable conclusion in a few sentences. Distinguish an observation in
this case from behavior that is documented or verified to be general.

## Context and objective

Describe what was being calculated, implemented, diagnosed, or evaluated and
why the case may be useful to another SALMON developer or user.

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
excerpts that are necessary to understand the case.

## Observed result

Record what actually happened, including the relevant output, error, numerical
behavior, or performance observation. Do not replace observations with an
expected result.

## Validation

Explain how the result or diagnosis was checked. Identify builds, tests,
comparisons, independent reproductions, or source-code inspection. Ensure that
the front-matter `verification_level` matches this evidence.

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
