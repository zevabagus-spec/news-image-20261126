"""Draw the news-image-20261126 front page (build-time script, Pillow only).

Renders entry.png: a one-page newspaper front page summing up the world
news of Thursday 26 November 2026. Every story on the page was checked
against reporting dated 26 November 2026 (Reuters, KCNA via Reuters, Bank of
Korea, AP/CNN round-ups); stories that broke on earlier days were left out.

    python3 render.py            # writes entry.png next to this file

Layout (1024 x 1024): masthead naming the day, one lead story, a 2 x 3 grid
of stories across regions and fields, and an "Also on the day" strip. Flat
colours and real rendered text only, so the page stays legible at 300 px
across and the PNG stays far under the 1 MiB cap.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1024, 1024

PAPER = (248, 244, 236)
CARD = (255, 253, 246)
INK = (22, 22, 22)
MUTED = (90, 86, 76)
NAVY = (22, 50, 79)
RED = (176, 42, 42)
GOLD = (200, 155, 60)
TEAL = (31, 111, 107)
BORDER = (216, 210, 194)
GOLD_BAND = (242, 225, 178)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)  # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)  # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)  # noqa: E731


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
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


def kicker(draw, x, y, label, color):
    draw.text((x, y), label, font=SANS_B(15), fill=color)
    return y + 20


# ---------------------------------------------------------------- stories

LEAD = {
    "kicker": "NORTH KOREA",
    "headline": "Kim orders wider spread of tactical nuclear arms",
    "body": (
        "Kim Jong Un says North Korea should deploy tactical nuclear arms across "
        "more domains and expand nuclear-material output, KCNA reports."
    ),
}

CARDS = [
    {
        "kicker": "MARKETS",
        "color": TEAL,
        "headline": "Asian shares bounce back as oil holds above $94",
        "body": (
            "Stocks across Asia rally after Wall Street steadies; Brent crude "
            "stays above $94 as traders weigh attacks on Saudi oil sites."
        ),
        "pic": "markets",
    },
    {
        "kicker": "CENTRAL BANKS",
        "color": NAVY,
        "headline": "Seoul hikes rates as Tokyo signals faster rises",
        "body": (
            "South Korea lifts its base rate 25 points to 3.25%; a Bank of Japan "
            "member says it must act swiftly on signs of an inflation overshoot."
        ),
        "pic": "bank",
    },
    {
        "kicker": "INDONESIA",
        "color": RED,
        "headline": "Rescue resumes for 13 trapped in gold mine",
        "body": (
            "Search teams return to an illegal gold mine in West Java: 13 miners "
            "confirmed dead, 13 more still trapped underground."
        ),
        "pic": "mine",
    },
    {
        "kicker": "LEBANON",
        "color": TEAL,
        "headline": "Second airport planned as Hezbollah's sway wanes",
        "body": (
            "Lebanon plans to open a second international airport next month, a "
            "project that underlines Hezbollah's diminished sway."
        ),
        "pic": "plane",
    },
    {
        "kicker": "UNITED STATES",
        "color": GOLD,
        "headline": "Macy's parade marks 100 years at Thanksgiving",
        "body": (
            "Americans mark Thanksgiving as the Macy's parade in New York "
            "celebrates 100 years."
        ),
        "pic": "balloon",
    },
    {
        "kicker": "PACIFIC",
        "color": NAVY,
        "headline": "Solomons shift security pact to Australia",
        "body": (
            "The Solomon Islands shifts its security pact from China to Australia, "
            "a notable Pacific realignment."
        ),
        "pic": "island",
    },
]

ALSO = (
    "Vietnam races to finish a US trade deal \u00b7 Uber names Rakesh Ranjan to run "
    "India and South Asia \u00b7 Russia's oil refining falls to a 20-year low \u00b7 "
    "Australia's inflation hits 4.9%, a three-year high \u00b7 Gukesh faces Sindarov "
    "for the world chess title \u00b7 India marks Constitution Day"
)


# ------------------------------------------------------------- pictograms

def pic_markets(d, x, y, s):
    # Three rising bars and an arrow.
    base = y + s - 14
    bars = [(0.12, 0.45), (0.38, 0.65), (0.64, 0.85)]
    for fx, fh in bars:
        bx = x + fx * s
        d.rectangle([bx, base - fh * s, bx + 0.18 * s, base], fill=TEAL)
    d.line([(x + 0.08 * s, base - 0.42 * s), (x + 0.92 * s, base - 0.88 * s)],
           fill=RED, width=5)
    d.polygon([(x + 0.92 * s, base - 0.88 * s), (x + 0.74 * s, base - 0.88 * s),
               (x + 0.92 * s, base - 0.70 * s)], fill=RED)
    d.line([(x + 0.05 * s, base), (x + 0.95 * s, base)], fill=INK, width=3)


def pic_bank(d, x, y, s):
    # A bank: pediment, three columns, base, and a % sign.
    d.polygon([(x + 0.05 * s, y + 0.34 * s), (x + 0.5 * s, y + 0.06 * s),
               (x + 0.95 * s, y + 0.34 * s)], fill=NAVY)
    for fx in (0.18, 0.42, 0.66):
        d.rectangle([x + fx * s, y + 0.40 * s, x + (fx + 0.14) * s,
                     y + 0.78 * s], fill=NAVY)
    d.rectangle([x + 0.08 * s, y + 0.82 * s, x + 0.92 * s, y + 0.92 * s],
                fill=NAVY)
    d.text((x + 0.62 * s, y + 0.02 * s), "%", font=SANS_B(int(s * 0.34)),
           fill=RED)


def pic_mine(d, x, y, s):
    # A mountain with a tunnel mouth and a hard hat below it.
    d.polygon([(x + 0.05 * s, y + 0.62 * s), (x + 0.5 * s, y + 0.08 * s),
               (x + 0.95 * s, y + 0.62 * s)], fill=(122, 102, 78))
    d.pieslice([x + 0.38 * s, y + 0.42 * s, x + 0.62 * s, y + 0.66 * s],
               180, 360, fill=INK)
    d.rectangle([x + 0.38 * s, y + 0.54 * s, x + 0.62 * s, y + 0.66 * s],
                fill=INK)
    d.arc([x + 0.30 * s, y + 0.66 * s, x + 0.70 * s, y + 0.98 * s],
          180, 360, fill=GOLD, width=10)
    d.rectangle([x + 0.26 * s, y + 0.86 * s, x + 0.74 * s, y + 0.94 * s],
                fill=GOLD)


def pic_plane(d, x, y, s):
    # A simple jet in profile above a runway.
    d.rounded_rectangle([x + 0.08 * s, y + 0.42 * s, x + 0.86 * s, y + 0.56 * s],
                        radius=int(0.07 * s), fill=NAVY)
    d.polygon([(x + 0.84 * s, y + 0.44 * s), (x + 0.99 * s, y + 0.49 * s),
               (x + 0.84 * s, y + 0.54 * s)], fill=NAVY)
    d.polygon([(x + 0.16 * s, y + 0.44 * s), (x + 0.24 * s, y + 0.24 * s),
               (x + 0.32 * s, y + 0.44 * s)], fill=NAVY)
    d.polygon([(x + 0.44 * s, y + 0.56 * s), (x + 0.56 * s, y + 0.76 * s),
               (x + 0.64 * s, y + 0.56 * s)], fill=NAVY)
    d.ellipse([x + 0.68 * s, y + 0.45 * s, x + 0.76 * s, y + 0.53 * s],
              fill=(255, 255, 255))
    for i in range(4):
        bx = x + (0.10 + i * 0.22) * s
        d.line([(bx, y + 0.88 * s), (bx + 0.10 * s, y + 0.88 * s)],
               fill=MUTED, width=4)


def pic_balloon(d, x, y, s):
    # A parade balloon: big striped balloon with strings and bunting.
    d.ellipse([x + 0.18 * s, y + 0.06 * s, x + 0.82 * s, y + 0.62 * s],
              fill=RED)
    d.ellipse([x + 0.38 * s, y + 0.06 * s, x + 0.62 * s, y + 0.62 * s],
              fill=(255, 255, 255))
    d.line([(x + 0.34 * s, y + 0.62 * s), (x + 0.30 * s, y + 0.88 * s)],
           fill=INK, width=3)
    d.line([(x + 0.66 * s, y + 0.62 * s), (x + 0.70 * s, y + 0.88 * s)],
           fill=INK, width=3)
    for i, cx in enumerate((0.12, 0.36, 0.60, 0.84)):
        col = (GOLD, TEAL, RED, NAVY)[i]
        d.polygon([(x + cx * s, y + 0.90 * s), (x + (cx + 0.12) * s, y + 0.90 * s),
                   (x + (cx + 0.06) * s, y + 1.02 * s)], fill=col)


def pic_island(d, x, y, s):
    # Sun, a palm and waves: a Pacific island.
    d.ellipse([x + 0.62 * s, y + 0.06 * s, x + 0.88 * s, y + 0.32 * s],
              fill=GOLD)
    d.line([(x + 0.42 * s, y + 0.66 * s), (x + 0.48 * s, y + 0.34 * s)],
           fill=(122, 102, 78), width=7)
    for dx, dy in ((-0.16, -0.10), (0.16, -0.12), (-0.20, 0.02), (0.18, 0.00)):
        d.arc([x + (0.48 + dx) * s - 12, y + (0.34 + dy) * s - 12,
               x + (0.48 + dx) * s + 12, y + (0.34 + dy) * s + 12],
              200, 340, fill=TEAL, width=5)
    d.ellipse([x + 0.06 * s, y + 0.66 * s, x + 0.94 * s, y + 0.86 * s],
              fill=TEAL)
    for wy in (0.90, 0.97):
        d.line([(x + 0.10 * s, y + wy * s), (x + 0.90 * s, y + wy * s)],
               fill=(255, 255, 255), width=3)


PICS = {
    "markets": pic_markets, "bank": pic_bank, "mine": pic_mine,
    "plane": pic_plane, "balloon": pic_balloon, "island": pic_island,
}


def pic_lead(d, x, y, w, h):
    """Lead pictogram: a missile rising past a radiation trefoil."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=NAVY)
    # Trefoil: three wedges around a hub.
    cx, cy, r = x + 62, y + h - 58, 34
    for ang in (90, 210, 330):
        d.pieslice([cx - r, cy - r, cx + r, cy + r], ang - 28, ang + 28,
                   fill=GOLD)
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=NAVY)
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], outline=GOLD, width=3)
    # Missile, diagonal.
    d.polygon([(x + w - 40, y + 22), (x + w - 14, y + 48),
               (x + w - 66, y + 100), (x + w - 92, y + 74)], fill=(240, 240, 240))
    d.polygon([(x + w - 92, y + 74), (x + w - 66, y + 100),
               (x + w - 84, y + 118), (x + w - 110, y + 92)], fill=RED)
    d.polygon([(x + w - 118, y + 118), (x + w - 96, y + 140),
               (x + w - 84, y + 118)], fill=GOLD)
    d.text((x + 18, y + 16), "TACTICAL", font=SANS_B(17), fill=(255, 255, 255))
    d.text((x + 18, y + 38), "NUCLEAR", font=SANS_B(17), fill=GOLD)


