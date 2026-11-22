#!/usr/bin/env python3
"""Render the news-image-20261122 entry: one 1024x1024 PNG summing up
Sunday 22 November 2026. Build-time only; the committed entry.png is what
main.py validates and copies. Stories are shortened wire headlines with
figures as reported on 22 Nov 2026 (incl. late 21 Nov UTC = 22 Nov in
Asia/Oceania). Nothing invented: every line traces to a 22 Nov report.
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FONTS = "/usr/share/fonts/truetype"
F_SERIF = os.path.join(FONTS, "dejavu/DejaVuSerif-Bold.ttf")
F_SANS = os.path.join(FONTS, "dejavu/DejaVuSans.ttf")
F_SANSB = os.path.join(FONTS, "dejavu/DejaVuSans-Bold.ttf")
F_SERIFR = os.path.join(FONTS, "dejavu/DejaVuSerif.ttf")

INK = (26, 24, 22)
PAPER = (250, 247, 240)
RED = (178, 34, 34)
BLUE = (28, 74, 140)
TEAL = (16, 120, 110)
GOLD = (196, 138, 20)
GREY = (110, 105, 98)

# (number, region, field, headline, detail, icon, map_xy or None)
# icon: key into ICONS. map_xy: (x, y) in 0..1 world-map space.
STORIES = [
    (1, "Europe", "Climate", "COP31 deadlocked on fossil fuels",
     "Antalya talks 36h into overtime; ~200 nations split", "globe", (0.53, 0.36)),
    (2, "Middle East", "Conflict", "Iran strikes US base in Kuwait",
     "Bahrain industrial site ablaze after attack", "flame", (0.585, 0.42)),
    (3, "Europe", "Conflict", "Russian strikes kill at least 2 in Ukraine",
     "Overnight attacks across the country", "burst", (0.56, 0.30)),
    (4, "North America", "Crime", "Mexico captures 'El Chapo Isidro'",
     "FBI most-wanted; 11 killed in violence after arrest", "cuffs", (0.16, 0.45)),
    (5, "South America", "Disaster", "M6.9 quake shakes Peru's Andes",
     "No damage or casualties immediately reported", "quake", (0.24, 0.66)),
    (6, "North America", "Disaster", "Florida river at record flood",
     "St Johns spreading Sunday; 270+ rescued by airboat", "wave", (0.20, 0.40)),
    (7, "Asia", "Politics", "Modi opens Nitish Setu bridge",
     "Patna-Vaishali link named for Nitish Kumar", "bridge", (0.68, 0.44)),
    (8, "North America", "Health", "Virginia child dies of measles",
     "First such death in the state since 1978", "cross", (0.21, 0.36)),
    (9, "Europe", "Politics", "Thousands march in Lisbon",
     "Living costs fuel anger in Portugal's capital", "march", (0.475, 0.38)),
    (10, "Europe", "Economy", "German union calls 24-hour strike",
     "IG Metall: 23,000 workers, 19 firms, from Monday", "gear", (0.50, 0.31)),
    (11, "Asia", "Politics", "Trump in Shenzhen for APEC",
     "Trilateral talks planned with Xi and Putin", "podium", (0.76, 0.45)),
    (12, "Middle East", "Conflict", "ADNOC vessel attacked in Hormuz",
     "One crew member reported missing", "ship", (0.59, 0.44)),
    (13, "Europe", "Politics", "Estonia to close Russia border",
     "Moscow decries a 'new Iron Curtain'", "gate", (0.555, 0.27)),
    (14, "South America", "Disaster", "Brazil supercell storm kills 3",
     "Tupancireta: thousands of buildings damaged", "storm", (0.27, 0.76)),
    (15, "Asia", "Disaster", "Cyclone Akvan: 300,000 evacuated",
     "Odisha shelters; 14 flights cut at Ranchi", "cyclone", (0.70, 0.47)),
    (16, "Asia", "Defence", "Japan to train live-fire in India",
     "First use of Indian facilities by Japanese forces", "target", (0.72, 0.43)),
    (17, "Europe", "Politics", "France + US draft UNIFIL plan",
     "UN resolution to fill post-UNIFIL vacuum", "dove", (0.56, 0.40)),
    (18, "North America", "Politics", "US open to Latin UN chief",
     "Waltz 'would welcome' regional secretary-general", "dove", (0.20, 0.34)),
    (19, "Europe", "Economy", "EU budget plan cut by $224B",
     "Council leader proposes leaner 2028-34 draft", "chart", (0.50, 0.33)),
    (20, "Asia", "Technology", "China fines Baidu $96,600",
     "Penalty over live-streaming acquisition", "chip", (0.75, 0.40)),
    (21, "Middle East", "Disaster", "Basra power plant fire kills 4",
     "Dozens injured at Iraqi electricity facility", "flame", (0.58, 0.40)),
    (22, "Europe", "Politics", "France protests reach 6th week",
     "Turnout falls to 82,500, reports say", "march", (0.485, 0.34)),
    (23, "Asia", "Health", "ICMR seals 100 tech transfers",
     "20 licensing deals at health research summit", "cross", (0.69, 0.46)),
    (24, "Asia", "Nature", "Prince William backs forest cover",
     "Insurance scheme for 10,000 forest personnel", "tree", (0.685, 0.45)),
    (25, "Asia", "Politics", "Nepal PM's first India visit",
     "Balendra Shah to meet Modi bilaterally", "podium", (0.695, 0.42)),
    (26, "Africa", "Politics", "ANC at 31% races to hold cities",
     "Coalition deals due by 27 November", "ballot", (0.52, 0.72)),
    (27, "North America", "Technology", "FBI probes database hack",
     "Criminal justice system breach investigated", "chip", (0.19, 0.37)),
    (28, "Europe", "Conflict", "Denmark: Russia plotted killing",
     "Assassination plot alleged on Danish soil", "burst", (0.505, 0.29)),
    (29, "Europe", "Conflict", "Kerch Bridge hit 'fair response'",
     "Zelenskyy meets UK's Streeting in Kyiv", "bridge", (0.565, 0.32)),
    (30, "North America", "Economy", "S&P 500 sinks 3.7% in tech rout",
     "Nasdaq negative for the year, AP reports", "chart", (0.20, 0.35)),
    (31, "North America", "Technology", "Anthropic shares fall post-IPO",
     "Pullback a day after blockbuster listing", "chart", (0.195, 0.39)),
    (32, "North America", "Technology", "Trump: tax overseas AI centres",
     "Ban threatened on data centres built abroad", "chip", (0.21, 0.38)),
    (33, "Asia", "Economy", "Crude futures slide over 3%",
     "Down to Rs 7,842 a barrel", "chart", (0.71, 0.50)),
    (34, "Asia", "Economy", "Sensex ends two-day rally",
     "Profit booking amid Fed rate concerns", "chart", (0.69, 0.48)),
    (35, "Europe", "Sport", "Real Madrid 2-1 Celta Vigo",
     "Late winner at the Bernabeu", "ball", (0.48, 0.39)),
    (36, "Europe", "Sport", "Newcastle 2-2 Arsenal",
     "Points shared in Premier League thriller", "ball", (0.49, 0.30)),
    (37, "Oceania", "Sport", "Australia end England T20 run",
     "191/7 chases 187/9; streak of 7 broken", "bat", (0.84, 0.78)),
    (38, "Oceania", "Sport", "Cummins backed as Test captain",
     "Cricket Australia's 'unanimous support'", "bat", (0.845, 0.76)),
    (39, "Oceania", "Sport", "India Test in windy Wellington",
     "KL Rahul in focus for series opener", "bat", (0.90, 0.84)),
    (40, "Europe", "Sport", "Zverev beats Medvedev in Turin",
     "ATP Finals semi: 7-6 6-4", "racket", (0.50, 0.35)),
    (41, "Europe", "Sport", "Nadal joins Real Madrid board",
     "Approved by 99.5% of members", "ball", (0.482, 0.40)),
    (42, "North America", "Justice", "Palisades arsonist convicted",
     "Fire killed 12, destroyed ~6,800 buildings", "flame", (0.12, 0.38)),
    (43, "Europe", "Culture", "Oslo tree sails for Trafalgar Sq",
     "Annual Christmas tree sets off for London", "tree", (0.495, 0.28)),
    (44, "Europe", "Culture", "'Cancer changes you' - Kate",
     "Princess reflects in new documentary", "cross", (0.49, 0.31)),
    (45, "Middle East", "Politics", "Eisenkot backed against Bibi",
     "Ex-PM: won't serve under Netanyahu", "ballot", (0.565, 0.41)),
    (46, "Asia", "Politics", "Cricketer Chahal joins BJP",
     "Named to OBC Morcha committee", "bat", (0.695, 0.44)),
    (47, "Asia", "Culture", "IFFI adds animation section",
     "57th festival screens 5 international films", "film", (0.70, 0.49)),
    (48, "Asia", "Disaster", "Indonesia floods displace 6,133",
     "Four deaths in GDACS assessment", "wave", (0.76, 0.60)),
    (49, "Europe", "Justice", "French police jailed for beating",
     "2020 Zecler attack; racism an aggravating factor", "cuffs", (0.487, 0.33)),
    (50, "Asia", "Disaster", "M6.8 quake near Timor-Leste",
     "Deep tremor; no tsunami threat", "quake", (0.80, 0.63)),
]

ILLUSTRATED = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 26, 28, 35,
               37, 42, 43, 48, 50]  # 22 panels
HERO = 1


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def badge(d, x, y, n, r=11):
    d.ellipse([x - r, y - r, x + r, y + r], fill=RED, outline=PAPER, width=2)
    f = font(F_SANSB, 13)
    d.text((x, y), str(n), font=f, fill=PAPER, anchor="mm")


# --- tiny flat icons, drawn in a box (x0,y0,x1,y1) -------------------------
def icon(d, kind, box, col):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    s = min(x1 - x0, y1 - y0)
    if kind == "globe":
        d.ellipse([cx - s * .42, cy - s * .42, cx + s * .42, cy + s * .42], outline=col, width=3)
        d.ellipse([cx - s * .18, cy - s * .42, cx + s * .18, cy + s * .42], outline=col, width=2)
        d.line([cx - s * .42, cy, cx + s * .42, cy], fill=col, width=2)
    elif kind == "flame":
        d.polygon([(cx, y0 + s * .08), (cx + s * .3, cy + s * .1), (cx + s * .18, y1 - s * .08),
                   (cx - s * .18, y1 - s * .08), (cx - s * .3, cy + s * .1)], fill=col)
        d.ellipse([cx - s * .12, cy + s * .05, cx + s * .12, y1 - s * .12], fill=GOLD)
    elif kind == "burst":
        for a in range(0, 360, 45):
            r = math.radians(a)
            d.line([cx, cy, cx + math.cos(r) * s * .42, cy + math.sin(r) * s * .42], fill=col, width=3)
        d.ellipse([cx - s * .13, cy - s * .13, cx + s * .13, cy + s * .13], fill=col)
    elif kind == "cuffs":
        d.ellipse([x0 + s * .08, cy - s * .2, x0 + s * .48, cy + s * .2], outline=col, width=4)
        d.ellipse([x1 - s * .48, cy - s * .2, x1 - s * .08, cy + s * .2], outline=col, width=4)
        d.line([x0 + s * .44, cy - s * .08, x1 - s * .44, cy - s * .08], fill=col, width=3)
    elif kind == "quake":
        pts = [(x0 + s * .05, cy), (x0 + s * .3, cy - s * .3), (cx, cy + s * .3),
               (x0 + s * .7, cy - s * .3), (x1 - s * .05, cy)]
        d.line(pts, fill=col, width=4, joint="curve")
    elif kind == "wave":
        for i, yy in enumerate((cy - s * .18, cy + s * .08)):
            pts = [(x0 + s * .05 + j * s * .09, yy + math.sin(j * 1.2 + i) * s * .07) for j in range(11)]
            d.line(pts, fill=col, width=3)
    elif kind == "bridge":
        d.arc([x0 + s * .05, cy - s * .1, x1 - s * .05, y1 - s * .05], 180, 360, fill=col, width=4)
        d.line([x0 + s * .05, cy + s * .12, x1 - s * .05, cy + s * .12], fill=col, width=4)
        for fx in (.25, .5, .75):
            d.line([x0 + s * fx, cy - s * .05, x0 + s * fx, cy + s * .12], fill=col, width=2)
    elif kind == "cross":
        w = s * .16
        d.rectangle([cx - w / 2, y0 + s * .12, cx + w / 2, y1 - s * .12], fill=col)
        d.rectangle([x0 + s * .12, cy - w / 2, x1 - s * .12, cy + w / 2], fill=col)
    elif kind == "march":
        for fx in (.25, .5, .75):
            px = x0 + s * fx
            d.ellipse([px - s * .07, y0 + s * .18, px + s * .07, y0 + s * .32], fill=col)
            d.line([px, y0 + s * .32, px, y1 - s * .18], fill=col, width=4)
        d.rectangle([x0 + s * .12, y0 + s * .06, x1 - s * .12, y0 + s * .16], fill=col)
    elif kind == "gear":
        d.ellipse([cx - s * .3, cy - s * .3, cx + s * .3, cy + s * .3], outline=col, width=5)
        for a in range(0, 360, 45):
            r = math.radians(a)
            d.line([cx + math.cos(r) * s * .3, cy + math.sin(r) * s * .3,
                    cx + math.cos(r) * s * .44, cy + math.sin(r) * s * .44], fill=col, width=5)
    elif kind == "podium":
        d.rectangle([x0 + s * .18, cy, x1 - s * .18, y1 - s * .1], outline=col, width=3)
        d.ellipse([cx - s * .1, y0 + s * .12, cx + s * .1, y0 + s * .32], fill=col)
        d.line([cx, y0 + s * .32, cx, cy], fill=col, width=4)
    elif kind == "ship":
        d.polygon([(x0 + s * .1, cy + s * .1), (x1 - s * .1, cy + s * .1),
                   (x1 - s * .25, y1 - s * .12), (x0 + s * .25, y1 - s * .12)], fill=col)
        d.rectangle([cx - s * .16, cy - s * .22, cx + s * .16, cy + s * .1], outline=col, width=3)
    elif kind == "gate":
        d.rectangle([x0 + s * .15, y0 + s * .15, x1 - s * .15, y1 - s * .1], outline=col, width=4)
        d.line([cx, y0 + s * .15, cx, y1 - s * .1], fill=col, width=3)
        d.line([x0 + s * .15, cy, x1 - s * .15, cy], fill=RED, width=4)
    elif kind == "storm":
        d.ellipse([x0 + s * .1, y0 + s * .12, x1 - s * .1, cy + s * .05], fill=col)
        d.polygon([(cx + s * .05, cy), (cx - s * .12, cy + s * .3), (cx + s * .02, cy + s * .3),
                   (cx - s * .08, y1 - s * .06), (cx + s * .18, cy + s * .22), (cx + s * .04, cy + s * .22)], fill=GOLD)
    elif kind == "cyclone":
        for r in (.42, .3, .18):
            d.arc([cx - s * r, cy - s * r, cx + s * r, cy + s * r], 20, 300, fill=col, width=4)
    elif kind == "target":
        for r in (.42, .28, .14):
            d.ellipse([cx - s * r, cy - s * r, cx + s * r, cy + s * r], outline=col, width=3)
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)
    elif kind == "dove":
        d.polygon([(x0 + s * .15, cy + s * .1), (cx, y0 + s * .15), (x1 - s * .2, cy - s * .05),
                   (x1 - s * .1, cy + s * .15), (cx, cy + s * .25)], fill=col)
        d.ellipse([x0 + s * .12, cy - s * .02, x0 + s * .3, cy + s * .16], fill=col)
    elif kind == "chart":
        pts = [(x0 + s * .1, y1 - s * .25), (x0 + s * .35, cy + s * .05),
               (x0 + s * .6, y1 - s * .3), (x1 - s * .1, y0 + s * .2)]
        d.line(pts, fill=col, width=4)
        d.polygon([(x1 - s * .1, y0 + s * .2), (x1 - s * .3, y0 + s * .22), (x1 - s * .12, y0 + s * .4)], fill=col)
    elif kind == "chip":
        d.rectangle([cx - s * .25, cy - s * .25, cx + s * .25, cy + s * .25], outline=col, width=4)
        for fx in (.3, .5, .7):
            d.line([x0 + s * fx, cy - s * .25, x0 + s * fx, y0 + s * .08], fill=col, width=3)
            d.line([x0 + s * fx, cy + s * .25, x0 + s * fx, y1 - s * .08], fill=col, width=3)
    elif kind == "tree":
        d.polygon([(cx, y0 + s * .08), (cx + s * .3, cy + s * .1), (cx - s * .3, cy + s * .1)], fill=col)
        d.rectangle([cx - s * .05, cy + s * .1, cx + s * .05, y1 - s * .1], fill=(120, 80, 40))
    elif kind == "ballot":
        d.rectangle([x0 + s * .15, cy, x1 - s * .15, y1 - s * .1], outline=col, width=4)
        d.rectangle([cx - s * .18, y0 + s * .1, cx + s * .18, cy + s * .05], outline=col, width=3)
        d.line([cx - s * .08, y0 + s * .3, cx - s * .02, y0 + s * .42], fill=RED, width=3)
        d.line([cx - s * .02, y0 + s * .42, cx + s * .12, y0 + s * .18], fill=RED, width=3)
    elif kind == "ball":
        d.ellipse([cx - s * .38, cy - s * .38, cx + s * .38, cy + s * .38], outline=col, width=3)
        d.polygon([(cx, cy - s * .14), (cx + s * .13, cy - s * .04), (cx + s * .08, cy + s * .12),
                   (cx - s * .08, cy + s * .12), (cx - s * .13, cy - s * .04)], fill=col)
    elif kind == "bat":
        d.line([x0 + s * .2, y1 - s * .15, x1 - s * .2, y0 + s * .15], fill=col, width=6)
        d.ellipse([x1 - s * .35, y0 + s * .1, x1 - s * .15, y0 + s * .3], fill=RED)
    elif kind == "racket":
        d.ellipse([cx - s * .3, y0 + s * .08, cx + s * .3, cy + s * .15], outline=col, width=4)
        d.line([cx, cy + s * .15, cx, y1 - s * .08], fill=col, width=5)
    elif kind == "film":
        d.rectangle([x0 + s * .12, y0 + s * .15, x1 - s * .12, y1 - s * .15], outline=col, width=4)
        d.polygon([(cx - s * .1, cy - s * .15), (cx - s * .1, cy + s * .15), (cx + s * .18, cy)], fill=col)
    else:
        d.ellipse([cx - s * .3, cy - s * .3, cx + s * .3, cy + s * .3], outline=col, width=3)


def world_map(d, box):
    """Stylised world map: continent blobs in Robinson-ish layout."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(214, 228, 240), outline=INK, width=2)
    land = (150, 175, 140)
    def blob(pts):
        d.polygon([(x0 + (x1 - x0) * px, y0 + (y1 - y0) * py) for px, py in pts], fill=land)
    blob([(0.03, 0.30), (0.10, 0.16), (0.22, 0.14), (0.30, 0.22), (0.29, 0.36), (0.24, 0.44), (0.17, 0.42), (0.10, 0.48), (0.05, 0.40)])  # N America
    blob([(0.24, 0.50), (0.30, 0.52), (0.33, 0.62), (0.30, 0.78), (0.26, 0.88), (0.23, 0.72), (0.22, 0.58)])  # S America
    blob([(0.44, 0.22), (0.50, 0.16), (0.56, 0.20), (0.55, 0.32), (0.49, 0.34), (0.45, 0.30)])  # Europe
    blob([(0.46, 0.38), (0.56, 0.36), (0.60, 0.48), (0.57, 0.66), (0.52, 0.80), (0.48, 0.62), (0.45, 0.48)])  # Africa
    blob([(0.57, 0.16), (0.78, 0.12), (0.90, 0.22), (0.88, 0.38), (0.78, 0.48), (0.70, 0.56), (0.64, 0.44), (0.58, 0.36)])  # Asia
    blob([(0.80, 0.66), (0.90, 0.64), (0.92, 0.76), (0.84, 0.82), (0.79, 0.74)])  # Oceania
    for st in STORIES:
        if st[6]:
            px = x0 + (x1 - x0) * st[6][0]
            py = y0 + (y1 - y0) * st[6][1]
            badge(d, px, py, st[0], r=10)


