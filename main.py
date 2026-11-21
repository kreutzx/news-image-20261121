#!/usr/bin/env python3
"""The World in One Day -- Saturday 21 November 2026.

Renders a 1024x1024 front page summing up the world's news of
Saturday 21 November 2026, from a story database written into this file.

Deterministic: fixed layout, fixed seed, no clock, no network, no
randomness. Running it twice writes byte-identical PNGs.

Usage:  MAKEFUN_OUTPUT_DIR=out python3 main.py
Writes entry.png into MAKEFUN_OUTPUT_DIR (default /output, else ".").
"""

import hashlib
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- constants

W, H = 1024, 1024
CREAM = (247, 241, 227)
PAPER = (252, 248, 238)
INK = (20, 33, 61)
INK_SOFT = (58, 68, 92)
RED = (193, 39, 45)
GOLD = (176, 141, 42)
GOLD_LIGHT = (214, 178, 94)
RULE = (20, 33, 61)
GREY_LINE = (198, 190, 170)
MUTED = (110, 104, 88)

SECTION_COLORS = {
    "World": (29, 78, 137),
    "Money & Tech": (140, 109, 31),
    "Science & Planet": (39, 106, 75),
    "Society & Culture": (140, 47, 57),
}

CERT_COLORS = {
    "CONFIRMED": (39, 106, 75),
    "CLAIM": (176, 120, 20),
    "REPORTED": (74, 111, 165),
}

# ---------------------------------------------------------------- story data
# (section, headline, deck, source, certainty, region, field)
# Headlines and decks are written in the author's own words from facts
# read in reporting on 21 November 2026. Certainty:
#   CONFIRMED -- verified by a major outlet or official source
#   CLAIM     -- one side asserts it
#   REPORTED  -- reported but unconfirmed

HEROES = [
    (
        "MARKETS",
        "WALL STREET'S\nBLACK FRIDAY",
        "Stocks plunge as AI shares collapse: the S&P 500 falls 3.7%, the "
        "Nasdaq 5.3% and the Dow sheds about 950 points. Both benchmarks "
        "close in correction territory after a seventh straight down day.",
        "Wall Street Journal",
        "CONFIRMED",
        "North America",
        "Markets",
    ),
    (
        "MIDDLE EAST",
        "BLASTS IN RIYADH\nAS WAR WIDENS",
        "Two explosions are heard in the Saudi capital hours after Houthi "
        "missiles strike its tallest tower. Trump says Tehran wants a deal "
        "he will not accept; Israel presses for strikes on Iran.",
        "AFP",
        "CONFIRMED",
        "Middle East",
        "Conflict",
    ),
]

