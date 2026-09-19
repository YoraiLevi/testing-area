# Contract: `rec-<tool>.yml` Workflow Shape

Every per-tool workflow MUST follow this shape so results and badges are uniform.

## Triggers

```yaml
on:
  push:
    branches: [testing-vhs]
    paths:
      - '.github/workflows/rec-<tool>.yml'
      - 'scenarios/**'
      - 'scripts/**'
  workflow_dispatch: {}
```

## Matrix job (`record`)

- `strategy.fail-fast: false` (one broken cell must not hide the others).
- `strategy.matrix.include:` lists only the **applicable** `{os, shell}` cells for this tool.
  Non-applicable cells are NOT run here; instead the aggregate job emits their `not-applicable`
  result records with a reason.
- Steps per cell:
  1. `actions/checkout@v4`.
  2. Install omp (`scenarios/shared/install-omp.sh` or `.ps1`) and assert `omp --version`.
  3. Install the pinned recorder (+ converter such as `agg`/`ffmpeg` if needed).
  4. Run each of the four scenarios; produce `out/<os>-<shell>-<scenario>.gif` (+ optional
     `.mp4`/`.svg`).
  5. `python scripts/validate_gif.py out/*.gif` — fail the step if any required GIF is missing,
     zero-byte, or lacks GIF magic bytes (FR-007).
  6. Write a `results/<tool>/<os>-<shell>-<scenario>.json` per scenario
     (schema: `result.schema.json`), including `run_url = ${{ github.server_url }}/${{
     github.repository }}/actions/runs/${{ github.run_id }}`.
  7. `actions/upload-artifact@v4` with name `rec-<tool>-<os>-<shell>` containing the GIFs + JSONs.

## Aggregate job (`collect`)

- `needs: [record]`, `if: always()` (still commit results even if some cells failed).
- Steps:
  1. `actions/checkout@v4` on `testing-vhs`.
  2. `actions/download-artifact@v4` (all `rec-<tool>-*`).
  3. Copy GIFs to `assets/<tool>/…`, JSONs to `results/<tool>/…`.
  4. Emit `not-applicable` result records for every cell in the tool's declared skip list, each with
     a reason (Principle III / FR-005).
  5. Commit via `scripts/commit-artifacts.sh` (configures bot identity, `git pull --rebase`, commit
     with `[skip ci]`, push with retry loop) so concurrent tool workflows never race.

## Invariants

- The workflow MUST NOT modify `README.md` (only `report.yml` / `build_report.py` writes it).
- Every declared cell (run or skipped) MUST end with exactly one result record (no blank grid cells,
  SC-001).
- A `working` verdict MUST reference a validated, committed GIF (Principles II, V; SC-003).
