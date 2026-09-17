#!/usr/bin/env python3
"""Endüstriyel tesisler için Mavi Su Verimliliği Belgesi sunumu üreticisi."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import nsmap, qn
from pptx.util import Emu, Inches, Pt
from lxml import etree

ROOT = Path(__file__).resolve().parent
IMG = ROOT / "gorseller"
OUT = ROOT / "Endustriyel_Tesisler_Mavi_Su_Belgesi.pptx"
CACHE = ROOT / "_cache"
CACHE.mkdir(exist_ok=True)

# Widescreen 16:9
W, H = Inches(13.333), Inches(7.5)

NAVY = RGBColor(10, 36, 72)
NAVY2 = RGBColor(15, 52, 96)
TEAL = RGBColor(0, 148, 154)
TEAL_D = RGBColor(0, 112, 118)
GOLD = RGBColor(214, 148, 42)
AMBER = RGBColor(196, 112, 28)
CREAM = RGBColor(247, 242, 232)
WHITE = RGBColor(255, 255, 255)
SOFT = RGBColor(232, 244, 247)
MINT = RGBColor(230, 246, 238)
SAND = RGBColor(255, 244, 224)
LAV = RGBColor(236, 232, 252)
INK = RGBColor(28, 39, 54)
MUTED = RGBColor(90, 104, 122)
GREEN = RGBColor(26, 138, 99)
CORAL = RGBColor(214, 78, 72)
SKY = RGBColor(36, 120, 196)
PURPLE = RGBColor(92, 78, 168)

FONT = "Calibri"


def emu(inches: float) -> int:
    return int(Inches(inches))


def set_run(run, size, bold=False, color=INK, italic=False):
    run.font.name = FONT
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    rPr = run._r.get_or_add_rPr()
    latin = rPr.find(qn("a:latin"))
    if latin is None:
        latin = etree.SubElement(rPr, qn("a:latin"))
    latin.set("typeface", FONT)


def add_text(tf, text, size, bold=False, color=INK, align=PP_ALIGN.LEFT, italic=False):
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    set_run(run, size, bold, color, italic)
    return p


def add_para(tf, text, size, bold=False, color=INK, align=PP_ALIGN.LEFT, space_before=0, space_after=4):
    p = tf.add_paragraph()
    p.alignment = align
    p.space_before = Pt(space_before)
    p.space_after = Pt(space_after)
    run = p.add_run()
    run.text = text
    set_run(run, size, bold, color)
    return p


def fill(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()


def fill_line(shape, color, line=None):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    if line:
        shape.line.color.rgb = line
        shape.line.width = Pt(1)
    else:
        shape.line.fill.background()


def rect(slide, l, t, w, h, color, rounded=True, radius=0.08):
    shp = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
        Inches(l), Inches(t), Inches(w), Inches(h),
    )
    fill(shp, color)
    if rounded:
        try:
            shp.adjustments[0] = radius
        except Exception:
            pass
    return shp


def pill(slide, l, t, w, h, color):
    shp = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(l), Inches(t), Inches(w), Inches(h)
    )
    fill(shp, color)
    try:
        shp.adjustments[0] = 0.5
    except Exception:
        pass
    return shp


def oval(slide, l, t, w, h, color):
    shp = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(l), Inches(t), Inches(w), Inches(h))
    fill(shp, color)
    return shp


def tb(slide, l, t, w, h, text, size, bold=False, color=INK, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    try:
        tf.auto_size = None
    except Exception:
        pass
    box.text_frame.paragraphs[0].alignment = align
    tf._txBody.bodyPr.set("anchor", {MSO_ANCHOR.TOP: "t", MSO_ANCHOR.MIDDLE: "ctr", MSO_ANCHOR.BOTTOM: "b"}.get(anchor, "t"))
    add_text(tf, text, size, bold, color, align)
    return box


def tb_multi(slide, l, t, w, h, lines, anchor=MSO_ANCHOR.TOP):
    """lines: list of (text, size, bold, color, space_before)."""
    box = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf._txBody.bodyPr.set("anchor", {MSO_ANCHOR.TOP: "t", MSO_ANCHOR.MIDDLE: "ctr", MSO_ANCHOR.BOTTOM: "b"}.get(anchor, "t"))
    first = True
    for item in lines:
        text, size = item[0], item[1]
        bold = item[2] if len(item) > 2 else False
        color = item[3] if len(item) > 3 else INK
        spb = item[4] if len(item) > 4 else 0
        if first:
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT
            p.space_before = Pt(spb)
            run = p.add_run()
            run.text = text
            set_run(run, size, bold, color)
            first = False
        else:
            add_para(tf, text, size, bold, color, space_before=spb, space_after=2)
    return box


def picture(slide, path, l, t, w, h):
    slide.shapes.add_picture(str(path), Inches(l), Inches(t), Inches(w), Inches(h))


def crop_cover(src: Path, dest: Path, size=(1920, 1080), dark_left=True):
    im = Image.open(src).convert("RGB")
    im = ImageOps.fit(im, size, Image.Resampling.LANCZOS)
    if dark_left:
        overlay = Image.new("RGB", size, (8, 28, 56))
        mask = Image.new("L", size, 0)
        d = ImageDraw.Draw(mask)
        for x in range(size[0]):
            if x < int(size[0] * 0.52):
                a = 185
            else:
                a = max(0, int(185 - (x - size[0] * 0.52) / (size[0] * 0.28) * 185))
            d.line([(x, 0), (x, size[1])], fill=a)
        im = Image.composite(overlay, im, mask)
        im = ImageEnhance.Color(im).enhance(1.08)
    im.save(dest, quality=92)
    return dest


def crop_fit(src: Path, dest: Path, size, boost=1.08):
    im = Image.open(src).convert("RGB")
    im = ImageOps.fit(im, size, Image.Resampling.LANCZOS)
    im = ImageEnhance.Color(im).enhance(boost)
    im = ImageEnhance.Contrast(im).enhance(1.04)
    im.save(dest, quality=90)
    return dest


def footer(slide, n, total=12, dark=False):
    color = RGBColor(180, 198, 214) if dark else MUTED
    tb(slide, 0.4, 7.18, 9.5, 0.25,
       "Endüstriyel Tesisler için Mavi Su Verimliliği Belgesi  •  Tarım ve Orman Bakanlığı mevzuatı esas alınmıştır",
       10, False, color)
    tb(slide, 12.2, 7.18, 0.8, 0.25, f"{n}/{total}", 10, True, color, PP_ALIGN.RIGHT)


def tr_upper(text: str) -> str:
    return text.translate(str.maketrans({"i": "İ", "ı": "I"})).upper()


def header_bar(slide, kicker, title, subtitle=None):
    rect(slide, 0, 0, 13.333, 0.12, GOLD, rounded=False)
    rect(slide, 0, 0.12, 13.333, 1.18, NAVY, rounded=False)
    tb(slide, 0.45, 0.22, 12.4, 0.28, tr_upper(kicker), 11, True, GOLD)
    tb(slide, 0.45, 0.48, 12.4, 0.42, title, 24, True, WHITE)
    if subtitle:
        tb(slide, 0.45, 0.92, 12.4, 0.28, subtitle, 12, False, RGBColor(186, 214, 230))


def card(slide, l, t, w, h, color=WHITE):
    shadow = rect(slide, l + 0.04, t + 0.05, w, h, RGBColor(220, 228, 234), radius=0.08)
    return rect(slide, l, t, w, h, color, radius=0.08)


def num_badge(slide, l, t, n, color=TEAL):
    oval(slide, l, t, 0.42, 0.42, color)
    tb(slide, l, t + 0.05, 0.42, 0.32, str(n), 14, True, WHITE, PP_ALIGN.CENTER)


def blank(prs, bg=CREAM):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, H)
    fill(bg_shape, bg)
    spTree = slide.shapes._spTree
    sp = bg_shape._element
    spTree.remove(sp)
    spTree.insert(2, sp)
    return slide

def build():
    cover = crop_cover(IMG / "cover-simple-water.jpg", CACHE / "cover.jpg")
    flush = crop_fit(IMG / "dual-flush-buttons.jpg", CACHE / "flush.jpg", (1100, 900))
    sensor = crop_fit(IMG / "sensor-faucet.jpg", CACHE / "sensor.jpg", (900, 720))
    aero = crop_fit(IMG / "aerator-tap.jpg", CACHE / "aero.jpg", (900, 720))
    oldnew = crop_fit(IMG / "old-vs-new-tap.jpg", CACHE / "oldnew.jpg", (1100, 720))
    hose_bad = crop_fit(IMG / "open-hose-waste.jpg", CACHE / "hosebad.jpg", (900, 720))
    hose_good = crop_fit(IMG / "spray-gun-hose.jpg", CACHE / "hosegood.jpg", (900, 720))
    leak = crop_fit(IMG / "leak-pipe.jpg", CACHE / "leak.jpg", (900, 720))
    poster = crop_fit(IMG / "save-water-poster.jpg", CACHE / "poster.jpg", (900, 720))
    train = crop_fit(IMG / "training-session.jpg", CACHE / "train.jpg", (900, 720))
    rain = crop_fit(IMG / "rainwater.jpg", CACHE / "rain.jpg", (900, 720))
    team = crop_fit(IMG / "water-team.jpg", CACHE / "team.jpg", (900, 700))
    cert = crop_fit(IMG / "blue-certificate-generic.jpg", CACHE / "cert.jpg", (900, 680))
    plant = crop_fit(IMG / "textile-plant.jpg", CACHE / "plant.jpg", (900, 700))
    small = crop_fit(IMG / "small-factory.jpg", CACHE / "small.jpg", (900, 700))

    prs = Presentation()
    prs.slide_width = W
    prs.slide_height = H

    # 1 KAPAK
    s = blank(prs, NAVY)
    picture(s, cover, 0, 0, 13.333, 7.5)
    rect(s, 0, 0, 13.333, 0.14, GOLD, rounded=False)
    pill(s, 0.5, 1.25, 5.6, 0.38, GOLD)
    tb(s, 0.5, 1.30, 5.6, 0.30, "MAVİ SU BELGESİ  •  NE YAPACAĞIZ?", 12, True, NAVY, PP_ALIGN.CENTER)
    tb(s, 0.5, 1.85, 8.4, 1.8, "Suyu boşa akıtmayın.\nBelgeyi alın.", 40, True, WHITE)
    tb(s, 0.5, 3.85, 7.8, 0.9,
       "Bu sunum kafa karıştırmadan anlatır: tesisinizde hangi musluk,\nhangi sifon, hangi hortum değişecek — ve belgeye nasıl yazılacak.",
       16, False, RGBColor(210, 228, 238))
    for i, (lab, col) in enumerate([("Somut örnekler", TEAL), ("Görsellerle", SKY), ("Kısa ve net", GREEN)]):
        pill(s, 0.5 + i * 2.35, 5.15, 2.2, 0.38, col)
        tb(s, 0.5 + i * 2.35, 5.20, 2.2, 0.30, lab, 12, True, WHITE, PP_ALIGN.CENTER)
    tb(s, 0.5, 6.85, 9.0, 0.28, "Tarım ve Orman Bakanlığı  •  Su Verimliliği Yönetmeliği", 12, False, RGBColor(176, 200, 216))
    tb(s, 11.4, 6.85, 1.5, 0.28, "1 / 12", 12, True, RGBColor(176, 200, 216), PP_ALIGN.RIGHT)

    # 2 NE BU BELGE
    s = blank(prs, CREAM)
    header_bar(s, "Önce netleştirelim", "Mavi belge tek cümle: suyu ölçün, azaltın, kanıtlayın",
               "Teknik terim yok. Aşağıdaki 3 kutu bütün işi anlatır.")
    boxes = [
        (TEAL, "1. Tesisinizde suyu görün", "Hangi musluktan, hangi makineden, günde kaç m³ çıktığını yazın. Sayaç yoksa fatura + tahminle başlayın."),
        (GOLD, "2. Boşa giden suyu kesin", "Sifonu 2 kademeli yapın, musluğu fotoselli yapın, hortumu tabancalı yapın, kaçağı tamir edin."),
        (SKY, "3. Bunu sisteme yükleyin", "csys.tarimorman.gov.tr  •  fotoğraf, fatura, eğitim imzası  •  belge 5 yıl geçerli."),
    ]
    for i, (col, t, d) in enumerate(boxes):
        x = 0.4 + i * 4.25
        card(s, x, 1.55, 4.05, 3.55, WHITE)
        rect(s, x, 1.55, 4.05, 0.9, col, radius=0.08)
        tb(s, x + 0.2, 1.72, 3.65, 0.6, t, 16, True, WHITE)
        tb(s, x + 0.2, 2.65, 3.65, 2.2, d, 15, False, INK)
    card(s, 0.4, 5.3, 12.5, 1.55, NAVY)
    tb(s, 0.65, 5.45, 12.0, 0.4, "Kim almak zorunda?", 16, True, GOLD)
    tb(s, 0.65, 5.9, 12.0, 0.75,
       "Kılavuz listesindeki NACE’de çalışıyor ve 50 veya daha fazla personeliniz varsa → zorunlu. 50’nin altındaysanız → isterseniz alın (aynı işler). Liste: suverimliligi.gov.tr",
       15, False, WHITE)
    footer(s, 2)

    # 3 YEDI İŞ
    s = blank(prs, CREAM)
    header_bar(s, "Yol haritası", "Yapacağınız iş tam 7 tane. Hepsi bu.",
               "Mavi belge bu 7’nin kanıtını ister. Aşağıdakileri bitirince başvurursunuz.")
    jobs = [
        ("1", "Sorumlu seçin", "1 lider + 1 eğitici + 1 teknik kişi", TEAL),
        ("2", "Suyu yazın", "Nereden geliyor, nerede bitiyor, m³ olarak", SKY),
        ("3", "Hedef koyun", "Örn. 5 yılda %15 daha az su", GOLD),
        ("4", "Plan yazın", "Bu yıl musluk, gelecek yıl yağmur deposu", AMBER),
        ("5", "Eğitim verin", "Herkese 1 kez ‘suyu boşa akıtma’", PURPLE),
        ("6", "Armatürü değiştirin", "Sifon, musluk, perlatör, hortum", GREEN),
        ("7", "Afiş asın", "Tuvalette, yemekhanede, atölyede görünsün", CORAL),
    ]
    for i, (n, t, d, col) in enumerate(jobs):
        y = 1.5 + i * 0.72
        card(s, 0.4, y, 8.4, 0.66, WHITE)
        oval(s, 0.55, y + 0.12, 0.42, 0.42, col)
        tb(s, 0.55, y + 0.18, 0.42, 0.32, n, 14, True, WHITE, PP_ALIGN.CENTER)
        tb(s, 1.15, y + 0.08, 2.6, 0.48, t, 16, True, NAVY, anchor=MSO_ANCHOR.MIDDLE)
        tb(s, 3.8, y + 0.08, 4.8, 0.48, d, 14, False, MUTED, anchor=MSO_ANCHOR.MIDDLE)
    picture(s, team, 9.05, 1.5, 3.85, 5.2)
    footer(s, 3)

    # 4 SİFON — asıl istenen örnek
    s = blank(prs, CREAM)
    header_bar(s, "Örnek 1  •  Tuvalet", "Sifon kapağında 2 düğme olsun",
               "Mavi belgenin 6. maddesi bunu ister: bireysel kullanımda suyu az harcayan armatür.")
    picture(s, flush, 0.4, 1.5, 6.15, 5.35)
    card(s, 6.75, 1.5, 6.15, 2.45, WHITE)
    oval(s, 6.95, 1.72, 0.7, 0.7, CORAL)
    tb(s, 6.95, 1.88, 0.7, 0.42, "8 L", 16, True, WHITE, PP_ALIGN.CENTER)
    tb(s, 7.8, 1.72, 4.85, 0.4, "Büyük düğme  =  tam sifon", 18, True, NAVY)
    tb(s, 7.8, 2.2, 4.85, 1.45,
       "Katı atık için. Eski tek düğmeli rezervuar her seferinde 8–9 litre boşaltır. Bunu yalnızca gerektiğinde kullanın.",
       14, False, INK)
    card(s, 6.75, 4.15, 6.15, 2.7, WHITE)
    oval(s, 6.95, 4.4, 0.7, 0.7, TEAL)
    tb(s, 6.95, 4.56, 0.7, 0.42, "2 L", 16, True, WHITE, PP_ALIGN.CENTER)
    tb(s, 7.8, 4.4, 4.85, 0.4, "Küçük düğme  =  yarım sifon", 18, True, NAVY)
    tb(s, 7.8, 4.9, 4.85, 1.7,
       "Sıvı atık için. 2–3 litre yeter. 40 çalışan günde 4 kez basarsa: eski sistem ~1.280 L, yeni sistem ~480 L. Fark günde 800 litre.",
       14, False, INK)
    footer(s, 4)

    # 5 MUSLUK
    s = blank(prs, CREAM)
    header_bar(s, "Örnek 2  •  Musluk", "Fotoselli musluk + perlatör",
               "El çekilince su kesilir. Uca takılan süzgeç (perlatör) aynı yıkamayı yarı suyla yapar.")
    picture(s, sensor, 0.35, 1.48, 4.15, 3.35)
    picture(s, aero, 4.6, 1.48, 4.15, 3.35)
    picture(s, oldnew, 8.85, 1.48, 4.1, 3.35)
    cards = [
        (0.35, TEAL, "Fotoselli (fotocell) musluk", "Sensör eli görünce açılır, el gidince kapanır. ‘Açık unutulan musluk’ biter. Lavabo başında 10–12 L/dk yerine 5–6 L/dk."),
        (4.6, GOLD, "Perlatör (musluk ucu süzgeci)", "Uca vidalanır, suyu havayla karıştırır. Pahalı bir yatırım değil. Mevcut musluğa 5 dakikada takılır. Debi yarıya iner, yıkama aynı durur."),
        (8.85, SKY, "Eski musluk → yeni musluk", "Solda damlayan, sürekli açık musluk. Sağda fotosel + perlatör. Belgeye: satın alma faturası + takılı fotoğraf yeter."),
    ]
    for x, col, t, d in cards:
        card(s, x, 5.0, 4.15, 1.85, WHITE)
        tb(s, x + 0.15, 5.1, 3.85, 0.4, t, 14, True, col)
        tb(s, x + 0.15, 5.5, 3.85, 1.2, d, 12, False, INK)
    footer(s, 5)

    # 6 HORTUM / KAÇAK
    s = blank(prs, CREAM)
    header_bar(s, "Örnek 3  •  Atölye ve bahçe", "Açık hortum yasak, tabanca zorunlu, damlama tamir",
               "Fabrika suyunun çoğu burada kaçar. Üç fotoğraf: yapmayın / yapın / hemen onarın.")
    picture(s, hose_bad, 0.35, 1.48, 4.15, 3.15)
    picture(s, hose_good, 4.6, 1.48, 4.15, 3.15)
    picture(s, leak, 8.85, 1.48, 4.1, 3.15)
    cards = [
        (0.35, CORAL, "Yapmayın", "Hortumu yere bırakıp suyu açık akıtmak. 1 dakika ≈ 15–20 litre. Belgede bu fotoğraf ‘kayıp’ sayılır."),
        (4.6, TEAL, "Yapın", "Tetikli tabanca: el basınca su gelir, bırakınca kesilir. Zemin ve makine yıkamada aynı temizlik, yarı su."),
        (8.85, GOLD, "Hemen onarın", "Damlayan flanş, salmastra, vanadan gece boyu m³ gider. Haftalık ‘kaçak turu’ hedefe yazılır."),
    ]
    for x, col, t, d in cards:
        card(s, x, 4.8, 4.15, 2.05, WHITE)
        tb(s, x + 0.15, 4.92, 3.85, 0.38, t, 16, True, col)
        tb(s, x + 0.15, 5.35, 3.85, 1.3, d, 13, False, INK)
    footer(s, 6)

    # 7 AFİŞ EĞİTİM YAĞMUR
    s = blank(prs, CREAM)
    header_bar(s, "Örnek 4  •  İnsan + hatırlatıcı + yağmur", "Afişi asın, 20 dakika eğitim, çatı suyunu toplayın",
               "5. madde eğitim, 7. madde afiş. Yağmur ise sonraki Yeşil belge için şimdiden puan.")
    picture(s, poster, 0.35, 1.48, 4.15, 3.15)
    picture(s, train, 4.6, 1.48, 4.15, 3.15)
    picture(s, rain, 8.85, 1.48, 4.1, 3.15)
    cards = [
        (0.35, GOLD, "Tuvalet kapısına afiş", "‘Küçük düğme 2 L — büyük düğme 8 L’. Yemekhane ekranında aynı mesaj. Fotoğrafını çekin, sisteme yükleyin."),
        (4.6, TEAL, "Kısa eğitim", "Başvurudan önce 1 bireysel + 1 işyeri eğitimi. Video: suverimliligi.gov.tr. İmza listesi 5 yıl saklanır."),
        (8.85, SKY, "Yağmur deposu", "Çatı oluğu → filtre → depo → bahçe / zemin yıkama. Şebeke suyunu çiçeğe vermeyin."),
    ]
    for x, col, t, d in cards:
        card(s, x, 4.8, 4.15, 2.05, WHITE)
        tb(s, x + 0.15, 4.92, 3.85, 0.38, t, 15, True, col)
        tb(s, x + 0.15, 5.35, 3.85, 1.3, d, 13, False, INK)
    footer(s, 7)

    # 8 EKİP SAYAÇ HEDEF
    s = blank(prs, CREAM)
    header_bar(s, "Kağıt işi de basit", "3 kişi, 1 tablo, 1 hedef yeterli",
               "Büyük danışmanlık şart değil. Aşağıdaki örnek bir KOBİ’nin defterinden.")
    card(s, 0.4, 1.5, 4.05, 5.25, WHITE)
    tb(s, 0.6, 1.68, 3.7, 0.4, "Kim yapacak?", 18, True, TEAL)
    tb(s, 0.6, 2.2, 3.7, 4.2,
       "Lider: işletme müdürü (tek kişi).\n\nEğitim: İK veya vardiya amiri.\n\nYardımcı: bakım ustası.\n\nBir kişi 2 rol alabilir.\nAtamayı bir A4 yazıyla imzalayın.",
       15, False, INK)
    card(s, 4.65, 1.5, 4.05, 5.25, WHITE)
    tb(s, 4.85, 1.68, 3.7, 0.4, "Suyu nasıl yazacaksınız?", 18, True, SKY)
    tb(s, 4.85, 2.2, 3.7, 4.2,
       "Kaynak: şebeke 8.400 m³\nkuyu 3.100 m³\n\nNereye gitti:\nmusluk-tuvalet 1.200\nyıkama 4.600\nsoğutma 4.500\nkaçak 1.200\n\nToplam = kaynak toplamı olmalı.",
       15, False, INK)
    card(s, 8.9, 1.5, 4.05, 5.25, WHITE)
    tb(s, 9.1, 1.68, 3.7, 0.4, "Hedef örneği", 18, True, GOLD)
    tb(s, 9.1, 2.2, 3.7, 4.2,
       "Bu yıl: tüm tuvaletlere 2 kademeli sifon.\n\nBu yıl: 20 lavaboya perlatör + 8’ine fotosel.\n\nBu yıl: hortum tabancası.\n\n3 yılda: yağmur deposu.\n\nSayı: 11.500 → 9.800 m³/yıl.",
       15, False, INK)
    footer(s, 8)

    # 9 ZORUNLU GÖNÜLLÜ
    s = blank(prs, CREAM)
    header_bar(s, "Kim başvurur?", "50 kişi eşiği. NACE listeniz kılavuzda varsa bakın.",
               "Şüpheniz varsa SGK personel sayısı + oda belgesindeki NACE koduna bakın.")
    picture(s, plant, 0.4, 1.5, 4.15, 5.25)
    card(s, 4.75, 1.5, 8.15, 2.45, WHITE)
    rect(s, 4.75, 1.5, 0.18, 2.45, CORAL, rounded=False)
    tb(s, 5.15, 1.65, 7.5, 0.4, "Zorunlu", 18, True, CORAL)
    tb(s, 5.15, 2.1, 7.5, 1.55,
       "NACE kılavuzda YÜKÜMLÜ ve 50+ çalışan. 18 ay içinde sistemi kurup Mavi belgeye başvurun. Sonra 5 yıl içinde Yeşil’e gidin. Örnek: 180 kişilik boyahane, dökümhane, gıda tesisi.",
       14, False, INK)
    card(s, 4.75, 4.15, 8.15, 2.6, WHITE)
    rect(s, 4.75, 4.15, 0.18, 2.6, GREEN, rounded=False)
    tb(s, 5.15, 4.3, 7.5, 0.4, "Gönüllü", 18, True, GREEN)
    tb(s, 5.15, 4.75, 7.5, 1.7,
       "50’nin altı KOBİ veya listede gönüllü yazan faaliyet. Aynı sifon, aynı musluk, aynı form. İsterseniz Yeşil’e de atlayabilirsiniz. Örnek: 22 kişilik atölye.",
       14, False, INK)
    footer(s, 9)

    # 10 BAŞVURU
    s = blank(prs, CREAM)
    header_bar(s, "Başvuru", "Önce yetkili kişi, sonra 6 evrak, sonra gönder",
               "Tek adres: csys.tarimorman.gov.tr  •  e-Devlet  •  kargo ile gitmez")
    picture(s, cert, 9.15, 1.48, 3.75, 2.55)
    steps = [
        ("1", "Yetki", "Firma + tesis + bir kişi sistemde eşleşsin. Onay maili gelince devam."),
        ("2", "6 evrak", "SGK, oda belgesi, kapasite, sanayi sicil, ticaret sicil, çevre izin. Her biri en fazla 15 MB."),
        ("3", "7 işin kanıtı", "Ekip yazısı, su tablosu, hedef, eğitim imzası, musluk-sifon fotoğrafı, afiş fotoğrafı."),
        ("4", "Gönder", "PDF’i oku, ‘doğrudur’ de, Başvuruyu Gönder. Eksik olursa 60 gün düzeltme."),
    ]
    for i, (n, t, d) in enumerate(steps):
        y = 1.48 + i * 1.28
        card(s, 0.4, y, 8.5, 1.18, WHITE)
        oval(s, 0.55, y + 0.35, 0.48, 0.48, TEAL)
        tb(s, 0.55, y + 0.44, 0.48, 0.32, n, 16, True, WHITE, PP_ALIGN.CENTER)
        tb(s, 1.2, y + 0.18, 7.4, 0.38, t, 16, True, NAVY)
        tb(s, 1.2, y + 0.58, 7.4, 0.48, d, 13, False, MUTED)
    footer(s, 10)

    # 11 YARIN NE
    s = blank(prs, CREAM)
    header_bar(s, "Yarın sabah", "Bu 8 işi bu ay bitirirseniz belgenin yarısı biter",
               "Pahalı yatırım şart değil. Çoğu hırdavatçıdan çıkar.")
    actions = [
        (TEAL, "1", "Tuvaletleri sayın. Tek düğmeliyse 2 kademeli rezervuar sipariş edin. Kapakta ‘8 L / 2 L’ yazsın."),
        (SKY, "2", "Her lavaboya perlatör takın. Yemekhane ve misafir tuvaletlerine fotoselli musluk koyun."),
        (GOLD, "3", "Açık hortumları toplayın. Her hortumun ucuna tetikli tabanca."),
        (CORAL, "4", "Damlayan vanayı bu hafta değiştirin. Gece su sayacını okuyun: üretim yokken dönüyorsa kaçak var."),
        (PURPLE, "5", "Tuvalet kapısına A4 asın: küçük düğme 2 L, büyük düğme 8 L, musluğu kapat."),
        (GREEN, "6", "3 kişilik ekibi yazıyla atayın. Su faturasını Excel’e dökün."),
        (TEAL, "7", "suverimliligi.gov.tr videosunu tüm personele izletin, imza alın."),
        (GOLD, "8", "csys.tarimorman.gov.tr hesabını açın, yetki başvurusunu başlatın."),
    ]
    for i, (col, n, t) in enumerate(actions):
        coln, row = i % 2, i // 2
        x = 0.4 + coln * 6.45
        y = 1.48 + row * 1.32
        card(s, x, y, 6.25, 1.2, WHITE)
        oval(s, x + 0.15, y + 0.36, 0.48, 0.48, col)
        tb(s, x + 0.15, y + 0.45, 0.48, 0.32, n, 16, True, WHITE, PP_ALIGN.CENTER)
        tb(s, x + 0.78, y + 0.22, 5.25, 0.8, t, 13, False, INK, anchor=MSO_ANCHOR.MIDDLE)
    footer(s, 11)

    # 12 KONTROL
    s = blank(prs, CREAM)
    header_bar(s, "Kapıdan çıkmadan", "Fotoğrafı çekilmiş mi?",
               "Mavi belge müfettişi tesisde dolaşır gibi düşünün. Gözle görünen şeyler puan kazandırır.")
    checks = [
        ("Tuvalette 2 düğmeli sifon var, üzerinde 8 L / 2 L yazıyor.", TEAL),
        ("Lavabolarda perlatör var; yoğun yerde fotosel var.", SKY),
        ("Hortumların ucunda tabanca var, açık akan hortum yok.", GOLD),
        ("Kaçak yok / tamir kaydı var.", CORAL),
        ("Kapıda afiş var; fotoğraf çekildi.", PURPLE),
        ("Eğitim imza listesi klasörde.", GREEN),
        ("3 kişilik ekip yazısı imzalı.", TEAL),
        ("Yıllık su tablosu (gelen = giden) duruyor.", SKY),
        ("Hedef kâğıtta: bu yıl musluk, 3. yıl yağmur.", GOLD),
        ("6 evrak tarandı (SGK, oda, kapasite, sicil, gazete, çevre).", CORAL),
        ("Yetki maili geldi, CSYS açık.", PURPLE),
        ("PDF’e bakıldı, gönderildi.", GREEN),
    ]
    for i, (txt, col) in enumerate(checks):
        coln, row = i % 2, i // 2
        x = 0.4 + coln * 6.45
        y = 1.48 + row * 0.85
        card(s, x, y, 6.25, 0.75, WHITE)
        oval(s, x + 0.15, y + 0.18, 0.38, 0.38, col)
        tb(s, x + 0.15, y + 0.24, 0.38, 0.28, "✓", 14, True, WHITE, PP_ALIGN.CENTER)
        tb(s, x + 0.65, y + 0.12, 5.4, 0.52, txt, 13, False, INK, anchor=MSO_ANCHOR.MIDDLE)
    footer(s, 12)
    prs.save(OUT)
    print(f"Saved {OUT} ({OUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    build()