# 24 section cards: 6 per section. Decks are one-line teasers (<= ~40 chars).
CARDS = [
    # World
    ("World",
     "COP31 slips into overtime",
     "Draft drops fossil fuels; Panama objects.",
     "Reuters", "CONFIRMED", "Global", "Climate"),
    ("World",
     "Britain and EU strike reset deal",
     "Food trade, youth travel, carbon agreed.",
     "CNA", "CONFIRMED", "Europe", "Politics"),
    ("World",
     "Estonia to seal Russian border",
     "Shut from 1 Dec after alleged GRU arson.",
     "Al Jazeera", "CONFIRMED", "Europe", "Security"),
    ("World",
     "Mongolia's president quits",
     "Parliament accepts it; early vote looms.",
     "Reuters", "CONFIRMED", "Asia-Pacific", "Politics"),
    ("World",
     "19 years for NY murder plot",
     "Jailed 235 months over a foiled hit.",
     "US Dept of Justice", "CONFIRMED", "North America", "Justice"),
    ("World",
     "Denmark alleges Russian murder plot",
     "Copenhagen alleges a Russian plot.",
     "Wire reports", "REPORTED", "Europe", "Security"),
    # Money & Tech
    ("Money & Tech",
     "Anthropic slides after record IPO",
     "Shares fall ~11% after the $81.3bn debut.",
     "Wall Street Journal", "CONFIRMED", "North America", "Tech"),
    ("Money & Tech",
     "Bitcoin drops below $60,000",
     "Token steadies near $58,000.",
     "BlockBeats", "CONFIRMED", "Global", "Markets"),
    ("Money & Tech",
     "Fear gauge hits 35.89",
     "Highest close since last year's turmoil.",
     "BlockBeats", "CONFIRMED", "Global", "Markets"),
    ("Money & Tech",
     "Banks hit by vendor cyberattack",
     "Big banks hit via outside vendors.",
     "JagranJosh", "REPORTED", "North America", "Tech"),
    ("Money & Tech",
     "Hyundai unveils new Elantra",
     "New sedan debuts in Los Angeles.",
     "JagranJosh", "CONFIRMED", "North America", "Tech"),
    ("Money & Tech",
     "Sensex jumps nearly 900 points",
     "Mumbai bucks the global sell-off.",
     "JagranJosh", "CONFIRMED", "South Asia", "Markets"),
    # Science & Planet
    ("Science & Planet",
     "Cyclone Akvan weakens inland",
     "No major damage after 370,000 evacuated.",
     "IMD", "CONFIRMED", "South Asia", "Weather"),
    ("Science & Planet",
     "Ebola's toll on children laid bare",
     "Seven in ten infected under-fives die.",
     "Reuters", "CONFIRMED", "Africa", "Health"),
    ("Science & Planet",
     "Storm Xavier gales narrow",
     "Warning shrinks the gale-force area.",
     "AppiSToS", "CONFIRMED", "Europe", "Weather"),
    ("Science & Planet",
     "Russia stalls killer-robot rules",
     "Moscow blocks UN weapons rules.",
     "Euronews", "REPORTED", "Global", "Tech"),
    ("Science & Planet",
     "Saudi storms warning to Tuesday",
     "Heavy rain, hail, floods warned.",
     "AppiSToS", "CONFIRMED", "Middle East", "Weather"),
    ("Science & Planet",
     "Kenya clears its Ebola cases",
     "Nairobi says cases are over.",
     "Outbreak Watch", "CONFIRMED", "Africa", "Health"),
    # Society & Culture
    ("Society & Culture",
     "Six killed in Gaza strikes",
     "Attacks hit central Gaza despite truce.",
     "Associated Press", "CONFIRMED", "Middle East", "Conflict"),
    ("Society & Culture",
     "22,000 Gaza children dead, ministry says",
     "Child toll passes 22,000, ministry says.",
     "Gaza health ministry", "REPORTED", "Middle East", "Society"),
    ("Society & Culture",
     "UN warns over Hudaydah attacks",
     "Strikes threaten a key aid lifeline.",
     "United Nations", "REPORTED", "Middle East", "Society"),
    ("Society & Culture",
     "Two Salvadorans killed in Haiti",
     "Men die handling explosives, military says.",
     "Haitian military", "REPORTED", "Latin America", "Security"),
    ("Society & Culture",
     "Brazil shields Indigenous land",
     "Lula strengthens Indigenous safeguards.",
     "Wire reports", "REPORTED", "Latin America", "Politics"),
    ("Society & Culture",
     "Bukele seeks third term",
     "Bid could keep him in power to 2033.",
     "Wire reports", "REPORTED", "Latin America", "Politics"),
]

SPORT = [
    ("Norris takes rainy Vegas pole",
     "Norris beats Verstappen by 0.32s.",
     "Associated Press", "CONFIRMED", "North America", "Sport"),
    ("Rahul's century puts India on top",
     "13th Test ton; India reach 247/1.",
     "NDTV", "CONFIRMED", "Asia-Pacific", "Sport"),
    ("Seven Premier League games today",
     "Man City v Fulham opens the day.",
     "LiveScore", "CONFIRMED", "Europe", "Sport"),
    ("Palmowski's record pole",
     "Seventh pole by a record 1.578s.",
     "F1 Academy", "CONFIRMED", "North America", "Sport"),
    ("India edge NZ in ODI decider",
     "India win the fifth ODI by 22 runs.",
     "Live scores", "REPORTED", "Asia-Pacific", "Sport"),
]

NUMBERS = [
    ("-5.28%", "Nasdaq's Friday fall"),
    ("-3.7%", "S&P 500, seventh straight loss"),
    ("35.89", "VIX fear-gauge close"),
    ("$81.3bn", "Anthropic's record IPO"),
    ("370,000", "people evacuated for Akvan"),
    ("11,376", "confirmed Ebola cases"),
    ("235", "months for Gupta's sentence"),
    ("1:47.934", "Norris's pole lap"),
]

