#!/usr/bin/env python3
"""Generate editable draw.io + PDF for the fertilizer production site plan."""

from __future__ import annotations

import html
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

PAGE_W = 1680
PAGE_H = 1000
FONT = "Arial"
BLUE = "#5B9BD5"
BLUE_STROKE = "#2E5984"
RED = "#C00000"

# id, value, style, x, y, w, h
CELLS: list[tuple[str, str, str, float, float, float, float]] = []


def style_box(
    fill: str = "#ffffff",
    stroke: str = "#000000",
    size: int = 13,
    rounded: int = 0,
    extra: str = "",
    font_color: str = "#000000",
    bold: bool = False,
    vertical: bool = False,
) -> str:
    s = (
        f"rounded={rounded};whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
        f"strokeWidth=1.4;fontFamily={FONT};fontSize={size};fontColor={font_color};"
        f"align=center;verticalAlign=middle;editable=1;locked=0;"
        f"fontStyle={'1' if bold else '0'};"
    )
    if vertical:
        s += "horizontal=0;"
    return s + extra


def xml_text(value: str) -> str:
    parts = value.split("<br>")
    return "&#xa;".join(html.escape(p, quote=True) for p in parts)


def add(cid: str, value: str, style: str, x: float, y: float, w: float, h: float) -> None:
    CELLS.append((cid, value, style, x, y, w, h))


