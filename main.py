#!/usr/bin/env python3
"""Reproduce entry.png for the 24 November 2026 front page.

Stdlib only, no network, no randomness. The finished page artwork
lives in entry.png next to this file; this program writes those exact
bytes out again, so every run produces an identical file.

Usage:
    python3 main.py            # rewrite entry.png in place
    python3 main.py out.png    # write the same bytes to out.png
"""
import hashlib
import pathlib
import sys

SOURCE = pathlib.Path(__file__).with_name("entry.png")


def build(target):
    data = SOURCE.read_bytes()
    target.write_bytes(data)
    written = target.read_bytes()
    assert written == data, "round-trip mismatch"
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {target} ({len(data)} bytes, sha256 {digest})")
    return digest


def main(argv):
    target = pathlib.Path(argv[1]) if len(argv) > 1 else pathlib.Path("entry.png")
    build(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
