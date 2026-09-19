# Feature Specification: Terminal Recorder Trials

**Feature Branch**: `testing-vhs`

**Created**: 2026-09-19

**Status**: Draft

**Input**: User description: "Test a few terminal recorders. The output is a successful, as-simple-as-
possible, concise workflow CI/CD run that executes Oh My Pi (omp) and closes it (plus 3 more creative
examples), recorded into a GIF, optionally videos, for use in Markdown files and presentations. The
task is to analyze what is working and for which platform. Cover the landscape of 'scripted and
deterministic demonstrations' and 'interactive terminal capture and replay' without missing tools;
find tools that actually work, not just popular ones. Per tool, per Windows/Linux/macOS and per
bash/zsh/pwsh where applicable. Final output is a full breakdown report with CI/CD badges and output
GIFs/videos in the README."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Read the recorder capability report (Priority: P1)

A maintainer evaluating how to record terminal demos opens the project README and immediately sees,
for every terminal recorder tried, whether it works on each operating system and shell, backed by an
embedded GIF of `omp` starting and cleanly exiting and a live CI status badge that links to the run
that produced the artifact.

**Why this priority**: This is the deliverable. Without a readable, evidence-backed capability
report, the whole effort has produced nothing consumable. It is independently valuable even if only
one recorder is covered.

**Independent Test**: Open the README and confirm at least one tool shows a per-OS/per-shell status
grid, an embedded GIF that plays, and a badge that links to a passing CI run for that tool.

**Acceptance Scenarios**:

1. **Given** the README is published on `testing-vhs`, **When** a reader scans a tool's row,
   **Then** they see a working/broken/not-applicable verdict for each of Windows, Linux, and macOS
   and each applicable shell (bash, zsh, pwsh), each traceable to a CI run.
2. **Given** a tool is marked "working" for a platform, **When** the reader clicks its badge or run
   link, **Then** they reach the CI run whose uploaded artifact is the embedded recording.
3. **Given** a tool failed on a platform, **When** the reader reads that cell, **Then** a concrete
   reason is stated rather than the cell being omitted.

---

### User Story 2 - Prove a recorder in CI (Priority: P1)

For a given terminal recorder, a CI workflow installs a pinned version, records the minimal scenario
(launch `omp`, then close it), and uploads the resulting GIF as a build artifact, failing loudly if
no valid recording is produced.

**Why this priority**: CI runs are the only accepted evidence (constitution Principle I/II). This is
the engine that generates every artifact and every verdict the report depends on.

**Independent Test**: Trigger the workflow for one tool on one platform and confirm the run either
uploads an openable GIF artifact or fails visibly with the reason.

**Acceptance Scenarios**:

1. **Given** a recorder's workflow runs on a supported platform/shell, **When** it completes,
   **Then** a non-empty, openable GIF of the `omp` launch-and-close scenario is attached to the run.
2. **Given** a recorder cannot produce a recording on a platform, **When** its workflow runs,
   **Then** the job fails (or is skipped with a recorded reason) rather than reporting a false pass.
3. **Given** a workflow is re-run without code changes, **When** it completes again, **Then** it
   produces an equivalent recording of the same deterministic scenario.

---

### User Story 3 - Creative demonstration scenarios (Priority: P2)

Beyond the minimal launch-and-close, each viable recorder also captures at least three additional
creative scenarios that show more of a recorder's fidelity (for example: colored/styled output, a
multi-step interaction, and a longer session), each recorded to a GIF.

**Why this priority**: The minimal scenario proves the tool runs; the creative scenarios reveal
quality differences (color accuracy, timing, resizing, Unicode) that matter when choosing a tool for
presentations. Valuable but secondary to having any working recording at all.

**Independent Test**: For one working tool, confirm three additional distinct GIFs exist as CI
artifacts and are embedded in the report.

**Acceptance Scenarios**:

1. **Given** a recorder works for the minimal scenario on a platform, **When** its creative
   scenarios run, **Then** three additional distinct GIFs are produced and embedded.
2. **Given** a creative scenario exercises color or Unicode, **When** the recording is viewed,
   **Then** the report notes any fidelity issues observed (e.g. missing color, broken glyphs).

---

### User Story 4 - Complete, honest landscape (Priority: P2)

A reader can trust that the survey covers the terminal-recorder landscape broadly (both scripted and
interactive families), including tools discovered beyond the initial list, and that tools which are
abandoned, broken, or unavailable are reported with reasons instead of being silently dropped.

**Why this priority**: The stated goal is to find what actually works across the whole landscape; an
incomplete or flattering survey undermines the report's usefulness.

**Independent Test**: Confirm the report enumerates every candidate from both families, marks each as
evaluated/failed/not-applicable with a reason, and includes at least one tool discovered during
research beyond the provided list (or explicitly states none was found).

**Acceptance Scenarios**:

1. **Given** the report is complete, **When** a reader looks for a candidate tool, **Then** it
   appears with a status and, if not evaluated in CI, a stated reason.
2. **Given** a non-GIF-native tool (e.g. one producing a cast or typescript), **When** it is
   evaluated, **Then** the report documents the converter used to normalize its output to GIF.

---

### Edge Cases