def build_cells() -> None:
    CELLS.clear()
    add(
        "site",
        "",
        "rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;strokeWidth=2;editable=0;locked=0;",
        40,
        36,
        1600,
        860,
    )
    add(
        "giris-kapi",
        "",
        "rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.6;editable=1;locked=0;",
        40,
        70,
        18,
        110,
    )
    add(
        "giris",
        "GİRİŞ",
        "text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontFamily=Arial;fontSize=14;fontStyle=1;editable=1;locked=0;horizontal=0;",
        8,
        70,
        32,
        110,
    )
    add(
        "idari",
        "İDARİ BÜRO",
        style_box(rounded=1, size=16, extra="arcSize=18;"),
        90,
        150,
        300,
        280,
    )
    add(
        "sivi",
        "SIVI GÜBRE ÜRETİM VE PAKETLEME",
        style_box(size=13, extra="verticalAlign=top;spacingTop=12;"),
        90,
        450,
        380,
        250,
    )
    add(
        "karistirici-label",
        "Karıştırıcılı Üretim Tankı",
        style_box(fill="none", stroke="none", size=12, font_color=RED, extra="fontStyle=1;"),
        110,
        520,
        280,
        28,
    )
    for i in range(5):
        add(
            f"tank-{i+1}",
            "",
            style_box(fill=BLUE, stroke=BLUE_STROKE, rounded=1, extra="arcSize=20;"),
            130 + i * 58,
            600,
            48,
            42,
        )
    add(
        "dinlendir-silindir",
        "",
        f"shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=10;"
        f"fillColor={BLUE};strokeColor={BLUE_STROKE};strokeWidth=1.4;editable=1;locked=0;",
        410,
        530,
        44,
        100,
    )
    add(
        "sevk",
        "MAMÜL MALLAR<br>SEVK BÖLÜMÜ",
        style_box(fill="none", extra="verticalAlign=top;align=left;spacingLeft=16;spacingTop=10;fontStyle=1;"),
        490,
        56,
        720,
        644,
    )
    add(
        "cuvalli",
        "ÇUVALLI MAMUL<br>MALLAR STOK",
        style_box(rounded=1, size=15, extra="arcSize=12;"),
        780,
        80,
        410,
        190,
    )
    add(
        "kati",
        "KATI<br>ORGANİK<br>GÜBRE<br>STOKLAMA",
        style_box(size=16, extra="fontStyle=1;"),
        1210,
        56,
        410,
        644,
    )
    add(
        "bunker",
        "",
        f"shape=trapezoid;perimeter=none;whiteSpace=wrap;html=1;fillColor={BLUE};"
        f"strokeColor={BLUE_STROKE};strokeWidth=1.4;rotation=180;editable=1;locked=0;",
        530,
        150,
        100,
        110,
    )
    add(
        "bunker-label",
        "Paketleme Bunkeri",
        style_box(size=12, font_color=RED, extra="fontStyle=1;"),
        650,
        175,
        170,
        36,
    )
    add(
        "elek",
        "",
        style_box(fill=BLUE, stroke=BLUE_STROKE, rounded=1, extra="arcSize=8;"),
        530,
        290,
        78,
        70,
    )
    add(
        "elek-label",
        "Elek",
        style_box(size=12, font_color=RED, extra="fontStyle=1;"),
        620,
        305,
        56,
        36,
    )
    add(
        "kirici",
        "",
        style_box(fill=BLUE, stroke=BLUE_STROKE, rounded=1, extra="arcSize=8;"),
        1040,
        280,
        90,
        80,
    )
    add(
        "kirici-label",
        "Çekiçli Kırıcı",
        style_box(size=12, font_color=RED, extra="fontStyle=1;"),
        870,
        300,
        150,
        36,
    )
    add(
        "firin",
        "",
        f"shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=12;"
        f"fillColor={BLUE};strokeColor={BLUE_STROKE};strokeWidth=1.4;direction=south;editable=1;locked=0;",
        542,
        385,
        42,
        175,
    )
    add(
        "firin-kucuk",
        "",
        f"shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=8;"
        f"fillColor={BLUE};strokeColor={BLUE_STROKE};strokeWidth=1.4;editable=1;locked=0;",
        548,
        565,
        30,
        40,
    )
    add(
        "firin-label",
        "Fırın",
        style_box(size=12, font_color=RED, extra="fontStyle=1;"),
        595,
        430,
        50,
        40,
    )
    add(
        "granulator-label",
        "Granülatör Mikseri",
        style_box(size=12, font_color=RED, extra="fontStyle=1;"),
        720,
        430,
        180,
        36,
    )
    hex_x = [690, 780, 870, 960, 1080]
    for i, x in enumerate(hex_x, start=1):
        add(
            f"hex-{i}",
            "",
            f"shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;"
            f"fillColor={BLUE};strokeColor={BLUE_STROKE};strokeWidth=1.4;editable=1;locked=0;",
            x,
            490,
            78,
            88,
        )
    add(
        "konveyor",
        "",
        "rounded=0;whiteSpace=wrap;html=1;fillColor=#C00000;strokeColor=#8B0000;strokeWidth=1;editable=1;locked=0;",
        680,
        590,
        500,
        16,
    )
    add(
        "hammadde",
        "Hammadde Stok Tankı",
        style_box(size=12, font_color=RED, extra="fontStyle=1;"),
        150,
        790,
        180,
        60,
    )
    add(
        "dinlendir-label",
        "Sıvı Gübre<br>Dinlendirme<br>Tankı",
        style_box(size=12, font_color=RED, extra="fontStyle=1;"),
        350,
        790,
        180,
        70,
    )
    add(
        "konveyor-label",
        "Lastik Bantlı Konveyör",
        style_box(size=12, font_color=RED, extra="fontStyle=1;"),
        780,
        790,
        210,
        40,
    )
    add(
        "caption",
        "Şekil 2: Tüm Gübre Üretimi Vaziyet Planı",
        "text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;"
        "fontFamily=Arial;fontSize=14;fontStyle=1;editable=1;locked=0;",
        500,
        930,
        680,
        32,
    )


