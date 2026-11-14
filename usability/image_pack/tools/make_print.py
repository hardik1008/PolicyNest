"""Build the A4 print layouts (actual size) as HTML and PDF. Needs Playwright + installed Chrome for the PDF.
Run from anywhere:  python make_print.py
Sizes: PAN and Aadhaar 85.6 x 54 mm (ID-1 card), marksheet 98 x 140 mm, cheque 190 x 76 mm.
"""
import os
from playwright.sync_api import sync_playwright

PACK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRINT = os.path.join(PACK, "print")

CSS = """
@page { size: 210mm 297mm; margin: 0 }
* { box-sizing: border-box }
html, body { margin: 0; padding: 0; background: #fff }
body { font-family: Arial, Helvetica, sans-serif; color: #222 }
.page { position: relative; width: 210mm; height: 297mm; overflow: hidden; page-break-after: always }
.page:last-child { page-break-after: auto }
h1 { position: absolute; left: 10mm; top: 7mm; margin: 0; font-size: 4.4mm; line-height: 1.2 }
.sub { position: absolute; left: 10mm; top: 13.2mm; width: 190mm; font-size: 2.7mm; line-height: 1.35; color: #444 }
.cap { position: absolute; font-size: 2.5mm; color: #555; line-height: 1.2 }
img { position: absolute; display: block }
.cut { position: absolute; border: 0.2mm dashed #777 }
.how { position: absolute; border: 0.25mm solid #999; border-radius: 1.5mm; padding: 2.2mm 2.8mm; font-size: 2.55mm; line-height: 1.4; color: #333 }
.how b { font-size: 2.8mm }
.how ul { margin: 1mm 0 0; padding-left: 3.6mm }
.foot { position: absolute; left: 10mm; bottom: 4mm; font-size: 2.3mm; color: #777 }
"""


def item(x, y, w, h, src, cap, capdy=-3.6):
    return ('<div class="cap" style="left:%smm;top:%smm">%s</div>'
            '<div class="cut" style="left:%smm;top:%smm;width:%smm;height:%smm"></div>'
            '<img src="../%s" style="left:%smm;top:%smm;width:%smm;height:%smm" alt="">'
            % (x, y + capdy - 0.6, cap, x - 1, y - 1, w + 2, h + 2, src, x, y, w, h))


def page1():
    return ('<section class="page"><h1>PolicyNest usability test: Rahul Kulkarni\'s documents (SPECIMEN, SYNTHETIC)</h1>'
            '<div class="sub">Invented person, invented numbers. Not real documents. Print on A4 at <b>100% / Actual size</b> '
            '(turn off "Fit to page"). Cut along the dashed lines, then photograph each paper with the phone camera and upload it in the matching slot.</div>'
            + item(10, 26, 85.6, 54, "01_PAN_card.png", "1. PAN card (85.6 x 54 mm)")
            + item(10, 88, 85.6, 54, "02_Aadhaar_front_masked.png", "2. Aadhaar, front (masked, last four digits only)")
            + item(10, 150, 85.6, 54, "03_Aadhaar_back_masked.png", "3. Aadhaar, back (masked)")
            + item(104, 26, 98, 140, "04_Class10_marksheet.png", "4. Class 10 marksheet")
            + '<div class="how" style="left:104mm;top:172mm;width:98mm;height:32mm"><b>Photographing tips</b><ul>'
              '<li>Daylight, paper flat on a table, phone parallel above it.</li>'
              '<li>All four corners in the frame, no glare, no finger on the paper.</li>'
              '<li>Upload each photo in its own slot. The selfie is not here: see the README.</li></ul></div>'
            + item(10, 212, 190, 76, "05_Cancelled_cheque.png", "5. Cancelled cheque (190 x 76 mm)")
            + '<div class="foot">Synthetic specimen pack for PolicyNest usability tests. Page 1 of 1 (clean set). Defect variants are on a separate page.</div></section>')


def page2():
    return ('<section class="page"><h1>PolicyNest usability test: defect variants (SPECIMEN, SYNTHETIC)</h1>'
            '<div class="sub">Use these only for task A4 (scenario T5). The marksheet is deliberately out of focus with the date of birth unreadable. '
            'The cheque is in the account holder\'s father\'s name. Print at <b>100% / Actual size</b>.</div>'
            + item(10, 26, 98, 140, "variants/04b_Class10_marksheet_BLURRY_dob_unreadable.png", "4b. Class 10 marksheet, blurry, date of birth unreadable (T5)")
            + item(10, 190, 190, 76, "variants/05b_Cancelled_cheque_PARENT_name.png", "5b. Cancelled cheque in a parent's name (T5)")
            + '<div class="foot">Synthetic specimen pack for PolicyNest usability tests. Variants page.</div></section>')


def html(body, title):
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>%s</title><style>%s</style></head><body>%s</body></html>'
            % (title, CSS, body))


def main():
    os.makedirs(PRINT, exist_ok=True)
    jobs = [("print_layout_A4_clean_set", page1(), "PolicyNest clean set"), ("print_layout_A4_defect_variants", page2(), "PolicyNest defect variants")]
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        for name, body, title in jobs:
            hp = os.path.join(PRINT, name + ".html")
            open(hp, "w", encoding="utf-8").write(html(body, title))
            pg = b.new_page()
            pg.goto("file:///" + hp.replace("\\", "/"))
            pg.wait_for_load_state("networkidle")
            pg.pdf(path=os.path.join(PRINT, name + ".pdf"), width="210mm", height="297mm", print_background=True, prefer_css_page_size=True,
                   margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
            pg.close()
        b.close()
    print("done")


if __name__ == "__main__":
    main()
