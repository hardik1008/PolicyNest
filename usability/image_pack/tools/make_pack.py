"""Generate the synthetic PolicyNest usability-test image pack (one invented person, "Rahul Kulkarni").

Everything here is invented: names, PAN, Aadhaar last four, roll number, account number, IFSC.
No real person's data is used and no full Aadhaar number is ever drawn (only XXXX XXXX + last four).
Every image carries the words SPECIMEN, SYNTHETIC (a red banner line, as in the PS-01 specimens, plus a
faint repeated diagonal watermark). No face is drawn: the photo boxes hold a plain grey avatar icon.

Needs Pillow only. Run:  python make_pack.py <output folder>
(Pillow was installed into a scratch folder; set PYTHONPATH to it if Pillow is not installed globally.)
Layout and wording follow Specimens 1-3 in PS-01_specimen_documents.docx.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

K = 16                       # pixels per millimetre (about 406 dpi when printed at actual size)
FD = "C:/Windows/Fonts/"
OUT = sys.argv[1] if len(sys.argv) > 1 else "."

# ---- the invented person -------------------------------------------------------------------------
P = dict(
    name="RAHUL KULKARNI", name_tc="Rahul Kulkarni",
    father="SURESH KULKARNI", father_tc="Suresh Kulkarni",
    dob="17/09/1996",
    pan="QWTPK7305L",
    aadhaar4="6407",
    house="214, Lakshmi Nagar", city="Pune", state="Maharashtra", pin="411057",
    board="MAHARASHTRA STATE BOARD OF SECONDARY EDUCATION",
    exam_year=2012, roll="3149026",
    marks=[("Hindi", 72), ("English", 84), ("Mathematics", 76), ("Science", 68), ("Social Science", 81)],
    bank="POLICYNEST DEMO BANK", ifsc="NEST0371264", acct4="3829",  # fictional bank and IFSC (G-36)
)


def mm(v):
    return int(round(v * K))


def font(name, size_mm):
    return ImageFont.truetype(FD + name, mm(size_mm))


ARIAL, ARIALB = "arial.ttf", "arialbd.ttf"
TIMES, TIMESB, TIMESI = "times.ttf", "timesbd.ttf", "timesi.ttf"
RED = (176, 28, 28)
INK = (20, 22, 30)
GREY = (70, 74, 84)


def new_card(w_mm, h_mm, bg):
    return Image.new("RGBA", (mm(w_mm), mm(h_mm)), bg + (255,))


def watermark(img, size_mm=6.0, alpha=17, angle=24):
    W, H = img.size
    layer = Image.new("RGBA", (W * 2, H * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = font(ARIALB, size_mm)
    text = "SPECIMEN, SYNTHETIC"
    tw = d.textlength(text, font=f)
    sx, sy = int(tw + mm(9)), int(mm(size_mm * 3.4))
    for r, y in enumerate(range(0, H * 2, sy)):
        off = (r % 2) * sx // 2
        for x in range(-sx, W * 2, sx):
            d.text((x + off, y), text, font=f, fill=(40, 50, 70, alpha))
    layer = layer.rotate(angle, resample=Image.BICUBIC)
    left, top = (W * 2 - W) // 2, (H * 2 - H) // 2
    img.alpha_composite(layer.crop((left, top, left + W, top + H)))


def text(d, x, y, s, f, fill=INK, anchor="ls"):
    d.text((mm(x), mm(y)), s, font=f, fill=fill, anchor=anchor)


def avatar(d, x0, y0, x1, y1):
    """A plain grey avatar icon in a photo box. No face is drawn."""
    d.rectangle([mm(x0), mm(y0), mm(x1), mm(y1)], fill=(214, 219, 226), outline=(150, 156, 168), width=mm(0.25))
    cx, w, h = (x0 + x1) / 2, x1 - x0, y1 - y0
    d.ellipse([mm(cx - w * .2), mm(y0 + h * .18), mm(cx + w * .2), mm(y0 + h * .18 + w * .4)], fill=(170, 177, 190))
    body = Image.new("RGBA", (mm(w), mm(h)), (0, 0, 0, 0))
    bd = ImageDraw.Draw(body)
    bd.ellipse([mm(w * .12), mm(h * .62), mm(w * .88), mm(h * 1.5)], fill=(170, 177, 190, 255))
    return body, (mm(x0), mm(y0))


def finish(img, path):
    watermark(img)
    img.convert("RGB").save(path, dpi=(K * 25.4, K * 25.4), optimize=True)


def paste_avatar(img, x0, y0, x1, y1):
    d = ImageDraw.Draw(img)
    body, pos = avatar(d, x0, y0, x1, y1)
    img.alpha_composite(body, pos)
    d.rectangle([mm(x0), mm(y0), mm(x1), mm(y1)], outline=(150, 156, 168), width=mm(0.25))


def rounded_border(img, inset, radius, color, width):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([mm(inset), mm(inset), img.size[0] - mm(inset), img.size[1] - mm(inset)],
                        radius=mm(radius), outline=color, width=mm(width))


# ---- 1. PAN card (85.6 x 54 mm) ------------------------------------------------------------------
def pan_card(path):
    img = new_card(85.6, 54, (231, 239, 248))
    d = ImageDraw.Draw(img)
    rounded_border(img, 0.8, 3, (40, 70, 120), 0.35)
    text(d, 5, 5.6, "SPECIMEN, SYNTHETIC", font(ARIALB, 2.7), RED)
    text(d, 5, 11.4, "INCOME TAX DEPARTMENT", font(ARIALB, 3.7), (25, 45, 95))
    text(d, 5, 16.0, "Permanent Account Number Card", font(ARIAL, 2.9), (25, 45, 95))
    text(d, 5, 23.6, P["pan"], font(ARIALB, 5.6), INK)
    text(d, 5, 28.4, "Name", font(ARIAL, 2.4), GREY)
    text(d, 5, 33.2, P["name"], font(ARIALB, 3.9), INK)
    text(d, 5, 37.6, "Father's Name", font(ARIAL, 2.4), GREY)
    text(d, 5, 42.0, P["father"], font(ARIAL, 3.5), INK)
    text(d, 5, 46.2, "Date of Birth", font(ARIAL, 2.4), GREY)
    text(d, 5, 50.4, P["dob"], font(ARIALB, 3.5), INK)
    paste_avatar(img, 60, 19, 80, 43)
    finish(img, path)


# ---- 2/3. Aadhaar front and back (85.6 x 54 mm), masked to the last four digits --------------------
def aadhaar_frame():
    img = new_card(85.6, 54, (255, 253, 247))
    d = ImageDraw.Draw(img)
    # Neutral frame only: no saffron/green bands, so the card does not imitate the real Aadhaar design (G-36)
    d.rectangle([0, 0, img.size[0] - 1, img.size[1] - 1], outline=(190, 186, 176), width=mm(0.25))
    return img, d


def aadhaar_front(path):
    img, d = aadhaar_frame()
    text(d, 5, 6.6, "SPECIMEN, SYNTHETIC", font(ARIALB, 2.7), RED)
    text(d, 5, 12.0, "Government of India", font(ARIALB, 3.4), INK)
    paste_avatar(img, 5, 16, 27, 43)
    text(d, 31, 23.0, P["name_tc"], font(ARIALB, 4.5), INK)
    text(d, 31, 29.8, "DOB: " + P["dob"], font(ARIAL, 3.9), INK)
    text(d, 31, 36.0, "MALE", font(ARIAL, 3.9), INK)
    text(d, 42.8, 48.0, "XXXX XXXX " + P["aadhaar4"], font(ARIALB, 5.0), INK, anchor="ms")
    text(d, 42.8, 52.0, "Synthetic test card, not an Aadhaar", font(ARIAL, 2.3), GREY, anchor="ms")
    finish(img, path)


def aadhaar_back(path):
    img, d = aadhaar_frame()
    text(d, 5, 6.6, "SPECIMEN, SYNTHETIC", font(ARIALB, 2.7), RED)
    text(d, 5, 12.0, "Unique Identification Authority of India", font(ARIALB, 3.1), INK)
    text(d, 5, 19.5, "Address:", font(ARIALB, 3.6), INK)
    text(d, 5, 25.8, "S/O %s, %s," % (P["father_tc"], P["house"]), font(ARIAL, 3.6), INK)
    text(d, 5, 31.4, "%s, %s - %s" % (P["city"], P["state"], P["pin"]), font(ARIAL, 3.6), INK)
    text(d, 42.8, 48.0, "XXXX XXXX " + P["aadhaar4"], font(ARIALB, 5.0), INK, anchor="ms")
    text(d, 42.8, 52.0, "Synthetic test card, not an Aadhaar", font(ARIAL, 2.3), GREY, anchor="ms")
    finish(img, path)


# ---- 4. Class 10 marksheet (98 x 140 mm, portrait) -----------------------------------------------
def fit_font(d, s, name, start_mm, max_w_mm):
    size = start_mm
    while size > 1.5:
        f = font(name, size)
        if d.textlength(s, font=f) <= mm(max_w_mm):
            return f
        size -= 0.05
    return f


def marksheet_image():
    W, H = 98, 140
    img = new_card(W, H, (255, 251, 238))
    d = ImageDraw.Draw(img)
    d.rectangle([mm(2), mm(2), mm(W - 2), mm(H - 2)], outline=(110, 40, 40), width=mm(0.5))
    d.rectangle([mm(3.2), mm(3.2), mm(W - 3.2), mm(H - 3.2)], outline=(110, 40, 40), width=mm(0.2))
    cx = W / 2
    text(d, cx, 9.2, "SPECIMEN, SYNTHETIC", font(ARIALB, 2.8), RED, anchor="ms")
    d.text((mm(cx), mm(16.8)), P["board"], font=fit_font(d, P["board"], TIMESB, 3.0, 85), fill=INK, anchor="ms")
    text(d, cx, 24.6, "SECONDARY SCHOOL EXAMINATION %d" % P["exam_year"], font(TIMESB, 3.5), INK, anchor="ms")
    text(d, cx, 33.0, "MARKS STATEMENT", font(TIMESB, 4.4), INK, anchor="ms")
    d.line([mm(30), mm(34.6), mm(68), mm(34.6)], fill=INK, width=mm(0.3))
    fy = {}
    rows = [("Roll No. " + P["roll"], 45.0, TIMES), ("Name of Candidate: " + P["name"], 53.0, TIMESB),
            ("Father's Name: " + P["father"], 60.6, TIMES), ("Date of Birth: " + P["dob"], 68.2, TIMESB)]
    for s, y, fn in rows:
        text(d, 8, y, s, font(fn, 3.5), INK)
        fy[s.split(":")[0]] = y
    P["_dob_y"] = 68.2
    d.line([mm(8), mm(73.5), mm(W - 8), mm(73.5)], fill=INK, width=mm(0.25))
    text(d, 10, 78.6, "Subject", font(TIMESB, 3.1), INK)
    text(d, W - 10, 78.6, "Marks (out of 100)", font(TIMESB, 3.1), INK, anchor="rs")
    d.line([mm(8), mm(80.3), mm(W - 8), mm(80.3)], fill=INK, width=mm(0.15))
    y = 86.8
    for sub, m in P["marks"]:
        text(d, 10, y, sub, font(TIMES, 3.4), INK)
        text(d, W - 10, y, str(m), font(TIMES, 3.4), INK, anchor="rs")
        y += 7.0
    d.line([mm(8), mm(y - 4.6), mm(W - 8), mm(y - 4.6)], fill=INK, width=mm(0.15))
    tot = sum(m for _, m in P["marks"])
    text(d, 10, y + 0.4, "Total", font(TIMESB, 3.3), INK)
    text(d, W - 10, y + 0.4, "%d / 500" % tot, font(TIMESB, 3.3), INK, anchor="rs")
    text(d, 8, y + 9.6, "Result: PASS", font(TIMESB, 4.0), (20, 90, 40))
    d.line([mm(60), mm(H - 11), mm(W - 8), mm(H - 11)], fill=INK, width=mm(0.2))
    text(d, W - 8, H - 7.6, "Controller of Examinations", font(TIMESI, 2.5), GREY, anchor="rs")
    return img


def marksheet(path):
    img = marksheet_image()
    finish(img, path)


def marksheet_blurry(path):
    """Out-of-focus phone shot: mild blur everywhere, and the date-of-birth line smeared past reading."""
    img = marksheet_image()
    W, H = img.size
    box = (mm(6), mm(P["_dob_y"] - 5.0), mm(92), mm(P["_dob_y"] + 2.2))
    region = img.crop(box).filter(ImageFilter.GaussianBlur(mm(1.15)))
    mask = Image.new("L", region.size, 255)
    img.paste(region, box[:2])
    # smudge: drag the line sideways
    sm = img.crop(box)
    sm = ImageChops.offset(sm, mm(1.6), 0)
    img.paste(Image.blend(img.crop(box), sm, 0.5), box[:2])
    img = img.filter(ImageFilter.GaussianBlur(mm(0.1)))
    watermark(img)
    img = img.convert("RGB")
    small = img.resize((int(W * 0.8), int(H * 0.8)), Image.LANCZOS).resize((W, H), Image.BICUBIC)
    small.save(path, dpi=(K * 25.4, K * 25.4), optimize=True)


# ---- 5. Cancelled cheque (190 x 76 mm) -----------------------------------------------------------
def cheque(path, holder=None):
    holder = holder or P["name"]
    W, H = 190, 76
    img = new_card(W, H, (240, 247, 238))
    d = ImageDraw.Draw(img)
    d.rectangle([mm(1), mm(1), mm(W - 1), mm(H - 1)], outline=(90, 120, 90), width=mm(0.3))
    text(d, 6, 6.8, "SPECIMEN, SYNTHETIC", font(ARIALB, 3.0), RED)
    text(d, 6, 15.4, P["bank"], font(ARIALB, 6.0), (140, 50, 10))
    text(d, 6, 24.0, "IFSC: " + P["ifsc"], font(ARIALB, 4.0), INK)
    text(d, 6, 31.6, "A/c No. XXXXXXXX" + P["acct4"], font(ARIALB, 4.0), INK)
    text(d, 6, 39.4, holder, font(ARIALB, 4.6), INK)
    # date boxes
    text(d, 112, 7.2, "DATE", font(ARIAL, 2.6), GREY)
    for i in range(8):
        x = 124 + i * 7.0
        d.rectangle([mm(x), mm(3.4), mm(x + 5.6), mm(9.4)], outline=(90, 120, 90), width=mm(0.2))
    # cancelled stamp (kept clear of the text block)
    d.rectangle([mm(122), mm(17), mm(180), mm(33)], outline=RED, width=mm(0.9))
    text(d, 151, 28.2, "CANCELLED", font(ARIALB, 7.0), RED, anchor="ms")
    # pay lines (solid rules, so they do not read as dotted text)
    text(d, 6, 51.0, "PAY", font(ARIALB, 3.0), INK)
    d.line([mm(18), mm(51.4), mm(150), mm(51.4)], fill=(90, 120, 90), width=mm(0.2))
    text(d, 154, 51.0, "OR BEARER", font(ARIALB, 3.0), INK)
    text(d, 6, 59.0, "RUPEES", font(ARIALB, 3.0), INK)
    d.line([mm(26), mm(59.4), mm(150), mm(59.4)], fill=(90, 120, 90), width=mm(0.2))
    d.rectangle([mm(154), mm(54.4), mm(184), mm(63.4)], outline=(90, 120, 90), width=mm(0.3))
    d.line([mm(136), mm(66), mm(184), mm(66)], fill=INK, width=mm(0.2))
    text(d, 160, 69.2, "AUTHORISED SIGNATORY", font(ARIAL, 2.3), GREY, anchor="ms")
    text(d, 14, 73.4, "000371    999999999    000000    00", font("consolab.ttf", 3.6), INK)
    finish(img, path)


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.join(OUT, "variants"), exist_ok=True)
    pan_card(os.path.join(OUT, "01_PAN_card.png"))
    aadhaar_front(os.path.join(OUT, "02_Aadhaar_front_masked.png"))
    aadhaar_back(os.path.join(OUT, "03_Aadhaar_back_masked.png"))
    marksheet(os.path.join(OUT, "04_Class10_marksheet.png"))
    cheque(os.path.join(OUT, "05_Cancelled_cheque.png"))
    marksheet_blurry(os.path.join(OUT, "variants", "04b_Class10_marksheet_BLURRY_dob_unreadable.png"))
    cheque(os.path.join(OUT, "variants", "05b_Cancelled_cheque_PARENT_name.png"), holder=P["father"])
    print("done:", OUT)


if __name__ == "__main__":
    main()
