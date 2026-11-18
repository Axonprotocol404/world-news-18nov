#!/usr/bin/env python3
"""
make.fun entry — "Sum up 18 November's world news in one image".

The finished image is committed in this repo as entry.png (1024x1024 PNG).
This script does exactly one thing: copy the committed image to the
grader's expected output path /output/entry.png.

Standard library only — no Pillow, no network access.
"""

import os
import shutil

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
PRIMARY = "/output/entry.png"
FALLBACK = os.path.join(os.getcwd(), "output", "entry.png")


def copy_entry():
    for dest in (PRIMARY, FALLBACK):
        try:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copyfile(SRC, dest)
            print("copied", SRC, "->", dest,
                  os.path.getsize(dest), "bytes")
            return dest
        except OSError as exc:
            print("could not write", dest, ":", exc)
    raise SystemExit("failed to copy entry.png")


def main():
    if not os.path.isfile(SRC):
        raise SystemExit("entry.png not found next to main.py")
    copy_entry()
    print("done")
    return 0


if __name__ == "__main__":
    main()
