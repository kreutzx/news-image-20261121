# Flat vector illustrations drawn in code with PIL ImageDraw.
# Each scene takes (draw, x, y, w, h, P) and paints inside the box.
# One restrained palette for the whole page: cream paper, ink navy,
# signal red, gold, plus muted section hues.

PALETTE = dict(
    paper=(247, 242, 231), ink=(20, 33, 61), red=(179, 39, 30),
    gold=(201, 162, 39), sky=(174, 199, 219), sea=(84, 130, 168),
    land=(148, 168, 120), grey=(110, 110, 110), white=(255, 255, 255),
    teal=(30, 107, 82), plum=(91, 75, 138), brown=(138, 90, 43),
)


def _sky(d, x, y, w, h, P, top=None):
    d.rectangle([x, y, x + w, y + h], fill=top or P["sky"])


def missiles(d, x, y, w, h, P):
    _sky(d, x, y, w, h, P, (38, 48, 84))
    # city skyline
    base = y + h
    bw = w // 9
    for i, bh in enumerate([0.34, 0.5, 0.4, 0.62, 0.45, 0.55, 0.38, 0.5, 0.42]):
        bx = x + i * bw
        d.rectangle([bx, base - h * bh, bx + bw - 3, base], fill=P["ink"])
        for wy in range(int(h * bh) - 8, 6, -9):
            d.rectangle([bx + 3, base - wy - 3, bx + 6, base - wy], fill=P["gold"])
    # missile trails arcing down
    for i, fx in enumerate([0.15, 0.45, 0.75]):
        sx, sy = x + w * fx, y + 4
        ex, ey = x + w * (fx + 0.12), y + h * 0.55
        d.line([sx, sy, ex, ey], fill=P["gold"], width=2)
        d.line([sx + 3, sy, ex + 3, ey], fill=(240, 220, 160), width=1)
        d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=P["red"])
    # interceptor bursts
    for fx, fy in [(0.3, 0.3), (0.62, 0.22)]:
        cx, cy = x + w * fx, y + h * fy
        for dx, dy in [(0, -6), (4, -4), (6, 0), (4, 4), (0, 6), (-4, 4), (-6, 0), (-4, -4)]:
            d.line([cx, cy, cx + dx, cy + dy], fill=P["white"], width=1)


def gavel(d, x, y, w, h, P):
    d.rectangle([x, y, x + w, y + h], fill=(226, 216, 192))
    cx, cy = x + w // 2, y + h // 2
    # scales of justice: post, beam, two hanging pans drawn as bowls
    top = cy - h * 0.4
    d.line([cx, top, cx, cy + h * 0.3], fill=P["ink"], width=3)
    d.line([cx - w * 0.3, top + 4, cx + w * 0.3, top + 4], fill=P["ink"], width=3)
    d.ellipse([cx - 4, top - 4, cx + 4, top + 4], fill=P["gold"])
    for sgn in (-1, 1):
        px = cx + sgn * w * 0.3
        pan_y = cy + h * 0.02
        d.line([px, top + 4, px - 12, pan_y], fill=P["ink"], width=1)
        d.line([px, top + 4, px + 12, pan_y], fill=P["ink"], width=1)
        d.line([px, top + 4, px, pan_y], fill=P["ink"], width=1)
        d.pieslice([px - 13, pan_y - 6, px + 13, pan_y + 10], 0, 180, fill=P["gold"])
        d.rectangle([px - 13, pan_y - 6, px + 13, pan_y], fill=(226, 216, 192))
        d.line([px - 13, pan_y, px + 13, pan_y], fill=P["ink"], width=1)
    d.rectangle([cx - w * 0.16, cy + h * 0.3, cx + w * 0.16, cy + h * 0.38], fill=P["ink"])
    # gavel at lower right, struck diagonally
    gx, gy = x + w * 0.8, y + h * 0.68
    d.line([gx - 14, gy + 12, gx + 10, gy - 12], fill=P["brown"], width=4)
    d.polygon([(gx + 2, gy - 20), (gx + 16, gy - 8), (gx + 8, gy + 2), (gx - 6, gy - 10)], fill=P["brown"])
    d.rectangle([x + w * 0.62, y + h * 0.84, x + w * 0.9, y + h * 0.88], fill=P["ink"])