EDGES = [
    # source, target, extra style
    ("karistirici-label", "tank-3", "endArrow=none;startArrow=none;exitX=0.15;exitY=1;entryX=0.5;entryY=0;"),
    ("karistirici-label", "tank-5", "endArrow=none;startArrow=none;exitX=0.85;exitY=1;entryX=0.5;entryY=0;"),
    ("granulator-label", "hex-2", "endArrow=classic;exitX=0.3;exitY=1;entryX=0.5;entryY=0;"),
    ("konveyor-label", "konveyor", "endArrow=classic;exitX=0.5;exitY=0;entryX=0.5;entryY=1;"),
]


def build_drawio() -> str:
    build_cells()
    parts: list[str] = []
    for cid, value, style, x, y, w, h in CELLS:
        parts.append(
            f'        <mxCell id="{cid}" value="{xml_text(value)}" style="{style}" '
            f'vertex="1" parent="1">\n'
            f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>\n'
            f"        </mxCell>"
        )
    for i, (src, tgt, extra) in enumerate(EDGES, start=1):
        parts.append(
            f'        <mxCell id="edge-{i}" value="" style="html=1;strokeColor=#000000;'
            f'strokeWidth=1;{extra}editable=1;locked=0;" edge="1" parent="1" '
            f'source="{src}" target="{tgt}">\n'
            f'          <mxGeometry relative="1" as="geometry"/>\n'
            f"        </mxCell>"
        )
    # bracket line under Karıştırıcılı Üretim Tankı
    parts.append(
        """        <mxCell id="bracket" value="" style="endArrow=none;html=1;strokeColor=#C00000;strokeWidth=1.2;editable=1;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="130" y="555" as="sourcePoint"/>
            <mxPoint x="410" y="555" as="targetPoint"/>
          </mxGeometry>
        </mxCell>"""
    )
    body = "\n".join(parts)
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


def draw_hexagon(c: pdfcanvas.Canvas, x: float, y: float, w: float, h: float) -> None:
    py = PAGE_H - y - h
    path = c.beginPath()
    pts = [
        (x + w * 0.25, py + h),
        (x + w * 0.75, py + h),
        (x + w, py + h * 0.5),
        (x + w * 0.75, py),
        (x + w * 0.25, py),
        (x, py + h * 0.5),
    ]
    path.moveTo(*pts[0])
    for px, pyy in pts[1:]:
        path.lineTo(px, pyy)
    path.close()
    c.setFillColor(HexColor(BLUE))
    c.setStrokeColor(HexColor(BLUE_STROKE))
    c.setLineWidth(1.3)
    c.drawPath(path, stroke=1, fill=1)


def draw_hopper(c: pdfcanvas.Canvas, x: float, y: float, w: float, h: float) -> None:
    py = PAGE_H - y - h
    path = c.beginPath()
    path.moveTo(x, py + h)
    path.lineTo(x + w, py + h)
    path.lineTo(x + w * 0.78, py)
    path.lineTo(x + w * 0.22, py)
    path.close()
    c.setFillColor(HexColor(BLUE))
    c.setStrokeColor(HexColor(BLUE_STROKE))
    c.setLineWidth(1.3)
    c.drawPath(path, stroke=1, fill=1)


def draw_cylinder(c: pdfcanvas.Canvas, x: float, y: float, w: float, h: float) -> None:
    py = PAGE_H - y - h
    r = w / 2
    c.setFillColor(HexColor(BLUE))
    c.setStrokeColor(HexColor(BLUE_STROKE))
    c.setLineWidth(1.3)
    c.roundRect(x, py, w, h, r * 0.35, stroke=1, fill=1)
    c.ellipse(x, py + h - r * 0.45, x + w, py + h + r * 0.15, stroke=1, fill=1)


