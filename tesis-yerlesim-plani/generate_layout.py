#!/usr/bin/env python3
"""Generate draw.io XML and PDF for the facility site plan."""

from __future__ import annotations

import html
from pathlib import Path

from reportlab.lib.colors import Color, black, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as pdfcanvas

ROOT = Path(__file__).resolve().parent
DRAWIO_PATH = ROOT / "tesis-yerlesim-plani.drawio"
PDF_PATH = ROOT / "tesis-yerlesim-plani.pdf"

pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(
    TTFont("DejaVuBold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
)

PAGE_W = 1600
PAGE_H = 1280

STROKE = "#000000"
FILL = "#ffffff"
BLUE = "#5B9BD5"
YELLOW = "#E8B84A"
FONT = "Arial"

# Shared layout: id, label, x, y, w, h, font_size, vertical, is_html
BOXES = [
    ("site", "", 50, 36, 1504, 1140, 12, False, False),
    ("jenerator", "Jeneratör", 168, 52, 132, 68, 13, False, False),
    ("fosseptik", "Fosseptik", 320, 52, 140, 68, 13, False, False),
    ("aritma", "Arıtma Tesisi", 480, 52, 188, 68, 13, False, False),
    ("desarj", "Deşarj", 688, 52, 84, 52, 12, False, False),
    ("mumlama", "3 Adet Mumlama Odası", 1060, 52, 470, 168, 16, False, False),
    ("yemekhane", "Yemekhane - Lojmanlar", 140, 140, 680, 80, 14, False, False),
    ("fileleme", "2 Adet<br>Fileleme", 140, 220, 160, 96, 13, False, True),
    (
        "yikama",
        "Narenciye Yıkama Kurutma Boylama Hattı",
        300,
        220,
        540,
        96,
        13,
        False,
        False,
    ),
    ("makinaci", "Makina-cı", 140, 316, 160, 52, 12, False, False),
    (
        "paket80",
        "80 Kişilik Narenciye Paketleme Hattı",
        300,
        316,
        540,
        232,
        15,
        False,
        False,
    ),
    (
        "biber",
        "Biber, Domates,<br>Sebze, Salatalık<br>Paketleme Hattı",
        140,
        368,
        160,
        180,
        12,
        False,
        True,
    ),
    (
        "hammadde",
        "Hammadde<br>Kabul Stok Alanı",
        840,
        220,
        220,
        428,
        14,
        False,
        True,
    ),
    (
        "soguk",
        "5 Adet Soğuk Hava Deposu",
        1060,
        220,
        470,
        444,
        16,
        False,
        False,
    ),
    ("sevkiyat", "Sevkiyat Alanı", 140, 548, 500, 100, 15, False, False),
    ("idari", "İdari Bina", 640, 548, 200, 232, 15, False, False),
    (
        "atik",
        "Atık Geçici Depolama Alanı",
        56,
        780,
        96,
        200,
        12,
        True,
        False,
    ),
    ("dranger", "Dranger", 1060, 688, 220, 60, 14, False, False),
    (
        "kasa",
        "Kasa Yıkama Alanı",
        1310,
        688,
        220,
        120,
        12,
        True,
        False,
    ),
    (
        "palet",
        "Palet Onarım Alanı",
        1310,
        808,
        220,
        160,
        12,
        True,
        False,
    ),
    (
        "boskasa",
        "Boş Kasa, Yaprak Depolama Alanı",
        1310,
        968,
        220,
        184,
        12,
        True,
        False,
    ),
    ("ofis", "Ofis", 250, 1008, 156, 132, 14, False, False),
    ("guvenlik", "Güvenlik - Danışma", 430, 1008, 220, 132, 13, False, False),
    ("kantar", "Kantar", 1000, 1056, 280, 96, 15, False, False),
]

# Parking bay vertical lines (x, y0, y1)
PARKING = [
    (188, 648, 780),
    (268, 648, 780),
    (348, 648, 780),
    (428, 648, 780),
    (508, 648, 780),
    (588, 648, 780),
    (880, 648, 760),
    (960, 648, 760),
]

DOTS = [
    (780, 180, 10, BLUE),
    (360, 268, 9, YELLOW),
    (456, 300, 8, YELLOW),
    (792, 268, 10, BLUE),
    (1236, 718, 10, BLUE),
    (1420, 728, 9, BLUE),
    (1464, 768, 9, BLUE),
]

# Up-pointing arrow in top-left geometry space
ARROW = {
    "cx": 820,
    "top": 840,
    "bottom": 1120,
    "head_h": 88,
    "head_w": 132,
    "shaft_w": 72,
}

LEGEND = [
    (56, 1194, BLUE, "Atıksu"),
    (56, 1230, YELLOW, "Emisyon"),
]


def xml_text(value: str, is_html: bool = False) -> str:
    parts = value.split("<br>")
    return "&#xa;".join(html.escape(part, quote=True) for part in parts)


def box_style(vertical: bool, font_size: int) -> str:
    base = (
        f"rounded=0;whiteSpace=wrap;html=1;fillColor={FILL};strokeColor={STROKE};"
        f"strokeWidth=1.5;fontFamily={FONT};fontSize={font_size};fontColor=#000000;"
        "align=center;verticalAlign=middle;fontStyle=0;editable=1;locked=0;"
    )
    if vertical:
        base += "horizontal=0;"
    return base


def arrow_bounds() -> tuple[float, float, float, float]:
    cx = ARROW["cx"]
    top = ARROW["top"]
    bottom = ARROW["bottom"]
    hw = ARROW["head_w"]
    return cx - hw / 2, top, hw, bottom - top


def build_drawio() -> str:
    cells: list[str] = []

    def add(cell: str) -> None:
        cells.append(cell)

    for box_id, label, x, y, w, h, font_size, vertical, is_html in BOXES:
        if box_id == "site":
            style = (
                f"rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor={STROKE};"
                "strokeWidth=2;"
            )
            value = ""
        else:
            style = box_style(vertical, font_size)
            value = xml_text(label, is_html)
        add(
            f'        <mxCell id="{box_id}" value="{value}" style="{style}" '
            f'vertex="1" parent="1">\n'
            f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>\n'
            f"        </mxCell>"
        )

    for i, (x, y0, y1) in enumerate(PARKING, start=1):
        add(
            f'        <mxCell id="park-{i}" value="" '
            f'style="endArrow=none;html=1;strokeWidth=1.5;strokeColor={STROKE};" '
            f'edge="1" parent="1">\n'
            f'          <mxGeometry relative="1" as="geometry">\n'
            f'            <mxPoint x="{x}" y="{y0}" as="sourcePoint"/>\n'
            f'            <mxPoint x="{x}" y="{y1}" as="targetPoint"/>\n'
            f"          </mxGeometry>\n"
            f"        </mxCell>"
        )

    ax, ay, aw, ah = arrow_bounds()
    head_h = ARROW["head_h"]
    shaft_w = ARROW["shaft_w"]
    shaft_x = (aw - shaft_w) / 2
    add(
        f'        <mxCell id="giris" value="" style="group;rotatable=1;" vertex="1" '
        f'connectable="0" parent="1">\n'
        f'          <mxGeometry x="{ax}" y="{ay}" width="{aw}" height="{ah}" as="geometry"/>\n'
        f"        </mxCell>"
    )
    add(
        f'        <mxCell id="giris-head" value="" '
        f'style="shape=triangle;direction=north;fillColor={FILL};strokeColor={STROKE};'
        f'strokeWidth=1.5;" vertex="1" parent="giris">\n'
        f'          <mxGeometry x="0" y="0" width="{aw}" height="{head_h}" as="geometry"/>\n'
        f"        </mxCell>"
    )
    add(
        f'        <mxCell id="giris-shaft" value="" '
        f'style="rounded=0;fillColor={FILL};strokeColor={STROKE};strokeWidth=1.5;" '
        f'vertex="1" parent="giris">\n'
        f'          <mxGeometry x="{shaft_x}" y="{head_h - 1}" width="{shaft_w}" '
        f'height="{ah - head_h + 1}" as="geometry"/>\n'
        f"        </mxCell>"
    )
    add(
        f'        <mxCell id="giris-label" value="GİRİŞ" '
        f'style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;'
        f'fontFamily={FONT};fontSize=16;fontStyle=1;horizontal=0;" vertex="1" parent="giris">\n'
        f'          <mxGeometry x="{shaft_x}" y="{head_h + 24}" width="{shaft_w}" '
        f'height="{ah - head_h - 40}" as="geometry"/>\n'
        f"        </mxCell>"
    )

    for i, (x, y, r, color) in enumerate(DOTS, start=1):
        add(
            f'        <mxCell id="dot-{i}" value="" '
            f'style="ellipse;html=1;aspect=fixed;fillColor={color};strokeColor=none;" '
            f'vertex="1" parent="1">\n'
            f'          <mxGeometry x="{x - r}" y="{y - r}" width="{r * 2}" height="{r * 2}" as="geometry"/>\n'
            f"        </mxCell>"
        )

    for i, (x, y, color, label) in enumerate(LEGEND, start=1):
        add(
            f'        <mxCell id="legend-dot-{i}" value="" '
            f'style="ellipse;html=1;aspect=fixed;fillColor={color};strokeColor=none;" '
            f'vertex="1" parent="1">\n'
            f'          <mxGeometry x="{x}" y="{y}" width="18" height="18" as="geometry"/>\n'
            f"        </mxCell>"
        )
        add(
            f'        <mxCell id="legend-label-{i}" value="{html.escape(label)}" '
            f'style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;'
            f'fontFamily={FONT};fontSize=13;" vertex="1" parent="1">\n'
            f'          <mxGeometry x="{x + 28}" y="{y - 2}" width="90" height="22" as="geometry"/>\n'
            f"        </mxCell>"
        )

    body = "\n".join(cells)
    return f"""<mxfile host="Electron" agent="draw.io" version="24.7.17" type="device">
  <diagram id="tesis-yerlesim" name="Tesis Yerleşim Planı">
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
    v = value.lstrip("#")
    r, g, b = int(v[0:2], 16), int(v[2:4], 16), int(v[4:6], 16)
    return Color(r / 255, g / 255, b / 255)


def wrap_text(c: pdfcanvas.Canvas, text: str, font: str, size: float, max_width: float) -> list[str]:
    text = text.replace("<br>", "\n")
    paragraphs = text.split("\n")
    lines: list[str] = []
    for para in paragraphs:
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


def draw_box_pdf(
    c: pdfcanvas.Canvas,
    label: str,
    x: float,
    y: float,
    w: float,
    h: float,
    font_size: int,
    vertical: bool,
    fill: bool = True,
) -> None:
    py = PAGE_H - y - h
    c.setStrokeColor(black)
    c.setLineWidth(1.4 if fill else 2.0)
    if fill:
        c.setFillColor(white)
        c.rect(x, py, w, h, stroke=1, fill=1)
    else:
        c.setFillColor(white)
        c.rect(x, py, w, h, stroke=1, fill=0)

    if not label:
        return

    c.setFillColor(black)
    font = "DejaVu"
    pad = 8
    if vertical:
        c.saveState()
        cx, cy = x + w / 2, py + h / 2
        c.translate(cx, cy)
        c.rotate(90)
        max_w = h - pad * 2
        lines = wrap_text(c, label, font, font_size, max_w)
        line_h = font_size + 3
        total = line_h * len(lines)
        ty = total / 2 - font_size
        c.setFont(font, font_size)
        for line in lines:
            tw = c.stringWidth(line, font, font_size)
            c.drawString(-tw / 2, ty, line)
            ty -= line_h
        c.restoreState()
        return

    max_w = w - pad * 2
    lines = wrap_text(c, label, font, font_size, max_w)
    line_h = font_size + 4
    total = line_h * len(lines)
    ty = py + h / 2 + total / 2 - font_size
    c.setFont(font, font_size)
    for line in lines:
        tw = c.stringWidth(line, font, font_size)
        c.drawString(x + w / 2 - tw / 2, ty, line)
        ty -= line_h


def draw_arrow_pdf(c: pdfcanvas.Canvas) -> None:
    cx = ARROW["cx"]
    top = PAGE_H - ARROW["top"]
    bottom = PAGE_H - ARROW["bottom"]
    head_h = ARROW["head_h"]
    head_w = ARROW["head_w"]
    shaft_w = ARROW["shaft_w"]
    head_bottom = top - head_h
    shaft_left = cx - shaft_w / 2
    shaft_right = cx + shaft_w / 2

    path = c.beginPath()
    path.moveTo(cx, top)
    path.lineTo(cx - head_w / 2, head_bottom)
    path.lineTo(shaft_left, head_bottom)
    path.lineTo(shaft_left, bottom)
    path.lineTo(shaft_right, bottom)
    path.lineTo(shaft_right, head_bottom)
    path.lineTo(cx + head_w / 2, head_bottom)
    path.close()
    c.setStrokeColor(black)
    c.setFillColor(white)
    c.setLineWidth(1.5)
    c.drawPath(path, stroke=1, fill=1)

    c.setFillColor(black)
    c.setFont("DejaVuBold", 15)
    c.saveState()
    label_y = (head_bottom + bottom) / 2
    c.translate(cx, label_y)
    c.rotate(90)
    label = "GİRİŞ"
    tw = c.stringWidth(label, "DejaVuBold", 15)
    c.drawString(-tw / 2, -5, label)
    c.restoreState()


def build_pdf() -> None:
    c = pdfcanvas.Canvas(str(PDF_PATH), pagesize=(PAGE_W, PAGE_H))
    c.setTitle("Tesis Yerleşim Planı")
    c.setAuthor("Tesis Yerleşim")

    for box_id, label, x, y, w, h, font_size, vertical, _is_html in BOXES:
        draw_box_pdf(
            c,
            label.replace("<br>", "\n") if label else "",
            x,
            y,
            w,
            h,
            font_size,
            vertical,
            fill=(box_id != "site"),
        )

    c.setStrokeColor(black)
    c.setLineWidth(1.5)
    for x, y0, y1 in PARKING:
        c.line(x, PAGE_H - y0, x, PAGE_H - y1)

    draw_arrow_pdf(c)

    for x, y, r, color in DOTS:
        c.setFillColor(hex_color(color))
        c.circle(x, PAGE_H - y, r, stroke=0, fill=1)

    for x, y, color, label in LEGEND:
        c.setFillColor(hex_color(color))
        c.circle(x + 9, PAGE_H - y - 9, 8, stroke=0, fill=1)
        c.setFillColor(black)
        c.setFont("DejaVu", 13)
        c.drawString(x + 28, PAGE_H - y - 14, label)

    c.showPage()
    c.save()


def main() -> None:
    DRAWIO_PATH.write_text(build_drawio(), encoding="utf-8")
    build_pdf()
    print(f"Wrote {DRAWIO_PATH}")
    print(f"Wrote {PDF_PATH}")


if __name__ == "__main__":
    main()