def chart(d, x, y, w, h, P):
    d.rectangle([x, y, x + w, y + h], fill=(233, 236, 240))
    for i in range(1, 4):
        gy = y + h * i / 4
        d.line([x + 4, gy, x + w - 4, gy], fill=(200, 205, 212), width=1)
    pts = [(x + w * f, y + h * v) for f, v in
           [(0.03, 0.25), (0.2, 0.2), (0.35, 0.34), (0.5, 0.3), (0.65, 0.5), (0.8, 0.62), (0.97, 0.82)]]
    d.line(pts, fill=P["red"], width=3)
    for px, py in pts:
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=P["red"])
    ax, ay = pts[-1]
    d.polygon([(ax, ay + 8), (ax - 7, ay - 3), (ax + 7, ay - 3)], fill=P["red"])
    # falling bars
    for i, bh in enumerate([0.3, 0.42, 0.55, 0.72]):
        bx = x + w * 0.08 + i * w * 0.1
        d.rectangle([bx, y + h * 0.88 - h * bh * 0.4, bx + w * 0.06, y + h * 0.88], fill=P["ink"])


def pill(d, x, y, w, h, P):
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 224))
    cx, cy = x + w // 2, y + h // 2
    # capsule (integer geometry: this PIL build rejects float boxes)
    hw_, hh_ = int(w * 0.22), max(5, int(h * 0.22))
    d.rounded_rectangle([cx - hw_, cy - hh_, cx + hw_, cy + hh_],
                        radius=hh_, fill=P["white"], outline=P["ink"], width=2)
    d.pieslice([cx + hw_ - 2 * hh_, cy - hh_, cx + hw_, cy + hh_], -90, 90, fill=P["teal"])
    d.rectangle([cx, cy - hh_, cx + hw_ - hh_, cy + hh_], fill=P["teal"])
    d.line([cx, cy - hh_, cx, cy + hh_], fill=P["ink"], width=2)
    # tumour dots shrinking away
    for i, (fx, fy, r) in enumerate([(0.12, 0.2, 5), (0.2, 0.75, 4), (0.85, 0.25, 3), (0.8, 0.78, 2)]):
        d.ellipse([x + w * fx - r, y + h * fy - r, x + w * fx + r, y + h * fy + r],
                  outline=P["red"], width=2)
    d.line([x + w * 0.85 - 5, y + h * 0.25 - 5, x + w * 0.85 + 5, y + h * 0.25 + 5], fill=P["red"], width=2)
    d.line([x + w * 0.85 - 5, y + h * 0.25 + 5, x + w * 0.85 + 5, y + h * 0.25 - 5], fill=P["red"], width=2)


def flags(d, x, y, w, h, P):
    d.rectangle([x, y, x + w, y + h], fill=(206, 219, 233))
    # two flags: UK-ish (navy/red cross) and EU-ish (blue/gold stars)
    fx, fy, fw, fh = x + w * 0.08, y + h * 0.18, w * 0.38, h * 0.55
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(36, 52, 110))
    d.line([fx, fy + fh / 2, fx + fw, fy + fh / 2], fill=P["white"], width=5)
    d.line([fx + fw / 2, fy, fx + fw / 2, fy + fh], fill=P["white"], width=5)
    d.line([fx, fy + fh / 2, fx + fw, fy + fh / 2], fill=P["red"], width=2)
    d.line([fx + fw / 2, fy, fx + fw / 2, fy + fh], fill=P["red"], width=2)
    ex = x + w * 0.54
    d.rectangle([ex, fy, ex + fw, fy + fh], fill=(32, 64, 150))
    import math
    for i in range(8):
        a = 2 * math.pi * i / 8
        sx, sy = ex + fw / 2 + math.cos(a) * fw * 0.3, fy + fh / 2 + math.sin(a) * fh * 0.3
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=P["gold"])
    d.line([fx + 2, fy, fx + 2, y + h * 0.92], fill=P["ink"], width=2)
    d.line([ex + 2, fy, ex + 2, y + h * 0.92], fill=P["ink"], width=2)


