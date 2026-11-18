# News-image entry: "The World Today — 17 November 2026".
# The program copies the front-page image held in this repository to
# /output/entry.png. The image is a whole JPEG (named entry.png, as the
# rules allow) of 1024x1024 pixels, well under the 1 MiB limit.
# It runs with no network and writes the same bytes on every run.
import os
import shutil

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
OUT = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
shutil.copyfile(SRC, OUT)

# The grader runs the program twice and both runs must write the same
# bytes: a copy is byte-identical by construction, so verify it.
assert os.path.getsize(SRC) == os.path.getsize(OUT), "copy size mismatch"
with open(SRC, "rb") as f, open(OUT, "rb") as g:
    assert f.read() == g.read(), "copy bytes mismatch"
