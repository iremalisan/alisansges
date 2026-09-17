#!/usr/bin/env python3
"""Yılpack ÇED proje özeti ve iş akım şeması — Emrenes taslağı formatında."""

from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Flowable,
    KeepTogether,
)

pdfmetrics.registerFont(TTFont("Serif", "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Serif-Bold", "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))

BOX_FILL = HexColor("#B8D4E8")
BOX_EDGE = HexColor("#5B8BB5")
OVAL_FILL = HexColor("#7EB6D9")
ARROW = HexColor("#2F2F2F")
HEADER_BG = HexColor("#D9E2F3")
ROW_ALT = HexColor("#F2F2F2")


class FlowChart(Flowable):
    """Yılpack iş akış şemasının Emrenes tarzında, dik bağlantılı çizimi."""

    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height

    def draw(self):
        import math
        c = self.canv
        w, h = self.width, self.height

        c.setStrokeColor(HexColor("#1F4E79"))
        c.setLineWidth(1.4)
        c.rect(2, 2, w - 4, h - 4)

        def box(x, y, bw, bh, text, fill=BOX_FILL, radius=5):
            c.setFillColor(fill)
            c.setStrokeColor(BOX_EDGE)
            c.setLineWidth(1)
            c.roundRect(x - bw / 2, y - bh / 2, bw, bh, radius, fill=1, stroke=1)
            c.setFillColor(HexColor("#1A1A1A"))
            c.setFont("Sans-Bold", 7.4)
            lines = text.split("\n")
            total = (len(lines) - 1) * 9.5
            ty = y + total / 2 - 2
            for i, line in enumerate(lines):
                c.drawCentredString(x, ty - i * 9.5, line)

        def oval(x, y, bw, bh, text):
            c.setFillColor(OVAL_FILL)
            c.setStrokeColor(BOX_EDGE)
            c.setLineWidth(1)
            c.ellipse(x - bw / 2, y - bh / 2, x + bw / 2, y + bh / 2, fill=1, stroke=1)
            c.setFillColor(HexColor("#1A1A1A"))
            c.setFont("Sans-Bold", 7.4)
            lines = text.split("\n")
            total = (len(lines) - 1) * 9.5
            ty = y + total / 2 - 2
            for i, line in enumerate(lines):
                c.drawCentredString(x, ty - i * 9.5, line)

        def head(x2, y2, x1, y1):
            ang = math.atan2(y2 - y1, x2 - x1)
            size = 6.5
            p1x = x2 - size * math.cos(ang - 0.38)
            p1y = y2 - size * math.sin(ang - 0.38)
            p2x = x2 - size * math.cos(ang + 0.38)
            p2y = y2 - size * math.sin(ang + 0.38)
            c.setFillColor(ARROW)
            p = c.beginPath()
            p.moveTo(x2, y2)
            p.lineTo(p1x, p1y)
            p.lineTo(p2x, p2y)
            p.close()
            c.drawPath(p, fill=1, stroke=0)

        def polyline(pts):
            c.setStrokeColor(ARROW)
            c.setFillColor(ARROW)
            c.setLineWidth(1.15)
            p = c.beginPath()
            p.moveTo(pts[0][0], pts[0][1])
            for x, y in pts[1:]:
                p.lineTo(x, y)
            c.drawPath(p, fill=0, stroke=1)
            head(pts[-1][0], pts[-1][1], pts[-2][0], pts[-2][1])

        # Kaynak şemadaki yerleşim: ana hat ortada, PE/laminasyon sağda, baskısız kumaş solda
        x_l = w * 0.18
        x_m = w * 0.42
        x_r = w * 0.72
        x_far = w * 0.90

        bw, bh = 118, 34
        bw_w, bh_w = 132, 38
        ov_w, ov_h = 94, 32

        y_kantar = h - 44
        y_ext = y_kantar - 62
        y_dokuma = y_ext - 62
        y_pe = y_kantar
        y_lam = y_dokuma - 10
        y_baski = y_dokuma - 72
        y_konf = y_baski - 62
        y_paket = y_konf - 62
        y_gubre = y_paket
        y_sevk = y_paket - 78
        y_bkumas = y_konf
        y_basksiz = y_baski + 6

        box(x_m, y_kantar, bw_w, bh, "Hammaddenin\nKantar İşlemleri")
        box(x_m, y_ext, bw_w, bh, "Extruder (Rafya)\nİplik Üretimi")
        box(x_m, y_dokuma, bw, bh, "Dokuma")
        box(x_r, y_pe, bw, bh_w, "Polietilen\nPoşet Üretimi")
        box(x_r, y_lam, bw_w, bh_w, "Laminasyon\n(Kömür Torbaları)")
        box(x_m, y_baski, bw, bh, "Baskı")
        oval(x_r, y_basksiz, ov_w, ov_h, "Baskısız")
        oval(x_l, y_bkumas, ov_w + 6, ov_h + 4, "Baskısız\nKumaş")
        box(x_m, y_konf, bw, bh, "Konfeksiyon")
        box(x_m, y_paket, bw, bh, "Paketleme / Ambalaj")
        box(x_r, y_gubre, bw_w, bh_w, "Gübre Torbası için\nİç Geçirme İşlemi")
        box(x_m, y_sevk, bw, bh, "Sevkiyat")

        # Ana üretim hattı (kantar → extruder → dokuma; baskı laminasyondan gelir)
        polyline([(x_m, y_kantar - bh / 2), (x_m, y_ext + bh / 2)])
        polyline([(x_m, y_ext - bh / 2), (x_m, y_dokuma + bh / 2)])
        polyline([(x_m, y_baski - bh / 2), (x_m, y_konf + bh / 2)])
        polyline([(x_m, y_konf - bh / 2), (x_m, y_paket + bh / 2)])
        polyline([(x_m, y_paket - bh / 2), (x_m, y_sevk + bh / 2)])

        # Kantar -> Polietilen poşet (üstten sağa)
        y_top = y_kantar + bh / 2 + 16
        polyline([
            (x_m, y_kantar + bh / 2),
            (x_m, y_top),
            (x_r, y_top),
            (x_r, y_pe + bh_w / 2),
        ])

        # Dokuma -> Polietilen poşet (laminasyonun solundan yukarı)
        x_ch = x_m + bw / 2 + 22
        polyline([
            (x_m + bw / 2, y_dokuma + 10),
            (x_ch, y_dokuma + 10),
            (x_ch, y_pe - bh_w / 2),
            (x_r - bw / 2, y_pe - bh_w / 2),
        ])

        # Dokuma -> Laminasyon
        polyline([
            (x_m + bw / 2, y_dokuma),
            (x_r - bw_w / 2, y_lam),
        ])

        # Dokuma -> Baskısız kumaş
        polyline([
            (x_m - bw / 2, y_dokuma),
            (x_l, y_dokuma),
            (x_l, y_bkumas + (ov_h + 4) / 2),
        ])

        # Laminasyon -> Baskı
        polyline([
            (x_r - bw_w / 2, y_lam - 6),
            (x_m + bw / 2, y_lam - 6),
            (x_m, y_baski + bh / 2),
        ])

        # Laminasyon -> Baskısız
        polyline([(x_r, y_lam - bh_w / 2), (x_r, y_basksiz + ov_h / 2)])

        # Laminasyon -> Konfeksiyon
        x_mid = (x_m + x_r) / 2
        polyline([
            (x_r - bw_w / 2, y_lam),
            (x_mid, y_lam),
            (x_mid, y_konf),
            (x_m + bw / 2, y_konf),
        ])

        # Baskısız kumaş -> Konfeksiyon
        polyline([
            (x_l + (ov_w + 6) / 2, y_bkumas),
            (x_m - bw / 2, y_konf),
        ])

        # Polietilen poşet -> Gübre (sağ kenardan aşağı)
        polyline([
            (x_r + bw / 2, y_pe),
            (x_far, y_pe),
            (x_far, y_gubre),
            (x_r + bw_w / 2, y_gubre),
        ])

        # Baskısız -> Gübre
        polyline([(x_r, y_basksiz - ov_h / 2), (x_r, y_gubre + bh_w / 2)])

        # Paketleme -> Gübre
        polyline([(x_m + bw / 2, y_paket), (x_r - bw_w / 2, y_gubre)])

        # Gübre -> Sevkiyat
        polyline([
            (x_r, y_gubre - bh_w / 2),
            (x_r, y_sevk),
            (x_m + bw / 2, y_sevk),
        ])


def make_styles():
    return {
        "title": ParagraphStyle(
            "title",
            fontName="Serif-Bold",
            fontSize=13,
            leading=16,
            alignment=TA_CENTER,
            spaceAfter=10,
            textColor=black,
        ),
        "h": ParagraphStyle(
            "h",
            fontName="Serif-Bold",
            fontSize=11,
            leading=14,
            alignment=TA_LEFT,
            spaceBefore=5,
            spaceAfter=2,
        ),
        "body": ParagraphStyle(
            "body",
            fontName="Serif",
            fontSize=10,
            leading=13.5,
            alignment=TA_JUSTIFY,
            firstLineIndent=12,
        ),
        "body0": ParagraphStyle(
            "body0",
            fontName="Serif",
            fontSize=10,
            leading=13.5,
            alignment=TA_JUSTIFY,
        ),
        "sub": ParagraphStyle(
            "sub",
            fontName="Serif-Bold",
            fontSize=10,
            leading=13.5,
            alignment=TA_LEFT,
            spaceBefore=4,
            spaceAfter=2,
        ),
        "center_title": ParagraphStyle(
            "center_title",
            fontName="Serif-Bold",
            fontSize=11,
            leading=15,
            alignment=TA_CENTER,
            spaceAfter=2,
        ),
        "center_sub": ParagraphStyle(
            "center_sub",
            fontName="Serif-Bold",
            fontSize=10.5,
            leading=14,
            alignment=TA_CENTER,
            spaceAfter=10,
        ),
        "footer": ParagraphStyle(
            "footer",
            fontName="Serif",
            fontSize=9,
            alignment=TA_CENTER,
        ),
    }


def waste_table():
    data = [
        ("15 02 02*", "Tehlikeli maddelerle kirlenmiş emiciler, filtre malzemeleri (başka şekilde tanımlanmamış ise yağ filtreleri), temizleme bezleri, koruyucu giysiler"),
        ("15 01 10*", "Tehlikeli maddelerin kalıntılarını içeren ya da tehlikeli maddelerle kontamine olmuş ambalajlar"),
        ("12 01 09*", "Halojen içermeyen işleme emülsiyon ve solüsyonları"),
        ("15 01 01", "Kağıt ve karton ambalaj"),
        ("20 01 33*", "16 06 01, 16 06 02 veya 16 06 03’un altında geçen pil ve akümülatörler ve bu pilleri içeren sınıflandırılmamış karışık pil ve akümülatörler"),
        ("20 01 21*", "Flüoresan lambalar ve diğer cıva içeren atıklar"),
        ("08 01 11*", "Organik çözücüler ya da diğer tehlikeli maddeler içeren atık boya ve vernikler"),
        ("04 02 16*", "Tehlikeli maddeler içeren boya maddeleri ve pigmentler"),
    ]
    cell = ParagraphStyle("cell", fontName="Serif", fontSize=8.5, leading=11, alignment=TA_LEFT)
    rows = [[
        Paragraph("<b>ATIK<br/>KODU</b>", ParagraphStyle("th", fontName="Serif-Bold", fontSize=8.5, leading=10, alignment=TA_CENTER)),
        Paragraph("<b>ATIK KODU TANIMI</b>", ParagraphStyle("th2", fontName="Serif-Bold", fontSize=8.5, leading=10, alignment=TA_CENTER)),
    ]]
    for kod, tanim in data:
        rows.append([
            Paragraph(kod, ParagraphStyle("kod", fontName="Serif-Bold", fontSize=8.5, leading=11, alignment=TA_CENTER)),
            Paragraph(tanim, cell),
        ])
    t = Table(rows, colWidths=[28 * mm, 142 * mm])
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#7F7F7F")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]
    for i in range(1, len(rows)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), ROW_ALT))
        else:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), white))
    t.setStyle(TableStyle(style_cmds))
    return t


