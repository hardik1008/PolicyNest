# PolicyNest usability test: synthetic image pack

Made 14 Nov 2026 for `USABILITY_TEST_PLAN.md` (task A2, A4 and the optional stretch task A2b). One invented person, **Rahul Kulkarni**, with five clean documents and two defect variants. Everything is made up: the name, PAN, Aadhaar last four digits, roll number, account number and IFSC. No real person's data is used, and **no full Aadhaar number appears anywhere** (only `XXXX XXXX 6407`).

Every image carries the words **SPECIMEN, SYNTHETIC** twice: a red banner line at the top (as in the PS-01 specimens) and a faint repeated diagonal watermark. The photo boxes hold a plain grey avatar icon. **No face is drawn.** Layout and wording follow Specimens 1 to 3 in `PS-01_specimen_documents.docx` (same lines, same order, same labels); the person's own values are different.

## 1. Details to type into the form ("Your details")

| Field | Type this |
| --- | --- |
| Full name as on PAN | `Rahul Kulkarni` |
| Date of birth | `17/09/1996` (17 September 1996) |
| PAN | `QWTPK7305L` |
| Aadhaar, last four digits | `6407` |
| Mobile number | `9000012345` |
| Email | `rahul.kulkarni.test@example.com` |
| Highest education | `Graduate` |
| State | `Maharashtra` |
| City | `Pune` |
| Account number | `612304583829` |
| IFSC | `NEST0371264` |
| Consent | tick the box |

Father (printed on PAN, Aadhaar back and marksheet): Suresh Kulkarni. Address on the Aadhaar back: 214, Lakshmi Nagar, Pune, Maharashtra - 411057.

## 2. Files and expected result

Upload each file in the slot named in the table. Images are PNG, about 400 dpi if printed at actual size. Cards are 85.6 x 54 mm, the marksheet 98 x 140 mm, the cheque 190 x 76 mm.

| File | Slot | Expected result in the app |
| --- | --- | --- |
| `01_PAN_card.png` | PAN card | Verified. Reads name RAHUL KULKARNI, DOB 17 Sep 1996, PAN XXXXXX305L. |
| `02_Aadhaar_front_masked.png` | Aadhaar card (front) | Verified. Reads name, DOB 17 Sep 1996, XXXX-XXXX-6407. |
| `03_Aadhaar_back_masked.png` | Aadhaar card (back) | Verified. Reads address state Maharashtra. |
| `04_Class10_marksheet.png` | Class 10 marksheet | Verified. Reads name, DOB, Result PASS (board: Maharashtra State Board of Secondary Education). |
| `05_Cancelled_cheque.png` | Cancelled cheque or bank statement | Verified. Reads holder RAHUL KULKARNI, IFSC NEST0371264, account ending 3829. |
| `variants/04b_Class10_marksheet_BLURRY_dob_unreadable.png` | Class 10 marksheet | Accepted into the slot, but "Fields read: Not all read" and "Could not read: date of birth". After Submit the case is NEEDS_MORE_INFO and the follow-up message says the marksheet photo is not clear. **Re-upload path (T5).** |
| `variants/05b_Cancelled_cheque_PARENT_name.png` | Cancelled cheque or bank statement | Accepted into the slot (holder SURESH KULKARNI). After Submit the follow-up message says the bank account is not in the applicant's name. **Parent's account (T5).** Account last four and IFSC are the same as the clean cheque, so only the holder name differs. |

A clean set (01 to 05, plus a selfie) ends in **KYC approved** with no follow-up. The two variants together give **"2 things to fix"** in one message; replacing them with `04` and `05` and sending the fixes gives **KYC approved** after one follow-up round.

**Wrong slot:** any of the five files dropped in another slot (including the selfie slot, and the Aadhaar front in the back slot or the reverse) is refused with a plain reason such as "This looks like a PAN card, not a Class 10 marksheet. Upload your Class 10 marksheet here."

## 3. The selfie (no image provided on purpose)

There is no selfie in the pack, and none should be made up: no photo of a real person, no stock photo, no generated face. Options, best first:

1. **"Use specimen" in the selfie slot.** Gives a clean simulated face match (0.91), skips the camera. Fine for the document tasks. The face-match step is simulated in the app anyway.
2. **The participant takes a selfie of themselves** with their own phone, as a role-play applicant. The photo stays in the browser (the app says nothing leaves it). Do not save or share these photos after the session. The slot refuses images that look like documents or are mostly text, and where the browser has a face detector it refuses images with no face.
3. For the borderline-score task (T8), pick **"Borderline score 0.68"** in the selfie slot's specimen dropdown, then "Use specimen".