MARKETS = [
    ("MARKETS -- FRIDAY CLOSE",
     "S&P 6,910.39  -3.7%   Nasdaq 22,617.73  -5.3%\n"
     "Dow 48,147.33  -1.9%   Brent $92.57   WTI $83.98",
     "North America", "Markets"),
    ("WEATHER -- AKVAN",
     "Cyclone weakens to a deep depression inland;\n"
     "heavy rain across Odisha for 48 hours; 39 trains axed.",
     "South Asia", "Weather"),
    ("WEATHER -- GULF",
     "Thunderstorms and hail warned in Saudi Arabia\n"
     "through Tuesday; gale warnings narrow for Storm Xavier.",
     "Middle East", "Weather"),
]

WIRE = [
    ("Two explosions heard in Riyadh early Saturday, AFP reports.", "AFP", "REPORTED", "Middle East", "Conflict"),
    ("Tanker struck by a projectile near the Strait of Hormuz; fire reported.", "UKMTO", "REPORTED", "Middle East", "Conflict"),
    ("US Treasury adds four Iranians to its sanctions list over oil revenues.", "US Treasury", "CONFIRMED", "North America", "Politics"),
    ("Trump puts off any decision on new Iran strikes until next year, reports say.", "Wire reports", "REPORTED", "North America", "Politics"),
    ("Israel presses the US for a 4-7 day bombing campaign on Iran, sources say.", "Wire reports", "REPORTED", "Middle East", "Conflict"),
    ("Iraqi troops move into a Hezbollah stronghold south of Baghdad.", "Associated Press", "CONFIRMED", "Middle East", "Security"),
    ("Ukraine to send food aid to nine countries, Kyiv says.", "Wire reports", "CONFIRMED", "Europe", "Politics"),
    ("UK and Canadian retail sales strengthen; pound ends at $1.3082.", "Equiti", "CONFIRMED", "Europe", "Markets"),
]

TIMELINE = [
    ("FRI 21:00 UTC", "Wall Street closes in correction"),
    ("00:04 UTC", "India 239/1 at lunch, day 3, Wellington"),
    ("00:54 UTC", "Rahul's 13th Test century"),
    ("01:25 UTC", "Gupta's 235-month sentence published"),
    ("02:43 RIYADH", "Explosions heard in the Saudi capital"),
    ("04:00 UTC", "Las Vegas GP qualifying: Norris on pole"),
    ("10:00 UTC", "Sensex closes up ~898 points"),
]

# ---------------------------------------------------------------- fonts

