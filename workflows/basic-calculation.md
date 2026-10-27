# Basic calculation workflow

Use this workflow to reproduce a tutorial or begin a SALMON calculation with an
AI assistant. It defines operational steps; scientific choices and adoption of
interpretations belong to the user under [AGENTS.md](../AGENTS.md).

For a beginner, the first milestone is one official Si ground-state (GS) run
from [tutorial 001](../tutorials/001-si-hhg-official-exercise-reproduction/),
followed by inspection of its output. Do not start real-time (RT) propagation,
convergence ladders, or a new material as part of that first task.

## Environment and installation route

Ask which operating system and architecture will run SALMON, whether it is a
local machine or a scheduled computing resource, and whether a usable SALMON
installation already exists. The assistant should inspect what it can before
asking the user for missing facts.

| Situation | Next action |
|---|---|
| SALMON is installed | Establish the executable's version/build provenance, compatible MPI launcher, and available processes/threads. Proceed to the sample plan. |
| SALMON is absent on a local machine | Consult the official installation instructions for the selected version. Identify compilers, numerical libraries, build tools, MPI needs, and a proposed installation location before making environment changes. |
| SALMON is absent or unknown on a shared system | Check the site's documented software/module and scheduler instructions or ask its support staff. Do not invent module names or run compute work on a login node. |
| The platform or version differs from the recorded example | Explain the difference and propose the execution plan. Report it as a new environment check, without claiming the recorded environment was reproduced. |

Use [SALMON-DOCS Install and Run at the recorded documentation commit](https://github.com/SALMON-TDDFT/SALMON-DOCS/blob/e4d97e0328a559f5f99c706260d9c63763be0dee/source/install_and_run.rst)
and [SALMON2 build files at the sample commit](https://github.com/SALMON-TDDFT/SALMON2/tree/30ba64694ec761cdb6288f01a75b8bcabf05721f).
Check the selected SALMON version's source configuration against the guide;
do not silently apply instructions from a different release. This route is a
handoff to formal installation documentation, not a verified cross-platform
build recipe. Keep per-user downloads and builds under ignored `.local/`.

Commands such as `command -v salmon` and `command -v mpiexec` can locate tools
on `PATH`; their presence alone does not prove the version, MPI compatibility,
or working execution. A missing build commit remains `unknown`.

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

For the first GS task, no numerical acceptance tolerance has been selected.
Report completion markers, the exit status, required restart data, warnings,
and whether the inspected numerical quantities are finite. Report the final
SCF residual, energy, gap, electron count where available, and differences
from the tutorial's historical observations. Mark numerical agreement as
`not judged (no user-approved tolerance)`; do not convert a small difference
into a pass. The sample's existing SCF `threshold` is an input setting, not a
newly approved tolerance for agreement between runs.

## 5. Propose reusable knowledge separately

A calculation request does not authorize a repository addition. If a reusable
lesson emerges, prepare [a knowledge proposal](../templates/knowledge-proposal.md)
in the conversation or ignored workspace. Do not copy unpublished research or
restricted data into curated resources.

Only after the user approves the topic, destination, and scope, follow
[CONTRIBUTING.md](../CONTRIBUTING.md) to prepare a draft and its small,
reproducible supporting artifacts. Admission approval, scientific acceptance,
human review, and permission to commit or push remain separate decisions.

## Short glossary

| Term | Meaning in this workflow |
|---|---|
| GS / DFT | Ground-state calculation: obtain a self-consistent electronic state for the fixed input system. |
| SCF | Self-consistent field iteration used in the GS calculation. Its convergence marker concerns that iteration, not convergence of all physical observables. |
| RT / TDDFT | Real-time propagation of electronic states, for example under a prescribed pulse. It follows the GS milestone. |
| HHG | High-harmonic generation; interpreting a calculated response requires further analysis and validation. |
| Pseudopotential | Element-specific input describing the effective ionic potential used for valence electrons. Preserve the sample's file for reproduction. |
| Real-space grid | Spatial discretization controlled here by `num_rgrid`; changing it is a separate numerical study. |
| k mesh | Sampling of crystal momentum controlled here by `num_kgrid`; it is distinct from the real-space grid. |
| MPI / OpenMP | Process and thread parallelism. Their layout must match the executable, launcher, and allocated resources. |
| Restart data | Saved computational state used to continue or initialize a compatible calculation. It is not interchangeable between arbitrary inputs. |
