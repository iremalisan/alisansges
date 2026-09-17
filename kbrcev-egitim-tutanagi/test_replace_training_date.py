#!/usr/bin/env python3
"""Checks that 01.09.2026 was replaced with 07.09.2026 on the attendance form."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

import numpy as np
import pymupdf
from PIL import Image

ROOT = Path(__file__).resolve().parent
SOURCE_PDF = ROOT / "CCF17092026_Egitime_Katilim_Tutanagi_orijinal.pdf"
OUTPUT_PDF = ROOT / "CCF17092026_Egitime_Katilim_Tutanagi_07.09.2026.pdf"

# Tight crops around each date on the 2409x3437 page images.
DATE_CROPS = (
    (0, (1000, 348, 1180, 390)),
    (0, (480, 2604, 670, 2642)),
    (0, (1655, 2644, 1855, 2684)),
    (1, (1465, 2298, 1680, 2342)),
)

# Unchanged control crop (gazette date 01/11/2022 on page 2).
CONTROL_CROP = (1, (180, 160, 900, 280))


def _page_image(pdf_path: Path, page_index: int) -> Image.Image:
    doc = pymupdf.open(pdf_path)
    try:
        page = doc[page_index]
        xref = max(page.get_images(full=True), key=lambda info: info[2] * info[3])[0]
        extracted = doc.extract_image(xref)
        return Image.open(BytesIO(extracted["image"])).convert("RGB")
    finally:
        doc.close()


def _crop(image: Image.Image, box: tuple[int, int, int, int]) -> np.ndarray:
    return np.array(image.crop(box), dtype=np.int16)


def test_output_pdf_exists_and_has_two_pages() -> None:
    assert OUTPUT_PDF.exists(), f"Missing {OUTPUT_PDF.name} — run replace_training_date.py"
    doc = pymupdf.open(OUTPUT_PDF)
    try:
        assert doc.page_count == 2
        assert doc[0].rect.width > 500
        assert doc[1].rect.height > 800
    finally:
        doc.close()


def test_date_regions_changed() -> None:
    originals = [_page_image(SOURCE_PDF, 0), _page_image(SOURCE_PDF, 1)]
    updated = [_page_image(OUTPUT_PDF, 0), _page_image(OUTPUT_PDF, 1)]
    for page_index, box in DATE_CROPS:
        before = _crop(originals[page_index], box)
        after = _crop(updated[page_index], box)
        delta = np.abs(after - before).mean()
        assert delta > 4, f"Date crop {box} did not change enough (delta={delta:.2f})"


def test_unrelated_header_stayed_the_same() -> None:
    page_index, box = CONTROL_CROP
    before = _crop(_page_image(SOURCE_PDF, page_index), box)
    after = _crop(_page_image(OUTPUT_PDF, page_index), box)
    delta = np.abs(after - before).mean()
    assert delta < 8, f"Unrelated header changed too much (delta={delta:.2f})"


if __name__ == "__main__":
    test_output_pdf_exists_and_has_two_pages()
    test_date_regions_changed()
    test_unrelated_header_stayed_the_same()
    print("ok")
