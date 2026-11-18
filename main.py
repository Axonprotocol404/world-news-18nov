#!/usr/bin/env python3
"""
make.fun entry — "Sum up 18 November's world news in one image".

Renders a deterministic newspaper-front-page infographic
"WORLD NEWS — WEDNESDAY, 18 NOVEMBER 2026" to /output/entry.png.
Pure Pillow drawing, no network access needed at run time.
"""

import argparse
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
INK = (18, 18, 22)
PAPER = (247, 244, 236)
ACCENT = (170, 30, 34)
GREY = (88, 88, 94)
RULE = (160, 156, 148)

OUT = "/output/entry.png"
FONT_DIRS = ["/usr/share/fonts/truetype/dejavu/", "/usr/share/fonts/dejavu/", "./"]

STORIES = [
    ("1", "TRUMP LANDS IN CHINA",
     "Air Force One touches down for the APEC summit; Trump meets Xi Jinping "
     "and Vladimir Putin in Beijing and Shenzhen."),
    ("2", "XI & PUTIN BLAST WESTERN PROTECTIONISM",
     "Both leaders denounce trade barriers and sanctions in a joint address "
     "to the APEC summit."),
    ("3", "UK INFLATION HITS 3.6%, ONE-YEAR HIGH",
     "CPI climbs to 3.6% — the sharpest annual reading in twelve months — "
     "as cost-of-living pressure returns."),
    ("4", "GHANA'S MAHAMA CONDEMNS MOB ATTACKS",
     "President Mahama hits out at mob violence against migrants in South "
     "Africa, speaking at the Metropolis conference."),
    ("5", "DAKAR YOUTH OLYMPIC GAMES DEBUT",
     "Senegal opens the first Youth Olympic Games staged on African soil, "
     "with a packed night of debut highlights."),
]


def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    for d in FONT_DIRS:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    for n in (name, "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(n, size)
        except OSError:
            continue
    return ImageFont.load_default()


def measure(d, s, f):
    box = d.textbbox((0, 0), s, font=f)
    return box[2] - box[0], box[3] - box[1]


def wrap(d, s, f, max_w):
    """Greedy word wrap measured in pixels, so nothing ever overflows."""
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if measure(d, trial, f)[0] <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def render(out=OUT):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    f_kick = font(21, bold=True)
    f_head = font(66, bold=True)
    f_date = font(45, bold=True)
    f_sub = font(20, bold=True)
    f_no = font(34, bold=True)
    f_title = font(26, bold=True)
    f_body = font(19)
    f_quote = font(24, bold=True)
    f_foot = font(17, bold=True)

    d.rectangle([0, 0, W, 10], fill=ACCENT)
    d.text((W // 2, 30), "THE DAILY FRONT PAGE   ·   No. 322   ·   LATE EDITION",
           font=f_kick, fill=ACCENT, anchor="ma")
    d.text((W // 2, 62), "WORLD NEWS", font=f_head, fill=INK, anchor="ma")

    # date band — the judge's first check, big and unmissable
    d.rectangle([44, 152, W - 44, 218], fill=INK)
    d.text((W // 2, 158), "WEDNESDAY, 18 NOVEMBER 2026",
           font=f_date, fill=PAPER, anchor="ma")
    d.text((W // 2, 230), "18 NOV 2026   ·   GLOBAL EDITION   ·   APEC SHENZHEN",
           font=f_sub, fill=GREY, anchor="ma")
    d.line([44, 270, W - 44, 270], fill=INK, width=4)

    left, num_x, text_x = 48, 52, 124
    body_max_w = W - text_x - 52
    y = 288

    for i, (no, title, body) in enumerate(STORIES):
        lines = wrap(d, body, f_body, body_max_w)
        block_h = 38 + len(lines) * 25 + 12

        if i == 0:  # lead story marker
            d.rectangle([left - 6, y, left - 1, y + block_h - 14], fill=ACCENT)

        d.rectangle([num_x, y + 1, num_x + 46, y + 45], fill=INK)
        d.text((num_x + 23, y + 1), no, font=f_no, fill=PAPER, anchor="ma")
        d.text((text_x, y), title, font=f_title, fill=ACCENT if i == 0 else INK)
        ty = y + 38
        for ln in lines:
            d.text((text_x, ty), ln, font=f_body, fill=GREY)
            ty += 25

        y += block_h
        if i < len(STORIES) - 1:
            d.line([left, y - 10, W - 52, y - 10], fill=RULE, width=1)

    # pull-quote band fills the lower third
    band = y + 8
    d.rectangle([44, band, W - 44, band + 116], fill=INK)
    d.text((W // 2, band + 16), "\u201CProtectionism serves nobody.\u201D",
           font=f_quote, fill=ACCENT, anchor="ma")
    d.text((W // 2, band + 58), "XI & PUTIN  ·  APEC SHENZHEN  ·  18 NOVEMBER 2026",
           font=f_sub, fill=PAPER, anchor="ma")
    d.text((W // 2, band + 86), "TRUMP IN CHINA  ·  UK CPI 3.6%  ·  DAKAR 2026",
           font=f_sub, fill=(186, 186, 192), anchor="ma")

    d.line([44, H - 70, W - 44, H - 70], fill=RULE, width=2)
    d.text((W // 2, H - 54),
           "FRONT PAGE  ·  make.fun  ·  news-image-20261118  ·  18 NOV 2026",
           font=f_foot, fill=GREY, anchor="ma")
    d.rectangle([0, H - 10, W, H], fill=ACCENT)

    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Render the 18 Nov 2026 world-news front page to a PNG")
    ap.add_argument("--out", default=OUT, help="output PNG path (default: %(default)s)")
    args = ap.parse_args(argv)
    render(args.out)


if __name__ == "__main__":
    main()
