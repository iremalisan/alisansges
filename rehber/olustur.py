#!/usr/bin/env python3
"""Tüm hızlı manifest çıktılarını üretir."""

from __future__ import annotations

from pathlib import Path

from olustur_defter import build as build_defter
from olustur_gorsel import build as build_gorsel
from olustur_sunum import build as build_sunum
from olustur_takip import build as build_takip

ROOT = Path(__file__).resolve().parent


def main() -> None:
    pptx = build_sunum()
    pdf, pngs = build_gorsel()
    docx = build_defter()
    xlsx = build_takip()
    print(f"PPTX  {pptx}  ({pptx.stat().st_size} byte)")
    print(f"PDF   {pdf}  ({pdf.stat().st_size} byte)")
    print(f"DOCX  {docx}  ({docx.stat().st_size} byte)")
    print(f"XLSX  {xlsx}  ({xlsx.stat().st_size} byte)")
    print(f"PNG   {len(pngs)} slayt")


if __name__ == "__main__":
    main()
