# Knowledge cards

This directory contains use-case cards created from actual SALMON development
or use.

Store cards under a directory for the year in which the card was created:

```text
cases/
└── 2026/
    └── 001-short-descriptive-title/
        └── README.md
```

Create a card directory and copy `templates/use-case.md` to its `README.md`.
The directory number and front-matter `id` must be unique. Use lowercase ASCII
words separated by hyphens in directory names. Supporting figures and one
representative input may be stored below the card directory. Keep a card's
`id` unchanged after merge.

Cards may be `draft`, `reviewed`, or `deprecated`, as defined in
`CONTRIBUTING.md`. New cards start as `draft`; another developer reviews the
technical claims before changing the status to `reviewed`.

Do not create placeholder or hypothetical cards simply to populate this
directory. Each card must be based on an actual calculation, implementation,
diagnosis, or validation activity.
