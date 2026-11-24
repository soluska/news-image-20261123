#!/usr/bin/env python3
"""Draw entry.png for make.fun news-image-20261123.

A newspaper front page for Monday 23 November 2026, painted entirely
with PIL primitives (rectangles, ellipses, lines, polygons and text).
No AI image generation, no downloaded pictures, no network. Run:

    python3 draw.py

Writes entry.png (1024 x 1024, well under 1 MiB) next to this file.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 26
PAPER = (247, 243, 232)
INK = (17, 17, 17)
RED = (176, 0, 32)
GREY = (90, 88, 82)
LIGHT_LINE = (205, 198, 182)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def draw_chip(d, cx, cy, s):
    """Lead icon: a microchip with a rising arrow."""
    d.rounded_rectangle([cx - s, cy - s, cx + s, cy + s], radius=10,
                        outline=(34, 120, 60), width=6)
    d.rectangle([cx - s * 0.45, cy - s * 0.45, cx + s * 0.45, cy + s * 0.45],
                fill=(34, 120, 60))
    for k in (-1, 0, 1):
        d.line([cx + k * s * 0.55, cy - s - 14, cx + k * s * 0.55, cy - s],
               fill=(34, 120, 60), width=5)
        d.line([cx - s - 14, cy + k * s * 0.55, cx - s, cy + k * s * 0.55],
               fill=(34, 120, 60), width=5)
    pts = [(cx - s * 0.9, cy + s * 0.75), (cx - s * 0.25, cy + s * 0.1),
           (cx + s * 0.15, cy + s * 0.45), (cx + s * 0.9, cy - s * 0.55)]
    d.line(pts, fill=(176, 0, 32), width=7, joint="curve")
    d.polygon([(cx + s * 0.9, cy - s * 0.55), (cx + s * 0.55, cy - s * 0.55),
               (cx + s * 0.9, cy - s * 0.2)], fill=(176, 0, 32))


def draw_globe(d, cx, cy, r):
    """Cracked globe for the climate panel."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(30, 90, 140), width=5)
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(30, 90, 140), width=4)
    d.line([cx - r, cy, cx + r, cy], fill=(30, 90, 140), width=3)
    d.line([cx, cy - r, cx, cy + r], fill=(30, 90, 140), width=3)
    crack = [(cx - 6, cy - r + 4), (cx + 8, cy - r * 0.4), (cx - 4, cy),
             (cx + 10, cy + r * 0.4), (cx - 2, cy + r - 4)]
    d.line(crack, fill=(176, 0, 32), width=5, joint="curve")


def draw_ship(d, cx, cy, s):
    """Warship with a blast for the Libya panel."""
    d.polygon([(cx - s, cy + s * 0.35), (cx + s, cy + s * 0.35),
               (cx + s * 0.75, cy + s * 0.7), (cx - s * 0.75, cy + s * 0.7)],
              fill=(40, 60, 90))
    d.rectangle([cx - s * 0.45, cy - s * 0.15, cx + s * 0.3, cy + s * 0.35],
                fill=(40, 60, 90))
    d.line([cx + s * 0.1, cy - s * 0.75, cx + s * 0.1, cy - s * 0.15],
           fill=(40, 60, 90), width=5)
    for i, (dx, dy, r) in enumerate([(-14, -34, 12), (6, -42, 15), (24, -26, 10)]):
        d.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r],
                  fill=(230, 120, 30) if i % 2 == 0 else (240, 200, 40))
    d.line([cx - s - 6, cy + s * 0.85, cx + s + 6, cy + s * 0.85],
           fill=(60, 120, 170), width=4)


def draw_flats(d, cx, cy, s):
    """Damaged block of flats for the Dymer panel."""
    d.rectangle([cx - s, cy - s * 0.7, cx - s * 0.08, cy + s * 0.7],
                outline=(70, 70, 70), width=4)
    d.polygon([(cx - s * 0.08, cy - s * 0.7), (cx + s * 0.8, cy - s * 0.7),
               (cx + s * 0.8, cy + s * 0.7), (cx + s * 0.1, cy + s * 0.7),
               (cx - s * 0.08, cy + s * 0.2)], fill=(200, 190, 170),
              outline=(70, 70, 70))
    for wy in (-0.45, 0.0, 0.45):
        for wx in (-0.7, -0.35):
            d.rectangle([cx + wx * s - 7, cy + wy * s - 7,
                         cx + wx * s + 7, cy + wy * s + 7],
                        fill=(250, 220, 90))
    d.line([(cx + s * 0.15, cy - s * 0.7), (cx + s * 0.45, cy - s * 0.2),
            (cx + s * 0.2, cy + s * 0.2)], fill=(176, 0, 32), width=4)