def _load_font(bold=False, serif=False, size=14):
    """Best available font: Noto, then DejaVu, then Pillow's default."""
    candidates = []
    if serif:
        candidates += [
            "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf" if bold
            else "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold
            else "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        ]
    else:
        candidates += [
            "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf" if bold
            else "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
            else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def fonts():
    return {
        "masthead": _load_font(bold=True, serif=True, size=46),
        "date": _load_font(bold=True, size=19),
        "account": _load_font(bold=True, size=13),
        "hero_kicker": _load_font(bold=True, size=12),
        "hero_head": _load_font(bold=True, serif=True, size=25),
        "hero_deck": _load_font(size=13),
        "section": _load_font(bold=True, size=13),
        "card_head": _load_font(bold=True, serif=True, size=14),
        "card_deck": _load_font(size=11),
        "tag": _load_font(bold=True, size=8),
        "sport_head": _load_font(bold=True, serif=True, size=13),
        "sport_deck": _load_font(size=10),
        "num_big": _load_font(bold=True, serif=True, size=24),
        "num_label": _load_font(size=10),
        "panel_head": _load_font(bold=True, size=11),
        "panel_body": _load_font(size=11),
        "wire": _load_font(size=11),
        "time": _load_font(bold=True, size=10),
        "time_body": _load_font(size=10),
        "footer": _load_font(size=9),
    }


# ---------------------------------------------------------------- text helpers

def wrap(draw, text, font, width):
    """Greedy word wrap; returns list of lines that fit in width px."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, font, width, max_lines):
    """Wrap text to at most max_lines, ellipsising the last line."""
    lines = wrap(draw, text, font, width)
    if len(lines) <= max_lines:
        return lines
    lines = lines[:max_lines]
    last = lines[-1]
    while last and draw.textlength(last + " ...", font=font) > width:
        last = last.rsplit(" ", 1)[0] if " " in last else last[:-1]
    lines[-1] = (last + " ...").strip()
    return lines


def text_h(draw, text, font):
    box = draw.textbbox((0, 0), text, font=font)
    return box[3] - box[1]


def cert_chip(draw, x, y, cert, font):
    """Small coloured certainty chip; returns width used."""
    label = " " + cert + " "
    w = int(draw.textlength(label, font=font)) + 8
    h = 12
    color = CERT_COLORS.get(cert, INK_SOFT)
    draw.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=color)
    draw.text((x + 4, y + 1), label, font=font, fill=(255, 255, 255))
    return w


def source_tag(draw, x, y, source, font):
    draw.text((x, y), source.upper(), font=font, fill=MUTED)
    return int(draw.textlength(source.upper(), font=font))


# ---------------------------------------------------------------- drawing

def draw_masthead(draw, f, counts):
    n_stories = counts["stories"]
    n_regions = counts["regions"]
    n_fields = counts["fields"]
    draw.rectangle([0, 0, W, 112], fill=INK)
    draw.rectangle([0, 112, W, 116], fill=RED)
    # small globe mark, left
    cx, cy, r = 52, 56, 30
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD_LIGHT, width=2)
    for k in (-1, 0, 1):
        draw.arc([cx - r, cy - r, cx + r, cy + r], 90 + 55 * k, 90 + 55 * k + 55,
                 fill=GOLD_LIGHT, width=1)
    draw.line([cx - r, cy, cx + r, cy], fill=GOLD_LIGHT, width=1)
    draw.line([cx, cy - r, cx, cy + r], fill=GOLD_LIGHT, width=1)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
    draw.text((96, 18), "THE WORLD IN ONE DAY", font=f["masthead"], fill=(252, 248, 238))
    draw.text((98, 72), "SATURDAY  \u00b7  21 NOVEMBER 2026",
              font=f["date"], fill=GOLD_LIGHT)
    account = ("{} STORIES  \u00b7  {} REGIONS  \u00b7  {} FIELDS  \u00b7  "
               "ALL FROM THIS SATURDAY".format(n_stories, n_regions, n_fields))
    draw.text((98, 94), account, font=f["account"], fill=(200, 205, 220))


def draw_hero_chart(draw, x, y, w, h):
    """Falling market bars for hero 1."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 222, 200))
    draw.rectangle([x, y, x + w, y + h], outline=GREY_LINE, width=1)
    bars = [0.92, 0.86, 0.88, 0.74, 0.66, 0.55, 0.42]
    bw = (w - 24) // len(bars)
    base = y + h - 18
    for i, frac in enumerate(bars):
        bx = x + 12 + i * bw
        bh = int((h - 34) * frac)
        col = RED if i >= len(bars) - 2 else INK
        draw.rectangle([bx + 2, base - bh, bx + bw - 3, base], fill=col)
    draw.line([x + 10, base, x + w - 10, base], fill=INK, width=1)
    draw.text((x + 10, y + 5), "S&P 500  -3.7%", font=_load_font(bold=True, size=10),
              fill=RED)


def draw_hero_map(draw, x, y, w, h):
    """Stylised Gulf map with a blast marker for hero 2."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 226, 232))
    draw.rectangle([x, y, x + w, y + h], outline=GREY_LINE, width=1)
    # crude landmass blobs
    draw.polygon([(x + 8, y + 12), (x + 70, y + 6), (x + 96, y + 30),
                  (x + 60, y + 52), (x + 14, y + 44)], fill=(232, 222, 200))
    draw.polygon([(x + 96, y + 62), (x + w - 10, y + 56), (x + w - 8, y + h - 12),
                  (x + 110, y + h - 8), (x + 92, y + 84)], fill=(232, 222, 200))
    draw.polygon([(x + 30, y + h - 30), (x + 80, y + h - 44), (x + 96, y + h - 16),
                  (x + 60, y + h - 6)], fill=(232, 222, 200))
    # blast marker on Riyadh
    bx, by = x + 78, y + 44
    for rr, col in ((16, (193, 39, 45)), (10, (193, 39, 45)), (4, (255, 255, 255))):
        draw.ellipse([bx - rr, by - rr, bx + rr, by + rr], outline=col, width=2)
    draw.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=RED)
    draw.text((x + 10, y + h - 16), "RIYADH", font=_load_font(bold=True, size=9),
              fill=INK)
    draw.text((x + w - 52, y + 6), "GULF", font=_load_font(bold=True, size=9),
              fill=INK_SOFT)


def draw_heroes(draw, f):
    y0, y1 = 122, 288
    gap = 12
    hw = (W - 56 - gap) // 2
    for i, hero in enumerate(HEROES):
        kicker, head, deck, source, cert, _region, _field = hero
        x = 28 + i * (hw + gap)
        draw.rectangle([x, y0, x + hw, y1], fill=PAPER)
        draw.rectangle([x, y0, x + hw, y1], outline=GREY_LINE, width=1)
        draw.rectangle([x, y0, x + hw, y0 + 4], fill=RED)
        draw.text((x + 12, y0 + 12), kicker, font=f["hero_kicker"], fill=RED)
        # illustration, top right
        iw, ih = 120, 56
        ix, iy = x + hw - iw - 12, y0 + 32
        if i == 0:
            draw_hero_chart(draw, ix, iy, iw, ih)
        else:
            draw_hero_map(draw, ix, iy, iw, ih)
        head_w = hw - iw - 36
        lines = head.split("\n")
        ty = y0 + 32
        for ln in lines:
            draw.text((x + 12, ty), ln, font=f["hero_head"], fill=INK)
            ty += 28
        # deck runs full width, below the headline block and illustration
        deck_lines = fit_lines(draw, deck, f["hero_deck"], hw - 24, 3)
        ty = y0 + 32 + 56 + 4
        for ln in deck_lines:
            draw.text((x + 12, ty), ln, font=f["hero_deck"], fill=INK_SOFT)
            ty += 15
        # source + certainty, bottom
        by = y1 - 20
        source_tag(draw, x + 12, by, source, f["tag"])
        label = " " + cert + " "
        cw = int(draw.textlength(label, font=f["tag"])) + 8
        cert_chip(draw, x + hw - 12 - cw, by - 1, cert, f["tag"])


def draw_region_band(draw, f, region_counts, y=292):
    draw.rectangle([0, y, W, y + 22], fill=(232, 222, 200))
    parts = []
    for region in ["Middle East", "Europe", "North America", "Asia-Pacific",
                   "South Asia", "Africa", "Latin America", "Global"]:
        n = region_counts.get(region, 0)
        if n:
            parts.append("{} {}".format(region.upper(), n))
    text = "  \u00b7  ".join(parts)
    tw = draw.textlength(text, font=f["account"])
    draw.text(((W - tw) / 2, y + 4), text, font=f["account"], fill=INK)


def draw_sections(draw, f, y0=320):
    col_w = 234
    gap = 10
    sections = ["World", "Money & Tech", "Science & Planet", "Society & Culture"]
    card_h = 52
    for ci, section in enumerate(sections):
        x = 28 + ci * (col_w + gap)
        color = SECTION_COLORS[section]
        draw.rectangle([x, y0, x + col_w, y0 + 20], fill=color)
        draw.text((x + 8, y0 + 3), section.upper(), font=f["section"],
                  fill=(255, 255, 255))
        cards = [c for c in CARDS if c[0] == section]
        cy = y0 + 26
        for card in cards:
            _sec, head, deck, source, cert, _r, _fl = card
            draw.line([x, cy + card_h - 1, x + col_w, cy + card_h - 1],
                      fill=GREY_LINE, width=1)
            head_lines = fit_lines(draw, head, f["card_head"], col_w - 4, 2)
            ty = cy + 1
            for ln in head_lines:
                draw.text((x + 2, ty), ln, font=f["card_head"], fill=INK)
                ty += 14
            deck_lines = fit_lines(draw, deck, f["card_deck"], col_w - 4, 1)
            for ln in deck_lines:
                draw.text((x + 2, ty), ln, font=f["card_deck"], fill=INK_SOFT)
                ty += 12
            by = cy + card_h - 11
            source_tag(draw, x + 2, by, source, f["tag"])
            label = " " + cert + " "
            cw = int(draw.textlength(label, font=f["tag"])) + 8
            cert_chip(draw, x + col_w - cw, by - 1, cert, f["tag"])
            cy += card_h
    return y0 + 26 + 6 * card_h


def draw_sport(draw, f, y0):
    draw.rectangle([28, y0, W - 28, y0 + 20], fill=INK)
    draw.text((36, y0 + 3), "SPORT", font=f["section"], fill=(255, 255, 255))
    draw.text((W - 210, y0 + 4), "SATURDAY'S GAMES & RESULTS",
              font=f["tag"], fill=GOLD_LIGHT)
    col_w = 188
    gap = 8
    y = y0 + 24
    for i, item in enumerate(SPORT):
        head, deck, source, cert, _r, _fl = item
        x = 28 + i * (col_w + gap)
        draw.rectangle([x, y, x + col_w, y + 54], fill=PAPER)
        draw.rectangle([x, y, x + col_w, y + 54], outline=GREY_LINE, width=1)
        head_lines = fit_lines(draw, head, f["sport_head"], col_w - 12, 2)
        ty = y + 4
        for ln in head_lines:
            draw.text((x + 6, ty), ln, font=f["sport_head"], fill=INK)
            ty += 13
        deck_lines = fit_lines(draw, deck, f["sport_deck"], col_w - 12, 1)
        for ln in deck_lines:
            draw.text((x + 6, ty), ln, font=f["sport_deck"], fill=INK_SOFT)
            ty += 11
        by = y + 54 - 11
        source_tag(draw, x + 6, by, source, f["tag"])
        label = " " + cert + " "
        cw = int(draw.textlength(label, font=f["tag"])) + 8
        cert_chip(draw, x + col_w - 6 - cw, by - 1, cert, f["tag"])
    return y + 54


def draw_numbers(draw, f, y0):
    draw.text((28, y0), "BY THE NUMBERS", font=f["section"], fill=RED)
    draw.line([28, y0 + 18, W - 28, y0 + 18], fill=RED, width=2)
    col_w = 118
    gap = 4
    y = y0 + 23
    for i, (num, label) in enumerate(NUMBERS):
        x = 28 + i * (col_w + gap)
        draw.text((x, y), num, font=f["num_big"], fill=INK)
        lab_lines = fit_lines(draw, label, f["num_label"], col_w - 4, 2)
        ty = y + 29
        for ln in lab_lines:
            draw.text((x, ty), ln, font=f["num_label"], fill=INK_SOFT)
            ty += 11
    return y + 51


def draw_markets(draw, f, y0):
    panel_w = 312
    gap = 8
    y = y0
    for i, (head, body, _r, _fl) in enumerate(MARKETS):
        x = 28 + i * (panel_w + gap)
        draw.rectangle([x, y, x + panel_w, y + 48], fill=PAPER)
        draw.rectangle([x, y, x + panel_w, y + 48], outline=GREY_LINE, width=1)
        draw.text((x + 8, y + 4), head, font=f["panel_head"], fill=RED)
        ty = y + 19
        for ln in body.split("\n"):
            draw.text((x + 8, ty), ln, font=f["panel_body"], fill=INK)
            ty += 13
    return y + 48


def draw_wire(draw, f, y0):
    draw.rectangle([28, y0, W - 28, y0 + 20], fill=INK)
    draw.text((36, y0 + 3), "LATE WIRE", font=f["section"], fill=(255, 255, 255))
    col_w = 476
    gap = 8
    y = y0 + 24
    for i, (line, source, cert, _r, _fl) in enumerate(WIRE):
        col = i // 4
        row = i % 4
        x = 28 + col * (col_w + gap)
        yy = y + row * 14
        draw.text((x, yy), "\u25aa ", font=f["wire"], fill=RED)
        tw = draw.textlength("\u25aa ", font=f["wire"])
        lines = fit_lines(draw, line, f["wire"], col_w - tw - 4, 1)
        draw.text((x + tw, yy), lines[0] if lines else "", font=f["wire"],
                  fill=INK)
    return y + 4 * 14


def draw_timeline(draw, f, y0):
    draw.line([28, y0, W - 28, y0], fill=GREY_LINE, width=1)
    draw.text((28, y0 + 4), "SATURDAY, IN UTC", font=f["section"], fill=RED)
    y = y0 + 22
    # flow items across the width in two rows
    x = 28
    row_y = [y, y + 13]
    row = 0
    for t, body in TIMELINE:
        label = t + "  " + body
        wdt = draw.textlength(label, font=f["time_body"]) + 14
        if x + wdt > W - 28 and row == 0:
            row = 1
            x = 28
        draw.text((x, row_y[row]), t, font=f["time"], fill=RED)
        tw = draw.textlength(t, font=f["time"])
        draw.text((x + tw + 5, row_y[row]), body, font=f["time_body"],
                  fill=INK_SOFT)
        x += wdt
    return row_y[1] + 13


def count_stats():
    """Count stories, regions and fields from the data lists.

    Tuple shapes differ per list, so each is normalised explicitly:
      HEROES / CARDS : (section, head, deck, source, cert, region, field)
      SPORT          : (head, deck, source, cert, region, field)
      MARKETS        : (head, body, region, field)
      WIRE           : (line, source, cert, region, field)
      NUMBERS        : (big, label) -- no region or field
    """
    tagged = []
    for h in HEROES:
        tagged.append((h[5], h[6]))
    for c in CARDS:
        tagged.append((c[5], c[6]))
    for s in SPORT:
        tagged.append((s[4], s[5]))
    for m in MARKETS:
        tagged.append((m[2], m[3]))
    for w in WIRE:
        tagged.append((w[3], w[4]))
    total = (len(HEROES) + len(CARDS) + len(SPORT) + len(NUMBERS)
             + len(MARKETS) + len(WIRE))
    regions = {}
    fields = set()
    for region, field in tagged:
        if region:
            regions[region] = regions.get(region, 0) + 1
        if field:
            fields.add(field)
    return {
        "stories": total,
        "regions": len(regions),
        "fields": len(fields),
        "region_counts": regions,
    }


def render():
    counts = count_stats()
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    f = fonts()
    draw_masthead(draw, f, counts)
    draw_heroes(draw, f)
    draw_region_band(draw, f, counts["region_counts"])
    y = draw_sections(draw, f)
    y = draw_sport(draw, f, y + 4)
    y = draw_numbers(draw, f, y + 4)
    y = draw_markets(draw, f, y + 4)
    y = draw_wire(draw, f, y + 4)
    y = draw_timeline(draw, f, y + 4)
    # footer
    fy = H - 16
    draw.line([28, fy - 5, W - 28, fy - 5], fill=GREY_LINE, width=1)
    footer = ("Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 CNA \u00b7 Al Jazeera "
              "\u00b7 Wall Street Journal \u00b7 IMD \u00b7 US Dept of Justice "
              "\u00b7 NDTV \u00b7 LiveScore \u00b7 F1 Academy \u00b7 BlockBeats "
              "\u00b7 Equiti \u00b7 UKMTO \u00b7 AppiSToS  --  Unconfirmed items "
              "labelled CLAIM or REPORTED.")
    draw.text((28, fy), footer, font=f["footer"], fill=MUTED)
    return img


def main():
    random.seed(20261121)  # fixed; no randomness is actually used
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not outdir:
        outdir = "/output" if os.path.isdir("/output") else "."
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    img = render()
    img.save(path, format="PNG", optimize=True)
    size = os.path.getsize(path)
    digest = hashlib.sha256(open(path, "rb").read()).hexdigest()
    counts = count_stats()
    print("wrote {} ({}x{}, {} bytes, sha256 {})".format(
        path, W, H, size, digest[:16]))
    print("stories={} regions={} fields={}".format(
        counts["stories"], counts["regions"], counts["fields"]))
    print("region counts: {}".format(counts["region_counts"]))
    if size > 1048576:
        print("ERROR: entry.png exceeds 1 MiB", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
