# Renderer for "The World in One Day" — Saturday 21 November 2026.
# Builds entry.png (1024x1024) from stories.py's records with art.py's
# drawn scenes. Deterministic: no clock, no network, no randomness
# outside fixed seeds in art.py — two runs give byte-identical output.
# Run:  python3 build.py   (writes entry.png beside this file)

import hashlib
import io
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import PALETTE as P, SCENES          # noqa: E402
from stories import STORIES, CARDS, SPORT, NUMBERS, TICKER, TIMELINE, DATE_CHECK  # noqa: E402

W = H = 1024
MARGIN = 22
CW = W - 2 * MARGIN
FD = "/usr/share/fonts/truetype/noto/"


def font(name, size):
    return ImageFont.truetype(FD + name, size)


F_TITLE = font("NotoSerif-Black.ttf", 50)
F_DATE = font("NotoSans-Bold.ttf", 13)
F_ACCT = font("NotoSans-Bold.ttf", 15)
F_TIME_T = font("NotoSans-Bold.ttf", 10)
F_TIME_L = font("NotoSans-Regular.ttf", 10)
F_HERO_H = font("NotoSerif-Black.ttf", 21)
F_HERO_D = font("NotoSans-Regular.ttf", 11)
F_LEAD_H = font("NotoSerif-Bold.ttf", 14)
F_LEAD_D = font("NotoSans-Regular.ttf", 10)
F_WIRE_H = font("NotoSans-SemiBold.ttf", 11)
F_CARD = font("NotoSans-SemiBold.ttf", 11)
F_CARD_SRC = font("NotoSans-Regular.ttf", 9)
F_META = font("NotoSans-Bold.ttf", 8)
F_SEC = font("NotoSans-Bold.ttf", 13)
F_NUM_V = font("NotoSerif-Bold.ttf", 15)
F_NUM_L = font("NotoSans-Bold.ttf", 9)
F_SMALL = font("NotoSans-Regular.ttf", 10)
F_SMALL_B = font("NotoSans-Bold.ttf", 10)
F_FINE = font("NotoSans-Regular.ttf", 9)

TAG_COLORS = {
    "CONFIRMED": (30, 107, 82), "REPORTED": (91, 75, 138),
    "DEVELOPING": (179, 39, 30), "FORECAST": (32, 80, 122),
}
PANEL_BG = (252, 250, 244)


def wrap(d, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, text, fnt, maxw, lh, fill=None, max_lines=None):
    lines = wrap(d, text, fnt, maxw)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill or P["ink"])
        y += lh
    return y


def chip(d, x, y, tag):
    label = tag
    w_ = d.textlength(label, font=F_META) + 8
    d.rectangle([x, y, x + w_, y + 11], fill=TAG_COLORS[tag])
    d.text((x + 4, y + 1), label, font=F_META, fill=P["white"])
    return x + w_ + 5


def meta_line(d, x, y, story, maxw):
    nx = chip(d, x, y, story["tag"])
    d.text((nx, y + 1), story.get("src", ""), font=F_META, fill=P["grey"])


def panel(d, x, y, w_, h_):
    d.rectangle([x, y, x + w_, y + h_], fill=PANEL_BG, outline=P["ink"], width=1)


def art_box(d, story, x, y, w_, h_):
    d.rectangle([x, y, x + w_, y + h_], fill=P["sky"])
    SCENES[story["art"]](d, x, y, w_, h_, P)
    d.rectangle([x, y, x + w_, y + h_], outline=P["ink"], width=1)


def hero_panel(d, x, y, w_, h_, story):
    panel(d, x, y, w_, h_)
    art_box(d, story, x + 1, y + 1, w_ - 2, 84)
    ty = y + 92
    meta_line(d, x + 9, ty, story, w_ - 18)
    ty += 16
    ty = block(d, x + 9, ty, story["head"], F_HERO_H, w_ - 18, 24, max_lines=2)
    block(d, x + 9, ty + 2, story["deck"], F_HERO_D, w_ - 18, 13, max_lines=2)


def lead_panel(d, x, y, w_, h_, story):
    panel(d, x, y, w_, h_)
    art_box(d, story, x + 1, y + 1, w_ - 2, 58)
    ty = y + 65
    meta_line(d, x + 8, ty, story, w_ - 16)
    ty += 15
    ty = block(d, x + 8, ty, story["head"], F_LEAD_H, w_ - 16, 17, max_lines=2)
    block(d, x + 8, ty + 1, story["deck"], F_LEAD_D, w_ - 16, 12, max_lines=2)