# ------------------------------------------------------------------ page

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28
    cw = W - 2 * mx  # 968

    # Masthead.
    y = 18
    title = "THE WORLD TODAY"
    tf = SERIF_B(58)
    d.text(((W - d.textlength(title, font=tf)) / 2, y), title, font=tf, fill=NAVY)
    y += 70
    d.line([(mx, y), (W - mx, y)], fill=RED, width=4)
    y += 9
    date = "THURSDAY 26 NOVEMBER 2026"
    df = SANS_B(30)
    d.text(((W - d.textlength(date, font=df)) / 2, y), date, font=df, fill=RED)
    y += 40
    sub = "One day's world news, in one page"
    sf = SANS(18)
    d.text(((W - d.textlength(sub, font=sf)) / 2, y), sub, font=sf, fill=MUTED)
    y += 27
    d.line([(mx, y), (W - mx, y)], fill=INK, width=2)

    # Lead story.
    y += 12
    lead_h = 200
    d.rounded_rectangle([mx, y, W - mx, y + lead_h], radius=8, fill=CARD,
                        outline=BORDER, width=1)
    d.rectangle([mx, y + 8, mx + 6, y + lead_h - 8], fill=RED)
    tx = mx + 22
    ty = y + 13
    ty = kicker(d, tx, ty, LEAD["kicker"], RED)
    hl = wrap(d, LEAD["headline"], SANS_B(36), 560)
    ty = text_block(d, tx, ty + 2, hl, SANS_B(36), INK, 42)
    body = wrap(d, LEAD["body"], SANS(19), 560)
    text_block(d, tx, ty + 8, body, SANS(19), (52, 52, 52), 25)
    pic_lead(d, W - mx - 22 - 268, y + 16, 268, lead_h - 32)

    # Story grid: 2 columns x 3 rows.
    y += lead_h + 12
    card_w = (cw - 14) // 2
    card_h = 158
    for i, card in enumerate(CARDS):
        row, col = divmod(i, 2)
        cx = mx + col * (card_w + 14)
        cy = y + row * (card_h + 10)
        d.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=8,
                            fill=CARD, outline=BORDER, width=1)
        tx = cx + 16
        ty = cy + 11
        ty = kicker(d, tx, ty, card["kicker"], card["color"])
        hl = wrap(d, card["headline"], SANS_B(22), card_w - 132)
        ty = text_block(d, tx, ty + 1, hl, SANS_B(22), INK, 26)
        body = wrap(d, card["body"], SANS(15), card_w - 132)
        text_block(d, tx, ty + 6, body, SANS(15), (52, 52, 52), 19)
        PICS[card["pic"]](d, cx + card_w - 116, cy + card_h - 112, 100)

    # Also on the day.
    y += 3 * card_h + 2 * 10 + 12
    d.line([(mx, y), (W - mx, y)], fill=INK, width=2)
    y += 10
    d.text((mx, y), "ALSO ON THE DAY", font=SANS_B(16), fill=RED)
    y += 24
    lines = wrap(d, ALSO, SANS(15), cw)
    text_block(d, mx, y, lines, SANS(15), (52, 52, 52), 20)

    out = HERE / "entry.png"
    img.save(out, optimize=True)
    print(f"wrote {out} {out.stat().st_size} bytes")


if __name__ == "__main__":
    main()
