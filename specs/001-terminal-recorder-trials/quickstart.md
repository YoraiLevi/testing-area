# Quickstart / Validation Guide: Terminal Recorder Trials

This project is validated **in CI only** (constitution Principle I). There is no local run path;
the steps below describe how to trigger and read the evidence.

## Prerequisites

- Push access to `github.com/YoraiLevi/testing-area`, branch `testing-vhs`.
- GitHub Actions enabled with write permission for the `GITHUB_TOKEN` (Settings → Actions → Workflow
  permissions → Read and write), so aggregate jobs can commit GIFs/results back to `testing-vhs`.

## Trigger a single tool trial

1. Push a change under `scenarios/**` / `scripts/**` / the tool workflow, or use the Actions tab →
   `rec-<tool>` → **Run workflow** (`workflow_dispatch`) on `testing-vhs`.
2. Watch the matrix: each `{os, shell}` cell records the four scenarios and uploads
   `rec-<tool>-<os>-<shell>` artifacts.

## Validate the evidence (per constitution)

A cell counts as **working** only if all of these hold:

- The `record` matrix job for that cell is green.
- The uploaded artifact contains a non-empty GIF that passes `scripts/validate_gif.py`
  (GIF magic bytes + non-zero size).
- A `results/<tool>/<os>-<shell>-<scenario>.json` exists with `verdict: working`, a `gif` path, and
  a `run_url`.

Expected outcomes:

- **Green + GIF present** → the cell is proven working; the GIF appears under `assets/<tool>/`.
- **Red step / missing GIF** → the cell is `broken` with a recorded reason; never a silent pass.
- **Non-applicable cell** (e.g. zsh on stock Windows) → a `not-applicable` result with a reason.

## Regenerate the report

1. Run the `report` workflow (or `python scripts/build_report.py` in CI). It reads `results/**` and
   `assets/**` and rewrites the README status grid, badges, and embedded GIFs between the
   `<!-- REPORT:START -->` / `<!-- REPORT:END -->` markers.
2. Confirm in the README:
   - Every tool row shows a verdict for each applicable cell, with no blanks (SC-001).
   - Each `working` cell links to its generating run (SC-003).
   - Each working tool shows the minimal GIF plus three creative GIFs (SC-004).
   - The skipped-tool ledger is present with reasons (Principle VI).

## Smoke expectations for the first green run

The highest-confidence first proof is **VHS via `charmbracelet/vhs-action@v2` on `ubuntu-latest`**
recording `S1 launch-exit`: it should yield a committed `assets/vhs/linux-bash-launch-exit.gif` and a
`working` result — satisfying SC-002 end-to-end.

## References

- Scenarios: [contracts/scenarios.md](./contracts/scenarios.md)
- Workflow shape: [contracts/workflow-contract.md](./contracts/workflow-contract.md)
- Result schema: [contracts/result.schema.json](./contracts/result.schema.json)
- Tool selection & skip ledger: [research.md](./research.md)