def masthead(d, y=14):
    d.text((W / 2, y), "THE WORLD IN ONE PICTURE", font=font(F_SERIF, 34), fill=INK, anchor="ma")
    d.text((W / 2, y + 44), "Sunday 22 November 2026  -  50 stories, 22 illustrated, one map",
           font=font(F_SANSB, 19), fill=RED, anchor="ma")
    d.line([24, y + 74, W - 24, y + 74], fill=INK, width=3)
    d.line([24, y + 79, W - 24, y + 79], fill=INK, width=1)


def panel(d, box, st, big=False):
    x0, y0, x1, y1 = box
    d.rectangle(box, outline=INK, width=2, fill=(255, 255, 255))
    n, region, field, head, detail, ic, _ = st
    badge(d, x0 + 14, y0 + 14, n)
    icon(d, ic, (x0 + 6, y0 + 24, x0 + 58, y0 + 76), BLUE if n % 2 else TEAL)
    hf = font(F_SANSB, 15 if big else 13)
    df = font(F_SANS, 11)
    lines = wrap(d, head, hf, x1 - x0 - 70)
    ty = y0 + 6
    for ln in lines[:3]:
        d.text((x0 + 64, ty), ln, font=hf, fill=INK)
        ty += 16
    for ln in wrap(d, detail, df, x1 - x0 - 70)[:2]:
        d.text((x0 + 64, ty), ln, font=df, fill=GREY)
        ty += 13
    d.text((x0 + 8, y1 - 16), f"{region} - {field}", font=font(F_SANS, 9), fill=GREY)


