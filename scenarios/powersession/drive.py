#!/usr/bin/env python3
"""Drive PowerSession-rs `rec` headlessly on the windows-pwsh CI runner.

PowerSession (v0.1.16) is a Windows-only, asciinema-compatible recorder built on
the Windows Pseudo Console (ConPTY). `PowerSession.exe rec <file> --command
"<cmd>"` spawns <cmd> under a pseudo console, forwards this process's stdin to
it, and writes every stdout chunk to an asciicast v2 `.cast` until the child
exits.

Scenario handling:
  * launch-exit / help-tour  hand PowerSession a self-contained `pwsh -File`
    script that runs omp and exits, so the recording is a real launch->exit with
    no keystroke-timing races.
  * tui-splash  launches the omp TUI (which never exits on its own headlessly); a
    watchdog tree-kills PowerSession after the splash has rendered, ending the
    recording with the splash captured (PowerSession cannot send an interactive
    quit to the TUI headlessly).
  * typing-demo  scenarios.md S4 shell-prompt fallback: PowerSession cannot inject
    keystrokes into the omp TUI input box headlessly, so an interactive pwsh is
    driven over stdin to TYPE a sample prompt (without Enter) at the shell prompt,
    exercising keystroke animation, then the shell is closed.

Usage: drive.py <scenario> <cast_path>
"""
import os
import subprocess
import sys
import threading
import time

TYPING = 0.05  # per-character delay, fixed typing speed
CR = b"\r"
CTRL_C = b"\x03"

SCRIPT_DIR = "scenarios/powersession"


def pwsh_file(script: str) -> str:
    return f"pwsh.exe -NoLogo -NoProfile -File {SCRIPT_DIR}/{script}"


def tree_kill(pid: int) -> None:
    subprocess.run(
        ["taskkill", "/F", "/T", "/PID", str(pid)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )


def plan(scenario: str):
    """Return (command_arg, kill_after_seconds, steps)."""
    if scenario == "launch-exit":
        return pwsh_file("launch-exit.ps1"), None, []
    if scenario == "help-tour":
        return pwsh_file("help-tour.ps1"), None, []
    if scenario == "tui-splash":
        # No stdin steps; a watchdog tree-kills PowerSession once the splash rendered.
        return pwsh_file("tui-splash.ps1"), 6.0, []
    if scenario == "typing-demo":
        steps = [
            ("sleep", 1.5),
            ("type", "explain what this repository does"),
            ("sleep", 2.0),
            ("send", CTRL_C),
            ("sleep", 0.6),
            ("type", "exit"), ("send", CR),
            ("sleep", 0.8),
        ]
        return "pwsh.exe -NoLogo -NoProfile", None, steps
    raise SystemExit(f"drive: unknown scenario {scenario!r}")


def record(scenario: str, cast: str) -> int:
    command_arg, kill_after, steps = plan(scenario)
    cmd = ["PowerSession.exe", "rec", cast, "-f", "--log-level", "trace",
           "--command", command_arg]
    print(f"drive: {' '.join(cmd)}", flush=True)

    # CREATE_NEW_CONSOLE gives PowerSession its own real console screen buffer,
    # so its stdout-mirror thread's WriteConsoleW (record.rs:270) no longer fails
    # with HRESULT 0x80070001 the way it does on the runner's redirected stdout.
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                            creationflags=subprocess.CREATE_NEW_CONSOLE)

    if kill_after is not None:
        def watchdog():
            time.sleep(kill_after)
            print(f"drive: watchdog tree-killing PowerSession pid={proc.pid}", flush=True)
            tree_kill(proc.pid)
        threading.Thread(target=watchdog, daemon=True).start()

    def write(data: bytes) -> None:
        if proc.poll() is not None:
            return
        try:
            proc.stdin.write(data)
            proc.stdin.flush()
        except (BrokenPipeError, OSError):
            pass

    for kind, payload in steps:
        if kind == "sleep":
            time.sleep(payload)
        elif kind == "type":
            for ch in payload:
                write(ch.encode("utf-8"))
                time.sleep(TYPING)
        elif kind == "send":
            write(payload)

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
    finally:
        try:
            if proc.stdin:
                proc.stdin.close()
        except (BrokenPipeError, OSError):
            pass

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
