# Terminal Recorder Trials

**Which terminal recorder actually works, on which OS and shell, for recording a real program
(here: [Oh My Pi `omp`](https://omp.sh)) — proven in CI, not by popularity.**

Every verdict below is produced by a GitHub Actions run on the `testing-vhs` branch that uploaded a
GIF artifact. Stars and issue counts never decide the verdict (see
[`.specify/memory/constitution.md`](.specify/memory/constitution.md), Principles I & II). Design
lives in [`specs/001-terminal-recorder-trials/`](specs/001-terminal-recorder-trials/).

## The two families surveyed

```mermaid
flowchart LR
  subgraph F1["Scripted &amp; deterministic (.tape / capture-cmd)"]
    direction TB
    VHS["VHS"]:::a
    FOLEY["Foley"]:::a
    BETA["Betamax"]:::a
    EVP["EVP"]:::a
    C2S["console2svg"]:::a
    DT["Demo Tape"]:::a
  end
  subgraph F2["Interactive capture &amp; replay (.cast / typescript)"]
    direction TB
    ASC["asciinema + agg"]:::b
    PS["PowerSession-rs + agg"]:::b
    TZ["Terminalizer"]:::b
    ACAST["acast"]:::b
    TSVG["termsvg"]:::b
  end
  OMP(["omp launch + exit\n(+ 3 creative scenarios)"]):::c
  OMP --> F1
  OMP --> F2
  F1 --> GIF["GIF artifact\n(committed to repo)"]:::d
  F2 --> GIF
  classDef a fill:#4477AA,color:#fff,stroke:#222
  classDef b fill:#228833,color:#fff,stroke:#222
  classDef c fill:#CCBB44,color:#111,stroke:#222
  classDef d fill:#AA3377,color:#fff,stroke:#222
```

## Platform × shell reality

The real split is **PTY (Unix) vs ConPTY (Windows)**, not bash vs zsh. `pwsh` runs everywhere;
`bash` on Windows is Git Bash (not WSL) on GitHub runners. Window-screenshot tools (t-rec, ttygif,
Peek, menyoki) cannot run on headless runners and are excluded with reasons in the ledger below.

## How to read this report

- The **Capability Grid** cell links to the exact CI run that produced (or failed to produce) the
  recording.
- The **Recordings** section embeds the four omp scenarios (`launch-exit`, `help-tour`,
  `tui-splash`, `typing-demo`) for each working tool.
- The **Skipped ledger** lists every candidate not evaluated in CI, with the reason (honest coverage,
  constitution Principle VI).

<!-- REPORT:START -->
<!-- REPORT:END -->

## Reproduce

This project is validated in CI only. Trigger a tool via the Actions tab
(`rec-<tool>` → Run workflow on `testing-vhs`) or push a change under `scenarios/**`. See
[`specs/001-terminal-recorder-trials/quickstart.md`](specs/001-terminal-recorder-trials/quickstart.md).