def hero(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(30, 52, 84), outline=INK, width=2)
    # night negotiating hall: table, flags, clock past deadline
    cx = (x0 + x1) / 2
    d.ellipse([x1 - 92, y0 + 12, x1 - 32, y0 + 72], outline=PAPER, width=3)
    d.line([x1 - 62, y0 + 42, x1 - 62, y0 + 24], fill=PAPER, width=3)
    d.line([x1 - 62, y0 + 42, x1 - 44, y0 + 50], fill=RED, width=3)
    d.text((x1 - 62, y0 + 76), "36h over", font=font(F_SANSB, 11), fill=PAPER, anchor="ma")
    for i in range(7):
        fx = x0 + 30 + i * ((x1 - x0 - 60) / 6)
        d.line([fx, y1 - 58, fx, y1 - 92], fill=PAPER, width=2)
        d.rectangle([fx, y1 - 92, fx + 18, y1 - 80], fill=[RED, GOLD, TEAL, PAPER, BLUE, RED, GOLD][i])
    d.rectangle([x0 + 24, y1 - 56, x1 - 24, y1 - 34], fill=(120, 86, 50))
    for i in range(9):
        px = x0 + 40 + i * ((x1 - x0 - 80) / 8)
        d.ellipse([px - 8, y1 - 78, px + 8, y1 - 62], fill=PAPER)
        d.rectangle([px - 9, y1 - 62, px + 9, y1 - 56], fill=PAPER)
    badge(d, x0 + 18, y0 + 18, HERO, r=13)
    d.text((x0 + 40, y0 + 10), "COP31 DEADLOCKED ON FOSSIL FUELS", font=font(F_SERIF, 20), fill=PAPER)
    d.text((x0 + 40, y0 + 40), "Antalya talks run 36 hours past deadline;",
           font=font(F_SANS, 13), fill=(220, 228, 240))
    d.text((x0 + 40, y0 + 58), "~200 nations split over oil, gas and coal",
           font=font(F_SANS, 13), fill=(220, 228, 240))
    d.text((x0 + 40, y0 + 76), "EU + Pacific states push back on draft",
           font=font(F_SANS, 13), fill=(220, 228, 240))


