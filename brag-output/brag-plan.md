# Brag Plan: Terminal Recorder Trials

## What is this app?
A CI bake-off that pits eleven terminal-to-GIF recorders against one TUI (Oh My Pi, `omp`)
across five OS/shell cells and four scenarios, where a cell counts as working only when a
`testing-vhs` GitHub Actions job actually committed a GIF. It is a benchmark that refuses to
take a screenshot's word for it.

## The angle
Every "record your terminal" tool claims it works. This project made all eleven of them prove
it, in CI, on five platforms, and published one honest grid of who passed. The flex is the
rigor: not a demo reel, an evidence table. Deadpan engineering confidence, terminal-native.

## Hook (first 2-3 seconds)
A dark terminal with a blinking prompt. A command types itself: `omp --version` -> `omp/18.2.7`.
Then one line lands: "You recorded it. Did the recording actually work?" The real captured
output IS the hook, so the video opens inside the exact thing being measured.

## Key moments (the middle)
- The scale, stated as fact: 11 recorders / 5 platforms / 4 scenarios pop in as hard numbers.
- The Capability Grid fills in: rows of tools, columns of platforms, cells stamping to green
  check-marks with a scatter of red and grey — the actual README matrix.
- The proof rule, verbatim in spirit: "Every check-mark is a committed GIF. Not a screenshot."

## Outro / punchline
The tally settles — 161 green cells, 9 output formats — then the title lands:
"Terminal Recorder Trials. The honest terminal-recorder benchmark."

## User flow worth showing
none — repo/report, no interactive app. Centerpiece is the real Capability Grid matrix plus
the real `omp --version` capture. Both are genuine artifacts from this project.

## Tone
- Preset: polished
- Creative direction: deadpan engineering benchmark, terminal-native, numbers-forward, CI-proven
- Interpretation: few scenes, confident holds, monospace type, restraint. The narration states
  facts calmly; the numbers and the grid do the bragging. No hype adjectives.

## Format: landscape — 1920x1080
## Duration: ~21s (voice-driven; scene lengths flex to the narration WAV)

## Visual identity (from the project)
- Background: #0d1117 (GitHub canvas dark, where this report lives)
- Panel: #161b22 with #30363d borders (GitHub surface)
- Accent (working / pass): #228833 (the grid's working glyph + interactive-family color)
- Secondary accents: #4477AA blue (scripted family), #AA3377 purple (hybrid family),
  #EE6677 red (broken), #BBBBBB grey (n/a) — Tol palette used across the repo
- Text: #e6edf3 primary, #7d8590 muted
- Display font: monospace (ui-monospace / "JetBrains Mono" / "SF Mono" fallback) — terminal-native
- Body font: same mono, lighter weight for captions
- Strongest visual element: the Capability Grid (tools x platforms, check/cross/dash), and the
  live terminal capture `omp --version` -> `omp/18.2.7`

## Share copy (draft)
I made all 11 terminal-to-GIF recorders prove they work — in CI, on 5 platforms, 4 scenarios.
Every green cell is a GitHub Actions run that committed a real GIF, not a screenshot. 161 passed.

## Audio direction
- Role: clean, steady bed under a calm voiceover; sparse terminal-native SFX
- Music: happy-beats-business-moves-vol-12 (steady/clean, fits polished)
- Music treatment: start at 0.0, bed ~0.30; duck to 0.13 whenever the voiceover speaks; small
  swell into the final title; fade out over the last ~0.8s
- Music cue guidance: bundled preset for vol-12 (110 BPM). Strong cues in window: 8.74, 13.11,
  17.47, 18.56, 22.93s. Bias the grid-complete payoff and the title reveal toward a strong cue
  (~13.1s grid, ~17.5-18.6s title) within 0.15s; let the voiceover set the real pace.
- Audio-reactive treatment: subtle; let the grid's green glow and the final title presence
  breathe with music RMS. No waveform/equalizer visuals.
- SFX posture: sparse, motion-matched. Per-character key ticks on the typed command; soft drops
  on the three big numbers; a light stamp tick as grid cells flip green; one soft bell on the
  title. Nothing aggressive (polished restraint).
