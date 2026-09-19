# Contract: The Four omp Scenarios

Every evaluated tool records these same four scenarios so the report is comparable. Scenarios are
deterministic and pinned (constitution Principle IV). Each produces one GIF per cell.

Terminal geometry for every scenario: **100 cols × 24 rows**, typing speed fixed, theme default.
omp is installed first via `scenarios/shared/install-omp.{sh,ps1}` and `omp --version` must succeed
before recording.

## S1 `launch-exit` (minimal, REQUIRED)

Purpose: prove the recorder captures a real omp launch that starts and cleanly exits.

Behavior:
1. Show a prompt.
2. Run `omp --version`.
3. Brief pause so the version line is legible.
4. Exit the shell cleanly (exit code 0).

Reference (VHS-family `.tape`):
```
Output out.gif
Set Shell "bash"
Set FontSize 20
Set Width 1000
Set Height 600
Type "omp --version"  Enter  Sleep 2s
Type "exit"  Enter  Sleep 500ms
```

## S2 `help-tour` (creative)

Purpose: exercise color and long/scrolling output fidelity.

Behavior: run `omp --help`, pause to let the colored help render, exit. (`--help` is long and
colorized — good for judging color accuracy and scrollback capture.)

## S3 `tui-splash` (creative)

Purpose: exercise interactive TUI capture and clean quit handling.

Behavior: launch the omp TUI (`omp`), let the splash / onboarding screen render (~3s), then quit
(`Ctrl+C`, or type `/exit` + Enter where the TUI is interactive). Recording the onboarding screen
without provider keys is acceptable and honest — it still demonstrates interactive capture.

Note: some tools cannot drive/quit an interactive TUI headlessly. Such a cell is recorded as
`broken` with the reason (Principle III / FR-005), which is itself an informative result.

## S4 `typing-demo` (creative)

Purpose: exercise keystroke animation and input rendering.

Behavior: launch the omp TUI, type a sample prompt into the input box **without sending it**
(e.g. `Type "explain this repo"`), pause so the typed text is visible, then quit. Where a tool
cannot reach the TUI input, fall back to typing the sample text at a shell prompt (still exercises
keystroke animation) and record that substitution in the trial `reason`.

## Determinism requirements (all scenarios)

- Pin the recorder version and record it in the trial `extra.tool_version`.
- Record `omp --version` output in `extra.omp_version`.
- Fixed geometry, font size, and typing speed; no wall-clock timestamps rendered.
- Re-running a cell without changes MUST yield an equivalent GIF (SC-007).
