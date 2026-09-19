---
description: "Task list for Terminal Recorder Trials"
---

# Tasks: Terminal Recorder Trials

**Input**: Design documents from `specs/001-terminal-recorder-trials/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: This is a CI-only evaluation harness. The "tests" are the recorder workflows plus a GIF
validator (FR-007). No unit-test suite is requested; a throwaway smoke check per the constitution
is a green CI cell.

**Branch**: all work on `testing-vhs` (no new branches).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: US1 report · US2 CI proof engine · US3 creative scenarios · US4 honest landscape

## Path Conventions

Repository root: `.github/workflows/`, `scenarios/`, `scripts/`, `assets/`, `results/`, `README.md`.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Repo skeleton and shared glue every tool workflow reuses.

- [X] T001 Create directory skeleton: `scenarios/{vhs,console2svg,asciinema,shared}/`, `scripts/`, `assets/.gitkeep`, `results/.gitkeep`
- [X] T002 [P] Write `scenarios/shared/install-omp.sh` (curl `https://omp.sh/install`, add install dir to PATH, assert `omp --version`)
- [X] T003 [P] Write `scenarios/shared/install-omp.ps1` (irm `https://omp.sh/install.ps1`, ensure PATH, assert `omp --version`)
- [X] T004 [P] Write `scripts/validate_gif.py` (fail on missing/zero-byte/non-`GIF8` magic; usable as `python scripts/validate_gif.py <glob>`)
- [X] T005 [P] Write `scripts/commit-artifacts.sh` (bot identity, stage `assets/ results/`, commit `[skip ci]`, `git pull --rebase` + push retry loop)
- [X] T006 [P] Copy `contracts/result.schema.json` to `scripts/result.schema.json` and add `scripts/emit_result.py` (writes/validates one trial record)
- [X] T007 [P] Add `README.md` report markers `<!-- REPORT:START -->` / `<!-- REPORT:END -->` and a static intro/heading

**Checkpoint**: shared install + validation + commit + result helpers exist.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: The shared scenario library and a proven end-to-end pipeline. BLOCKS all tool workflows.

**⚠️ CRITICAL**: No per-tool workflow can be trusted until the reference pipeline is green.

- [X] T008 [P] Author `scenarios/vhs/01-launch-exit.tape` (VHS/Foley/Betamax/EVP-compatible: `omp --version`, clean exit; 100x24, fixed font/typing)
- [X] T009 [P] Author `scenarios/console2svg/cmds.md` + capture spec (`console2svg capture --timeout N -- omp --version`, etc.)
- [X] T010 [P] Author `scenarios/asciinema/cmds.md` (`asciinema rec -c '<scenario cmd>'` + `agg` invocation per scenario)
- [X] T011 Write reference workflow `.github/workflows/rec-vhs.yml` per `contracts/workflow-contract.md` (matrix ubuntu-bash first; record job + collect job)
- [X] T012 Push to `testing-vhs`; confirm `rec-vhs` green on ubuntu-bash and `assets/vhs/linux-bash-launch-exit.gif` committed (SC-002 proof)

**Checkpoint**: pipeline proven — install omp → record → validate GIF → commit artifact + result.

---

## Phase 3: User Story 1 - Read the recorder capability report (Priority: P1) 🎯 MVP

**Goal**: A README grid with per-tool/per-OS/per-shell verdicts, badges, embedded GIFs, run links.

**Independent Test**: With only `rec-vhs` results present, the README renders a grid row for VHS with
a working cell linking to its run and an embedded GIF.

