#!/usr/bin/env python3
"""Replace 01.09.2026 with 07.09.2026 on the scanned training attendance PDF.

The source is an image-only scan. Each date is corrected by erasing the
second digit of the day ('1') and drawing a matching serif '7'.
"""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

import numpy as np
import pymupdf
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
SOURCE_PDF = ROOT / "CCF17092026_Egitime_Katilim_Tutanagi_orijinal.pdf"
OUTPUT_PDF = ROOT / "CCF17092026_Egitime_Katilim_Tutanagi_07.09.2026.pdf"

TINOS_REGULAR = Path("/usr/share/fonts/truetype/croscore/Tinos-Regular.ttf")
TINOS_BOLD = Path("/usr/share/fonts/truetype/croscore/Tinos-Bold.ttf")

# Pixel boxes on the extracted 2409x3437 page images (JPEG, 1:1 with the PDF).
# (x, y, w, h) is the bounding box of the '1' in 01.09.2026.
DATE_EDITS = (
    {
        "page": 0,
        "name": "table_date",
        "box": (1010, 356, 15, 29),
        "pad": 2,
        "font_size": 44,
        "bold": False,
        "origin": (1010, 356),
    },
    {
        "page": 0,
        "name": "left_signature_date",
        "box": (506, 2608, 15, 29),
        "pad": 2,
        "font_size": 44,
        "bold": False,
        "origin": (506, 2608),
    },
    {
        "page": 0,
        "name": "right_signature_date",
        "box": (1684, 2648, 15, 29),
        "pad": 2,
        "font_size": 44,
        "bold": False,
        "origin": (1684, 2648),
    },
    {
        "page": 1,
        "name": "content_paragraph_date",
        "box": (1488, 2305, 20, 31),
        "pad": 0,
        "font_size": 47,
        "bold": True,
        "origin": (1489, 2306),
    },
)


def _sample_ink_and_paper(image: Image.Image, x: int, y: int, w: int, h: int) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    arr = np.array(image.crop((x, y, x + w, y + h)))
    gray = arr.mean(axis=2)
    dark = gray < 90
    light = gray > 200
    if dark.any():
        ink = tuple(int(v) for v in np.percentile(arr[dark], 18, axis=0))
    else:
        ink = (40, 40, 40)
    if light.any():
        paper = tuple(int(v) for v in np.median(arr[light], axis=0))
    else:
        paper = (252, 252, 252)
    return ink, paper  # type: ignore[return-value]


def _erase_digit(
    image: Image.Image,
    x: int,
    y: int,
    w: int,
    h: int,
    pad: int,
    paper: tuple[int, int, int],
) -> Image.Image:
    x0, y0, x1, y1 = x - pad, y - pad, x + w + pad, y + h + pad
    region = np.array(image.crop((x0, y0, x1, y1)))
    gray = region.mean(axis=2)
    dark = gray < 188
    dilated = np.zeros_like(dark)
    padded = np.pad(dark.astype(np.uint8), 1)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            dilated |= padded[
                1 + dy : 1 + dy + dark.shape[0],
                1 + dx : 1 + dx + dark.shape[1],
            ].astype(bool)
    region[dilated] = paper
    out = image.copy()
    out.paste(Image.fromarray(region), (x0, y0))
    return out


def _draw_seven(
    image: Image.Image,
    origin_x: int,
    origin_y: int,
    font_size: int,
    ink: tuple[int, int, int],
    bold: bool,
) -> Image.Image:
    font_path = TINOS_BOLD if bold else TINOS_REGULAR
    font = ImageFont.truetype(str(font_path), font_size)

    probe = Image.new("L", (120, 120), 0)
    ImageDraw.Draw(probe).text((20, 20), "1", font=font, fill=255)
    one_box = probe.getbbox()
    if one_box is None:
        raise RuntimeError("Failed to measure digit 1")

    text_x = origin_x - (one_box[0] - 20)
    text_y = origin_y - (one_box[1] - 20)

    glyph = Image.new("L", (120, 120), 0)
    ImageDraw.Draw(glyph).text((20, 20), "7", font=font, fill=255)
    glyph = glyph.filter(ImageFilter.GaussianBlur(radius=0.35))

    colored = Image.new("RGBA", (120, 120), ink + (0,))
    colored.putalpha(glyph)
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    overlay.paste(colored, (text_x - 20, text_y - 20), colored)
    return Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")


def _main_image_xref(page: pymupdf.Page) -> int:
    images = page.get_images(full=True)
    if not images:
        raise RuntimeError(f"No images on page {page.number}")
    return max(images, key=lambda info: info[2] * info[3])[0]


def replace_dates(source: Path = SOURCE_PDF, output: Path = OUTPUT_PDF) -> Path:
    if not TINOS_REGULAR.exists() or not TINOS_BOLD.exists():
        raise RuntimeError("Tinos fonts are required (ttf-mscorefonts / fonts-croscore)")

    doc = pymupdf.open(source)
    pages: list[Image.Image] = []

    for page in doc:
        xref = _main_image_xref(page)
        extracted = doc.extract_image(xref)
        image = Image.open(BytesIO(extracted["image"])).convert("RGB")
        pages.append(image)

    for edit in DATE_EDITS:
        image = pages[edit["page"]]
        x, y, w, h = edit["box"]
        ink, paper = _sample_ink_and_paper(image, x, y, w, h)
        erased = _erase_digit(image, x, y, w, h, edit["pad"], paper)
        ox, oy = edit["origin"]
        pages[edit["page"]] = _draw_seven(
            erased,
            ox,
            oy,
            edit["font_size"],
            ink,
            bold=edit["bold"],
        )

    tmp_dir = ROOT / ".tmp_page_images"
    tmp_dir.mkdir(exist_ok=True)
    new_doc = pymupdf.open()
    try:
        page_rect = doc[0].rect
        overlay = None
        overlay_rect = None
        for info in doc[0].get_images(full=True):
            if info[2] < 1000:
                overlay = doc.extract_image(info[0])["image"]
                rects = doc[0].get_image_rects(info[0])
                overlay_rect = rects[0] if rects else None
                break

        for index, image in enumerate(pages):
            jpg_path = tmp_dir / f"page_{index + 1}.jpg"
            image.save(jpg_path, format="JPEG", quality=95, subsampling=0, optimize=True)
            page = new_doc.new_page(width=page_rect.width, height=page_rect.height)
            page.insert_image(page_rect, filename=jpg_path)
            if index == 0 and overlay and overlay_rect is not None:
                stamp_path = tmp_dir / "stamp.jpg"
                stamp_path.write_bytes(overlay)
                page.insert_image(overlay_rect, filename=stamp_path)

        new_doc.save(output, deflate=True, garbage=4)
    finally:
        new_doc.close()
        doc.close()
        for leftover in tmp_dir.glob("*"):
            leftover.unlink()
        tmp_dir.rmdir()

    return output


if __name__ == "__main__":
    path = replace_dates()
    print(f"Wrote {path}")
