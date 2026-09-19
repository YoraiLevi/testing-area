# Phase 0 Research: Terminal Recorder Trials

Survey date: 2026-09-19. Source: read-only landscape scout (web + GitHub API) plus omp packaging
docs. Full raw report retained at `agent://RecorderLandscape` at generation time; the decisions
below are the distilled, load-bearing conclusions.

Per the project constitution (Principles I and II), nothing here is a verdict. Every "works" claim
is a *hypothesis* to be proven by a green CI job on `testing-vhs` that uploads a GIF artifact.

## Decision: Recorded subject (omp invocation)

- **Decision**: Install omp in CI and record real omp invocations. Minimal scenario uses
  `omp --version` (deterministic, no auth, clean exit). Creative scenarios add `omp --help`
  (color/scrollback fidelity) and the interactive TUI splash launched then quit.
- **Rationale**: `omp --version`/`--help` run without provider credentials and exit deterministically,
  satisfying Principle IV. The TUI splash (even the onboarding screen shown without keys) is a
  legitimate "launch and close" recording and reveals interactive-capture quality.
- **Install method** (from omp docs + official README):
  - Linux/macOS: `curl -fsSL https://omp.sh/install | sh`
  - Windows: `irm https://omp.sh/install.ps1 | iex`
  - Alt: `bun install -g @oh-my-pi/pi-coding-agent` (Bun >= 1.3.14)
- **Alternatives considered**: `omp -p "..."` (rejected: needs API keys, non-deterministic output);
  driving a full authenticated session (rejected: non-deterministic, secret-dependent, slow).

## Decision: GIF is the leveling artifact; converters normalize the rest

- **Decision**: GIF is required for every "working" verdict. Tools whose native output is
  `.cast`/`.ttyrec`/SVG/video are normalized to GIF with a documented converter.
- **Converter matrix**:
  - `.cast` (v1/v2/v3) -> **agg** v1.9.0 (Linux/macOS/Windows binaries). Official successor to the
    archived `asciicast2gif`.
  - SVG (animated) -> ffmpeg/resvg, or `console2svg convert`.
  - MP4/WebM -> `ffmpeg -i in.mp4 out.gif` (palettegen).
  - `.tape` (VHS/Foley/Betamax/EVP) -> native GIF, no converter.
  - `ttyrec` -> ttygif needs X11 (**fails headless**); no good headless GIF path.
  - util-linux `typescript` -> no practical headless GIF path.
- **Rationale**: A uniform artifact makes the cross-tool grid comparable (Principle V). agg is the
  maintained, cross-platform, no-browser converter.
- **Alternatives rejected**: asciicast2gif (archived 2022, PhantomJS), gifcast (browser-only, no CLI).

## Decision: Tool eval set

Selected for CI plausibility and a GIF path. Each row is a hypothesis pending a green run.

### Family 1 — Scripted & deterministic (best fit for launch-and-exit)

| Tool | Pin | Platforms to try | GIF path | GHA path |
|------|-----|------------------|----------|----------|
| VHS | v0.12.0 via `charmbracelet/vhs-action@v2` | linux, macos, windows | native | official action |
| Foley | latest (no tagged release) | linux, macos | native | custom install |
| Betamax (joshka) | v0.1.21 | linux, macos | native | custom install |
| EVP | latest (WIP) | linux | native (+SVG) | repo `action.yml` |
| console2svg | v0.9.3 | linux, macos, windows | SVG native + ffmpeg->GIF | official action |
| Demo Tape | gem 0.0.10 | linux, macos | native/ffmpeg | custom install |

### Family 2 — Interactive capture & replay

| Tool | Pin | Platforms to try | GIF path | GHA path |
|------|-----|------------------|----------|----------|
| asciinema + agg | CLI v3.2.1 + agg v1.9.0 | linux, macos | `.cast` -> agg | custom |
| PowerSession-rs + agg | v0.1.16 + agg v1.9.0 | windows | `.cast` -> agg | custom |
| Terminalizer | latest npm | linux (xvfb) | `render` (Electron) | custom |
| acast | v0.4.0 | linux, macos, windows | `.cast` -> agg | custom |
| termsvg | v0.11.0 | linux, macos | SVG -> GIF (repo renderer) | custom |