- [X] T013 [US1] Write `scripts/build_report.py`: read `results/**/*.json` + `assets/**`, emit the tool×cell grid (verdict glyph + run link + reason) between README markers
- [X] T014 [US1] Extend `build_report.py` to render per-tool workflow badges (`…/actions/workflows/rec-<tool>.yml/badge.svg`) and embed the 4 scenario GIFs per working tool
- [X] T015 [US1] Add tool metadata table `scripts/tools.yml` (id, name, family, pinned_version, applicable cells, skip reasons) consumed by `build_report.py`
- [X] T016 [US1] Write `.github/workflows/report.yml` (workflow_dispatch + `workflow_run` on rec-* completion): run `build_report.py`, commit README via `commit-artifacts.sh` (sole README writer)
- [X] T017 [US1] Run `report.yml`; confirm README grid shows the VHS row with badge, verdict, run link, embedded GIF

**Checkpoint**: MVP — the report exists and is evidence-linked for at least one tool.

---

## Phase 4: User Story 2 - Prove a recorder in CI (Priority: P1)

**Goal**: Each evaluated tool has a workflow that installs it pinned, records the minimal scenario
across applicable cells, validates the GIF, and emits results. (Scenario sources shared from Phase 2;
creative scenarios added in US3.)

**Independent Test**: Trigger any one tool workflow; a cell yields a validated GIF + `working` record
or a loud failure with a reason.

Each tool = one workflow file, independent and parallelizable. Applicable cells per research.md.

- [X] T018 [P] [US2] `rec-console2svg.yml` — cells: linux/macos/windows × {bash,zsh,pwsh applicable}; `console2svg capture` + ffmpeg→GIF (already partially covered by T011 pattern)
- [X] T019 [P] [US2] `rec-foley.yml` — cells: linux,macos × {bash,zsh}; install via brew/tarball; native GIF; windows→not-applicable record
- [X] T020 [P] [US2] `rec-betamax.yml` — cells: linux,macos × {bash,zsh}; cargo-binstall/brew; native GIF; windows→not-applicable
- [X] T021 [P] [US2] `rec-evp.yml` — cells: linux × {bash}; repo `action.yml`; native GIF/SVG; others→not-applicable (WIP note)
- [X] T022 [P] [US2] `rec-demotape.yml` — cells: linux,macos × {bash,zsh}; gem install + ttyd/ffmpeg; GIF
- [X] T023 [P] [US2] `rec-asciinema.yml` — cells: linux,macos × {bash,zsh,pwsh}; `asciinema rec -c` + agg→GIF; windows→not-applicable
- [X] T024 [P] [US2] `rec-powersession.yml` — cells: windows × {pwsh}; winget/scoop + agg.exe→GIF; unix→not-applicable
- [X] T025 [P] [US2] `rec-terminalizer.yml` — cells: linux × {bash} (xvfb for Electron render); YAML→render→GIF; note heavy deps
- [X] T026 [P] [US2] `rec-acast.yml` — cells: linux,macos,windows × applicable shells; acast record/convert-to-gif (agg)
- [X] T027 [P] [US2] `rec-termsvg.yml` — cells: linux,macos × {bash,zsh}; termsvg rec→export SVG→GIF; windows rec unsupported→not-applicable
- [X] T028 [US2] Push all tool workflows to `testing-vhs`; triage each run; record actual verdicts (green→working, red→broken with reason) — evidence gathering, not forcing green

**Checkpoint**: every tool has a run; the grid fills with real, evidence-backed verdicts.

---

## Phase 5: User Story 3 - Creative demonstration scenarios (Priority: P2)

**Goal**: Beyond launch-exit, every viable tool records the three creative scenarios (SC-004).

**Independent Test**: A working tool shows four distinct GIFs (minimal + 3 creative) embedded.

- [X] T029 [P] [US3] Author `scenarios/vhs/02-help-tour.tape`, `03-tui-splash.tape`, `04-typing-demo.tape` per `contracts/scenarios.md`
- [X] T030 [P] [US3] Add the 3 creative capture specs to `scenarios/console2svg/cmds.md` and `scenarios/asciinema/cmds.md`
- [X] T031 [US3] Update every `rec-<tool>.yml` to loop all four scenarios (matrix `scenario` axis or per-scenario steps); emit a result + GIF per scenario
- [X] T032 [US3] Re-run tool workflows; confirm working tools produce 4 GIFs each; note fidelity issues (color/Unicode) in result `reason`/`extra`

