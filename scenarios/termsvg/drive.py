#!/usr/bin/env python3
"""Headless PTY driver for `termsvg record`.

termsvg's `record` command calls `term.MakeRaw(os.Stdin)` and
`term.GetSize(os.Stdout)` (see cmd/termsvg/record/record.go), so it refuses to
run unless BOTH stdin and stdout are real TTYs. GitHub Actions runners have no
controlling terminal, so we allocate our own PTY sized to the scenario geometry
(100x24), run termsvg inside it, and feed a scripted sequence of keystrokes into
the recorded shell -- typing char-by-char so the resulting asciicast animates the
input just like an interactive session.

Usage: drive.py <cast-out> <shell> <scenario> <rec-subcommand>
  scenario in {launch-exit, help-tour, tui-splash, typing-demo}
"""
from __future__ import annotations

import fcntl
import os
import select
import signal
import struct
import sys
import termios
import time

COLS, ROWS = 100, 24
TYPE_DELAY = 0.06          # seconds between characters while "typing"
STARTUP_WAIT = 1.6        # let termsvg + shell spin up and print a prompt
CHILD_GRACE = 25.0         # seconds to wait for termsvg to save after the script
HARD_LIMIT = 150           # absolute backstop (seconds) for the whole run


def omp_watchdog(run_secs: int) -> str:
    """Command that runs the omp TUI in the terminal's foreground group and force-
    terminates it after `run_secs`. Using `sh -c` (job control off) keeps omp in the
    foreground process group so it renders and receives typed input, while a
    background watchdog escalates INT -> TERM -> KILL to guarantee a clean return."""
    return (
        "sh -c 'omp --no-session & p=$!; "
        f"(sleep {run_secs}; kill -INT $p 2>/dev/null; sleep 1; "
        "kill -TERM $p 2>/dev/null; sleep 1; kill -KILL $p 2>/dev/null) "
        ">/dev/null 2>&1 & wait $p'"
    )


def build_actions(scenario: str):
    """A scenario is a list of actions:
        ("type", text, per_char_delay) -- type text character by character
        ("key",  bytes)                -- send raw bytes (Enter=\\r, Ctrl+C=\\x03)
        ("sleep", seconds)             -- idle, keeping the recording running
    """
    acts: list = [("sleep", STARTUP_WAIT)]

    def run_line(cmd: str, delay: float = TYPE_DELAY):
        acts.append(("type", cmd, delay))
        acts.append(("sleep", 0.4))
        acts.append(("key", b"\r"))

    if scenario == "launch-exit":
        run_line("omp --version")
        acts.append(("sleep", 2.5))
        run_line("exit")
        acts.append(("sleep", 0.6))
    elif scenario == "help-tour":
        run_line("omp --help")
        acts.append(("sleep", 3.5))
        run_line("exit")
        acts.append(("sleep", 0.6))
    elif scenario == "tui-splash":
        # `omp --no-session` on a keyless CI runner opens the interactive onboarding
        # wizard (documented as an acceptable, honest capture in scenarios.md S3). It
        # traps SIGINT and has no reliable headless quit key, so we run it inside a
        # non-job-control `sh -c` (omp stays in the terminal's foreground group and
        # renders normally) with a watchdog that escalates INT -> TERM -> KILL. When
        # omp dies, `sh -c` returns to the interactive shell and termsvg saves the
        # cast (a hard-killed termsvg would save nothing).
        run_line(omp_watchdog(5), delay=0.02)
        acts.append(("sleep", 8.0))          # splash renders ~5s, watchdog then kills
        run_line("exit")
        acts.append(("sleep", 0.6))
    elif scenario == "typing-demo":
        run_line(omp_watchdog(9), delay=0.02)
        acts.append(("sleep", 3.5))          # let the TUI input box appear
        acts.append(("type", "explain what this repository does", 0.11))
        acts.append(("sleep", 4.0))          # keep the typed (unsent) text visible
        run_line("exit")                     # watchdog has killed omp by now (~11s)
        acts.append(("sleep", 0.6))
    else:
        raise SystemExit(f"drive.py: unknown scenario {scenario!r}")
    return acts