def wire_panel(d, x, y, w_, h_, story):
    panel(d, x, y, w_, h_)
    art_box(d, story, x + 1, y + 1, 64, h_ - 2)
    tx = x + 73
    ty = block(d, tx, y + 6, story["head"], F_WIRE_H, w_ - 81, 13, max_lines=2)
    meta_line(d, tx, max(ty + 2, y + h_ - 15), story, w_ - 81)


SECTION_ORDER = ["WORLD", "POLITICS & MONEY", "SCIENCE & SOCIETY"]
SECTION_COLORS = {"WORLD": (32, 80, 122), "POLITICS & MONEY": (30, 107, 82),
                  "SCIENCE & SOCIETY": (91, 75, 138)}


def card(d, x, y, w_, story):
    # headline (semibold) with source appended in grey, max 2 lines;
    # the row height follows the lines actually drawn, plus breathing room
    lines = wrap(d, story["head"], F_CARD, w_ - 14)[:2]
    sq = TAG_COLORS[story["tag"]]
    d.rectangle([x, y + 3, x + 6, y + 10], fill=sq)
    ty = y
    for i, ln in enumerate(lines):
        d.text((x + 10, ty), ln, font=F_CARD, fill=P["ink"])
        if i == len(lines) - 1:
            tail = "  · " + story["src"]
            lx = x + 10 + d.textlength(ln, font=F_CARD)
            if lx + d.textlength(tail, font=F_CARD_SRC) <= x + w_:
                d.text((lx, ty + 2), tail, font=F_CARD_SRC, fill=P["grey"])
        ty += 13
    return ty + 7