def index_block(d, box, cols=3):
    x0, y0, x1, y1 = box
    d.rectangle(box, outline=INK, width=2, fill=(255, 255, 255))
    f = font(F_SANS, 9.5)
    colw = (x1 - x0 - 16) / cols
    per = math.ceil(len(STORIES) / cols)
    lh = max(11.0, (y1 - y0 - 12) / per)
    for i, st in enumerate(STORIES):
        c, r = divmod(i, per)
        tx, ty = x0 + 8 + c * colw, y0 + 6 + r * lh
        label = f"{st[0]}. {st[3]}"
        while d.textlength(label, font=f) > colw - 6 and " " in label:
            label = label.rsplit(" ", 1)[0]
        d.text((tx, ty), label, font=f, fill=INK)


def layout_a():
    """Broadsheet: masthead, hero, map, 22 panels, 50-index."""
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    masthead(d)
    hero(d, (24, 100, 640, 300))
    world_map(d, (652, 100, 1000, 300))
    d.text((652, 304), "Numbers match panels + index", font=font(F_SANS, 10), fill=GREY)
    ill = [s for s in STORIES if s[0] in ILLUSTRATED and s[0] != HERO]
    pw, ph = 238, 88
    for i, st in enumerate(ill):
        c, r = i % 4, i // 4
        panel(d, (24 + c * (pw + 8), 322 + r * (ph + 6), 24 + c * (pw + 8) + pw, 322 + r * (ph + 6) + ph), st)
    index_block(d, (24, 322 + 6 * (ph + 6) + 4, 1000, 1000), cols=5)
    return im


