"""Drive the live PolicyNest site with the image pack and print what the app says for each upload.

Uses Playwright with the installed Chrome (Playwright was pip-installed into a scratch folder; set PYTHONPATH).
Each upload goes through the real <input type=file> of the slot (a genuine File, change event, on-device OCR).
Usage: python verify_live.py [group ...]   groups: clean wrong full t5   (default: all)
"""
import sys, os, time, json
from playwright.sync_api import sync_playwright

URL = os.environ.get("PN_URL", "https://policynest.embarko.app/#apply")
PACK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = {
    "PAN": "01_PAN_card.png", "AADHAAR_FRONT": "02_Aadhaar_front_masked.png", "AADHAAR_BACK": "03_Aadhaar_back_masked.png",
    "CLASS10": "04_Class10_marksheet.png", "BANK": "05_Cancelled_cheque.png",
}
V = {"CLASS10": "variants/04b_Class10_marksheet_BLURRY_dob_unreadable.png", "BANK": "variants/05b_Cancelled_cheque_PARENT_name.png"}
SLOTS = ["PAN", "AADHAAR_FRONT", "AADHAAR_BACK", "CLASS10", "BANK", "SELFIE"]
DETAILS = {"name": "Rahul Kulkarni", "dob": "1996-09-17", "pan": "QWTPK7305L", "aadhaar4": "6407", "mobile": "9000012345",
           "email": "rahul.kulkarni.test@example.com", "city": "Pune", "acct": "612304583829", "ifsc": "NEST0371264"}


def path(rel):
    return os.path.join(PACK, rel)


def open_app(p):
    b = p.chromium.launch(channel="chrome", headless=True)
    pg = b.new_page(viewport={"width": 1300, "height": 1000})
    pg.on("console", lambda m: print("   [console]", m.type, m.text[:200]) if m.type == "error" else None)
    pg.goto(URL, wait_until="networkidle")
    return b, pg


def fill_details(pg):
    pg.click('[data-act="go-apply"]') if pg.query_selector('[data-act="go-apply"]') else None
    for k, v in DETAILS.items():
        pg.fill("#f-" + k, v)
    pg.select_option("#f-education", "Graduate")
    pg.select_option("#f-state", "Maharashtra")
    pg.check("#f-consent")
    pg.click('[data-act="details-next"]')
    pg.wait_for_selector("#up-PAN", state="attached")


def card(pg, k):
    el = pg.query_selector(".vcard.k-" + k)
    return el.inner_text().replace("\n", " | ") if el else "(no card)"


def upload(pg, slot, rel, wait=90):
    pg.set_input_files("#up-" + slot, path(rel))
    t0 = time.time()
    while time.time() - t0 < wait:
        txt = card(pg, slot)
        if "Reading text" not in txt and "In progress" not in txt and ("Verified" in txt or "Not accepted" in txt):
            return txt, round(time.time() - t0, 1)
        time.sleep(0.5)
    return card(pg, slot) + " [TIMEOUT]", wait


def status(txt):
    return "VERIFIED" if "Verified" in txt and "Not accepted" not in txt else "REFUSED" if "Not accepted" in txt else "?"


def g_clean(p):
    print("== clean images into their own slots")
    b, pg = open_app(p)
    fill_details(pg)
    for k in ["PAN", "AADHAAR_FRONT", "AADHAAR_BACK", "CLASS10", "BANK"]:
        txt, s = upload(pg, k, F[k])
        print(" %-14s %-8s %5.1fs  %s" % (k, status(txt), s, txt[:420]))
    b.close()


def g_wrong(p):
    print("== wrong slots (each file into every other slot, plus every file into the selfie slot)")
    b, pg = open_app(p)
    fill_details(pg)
    for k, rel in F.items():
        for slot in SLOTS:
            if slot == k:
                continue
            txt, s = upload(pg, slot, rel)
            print(" file %-14s -> slot %-14s %-8s %s" % (k, slot, status(txt), txt.split("What to fix |")[-1][:170]))
    b.close()


def finish_flow(pg):
    pg.click('[data-spec="SELFIE"]')
    for _ in range(40):
        if "Verified" in card(pg, "SELFIE"):
            break
        time.sleep(0.5)
    time.sleep(1)
    pg.click('[data-act="submit"]')
    pg.wait_for_selector('.verdict', timeout=40000)
    time.sleep(2)
    return pg.inner_text(".verdict").replace("\n", " | ")


def g_full(p):
    print("== full run: five clean images + specimen selfie")
    b, pg = open_app(p)
    fill_details(pg)
    for k in ["PAN", "AADHAAR_FRONT", "AADHAAR_BACK", "CLASS10", "BANK"]:
        upload(pg, k, F[k])
    print(" verdict:", finish_flow(pg))
    print(" checks:", pg.inner_text(".cards").replace("\n", " | ")[:1800])
    b.close()


def g_t5(p):
    print("== T5: blurry marksheet + parent's cheque")
    b, pg = open_app(p)
    fill_details(pg)
    for k in ["PAN", "AADHAAR_FRONT", "AADHAAR_BACK"]:
        upload(pg, k, F[k])
    for k in ["CLASS10", "BANK"]:
        txt, s = upload(pg, k, V[k])
        print(" variant %-8s %-8s %s" % (k, status(txt), txt[:400]))
    print(" verdict:", finish_flow(pg))
    print(" message:", (pg.inner_text(".msg") if pg.query_selector(".msg") else "(none)").replace("\n", " | ")[:800])
    for k in ["CLASS10", "BANK"]:
        txt, s = upload(pg, k, F[k])
        print(" fix %-8s %-8s %s" % (k, status(txt), txt[:200]))
    time.sleep(1)
    pg.click('[data-act="resubmit"]')
    time.sleep(5)
    print(" after re-check:", pg.inner_text(".verdict").replace("\n", " | "))
    b.close()


if __name__ == "__main__":
    groups = sys.argv[1:] or ["clean", "wrong", "full", "t5"]
    with sync_playwright() as p:
        for g in groups:
            {"clean": g_clean, "wrong": g_wrong, "full": g_full, "t5": g_t5}[g](p)
