# Basic calculation workflow

Use this workflow to reproduce a tutorial or begin a SALMON calculation with an
AI assistant. It defines operational steps; scientific choices and adoption of
interpretations belong to the user under [AGENTS.md](../AGENTS.md).

## 1. Establish the task and evidence

- Identify the requested observable and whether the task is reproduction,
  numerical exploration, or application to a new system.
- Read the relevant [learning path](../tutorials/README.md), prerequisites,
  conditions, validation, limitations, and judgment records. Consult linked
  troubleshooting entries before preparing inputs.
- Identify the SALMON version and commit, executable, platform, compiler,
  libraries, and MPI/OpenMP configuration where available. Record unconfirmed
  facts as `unknown`; never claim a version-specific reproduction without the
  evidence needed to establish it.
- Follow the source priority in AGENTS.md. Report conflicts rather than
  silently changing the procedure to match a different version.

## 2. Establish the authorized plan

Present the input sources, model and fixed settings, varied parameters and
ranges, observables, evaluation criteria, expected cost, and execution budget.
Identify which choices the user has already approved and which remain proposals.
For reproduction, distinguish retained tutorial choices from environment changes.

The user decides scientific choices, including functional, pseudopotentials,
convergence criteria, and which settings to adopt. Obtain decisions on unresolved
choices before executing dependent work. An explicit request to reproduce a
specific tutorial may authorize its stated settings and procedure; it does not
authorize transferring its judgments to another system or expanding its cost.
If cost is unknown, propose a bounded pilot before a large calculation.

## 3. Prepare and execute within scope

- Use ignored `.local/<tutorial-directory-name>/` for a tutorial reproduction,
  or `.local/<work-id>/` for work without an approved tutorial identifier.
  Keep raw inputs, downloads, outputs, and candidate notes there.
- Record input provenance, checksums when available, conversions, exact
  commands, and the executable identity. Keep non-sensitive local environment
  notes in ignored `LOCAL_ENV.md` when useful.
- Check units, structure, electron counts, restart compatibility, and parallel
  configuration against the approved inputs and version-specific evidence.
- Run the approved cases and collect exit status, completion markers, relevant
  residuals, warnings, and requested observables. Preserve failed cases as
  evidence; do not silently change scientific settings to make a run pass.
- Continue routine execution within the approved plan without repeated
  permission requests. If a new scientific choice or budget expansion is
  needed, propose it and wait for the user's decision on that part.

## 4. Compare and report

Separate these four parts in the result:

1. **Observations:** what ran, what failed, measured values, and evidence paths.
2. **Comparison with approved criteria:** numerical differences and which
   criteria passed, failed, or could not be evaluated.
3. **Interpretation proposals:** explanations, candidate settings, alternatives,
   and uncertainties, labeled `provisional (AI assistant)` and unadopted.
4. **User decisions needed:** the specific interpretation or setting to adopt,
   with evidence and limitations sufficient to assess the proposal.

Execution success and numerical checks alone do not establish physical validity,
convergence for every observable, or suitability for publication. Record the
user's explicit decisions without extending them beyond their approved scope.

## 5. Propose reusable knowledge separately

A calculation request does not authorize a repository addition. If a reusable
lesson emerges, prepare [a knowledge proposal](../templates/knowledge-proposal.md)
in the conversation or ignored workspace. Do not copy unpublished research or
restricted data into curated resources.

Only after the user approves the topic, destination, and scope, follow
[CONTRIBUTING.md](../CONTRIBUTING.md) to prepare a draft and its small,
reproducible supporting artifacts. Admission approval, scientific acceptance,
human review, and permission to commit or push remain separate decisions.