def layout_b():
    """Map-hero: giant map top, hero strip, panels, index."""
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    masthead(d)
    world_map(d, (24, 100, 1000, 420))
    hero(d, (24, 428, 1000, 540))
    ill = [s for s in STORIES if s[0] in ILLUSTRATED and s[0] != HERO][:12]
    pw, ph = 238, 96
    for i, st in enumerate(ill):
        c, r = i % 4, i // 4
        panel(d, (24 + c * (pw + 8), 548 + r * (ph + 6), 24 + c * (pw + 8) + pw, 548 + r * (ph + 6) + ph), st)
    index_block(d, (24, 856, 1000, 1000))
    return im


def layout_c():
    """Panels-only grid: 24 big panels, thin index, small map."""
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    masthead(d)
    ill = [s for s in STORIES if s[0] in ILLUSTRATED]
    pw, ph = 316, 92
    for i, st in enumerate(ill):
        c, r = i % 3, i // 3
        panel(d, (24 + c * (pw + 8), 100 + r * (ph + 6), 24 + c * (pw + 8) + pw, 100 + r * (ph + 6) + ph), st, big=True)
    world_map(d, (24, 100 + 8 * (ph + 6), 480, 1000))
    index_block(d, (488, 100 + 8 * (ph + 6), 1000, 1000), cols=2)
    return im


