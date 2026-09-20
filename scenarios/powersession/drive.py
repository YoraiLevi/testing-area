#!/usr/bin/env python3
"""Drive PowerSession-rs `rec` headlessly on the windows-pwsh CI runner.

PowerSession (v0.1.16) is a Windows-only, asciinema-compatible recorder built on
the Windows Pseudo Console (ConPTY). `PowerSession.exe rec <file> --command
"<cmd>"` spawns <cmd> under a pseudo console and writes every stdout chunk to an
asciicast v2 `.cast` until the child exits. Its stdout-mirror thread uses
WriteConsoleW, so PowerSession is launched in its own new console (see record()).

Scenario handling:
  * launch-exit / help-tour  hand PowerSession a self-contained `pwsh -File`
    script that runs omp and exits, so the recording is a real launch->exit with
    no keystroke-timing races.
  * tui-splash  launches the omp TUI (which never exits on its own headlessly); a
    watchdog tree-kills PowerSession after the splash has rendered, ending the
    recording with the splash captured (PowerSession cannot send an interactive
    quit to the TUI headlessly).
  * typing-demo  scenarios.md S4 shell-prompt fallback: PowerSession cannot inject
    keystrokes into the omp TUI input box headlessly, so a self-contained
    `pwsh -File` script types a sample prompt char-by-char at the shell prompt
    (keystroke animation) and exits.

Usage: drive.py <scenario> <cast_path>
"""
import os
import subprocess
import sys
import threading
import time

SCRIPT_DIR = "scenarios/powersession"


def pwsh_file(script: str) -> str:
    return f"pwsh.exe -NoLogo -NoProfile -File {SCRIPT_DIR}/{script}"


def tree_kill(pid: int) -> None:
    subprocess.run(
        ["taskkill", "/F", "/T", "/PID", str(pid)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )


def plan(scenario: str):
    """Return (command_arg, kill_after_seconds). Every scenario is a self-exiting
    `--command` script so PowerSession can run in a new console without stdin."""
    if scenario == "launch-exit":
        return pwsh_file("launch-exit.ps1"), None
    if scenario == "help-tour":
        return pwsh_file("help-tour.ps1"), None
    if scenario == "tui-splash":
        # A watchdog tree-kills PowerSession once the splash has rendered.
        return pwsh_file("tui-splash.ps1"), 6.0
    if scenario == "typing-demo":
        return pwsh_file("typing-demo.ps1"), None
    raise SystemExit(f"drive: unknown scenario {scenario!r}")


def record(scenario: str, cast: str) -> int:
    command_arg, kill_after = plan(scenario)
    cmd = ["PowerSession.exe", "rec", cast, "-f", "--log-level", "trace",
           "--command", command_arg]
    print(f"drive: {' '.join(cmd)}", flush=True)

    # PowerSession's stdout-mirror thread calls WriteConsoleW, which needs a real
    # console screen buffer. Launch it in a brand-new console with NO stdio
    # redirection so that console owns stdout/stderr; a redirected/inherited stdout
    # pipe makes WriteConsoleW fail with HRESULT 0x80070001. Every scenario is a
    # self-exiting `--command` script, so no stdin injection is needed.
    proc = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)

    if kill_after is not None:
        def watchdog():
            time.sleep(kill_after)
            print(f"drive: watchdog tree-killing PowerSession pid={proc.pid}", flush=True)
            tree_kill(proc.pid)
        threading.Thread(target=watchdog, daemon=True).start()

    try:
        rc = proc.wait(timeout=45)
    except subprocess.TimeoutExpired:
        print("drive: 45s timeout; tree-killing PowerSession", flush=True)
        tree_kill(proc.pid)
        try:
            rc = proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
            rc = 124

    print(f"drive: PowerSession exit={rc}", flush=True)
    return rc


def main(argv) -> int:
    if len(argv) != 2:
        print("usage: drive.py <scenario> <cast_path>", file=sys.stderr)
        return 2
    scenario, cast = argv
    os.makedirs(os.path.dirname(cast) or ".", exist_ok=True)
    record(scenario, cast)
    size = os.path.getsize(cast) if os.path.exists(cast) else 0
    print(f"drive: cast={cast} size={size}", flush=True)
    # Always succeed: the workflow's validate_gif + cast inspection set the verdict.
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
