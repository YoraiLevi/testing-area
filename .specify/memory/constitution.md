<!--
Sync Impact Report
==================
Version change: (unversioned template) -> 1.0.0
Bump rationale: Initial ratification of the project constitution (MAJOR baseline).

Modified principles:
  - [PRINCIPLE_1_NAME] -> I. CI-Only Verification (NON-NEGOTIABLE)
  - [PRINCIPLE_2_NAME] -> II. Evidence Over Popularity
  - [PRINCIPLE_3_NAME] -> III. Full Platform x Shell Matrix
  - [PRINCIPLE_4_NAME] -> IV. Deterministic, Minimal Demonstrations
  - [PRINCIPLE_5_NAME] -> V. Artifacts Are the Deliverable
  - (added)           -> VI. Exhaustive, Honest Landscape Coverage

Added sections:
  - Scope & Constraints (SECTION_2)
  - Evaluation Workflow (SECTION_3)

Removed sections: none (all template placeholders resolved)

Templates & runtime consumers reviewed:
  - .specify/templates/plan-template.md      : compatible (Constitution Check gate reads this file)
  - .specify/templates/spec-template.md      : compatible
  - .specify/templates/tasks-template.md     : compatible

Deferred TODOs: none
-->

# Terminal Recorder Trials Constitution

## Core Principles

### I. CI-Only Verification (NON-NEGOTIABLE)
Every tool trial MUST run exclusively inside CI/CD workflows; local execution is PROHIBITED
as a source of evidence.
A claim that a recorder "works" MUST be backed by a green CI job on the `testing-vhs` branch
that produced a downloadable artifact.
Rationale: local machines are non-reproducible and platform-biased; CI runners are the only
shared, auditable ground truth for a cross-platform tool survey.

### II. Evidence Over Popularity
A tool is classified "working" only when a CI run produces a valid, openable recording
(GIF, and optionally video/SVG) of the target program.
Stars, download counts, and issue totals MUST NOT influence the working/broken verdict; they
MAY only prioritize evaluation order.
Rationale: the goal is a truthful capability map, and popular tools frequently fail on one or
more platform/shell combinations.

### III. Full Platform x Shell Matrix
Each candidate MUST be evaluated across Windows, Linux, and macOS, and across the shells that
apply to it (bash, zsh, pwsh).
Any combination that is not attempted or not applicable MUST be recorded explicitly with a
reason; silently dropping a cell is PROHIBITED.
Rationale: partial coverage produces misleading conclusions; the value of this project is the
completeness of the per-tool, per-platform, per-shell grid.

### IV. Deterministic, Minimal Demonstrations
The canonical demonstration MUST be the simplest reproducible scenario: launch Oh My Pi (omp)
and close it cleanly.
Three or more additional creative examples MAY be added, but every demonstration MUST be
deterministic, pinned (fixed tool versions and inputs), and re-runnable to the same result.
Rationale: a recorder's fidelity can only be judged when the recorded content itself is stable
across runs.

### V. Artifacts Are the Deliverable
Recordings (GIF primary; video/SVG optional) and the comparison report with live CI status
badges are first-class outputs, not incidental logs.
The README MUST embed the produced GIFs/videos and the badges, and MUST link to the CI runs
that generated them.
Rationale: the audience consumes the result visually in Markdown and presentations; unpublished
artifacts have no value to that audience.

### VI. Exhaustive, Honest Landscape Coverage
The tool landscape MUST be surveyed beyond the initially supplied list; newly discovered
recorders MUST be added to the evaluation.
Tools that are abandoned, broken, or unavailable on a platform MUST be reported honestly with
the failure reason rather than omitted.
Rationale: an incomplete or flattering survey defeats the purpose of finding what actually
works.

## Scope & Constraints

- Branch scope: all work happens on `testing-vhs` only. No other branch is created or modified.
- Recorded subject: Oh My Pi (`omp`). The minimal scenario is start-then-clean-exit.
- Output formats: GIF is required for every working tool; video (MP4/WebM) and SVG are optional
  additions where the tool supports them.
- Two tool families are in scope:
  1. Scripted and deterministic demonstrations (e.g. VHS and relatives).
  2. Interactive terminal capture and replay (e.g. asciinema, terminalizer, script/scriptreplay).
- No local testing: contributors MUST NOT rely on their own machine to declare a tool working.

## Evaluation Workflow

- Each tool is exercised by a CI workflow (a dedicated workflow or a matrix job) that installs a
  pinned version, records the scenarios, and uploads the resulting artifacts.
- Workflows MUST use the OS/shell matrix required by Principle III and MUST fail loudly when a
  recording is not produced.
- Results feed a single comparison report: a per-tool, per-platform, per-shell status grid plus
  the embedded artifacts and CI badges in the README.
- A tool's verdict changes only in response to a CI run; documentation edits alone MUST NOT flip
  a working/broken status.

## Governance

This constitution supersedes ad hoc evaluation practices for this project. Amendments MUST be
recorded in this file with a version bump and an updated Sync Impact Report.

Versioning policy (semantic):
- MAJOR: removal or incompatible redefinition of a principle or governance rule.
- MINOR: a new principle or materially expanded section.
- PATCH: clarifications and wording fixes with no change in meaning.

Compliance: every change to workflows, artifacts, or the report MUST be checked against these
principles; a change that asserts a capability without a supporting CI run violates Principles I
and II and MUST be corrected before merge.

**Version**: 1.0.0 | **Ratified**: 2026-09-19 | **Last Amended**: 2026-09-19