def layout_d():
    """Single collage scene: globe centre, callouts, index."""
    im = Image.new("RGB", (W, H), (30, 52, 84))
    d = ImageDraw.Draw(im)
    d.text((W / 2, 18), "Sunday 22 November 2026", font=font(F_SERIF, 36), fill=PAPER, anchor="ma")
    d.ellipse([312, 90, 712, 490], fill=(70, 130, 180), outline=PAPER, width=3)
    icon(d, "globe", (412, 190, 612, 390), PAPER)
    ill = [s for s in STORIES if s[0] in ILLUSTRATED][:10]
    for i, st in enumerate(ill):
        a = math.radians(i * 36 - 90)
        px, py = 512 + math.cos(a) * 360, 290 + math.sin(a) * 190
        badge(d, px, py, st[0], r=13)
        d.text((px, py + 16), st[3][:26], font=font(F_SANS, 10), fill=PAPER, anchor="ma")
    index_block(d, (24, 520, 1000, 1000), cols=3)
    return im


def layout_e():
    """Timeline by region: 7 region columns with story chips."""
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    masthead(d)
    regions = ["Europe", "Asia", "North America", "South America", "Africa", "Middle East", "Oceania"]
    cw = (W - 48) / 7
    for ci, reg in enumerate(regions):
        x0 = 24 + ci * cw
        d.rectangle([x0, 100, x0 + cw - 4, 130], fill=BLUE)
        d.text((x0 + cw / 2, 106), reg, font=font(F_SANSB, 11), fill=PAPER, anchor="ma")
        rows = [s for s in STORIES if s[1] == reg]
        for ri, st in enumerate(rows):
            y0 = 136 + ri * 62
            d.rectangle([x0, y0, x0 + cw - 4, y0 + 58], outline=INK, fill=(255, 255, 255))
            badge(d, x0 + 12, y0 + 12, st[0], r=9)
            icon(d, st[5], (x0 + 4, y0 + 20, x0 + 34, y0 + 52), TEAL)
            for li, ln in enumerate(wrap(d, st[3], font(F_SANS, 9), cw - 44)[:3]):
                d.text((x0 + 38, y0 + 4 + li * 11), ln, font=font(F_SANS, 9), fill=INK)
    world_map(d, (24, 800, 620, 1000))
    d.text((636, 810), "50 stories - all regions, all fields", font=font(F_SANSB, 16), fill=INK)
    d.text((636, 838), "Conflict, climate, politics, economy,", font=font(F_SANS, 13), fill=GREY)
    d.text((636, 858), "health, disaster, sport, technology", font=font(F_SANS, 13), fill=GREY)
    return im


def layout_f():
    """Dense index-first: 50 numbered lines + hero + map."""
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    masthead(d)
    hero(d, (24, 100, 1000, 280))
    f = font(F_SANS, 13)
    for i, st in enumerate(STORIES):
        c, r = divmod(i, 25)
        x0, y0 = 24 + c * 488, 292 + r * 24
        badge(d, x0 + 12, y0 + 10, st[0], r=10)
        icon(d, st[5], (x0 + 26, y0, x0 + 50, y0 + 22), BLUE)
        d.text((x0 + 56, y0 + 3), st[3], font=f, fill=INK)
    world_map(d, (24, 292 + 25 * 24 + 8, 1000, 1000))
    return im


LAYOUTS = {"A": layout_a, "B": layout_b, "C": layout_c, "D": layout_d, "E": layout_e, "F": layout_f}

if __name__ == "__main__":
    key = sys.argv[1] if len(sys.argv) > 1 else "A"
    out = sys.argv[2] if len(sys.argv) > 2 else "entry.png"
    img = LAYOUTS[key]()
    img.save(out, "PNG", optimize=True)
    print(f"layout {key} -> {out} {os.path.getsize(out)} bytes, stories={len(STORIES)} illustrated={len(ILLUSTRATED)}")