- A recorder installs but produces a zero-byte or corrupt GIF: treated as a failure with the reason
  recorded, never as a pass.
- A shell is not available or not meaningful on a platform (e.g. zsh on a stock Windows runner):
  the cell is marked not-applicable with the reason, not left blank.
- A tool requires a GUI/display server and cannot run headless in CI: marked not-applicable for CI
  with the reason.
- `omp` cannot be launched interactively on a runner: a representative, deterministic `omp`
  invocation stands in as the recorded subject, and that substitution is documented.
- A tool's latest version breaks while a pinned older version works (or vice versa): the working
  version is pinned and the observation recorded.
- Recordings differ across runs due to timestamps/animation: scenarios are pinned to remove
  nondeterminism so re-runs are equivalent.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The evaluation MUST run exclusively in CI/CD workflows on the `testing-vhs` branch;
  no verdict may rest on local execution.
- **FR-002**: For each evaluated recorder, the system MUST record the minimal scenario of launching
  `omp` and closing it cleanly, and produce a GIF artifact of that scenario.
- **FR-003**: For each viable recorder, the system MUST additionally record at least three distinct
  creative scenarios, each producing its own GIF artifact.
- **FR-004**: Each recorder MUST be evaluated across Windows, Linux, and macOS, and across the
  shells applicable to it among bash, zsh, and pwsh.
- **FR-005**: Every platform/shell combination that is not attempted or not applicable MUST be
  recorded with an explicit reason; no combination may be silently omitted.
- **FR-006**: A recorder MUST be classified "working" for a platform/shell only when a CI run
  produced a non-empty, openable GIF; popularity metrics MUST NOT affect the verdict.
- **FR-007**: Workflows MUST fail loudly (or skip with a recorded reason) when no valid recording is
  produced, so passes are never false.
- **FR-008**: Recorder versions and scenario inputs MUST be pinned so re-runs produce equivalent
  recordings.
- **FR-009**: The survey MUST cover both the scripted/deterministic family and the interactive
  capture/replay family, including tools discovered beyond the initially provided list.
- **FR-010**: For tools whose native output is not a GIF (e.g. cast, typescript, SVG, video), the
  system MUST convert output to GIF and document the converter used.
- **FR-011**: The README MUST present a per-tool, per-OS, per-shell status grid, embed the produced
  GIFs, and display live CI status badges linking to the generating runs.
- **FR-012**: Video (e.g. MP4/WebM) outputs MAY be produced where a tool supports them, as optional
  additions to the required GIF.
- **FR-013**: Abandoned, broken, or unavailable tools MUST be reported with the failure reason
  rather than excluded.

### Key Entities *(include if feature involves data)*

- **Recorder Tool**: A terminal-recording program under evaluation; attributes include name, family
  (scripted vs interactive), pinned version, native output format(s), and required converter.
- **Trial**: A single CI evaluation of one tool on one OS and shell for one scenario; attributes
  include platform, shell, scenario, verdict (working/broken/not-applicable), reason, and produced
  artifact reference.
- **Scenario**: A deterministic recorded script; the minimal launch-and-close plus creative variants.
- **Artifact**: A produced recording (GIF required; video/SVG optional) with a link to its CI run.
- **Report**: The README-embedded synthesis — the status grid, badges, and embedded artifacts.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every candidate tool from both families appears in the report with a verdict for each
  of the three operating systems and each applicable shell (100% grid coverage, no blank cells).
- **SC-002**: At least one recorder is demonstrated end-to-end (minimal scenario) with a passing CI
  run and an embedded, playable GIF for at least one platform.
- **SC-003**: Every "working" verdict in the report links to a CI run whose uploaded artifact is the
  embedded recording (100% of positive verdicts are traceable to evidence).
- **SC-004**: Each viable recorder shows the minimal scenario plus at least three creative scenarios
  (four or more GIFs per viable tool).
- **SC-005**: The survey adds at least one tool discovered beyond the provided list, or explicitly
  states that research found no additional viable tools.
- **SC-006**: A reader can determine, in under one minute of scanning the README, which recorder to
  use for a given OS and shell.
- **SC-007**: Re-running any tool's workflow without changes yields an equivalent recording of the
  same scenario (deterministic output).

## Assumptions

- "Oh My Pi (omp)" refers to a command-line/TUI invocation available on the CI runner; where an
  interactive session cannot be driven headlessly, a representative deterministic `omp` invocation
  (e.g. a help/version or scripted prompt-and-exit) stands in and the substitution is documented.
- GitHub Actions is the CI/CD provider, providing Windows, Linux, and macOS runners.
- GIF is the required leveling artifact for cross-tool comparison; video and SVG are optional extras.
- Work is confined to the `testing-vhs` branch; no new branches are created (overrides the default
  Spec Kit feature-branch behavior, per the project constitution's Scope & Constraints).
- Shell applicability follows platform norms: bash/zsh on Linux/macOS, pwsh cross-platform, and the
  default Windows shell for Windows-native tools; non-applicable combinations are marked as such.
- Recorders that require an interactive GUI or a display server and cannot run headless are out of
  scope for CI evaluation and are reported as not-applicable with the reason.
