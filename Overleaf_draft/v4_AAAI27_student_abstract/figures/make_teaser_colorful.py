"""Rasterise the v3 teaser (Google-Sheets PDF with colour text + emoji verdicts), crop it outside LaTeX, and patch the trainer label CITA -> SwiPO. CPU-only.
    source venv_CITA/bin/activate && python3 -u Overleaf_draft/v4_AAAI27_student_abstract/figures/make_teaser_colorful.py

Why a raster: the source PDF embeds CID (Identity-H) fonts, which the AAAI kit rejects, and the
kit forbids trim/clip in \\includegraphics, so the page is rendered at 600 dpi, cropped to its ink
box, and the one old-name cell is repainted in the same face (Arial) at the size whose rendered
width of "CITA" matches the measured ink box. The script asserts that no pixel outside that cell
changed relative to the plain render.
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
SRC = HERE.parent.parent / "v3_submission_ARR" / "figures" / "misc" / "teaser_single_prompt_idx287.pdf"
OUT = HERE / "teaser_colorful.png"
DPI = 600
ARIAL = "/System/Library/Fonts/Supplemental/Arial.ttf"
INK = 120
MARGIN_PX = 12
# Trainer-column cell that reads "CITA": on the 90-dpi render the word sits at x 52-85 px,
# y 150-165 px inside a cell spanning x 30-110, y 120-195 (90 dpi -> 600 dpi is x 6.67);
# the ROI stays inside the cell so no border line counts as ink.
CELL_ROI = (int(330 * DPI / 600), int(990 * DPI / 600), int(600 * DPI / 600), int(1110 * DPI / 600))


def ink_bbox(gray: np.ndarray, roi=None) -> tuple:
    x0, y0 = (0, 0) if roi is None else roi[:2]
    sub = gray if roi is None else gray[roi[1]:roi[3], roi[0]:roi[2]]
    mask = sub < INK
    rows, cols = np.where(mask.any(axis=1))[0], np.where(mask.any(axis=0))[0]
    if len(rows) == 0:
        raise RuntimeError(f"no ink in {roi}")
    return x0 + cols.min(), y0 + rows.min(), x0 + cols.max() + 1, y0 + rows.max() + 1


def fit_font(text: str, target_width: int) -> ImageFont.FreeTypeFont:
    lo, hi = 8, 400
    while lo < hi:
        mid = (lo + hi) // 2
        if ImageFont.truetype(ARIAL, mid).getbbox(text)[2] < target_width:
            lo = mid + 1
        else:
            hi = mid
    return ImageFont.truetype(ARIAL, lo)


def main() -> None:
    with tempfile.TemporaryDirectory() as td:
        stem = Path(td) / "page"
        subprocess.run(["pdftoppm", "-r", str(DPI), "-png", "-singlefile", str(SRC), str(stem)], check=True)
        page = Image.open(f"{stem}.png").convert("RGB")
    gray = np.asarray(page.convert("L"))
    # crop to the content (the source page is letter-size with the table in its upper part)
    non_white = np.asarray(page).min(axis=2) < 250
    rows, cols = np.where(non_white.any(axis=1))[0], np.where(non_white.any(axis=0))[0]
    x0, y0, x1, y1 = cols.min() - MARGIN_PX, rows.min() - MARGIN_PX, cols.max() + 1 + MARGIN_PX, rows.max() + 1 + MARGIN_PX
    crop = page.crop((x0, y0, x1, y1))
    before = np.asarray(crop).copy()

    # patch the trainer label
    roi = (CELL_ROI[0] - x0, CELL_ROI[1] - y0, CELL_ROI[2] - x0, CELL_ROI[3] - y0)
    bx0, by0, bx1, by1 = ink_bbox(np.asarray(crop.convert("L")), roi)
    if not (40 <= by1 - by0 <= 160):                      # a word, not a border line or a whole row
        raise RuntimeError(f"ink box h={by1 - by0} px in the trainer cell is not one text line: {(bx0, by0, bx1, by1)}")
    font = fit_font("CITA", bx1 - bx0)
    nb, ob = font.getbbox("SwiPO"), font.getbbox("CITA")
    draw = ImageDraw.Draw(crop)
    draw.rectangle([bx0 - 4, by0 - 4, bx1 + 4, by1 + 4], fill=(255, 255, 255))
    cx = (bx0 + bx1) / 2
    x = cx - (nb[2] - nb[0]) / 2 - nb[0]
    y = by0 - ob[1]
    draw.text((x, y), "SwiPO", font=font, fill=(0, 0, 0))
    nx0, nx1, ny1 = int(x + nb[0]), int(x + nb[2]), int(y + nb[3])
    touched = (min(bx0 - 4, nx0 - 4), by0 - 4, max(bx1 + 4, nx1 + 4), max(by1 + 4, ny1 + 4))

    after = np.asarray(crop)
    diff = (np.abs(after.astype(np.int16) - before.astype(np.int16)).sum(-1) > 0)
    allowed = np.zeros_like(diff)
    allowed[touched[1]:touched[3] + 1, touched[0]:touched[2] + 1] = True
    stray = int((diff & ~allowed).sum())
    if stray:
        raise RuntimeError(f"{stray} pixels changed outside the patched cell")
    crop.save(OUT, dpi=(DPI, DPI), optimize=True)
    w_pt, h_pt = crop.width * 72 / DPI, crop.height * 72 / DPI
    print(f"'CITA' ink box x{bx0}-{bx1} y{by0}-{by1} -> 'SwiPO' at Arial {font.size}px, x{nx0}-{nx1}; stray px = 0")
    print(f"{OUT.name}: {crop.width}x{crop.height} px @ {DPI} dpi = {w_pt:.0f} x {h_pt:.0f} pt; "
          f"at \\textwidth (504 pt) scale = {504 / w_pt:.3f}")


if __name__ == "__main__":
    main()
