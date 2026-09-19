#!/usr/bin/env python3
"""Drive `acast record` headlessly for the four omp scenarios.

acast (gvcgo/asciinema) records the *shell* session ($SHELL on unix,
powershell.exe on Windows) inside a PTY/ConPTY until the shell exits; it has no
`-c command` mode. So we allocate a controlling terminal, spawn `acast record
<out.cast>`, and feed keystrokes with realistic delays -- exactly like a VHS tape.

Terminal geometry is fixed at 100x24 (scenarios.md). On POSIX we open a real PTY
and set its winsize so acast's header dimensions and the inner shell match. On
Windows there is no pty module, but acast forwards its own stdin to the ConPTY,
so we stream keystrokes through a stdin pipe instead.

Usage: drive.py <scenario> <shell-path> <out.cast>
"""
import os
import subprocess
import sys
import time

COLS, ROWS = 100, 24
TYPING = 0.05  # per-character delay, fixed typing speed

CR = b"\r"
CTRL_C = b"\x03"


def actions(scenario: str):
    """A scenario is a list of (kind, payload) steps.

    kind: "sleep" -> seconds; "type" -> str typed char-by-char; "send" -> raw bytes.
    """
    if scenario == "launch-exit":
        return [
            ("sleep", 1.0),
            ("type", "omp --version"), ("send", CR),
            ("sleep", 2.5),
            ("type", "exit"), ("send", CR),
            ("sleep", 0.8),
        ]
    if scenario == "help-tour":
        return [
            ("sleep", 1.0),
            ("type", "omp --help"), ("send", CR),
            ("sleep", 3.5),
            ("type", "exit"), ("send", CR),
            ("sleep", 0.8),
        ]
    if scenario == "tui-splash":
        return [
            ("sleep", 1.0),
            ("type", "omp --no-session"), ("send", CR),
            ("sleep", 4.5),
            ("send", CTRL_C), ("sleep", 0.8),
            ("send", CTRL_C), ("sleep", 1.0),
            ("type", "exit"), ("send", CR),
            ("sleep", 0.8),
        ]
    if scenario == "typing-demo":
        return [
            ("sleep", 1.0),
            ("type", "omp --no-session"), ("send", CR),
            ("sleep", 3.5),
            ("type", "explain what this repository does"),
            ("sleep", 2.0),
            ("send", CTRL_C), ("sleep", 0.8),
            ("send", CTRL_C), ("sleep", 1.0),
            ("type", "exit"), ("send", CR),
            ("sleep", 0.8),
        ]
    raise SystemExit(f"drive: unknown scenario {scenario!r}")


def perform(write, steps):
    for kind, payload in steps:
        if kind == "sleep":
            time.sleep(payload)
        elif kind == "type":
            for ch in payload:
                write(ch.encode("utf-8"))
                time.sleep(TYPING)
        elif kind == "send":
            write(payload)


def run_posix(cmd, env, steps) -> int:
    import fcntl
    import pty
    import select
    import struct
    import termios
    import threading

    master, slave = pty.openpty()
    winsize = struct.pack("HHHH", ROWS, COLS, 0, 0)
    fcntl.ioctl(slave, termios.TIOCSWINSZ, winsize)

    proc = subprocess.Popen(
        cmd, stdin=slave, stdout=slave, stderr=slave,
        env=env, close_fds=True, preexec_fn=os.setsid,
    )
    os.close(slave)

    def drain():
        while True:
            try:
                r, _, _ = select.select([master], [], [], 0.2)
            except (OSError, ValueError):
                return
            if master in r:
                try:
                    if not os.read(master, 65536):
                        return
                except OSError:
                    return

    reader = threading.Thread(target=drain, daemon=True)
    reader.start()

    def write(data):
        os.write(master, data)

    perform(write, steps)

    try:
        rc = proc.wait(timeout=45)
    except subprocess.TimeoutExpired:
        proc.kill()
        rc = 124
    time.sleep(0.5)
    try:
        os.close(master)
    except OSError:
        pass
    return rc


def run_windows(cmd, env, steps) -> int:
    proc = subprocess.Popen(
        cmd, stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=env,
    )

    def write(data):
        proc.stdin.write(data)
        proc.stdin.flush()

    try:
        perform(write, steps)
    except (BrokenPipeError, OSError):
        pass
    try:
        rc = proc.wait(timeout=45)
    except subprocess.TimeoutExpired:
        proc.kill()
        rc = 124
    return rc


def main(argv) -> int:
    if len(argv) != 3:
        raise SystemExit("usage: drive.py <scenario> <shell-path> <out.cast>")
    scenario, shell, out_cast = argv
    steps = actions(scenario)

    env = dict(os.environ)
    if os.name == "posix":
        env["SHELL"] = shell
        env.setdefault("LANG", "C.UTF-8")
        env.setdefault("LC_ALL", "C.UTF-8")
        env["TERM"] = "xterm-256color"

    cmd = ["acast", "record", out_cast]
    print(f"drive: scenario={scenario} shell={shell} out={out_cast}", flush=True)

    if os.name == "nt":
        rc = run_windows(cmd, env, steps)
    else:
        rc = run_posix(cmd, env, steps)

    ok = os.path.exists(out_cast) and os.path.getsize(out_cast) > 0
    print(f"drive: rc={rc} cast_exists={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