def globe(d, x, y, w, h, P):
    d.rectangle([x, y, x + w, y + h], fill=(240, 226, 196))
    cx, cy, r = x + w // 2, y + h // 2, int(min(w, h) * 0.42)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=P["sea"], outline=P["ink"], width=2)
    d.ellipse([cx - r * 0.55, cy - r * 0.6, cx - r * 0.05, cy - r * 0.1], fill=P["land"])
    d.ellipse([cx + r * 0.1, cy + r * 0.05, cx + r * 0.6, cy + r * 0.55], fill=P["land"])
    d.ellipse([cx - r * 0.2, cy + r * 0.35, cx + r * 0.25, cy + r * 0.7], fill=P["land"])
    # thermometer
    tx = x + w * 0.86
    d.rounded_rectangle([tx - 3, y + h * 0.12, tx + 3, y + h * 0.7], radius=3, fill=P["white"], outline=P["ink"])
    d.rectangle([tx - 2, y + h * 0.2, tx + 2, y + h * 0.68], fill=P["red"])
    d.ellipse([tx - 6, y + h * 0.66, tx + 6, y + h * 0.66 + 12], fill=P["red"], outline=P["ink"])


def crowd(d, x, y, w, h, P):
    _sky(d, x, y, w, h, P, (196, 210, 226))
    d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(120, 120, 125))
    import random
    rng = random.Random(7)
    for i in range(26):
        px = x + 6 + (w - 12) * (i % 13) / 12 + rng.randint(-2, 2)
        py = y + h * (0.52 if i < 13 else 0.68)
        col = [P["red"], P["ink"], P["gold"], P["teal"], P["plum"]][i % 5]
        d.ellipse([px - 3, py - 8, px + 3, py - 2], fill=(232, 198, 168))
        d.rectangle([px - 4, py - 2, px + 4, py + 8], fill=col)
    # placards
    for fx, txt in [(0.2, "!"), (0.55, "%"), (0.82, "CO2")]:
        px, py = x + w * fx, y + h * 0.16
        d.line([px, py + 12, px, py + 26], fill=P["ink"], width=2)
        d.rectangle([px - 11, py - 8, px + 11, py + 12], fill=P["white"], outline=P["ink"])


def f1(d, x, y, w, h, P):
    d.rectangle([x, y, x + w, y + h], fill=(30, 30, 44))
    # track lights strip (Vegas night)
    for i in range(6):
        lx = x + w * 0.06 + i * w * 0.15
        d.ellipse([lx, y + h * 0.1, lx + 5, y + h * 0.1 + 5], fill=P["gold"])
    gy = y + h * 0.78
    d.rectangle([x, gy, x + w, y + h], fill=(52, 52, 60))
    d.line([x, gy, x + w, gy], fill=P["white"], width=2)
    # car silhouette
    cx, cw = x + w * 0.16, w * 0.68
    d.polygon([(cx, gy - h * 0.1), (cx + cw * 0.25, gy - h * 0.1), (cx + cw * 0.38, gy - h * 0.3),
               (cx + cw * 0.62, gy - h * 0.3), (cx + cw * 0.75, gy - h * 0.12),
               (cx + cw, gy - h * 0.12), (cx + cw, gy - h * 0.04), (cx, gy - h * 0.04)], fill=P["red"])
    d.rectangle([cx + cw * 0.42, gy - h * 0.42, cx + cw * 0.58, gy - h * 0.3], fill=P["ink"])
    d.rectangle([cx - 2, gy - h * 0.34, cx + 4, gy - h * 0.05], fill=P["ink"])
    d.rectangle([cx + cw - 4, gy - h * 0.4, cx + cw + 2, gy - h * 0.05], fill=P["ink"])
    for fx in (0.16, 0.82):
        wx, wy = cx + cw * fx, gy - h * 0.05
        d.ellipse([wx - 8, wy - 8, wx + 8, wy + 8], fill=(10, 10, 10), outline=P["grey"])


SCENES = {
    "missiles": missiles, "gavel": gavel, "chart": chart, "pill": pill,
    "flags": flags, "globe": globe, "crowd": crowd, "f1": f1,
}


def seismo(d, x, y, w, h, P):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 214))
    mid = y + h // 2
    pts = []
    import math
    for i in range(41):
        t = i / 40
        amp = 0.06 + 0.4 * math.exp(-((t - 0.45) ** 2) / 0.004)
        pts.append((x + w * t, mid + math.sin(t * 60) * h * amp))
    d.line(pts, fill=P["red"], width=2)
    d.line([x, mid, x + w, mid], fill=P["grey"], width=1)
    # cracked ground
    d.line([x + w * 0.1, y + h * 0.9, x + w * 0.35, y + h * 0.8, x + w * 0.5, y + h * 0.92,
            x + w * 0.75, y + h * 0.82, x + w * 0.92, y + h * 0.9], fill=P["ink"], width=2)


