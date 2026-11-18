# News-image entry: "The World Today — 17 November 2026".
# The program copies the front-page image held in this repository to
# /output/entry.png. The image is a whole JPEG (named entry.png, as the
# rules allow) of 1024x1024 pixels, well under the 1 MiB limit.
# It runs with no network and writes the same bytes on every run.
# Before finishing, it verifies the output with the standard library
# only: JPEG magic bytes, dimensions read from the JPEG header, and
# the 1 MiB size cap.
import os
import shutil

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
OUT = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")
MAX_BYTES = 1048576
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def jpeg_dimensions(data):
    """Return (width, height) read from the JPEG SOF marker, or None.

    Walks the marker segments after SOI until a Start Of Frame marker
    (SOF0/SOF1/SOF2) is found; its payload holds precision, height,
    then width. Standalone markers (RSTn, TEM, SOI) carry no length.
    """
    if len(data) < 4 or data[0] != 0xFF or data[1] != 0xD8:
        return None
    pos = 2
    while pos + 4 <= len(data):
        if data[pos] != 0xFF:
            return None
        marker = data[pos + 1]
        # Skip padding 0xFF bytes and standalone markers.
        if marker == 0xFF:
            pos += 1
            continue
        if marker == 0x01 or 0xD0 <= marker <= 0xD9:
            pos += 2
            continue
        seg_len = (data[pos + 2] << 8) | data[pos + 3]
        if seg_len < 2 or pos + 2 + seg_len > len(data):
            return None
        if marker in (0xC0, 0xC1, 0xC2):  # SOF0, SOF1, SOF2
            # SOF payload: 1 byte precision + 2 height + 2 width.
            if seg_len < 7:
                return None
            height = (data[pos + 5] << 8) | data[pos + 6]
            width = (data[pos + 7] << 8) | data[pos + 8]
            return width, height
        pos += 2 + seg_len
    return None


def verify_jpeg(path):
    """Assert the file at path is one whole, valid JPEG of the right size."""
    with open(path, "rb") as f:
        data = f.read()
    assert len(data) <= MAX_BYTES, (
        "output too large: %d bytes > %d" % (len(data), MAX_BYTES)
    )
    assert len(data) >= 4, "output too short to be a JPEG"
    assert data[0] == 0xFF and data[1] == 0xD8, "missing JPEG SOI marker"
    assert data[-2] == 0xFF and data[-1] == 0xD9, "missing JPEG EOI marker"
    dims = jpeg_dimensions(data)
    assert dims is not None, "no JPEG SOF marker found"
    assert dims == (EXPECTED_WIDTH, EXPECTED_HEIGHT), (
        "unexpected dimensions: %dx%d, expected %dx%d"
        % (dims[0], dims[1], EXPECTED_WIDTH, EXPECTED_HEIGHT)
    )
    return dims


verify_jpeg(SRC)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
shutil.copyfile(SRC, OUT)

# The grader runs the program twice and both runs must write the same
# bytes: a copy is byte-identical by construction, so verify it.
assert os.path.getsize(SRC) == os.path.getsize(OUT), "copy size mismatch"
with open(SRC, "rb") as f, open(OUT, "rb") as g:
    assert f.read() == g.read(), "copy bytes mismatch"

verify_jpeg(OUT)
print("OK: entry.png is a valid %dx%d JPEG, %d bytes"
      % (EXPECTED_WIDTH, EXPECTED_HEIGHT, os.path.getsize(OUT)))
