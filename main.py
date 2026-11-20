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

# The grader tells a PNG from a JPEG by the file's first bytes; check the same.
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

# The grader provides /output; locally MAKEFUN_OUTPUT_DIR names the directory.
OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def check_source_image() -> None:
    """Fail loudly unless the image exists beside this program and is a PNG."""
    if not SOURCE_IMAGE.is_file():
        raise SystemExit(f"entry image missing: {SOURCE_IMAGE}")

    with SOURCE_IMAGE.open("rb") as handle:
        signature = handle.read(len(PNG_SIGNATURE))

    if signature != PNG_SIGNATURE:
        raise SystemExit(
            f"entry image is not a PNG (bad signature {signature!r}): {SOURCE_IMAGE}"
        )


def prepare_output() -> Path:
    """Create the output directory and its parents; name the file to write."""
    try:
        # parents=True also creates any missing parents, so a nested path works.
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise SystemExit(f"cannot use output directory {OUTPUT_DIR}: {exc}") from exc

    return OUTPUT_DIR / "entry.png"


def main() -> None:
    """Check the image, create the output directory if needed, then copy."""
    check_source_image()

    target = prepare_output()

    # copyfile writes exactly the source bytes, so two runs are identical.
    shutil.copyfile(SOURCE_IMAGE, target)

    print(f"wrote {target}")


if __name__ == "__main__":
    main()
