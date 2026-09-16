#!/usr/bin/env python3
"""Generate editable draw.io XML and PDF for the fertilizer site plan."""

from __future__ import annotations

import html
import math
from pathlib import Path

from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as pdfcanvas

ROOT = Path(__file__).resolve().parent
DRAWIO_PATH = ROOT / "gubre-uretimi-vaziyet-plani.drawio"
PDF_PATH = ROOT / "gubre-uretimi-vaziyet-plani.pdf"

pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(
    TTFont("DejaVuBold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
)

PAGE_W = 1700
PAGE_H = 1050
FONT = "Arial"
BLUE = "#5B8FC7"
RED = "#C00000"
CONVEYOR = "#8B1A1A"

# id, label, x, y, w, h, font_size, fill, stroke, shape, font_color, rounded, vertical
SHAPES = [
    ("site", "", 40, 36, 1620, 920, 12, "none", "#000000", "rect", "#000000", 0, False),
    (
        "giris-kapi",
        "",
        40,
        56,
        14,
        90,
        11,
        "#ffffff",
        "#000000",
        "rect",
        "#000000",
        0,
        False,
    ),
    (
        "giris",
        "GİRİŞ",
        8,
        70,
        30,
        70,
        12,
        "none",
        "none",
        "text",
        "#000000",
        0,
        True,
    ),
    (
        "idari",
        "İDARİ BÜRO",
        90,
        200,
        280,
        260,
        16,
        "#ffffff",
        "#000000",
        "rect",
        "#000000",
        1,
        False,
    ),
    (
        "sivi",
        "",
        90,
        500,
        400,
        250,
        14,
        "#ffffff",
        "#000000",
        "rect",
        "#000000",
        0,
        False,
    ),
    (
        "sivi-title",
        "SIVI GÜBRE ÜRETİM VE PAKETLEME",
        100,
        510,
        380,
        44,
        13,
        "none",
        "none",
        "text",
        "#000000",
        0,
        False,
    ),
    (
        "karistirici-label",
        "Karıştırıcılı Üretim Tankı",
        130,
        560,
        220,
        36,
        12,
        "none",
        "none",
        "text",
        RED,
        0,
        False,
    ),
    ("tank1", "", 120, 640, 52, 52, 11, BLUE, "#1F4E79", "roundRect", "#000000", 1, False),
    ("tank2", "", 184, 640, 52, 52, 11, BLUE, "#1F4E79", "roundRect", "#000000", 1, False),
    ("tank3", "", 248, 640, 52, 52, 11, BLUE, "#1F4E79", "roundRect", "#000000", 1, False),
    ("tank4", "", 312, 640, 52, 52, 11, BLUE, "#1F4E79", "roundRect", "#000000", 1, False),
    ("tank5", "", 376, 640, 52, 52, 11, BLUE, "#1F4E79", "roundRect", "#000000", 1, False),
    (
        "hammadde-label",
        "Hammadde Stok Tankı",
        150,
        790,
        180,
        50,
        12,
        "#ffffff",
        "#000000",
        "rect",
        RED,
        0,
        False,
    ),
    (
        "dinlendirme",
        "",
        500,
        560,
        56,
        110,
        11,
        BLUE,
        "#1F4E79",
        "cylinder",
        "#000000",
        0,
        False,
    ),
    (
        "dinlendirme-label",
        "Sıvı Gübre Dinlendirme Tankı",
        430,
        790,
        170,
        70,
        12,
        "#ffffff",
        "#000000",
        "rect",
        RED,
        0,
        False,
    ),
    (
        "sevk",
        "MAMÜL MALLAR SEVK BÖLÜMÜ",
        530,
        64,
        280,
        70,
        14,
        "none",
        "none",
        "text",
        "#000000",
        0,
        False,
    ),
    (
        "bunker",
        "",
        540,
        150,
        100,
        110,
        11,
        BLUE,
        "#1F4E79",
        "hopper",
        "#000000",
        0,
        False,
    ),
    (
        "bunker-label",
        "Paketleme Bunkeri",
        650,
        180,
        170,
        40,
        12,
        "#ffffff",
        "#000000",
        "rect",
        RED,
        0,
        False,
    ),
    ("elek", "", 555, 290, 70, 70, 11, BLUE, "#1F4E79", "rect", "#000000", 0, False),
    (
        "elek-label",
        "Elek",
        640,
        305,
        70,
        40,
        12,
        "#ffffff",
        "#000000",
        "rect",
        RED,
        0,
        False,
    ),
    ("firin", "", 562, 400, 50, 200, 11, BLUE, "#1F4E79", "cylinder", "#000000", 0, False),
    (
        "firin-label",
        "Fırın",
        618,
        470,
        56,
        50,
        12,
        "#ffffff",
        "#000000",
        "rect",
        RED,
        0,
        False,
    ),
    (
        "gran-label",
        "Granülatör Mikseri",
        700,
        500,
        180,
        40,
        12,
        "#ffffff",
        "#000000",
        "rect",
        RED,
        0,
        False,
    ),
    ("hex1", "", 690, 560, 78, 78, 11, BLUE, "#1F4E79", "hexagon", "#000000", 0, False),
    ("hex2", "", 778, 560, 78, 78, 11, BLUE, "#1F4E79", "hexagon", "#000000", 0, False),
    ("hex3", "", 866, 560, 78, 78, 11, BLUE, "#1F4E79", "hexagon", "#000000", 0, False),
    ("hex4", "", 954, 560, 78, 78, 11, BLUE, "#1F4E79", "hexagon", "#000000", 0, False),
    ("hex5", "", 1070, 560, 78, 78, 11, BLUE, "#1F4E79", "hexagon", "#000000", 0, False),
    ("konveyor", "", 680, 650, 480, 18, 11, CONVEYOR, CONVEYOR, "rect", "#000000", 0, False),
    (
        "konveyor-label",
        "Lastik Bantlı Konveyör",
        760,
        790,
        220,
        44,
        12,
        "#ffffff",
        "#000000",
        "rect",
        RED,
        0,
        False,
    ),
    (
        "kirici-label",
        "Çekiçli Kırıcı",
        860,
        330,
        140,
        40,
        12,
        "#ffffff",
        "#000000",
        "rect",
        RED,
        0,
        False,
    ),
    ("kirici", "", 1020, 310, 80, 80, 11, BLUE, "#1F4E79", "rect", "#000000", 0, False),
    (
        "cuvalli",
        "ÇUVALLI MAMUL MALLAR STOK",
        860,
        90,
        360,
        180,
        14,
        "#ffffff",
        "#000000",
        "rect",
        "#000000",
        1,
        False,
    ),
    (
        "kati",
        "KATI<br>ORGANİK<br>GÜBRE<br>STOKLAMA",
        1240,
        56,
        400,
        880,
        18,
        "#ffffff",
        "#000000",
        "rect",
        "#000000",
        0,
        False,
    ),
    (
        "caption",
        "Şekil 2: Tüm Gübre Üretimi Vaziyet Planı",
        520,
        980,
        660,
        36,
        14,
        "none",
        "none",
        "text",
        "#000000",
        0,
        False,
    ),
]

# label_id, equipment_id, exitY, entryY, entryX
ARROWS = [
    ("karistirici-label", "tank3", 1, 0, 0.5),
    ("hammadde-label", "tank2", 0, 1, 0.5),
    ("dinlendirme-label", "dinlendirme", 0, 1, 0.5),
    ("bunker-label", "bunker", 0.5, 1, 1),
    ("elek-label", "elek", 0, 0.5, 1),
    ("firin-label", "firin", 0, 0.5, 1),
    ("gran-label", "hex2", 1, 0, 0.5),
    ("konveyor-label", "konveyor", 0, 1, 0.22),
    ("kirici-label", "kirici", 1, 0, 0),
]


def xml_text(value: str) -> str:
    parts = value.split("<br>")
    return "&#xa;".join(html.escape(part, quote=True) for part in parts)


def shape_style(
    shape: str,
    fill: str,
    stroke: str,
    font_size: int,
    font_color: str,
    rounded: int,
    vertical: bool,
) -> str:
    fill_css = "none" if fill == "none" else fill
    stroke_css = "none" if stroke == "none" else stroke
    common = (
        f"whiteSpace=wrap;html=1;fillColor={fill_css};strokeColor={stroke_css};"
        f"strokeWidth=1.5;fontFamily={FONT};fontSize={font_size};fontColor={font_color};"
        "align=center;verticalAlign=middle;editable=1;locked=0;"
    )
    if vertical:
        common += "horizontal=0;"
    if shape == "text":
        return (
            f"text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;"
            f"fontFamily={FONT};fontSize={font_size};fontColor={font_color};fontStyle=1;"
            "editable=1;locked=0;"
            + ("horizontal=0;" if vertical else "")
        )
    if shape == "hopper":
        return (
            "shape=trapezoid;perimeter=trapezoidPerimeter;whiteSpace=wrap;html=1;"
            f"fillColor={fill_css};strokeColor={stroke_css};strokeWidth=1.5;rotation=180;"
            "editable=1;locked=0;"
        )
    if shape == "hexagon":
        return f"shape=hexagon;perimeter=hexagonPerimeter;{common}"
    if shape == "cylinder":
        return f"shape=cylinder3;size=12;direction=south;{common}"
    if shape == "roundRect" or rounded:
        return f"rounded=1;arcSize=20;{common}"
    return f"rounded=0;{common}"


def build_drawio() -> str:
    cells: list[str] = []
    by_id = {s[0]: s for s in SHAPES}

    def add(s: str) -> None:
        cells.append(s)

    for (
        sid,
        label,
        x,
        y,
        w,
        h,
        font_size,
        fill,
        stroke,
        shape,
        font_color,
        rounded,
        vertical,
    ) in SHAPES:
        if sid == "site":
            style = (
                "rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;"
                "strokeWidth=2;editable=0;locked=0;"
            )
        elif sid == "kati":
            style = (
                "rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;"
                "strokeWidth=1.5;fontFamily=Arial;fontSize=18;fontColor=#000000;fontStyle=1;"
                "align=center;verticalAlign=middle;editable=1;locked=0;"
            )
        else:
            style = shape_style(shape, fill, stroke, font_size, font_color, rounded, vertical)
        add(
            f'        <mxCell id="{sid}" value="{xml_text(label)}" style="{style}" '
            f'vertex="1" parent="1">\n'
            f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>\n'
            f"        </mxCell>"
        )

    # bracket over the five mixer tanks
    add(
        '        <mxCell id="tank-bracket" value="" '
        'style="endArrow=none;startArrow=none;html=1;strokeColor=#C00000;strokeWidth=1.2;" '
        'edge="1" parent="1">\n'
        '          <mxGeometry relative="1" as="geometry">\n'
        '            <mxPoint x="120" y="620" as="sourcePoint"/>\n'
        '            <mxPoint x="428" y="620" as="targetPoint"/>\n'
        '            <Array as="points">\n'
        '              <mxPoint x="120" y="608"/>\n'
        '              <mxPoint x="428" y="608"/>\n'
        "            </Array>\n"
        "          </mxGeometry>\n"
        "        </mxCell>"
    )

    for i, (src, tgt, exit_y, entry_y, entry_x) in enumerate(ARROWS, start=1):
        add(
            f'        <mxCell id="arrow-{i}" value="" '
            f'style="endArrow=classic;html=1;strokeColor=#000000;strokeWidth=1.2;'
            f'exitX=0.5;exitY={exit_y};exitDx=0;exitDy=0;entryX={entry_x};entryY={entry_y};entryDx=0;entryDy=0;" '
            f'edge="1" parent="1" source="{src}" target="{tgt}">\n'
            '          <mxGeometry relative="1" as="geometry"/>\n'
            "        </mxCell>"
        )

    # granulator arrow should go down to hexes; conveyor up
    # Override a couple of arrows with explicit points via extra edges if needed.
    _ = by_id

    body = "\n".join(cells)
    return f"""<mxfile host="Electron" agent="draw.io" version="24.7.17" type="device">
  <diagram id="gubre-vaziyet" name="Tüm Gübre Üretimi Vaziyet Planı">
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


def hex_color(value: str):
    if value in {"none", ""}:
        return white
    return HexColor(value)


def wrap_text(c, text, font, size, max_width):
    text = text.replace("<br>", "\n")
    lines = []
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


def draw_hexagon(c, x, y, w, h, fill):
    py = PAGE_H - y - h
    cx, cy = x + w / 2, py + h / 2
    rx, ry = w / 2, h / 2
    path = c.beginPath()
    for i in range(6):
        ang = math.radians(30 + i * 60)
        px = cx + rx * math.cos(ang)
        pyy = cy + ry * math.sin(ang)
        if i == 0:
            path.moveTo(px, pyy)
        else:
            path.lineTo(px, pyy)
    path.close()
    c.setFillColor(hex_color(fill))
    c.setStrokeColor(HexColor("#1F4E79"))
    c.setLineWidth(1.4)
    c.drawPath(path, stroke=1, fill=1)


def draw_hopper(c, x, y, w, h, fill):
    # trapezoid, wide at top
    py = PAGE_H - y - h
    inset = w * 0.22
    path = c.beginPath()
    path.moveTo(x, py + h)
    path.lineTo(x + w, py + h)
    path.lineTo(x + w - inset, py)
    path.lineTo(x + inset, py)
    path.close()
    c.setFillColor(hex_color(fill))
    c.setStrokeColor(HexColor("#1F4E79"))
    c.setLineWidth(1.4)
    c.drawPath(path, stroke=1, fill=1)


def draw_cylinder(c, x, y, w, h, fill):
    py = PAGE_H - y - h
    c.setFillColor(hex_color(fill))
    c.setStrokeColor(HexColor("#1F4E79"))
    c.setLineWidth(1.4)
    r = w / 2
    c.roundRect(x, py, w, h, r * 0.35, stroke=1, fill=1)


def draw_label_box(c, label, x, y, w, h, font_size, font_color, fill, stroke, vertical, bold=False):
    py = PAGE_H - y - h
    if fill != "none":
        c.setFillColor(hex_color(fill))
        c.setStrokeColor(black if stroke != "none" else white)
        c.setLineWidth(1.2)
        if stroke == "none":
            pass
        else:
            c.rect(x, py, w, h, stroke=1, fill=1)
    elif stroke not in {"none", ""}:
        c.setStrokeColor(black)
        c.setLineWidth(2)
        c.rect(x, py, w, h, stroke=1, fill=0)

    if not label:
        return
    font = "DejaVuBold" if bold else "DejaVu"
    c.setFillColor(hex_color(font_color))
    if vertical:
        c.saveState()
        c.translate(x + w / 2, py + h / 2)
        c.rotate(90)
        lines = wrap_text(c, label, font, font_size, h - 8)
        line_h = font_size + 3
        ty = line_h * len(lines) / 2 - font_size
        c.setFont(font, font_size)
        for line in lines:
            tw = c.stringWidth(line, font, font_size)
            c.drawString(-tw / 2, ty, line)
            ty -= line_h
        c.restoreState()
        return
    lines = wrap_text(c, label, font, font_size, w - 10)
    line_h = font_size + 3
    ty = py + h / 2 + line_h * len(lines) / 2 - font_size
    c.setFont(font, font_size)
    for line in lines:
        tw = c.stringWidth(line, font, font_size)
        c.drawString(x + w / 2 - tw / 2, ty, line)
        ty -= line_h


def shape_center(sid):
    rec = next(s for s in SHAPES if s[0] == sid)
    _, _, x, y, w, h, *_ = rec
    return x + w / 2, y + h / 2


def build_pdf() -> None:
    c = pdfcanvas.Canvas(str(PDF_PATH), pagesize=(PAGE_W, PAGE_H))
    c.setTitle("Şekil 2: Tüm Gübre Üretimi Vaziyet Planı")

    for (
        sid,
        label,
        x,
        y,
        w,
        h,
        font_size,
        fill,
        stroke,
        shape,
        font_color,
        rounded,
        vertical,
    ) in SHAPES:
        py = PAGE_H - y - h
        if shape == "hopper":
            draw_hopper(c, x, y, w, h, fill)
            continue
        if shape == "hexagon":
            draw_hexagon(c, x, y, w, h, fill)
            continue
        if shape == "cylinder":
            draw_cylinder(c, x, y, w, h, fill)
            continue
        if shape == "roundRect" or rounded:
            c.setFillColor(hex_color(fill) if fill != "none" else white)
            c.setStrokeColor(black if stroke != "none" else white)
            c.setLineWidth(1.5)
            rad = min(w, h) * 0.18
            if fill == "none":
                c.roundRect(x, py, w, h, rad, stroke=1, fill=0)
            else:
                c.roundRect(x, py, w, h, rad, stroke=1, fill=1)
            if label:
                draw_label_box(c, label, x, y, w, h, font_size, font_color, "none", "none", vertical, bold=True)
            continue
        if sid == "sivi":
            c.setFillColor(white)
            c.setStrokeColor(black)
            c.setLineWidth(1.5)
            c.rect(x, PAGE_H - y - h, w, h, stroke=1, fill=1)
            continue
        if sid == "kati":
            draw_label_box(
                c,
                label.replace("<br>", "\n"),
                x,
                y,
                w,
                h,
                font_size,
                font_color,
                fill,
                stroke,
                False,
                bold=True,
            )
            continue
        if shape == "text":
            draw_label_box(c, label, x, y, w, h, font_size, font_color, "none", "none", vertical, bold=True)
            continue
        draw_label_box(
            c,
            label,
            x,
            y,
            w,
            h,
            font_size,
            font_color,
            fill,
            stroke,
            vertical,
            bold=(sid in {"idari", "sivi", "caption", "cuvalli", "sevk"}),
        )

    # red bracket over tanks
    c.setStrokeColor(HexColor(RED))
    c.setLineWidth(1.2)
    c.line(120, PAGE_H - 608, 428, PAGE_H - 608)
    c.line(120, PAGE_H - 608, 120, PAGE_H - 620)
    c.line(428, PAGE_H - 608, 428, PAGE_H - 620)

    c.setStrokeColor(black)
    c.setLineWidth(1.2)
    for src, tgt, _ey, _eny, entry_x in ARROWS:
        sx, sy = shape_center(src)
        rec = next(s for s in SHAPES if s[0] == tgt)
        _, _, tx0, ty0, tw, th, *_ = rec
        tx = tx0 + tw * entry_x
        ty = ty0 + th * _eny
        c.line(sx, PAGE_H - sy, tx, PAGE_H - ty)

    c.showPage()
    c.save()


def main() -> None:
    DRAWIO_PATH.write_text(build_drawio(), encoding="utf-8")
    build_pdf()
    print(f"Wrote {DRAWIO_PATH}")
    print(f"Wrote {PDF_PATH}")


if __name__ == "__main__":
    main()
