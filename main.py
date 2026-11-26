"""news-image-20261126 entrypoint (Python 3.13, standard library only).

The finished front page ships in this repository as entry.png; this program
just copies it to the grader's output directory, so both grader runs write
byte-identical output. The image itself was drawn by render.py (Pillow,
build-time only) from the verified news of Thursday 26 November 2026.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
SOURCE = HERE / "entry.png"

if not SOURCE.is_file():
    raise SystemExit(f"entry.png missing next to {__file__}")

OUT.mkdir(parents=True, exist_ok=True)
shutil.copyfile(SOURCE, OUT / "entry.png")
if (OUT / "entry.png").stat().st_size != SOURCE.stat().st_size:
    raise SystemExit("entry.png copy is incomplete")