def probe(d, x, y, w, h, P):
    d.rectangle([x, y, x + w, y + h], fill=(12, 14, 34))
    import random
    rng = random.Random(11)
    for _ in range(28):
        sx, sy = x + rng.randint(2, int(w) - 3), y + rng.randint(2, int(h) - 3)
        d.point([(sx, sy)], fill=P["white"])
        d.point([(sx + 1, sy)], fill=(180, 190, 220))
    cx, cy = x + w * 0.42, y + h * 0.5
    # dish
    d.arc([cx - w * 0.2, cy - h * 0.3, cx + w * 0.05, cy + h * 0.18], 300, 130, fill=P["white"], width=3)
    d.line([cx - w * 0.08, cy - h * 0.05, cx + w * 0.22, cy + h * 0.02], fill=P["gold"], width=2)
    d.line([cx + w * 0.22, cy + h * 0.02, cx + w * 0.34, cy - h * 0.34], fill=P["gold"], width=2)
    d.line([cx + w * 0.22, cy + h * 0.02, cx + w * 0.38, cy + h * 0.2], fill=P["gold"], width=2)
    # signal home
    for i in range(3):
        d.arc([cx - 14 - i * 7, cy - 10 - i * 6, cx - 2 - i * 7, cy + 8 + i * 6], 300, 60, fill=P["sea"], width=2)
    # distant sun dot
    d.ellipse([x + w * 0.88, y + h * 0.72, x + w * 0.88 + 5, y + h * 0.72 + 5], fill=P["gold"])


def mercury(d, x, y, w, h, P):
    d.rectangle([x, y, x + w, y + h], fill=(16, 16, 26))
    cx, cy, r = x + w * 0.38, y + h * 0.52, int(min(w, h) * 0.34)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(168, 158, 148), outline=P["grey"])
    import random
    rng = random.Random(3)
    for _ in range(9):
        a, b = rng.uniform(-0.8, 0.8), rng.uniform(-0.8, 0.8)
        rr = rng.randint(2, 5)
        d.ellipse([cx + a * r - rr, cy + b * r - rr, cx + a * r + rr, cy + b * r + rr], outline=(120, 112, 104))
    # spacecraft: bus + two wings
    sx, sy = x + w * 0.74, y + h * 0.3
    d.rectangle([sx - 5, sy - 5, sx + 5, sy + 5], fill=P["gold"], outline=P["ink"])
    d.polygon([(sx - 5, sy), (sx - 22, sy - 9), (sx - 22, sy + 9)], fill=P["sea"])
    d.polygon([(sx + 5, sy), (sx + 22, sy - 9), (sx + 22, sy + 9)], fill=P["sea"])
    d.line([sx, sy + 5, sx, sy + 14], fill=P["white"], width=2)


def boat(d, x, y, w, h, P):
    _sky(d, x, y, w, h, P)
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=P["sea"])
    import math
    for r in range(3):
        pts = [(x + w * t, y + h * 0.62 + r * h * 0.12 + math.sin(t * 22 + r * 2) * 2.5) for t in
               [i / 24 for i in range(25)]]
        d.line(pts, fill=(210, 228, 240), width=1)
    # capsized hull
    cx, cy = x + w * 0.5, y + h * 0.52
    d.polygon([(cx - w * 0.3, cy), (cx + w * 0.3, cy), (cx + w * 0.12, cy - h * 0.14),
               (cx - w * 0.12, cy - h * 0.14)], fill=P["brown"])
    d.line([cx - w * 0.12, cy - h * 0.14, cx + w * 0.02, cy - h * 0.3], fill=P["ink"], width=2)
    # heads in water + rescue ring
    for fx in (0.2, 0.68, 0.82):
        hx, hy = x + w * fx, y + h * 0.6
        d.ellipse([hx - 3, hy - 3, hx + 3, hy + 3], fill=(232, 198, 168))
    d.ellipse([x + w * 0.36, y + h * 0.6, x + w * 0.36 + 12, y + h * 0.6 + 12], outline=P["red"], width=3)


