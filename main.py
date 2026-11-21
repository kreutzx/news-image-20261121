# Entry point for the news-image-20261121 entry.
# The front page is rendered at build time by build.py (see stories.py
# for the story database and art.py for the drawings) and committed as
# entry.png; this program validates that file and copies it to the
# output directory, byte for byte, so both grading runs agree.
# Standard library only; no network.

import os
import sys

MAX_BYTES = 1048576
MAX_SIDE = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"


def png_size(data):
    # IHDR follows the 8-byte signature: length(4) type(4) then w, h.
    if len(data) < 24 or not data.startswith(PNG_MAGIC):
        return None
    w = int.from_bytes(data[16:20], "big")
    h = int.from_bytes(data[20:24], "big")
    return w, h


def check_image(data):
    if len(data) > MAX_BYTES:
        raise SystemExit(f"entry.png is {len(data)} bytes, over the cap")
    if data.startswith(PNG_MAGIC):
        size = png_size(data)
        if size is None or size[0] > MAX_SIDE or size[1] > MAX_SIDE:
            raise SystemExit(f"bad PNG size: {size}")
    elif not data.startswith(JPEG_MAGIC):
        raise SystemExit("entry.png is neither PNG nor JPEG")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    with open(src, "rb") as fh:
        data = fh.read()
    check_image(data)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as fh:
        fh.write(data)
    print(f"wrote {dst} ({len(data)} bytes)")


if __name__ == "__main__":
    sys.exit(main())