- Audio-coupled moments: typed `omp --version` (keyboard), number pops (drop), grid cell flips
  (tick), final title (bell).
- Restraint rule: no more than ~1 SFX per beat; never let SFX or music cover the voice; music
  stays <= 0.30 and ducks under narration.

## Voiceover script
Voice: af_heart (Kokoro), calm and confident. Four lines, one per scene.

1. "You recorded your terminal. But did the recording actually work?"
2. "So we tested eleven recorders in CI, across five platforms and four scenarios."
3. "Every green cell is a real GIF, committed by a GitHub Actions run. Not a screenshot, not a promise."
4. "A hundred and sixty-one green cells. Nine formats. One honest answer. Terminal Recorder Trials."

## Storyboard

### Scene 1 — Terminal hook — 5s
Dark terminal panel. Blinking block cursor at a `$` prompt. `omp --version` types out character
by character, then the output line `omp/18.2.7` appears. Beneath it, the hook line fades up:
"You recorded it. Did the recording actually work?"
Sequential/interaction: yes — the command types character by character (simulated typing), then
output appears one line below.
Audio intent: intimate, real; you are inside a terminal. Key ticks per character; low music enters.
Audio-coupled idea: per-character keyboard keypresses on the typed command; soft drop as output lands.
Music: vol-12 bed enters ~0.30, ducks under the voiceover.
Transition mood: soft crossfade -> Scene 2

### Scene 2 — The scale — 4s
Three hard numbers arrive one by one on a clean dark field: **11 recorders**, **5 platforms**,
**4 scenarios**. A muted fourth line settles under them: "one TUI: omp".
Sequential/interaction: yes — three numbers pop in sequence, held together on screen after the
third so all three are readable (hold the full set ~1.2s).
Audio intent: matter-of-fact accumulation; each number a soft placement.
Audio-coupled idea: a soft interface/drop on each number (beat-grid, every other beat).
Music: steady bed, ducked under voice.
Transition mood: clean -> Scene 3

### Scene 3 — The Capability Grid — 7s
The centerpiece. A compact matrix: ~8 tool rows down the left, five platform columns across the
top (linux-bash, linux-pwsh, linux-zsh, macos-zsh, windows-pwsh). Cells stamp in mostly green
check-marks, with a few red crosses and grey dashes, row by row. As it completes, a caption lands:
"Every check-mark is a committed GIF. Not a screenshot."
Sequential/interaction: yes — cells fill row by row (quick), then the completed grid holds ~2s so
it is readable; the caption reveals after the grid settles.
Audio intent: rhythmic assembling of evidence, resolving to a confident payoff on completion.
Audio-coupled idea: light stamp tick as rows flip green (accent rows, not every cell); one soft
bell when the grid completes and the caption lands.
Music: bed; small lift into the grid-complete beat (~13.1s strong cue) if timing allows.
Audio-reactive: subtle green glow on the grid breathes with RMS.
Transition mood: clean -> Scene 4

### Scene 4 — Tally + title — 5s
The result settles into two big figures: **161 working** and **9 formats**, with a row of format
chips beneath: `gif  mp4  webm  svg  cast  webp  yml  avi  svgz`. Then the title lands full-scale:
"Terminal Recorder Trials" with the line "The honest terminal-recorder benchmark."
Sequential/interaction: format chips appear as a quick fanned set, then hold; title reveals last.
Audio intent: quiet confidence; the flex is the number, not the volume.
Audio-coupled idea: soft card-fan on the format chips; one impactBell on the title.
Music: small swell into the title (bias to ~17.5-18.6s strong cue), then fade out over ~0.8s.
Audio-reactive: subtle title presence breathes on the final musical moment.
Transition mood: soft settle to hold (end)

**Music mood for this video:** polished / steady / clean
**Audio summary:** A calm confident voiceover carries four facts; a steady 110-BPM bed sits low
and ducks under the voice, with sparse terminal-native SFX (key ticks, drops, one bell) landing
on the typed command, the numbers, the grid completion, and the title.
