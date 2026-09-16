#!/usr/bin/env python3
"""Generate draw.io XML and PDF for the Yılpack OG vaziyet planı."""

from __future__ import annotations

import html
from pathlib import Path

from reportlab.lib.colors import Color, black, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.colors import HexColor

ROOT = Path(__file__).resolve().parent
DRAWIO_PATH = ROOT / "og-vaziyet-plani.drawio"
PDF_PATH = ROOT / "og-vaziyet-plani.pdf"

pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(
    TTFont("DejaVuBold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
)

PAGE_W = 2100
PAGE_H = 1480
FONT = "Arial"
STROKE = "#000000"

# id, label, x, y, w, h, font_size, vertical, html, fill
BOXES = [
    ("site", "", 36, 56, 2028, 1336, 12, False, False, "none"),
    (
        "title",
        "YENİ FABRİKA BİNASI — OG Vaziyet Planı",
        36,
        12,
        900,
        36,
        18,
        False,
        False,
        "none",
    ),
    # Kuzey / mevcut tesis
    (
        "hammadde",
        "Hammadde ve<br>Stok Ambarı",
        56,
        72,
        260,
        250,
        13,
        False,
        True,
        "#ffffff",
    ),
    (
        "yardimci",
        "Yardımcı Eleman<br>ve Stok Alanı",
        316,
        72,
        200,
        250,
        12,
        False,
        True,
        "#ffffff",
    ),
    (
        "tekulpa",
        "Tek Kulp Dikim Atölyesi-1<br>(1600 adet/gün)",
        516,
        72,
        280,
        160,
        12,
        False,
        True,
        "#F5F5F5",
    ),
    (
        "tekulpb",
        "Tek Kulp Dikim Atölyesi-1<br>(1600 adet/gün)",
        796,
        72,
        280,
        160,
        12,
        False,
        True,
        "#F5F5F5",
    ),
    (
        "hazirlik",
        "Bigbag Hazırlık<br>Makineleri",
        1076,
        72,
        190,
        160,
        12,
        False,
        True,
        "#F5F5F5",
    ),
    (
        "upanel",
        "U-Panel Dikim Atölyesi-2<br>(750 adet/gün)",
        1266,
        72,
        230,
        160,
        12,
        False,
        True,
        "#F5F5F5",
    ),
    (
        "dikim",
        "Bigbag Dikim Atölyesi<br>HOL 1",
        1496,
        72,
        200,
        250,
        12,
        False,
        True,
        "#ffffff",
    ),
    ("hol2e", "HOL 2", 1696, 72, 140, 250, 13, False, False, "#ffffff"),
    ("hol3e", "HOL 3", 1836, 72, 140, 250, 13, False, False, "#ffffff"),
    (
        "konveyor",
        "Konveyör",
        1266,
        232,
        230,
        90,
        11,
        False,
        False,
        "#E6E6E6",
    ),
    (
        "baglanti",
        "İki Tesis Bağlantı Kapısı",
        1496,
        328,
        200,
        36,
        11,
        False,
        False,
        "#ffffff",
    ),
    # Yeni fabrika — HOL 2
    ("yeni", "", 56, 380, 1520, 640, 12, False, False, "none"),
    (
        "hol2",
        "HOL 2",
        1000,
        640,
        80,
        28,
        13,
        False,
        False,
        "none",
    ),
    (
        "extruder",
        "Extruder Makinesi",
        72,
        396,
        980,
        72,
        14,
        False,
        False,
        "#ffffff",
    ),
    (
        "uretim1",
        "Üretim Alanı",
        200,
        484,
        220,
        150,
        12,
        False,
        False,
        "#F0F0F0",
    ),
    (
        "uretim2",
        "Üretim Alanı",
        440,
        484,
        220,
        150,
        12,
        False,
        False,
        "#F0F0F0",
    ),
    (
        "uretim3",
        "Üretim Alanı",
        680,
        484,
        220,
        150,
        12,
        False,
        False,
        "#F0F0F0",
    ),
    (
        "lohia",
        "Lohia Dokuma Makinesi",
        920,
        484,
        280,
        150,
        13,
        False,
        False,
        "#ffffff",
    ),
    (
        "bigbagdokuma",
        "Bigbag Dokuma Makinesi",
        1216,
        396,
        340,
        238,
        14,
        False,
        False,
        "#ffffff",
    ),
    (
        "forklift1",
        "Forklift Geçiş Kapısı",
        72,
        644,
        200,
        32,
        10,
        False,
        False,
        "#ffffff",
    ),
    (
        "forklift2",
        "Forklift Geçiş Kapısı",
        1216,
        644,
        200,
        32,
        10,
        False,
        False,
        "#ffffff",
    ),
    # HOL 1
    (
        "hol1",
        "HOL 1",
        1280,
        770,
        80,
        28,
        13,
        False,
        False,
        "none",
    ),
    ("ffs", "FFS Makinesi", 72, 700, 280, 150, 13, False, False, "#ffffff"),
    ("balon1", "Balon-1", 72, 854, 130, 50, 11, False, False, "#ffffff"),
    ("balon2", "Balon-2", 212, 854, 140, 50, 11, False, False, "#ffffff"),
    (
        "baski",
        "Baskı Makinesi<br>3000 × 10500",
        368,
        700,
        260,
        204,
        13,
        False,
        True,
        "#ffffff",
    ),
    ("ic1", "İç Geçirme", 644, 700, 130, 204, 12, True, False, "#ffffff"),
    ("ic2", "İç Geçirme", 774, 700, 130, 204, 12, True, False, "#ffffff"),
    ("ic3", "İç Geçirme", 904, 700, 130, 204, 12, True, False, "#ffffff"),
    ("ic4", "İç Geçirme", 1034, 700, 130, 204, 12, True, False, "#ffffff"),
    ("hol1acik", "HOL 1 üretim alanı", 1180, 700, 376, 204, 12, False, False, "#ffffff"),
    # Ofis şeridi
    ("komp", "Kompresör Odası", 72, 920, 160, 80, 11, False, False, "#ffffff"),
    (
        "yedek",
        "Yedek Parça Ambarı",
        232,
        920,
        170,
        80,
        11,
        False,
        False,
        "#ffffff",
    ),
    ("ofisler", "Ofis / WC", 402, 920, 280, 80, 11, False, False, "#ffffff"),
    ("boya", "Boya Deposu", 682, 920, 140, 80, 11, False, False, "#ffffff"),
    ("sorumlu", "Sorumlu Odası", 822, 920, 140, 80, 11, False, False, "#ffffff"),
    ("lab", "Laboratuvar", 962, 920, 140, 80, 11, False, False, "#ffffff"),
    (
        "sevkiyatodasi",
        "Sevkiyat / Mühendis<br>Sorumlu Odası",
        1102,
        920,
        200,
        80,
        11,
        False,
        True,
        "#ffffff",
    ),
    (
        "rampa",
        "Araç Sevkiyat Rampası",
        1302,
        920,
        254,
        80,
        11,
        False,
        False,
        "#ffffff",
    ),
    (
        "yenietiket",
        "YENİ FABRİKA BİNASI",
        56,
        1008,
        280,
        28,
        12,
        False,
        False,
        "none",
    ),
    ("arac1", "Araç Girişi", 1500, 700, 76, 90, 10, True, False, "#ffffff"),
    ("arac2", "Araç Girişi", 1500, 810, 76, 90, 10, True, False, "#ffffff"),
    # Güvenlik / OG
    (
        "guvenlik",
        "Güvenlik",
        1636,
        920,
        90,
        160,
        12,
        True,
        False,
        "#ffffff",
    ),
    (
        "oghucre",
        "OG Hücre Odası",
        1734,
        860,
        260,
        70,
        12,
        False,
        False,
        "#FFF2CC",
    ),
    (
        "trafo1",
        "31.5/0.4 kV<br>2000 kVA Trafo",
        1734,
        930,
        128,
        80,
        10,
        False,
        True,
        "#DAE8FC",
    ),
    (
        "trafo2",
        "31.5/0.4 kV<br>2000 kVA Trafo",
        1866,
        930,
        128,
        80,
        10,
        False,
        True,
        "#DAE8FC",
    ),
    # Yol
    ("yesil1", "Yeşil Alan", 56, 1100, 1520, 36, 11, False, False, "#D5E8D4"),
    ("duvar", "Duvar", 56, 1136, 1520, 22, 10, False, False, "#E6E6E6"),
    ("kaldirim", "Kaldırım", 56, 1158, 1520, 28, 11, False, False, "#F5F5F5"),
    ("yol", "Asfalt Yol", 56, 1186, 1520, 70, 14, False, False, "#D0D0D0"),
    (
        "yesil2",
        "Yeşil Alan",
        1576,
        1100,
        200,
        156,
        11,
        True,
        False,
        "#D5E8D4",
    ),
    (
        "kabloog",
        "OG  3×(1×95/16) mm²",
        1788,
        1100,
        36,
        156,
        10,
        True,
        False,
        "none",
    ),
    # Menholler
    ("me1", "ME", 56, 340, 40, 28, 10, False, False, "#E1F5FE"),
    ("me2",  "ME", 316, 340, 40, 28, 10, False, False, "#E1F5FE"),
    ("me3", "ME", 1836, 340, 40, 28, 10, False, False, "#E1F5FE"),
    ("me4", "ME", 1640, 860, 40, 28, 10, False, False, "#E1F5FE"),
    ("me5", "ME", 1640, 1100, 40, 28, 10, False, False, "#E1F5FE"),
    ("me6", "ME", 1990, 1100, 40, 28, 10, False, False, "#E1F5FE"),
]

# x1,y1,x2,y2, color, width, dashed, label
LINES = [
    # Kablo tavası HOL 2 kuzey
    (72, 388, 1556, 388, "#D79B00", 4, False, ""),
    # Kablo tavası HOL 1/2 arası
    (72, 688, 1556, 688, "#D79B00", 4, False, ""),
    # Kablo tavası HOL 1 güney
    (72, 916, 1556, 916, "#D79B00", 4, False, ""),
    # Magenta özel güzergah HOL 1 doğu
    (1568, 396, 1568, 916, "#C2185B", 3, False, ""),
    (1568, 700, 1648, 860, "#C2185B", 3, False, ""),
    # AG yeşil trafo -> fabrika
    (1734, 930, 1568, 700, "#82B366", 4, False, "AG"),
    (1734, 860, 1648, 396, "#82B366", 3, False, "AG"),
    # OG yeşil duvar hattı
    (76, 354, 1870, 354, "#82B366", 2, False, ""),
    (1856, 354, 1998, 1114, "#82B366", 2, False, "OG"),
]

ARROW = {"cx": 1480, "top": 1190, "bottom": 1252, "head_h": 22, "head_w": 48, "shaft_w": 22}

LEGEND = [
    (40, 1408, "#D79B00", "Kablo tavası / busbar"),
    (280, 1408, "#82B366", "OG / AG enerji hattı"),
    (520, 1408, "#C2185B", "Özel kablo güzergahı"),
    (760, 1408, "#00ACC1", "ME  Enerji menholü"),
    (1000, 1408, "#FFF2CC", "OG hücre / trafo"),
]


def xml_text(value: str) -> str:
    return html.escape(value, quote=True)


def box_style(vertical: bool, font_size: int, fill: str) -> str:
    fill_css = "none" if fill == "none" else fill
    stroke = "none" if fill == "none" and not vertical else STROKE
    # title has no stroke
    base = (
        f"rounded=0;whiteSpace=wrap;html=1;fillColor={fill_css};strokeColor={stroke};"
        f"strokeWidth=1.4;fontFamily={FONT};fontSize={font_size};fontColor=#000000;"
        "align=center;verticalAlign=middle;"
    )
    if vertical:
        base += "horizontal=0;"
    return base


def build_drawio() -> str:
    cells: list[str] = []

    def add(s: str) -> None:
        cells.append(s)

    for box_id, label, x, y, w, h, font_size, vertical, is_html, fill in BOXES:
        if box_id == "title":
            style = (
                f"text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;"
                f"fontFamily={FONT};fontSize={font_size};fontStyle=1;"
            )
        elif box_id in {"site", "yeni"}:
            style = (
                f"rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor={STROKE};"
                "strokeWidth=2;"
            )
        elif box_id in {"hol1", "hol2", "yenietiket", "kabloog"}:
            style = (
                f"text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;"
                f"fontFamily={FONT};fontSize={font_size};fontStyle=1;"
            )
            if vertical:
                style += "horizontal=0;"
        else:
            style = box_style(vertical, font_size, fill)
        value = xml_text(label)
        add(
            f'        <mxCell id="{box_id}" value="{value}" style="{style}" '
            f'vertex="1" parent="1">\n'
            f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>\n'
            f"        </mxCell>"
        )

    for i, (x1, y1, x2, y2, color, width, _dashed, label) in enumerate(LINES, start=1):
        dash = "dashed=1;dashPattern=8 6;" if _dashed else ""
        add(
            f'        <mxCell id="line-{i}" value="{xml_text(label)}" '
            f'style="endArrow=none;html=1;strokeWidth={width};strokeColor={color};'
            f'{dash}fontSize=10;fontColor={color};" '
            f'edge="1" parent="1">\n'
            f'          <mxGeometry relative="1" as="geometry">\n'
            f'            <mxPoint x="{x1}" y="{y1}" as="sourcePoint"/>\n'
            f'            <mxPoint x="{x2}" y="{y2}" as="targetPoint"/>\n'
            f"          </mxGeometry>\n"
            f"        </mxCell>"
        )

    ax = ARROW["cx"] - ARROW["head_w"] / 2
    ay = ARROW["top"]
    aw = ARROW["head_w"]
    ah = ARROW["bottom"] - ARROW["top"]
    add(
        f'        <mxCell id="giris" value="" style="group" vertex="1" connectable="0" parent="1">\n'
        f'          <mxGeometry x="{ax}" y="{ay}" width="{aw}" height="{ah}" as="geometry"/>\n'
        f"        </mxCell>"
    )
    add(
        f'        <mxCell id="giris-head" value="" style="shape=triangle;direction=south;'
        f'fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.4;" vertex="1" parent="giris">\n'
        f'          <mxGeometry x="0" y="{ah - ARROW["head_h"]}" width="{aw}" height="{ARROW["head_h"]}" as="geometry"/>\n'
        f"        </mxCell>"
    )
    shaft_x = (aw - ARROW["shaft_w"]) / 2
    add(
        f'        <mxCell id="giris-shaft" value="" style="rounded=0;fillColor=#ffffff;'
        f'strokeColor=#000000;strokeWidth=1.4;" vertex="1" parent="giris">\n'
        f'          <mxGeometry x="{shaft_x}" y="0" width="{ARROW["shaft_w"]}" '
        f'height="{ah - ARROW["head_h"] + 1}" as="geometry"/>\n'
        f"        </mxCell>"
    )
    add(
        f'        <mxCell id="giris-label" value="GİRİŞ" style="text;html=1;strokeColor=none;'
        f'fillColor=none;align=center;verticalAlign=middle;fontFamily={FONT};fontSize=12;fontStyle=1;" '
        f'vertex="1" parent="1">\n'
        f'          <mxGeometry x="{ax + aw + 8}" y="{ay}" width="70" height="{ah}" as="geometry"/>\n'
        f"        </mxCell>"
    )

    for i, (x, y, color, label) in enumerate(LEGEND, start=1):
        add(
            f'        <mxCell id="leg-swatch-{i}" value="" style="rounded=0;fillColor={color};'
            f'strokeColor=#000000;strokeWidth=1;" vertex="1" parent="1">\n'
            f'          <mxGeometry x="{x}" y="{y}" width="18" height="14" as="geometry"/>\n'
            f"        </mxCell>"
        )
        add(
            f'        <mxCell id="leg-label-{i}" value="{xml_text(label)}" style="text;html=1;'
            f'strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontFamily={FONT};'
            f'fontSize=11;" vertex="1" parent="1">\n'
            f'          <mxGeometry x="{x + 24}" y="{y - 4}" width="220" height="22" as="geometry"/>\n'
            f"        </mxCell>"
        )

    body = "\n".join(cells)
    return f"""<mxfile host="Electron" agent="draw.io" version="24.7.17" type="device">
  <diagram id="og-vaziyet" name="OG Vaziyet Planı">
    <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{PAGE_W}" pageHeight="{PAGE_H}" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
{body}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""


def hex_color(value: str) -> Color:
    if value in {"none", ""}:
        return white
    return HexColor(value)


def wrap_text(c: pdfcanvas.Canvas, text: str, font: str, size: float, max_width: float) -> list[str]:
    text = text.replace("<br>", "\n")
    lines: list[str] = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = f"{current} {word}"
            if c.stringWidth(trial, font, size) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def draw_box_pdf(c, label, x, y, w, h, font_size, vertical, fill, stroke=True, bold=False):
    py = PAGE_H - y - h
    c.setLineWidth(1.4 if stroke else 0)
    if fill == "none":
        if stroke:
            c.setStrokeColor(black)
            c.rect(x, py, w, h, stroke=1, fill=0)
    else:
        c.setFillColor(hex_color(fill))
        c.setStrokeColor(black)
        c.rect(x, py, w, h, stroke=1 if stroke else 0, fill=1)
    if not label:
        return
    font = "DejaVuBold" if bold else "DejaVu"
    c.setFillColor(black)
    pad = 6
    if vertical:
        c.saveState()
        c.translate(x + w / 2, py + h / 2)
        c.rotate(90)
        lines = wrap_text(c, label, font, font_size, h - pad * 2)
        line_h = font_size + 3
        ty = line_h * len(lines) / 2 - font_size
        c.setFont(font, font_size)
        for line in lines:
            tw = c.stringWidth(line, font, font_size)
            c.drawString(-tw / 2, ty, line)
            ty -= line_h
        c.restoreState()
        return
    lines = wrap_text(c, label, font, font_size, w - pad * 2)
    line_h = font_size + 3
    ty = py + h / 2 + line_h * len(lines) / 2 - font_size
    c.setFont(font, font_size)
    for line in lines:
        tw = c.stringWidth(line, font, font_size)
        c.drawString(x + w / 2 - tw / 2, ty, line)
        ty -= line_h


def build_pdf() -> None:
    c = pdfcanvas.Canvas(str(PDF_PATH), pagesize=(PAGE_W, PAGE_H))
    c.setTitle("Yeni Fabrika Binası — OG Vaziyet Planı")

    for box_id, label, x, y, w, h, font_size, vertical, _html, fill in BOXES:
        stroke = box_id not in {"title", "hol1", "hol2", "yenietiket", "kabloog"}
        bold = box_id in {"title", "hol1", "hol2", "yenietiket"}
        if box_id == "title":
            c.setFillColor(black)
            c.setFont("DejaVuBold", font_size)
            c.drawString(x, PAGE_H - y - 28, label)
            continue
        draw_box_pdf(
            c,
            label.replace("<br>", "\n") if label else "",
            x,
            y,
            w,
            h,
            font_size,
            vertical,
            fill,
            stroke=stroke,
            bold=bold,
        )

    for x1, y1, x2, y2, color, width, dashed, label in LINES:
        c.setStrokeColor(hex_color(color))
        c.setLineWidth(width)
        if dashed:
            c.setDash(8, 6)
        else:
            c.setDash()
        c.line(x1, PAGE_H - y1, x2, PAGE_H - y2)
        c.setDash()
        if label:
            c.setFillColor(hex_color(color))
            c.setFont("DejaVuBold", 10)
            c.drawString((x1 + x2) / 2 + 6, PAGE_H - (y1 + y2) / 2, label)

    # GİRİŞ arrow pointing down into the road
    cx = ARROW["cx"]
    top = PAGE_H - ARROW["top"]
    bottom = PAGE_H - ARROW["bottom"]
    head_h = ARROW["head_h"]
    head_w = ARROW["head_w"]
    shaft_w = ARROW["shaft_w"]
    head_top = bottom + head_h
    path = c.beginPath()
    path.moveTo(cx, bottom)
    path.lineTo(cx - head_w / 2, head_top)
    path.lineTo(cx - shaft_w / 2, head_top)
    path.lineTo(cx - shaft_w / 2, top)
    path.lineTo(cx + shaft_w / 2, top)
    path.lineTo(cx + shaft_w / 2, head_top)
    path.lineTo(cx + head_w / 2, head_top)
    path.close()
    c.setStrokeColor(black)
    c.setFillColor(white)
    c.setLineWidth(1.4)
    c.drawPath(path, stroke=1, fill=1)
    c.setFillColor(black)
    c.setFont("DejaVuBold", 12)
    c.drawString(cx + 28, (top + bottom) / 2 - 4, "GİRİŞ")

    for x, y, color, label in LEGEND:
        c.setFillColor(hex_color(color))
        c.setStrokeColor(black)
        c.setLineWidth(1)
        c.rect(x, PAGE_H - y - 14, 18, 14, stroke=1, fill=1)
        c.setFillColor(black)
        c.setFont("DejaVu", 11)
        c.drawString(x + 24, PAGE_H - y - 12, label)

    c.showPage()
    c.save()


def main() -> None:
    DRAWIO_PATH.write_text(build_drawio(), encoding="utf-8")
    build_pdf()
    print(f"Wrote {DRAWIO_PATH}")
    print(f"Wrote {PDF_PATH}")


if __name__ == "__main__":
    main()
