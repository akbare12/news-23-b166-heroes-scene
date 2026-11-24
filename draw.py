#!/usr/bin/env python3
"""Draw THE WORLD TODAY — Monday 23 November 2026 (31 stories).
Front page, 1024x1024. Heroes-scene variant: 3 BIG hero scenes."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
NAVY = (14, 30, 58)
NAVY2 = (24, 48, 88)
RED = (176, 30, 36)
GOLD = (201, 162, 39)
GOLD_L = (232, 196, 90)
INK = (20, 20, 20)
GREY = (90, 90, 90)
LINE = (200, 192, 175)
TEAL = (18, 90, 96)
BLUE = (38, 90, 160)
GREEN = (46, 120, 70)

FD = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FDB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FDS = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FDSB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(size, bold=False, serif=False):
    if serif:
        return ImageFont.truetype(FDSB if bold else FDS, size)
    return ImageFont.truetype(FDB if bold else FD, size)


def tw(d, text, f):
    return d.textlength(text, font=f)


def wrap(d, text, f, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(d, t, f) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit(d, text, f, maxw, min_size=9):
    """Shrink font until text fits on one line; return (font, text)."""
    size = f.size
    while size > min_size and tw(d, text, f) > maxw:
        size -= 1
        f = ImageFont.truetype(f.path, size)
    return f, text


def chip(d, x, y, label, color):
    f = font(9, bold=True)
    w = int(tw(d, label, f)) + 10
    d.rounded_rectangle([x, y, x + w, y + 14], radius=3, fill=color)
    d.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return w


def bar(d, x, y, w, h, text, fill, fg=(255, 255, 255), f=None, align="left"):
    d.rectangle([x, y, x + w, y + h], fill=fill)
    f = f or font(11, bold=True)
    if align == "left":
        d.text((x + 8, y + (h - f.size) // 2 - 1), text, font=f, fill=fg)
    else:
        d.text((x + (w - tw(d, text, f)) // 2, y + (h - f.size) // 2 - 1),
               text, font=f, fill=fg)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------- MASTHEAD ----------
d.rectangle([0, 0, W, 46], fill=NAVY)
f = font(30, bold=True, serif=True)
d.text((16, 6), "THE WORLD TODAY", font=f, fill=(255, 255, 255))
f2 = font(13, bold=True)
d.text((W - 16 - tw(d, "MONDAY 23 NOVEMBER 2026", f2), 15),
       "MONDAY 23 NOVEMBER 2026", font=f2, fill=GOLD_L)
d.rectangle([0, 46, W, 48], fill=GOLD)

# ---------- KICKER ----------
d.rectangle([0, 48, W, 68], fill=RED)
f = font(12, bold=True)
d.text((16, 54), "23 NOVEMBER 2026 — THE WORLD IN ONE PAGE",
       font=f, fill=(255, 255, 255))
r = "31 STORIES  ·  6 REGIONS"
d.text((W - 16 - tw(d, r, f), 54), r, font=f, fill=(255, 255, 255))

# ---------- NUMBER STRIP ----------
NUMS = [
    ("-3.3%", "KOSPI FALLS"), ("5.3", "US-CHINA GAP"),
    ("11,762", "EBOLA CASES, DRC"), ("10T WON", "SEOUL RESCUE FUND"),
    ("2%", "BILLIONAIRE TAX"), ("$450M", "SKUBAL TO METS"),
    ("165", "MISSILES / WEEK"), ("12,000", "CLEARED MANCHESTER"),
    ("264 KG", "LEBANON SEIZURE"), ("$107.3B", "ANTHROPIC IPO"),
]
strip_y, strip_h = 68, 56
d.rectangle([0, strip_y, W, strip_y + strip_h], fill=(255, 255, 255))
d.line([0, strip_y + strip_h, W, strip_y + strip_h], fill=LINE, width=1)
cw = W // 5
for i, (val, lab) in enumerate(NUMS):
    col, row = i % 5, i // 5
    cx = col * cw
    vy = strip_y + 4 + row * 26
    fv = font(15, bold=True)
    d.text((cx + 12, vy), val, font=fv, fill=NAVY)
    fl = font(8, bold=True)
    d.text((cx + 12, vy + 15), lab, font=fl, fill=GREY)
    if col:
        d.line([cx, strip_y + 6, cx, strip_y + strip_h - 6], fill=LINE, width=1)

# ---------- REGION BAR ----------
REGIONS = [("ASIA-PACIFIC", 7), ("AMERICAS", 8), ("MIDDLE EAST", 6),
           ("EUROPE", 5), ("AFRICA", 3), ("WORLD", 2)]
ry, rh = 124, 22
d.rectangle([0, ry, W, ry + rh], fill=NAVY2)
x = 16
f = font(11, bold=True)
for name, n in REGIONS:
    t = "%s %d" % (name, n)
    d.text((x, ry + 4), t, font=f, fill=(255, 255, 255))
    x += int(tw(d, t, f)) + 26
    d.text((x - 18, ry + 4), "|", font=f, fill=GOLD_L)
d.text((W - 16 - tw(d, "31 STORIES TOTAL", f), ry + 4),
       "31 STORIES TOTAL", font=f, fill=GOLD_L)

# ---------- HERO HEADER ----------
hy = 146
bar(d, 0, hy, W, 20, "THE BIG THREE — MONDAY'S DEFINING STORIES",
    (0, 0, 0), f=font(11, bold=True))

# ---------- HEROES ----------
# columns: x=16, 349, 682 ; width 326 ; gap 7
HEROES = [
    dict(
        scene="kospi",
        head="AI ROUT HITS ASIA",
        body=["Kospi sheds 161 points as AI stocks plunge;",
              "Samsung -3.1%, SK Hynix -2.5%."],
        src="REUTERS",
    ),
    dict(
        scene="guterres",
        head="GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
        body=["150 delegates in Bridgetown back a risk",
              "framework — a blueprint, not a treaty."],
        src="AP",
    ),
    dict(
        scene="power",
        head="US LEAD OVER CHINA AT RECORD LOW",
        body=["Asia Power Index 2026: US 78.9, China 73.6;",
              "gap of 5.3 is the narrowest since 2018."],
        src="BLOOMBERG",
    ),
]
SCENE_Y, SCENE_H = 166, 148
HEAD_Y = SCENE_Y + SCENE_H + 6

for i, hero in enumerate(HEROES):
    x0 = 16 + i * 333
    x1 = x0 + 326
    # scene frame
    d.rectangle([x0, SCENE_Y, x1, SCENE_Y + SCENE_H], outline=NAVY, width=2)
    if hero["scene"] == "kospi":
        d.rectangle([x0, SCENE_Y, x1, SCENE_Y + SCENE_H], fill=(10, 22, 44))
        # lit-window skyline
        import random
        rnd = random.Random(11)
        bx = x0 + 8
        while bx < x1 - 30:
            bw = rnd.randint(26, 44)
            bh = rnd.randint(34, 74)
            by = SCENE_Y + SCENE_H - 26 - bh
            d.rectangle([bx, by, bx + bw, SCENE_Y + SCENE_H - 26],
                        fill=(30, 52, 92), outline=(70, 100, 150))
            for wy in range(by + 6, SCENE_Y + SCENE_H - 30, 10):
                for wx in range(bx + 4, bx + bw - 4, 9):
                    if rnd.random() < 0.55:
                        d.rectangle([wx, wy, wx + 4, wy + 5],
                                    fill=(255, 214, 90))
            bx += bw + 5
        # falling chart line
        pts = []
        for k in range(9):
            px = x0 + 20 + k * 36
            py = SCENE_Y + 58 + k * 7 + (k % 2) * 4
            pts.append((px, py))
        d.line(pts, fill=(255, 122, 26), width=4)
        d.ellipse([pts[-1][0] - 4, pts[-1][1] - 4,
                   pts[-1][0] + 4, pts[-1][1] + 4], fill=(255, 122, 26))
        f = font(30, bold=True)
        d.text((x0 + 10, SCENE_Y + 8), "-3.3%", font=f, fill=GOLD_L)
        # caption band
        d.rectangle([x0, SCENE_Y + SCENE_H - 26, x1, SCENE_Y + SCENE_H],
                    fill=NAVY)
        fc = font(10, bold=True)
        cap = "KOSPI 4,708.54 · -161 PTS · INTRADAY -5.8%"
        fc, _ = fit(d, cap, fc, 326 - 12)
        d.text((x0 + 6, SCENE_Y + SCENE_H - 20), cap, font=fc,
               fill=(255, 255, 255))
    elif hero["scene"] == "guterres":
        d.rectangle([x0, SCENE_Y, x1, SCENE_Y + SCENE_H], fill=TEAL)
        # globe, right side, masked circle
        cx, cy, r = x1 - 62, SCENE_Y + 74, 52
        globe = Image.new("RGBA", (2 * r + 4, 2 * r + 4), (0, 0, 0, 0))
        gd = ImageDraw.Draw(globe)
        gd.ellipse([2, 2, 2 * r + 2, 2 * r + 2], fill=(38, 90, 160))
        for k in range(-2, 3):
            gd.arc([2 + abs(k) * 14, 2, 2 * r + 2 - abs(k) * 14, 2 * r + 2],
                   90, 270, fill=(120, 180, 220), width=2)
            gd.arc([2 + abs(k) * 14, 2, 2 * r + 2 - abs(k) * 14, 2 * r + 2],
                   270, 90, fill=(120, 180, 220), width=2)
        for k in range(1, 4):
            gd.line([2, 2 + k * r // 2, 2 * r + 2, 2 + k * r // 2],
                    fill=(120, 180, 220), width=2)
        gd.ellipse([2 + r // 2, 2 + r // 3, 2 + r, 2 + r], fill=(46, 120, 70))
        img.paste(globe, (cx - r - 2, cy - r - 2), globe)
        d = ImageDraw.Draw(img)
        f = font(15, bold=True)
        d.text((x0 + 10, SCENE_Y + 10), "150 DELEGATES", font=f, fill=GOLD_L)
        d.text((x0 + 10, SCENE_Y + 32), "BACK A RISK", font=f, fill=GOLD_L)
        d.text((x0 + 10, SCENE_Y + 54), "FRAMEWORK", font=f, fill=GOLD_L)
        f2 = font(10, bold=True)
        d.text((x0 + 10, SCENE_Y + 82), "BRIDGETOWN SUMMIT", font=f2,
               fill=(255, 255, 255))
        d.text((x0 + 10, SCENE_Y + 100), "BARBADOS", font=f2,
               fill=(255, 255, 255))
        # small flags row
        cols = [(176, 30, 36), (255, 255, 255), (38, 90, 160),
                (201, 162, 39)]
        for k, c in enumerate(cols):
            fx = x0 + 10 + k * 26
            d.rectangle([fx, SCENE_Y + 122, fx + 20, SCENE_Y + 134],
                        fill=c, outline=(255, 255, 255))
    else:  # power bars
        d.rectangle([x0, SCENE_Y, x1, SCENE_Y + SCENE_H], fill=(255, 255, 255))
        d.rectangle([x0, SCENE_Y, x1, SCENE_Y + SCENE_H], outline=NAVY, width=2)
        f = font(11, bold=True)
        rows = [("US", 78.9, GOLD), ("CHINA", 73.6, BLUE), ("INDIA", 40.5, GREEN)]
        by = SCENE_Y + 12
        for name, val, col in rows:
            d.text((x0 + 10, by), name, font=f, fill=INK)
            bw = int(val * 2.6)
            d.rectangle([x0 + 74, by + 2, x0 + 74 + bw, by + 16], fill=col)
            d.text((x0 + 80 + bw, by), "%.1f" % val, font=f, fill=INK)
            by += 30
        f2 = font(10, bold=True)
        d.text((x0 + 10, by + 2), "GAP 5.3 — NARROWEST SINCE 2018",
               font=f2, fill=RED)
        d.text((x0 + 10, by + 20), "US DIPLOMATIC INFLUENCE -6 TO 76.7",
               font=f2, fill=GREY)
    # headline (below scene, never touching the black bar above)
    fh = font(15, bold=True)
    lines = wrap(d, hero["head"], fh, 326)
    yy = HEAD_Y
    for ln in lines[:2]:
        d.text((x0, yy), ln, font=fh, fill=INK)
        yy += 19
    fb = font(11)
    for ln in hero["body"]:
        d.text((x0, yy), ln, font=fb, fill=(40, 40, 40))
        yy += 15
    # source + chip row
    sy = HEAD_Y + 66
    fs = font(10, bold=True)
    d.text((x0, sy), hero["src"], font=fs, fill=GREY)
    chip(d, x0 + int(tw(d, hero["src"], fs)) + 8, sy - 1, "REPORTED", GREEN)

# ---------- MORE OF THE DAY ----------
MY = HEAD_Y + 88
bar(d, 0, MY, W, 20, "MORE OF THE DAY", (0, 0, 0), f=font(11, bold=True))

CARDS = [
    ("BESSENT DEMANDS NVIDIA ANSWERS", "Treasury chief presses chipmaker.", "REUTERS", "REPORTED"),
    ("FBI PROBES NCIC POLICE-DATABASE HACK", "Federal system breached.", "AP", "REPORTED"),
    ("TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "AP", "REPORTED"),
    ("NASDAQ FUTURES JUMP 3%", "Holiday week rally.", "BLOOMBERG", "REPORTED"),
    ("SKUBAL $450M TO METS", "Two-time Cy Young, 9 years.", "ESPN", "REPORTED"),
    ("TOM JACKSON DIES AT 75", "NFL star and broadcaster.", "AP", "REPORTED"),
    ("STATES SUE SPACEX", "Over AI safety claims.", "REUTERS", "REPORTED"),
    ("ANTHROPIC IPO $107.3B", "Priced $83/share, debut $97.17.", "BLOOMBERG", "REPORTED"),
    ("POLAND: 3 KH-101 MISSILES CROSSED", "Moscow denies the claim.", "REUTERS", "CLAIM"),
    ("INTEL WARNS OF RUSSIAN NUCLEAR SAT", "US intel assessment.", "AP", "CLAIM"),
]
CY, CH, CG = MY + 28, 92, 8
CWID = (W - 32 - 4 * CG) // 5
for i, (head, body, src, tag) in enumerate(CARDS):
    col, row = i % 5, i // 5
    x0 = 16 + col * (CWID + CG)
    y0 = CY + row * (CH + CG)
    d.rectangle([x0, y0, x0 + CWID, y0 + CH], fill=(255, 255, 255),
                outline=LINE, width=1)
    fh = font(11, bold=True)
    lines = wrap(d, head, fh, CWID - 12)
    yy = y0 + 6
    for ln in lines[:2]:
        d.text((x0 + 6, yy), ln, font=fh, fill=INK)
        yy += 14
    fb = font(10)
    blines = wrap(d, body, fb, CWID - 12)
    for ln in blines[:1]:
        d.text((x0 + 6, yy), ln, font=fb, fill=(60, 60, 60))
        yy += 13
    sy = y0 + CH - 20
    fs = font(9, bold=True)
    d.text((x0 + 6, sy + 2), src, font=fs, fill=GREY)
    chip(d, x0 + 6 + int(tw(d, src, fs)) + 6, sy,
         tag, GREEN if tag == "REPORTED" else RED)

# ---------- MAP + ALSO ----------
MAP_Y = CY + 2 * (CH + CG) + 6
bar(d, 0, MAP_Y, W, 20, "THE WORLD AT A GLANCE", (0, 0, 0),
    f=font(11, bold=True))
BOX_Y = MAP_Y + 28
BOX_H = 168
# map panel (left)
MX, MW = 16, 500
d.rectangle([MX, BOX_Y, MX + MW, BOX_Y + BOX_H], fill=(232, 238, 244),
            outline=NAVY, width=1)
# stylised continents (light blobs)
d.ellipse([MX + 18, BOX_Y + 22, MX + 150, BOX_Y + 78], fill=(190, 200, 210))   # N America
d.ellipse([MX + 118, BOX_Y + 82, MX + 178, BOX_Y + 128], fill=(190, 200, 210))  # S America
d.ellipse([MX + 210, BOX_Y + 30, MX + 470, BOX_Y + 92], fill=(190, 200, 210))   # Eurasia
d.ellipse([MX + 296, BOX_Y + 94, MX + 380, BOX_Y + 156], fill=(190, 200, 210))  # Africa
d.ellipse([MX + 400, BOX_Y + 96, MX + 480, BOX_Y + 138], fill=(190, 200, 210))  # Oceania
# pins: (x, y, label) — spread, inside blobs, >=20px apart
PINS = [
    (MX + 452, BOX_Y + 52, "1"),   # Seoul
    (MX + 142, BOX_Y + 96, "2"),   # Bridgetown
    (MX + 62, BOX_Y + 52, "3"),    # Washington
    (MX + 238, BOX_Y + 56, "4"),   # Paris
    (MX + 224, BOX_Y + 40, "5"),   # Manchester
    (MX + 292, BOX_Y + 62, "6"),   # Kyiv
    (MX + 306, BOX_Y + 84, "7"),   # Antalya
    (MX + 322, BOX_Y + 100, "8"),   # Gaza
    (MX + 344, BOX_Y + 108, "9"),   # Beirut
    (MX + 360, BOX_Y + 128, "10"),  # Bahrain
    (MX + 308, BOX_Y + 122, "11"),  # Benghazi
    (MX + 336, BOX_Y + 140, "12"),  # Khartoum
    (MX + 316, BOX_Y + 148, "13"),  # Kinshasa
]
fp = font(9, bold=True)
for px, py, lab in PINS:
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
              outline=(255, 255, 255), width=1)
    d.text((px - tw(d, lab, fp) / 2, py - 6), lab, font=fp,
           fill=(255, 255, 255))
# map legend
fl = font(9)
d.text((MX + 8, BOX_Y + BOX_H - 48),
       "1 Seoul  2 Bridgetown  3 Washington  4 Paris  5 Manchester",
       font=fl, fill=GREY)
d.text((MX + 8, BOX_Y + BOX_H - 34),
       "6 Kyiv  7 Antalya  8 Gaza  9 Beirut  10 Bahrain  11 Benghazi",
       font=fl, fill=GREY)
d.text((MX + 8, BOX_Y + BOX_H - 20),
       "12 Khartoum  13 Kinshasa", font=fl, fill=GREY)

# ALSO panel (right)
AX, AW = 532, 476
d.text((AX, BOX_Y), "ALSO ON MONDAY", font=font(12, bold=True), fill=NAVY)
ALSO = [
    "Paris: 100+ back 2% billionaire tax",
    "Manchester: 12,000 cleared",
    "Zelenskyy: 165 Russian missiles in a week",
    "COP31: the day after Antalya pact rejected",
    "Israel unity talks resume",
    "Gaza: two killed in Israeli strike",
    "West Bank settler attacks",
    "Iran war: no deal in sight",
    "Lebanon seizes 264 kg explosives",
    "Bahrain: Iranian strike hits plant, 2 hurt",
    "Benghazi: UN demands port probe [CLAIM]",
    "Sudan: drones downed in Khartoum [CLAIM]",
    "DRC: fighting traps Ebola teams",
    "Bangladesh: Hasina jailed if she returns",
    "Seoul minister quits over AI exam chaos",
    "SK Telecom -7.3%",
    "China eases margin rules to 80%",
    "Seoul readies 10T-won stabilisation fund",
]
fa = font(10)
ay = BOX_Y + 20
for i, item in enumerate(ALSO):
    col = 0 if i < 9 else 1
    row = i % 9
    ix = AX + col * 244
    iy = ay + row * 16
    tag = " [CLAIM]" in item
    txt = item.replace(" [CLAIM]", "")
    d.text((ix, iy), "• " + txt, font=fa,
           fill=RED if tag else INK)
    if tag:
        d.text((ix + tw(d, "• " + txt, fa) + 2, iy), "[CLAIM]",
               font=font(9, bold=True), fill=RED)

# ---------- DATE CHECK ----------
DY = BOX_Y + BOX_H + 10
DH = 78
d.rectangle([16, DY, W - 16, DY + DH], outline=RED, width=2, fill=(255, 238, 238))
f = font(12, bold=True)
d.text((26, DY + 6), "DATE CHECK — LEFT OUT (NOT 23 NOVEMBER)",
       font=f, fill=RED)
f2 = font(10)
left = ("Democrats reach 258 (22 Nov)  ·  Sparta II fire (22 Nov)  ·  "
        "El Chapo Isidro captured (22 Nov)")
d.text((26, DY + 26), left, font=f2, fill=INK)
left2 = ("EU–Indonesia pact (21 Nov)  ·  Nigeria boat (21 Nov)  ·  "
         "ICJ Myanmar ruling (19 Nov)")
d.text((26, DY + 42), left2, font=f2, fill=INK)
f3 = font(10, bold=True)
d.text((26, DY + 60),
       "NOT YET: Dymer search continues (14 missing) · 4 House races "
       "uncalled · COP32 venue not set · WHO evacuating trapped Ebola staff",
       font=f3, fill=INK)

# ---------- FOOTER ----------
FY = DY + DH + 8
d.line([16, FY, W - 16, FY], fill=LINE, width=1)
ff = font(9)
d.text((16, FY + 6),
       "Sources: Reuters · AP · Bloomberg · ESPN · wires. "
       "REPORTED = confirmed by wires · CLAIM = one side's claim.",
       font=ff, fill=GREY)
d.text((16, FY + 20),
       "THE WORLD TODAY · Monday 23 November 2026 · 31 stories · 6 regions",
       font=font(9, bold=True), fill=NAVY)

img.save("entry.png")
print("saved entry.png", img.size)
