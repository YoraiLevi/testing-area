# Implementation Plan: Terminal Recorder Trials

**Branch**: `testing-vhs` | **Date**: 2026-09-19 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/001-terminal-recorder-trials/spec.md`

## Summary

Build a CI-only, evidence-based evaluation of terminal-recording tools. Each tool gets a GitHub
Actions workflow that installs a pinned version, records four omp scenarios (minimal launch-and-exit
plus three creative variants) across the applicable Windows/Linux/macOS × bash/zsh/pwsh cells,
normalizes output to GIF, and publishes the GIFs plus a per-cell result record. A single report
generator assembles a per-tool × per-platform × per-shell status grid with live CI badges and
embedded GIFs into the README. Verdicts come only from green CI runs (constitution Principles I, II).

## Technical Context

**Language/Version**: GitHub Actions workflow YAML; POSIX shell + PowerShell glue; Python 3
(preinstalled on all GHA runners) for the report generator; tool-native DSLs (VHS/Foley/Betamax/EVP
`.tape`, Terminalizer YAML, console2svg `capture`, asciinema/PowerSession `.cast`).

**Primary Dependencies**: omp (subject, via `omp.sh` installer); recorders per research.md; converters
`agg` (v1.9.0), `ffmpeg`, `resvg`; GHA actions `actions/checkout`, `actions/upload-artifact`,
`charmbracelet/vhs-action@v2`, `arika0093/console2svg@main`.

**Storage**: Git repository (`testing-vhs` branch). GIFs committed under `assets/<tool>/`; per-cell
results under `results/<tool>/*.json`. No database.

**Testing**: CI-only. "Tests" here are the recorder workflows themselves — a green matrix cell that
uploads a non-empty, openable GIF is the passing assertion (Principle I). A tiny GIF validator
(magic-byte + non-zero size check) guards against false passes (FR-007).

**Target Platform**: GitHub-hosted runners `ubuntu-latest`, `macos-latest`, `windows-latest`.

**Project Type**: CI/CD evaluation harness + generated documentation (not an application).

**Performance Goals**: Each tool workflow completes within GHA defaults; scenarios are short (<~15s
recorded) to keep GIFs presentation-friendly and runs fast.

**Constraints**: All work on `testing-vhs` only (no new branches). No local execution as evidence.
Deterministic, pinned scenarios. GIF required per working cell; video/SVG optional.

**Scale/Scope**: ~11 evaluated tools × up to 3 OS × up to 3 shells × 4 scenarios, plus the skipped-
tool ledger. Practical matrix is pruned to applicable cells (see research.md).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Design compliance |
|-----------|-------------------|
| I. CI-Only Verification | Every verdict is produced by a GHA job on `testing-vhs`; no local runs. **PASS** |
| II. Evidence Over Popularity | Grid cells flip only on a green run that uploads a GIF; stars only order work. **PASS** |
| III. Full Platform × Shell Matrix | Per-tool matrix spans OS × shell; non-applicable cells recorded with a reason. **PASS** |
| IV. Deterministic, Minimal Demonstrations | Pinned tool + omp versions, fixed dimensions/typing speed, `--version`-based minimal scenario. **PASS** |
| V. Artifacts Are the Deliverable | GIFs committed to `assets/`; README embeds them with badges + run links. **PASS** |
| VI. Exhaustive, Honest Coverage | Both families covered; skipped/broken tools listed with reasons (research.md ledger). **PASS** |

Post-design re-check: no new violations introduced; no entries in Complexity Tracking.

## Project Structure

### Documentation (this feature)

```text
specs/001-terminal-recorder-trials/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   ├── scenarios.md         # The 4 omp scenarios (tool-agnostic spec)
│   ├── workflow-contract.md # Required shape of every rec-<tool>.yml
│   └── result.schema.json   # Per-cell result JSON schema
└── tasks.md             # Phase 2 output (/speckit-tasks)
```

### Source Code (repository root)

```text
.github/workflows/
├── rec-vhs.yml            # one workflow per evaluated tool
├── rec-foley.yml
├── rec-betamax.yml
├── rec-evp.yml
├── rec-console2svg.yml
├── rec-demotape.yml
├── rec-asciinema.yml
├── rec-powersession.yml
├── rec-terminalizer.yml
├── rec-acast.yml
├── rec-termsvg.yml
└── report.yml             # sole README writer: assembles grid + badges + GIFs

scenarios/                 # shared, deterministic scenario sources
├── vhs/                   # .tape files (VHS/Foley/Betamax/EVP compatible)
│   ├── 01-launch-exit.tape
│   ├── 02-help-tour.tape
│   ├── 03-tui-splash.tape
│   └── 04-typing-demo.tape
├── console2svg/           # capture command specs
├── asciinema/             # -c command specs / expect wrappers
└── shared/                # omp install + scenario shell scripts (bash + pwsh)
    ├── install-omp.sh
    ├── install-omp.ps1
    └── scenario-cmds.md

scripts/
├── build_report.py        # results/** + assets/** -> README section
├── validate_gif.py        # magic-byte + non-zero size guard
└── commit-artifacts.sh    # pull-rebase-push retry loop for asset/result commits

assets/<tool>/<os>-<shell>-<scenario>.gif   # committed recordings (deliverable)
results/<tool>/<os>-<shell>-<scenario>.json # per-cell verdict records
README.md                                    # report: grid + badges + embedded GIFs
```

**Structure Decision**: One workflow per tool (clear badge per tool, isolated failures), a shared
scenario library so every tool records the same four omp scenarios, a single Python report generator
as the only README writer (no merge race), and per-tool asset/result paths so concurrent workflows
never collide. This directly realizes the spec's report (US1), CI proof engine (US2), creative
scenarios (US3), and honest coverage (US4).

## Complexity Tracking

> No constitution violations; table intentionally empty.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| (none)    | —          | —                                    |