- **Rationale**: This spans both families, both PTY (Unix) and ConPTY (Windows) capture paths, and
  covers the strongest "missed" tools (console2svg, EVP, agg, termsvg, acast).
- **Shell handling**: The real split is PTY vs ConPTY, not bash vs zsh. On Linux/macOS we vary
  bash/zsh/pwsh where a tool exposes shell selection; on Windows the default is pwsh (bash =
  Git bash, not WSL). Non-applicable shells are marked with a reason (Principle III).

## Decision: Explicitly skipped tools (reported, not omitted)

Per Principle VI these appear in the report with reasons, not silently dropped.

| Tool | Reason skipped for CI-GIF eval |
|------|-------------------------------|
| s-vhs | Not a maintained standalone product (means VHS itself or a DIY stack). |
| ttysvg | No matching maintained project. Closest are termsvg / svg-term-cli / termtosvg. |
| TermRecord | Dead since 2017; outputs HTML, not GIF. |
| terminal-recorder | Stale since 2020; HTML output, no GIF. |
| tty-record | Quiet; HTML output, no GIF. |
| ovh-ttyrec | Maintained but no headless GIF path (ttygif needs X11). |
| script/scriptreplay | typescript only; no practical headless GIF converter. |
| t-rec | Screenshots a desktop window; fails on headless GHA (repo confirms). |
| ttygif | Converter needing ImageMagick + X11; fails headless. |
| termgif (pypi) | 1 star, unproven; may be attempted opportunistically. |
| asciinema-windows (Ruby) | Niche (1 star); PowerSession-rs is the stronger Windows path. |
| freeze / termshot | Static PNG/SVG, not animated GIF. |
| termtosvg / svg-term-cli / asciicast2gif | Archived/unmaintained. |
| menyoki / Peek | Need a display/GUI; not headless CI. |

## Decision: CI/report architecture

- **Provider**: GitHub Actions on `github.com/YoraiLevi/testing-area`, branch `testing-vhs`.
- **Per-tool workflow**: `.github/workflows/rec-<tool>.yml`, matrix over applicable `{os, shell}`,
  runs all four scenarios, uploads a per-cell GIF artifact and writes a per-cell result JSON.
- **Aggregation**: an in-workflow `needs:` job downloads that workflow's artifacts, copies GIFs to
  `assets/<tool>/`, writes `results/<tool>/*.json`, and commits to `testing-vhs` with `[skip ci]`
  behind a pull-rebase-push retry loop (avoids cross-workflow git races).
- **Report**: `scripts/build_report.py` (Python is present on every GHA runner) reads
  `results/**/*.json` and `assets/**`, and regenerates the README matrix + badges + embedded GIFs
  between fenced markers. A single `report` workflow (or the manual generator) is the only README
  writer, so there is no README merge race.
- **Badges**: per-tool workflow status badges
  (`…/actions/workflows/rec-<tool>.yml/badge.svg`) plus per-cell run links.
- **Rationale**: Single-writer README + per-tool asset paths keep concurrent workflows race-free
  while keeping GIFs embeddable directly from the repo (Principle V).
- **Alternatives rejected**: committing README from every matrix job (race-prone); relying on
  artifact URLs in README (not stable/embeddable); gh-pages (extra surface, no benefit for GIFs).

## Open risks carried into implementation

- VHS `Set Shell pwsh` producing a real GIF on `windows-latest`: UNVERIFIED; needs a green job.
- Foley/Betamax on Windows: libghostty-vt is Unix-oriented; treat Windows as likely not-applicable.
- asciinema exact headless flag: use documented `rec -c <cmd>` as the verified CI hook.
- omp version pinning: the installer tracks latest; `omp --version` output changes across releases.
  Re-run determinism holds within a fixed omp version; record the omp version used in each cell.
