# Hyperframes Composition Brief: Terminal Recorder Trials

## Objective
Create a short launch-style brag video for **Terminal Recorder Trials**, a CI benchmark that
made eleven terminal-to-GIF recorders prove they work in GitHub Actions.

## Output
- Composition directory: `brag-output/composition/`
- Rendered video: `brag-output/brag.mp4`
- Format: landscape — 1920x1080
- Duration: ~21s (voice-driven; scene lengths flex to the voiceover WAV)

## Source Material
- Project root: `C:/Users/devic/source/testing-area.worktrees/testing-vhs`
- Primary files read: `README.md` (report + Capability Grid), `scripts/tools.json`,
  `assets/console2svg/README.md` (real terminal capture), `scripts/build_report.py`
- Product name: Terminal Recorder Trials
- Tagline / strongest claim: "A cell counts as working only when a `testing-vhs` GitHub Actions
  job committed a GIF."
- Key UI/visual moment to recreate: the **Capability Grid** (tool rows x 5 platform columns with
  check / cross / dash glyphs) and a **live terminal capture** (`omp --version` -> `omp/18.2.7`)
- Copy that must appear verbatim:
  - `omp --version`
  - `omp/18.2.7`
  - "Every check-mark is a committed GIF. Not a screenshot."
  - "Terminal Recorder Trials"
  - Numbers: 11 recorders, 5 platforms, 4 scenarios, 161 working, 9 formats
  - Format chips: `gif  mp4  webm  svg  cast  webp  yml  avi  svgz`

## Creative Direction
- Tone preset: polished
- Creative direction: deadpan engineering benchmark, terminal-native, numbers-forward, CI-proven
- Interpretation: 4 scenes, confident holds, monospace type, restraint. Narration states facts
  calmly; the grid and the numbers brag. No hype words, no gradients-for-decoration.
- Angle: Every "record your terminal" tool claims it works; this project made all eleven prove it
  in CI and published one honest grid of who passed. The flex is the rigor — an evidence table,
  not a demo reel.
- Hook: dark terminal, blinking cursor, `omp --version` types out to `omp/18.2.7`, then
  "You recorded it. Did the recording actually work?"
- Outro / punchline: "161 green cells. 9 formats." then the title "Terminal Recorder Trials —
  the honest terminal-recorder benchmark."
- Avoid: generic SaaS language, abstract filler visuals, unrelated redesign, rainbow gradients,
  waveform/equalizer visuals.

## Visual Identity
- Background: #0d1117 (GitHub canvas dark)
- Panel: #161b22 surface, #30363d borders
- Text: #e6edf3 primary, #7d8590 muted
- Accent (pass/working): #228833 green
- Secondary: #4477AA blue, #AA3377 purple, #EE6677 red (broken), #BBBBBB grey (n/a)
- Display font: monospace (ui-monospace / "JetBrains Mono" / "SF Mono" fallback stack)
- Body font: same mono, lighter weight
- Visual references from the project: the Capability Grid matrix; check/cross/dash glyphs; the
  terminal prompt aesthetic; the Tol color families for scripted/hybrid/interactive.

## Storyboard
Use the storyboard in `brag-output/brag-plan.md` as the creative contract.

Scene summary:
1. Terminal hook — 5s — dark terminal, typed `omp --version` -> `omp/18.2.7`, hook line.
2. The scale — 4s — three numbers pop: 11 recorders, 5 platforms, 4 scenarios (held together).
3. Capability Grid — 7s — tool x platform matrix fills to green check-marks (+ few red/grey),
   holds readable, caption "Every check-mark is a committed GIF. Not a screenshot."
4. Tally + title — 5s — 161 working, 9 formats, format chips, then the title lands.

## Audio
- Audio role: clean steady bed under a calm voiceover; sparse terminal-native SFX
- Audio arc: intimate terminal (key ticks) -> accumulating numbers (drops) -> assembling grid
  (ticks, resolving bell) -> confident title (bell, music swell then fade)
- Music: `assets/music/happy-beats-business-moves-vol-12-by-ende-dot-app.mp3`
- Music treatment: bed ~0.30; duck to 0.13 while the voiceover speaks; small swell into the title;
  fade out over the final ~0.8s. Never above 0.30.
- Music cue guidance: bundled preset for vol-12 at
  `assets/music/cues/happy-beats-business-moves-vol-12-by-ende-dot-app.music-cues.json`
  (110 BPM). Strong cues: 8.74, 13.11, 17.47, 18.56, 22.93s. Bias the grid-complete payoff toward
  ~13.1s and the title reveal toward ~17.5-18.6s within 0.15s; the voiceover sets the real pace.
- Audio-reactive treatment: subtle — grid green glow and final title presence breathe with music
  RMS. No waveform/equalizer/particles.
- Audio-coupled moments:
  - Scene 1 typed command — per-character `keyboard/keypress-*.wav` (randomized); soft drop on output
  - Scene 2 numbers — one `interface/drop_*` per number (beat-grid, every other beat)
  - Scene 3 grid rows — light stamp tick on row flips (accent rows, not every cell); one soft bell
    (`impact/impactBell_heavy_000` or `interface/bong_001`) on grid completion
  - Scene 4 title — one soft `impact/impactBell_heavy_000`; card-fan on the format chips
- SFX selection guidance: match motion; polished restraint (<= ~1 SFX per beat); softer volumes
  (0.55-0.7). Prefer low high-frequency-risk files per `sfx-analysis.md`.
- SFX analysis guidance: `.agents/skills/brag/assets/sfx/sfx-analysis.md`
- Exact SFX choice: Hyperframes picks filenames, timestamps, density, and volume after the
  animation exists.
- Voiceover: `assets/voiceover.wav` (Kokoro af_heart) on its own track; music ducks to 0.12-0.15
  under it. Scene durations must flex to the WAV length — do not hardcode if narration disagrees.
- Audio files: copy chosen music, SFX, and the voiceover into `brag-output/composition/assets/`.

## Hyperframes Instructions
Load the composition-building Hyperframes domain skills — `hyperframes-core`,
`hyperframes-animation`, `hyperframes-creative`, `hyperframes-keyframes`, `hyperframes-cli`.
This is the `/brag` workflow: do not enter the `hyperframes` entry-point intent interview or route
into its generic promo / launch-video workflow. Prefer native Hyperframes conventions.

Requirements:
- Show at least one real element from the project: the Capability Grid AND the `omp --version`
  capture both qualify — include both.
- Keep all text readable (reading-time floor: short label ~0.8s settled, sentence ~0.3s/word).
- Keep the video within 15-25 seconds; let the voiceover set the pace.
- Include the planned music + SFX + voiceover layer; music ducks under the voice.
- Treat audio notes as guidance; choose SFX after the visual animation exists.
- Beat/cue metadata is optional timing hints; 1-3 strong-cue locks max; ignore cues that hurt
  readability or pacing.
- Subtle audio-reactive on the grid glow and title presence; no visualizer graphics.
- Use local relative asset paths only (never absolute).
- Run `npx hyperframes check` before render — brag's single gate.