def draw_mountain(d, cx, cy, s):
    """Glacier mountain and flood wave for the Nepal panel."""
    d.polygon([(cx - s, cy + s * 0.7), (cx - s * 0.15, cy - s * 0.8),
               (cx + s * 0.7, cy + s * 0.7)], fill=(90, 110, 140))
    d.polygon([(cx - s * 0.15, cy - s * 0.8), (cx + s * 0.05, cy - s * 0.45),
               (cx - s * 0.1, cy - s * 0.3), (cx - s * 0.3, cy - s * 0.5)],
              fill=(255, 255, 255))
    d.arc([cx - s, cy + s * 0.35, cx - s * 0.2, cy + s * 1.0], 0, 180,
          fill=(40, 110, 180), width=5)
    d.arc([cx - s * 0.1, cy + s * 0.45, cx + s * 0.8, cy + s * 1.1], 0, 180,
          fill=(40, 110, 180), width=5)


def draw_ballot(d, cx, cy, s):
    """Ballot box for the US politics panel."""
    d.rectangle([cx - s * 0.8, cy - s * 0.1, cx + s * 0.8, cy + s * 0.8],
                outline=(30, 60, 130), width=5)
    d.rectangle([cx - s * 0.25, cy - s * 0.55, cx + s * 0.25, cy - s * 0.1],
                fill=(255, 255, 255), outline=(30, 60, 130), width=4)
    d.line([cx - s * 0.8, cy + s * 0.35, cx + s * 0.8, cy + s * 0.35],
           fill=(30, 60, 130), width=4)
    d.ellipse([cx - s * 0.45, cy + s * 0.45, cx - s * 0.15, cy + s * 0.65],
              fill=(176, 0, 32))
    d.ellipse([cx + s * 0.15, cy + s * 0.45, cx + s * 0.45, cy + s * 0.65],
              fill=(176, 0, 32))


def draw_ball(d, cx, cy, r):
    """Football for the sport panel."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(17, 17, 17), width=5,
              fill=(255, 255, 255))
    d.polygon([(cx, cy - r * 0.35), (cx + r * 0.33, cy - r * 0.1),
               (cx + r * 0.2, cy + r * 0.28), (cx - r * 0.2, cy + r * 0.28),
               (cx - r * 0.33, cy - r * 0.1)], fill=(17, 17, 17))
    for ang in (90, 210, 330):
        import math
        x2 = cx + r * 0.95 * math.cos(math.radians(ang))
        y2 = cy - r * 0.95 * math.sin(math.radians(ang))
        d.line([cx, cy, x2, y2], fill=(17, 17, 17), width=3)


ICONS = {
    "chip": draw_chip, "globe": draw_globe, "ship": draw_ship,
    "flats": draw_flats, "mountain": draw_mountain, "ballot": draw_ballot,
    "ball": draw_ball,
}


def mini_icon(d, kind, cx, cy, r, color):
    """Tiny white glyph drawn inside a panel's kicker strip."""
    if kind == "globe":
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=3)
        d.line([cx - r, cy, cx + r, cy], fill=color, width=2)
        d.line([cx, cy - r, cx, cy + r], fill=color, width=2)
    elif kind == "ship":
        d.polygon([(cx - r, cy + r * 0.4), (cx + r, cy + r * 0.4),
                   (cx + r * 0.7, cy + r * 0.8), (cx - r * 0.7, cy + r * 0.8)],
                  fill=color)
        d.line([cx, cy - r, cx, cy + r * 0.4], fill=color, width=3)
    elif kind == "flats":
        d.rectangle([cx - r, cy - r, cx - 2, cy + r], outline=color, width=3)
        d.rectangle([cx + 2, cy - r * 0.5, cx + r, cy + r], outline=color,
                    width=3)
    elif kind == "mountain":
        d.polygon([(cx - r, cy + r), (cx, cy - r), (cx + r, cy + r)],
                  outline=color, width=3)
    elif kind == "ballot":
        d.rectangle([cx - r, cy - r * 0.3, cx + r, cy + r], outline=color,
                    width=3)
        d.line([cx - r * 0.4, cy - r, cx + r * 0.4, cy - r * 0.3],
               fill=color, width=3)
    elif kind == "ball":
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=3)
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=color)


