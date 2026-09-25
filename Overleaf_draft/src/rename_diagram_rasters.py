"""Patch the old method name inside the three raster pipeline diagrams (PNG embedded in PDF) and re-wrap them as PDFs. CPU-only.
    source venv_CITA/bin/activate && python3 -u Overleaf_draft/src/rename_diagram_rasters.py 2>&1 | tee logs/rename_diagram_rasters.log

The draw.io sources of cita_pipeline / evaluation_pipeline are gone (only training_pipeline.svg
survived, and its text lives in foreignObject nodes that no local converter renders), so the
embedded rasters are edited in place: the ink box of each old label is measured, painted over
with the surrounding fill, and the new label is drawn in the same face at the size whose
rendered width of the OLD string matches the measured box (so the size is inferred, not guessed).
A label that shares its line with an emoji (the star before "CITA" in training_pipeline) is
re-centred as a group: the emoji patch is moved left by half the width increase. Every other
pixel is untouched, which the script asserts.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = Path(__file__).parent.parent.parent
FIG_DIR = PROJECT_ROOT / "Overleaf_draft" / "v5_arxiv_v2_SwiPO" / "figures" / "pipeline"
SCRATCH = Path(sys.argv[1]) if len(sys.argv) > 1 else PROJECT_ROOT / "outputs" / "diagram_rasters"
SANS_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
SERIF_BOLD = "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"
INK = 110   # grey level below which a pixel counts as text ink
PAD = 4     # px painted around the old ink box

# ROIs are interior regions (no box borders) measured on the 7616-px-wide rasters (scratch crops
# of 2026-09-24). `roi` must contain exactly one text line with the old name. `fit_new_to_box`
# shrinks the NEW string to the old ink width when the box cannot take a wider line (the
# evaluation INPUT box is 1,030 px wide; "GRPO,SwiPO)" at the inherited size would overrun it).
# `neighbor` is an emoji patch on the same line that is shifted left to keep the pair centred;
# `bounds` is the box interior the new line must stay inside (defaults to `roi`).
JOBS = [
    dict(stem="cita_pipeline", roi=(1800, 60, 5800, 240), font=SANS_BOLD,
         old="CITA (Contrastive Instruction-Tuned Alignment) Pipeline", new="SwiPO (Switchable Preference Optimization) Pipeline"),
    # OUTPUT boxes: interiors span x 6225-7495 (upper) and 6285-7440 (lower); the ROIs start
    # inside the left border, otherwise the border counts as ink and gets erased.
    dict(stem="cita_pipeline", roi=(6300, 2400, 7440, 2540), font=SERIF_BOLD, old="CITA_NoInstruct", new="SwiPO_NoInstruct",
         bounds=(6230, 2390, 7490, 2550)),
    dict(stem="cita_pipeline", roi=(6300, 3220, 7420, 3360), font=SERIF_BOLD, old="CITA_Instruct", new="SwiPO_Instruct",
         bounds=(6290, 3210, 7435, 3370)),
    # INPUT box interior spans x 120-1140; the text line is x 350-910, so the wider new word still fits.
    dict(stem="evaluation_pipeline", roi=(200, 2440, 1000, 2570), font=SERIF_BOLD, old="GRPO,CITA)", new="GRPO,SwiPO)",
         bounds=(125, 2430, 1135, 2580)),
    dict(stem="training_pipeline", roi=(4420, 880, 4760, 1040), font=SANS_BOLD, old="CITA", new="SwiPO",
         neighbor=(4250, 880, 4420, 1040), bounds=(3980, 860, 5030, 1060)),
]


def ink_bbox(gray: np.ndarray, roi: tuple) -> tuple:
    x0, y0, x1, y1 = roi
    mask = gray[y0:y1, x0:x1] < INK
    rows, cols = np.where(mask.any(axis=1))[0], np.where(mask.any(axis=0))[0]
    if len(rows) == 0:
        raise RuntimeError(f"no ink in ROI {roi}")
    return x0 + cols.min(), y0 + rows.min(), x0 + cols.max() + 1, y0 + rows.max() + 1


def fit_font(path: str, text: str, target_width: int) -> ImageFont.FreeTypeFont:
    """Smallest size whose rendered width of `text` reaches target_width (width is monotone in size)."""
    lo, hi = 8, 600
    while lo < hi:
        mid = (lo + hi) // 2
        if ImageFont.truetype(path, mid).getbbox(text)[2] < target_width:
            lo = mid + 1
        else:
            hi = mid
    return ImageFont.truetype(path, lo)


def extract(stem: str) -> Path:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    subprocess.run(["pdfimages", "-png", str(FIG_DIR / f"{stem}.pdf"), str(SCRATCH / stem)], check=True)
    pngs = sorted(SCRATCH.glob(f"{stem}-*.png"))
    if len(pngs) != 1:
        raise RuntimeError(f"{stem}.pdf: expected one embedded image, found {len(pngs)}")
    return pngs[0]


def patch(im: Image.Image, job: dict) -> tuple:
    """Replace one label; returns (touched x0, y0, x1, y1) for the change audit."""
    gray = np.asarray(im.convert("L"))
    bx0, by0, bx1, by1 = ink_bbox(gray, job["roi"])
    fill = tuple(int(v) for v in np.asarray(im)[by0 - 3, bx0 - 3])      # background just outside the ink
    old, new = job["old"], job["new"]
    fit_to = (bx1 - bx0 - 8) if job.get("fit_new_to_box") else (bx1 - bx0)
    font = fit_font(job["font"], new if job.get("fit_new_to_box") else old, fit_to)
    nb, ob = font.getbbox(new), font.getbbox(old)
    new_w = nb[2] - nb[0]
    draw = ImageDraw.Draw(im)
    draw.rectangle([bx0 - PAD, by0 - PAD, bx1 + PAD, by1 + PAD], fill=fill)
    touched = [bx0 - PAD, by0 - PAD, bx1 + PAD, by1 + PAD]

    if job.get("neighbor"):                                              # emoji + word: re-centre the pair
        n_x0, n_y0, n_x1, n_y1 = job["neighbor"]
        rgb = np.asarray(im)[n_y0:n_y1, n_x0:n_x1]
        non_bg = (np.abs(rgb.astype(np.int16) - np.array(fill, dtype=np.int16)).sum(-1) > 30)
        rows, cols = np.where(non_bg.any(axis=1))[0], np.where(non_bg.any(axis=0))[0]
        s_x0, s_x1 = n_x0 + cols.min(), n_x0 + cols.max() + 1
        s_y0, s_y1 = n_y0 + rows.min(), n_y0 + rows.max() + 1
        star = im.crop((s_x0, s_y0, s_x1, s_y1))
        gap = bx0 - s_x1
        group_center = (s_x0 + bx1) / 2
        total = (s_x1 - s_x0) + gap + new_w
        new_s_x0 = int(round(group_center - total / 2))
        draw.rectangle([s_x0 - PAD, s_y0 - PAD, s_x1 + PAD, s_y1 + PAD], fill=fill)
        im.paste(star, (new_s_x0, s_y0))
        text_x0 = new_s_x0 + (s_x1 - s_x0) + gap
        touched = [min(touched[0], min(s_x0, new_s_x0) - PAD), min(touched[1], s_y0 - PAD),
                   max(touched[2], text_x0 + new_w + PAD), max(touched[3], s_y1 + PAD)]
        print(f"  emoji patch {s_x0}-{s_x1} -> {new_s_x0}-{new_s_x0 + (s_x1 - s_x0)} (gap {gap} px kept)")
    else:
        text_x0 = (bx0 + bx1) / 2 - new_w / 2

    x = text_x0 - nb[0]
    y = by0 - ob[1]                                                     # old top-of-ink was at by0
    draw.text((x, y), new, font=font, fill=(0, 0, 0))
    nx0, nx1 = int(x + nb[0]), int(x + nb[2])
    touched = [min(touched[0], nx0 - PAD), touched[1], max(touched[2], nx1 + PAD), max(touched[3], int(y + nb[3]) + PAD)]
    b = job.get("bounds", job["roi"])
    print(f"{job['stem']}: '{old}' box x{bx0}-{bx1} y{by0}-{by1} (h={by1 - by0}) -> '{new}' at size {font.size}, "
          f"new x{nx0}-{nx1}; fill={fill}")
    if nx0 < b[0] - 4 or nx1 > b[2] + 4:                                 # 4-px tolerance for glyph side bearings
        raise RuntimeError(f"{job['stem']}: new label {nx0}-{nx1} leaves its bounds {b}")
    return tuple(touched)


def main() -> None:
    images, originals, touched = {}, {}, {}
    for job in JOBS:
        stem = job["stem"]
        if stem not in images:
            images[stem] = Image.open(extract(stem)).convert("RGB")
            originals[stem] = np.asarray(images[stem]).copy()
            touched[stem] = []
        touched[stem].append(patch(images[stem], job))

    for stem, im in images.items():
        diff = (np.abs(np.asarray(im).astype(np.int16) - originals[stem].astype(np.int16)).sum(-1) > 0)
        allowed = np.zeros_like(diff)
        for x0, y0, x1, y1 in touched[stem]:
            allowed[y0:y1 + 1, x0:x1 + 1] = True      # PIL rectangles are inclusive of x1, y1
        stray = int((diff & ~allowed).sum())
        if stray:
            ys, xs = np.where(diff & ~allowed)
            im.crop((xs.min() - 40, ys.min() - 40, xs.max() + 40, ys.max() + 40)).save(SCRATCH / f"{stem}_stray.png")
            raise RuntimeError(f"{stem}: {stray} pixels changed outside the patched boxes, at x{xs.min()}-{xs.max()} "
                               f"y{ys.min()}-{ys.max()} (boxes: {touched[stem]}); crop saved to {stem}_stray.png")
        im.save(SCRATCH / f"{stem}_swipo.png")
        pdf = FIG_DIR / f"{stem}.pdf"
        im.save(pdf, "PDF", resolution=300.0)
        print(f"{stem}: changed px inside patched boxes = {int(diff.sum())}, stray = 0 -> {pdf}")


if __name__ == "__main__":
    main()