class Session:
    def __init__(self, master: int, pid: int):
        self.master = master
        self.pid = pid
        self.eof = False

    def drain(self, duration: float) -> None:
        """Read (and mirror) child output for `duration` seconds so the PTY
        never blocks on a full buffer, preserving scenario timing."""
        end = time.time() + duration
        while time.time() < end:
            if self.eof:
                time.sleep(min(0.05, max(0.0, end - time.time())))
                continue
            r, _, _ = select.select([self.master], [], [], 0.05)
            if not r:
                continue
            try:
                data = os.read(self.master, 65536)
            except OSError:
                self.eof = True
                continue
            if not data:
                self.eof = True
                continue
            os.write(sys.stdout.fileno(), data)

    def send(self, data: bytes) -> None:
        try:
            os.write(self.master, data)
        except OSError:
            self.eof = True

    def type_text(self, text: str, per_char: float) -> None:
        for ch in text:
            self.send(ch.encode())
            self.drain(per_char)

    def run(self, actions) -> None:
        for act in actions:
            if act[0] == "sleep":
                self.drain(act[1])
            elif act[0] == "type":
                self.type_text(act[1], act[2])
            elif act[0] == "key":
                self.send(act[1])
            if self._child_gone():
                return

    def _child_gone(self) -> bool:
        try:
            wpid, _ = os.waitpid(self.pid, os.WNOHANG)
        except ChildProcessError:
            return True
        return wpid != 0

    def wait(self, timeout: float) -> int:
        end = time.time() + timeout
        while time.time() < end:
            try:
                wpid, status = os.waitpid(self.pid, os.WNOHANG)
            except ChildProcessError:
                return 0
            if wpid != 0:
                if os.WIFEXITED(status):
                    return os.WEXITSTATUS(status)
                return 1
            self.drain(0.1)
        # Backstop: termsvg never returned (e.g. TUI would not quit). Kill it so
        # the workflow moves on; a missing/invalid cast becomes a broken verdict.
        try:
            os.kill(self.pid, signal.SIGKILL)
            os.waitpid(self.pid, 0)
        except OSError:
            pass
        return 124


def main() -> int:
    if len(sys.argv) != 5:
        raise SystemExit("usage: drive.py <cast-out> <shell> <scenario> <rec-subcommand>")
    cast_out, shell, scenario, rec = sys.argv[1:5]
    actions = build_actions(scenario)

    master, slave = os.openpty()
    fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack("HHHH", ROWS, COLS, 0, 0))

    pid = os.fork()
    if pid == 0:
        os.close(master)
        try:
            os.login_tty(slave)  # setsid + controlling tty + dup to 0/1/2
        except (AttributeError, OSError):
            os.setsid()
            for fd in (0, 1, 2):
                os.dup2(slave, fd)
            if slave > 2:
                os.close(slave)
        os.environ.setdefault("TERM", "xterm-256color")
        os.environ["SHELL"] = shell
        try:
            os.execvp("termsvg", ["termsvg", rec, "-c", shell, cast_out])
        except OSError as exc:  # pragma: no cover
            sys.stderr.write(f"exec termsvg failed: {exc}\n")
            os._exit(127)

    os.close(slave)

    def _on_alarm(_signo, _frame):
        try:
            os.kill(pid, signal.SIGKILL)
        except OSError:
            pass
        raise SystemExit("drive.py: hard time limit hit")

    signal.signal(signal.SIGALRM, _on_alarm)
    signal.alarm(HARD_LIMIT)

    sess = Session(master, pid)
    sess.run(actions)
    code = sess.wait(CHILD_GRACE)
    signal.alarm(0)
    sys.stdout.flush()
    print(f"\ndrive.py: termsvg exited with {code} (scenario={scenario})", file=sys.stderr)
    return 0 if code in (0, 124) else code


if __name__ == "__main__":
    raise SystemExit(main())
