"""Copy this repository's entry.png to the grader's output directory.

The entry for make.fun's news-image-20261120 competition is a finished
1024 x 1024 PNG, entry.png, stored beside this program at the repository
root.  The grader runs this program twice in a fresh container with no
network, the repository mounted read-only at /bot and a writable /output,
and both runs must write the same bytes.

Outside the grader the environment variable MAKEFUN_OUTPUT_DIR stands in
for /output, so the program can be run locally:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

The image is already final, so the program only copies its bytes: it never
decodes or re-encodes the PNG, which keeps every run deterministic.
"""

import os
import shutil
from pathlib import Path

# The image sits next to this program, wherever the repository is mounted.
SOURCE_IMAGE = Path(__file__).resolve().parent / "entry.png"

# The grader provides /output; locally MAKEFUN_OUTPUT_DIR names the directory.
OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main() -> None:
    """Create the output directory if needed, then copy the image into it."""
    # parents=True also creates any missing parents, so a nested path works.
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # copyfile writes exactly the source bytes, so two runs are identical.
    shutil.copyfile(SOURCE_IMAGE, OUTPUT_DIR / "entry.png")


if __name__ == "__main__":
    main()
