#!/usr/bin/env python3
"""Guard against false passes (FR-007): every required GIF must exist, be non-empty,
and carry GIF magic bytes. Usage: python scripts/validate_gif.py <glob> [<glob> ...]"""
import glob
import os
import sys


def is_gif(path: str) -> bool:
    if os.path.getsize(path) == 0:
        return False
    with open(path, "rb") as fh:
        return fh.read(6) in (b"GIF87a", b"GIF89a")


def main(argv: list[str]) -> int:
    paths: list[str] = []
    for pattern in argv:
        paths.extend(sorted(glob.glob(pattern)))
    if not paths:
        print(f"validate_gif: no files matched {argv}", file=sys.stderr)
        return 1
    bad = [p for p in paths if not is_gif(p)]
    if bad:
        print("validate_gif: invalid/empty GIF(s): " + ", ".join(bad), file=sys.stderr)
        return 1
    print(f"validate_gif: OK ({len(paths)} valid GIF(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
