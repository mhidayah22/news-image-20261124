#!/usr/bin/env python3
"""Reproduce the 24 November 2026 front page (entry.png).

Stdlib only. Copies the bundled entry.png to the destination the
grader expects: an explicit output path first, then
MAKEFUN_OUTPUT_DIR, then /output when it exists, and finally the
current directory. The source is the entry.png shipped next to this
file (falling back to the working directory). No network, no
arguments required; running twice produces identical bytes.
"""
import hashlib
import os
import shutil
import sys
from pathlib import Path

NAME = "entry.png"


def find_source():
    here = Path(__file__).resolve().parent
    for cand in (here / NAME, Path.cwd() / NAME):
        if cand.is_file():
            return cand
    raise SystemExit("entry.png not found next to main.py or in the cwd")


def destination():
    if len(sys.argv) > 1:
        target = Path(sys.argv[1])
        if target.suffix.lower() in (".png", ".jpg", ".jpeg"):
            return target
        return target / NAME
    env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env:
        return Path(env) / NAME
    if Path("/output").is_dir():
        return Path("/output") / NAME
    return Path.cwd() / NAME


def main():
    src = find_source()
    dest = destination()
    if src.resolve() == dest.resolve():
        # Already in place (e.g. run inside the repo dir with no
        # output directory set): nothing to copy, still a success.
        digest = hashlib.sha256(src.read_bytes()).hexdigest()
        print(f"entry.png already at {dest} "
              f"({src.stat().st_size} bytes) sha256 {digest}")
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)
    digest = hashlib.sha256(dest.read_bytes()).hexdigest()
    print(f"wrote {dest} ({dest.stat().st_size} bytes) sha256 {digest}")


if __name__ == "__main__":
    main()