def swim(d, x, y, w, h, P):
    d.rectangle([x, y, x + w, y + h], fill=P["sea"])
    import math
    for r in range(3):
        pts = [(x + w * t, y + h * (0.25 + r * 0.28) + math.sin(t * 18 + r) * 2) for t in
               [i / 24 for i in range(25)]]
        d.line(pts, fill=(215, 232, 242), width=1)
    # tanker on horizon
    d.rectangle([x + w * 0.62, y + h * 0.08, x + w * 0.95, y + h * 0.16], fill=P["ink"])
    d.rectangle([x + w * 0.7, y + h * 0.02, x + w * 0.78, y + h * 0.08], fill=P["ink"])
    # swimmer: head, cap, arm stroke
    hx, hy = x + w * 0.34, y + h * 0.55
    d.ellipse([hx - 5, hy - 5, hx + 5, hy + 5], fill=(232, 198, 168))
    d.arc([hx - 5, hy - 6, hx + 5, hy + 2], 180, 360, fill=P["red"], width=3)
    d.line([hx + 2, hy + 3, hx + 16, hy - 8], fill=(232, 198, 168), width=4)
    d.line([hx, hy + 4, hx - 14, hy + 8], fill=(232, 198, 168), width=4)


def particle(d, x, y, w, h, P):
    d.rectangle([x, y, x + w, y + h], fill=(20, 22, 40))
    cx, cy = x + w * 0.2, y + h * 0.5
    import math
    for ang, col in [(0.5, P["gold"]), (-0.4, P["sea"]), (1.2, (220, 120, 160)), (-1.1, (140, 220, 180))]:
        pts = []
        for i in range(21):
            t = i / 20
            px = cx + (w * 0.75) * t
            py = cy + math.sin(t * 5 + ang * 4) * h * 0.3 * t + ang * h * 0.22 * t
            pts.append((px, py))
        d.line(pts, fill=col, width=2)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=P["white"])
    # detector rings
    for r in (0.18, 0.3, 0.42):
        d.ellipse([cx - w * r, cy - h * r, cx + w * r, cy + h * r], outline=(90, 95, 130))


def tree(d, x, y, w, h, P):
    _sky(d, x, y, w, h, P, (52, 62, 102))
    cx = x + w // 2
    # obelisk hint at left
    d.polygon([(x + w * 0.08, y + h * 0.85), (x + w * 0.12, y + h * 0.3),
               (x + w * 0.16, y + h * 0.85)], fill=(200, 200, 205))
    # tree tiers
    for i, (tw, ty) in enumerate([(0.52, 0.78), (0.4, 0.56), (0.28, 0.34)]):
        d.polygon([(cx - w * tw / 2, y + h * ty), (cx + w * tw / 2, y + h * ty),
                   (cx, y + h * (ty - 0.24))], fill=(34, 96, 58))
    d.rectangle([cx - 3, y + h * 0.78, cx + 3, y + h * 0.9], fill=P["brown"])
    d.polygon([(cx, y + h * 0.04), (cx - 5, y + h * 0.14), (cx + 5, y + h * 0.14)], fill=P["gold"])
    import random
    rng = random.Random(5)
    for _ in range(22):
        lx = cx + rng.randint(-int(w * 0.22), int(w * 0.22))
        ly = y + rng.randint(int(h * 0.2), int(h * 0.78))
        d.point([(lx, ly)], fill=P["gold"])
        d.point([(lx + 1, ly)], fill=(255, 240, 190))


def shield(d, x, y, w, h, P):
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 210))
    cx, cy = x + w // 2, y + h // 2
    # shield outline
    d.polygon([(cx - w * 0.22, cy - h * 0.34), (cx + w * 0.22, cy - h * 0.34),
               (cx + w * 0.22, cy + h * 0.05), (cx, cy + h * 0.4),
               (cx - w * 0.22, cy + h * 0.05)], fill=P["teal"], outline=P["ink"], width=2)
    # syringe, crossed out by measles spots escaping
    d.line([cx - 10, cy + 8, cx + 8, cy - 12], fill=P["white"], width=5)
    d.line([cx + 8, cy - 12, cx + 13, cy - 17], fill=P["white"], width=2)
    for fx, fy in [(0.78, 0.2), (0.85, 0.45), (0.15, 0.75)]:
        d.ellipse([x + w * fx - 3, y + h * fy - 3, x + w * fx + 3, y + h * fy + 3], fill=P["red"])
        d.ellipse([x + w * fx - 1, y + h * fy - 1, x + w * fx + 1, y + h * fy + 1], fill=(255, 190, 180))


SCENES.update({
    "seismo": seismo, "probe": probe, "mercury": mercury, "boat": boat,
    "swim": swim, "particle": particle, "tree": tree, "shield": shield,
})
