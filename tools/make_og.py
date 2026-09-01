"""Compose the social share card.

Run:  python tools/make_og.py

Two layers, deliberately split by what each medium is good at.

The plate (assets/og-plate.png, not served) is generated art: the navy field, the
grid, the aurora glow and the wordmark itself. Generation is excellent at
that and it is what gives the card its depth.

Everything a marketer needs the card to *say* — the headline, the proof
numbers, the offer, the URL — is drawn here in real Manrope at exact brand
colours. Text is the one thing an image model cannot be trusted with: a
misspelt wordmark or a wrong number is unshippable, and a share card is
copy first and art second.

Output is 1200x630 (the ratio every platform crops to) rendered at 2x and
downsampled, so the type stays crisp on retina timelines.
"""

import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLATE = os.path.join(ROOT, "assets", "og-plate.png")
FONT = os.path.join(ROOT, "static", "fonts", "Manrope.ttf")
OUT = os.path.join(ROOT, "static", "images", "og-card.png")

W, H = 2400, 1260          # 2x the 1200x630 target
MARGIN = 384               # aligns with the wordmark's left edge in the plate

INK = (255, 255, 255)
DIM = (150, 176, 211)
TEAL = (94, 234, 212)

HEADLINE = ["Learn Python by writing it,", "not watching it."]
PROOF = "55 lessons  ·  9 projects  ·  18 challenges"
OFFER = "Free. Runs in your browser. Nothing to install."
URL = "learnwithpython.com"


def font(size, weight="Bold"):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f


def build():
    plate = Image.open(PLATE).convert("RGB")
    pw, ph = plate.size

    # Crop to 1.91:1 from the bottom. The wordmark sits at ~38% height, so
    # trimming the bottom keeps it in the upper third and leaves the clean
    # lower band the copy needs.
    target_h = int(pw / (W / H))
    if target_h <= ph:
        plate = plate.crop((0, 0, pw, target_h))
    card = plate.resize((W, H), Image.LANCZOS)

    # Damp the copy band so white type sits on a predictable value rather
    # than on whatever the glow happened to do there. The ramp starts below
    # the wordmark: a plain top-to-bottom gradient greys out the logo, which
    # is the one element that has to stay at full strength.
    shade = Image.new("RGB", (W, H), (7, 21, 47))
    ramp = Image.new("L", (1, H))
    start = int(H * 0.52)
    for y in range(H):
        t = 0.0 if y < start else (y - start) / float(H - start)
        ramp.putpixel((0, y), int(255 * 0.5 * (t ** 1.4)))
    card = Image.composite(shade, card, ramp.resize((W, H)))

    d = ImageDraw.Draw(card)

    f_head = font(104, "ExtraBold")
    f_proof = font(46, "Bold")
    f_offer = font(42, "Medium")
    f_url = font(44, "ExtraBold")

    y = 660
    for line in HEADLINE:
        d.text((MARGIN, y), line, font=f_head, fill=INK)
        y += 116

    y += 26
    d.text((MARGIN, y), PROOF, font=f_proof, fill=TEAL)
    y += 74
    d.text((MARGIN, y), OFFER, font=f_offer, fill=DIM)

    # URL anchored bottom-right, the way a poster signs itself.
    bbox = d.textbbox((0, 0), URL, font=f_url)
    d.text((W - MARGIN - (bbox[2] - bbox[0]), H - 150), URL, font=f_url, fill=INK)

    card.resize((W // 2, H // 2), Image.LANCZOS).save(OUT, optimize=True)
    print("wrote %s (%dx%d, %d KB)"
          % (OUT, W // 2, H // 2, os.path.getsize(OUT) // 1024))


if __name__ == "__main__":
    build()