def wrap(c, text, font, size, max_w):
    text = text.replace("<br>", "\n")
    lines = []
    for para in text.split("\n"):
        words = para.split() or [""]
        cur = words[0]
        for w in words[1:]:
            trial = f"{cur} {w}"
            if c.stringWidth(trial, font, size) <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def build_pdf() -> None:
    build_cells()
    c = pdfcanvas.Canvas(str(PDF_PATH), pagesize=(PAGE_W, PAGE_H))
    c.setTitle("Şekil 2: Tüm Gübre Üretimi Vaziyet Planı")
    skip_draw = {"bunker", "firin", "firin-kucuk", "dinlendir-silindir"} | {f"hex-{i}" for i in range(1, 6)} | {
        "giris"
    }

    for cid, value, style, x, y, w, h in CELLS:
        if cid in {f"hex-{i}" for i in range(1, 6)}:
            draw_hexagon(c, x, y, w, h)
            continue
        if cid == "bunker":
            draw_hopper(c, x, y, w, h)
            continue
        if cid in {"firin", "firin-kucuk", "dinlendir-silindir"}:
            draw_cylinder(c, x, y, w, h)
            continue
        py = PAGE_H - y - h
        fill = "#ffffff"
        if "fillColor=#5B9BD5" in style:
            fill = BLUE
        elif "fillColor=#C00000" in style:
            fill = "#C00000"
        elif "fillColor=none" in style:
            fill = None
        stroke = "#000000" if "strokeColor=none" not in style else None
        rounded = "rounded=1" in style or "arcSize" in style
        if cid == "giris":
            c.setFillColor(black)
            c.setFont("DejaVuBold", 11)
            c.saveState()
            c.translate(x + w / 2, py + h / 2)
            c.rotate(90)
            c.drawCentredString(0, -4, "GİRİŞ")
            c.restoreState()
            continue
        c.setLineWidth(1.4)
        if fill:
            c.setFillColor(HexColor(fill))
        c.setStrokeColor(black if stroke else white)
        if rounded and fill:
            c.roundRect(x, py, w, h, 18 if cid in {"idari", "cuvalli"} else 8, stroke=1, fill=1)
        elif fill is None:
            if stroke:
                c.rect(x, py, w, h, stroke=1, fill=0)
        else:
            c.rect(x, py, w, h, stroke=1 if stroke else 0, fill=1)
        if not value:
            continue
        font_color = HexColor(RED) if "fontColor=#C00000" in style else black
        size = 12
        if "fontSize=16" in style:
            size = 15
        elif "fontSize=15" in style:
            size = 14
        elif "fontSize=14" in style:
            size = 13
        elif "fontSize=13" in style:
            size = 12
        bold = "fontStyle=1" in style
        font = "DejaVuBold" if bold else "DejaVu"
        c.setFillColor(font_color)
        c.setFont(font, size)
        lines = wrap(c, value, font, size, w - 12)
        line_h = size + 3
        top_align = "verticalAlign=top" in style
        if top_align:
            ty = py + h - 22
        else:
            ty = py + h / 2 + line_h * len(lines) / 2 - size
        align_left = "align=left" in style
        for line in lines:
            tw = c.stringWidth(line, font, size)
            tx = x + 16 if align_left else x + w / 2 - tw / 2
            c.drawString(tx, ty, line)
            ty -= line_h

    # arrows / bracket
    c.setStrokeColor(HexColor(RED))
    c.setLineWidth(1.2)
    c.line(130, PAGE_H - 555, 410, PAGE_H - 555)
    c.setStrokeColor(black)
    c.setLineWidth(1)
    # mixer bracket ticks
    c.line(130, PAGE_H - 555, 130, PAGE_H - 568)
    c.line(410, PAGE_H - 555, 410, PAGE_H - 568)
    # granulator arrow
    c.line(780, PAGE_H - 466, 819, PAGE_H - 490)
    # conveyor arrow
    c.line(885, PAGE_H - 790, 930, PAGE_H - 606)

    c.showPage()
    c.save()


def main() -> None:
    DRAWIO_PATH.write_text(build_drawio(), encoding="utf-8")
    build_pdf()
    print(f"Wrote {DRAWIO_PATH}")
    print(f"Wrote {PDF_PATH}")


if __name__ == "__main__":
    main()