Caution: on browsers without a face detector (desktop Chrome has none), the selfie slot accepts any photo without document text. A landscape photo or a gradient was accepted in testing. Moderators should not read "selfie verified" as "a face was found".

## 4. Printing and photographing (task A2b)

- `print/print_layout_A4_clean_set.pdf` (or `.html`): **one A4 page, actual size**, the five clean documents with dashed cut lines. Print at 100% / "Actual size", not "Fit to page". Check one card against a bank card: the PAN and Aadhaar should be about the same size.
- `print/print_layout_A4_defect_variants.pdf`: one A4 page with the two variants, for task A4 if you want them on paper. The blurry marksheet is blurry in the file itself, so photographing it keeps it blurry; that is intended.
- Tips are printed on the sheet: daylight, paper flat, phone parallel above, all four corners in frame, no glare.
- Photographs of paper will score lower OCR confidence than the files. Record what happens: this is the real phone-photo evidence for PRODUCT.md gap D6. The app treats confidence below 0.75 as unreadable, and the clean cheque file already reads at about 0.83, so a phone photo of the cheque is the likeliest to ask for a re-upload.

## 5. Verification log (live site, 14 Nov 2026)

Site: https://policynest.embarko.app, on-device OCR as deployed, Chrome (desktop, headless), driven by `tools/verify_live.py` through each slot's real `<input type=file>` (a genuine `File` and `change` event, not the "Use specimen" path). Nothing in the app or the deployment was changed. Pack-making changes made after the first run are listed under "Fixes made while testing".

| Check | Result |
| --- | --- |
| Five clean images, each in its own slot | **5 of 5 Verified**, "Fields read: Passed" on all. OCR confidence: PAN 0.94, Aadhaar front 0.92, Aadhaar back 0.90, marksheet 0.94, cheque 0.83. First upload took about 6 s (engine load), the rest 1 to 3 s. |
| Wrong slots: each of the five files into the four other document slots, and into the selfie slot | **25 of 25 refused**, each with the correct "looks like X, not Y" reason. Front and back Aadhaar in each other's slot are also refused. |
| Full run: five clean images + "Use specimen" selfie, Submit | **KYC approved**, "All checks passed. Nothing needs a second look." |
| T5: blurry marksheet + parent's cheque + the three clean cards + specimen selfie, Submit | Marksheet shown as "DOB not read"; decision **"2 things to fix"**, one message: marksheet photo not clear, so the date of birth could not be read; bank account not in the applicant's name. |
| T5 fix: upload clean `04` and `05`, send for re-check | **KYC approved** after 1 follow-up round. |

Not run: each variant on its own (they were run together, as T5 does), the Hindi message, and anything on a phone or with printed paper.

### Fixes made while testing (pack only)

- First PAN `QWTPK4829F` was read by OCR as `QWTPKA4829F` (a stray "A"), so the app said "PAN not read". The PAN was changed to `QWTPK7305L`, which reads correctly.
- Watermark made fainter (alpha 30 to 17) after that, to keep it from touching the OCR text.
- First marksheet used the board name "Maharashtra State Board of Secondary **and Higher Secondary** Education" (the wording of Specimen 5). The app refused it as a Class 12 marksheet. See the finding below; the pack uses "Maharashtra State Board of Secondary Education" so the clean set verifies.

### Findings for the product (not changed here)

1. **Class 10 marksheet wrongly refused as "Class 12".** `classify` in `PolicyNest.html` treats the phrase "HIGHER SECONDARY" as Class 12. A Class 10 marksheet whose board name contains it (Specimen 5's board, and real Maharashtra SSC sheets use that board name) is refused in the Class 10 slot with "This looks like a Class 12 marksheet". Reproduced on the live site with a scratch image. Suggest the Class 12 test look for "SENIOR SECONDARY", "CLASS XII" and similar on lines other than the board name.
2. **Selfie slot accepts any text-free photo** where `FaceDetector` does not exist (see section 3).
3. The browser console shows one 404 (a resource that is not found) on page load. It did not affect any test.

## 6. Regenerating

Pillow is not installed globally; the images were made with Pillow and Playwright installed into a scratch folder. `tools/` holds everything needed:

```bash
# PYTHONPATH must point at a folder containing PIL (and playwright for the last two)
python tools/make_pack.py .          # the seven PNGs
python tools/make_print.py           # the two A4 HTML and PDF files
python tools/verify_live.py clean wrong full t5   # re-run the live-site checks
```

If the images are regenerated, re-run `verify_live.py`: OCR results depend on the fonts and on the site's OCR build.
