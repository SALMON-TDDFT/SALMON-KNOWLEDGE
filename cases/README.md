# Knowledge cards

This directory contains use-case cards created from actual SALMON development
or use.

Store cards under a directory for the year in which the card was created:

```text
cases/
└── 2026/
    └── 001-short-descriptive-title.md
```

Create a card by copying `templates/use-case.md`. The file number and the
front-matter `id` must be unique. Use lowercase ASCII words separated by hyphens
in file names. Keep a card's `id` unchanged after merge.

Cards may be `draft`, `reviewed`, or `deprecated`, as defined in
`CONTRIBUTING.md`. New cards start as `draft`; another developer reviews the
technical claims before changing the status to `reviewed`.

Do not create placeholder or hypothetical cards simply to populate this
directory. Each card must be based on an actual calculation, implementation,
diagnosis, or validation activity.