def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Serif", 9)
    canvas.drawRightString(A4[0] - 18 * mm, 12 * mm, str(doc.page))
    canvas.restoreState()


def flowchart_story(styles):
    return [
        Paragraph("YILPACK AMBALAJ SAN. TİC. A.Ş. ADANA ŞB.", styles["center_title"]),
        Paragraph(
            "TEKSTİLDEN ÇUVAL, P.P. DEN MAMÜL ÇUVAL, LAMİNELİ ÇUVAL, PE POŞET ÜRETİMİ",
            styles["center_title"],
        ),
        Paragraph("İŞ AKIM ŞEMASI", styles["center_sub"]),
        Spacer(1, 4),
        FlowChart(170 * mm, 188 * mm),
    ]


def build(path):
    styles = make_styles()
    doc = SimpleDocTemplate(
        path,
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title="YILPACK AMBALAJ — Proje Özeti ve İş Akım Şeması",
        author="YILPACK AMBALAJ SAN. TİC. A.Ş. ADANA ŞB.",
    )
    s = []
    s.append(Paragraph("PROJE ÖZETİ", styles["title"]))

    s.append(Paragraph("1. TESİSİN YERİ", styles["h"]))
    s.append(Paragraph(
        "Adana İli, Sarıçam İlçesi, Acıdere OSB Mh. İnönü Blv. No:15 adresinde, "
        "“Tekstilden Çuval, P.P. den Mamül Çuval, Lamineli Çuval, PE Poşet Üretimi” "
        "faaliyetleri yapılması planlanmaktadır.",
        styles["body"],
    ))

    s.append(Paragraph("2. PROJENİN TÜRÜ", styles["h"]))
    s.append(Paragraph(
        "Tekstilden Çuval, P.P. den Mamül Çuval, Lamineli Çuval, PE Poşet Üretimi "
        "faaliyetleri yapılması planlanmaktadır. Aşağıda proses özeti belirtilmiştir.",
        styles["body"],
    ))

    s.append(Paragraph("Tekstilden Çuval, P.P. den Mamül Çuval, Lamineli Çuval, PE Poşet Üretimi;", styles["sub"]))
    s.append(Paragraph(
        "Firmanın işyerinde tekstilden çuval, P.P. den mamül çuval, lamineli çuval ve PE poşet "
        "üretimi yapılmaktadır. Üretimde kullanılacak hammaddeler (PP, PE, Kalsit vb.) hammadde "
        "deposuna stoklanır. PP hammadde ve katkı maddeleri dozajlama ünitesinde karıştırılıp "
        "extruder makinesinde istenilen ebat ve kalınlıkta iplik haline getirilir. Üretilen PP ipler "
        "yuvarlak dokuma makinelerinde hortum kumaş olarak dokunur. Dokunan kumaşlar rulo halinde "
        "yarı mamül stok alanına alınır.",
        styles["body"],
    ))
    s.append(Paragraph(
        "Dokumadan çıkan kumaşlar müşteri talebine göre laminasyon ve baskı işlemine alınır. "
        "Baskı ve lamine işleminden geçen kumaşlar talep edilen boylarda kesilerek çuval haline "
        "getirilir. Çuvallar preslenerek balyalar halinde paketlenir, paletler üzerinde stoklanır ve "
        "sevkiyatı gerçekleştirilir.",
        styles["body"],
    ))

    s.append(Paragraph("3. TESİSTE KAYNAKLANACAK SIVI ATIKLAR", styles["h"]))
    s.append(Paragraph(
        "Tesiste personelden kaynaklı evsel nitelikli atıksu oluşmakta olup endüstriyel nitelikli "
        "atıksu oluşmamaktadır. Oluşan evsel nitelikli atıksular, OSB kanalizasyon sistemine verilmektedir.",
        styles["body"],
    ))

    s.append(Paragraph("4. TESİSTE KAYNAKLANACAK EMİSYONLAR", styles["h"]))
    s.append(Paragraph(
        "Tesiste baskı makinesinde boya kullanılmakta olup lamine çuvalların üstüne kaplama işlemi "
        "yapılmaktadır. Baskı ve lamina makinelerinden kaynaklı bacalar tesis içerisinde birleşerek "
        "bir adet emisyon çıkış bacası olarak dışarıya verilmektedir. Bahse konu makinelerde yakıt "
        "olarak elektrik enerjisi kullanılmaktadır. Tesiste herhangi bir emisyon kaynağı olduğu taktirde "
        "SKHKKY hükümleri çerçevesinde gerekli ölçümler yaptırılıp söz konusu yönetmelikte belirtilen "
        "sınır değerleri sağlanacak, Çevre ve Şehircilik İl Müdürlüğü’ne bilgi verilecektir.",
        styles["body"],
    ))

    s.append(Paragraph("5. TESİSTE KAYNAKLANACAK ATIKLAR", styles["h"]))
    s.append(Paragraph("Tesiste oluşabilecek atık kodları", styles["body0"]))
    s.append(Spacer(1, 4))
    s.append(waste_table())
    s.append(Spacer(1, 6))
    s.append(Paragraph(
        "Tehlikeli olmayan atıklar, Çevre, Şehircilik ve İklim Değişikliği Bakanlığı’ndan yetki almış "
        "geri dönüşüm/kazanım firmalarına verilecektir. Oluşabilecek tehlikeli atıklar ise, Çevre, Şehircilik ve "
        "İklim Değişikliği Bakanlığı’ndan yetki almış bertaraf/geri kazanım tesislerine gönderilecek ve "
        "bertarafı sağlanacaktır.",
        styles["body"],
    ))

    s.append(KeepTogether([
        Paragraph("6. TESİSTE KAYNAKLANACAK GÜRÜLTÜ", styles["h"]),
        Paragraph(
            "Tesiste herhangi bir gürültü kaynağı mevcut değildir.",
            styles["body"],
        ),
    ]))

    s.append(PageBreak())
    s.extend(flowchart_story(styles))

    doc.build(s, onFirstPage=add_page_number, onLaterPages=add_page_number)


def build_flowchart(path):
    styles = make_styles()
    doc = SimpleDocTemplate(
        path,
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title="YILPACK AMBALAJ — İş Akım Şeması",
        author="YILPACK AMBALAJ SAN. TİC. A.Ş. ADANA ŞB.",
    )
    doc.build(flowchart_story(styles))


if __name__ == "__main__":
    out = "/workspace/ced-basvuru/yilpack/YILPACK_Proje_Ozeti_ve_Is_Akim_Semasi.pdf"
    flow = "/workspace/ced-basvuru/yilpack/YILPACK_Is_Akim_Semasi.pdf"
    build(out)
    build_flowchart(flow)
    print("Wrote", out)
    print("Wrote", flow)