def compose():
    img = Image.new("RGB", (W, H), P["paper"])
    d = ImageDraw.Draw(img)

    # ---- accounting, counted from the data itself --------------------
    all_stories = STORIES + CARDS + SPORT + TICKER
    total = len(all_stories) + len(NUMBERS)
    drawn = sum(1 for s in STORIES if s.get("art"))
    regions = {s["region"] for s in all_stories}
    fields = {s["field"] for s in all_stories}

    # ---- masthead -----------------------------------------------------
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=F_TITLE)
    d.text(((W - tw) / 2, 8), title, font=F_TITLE, fill=P["ink"])
    d.line([MARGIN, 68, W - MARGIN, 68], fill=P["ink"], width=2)
    d.text((MARGIN, 73), "SATURDAY 21 NOVEMBER 2026", font=F_DATE, fill=P["red"])
    rtxt = "ONE IMAGE - EVERY STORY SOURCED AND TAGGED"
    d.text((W - MARGIN - d.textlength(rtxt, font=F_DATE), 73), rtxt, font=F_DATE, fill=P["ink"])
    acct = (f"{total} STORIES - {drawn} DRAWN - {len(regions)} REGIONS - "
            f"{len(fields)} FIELDS - ALL FROM THIS SATURDAY")
    d.rectangle([MARGIN, 92, W - MARGIN, 114], fill=P["ink"])
    aw = d.textlength(acct, font=F_ACCT)
    d.text(((W - aw) / 2, 96), acct, font=F_ACCT, fill=P["paper"])

    # ---- UTC timeline --------------------------------------------------
    ty = 122
    d.line([MARGIN + 6, ty + 5, W - MARGIN - 6, ty + 5], fill=P["gold"], width=2)
    step = CW / len(TIMELINE)
    for i, (when, what) in enumerate(TIMELINE):
        cx = MARGIN + step * i + step / 2
        d.ellipse([cx - 4, ty + 1, cx + 4, ty + 9], fill=P["red"])
        wtxt = when
        d.text((cx - d.textlength(wtxt, font=F_TIME_T) / 2, ty + 12), wtxt, font=F_TIME_T, fill=P["ink"])
        d.text((cx - d.textlength(what, font=F_TIME_L) / 2, ty + 24), what, font=F_TIME_L, fill=P["grey"])

    # ---- heroes ---------------------------------------------------------
    heroes = [s for s in STORIES if s["kind"] == "hero"]
    hy, hh = 160, 188
    hw = (CW - 12) // 2
    for i, s in enumerate(heroes):
        hero_panel(d, MARGIN + i * (hw + 12), hy, hw, hh, s)

    # ---- lead panels: 2 rows of 3 ---------------------------------------
    leads = [s for s in STORIES if s["kind"] == "lead"]
    lw = (CW - 2 * 10) // 3
    for r in range(2):
        for c in range(3):
            lead_panel(d, MARGIN + c * (lw + 10), 356 + r * 148, lw, 140, leads[r * 3 + c])

    # ---- picture wire: 2 rows of 4 --------------------------------------
    wires = [s for s in STORIES if s["kind"] == "wire"]
    ww = (CW - 3 * 8) // 4
    for r in range(2):
        for c in range(4):
            wire_panel(d, MARGIN + c * (ww + 8), 660 + r * 62, ww, 56, wires[r * 4 + c])

    # ---- by the numbers ---------------------------------------------------
    ny = 786
    d.rectangle([MARGIN, ny, W - MARGIN, ny + 34], fill=(233, 228, 210), outline=P["ink"])
    nw = CW / len(NUMBERS)
    for i, (label, value, delta) in enumerate(NUMBERS):
        cx = MARGIN + nw * i
        if i:
            d.line([cx, ny + 4, cx, ny + 32], fill=P["grey"], width=1)
        vt = (value + " " + delta).strip()
        d.text((cx + nw / 2 - d.textlength(vt, font=F_NUM_V) / 2, ny + 4), vt,
               font=F_NUM_V, fill=P["red"] if delta.startswith("-") else P["ink"])
        d.text((cx + nw / 2 - d.textlength(label, font=F_NUM_L) / 2, ny + 23), label,
               font=F_NUM_L, fill=P["grey"])

    # ---- section columns ---------------------------------------------------
    sy = 828
    colw = (CW - 2 * 14) // 3
    for ci, sec in enumerate(SECTION_ORDER):
        cx = MARGIN + ci * (colw + 14)
        d.rectangle([cx, sy, cx + colw, sy + 17], fill=SECTION_COLORS[sec])
        d.text((cx + 6, sy + 2), sec, font=F_SEC, fill=P["white"])
        cy = sy + 23
        for s in [c for c in CARDS if c["section"] == sec]:
            cy = card(d, cx, cy, colw, s)

    # ---- sport strip ---------------------------------------------------------
    py = 954
    d.line([MARGIN, py - 5, W - MARGIN, py - 5], fill=P["ink"], width=1)
    d.text((MARGIN, py), "SPORT", font=F_SMALL_B, fill=P["red"])
    sx = MARGIN + 48
    roww = (W - MARGIN - sx) / len(SPORT)
    for i, s in enumerate(SPORT):
        tx = sx + i * roww
        d.rectangle([tx, py + 3, tx + 5, py + 8], fill=TAG_COLORS[s["tag"]])
        block(d, tx + 9, py, s["head"], F_SMALL, roww - 14, 12, max_lines=1)

    # ---- late wire ticker ------------------------------------------------------
    ly = 972
    d.rectangle([MARGIN, ly, W - MARGIN, ly + 30], outline=P["red"], width=1)
    d.rectangle([MARGIN, ly, MARGIN + 84, ly + 30], fill=P["red"])
    d.text((MARGIN + 8, ly + 2), "LATE", font=F_SEC, fill=P["white"])
    d.text((MARGIN + 8, ly + 16), "WIRE", font=F_SEC, fill=P["white"])
    items = "  ///  ".join(s["head"] for s in TICKER)
    block(d, MARGIN + 92, ly + 4, items, F_SMALL, CW - 100, 12, max_lines=2)

    # ---- date check + colophon ---------------------------------------------------
    fy = 1005
    block(d, MARGIN, fy, DATE_CHECK, F_FINE, CW, 9, fill=(70, 60, 40), max_lines=2)
    return img, total, drawn, len(regions), len(fields)


def main():
    img, total, drawn, nreg, nfield = compose()
    buf1, buf2 = io.BytesIO(), io.BytesIO()
    img.save(buf1, format="PNG", optimize=True)
    img2, *_ = compose()
    img2.save(buf2, format="PNG", optimize=True)
    b1, b2 = buf1.getvalue(), buf2.getvalue()
    assert b1 == b2, "render is not deterministic"
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    with open(out, "wb") as fh:
        fh.write(b1)
    print(f"stories={total} drawn={drawn} regions={nreg} fields={nfield}")
    print(f"entry.png {len(b1)} bytes sha256={hashlib.sha256(b1).hexdigest()}")
    assert len(b1) <= 1048576, "over the 1 MiB cap"


if __name__ == "__main__":
    main()
