#!/usr/bin/env python3
"""Draw "The World in One Day" for Tuesday 24 November 2026.

A one-page broadsheet, 1024x1024 PNG, summing up the day's world news
for the make.fun news-image-20261124 entry. Every story below was
reported on 24 November 2026 (SCMP, The Japan Times, Times of India).
Deterministic: the same input text gives the same bytes every run.

Run:  python3 draw.py            (writes entry.png beside this file)
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (248, 245, 238)
CARD = (254, 253, 249)
INK = (21, 20, 18)
GREY = (92, 86, 76)
RED = (163, 28, 28)
NAVY = (23, 50, 95)
RULE = (35, 33, 30)
FAINT = (168, 160, 146)
SEA = (38, 84, 124)
SKY = (196, 216, 232)
HULL = (52, 58, 66)
FIRE = (232, 119, 34)
SMOKE = (120, 118, 112)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 36                 # side margin
X1 = W - MX             # right edge of the text block
CW = X1 - MX            # column width


def hline(y, x0=MX, x1=X1, w=2, fill=RULE):
    d.line([(x0, y), (x1, y)], fill=fill, width=w)


def centered(text, y, fnt, fill=INK):
    tw = d.textlength(text, font=fnt)
    d.text(((W - tw) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def wrap(text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def fit_font(text, path, start, max_w, min_size=12):
    size = start
    while size > min_size and d.textlength(text, font=F(path, size)) > max_w:
        size -= 1
    return F(path, size)


def para(text, x, y, fnt, max_w, leading=1.24, fill=INK):
    for ln in wrap(text, fnt, max_w):
        d.text((x, y), ln, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def kicker(text, x, y, fill=RED):
    d.text((x, y), text, font=F(SANS_B, 17), fill=fill)
    return y + 24


# ---------------------------------------------------------------- masthead
y = 20
centered("THE WORLD IN ONE DAY", y, fit_font("THE WORLD IN ONE DAY", SERIF_B, 62, CW))
y += 76
hline(y, w=5)
y += 8
hline(y, w=1)
y += 14
date_f = F(SANS_B, 30)
tw = d.textlength("TUESDAY · 24 NOVEMBER 2026", font=date_f)
d.text(((W - tw) / 2, y), "TUESDAY · 24 NOVEMBER 2026", font=date_f, fill=RED)
y += 40
centered("The day's world news, on one page", y, F(SERIF, 20), fill=GREY)
y += 30
hline(y, w=2)
y += 16

# ---------------------------------------------------------------- lead story
LEAD_TOP = y
SCENE_W = 400
# scene: sky, sea, a warship under attack by sea drones
sx0, sy0, sx1, sy1 = MX, LEAD_TOP, MX + SCENE_W, LEAD_TOP + 200
d.rectangle([sx0, sy0, sx1, sy0 + 84], fill=SKY)
d.rectangle([sx0, sy0 + 84, sx1, sy1], fill=SEA)
for i in range(6):  # wave lines
    wy = sy0 + 100 + i * 14
    d.line([(sx0 + 12 + (i % 3) * 22, wy), (sx0 + 70 + (i % 3) * 22, wy)],
           fill=(120, 165, 200), width=3)
# warship silhouette
ship_y = sy0 + 88
d.polygon([(sx0 + 120, ship_y + 34), (sx0 + 356, ship_y + 34),
           (sx0 + 330, ship_y + 58), (sx0 + 146, ship_y + 58)], fill=HULL)
d.rectangle([sx0 + 176, ship_y + 12, sx0 + 268, ship_y + 34], fill=HULL)
d.rectangle([sx0 + 250, ship_y - 6, sx0 + 292, ship_y + 12], fill=HULL)
d.line([(sx0 + 200, ship_y + 12), (sx0 + 200, ship_y - 26)], fill=HULL, width=4)
d.line([(sx0 + 200, ship_y - 26), (sx0 + 232, ship_y - 12)], fill=HULL, width=3)
# explosion and smoke at the stern
ex, ey = sx0 + 322, ship_y + 6
for dx, dy in [(0, -20), (14, -12), (18, 4), (8, 16), (-10, 14), (-16, -2), (-8, -14)]:
    d.line([(ex, ey), (ex + dx, ey + dy)], fill=FIRE, width=5)
d.ellipse([ex - 9, ey - 9, ex + 9, ey + 9], fill=FIRE)
for r, off in [(15, 4), (22, 20), (30, 38)]:
    d.ellipse([ex + off - r // 2, ey - 26 - off // 2 - r // 2,
               ex + off + r // 2, ey - 26 - off // 2 + r // 2], fill=SMOKE)
# two sea drones closing in, with wakes
for bx, by in [(sx0 + 44, ship_y + 58), (sx0 + 96, ship_y + 80)]:
    d.polygon([(bx, by), (bx + 44, by), (bx + 34, by + 10), (bx + 8, by + 10)], fill=(30, 34, 40))
    d.line([(bx - 26, by + 12), (bx + 4, by + 10)], fill=(210, 228, 240), width=3)
    d.line([(bx - 16, by + 20), (bx + 8, by + 14)], fill=(210, 228, 240), width=2)
d.rectangle([sx0, sy0, sx1, sy1], outline=RULE, width=2)
d.text((sx0 + 10, sy0 + 8), "Sea drones strike at Benghazi",
       font=F(SANS_B, 16), fill=NAVY)

tx = MX + SCENE_W + 26
tw_w = X1 - tx
y2 = kicker("UKRAINE WAR · MEDITERRANEAN", tx, LEAD_TOP + 2)
lead_head = F(SERIF_B, 43)
for ln in wrap("Ukraine sinks Russian warship off Libya", lead_head, tw_w):
    d.text((tx, y2), ln, font=lead_head, fill=INK)
    y2 += 46
y2 += 6
para("Seven sea drones strike at Benghazi, destroying a Ka-27 helicopter "
     "and hitting the cargo ship Angara. Russian strikes kill at least "
     "12 in the Kyiv region.",
     tx, y2, F(SANS, 22), tw_w, leading=1.26)
y = LEAD_TOP + 214
hline(y, w=2)
y += 14

# ---------------------------------------------------------------- story grid
PANELS = [
    ("WASHINGTON", "Democrats win biggest House majority since 1992",
     "At least 258 seats — enough to block Trump's agenda in his final "
     "two years."),
    ("SPACE", "NATO vows space defence over Russian weapon fears",
     "Moscow may launch a satellite-killing nuclear weapon within "
     "weeks, allies say."),
    ("TECH", "Nvidia reinstates Huang as CEO in stunning reversal",
     "Jensen Huang returns after lobbying by JD Vance at Trump's "
     "behest."),
    ("SEOUL", "South Korea scrambles jets as Russian planes enter air zone",
     "A suspected North Korean aircraft also breaches airspace near "
     "Ulleung."),
    ("DHAKA", "Hasina seeks return to Bangladesh — and a death sentence",
     "The ousted PM wants to come home, where she faces a death "
     "sentence."),
    ("SPORT", "US to host 2031 Women's World Cup with three neighbours",
     "Mexico, Costa Rica and Jamaica co-host; the UK is awarded the "
     "2035 edition."),
]
COLS = 3
GAP = 16
PW = (CW - GAP * (COLS - 1)) // COLS
PH = 192


def panel_head_font(text, max_w):
    """Largest serif-bold size, 25 down, whose wrap of text is <= 3 lines."""
    size = 25
    while size > 19 and len(wrap(text, F(SERIF_B, size), max_w)) > 3:
        size -= 1
    return F(SERIF_B, size)


for i, (kick, head, body) in enumerate(PANELS):
    px = MX + (i % COLS) * (PW + GAP)
    py = y + (i // COLS) * (PH + GAP)
    d.rectangle([px, py, px + PW, py + PH], fill=CARD, outline=FAINT, width=1)
    d.rectangle([px, py, px + PW, py + 5], fill=NAVY if i % 2 == 0 else RED)
    ky = kicker(kick, px + 14, py + 13)
    hy = ky + 1
    hf = panel_head_font(head, PW - 28)
    for ln in wrap(head, hf, PW - 28):
        d.text((px + 14, hy), ln, font=hf, fill=INK)
        hy += int(hf.size * 1.12)
    para(body, px + 14, hy + 5, F(SANS, 18), PW - 28, leading=1.22,
         fill=(45, 43, 40))
y += 2 * PH + GAP + 12

# ---------------------------------------------------------------- WFP strip
hline(y, w=2)
y += 13
d.text((MX, y), "UNITED NATIONS · FOOD", font=F(SANS_B, 17), fill=RED)
wfp = ("Wars put food aid for 7.3 million more people at risk, "
       "the UN food agency's chief warns")
d.text((MX + 252, y - 5), wfp,
       font=fit_font(wfp, SERIF_B, 24, CW - 252), fill=INK)
y += 40

# ---------------------------------------------------------------- also today
hline(y, w=2)
y += 12
d.text((MX, y), "ALSO TODAY", font=F(SANS_B, 19), fill=RED)
src = "Drawn from the day's reporting · SCMP · The Japan Times · Times of India"
d.text((X1 - d.textlength(src, font=F(SANS, 15)), y + 2), src,
       font=F(SANS, 15), fill=GREY)
y += 30
also = ("Thousands evacuated from a UK concert after an unknown substance "
        "is released  ·  Israel's leadership rivals clash over Iran ahead "
        "of coalition talks  ·  GTA VI hacker jailed for seven years in "
        "London  ·  Honda recalls 810,000 vehicles in the US over airbag "
        "rupture risk")
y = para(also, MX, y, F(SANS, 19), CW, leading=1.25, fill=(45, 43, 40))
assert y < H - 8, f"layout overflow: content ends at y={y}"

img.save("/home/hatch/workspace/makefun-setup/bot16/repo/entry.png", optimize=True)
print("saved entry.png")