**Checkpoint**: creative scenarios captured; fidelity differences observable in the report.

---

## Phase 6: User Story 4 - Complete, honest landscape (Priority: P2)

**Goal**: Every candidate appears with a verdict or a stated skip reason; discovered tools included.

**Independent Test**: The README ledger lists all candidates and skipped tools with reasons; at least
one discovered-beyond-list tool is included (SC-005).

- [X] T033 [US4] Encode the skip ledger (research.md) into `scripts/tools.yml` (`skipped:` entries with reasons: s-vhs, ttysvg, TermRecord, terminal-recorder, tty-record, ovh-ttyrec, script, t-rec, ttygif, freeze, termshot, termtosvg, svg-term-cli, asciicast2gif, menyoki, Peek, asciinema-windows, termgif)
- [X] T034 [US4] Ensure each tool workflow's `collect` job emits `not-applicable` result records for its declared skip cells with reasons (Principle III, FR-005)
- [X] T035 [US4] Extend `build_report.py` to render a "Skipped / not evaluated" ledger section and mark discovered-beyond-list tools (console2svg, EVP, agg, termsvg, acast)
- [X] T036 [US4] Regenerate report; confirm no blank grid cells (SC-001) and the ledger is complete

**Checkpoint**: coverage is exhaustive and honest.

---

## Phase 7: Polish & Cross-Cutting Concerns

- [X] T037 [P] Add the final full breakdown write-up section to README (families overview mermaid, platform×shell reality, recommendation per OS/shell)
- [X] T038 [P] Verify determinism note per tool (record tool + omp versions in `extra`); spot-confirm re-run equivalence (SC-007) via one re-dispatch
- [X] T039 De-duplicate common workflow steps into `scenarios/shared/` and a composite action if repetition is heavy; keep one badge per tool
- [X] T040 Final `report.yml` run; validate all SC-001..SC-007 against the rendered README

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (P1)**: no deps.
- **Foundational (P2)**: needs Setup; BLOCKS all user stories (proves the pipeline).
- **US1 report (P3)**: needs Foundational; consumes results (works with just VHS results).
- **US2 CI proof (P4)**: needs Foundational; the 11 tool workflows are mutually independent [P].
- **US3 creative (P5)**: extends US2 workflows + scenario sources.
- **US4 landscape (P6)**: needs US1 report generator + US2 results.
- **Polish (P7)**: last.

### Parallel Opportunities

- Setup T002–T007 all [P].
- Foundational scenario authoring T008–T010 [P].
- US2 tool workflows T018–T027 all [P] (distinct files) — the main fan-out.
- US3 scenario sources T029–T030 [P].

---

## Implementation Strategy

### MVP First

1. Phase 1 Setup → Phase 2 Foundational (VHS pipeline green on ubuntu-bash, SC-002).
2. Phase 3 US1 → README grid renders VHS with badge + GIF + run link. **MVP shippable.**

### Incremental Delivery

1. Foundation + US1 = evidence-linked report for one tool.
2. US2 fans out all tools in parallel → grid fills with real verdicts.
3. US3 adds the 3 creative GIFs per working tool.
4. US4 completes the honest ledger; Polish adds the written breakdown + recommendations.

### Parallel Team Strategy (subagents)

After Foundational is green, dispatch tool workflows in waves of ≤4 subagents (T018–T027),
grouped by family/platform. Each subagent owns one `rec-<tool>.yml`, coordinates only through the
shared `scenarios/` (read-only) and never edits README (report generator owns it).

---

## Notes

- Verdicts come ONLY from CI runs (Principles I, II). Do not hand-edit a `working` verdict.
- A red cell is a valid, informative result — record the reason; do not force green.
- Commit assets/results via `commit-artifacts.sh`; README only via `report.yml`.
