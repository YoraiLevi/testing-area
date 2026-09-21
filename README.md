# Terminal Recorder Trials

CI bake-off of terminal-to-GIF recorders against one TUI, [Oh My Pi (`omp`)](https://omp.sh).
A cell counts as working only when a `testing-vhs` GitHub Actions job committed a GIF.

## Recorder Families

```mermaid
flowchart LR
  subgraph SCR["Scripted (tape)"]
    direction TB
    FOLEY["Foley"]:::a
    BETA["Betamax (joshka)"]:::a
    DT["Demo Tape"]:::a
  end
  subgraph HYB["Hybrid (tape + live)"]
    direction TB
    VHS["VHS"]:::h
    C2S["console2svg"]:::h
    EVP["EVP"]:::h
    ASC["asciinema + agg"]:::h
    PS["PowerSession-rs + agg"]:::h
    TZ["Terminalizer"]:::h
  end
  subgraph INT["Interactive (live TTY)"]
    direction TB
    ACAST["acast"]:::b
    TSVG["termsvg"]:::b
  end
  classDef a fill:#4477AA,color:#fff,stroke:#222
  classDef b fill:#228833,color:#fff,stroke:#222
  classDef h fill:#AA3377,color:#fff,stroke:#222
```

## Platform and Shell

The split that matters is PTY (Linux and macOS) versus ConPTY (Windows), not bash versus zsh.

## How to Read This Report

The grid is the `launch-exit` tape (start `omp`, quit); each cell also runs `help-tour`,
`tui-splash`, and `typing-demo`.

<!-- REPORT:START -->

_Generated from committed CI results on `testing-vhs`._

### Capability Grid (headline scenario `launch-exit`)

| Tool | Family | linux-bash | linux-pwsh | linux-zsh | macos-zsh | windows-pwsh |
|------|--------|:--:|:--:|:--:|:--:|:--:|
| [VHS][vhs]<br><sub>gif · mp4 · webm</sub> | hybrid | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35550134845) | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35550134845) | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35550134845) | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35550134845) | [➖](https://github.com/YoraiLevi/testing-area/actions/runs/35550134845)<sup>1</sup> |
| [console2svg][console2svg]<br><sub>svg · gif · mp4 · webm</sub> | hybrid | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35567181044) | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35567181044) | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35567181044) | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35567181044) | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35567181044) |
| [Foley][foley]<br><sub>gif · mp4 · webm · webp · cast</sub> | scripted | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35569668217) | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35569668217) | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35569668217) | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35569668217) | ➖<sup>2</sup> |
| [Betamax (joshka)][betamax]<br><sub>gif · webp · mp4 · webm</sub> | scripted | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35567181010) | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35567181010) | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35567181010) | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35567181010) | ➖<sup>3</sup> |
| [EVP][evp]<br><sub>gif · svg · svgz</sub> | hybrid | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35569668208) | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35569668208) | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35569668208) | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35569668208) | ➖<sup>4</sup> |
| [Demo Tape][demotape]<br><sub>gif · mp4 · webm · avi</sub> | scripted | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35567181070) | ➖<sup>5</sup> | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35567181070) | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35567181070) | ➖<sup>6</sup> |
| [asciinema + agg][asciinema]<br><sub>cast · gif</sub> | hybrid | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35569668222) | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35569668222) | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35569668222) | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35569668222) | ➖<sup>7</sup> |
| [PowerSession-rs + agg][powersession]<br><sub>cast · gif</sub> | hybrid | ➖<sup>8</sup> | ➖<sup>8</sup> | ➖<sup>8</sup> | ➖<sup>8</sup> | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35569668204) |
| [Terminalizer][terminalizer]<br><sub>yml · gif</sub> | hybrid | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35569668277) | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35569668277) | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35569668277) | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35569668277) | [❌](https://github.com/YoraiLevi/testing-area/actions/runs/35569668277)<sup>9</sup> |
| [acast][acast]<br><sub>cast · gif</sub> | interactive | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35569668252) | [❌](https://github.com/YoraiLevi/testing-area/actions/runs/35569668252)<sup>10</sup> | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35569668252) | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35569668252) | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35569668252) |
| [termsvg][termsvg]<br><sub>cast · svg · gif · webm</sub> | interactive | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35569668272) | [❌](https://github.com/YoraiLevi/testing-area/actions/runs/35569668272)<sup>11</sup> | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35569668272) | [✅](https://github.com/YoraiLevi/testing-area/actions/runs/35569668272) | ➖<sup>12</sup> |

Legend: ✅ working · ❌ broken · ➖ not applicable

**Grid notes**

- **➖ not applicable.** No upstream build, or a platform-only dependency. Numbered notes give the cell's cause.

1. **VHS · `windows-pwsh`**: VHS records via ttyd, which has no Windows build (Unix-only); the capture pipeline cannot run on Windows.
2. **Foley · `windows-pwsh`**: Foley builds on libghostty-vt, which has no Windows native build (Unix-only).
3. **Betamax (joshka) · `windows-pwsh`**: Betamax builds on libghostty-vt-sys, which has no Windows native build (unsupported upstream).
4. **EVP · `windows-pwsh`**: EVP ships Linux and macOS binaries only; there is no Windows build.
5. **Demo Tape · `linux-pwsh`**: Demo Tape's --shell flag accepts only bash, zsh, or fish; PowerShell is not a supported shell.
6. **Demo Tape · `windows-pwsh`**: Demo Tape captures through ttyd, which is Unix-only; there is no Windows recording path.
7. **asciinema + agg · `windows-pwsh`**: The asciinema CLI is Unix-only; Windows capture is out of scope (PowerSession-rs is the Windows-native alternative).
8. **PowerSession-rs + agg · `linux-bash`, `linux-pwsh`, `linux-zsh`, `macos-zsh`**: PowerSession-rs is a Windows-only recorder (Win32 ConPTY); it does not run on Unix.
9. **Terminalizer · `windows-pwsh`**: terminalizer is installed and its CLI runs and the config is found and passed, but 'record' fails on Windows with a blank-path ENOENT ('File not found') when spawning the pty recording session headlessly; no valid GIF produced
10. **acast · `linux-pwsh`**: acast (v0.4.0) + agg (v1.9.0) produced no valid GIF for this cell in CI; see run logs
11. **termsvg · `linux-pwsh`**: no valid GIF produced in CI
12. **termsvg · `windows-pwsh`**: termsvg's record command imports syscall.SIGWINCH (POSIX-only); the record subcommand does not compile on Windows.


### What To Use

Headline `launch-exit` green, ranked by how many of the four tapes landed.

| Cell | Working recorders (scenarios / 4) |
|------|-----------------------------------|
| `linux-bash` · `linux-zsh` · `macos-zsh` | [acast][acast] (4/4), [asciinema + agg][asciinema] (4/4), [Betamax (joshka)][betamax] (4/4), [console2svg][console2svg] (4/4), [Demo Tape][demotape] (4/4), [EVP][evp] (4/4), [Foley][foley] (4/4), [Terminalizer][terminalizer] (4/4), [termsvg][termsvg] (4/4), [VHS][vhs] (4/4) |
| `linux-pwsh` | [asciinema + agg][asciinema] (4/4), [Betamax (joshka)][betamax] (4/4), [console2svg][console2svg] (4/4), [EVP][evp] (4/4), [Foley][foley] (4/4), [Terminalizer][terminalizer] (4/4), [VHS][vhs] (4/4) |
| `windows-pwsh` | [acast][acast] (4/4), [console2svg][console2svg] (4/4), [PowerSession-rs + agg][powersession] (4/4) |

**Green on every cell they target:** [asciinema + agg][asciinema] (16/16), [Betamax (joshka)][betamax] (16/16), [console2svg][console2svg] (20/20), [Demo Tape][demotape] (12/12), [EVP][evp] (16/16), [Foley][foley] (16/16), [PowerSession-rs + agg][powersession] (4/4), [VHS][vhs] (16/16, 4 N/A).

**Attempted and failed at least one cell:** [acast][acast] (17/20), [Terminalizer][terminalizer] (16/20), [termsvg][termsvg] (12/16).


### Recordings

Each tool's recordings, one sample per output format, live on its asset page.

**Jump to a recording:** [VHS](assets/vhs/README.md) · [console2svg](assets/console2svg/README.md) · [Foley](assets/foley/README.md) · [Betamax (joshka)](assets/betamax/README.md) · [EVP](assets/evp/README.md) · [Demo Tape](assets/demotape/README.md) · [asciinema + agg](assets/asciinema/README.md) · [PowerSession-rs + agg](assets/powersession/README.md) · [Terminalizer](assets/terminalizer/README.md) · [acast](assets/acast/README.md) · [termsvg](assets/termsvg/README.md)


### Skipped Tools

| Tool | Reason skipped for CI-GIF evaluation |
|------|--------------------------------------|
| s-vhs | Not a maintained standalone product (means VHS itself or a DIY tmux+asciinema stack). |
| ttysvg | No matching maintained project; closest are termsvg / svg-term-cli / termtosvg. |
| TermRecord | Dead since 2017; outputs self-contained HTML, not GIF. |
| terminal-recorder | Stale since 2020; HTML output, no GIF path. |
| tty-record | Quiet; HTML (asciinema-player) output, no GIF path. |
| ovh-ttyrec | Maintained but no headless GIF path (ttygif needs X11). |
| script / scriptreplay | typescript only; no practical headless GIF converter. |
| t-rec | Screenshots a desktop window; fails on headless GHA (repo confirms). |
| ttygif | Converter needing ImageMagick + X11; fails headless. |
| termgif (pypi) | 1 star, unproven; no CI evidence. |
| asciinema-windows (Ruby) | Niche (1 star); PowerSession-rs is the stronger Windows path. |
| freeze | Static PNG/SVG, not animated GIF. |
| termshot | Static PNG; no Windows asset. |
| termtosvg | Read-only/archived since 2020; SVG only. |
| svg-term-cli | Unmaintained since 2019; SVG only. |
| asciicast2gif | Archived 2022 (PhantomJS); superseded by agg. |
| menyoki | Linux X11/Wayland window capture; needs a display. |
| Peek | GUI app, archived 2025; not headless. |

_Tools discovered beyond the original list and evaluated:_ console2svg, EVP, acast, termsvg.


### CI Status

[![VHS](https://github.com/YoraiLevi/testing-area/actions/workflows/rec-vhs.yml/badge.svg?branch=testing-vhs)](https://github.com/YoraiLevi/testing-area/actions/workflows/rec-vhs.yml)
[![console2svg](https://github.com/YoraiLevi/testing-area/actions/workflows/rec-console2svg.yml/badge.svg?branch=testing-vhs)](https://github.com/YoraiLevi/testing-area/actions/workflows/rec-console2svg.yml)
[![Foley](https://github.com/YoraiLevi/testing-area/actions/workflows/rec-foley.yml/badge.svg?branch=testing-vhs)](https://github.com/YoraiLevi/testing-area/actions/workflows/rec-foley.yml)
[![Betamax (joshka)](https://github.com/YoraiLevi/testing-area/actions/workflows/rec-betamax.yml/badge.svg?branch=testing-vhs)](https://github.com/YoraiLevi/testing-area/actions/workflows/rec-betamax.yml)
[![EVP](https://github.com/YoraiLevi/testing-area/actions/workflows/rec-evp.yml/badge.svg?branch=testing-vhs)](https://github.com/YoraiLevi/testing-area/actions/workflows/rec-evp.yml)
[![Demo Tape](https://github.com/YoraiLevi/testing-area/actions/workflows/rec-demotape.yml/badge.svg?branch=testing-vhs)](https://github.com/YoraiLevi/testing-area/actions/workflows/rec-demotape.yml)
[![asciinema + agg](https://github.com/YoraiLevi/testing-area/actions/workflows/rec-asciinema.yml/badge.svg?branch=testing-vhs)](https://github.com/YoraiLevi/testing-area/actions/workflows/rec-asciinema.yml)
[![PowerSession-rs + agg](https://github.com/YoraiLevi/testing-area/actions/workflows/rec-powersession.yml/badge.svg?branch=testing-vhs)](https://github.com/YoraiLevi/testing-area/actions/workflows/rec-powersession.yml)
[![Terminalizer](https://github.com/YoraiLevi/testing-area/actions/workflows/rec-terminalizer.yml/badge.svg?branch=testing-vhs)](https://github.com/YoraiLevi/testing-area/actions/workflows/rec-terminalizer.yml)
[![acast](https://github.com/YoraiLevi/testing-area/actions/workflows/rec-acast.yml/badge.svg?branch=testing-vhs)](https://github.com/YoraiLevi/testing-area/actions/workflows/rec-acast.yml)
[![termsvg](https://github.com/YoraiLevi/testing-area/actions/workflows/rec-termsvg.yml/badge.svg?branch=testing-vhs)](https://github.com/YoraiLevi/testing-area/actions/workflows/rec-termsvg.yml)


[vhs]: https://github.com/charmbracelet/vhs
[console2svg]: https://github.com/arika0093/console2svg
[foley]: https://github.com/GH-Jaider/foley
[betamax]: https://github.com/joshka/betamax
[evp]: https://github.com/HalFrgrd/evp
[demotape]: https://github.com/fnando/demotape
[asciinema]: https://github.com/asciinema/asciinema
[powersession]: https://github.com/Watfaq/PowerSession-rs
[terminalizer]: https://github.com/faressoft/terminalizer
[acast]: https://github.com/gvcgo/asciinema
[termsvg]: https://github.com/mrmarble/termsvg
<!-- REPORT:END -->

## How to Reproduce

Run `rec-<tool>` on `testing-vhs` from the Actions tab, or push a change under that tool's
workflow, its `scenarios/` directory, or `scripts/`. See the
[quickstart](specs/001-terminal-recorder-trials/quickstart.md).
