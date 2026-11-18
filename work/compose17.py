#!/usr/bin/env python3
"""Compose the 17 Nov 2026 news front page (1024x1024) from three AI-rendered
photo panels. Text is drawn with PIL so every letter is crisp and legible."""
import os
from PIL import Image, ImageDraw, ImageFont

W = os.path.dirname(os.path.abspath(__file__))
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

PAPER = (247, 243, 234)
NAVY = (20, 33, 61)
GOLD = (201, 162, 39)
INK = (24, 24, 24)
RED = (178, 34, 34)

canvas = Image.new("RGB", (1024, 1024), PAPER)
d = ImageDraw.Draw(canvas, "RGBA")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def cover(path, tw, th):
    im = Image.open(path).convert("RGB")
    iw, ih = im.size
    s = max(tw / iw, th / ih)
    im = im.resize((round(iw * s), round(ih * s)), Image.LANCZOS)
    x = (im.width - tw) // 2
    y = (im.height - th) // 2
    return im.crop((x, y, x + tw, y + th))


def caption_bar(x, y, w, h, head, sub, head_size=30, sub_size=20):
    d.rectangle([x, y, x + w, y + h], fill=(0, 0, 0, 205))
    hf, sf = font(SANS_B, head_size), font(SANS, sub_size)
    hl = wrap(d, head, hf, w - 28)
    sl = wrap(d, sub, sf, w - 28)
    ty = y + 10
    for line in hl:
        d.text((x + 14, ty), line, font=hf, fill=(255, 255, 255))
        ty += head_size + 4
    for line in sl:
        d.text((x + 14, ty), line, font=sf, fill=(225, 225, 225))
        ty += sub_size + 3


# --- Masthead ---
d.rectangle([0, 0, 1024, 118], fill=NAVY)
d.rectangle([0, 118, 1024, 122], fill=GOLD)
mf = font(SERIF_B, 62)
t = "THE WORLD TODAY"
d.text(((1024 - d.textlength(t, font=mf)) / 2, 12), t, font=mf, fill=(255, 255, 255))
df = font(SANS_B, 25)
t2 = "TUESDAY  ·  17 NOVEMBER 2026"
d.text(((1024 - d.textlength(t2, font=df)) / 2, 80), t2, font=df, fill=GOLD)

# --- Lead photo: Kerch Bridge ---
lead = cover(os.path.join(W, "media-generation-news17-kerch-bridge-0-f4c0df0d-67cf-48c4-8906-2e354790586a.webp"), 992, 470)
canvas.paste(lead, (16, 134))
d.rectangle([16, 134, 1008, 138], fill=RED)
caption_bar(16, 508, 992, 96, "KERCH BRIDGE COLLAPSES IN UKRAINE STRIKE",
            "Road span to Crimea falls; Russian missiles hit Kyiv bridges in return",
            head_size=33, sub_size=21)

# --- Second row: Hormuz + Manila ---
left = cover(os.path.join(W, "media-generation-news17-hormuz-tanker-0-dc05d7a4-d096-4fad-9f23-20aace80780f.webp"), 488, 258)
canvas.paste(left, (16, 620))
caption_bar(16, 790, 488, 88, "TANKERS HIT IN HORMUZ",
            "Iran: mines hit two tankers; 3rd US carrier arrives", head_size=26, sub_size=18)

right = cover(os.path.join(W, "media-generation-news17-manila-summit-0-44e5cade-925c-47b5-9a3e-6c8f2c029dfd.webp"), 488, 258)
canvas.paste(right, (520, 620))
caption_bar(520, 790, 488, 88, "TRUMP IN MANILA",
            "ASEAN summit opens Asia tour; trade pact signed", head_size=26, sub_size=18)

# --- Footer: also today ---
d.rectangle([16, 896, 1008, 898], fill=(120, 110, 90))
ff = font(SANS_B, 19)
d.text((16, 906), "ALSO TODAY", font=ff, fill=RED)
fl = font(SANS, 19)
lines = [
    "Nvidia reports after the bell  •  ULA Vulcan fails — 40 Amazon satellites lost",
    "JPMorgan blames software bug for outage  •  UK sanctions Israeli settlement firms",
    "Pentagon fails audit for a 9th year  •  Japan protests Russian jets in its airspace",
]
y = 934
for line in lines:
    d.text((16, y), line, font=fl, fill=INK)
    y += 26

out = os.path.join(os.path.dirname(W), "entry.png")
canvas.convert("RGB").save(out, "JPEG", quality=92)
print("saved", out, os.path.getsize(out), "bytes")