PANELS = [
    dict(kicker="CLIMATE", color=(30, 90, 140), icon="globe",
         head="COP31 ENDS WITH NO DEAL",
         sub="Longest summit ever collapses in Antalya; the draft drops "
             "fossil fuels \u2014 EU: \u201cworst COP ever\u201d."),
    dict(kicker="CONFLICT", color=(120, 30, 30), icon="ship",
         head="UKRAINE SINKS RUSSIAN WARSHIP IN LIBYA",
         sub="Seven sea drones sink the corvette Merkury at Benghazi; the "
             "cargo ship Angara is hit too."),
    dict(kicker="UKRAINE", color=(90, 70, 10), icon="flats",
         head="DYMER TOLL RISES TO 11",
         sub="A boy, 7, and a woman, 79, are pulled alive from the rubble; "
             "the region marks a day of mourning."),
    dict(kicker="ASIA", color=(20, 110, 90), icon="mountain",
         head="INDIA PLEDGES $1.6BN TO NEPAL",
         sub="Package after August\u2019s glacier flood killed about 1,500: "
             "a $377m grant and a $1.24bn energy credit."),
    dict(kicker="POLITICS", color=(30, 60, 130), icon="ballot",
         head="DEMOCRATS TAKE BIGGEST HOUSE MAJORITY SINCE 1992",
         sub="At least 258 seats after a North Carolina flip \u2014 the "
             "largest Democratic majority in 34 years."),
    dict(kicker="SPORT", color=(34, 120, 60), icon="ball",
         head="BRENTFORD HIT EVERTON FOR FOUR",
         sub="Lewis-Potter scores twice as 10-man Everton sink 4-0; "
             "Brentford climb into the top six."),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN

    # --- masthead ------------------------------------------------------
    d.line([x0, 28, x1, 28], fill=INK, width=3)
    mast = font(SERIF, 58)
    d.text(((W - d.textlength("THE WORLD IN ONE DAY", font=mast)) / 2, 36),
           "THE WORLD IN ONE DAY", font=mast, fill=INK)
    tag = font(SANS, 19)
    tagline = "One day \u00b7 Seven stories \u00b7 The world, in a single page"
    d.text(((W - d.textlength(tagline, font=tag)) / 2, 106),
           tagline, font=tag, fill=GREY)
    d.line([x0, 136, x1, 136], fill=INK, width=2)

    # --- red date band --------------------------------------------------
    d.rectangle([x0, 146, x1, 192], fill=RED)
    band = font(SANS_B, 32)
    band_txt = "MONDAY \u00b7 23 NOVEMBER 2026"
    d.text(((W - d.textlength(band_txt, font=band)) / 2, 152),
           band_txt, font=band, fill=(255, 255, 255))

    # --- lead story ------------------------------------------------------
    ly, lh = 204, 256
    d.rectangle([x0, ly, x1, ly + lh], outline=INK, width=3)
    d.rectangle([x0, ly, x1, ly + 34], fill=(34, 120, 60))
    kick = font(SANS_B, 20)
    d.text((x0 + 14, ly + 5), "MARKETS \u00b7 LEAD", font=kick,
           fill=(255, 255, 255))
    lead_head = font(SERIF, 44)
    lead_sub = font(SANS, 21)
    hx, hw = x0 + 16, 700
    head_lines = wrap(d, "HUANG IS BACK \u2014 NVIDIA SOARS 33%",
                      lead_head, hw)
    y = text_block(d, hx, ly + 46, head_lines, lead_head, INK, 52)
    sub_lines = wrap(d, "The board reinstates Jensen Huang as chief "
                        "executive 11 days after he quit; the Nasdaq jumps "
                        "6% and the S&P 500 4% as the AI sell-off reverses.",
                     lead_sub, hw)
    text_block(d, hx, y + 8, sub_lines, lead_sub, (45, 45, 45), 28)
    draw_chip(d, x1 - 95, ly + 150, 50)
    d.text((x1 - 165, ly + 214), "NVDA +33%", font=font(SANS_B, 22),
           fill=(34, 120, 60))

    # --- six story panels, 2 columns x 3 rows ---------------------------
    gap = 14
    col_w = (x1 - x0 - gap) // 2
    row_h = 160
    gy = ly + lh + gap
    head_f = font(SANS_B, 25)
    sub_f = font(SANS, 17)
    for i, p in enumerate(PANELS):
        px = x0 + (i % 2) * (col_w + gap)
        py = gy + (i // 2) * (row_h + gap)
        d.rectangle([px, py, px + col_w, py + row_h], outline=INK, width=2)
        d.rectangle([px, py, px + col_w, py + 30], fill=p["color"])
        d.text((px + 12, py + 4), p["kicker"], font=font(SANS_B, 18),
               fill=(255, 255, 255))
        mini_icon(d, p["icon"], px + col_w - 24, py + 15, 10,
                  (255, 255, 255))
        tw = col_w - 24
        hl = wrap(d, p["head"], head_f, tw)
        y = text_block(d, px + 12, py + 40, hl[:2], head_f, INK, 29)
        sl = wrap(d, p["sub"], sub_f, tw)
        text_block(d, px + 12, y + 4, sl[:2], sub_f, (55, 55, 55), 21)

    # --- footer ----------------------------------------------------------
    fy = gy + 3 * row_h + 2 * gap + 8
    d.line([x0, fy, x1, fy], fill=LIGHT_LINE, width=2)
    foot = font(SANS, 15)
    d.text((x0, fy + 8), "Sources: Reuters \u00b7 CNN \u00b7 AP \u00b7 Al Jazeera "
           "\u00b7 Sky Sports", font=foot, fill=GREY)
    d.text((x1 - d.textlength("23 NOVEMBER 2026", font=foot), fy + 8),
           "23 NOVEMBER 2026", font=foot, fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
