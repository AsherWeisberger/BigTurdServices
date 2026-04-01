#!/usr/bin/env python3
"""
OG Image Generator for BIG TURD Waste Removal
Creates a 1200x630 Facebook/Twitter share card.
Free, no API keys — uses only PIL/Pillow.
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

# ── Colors ──────────────────────────────────────────────────
LIME    = (132, 204, 22)    # #84cc16
BROWN   = ( 68,  64,  60)   # #44403c
DARK    = ( 41,  37,  36)   # #292524
WHITE   = (255, 255, 255)
CREAM   = (254, 252, 232)   # #fefce8

W, H = 1200, 630

# ── Font setup ──────────────────────────────────────────────
FONT_SEARCH = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Helvetica.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    None,
]

def make_font(size, bold=False):
    for path in FONT_SEARCH:
        if path and os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default(size=size)

def txt_sz(draw, text, font):
    bb = draw.textbbox((0, 0), text, font=font)
    return bb[2] - bb[0], bb[3] - bb[1]


# ── Draw poop emoji ──────────────────────────────────────────
def draw_poop(draw, cx, cy, radius=72):
    x, y = cx, cy

    # drop shadow
    draw.ellipse([x - radius + 4, y - radius + 10, x + radius + 4, y + radius + 14],
                 fill=(20, 20, 20))

    # main body
    draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=BROWN)

    # highlight top-left
    draw.ellipse([x - radius + 12, y - radius + 8, x - 8, y - radius + 30],
                 fill=(105, 95, 87))

    # swirl nub on top
    draw.ellipse([x - 22, y - radius - 22, x + 22, y - radius + 20],
                 fill=BROWN)
    draw.arc([x - 18, y - radius - 18, x + 18, y - radius + 18],
             200, 340, fill=(105, 95, 87), width=4)

    # eyes (white + dark pupils + shine)
    eye_r = 9
    draw.ellipse([x - 30, y - 18, x - 30 + eye_r*2, y - 18 + eye_r*2], fill=WHITE)
    draw.ellipse([x + 12, y - 18, x + 12 + eye_r*2, y - 18 + eye_r*2], fill=WHITE)
    draw.ellipse([x - 26, y - 16, x - 26 + 9, y - 16 + 9], fill=DARK)
    draw.ellipse([x + 16, y - 16, x + 16 + 9, y - 16 + 9], fill=DARK)
    draw.ellipse([x - 25, y - 18, x - 25 + 3, y - 18 + 3], fill=WHITE)
    draw.ellipse([x + 17, y - 18, x + 17 + 3, y - 18 + 3], fill=WHITE)

    # smile
    draw.arc([x - 22, y + 8, x + 22, y + 38], 15, 165, fill=DARK, width=4)

    return draw


# ── Draw paw print ───────────────────────────────────────────
def draw_paw(draw, cx, cy, size=40, color=LIME):
    x, y = cx, cy
    s = size

    # main pad
    draw.ellipse([x - s, y - s//2, x + s, y + s//2 + 10], fill=color)
    # toe pads
    offsets = [(-s*1.1, -s*0.9), (-s*0.35, -s*1.2), (s*0.35, -s*1.2), (s*1.1, -s*0.9)]
    for ox, oy in offsets:
        draw.ellipse([x + ox - s//2.5, y + oy - s//2.5,
                      x + ox + s//2.5, y + oy + s//2.5], fill=color)
    return draw


# ── Main ─────────────────────────────────────────────────────
def make_og_image(output_path="og-image.png"):
    img = Image.new("RGB", (W, H), DARK)
    draw = ImageDraw.Draw(img)

    # ── Gradient background (top-down) ──────────────────────────
    for i in range(H):
        t = i / H
        r = int(DARK[0] + (BROWN[0] - DARK[0]) * t * 0.25)
        g = int(DARK[1] + (BROWN[1] - DARK[1]) * t * 0.25)
        b = int(DARK[2] + (BROWN[2] - DARK[2]) * t * 0.25)
        draw.line([(0, i), (W, i)], fill=(r, g, b))

    # ── Lime glow behind center ─────────────────────────────────
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse([W//2 - 420, H//2 - 260, W//2 + 420, H//2 + 280],
                      fill=(132, 204, 22, 25))
    glow_blurred = glow.filter(ImageFilter.GaussianBlur(90))
    img.paste(glow_blurred, (0, 0), glow_blurred)

    # ── Paw prints in corners ───────────────────────────────────
    draw_paw(draw, 90,  80,  size=35, color=(132, 204, 22, 100))
    draw_paw(draw, W - 90, 80,  size=35, color=(132, 204, 22, 100))
    draw_paw(draw, 90,  H - 80, size=35, color=(132, 204, 22, 80))
    draw_paw(draw, W - 90, H - 80, size=35, color=(132, 204, 22, 80))

    # ── Lime top stripe ─────────────────────────────────────────
    for i in range(6):
        draw.line([(0, i), (W, i)], fill=LIME)

    # ── Poop emoji ─────────────────────────────────────────────
    draw_poop(draw, W // 2, H // 2 - 55, radius=68)

    # ── Brand text: BIG TURD ───────────────────────────────────
    fnt_brand = make_font(108)
    fnt_sub   = make_font(34)
    fnt_phone = make_font(30)
    fnt_kw    = make_font(20)
    fnt_url   = make_font(18)

    brand = "BIG TURD"
    bw, bh = txt_sz(draw, brand, fnt_brand)

    # shadow
    draw.text(((W - bw) // 2 + 4, 178 + 4), brand, font=fnt_brand, fill=(20, 20, 20))
    # main
    draw.text(((W - bw) // 2, 178), brand, font=fnt_brand, fill=WHITE)

    # lime underline bar
    bar_w = bw + 50
    bar_x = (W - bar_w) // 2
    draw.rectangle([bar_x, 178 + bh + 8, bar_x + bar_w, 178 + bh + 14], fill=LIME)

    # ── Tagline ───────────────────────────────────────────────
    tagline = "Waste Removal & Pet Cleanup Services"
    tw, th = txt_sz(draw, tagline, fnt_sub)
    draw.text(((W - tw) // 2, 178 + bh + 24), tagline, font=fnt_sub, fill=LIME)

    # ── Keywords strip ─────────────────────────────────────────
    keywords = "Dog Poop Cleanup  \u2022  Pet Waste Removal  \u2022  Terre Haute, IN  \u2022  Commercial & Residential"
    kw_w, kw_h = txt_sz(draw, keywords, fnt_kw)
    draw.text(((W - kw_w) // 2, 178 + bh + 65), keywords, font=fnt_kw, fill=(160, 150, 140))

    # ── Phone pill ─────────────────────────────────────────────
    phone = "\U0001f4de  812-508-6399"
    pw, ph = txt_sz(draw, phone, fnt_phone)

    # lime rounded pill bg
    pill_pad = 24
    px = (W - pw) // 2 - pill_pad
    py = H - 95
    draw.rounded_rectangle(
        [px, py, px + pw + pill_pad * 2, py + ph + 14],
        radius=36, fill=LIME)

    draw.text(((W - pw) // 2, py + 6), phone, font=fnt_phone, fill=DARK)

    # ── Website URL ────────────────────────────────────────────
    url = "bigturd.site"
    uw, uh = txt_sz(draw, url, fnt_url)
    draw.text(((W - uw) // 2, H - 32), url, font=fnt_url, fill=(110, 105, 95))

    # ── Save ──────────────────────────────────────────────────
    img.save(output_path, "PNG", optimize=True)
    size_kb = os.path.getsize(output_path) // 1024
    print(f"\u2705 OG image saved: {output_path}")
    print(f"   Size: {W}x{H}px  |  File: ~{size_kb}KB")


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "og-image.png")
    make_og_image(out)
