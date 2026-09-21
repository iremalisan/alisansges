#!/usr/bin/env python3
"""7 günde hızlı manifest teknikleri sunumu."""

from __future__ import annotations

from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "Hizli_Manifest_Teknikleri.pptx"

W, H = Inches(13.333), Inches(7.5)

PLUM = RGBColor(42, 22, 58)
PLUM2 = RGBColor(62, 34, 82)
ROSE = RGBColor(196, 84, 118)
GOLD = RGBColor(201, 154, 74)
CREAM = RGBColor(251, 246, 238)
WHITE = RGBColor(255, 255, 255)
LILAC = RGBColor(237, 228, 245)
BLUSH = RGBColor(248, 232, 238)
SAND = RGBColor(255, 244, 224)
MINT = RGBColor(232, 244, 236)
INK = RGBColor(32, 24, 42)
MUTED = RGBColor(110, 96, 118)
GREEN = RGBColor(46, 128, 96)
CORAL = RGBColor(176, 64, 72)
FONT = "Calibri"
TOTAL = 12


def set_run(run, size, bold=False, color=INK, italic=False):
    run.font.name = FONT
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    r_pr = run._r.get_or_add_rPr()
    latin = r_pr.find(qn("a:latin"))
    if latin is None:
        latin = etree.SubElement(r_pr, qn("a:latin"))
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


def rect(slide, left, top, width, height, color, rounded=True, radius=0.08):
    shp = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
        Inches(left),
        Inches(top),
        Inches(width),
        Inches(height),
    )
    fill(shp, color)
    if rounded:
        try:
            shp.adjustments[0] = radius
        except Exception:
            pass
    return shp


def pill(slide, left, top, width, height, color):
    shp = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left),
        Inches(top),
        Inches(width),
        Inches(height),
    )
    fill(shp, color)
    try:
        shp.adjustments[0] = 0.5
    except Exception:
        pass
    return shp


def oval(slide, left, top, width, height, color):
    shp = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(left), Inches(top), Inches(width), Inches(height))
    fill(shp, color)
    return shp


def tb(slide, left, top, width, height, text, size, bold=False, color=INK, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, italic=False):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = box.text_frame
    tf.word_wrap = True
    tf._txBody.bodyPr.set(
        "anchor",
        {MSO_ANCHOR.TOP: "t", MSO_ANCHOR.MIDDLE: "ctr", MSO_ANCHOR.BOTTOM: "b"}.get(anchor, "t"),
    )
    add_text(tf, text, size, bold, color, align, italic)
    return box


def blank(prs, color=CREAM):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, H)
    fill(bg, color)
    return slide


def header_bar(slide, kicker, title, subtitle=""):
    rect(slide, 0, 0, 13.333, 1.22, PLUM, rounded=False)
    rect(slide, 0, 1.22, 13.333, 0.08, GOLD, rounded=False)
    pill(slide, 0.4, 0.16, 2.2, 0.28, ROSE)
    tb(slide, 0.4, 0.18, 2.2, 0.24, kicker, 11, True, WHITE, PP_ALIGN.CENTER)
    tb(slide, 0.4, 0.48, 12.4, 0.42, title, 24, True, WHITE)
    if subtitle:
        tb(slide, 0.4, 0.9, 12.4, 0.26, subtitle, 12, False, RGBColor(230, 214, 236))


def footer(slide, page):
    tb(
        slide,
        0.4,
        7.16,
        11.2,
        0.26,
        "Kendi arabam  •  369 + SATS + WOOP  •  her gün 1 araba adımı",
        10,
        False,
        MUTED,
    )
    tb(slide, 12.05, 7.16, 0.9, 0.25, f"{page}/{TOTAL}", 10, True, MUTED, PP_ALIGN.RIGHT)


def card(slide, left, top, width, height, color=WHITE):
    return rect(slide, left, top, width, height, color, rounded=True, radius=0.06)


def build() -> Path:
    prs = Presentation()
    prs.slide_width = W
    prs.slide_height = H

    # 1 KAPAK
    s = blank(prs, PLUM)
    rect(s, 0, 0, 0.22, 7.5, GOLD, rounded=False)
    rect(s, 10.85, 0, 2.49, 7.5, PLUM2, rounded=False)
    pill(s, 0.55, 1.05, 3.9, 0.38, ROSE)
    tb(s, 0.55, 1.1, 3.9, 0.3, "NE YAP  •  NEREYE BAK  •  BUGÜN BAŞLA", 12, True, WHITE, PP_ALIGN.CENTER)
    tb(s, 0.55, 1.65, 10.0, 1.2, "Kendi arabam\niçin 7 günlük manifest", 38, True, WHITE)
    tb(
        s,
        0.55,
        3.35,
        9.8,
        0.7,
        "Cümleyi yaz. Direksiyonda uyu. Gündüz bir araba adımı at.\nBu 7 günün tek isteği: kendi araban.",
        18,
        False,
        RGBColor(236, 220, 232),
    )
    pill(s, 0.55, 4.3, 6.15, 0.5, GOLD)
    tb(s, 0.55, 4.38, 6.15, 0.36, "Kilit cümle: kendi arabamla yola çıkıyorum", 15, True, PLUM, PP_ALIGN.CENTER)
    for i, (num, label) in enumerate([("01", "Netleş"), ("02", "Hisset"), ("03", "Hareket")]):
        y = 1.45 + i * 1.55
        oval(s, 11.5, y, 0.9, 0.9, GOLD if i == 2 else ROSE)
        tb(s, 11.5, y + 0.24, 0.9, 0.42, num, 18, True, WHITE, PP_ALIGN.CENTER)
        tb(s, 11.3, y + 0.96, 1.3, 0.35, label, 13, True, WHITE, PP_ALIGN.CENTER)
    tb(s, 0.55, 6.85, 9.5, 0.3, "Pratik protokol  •  ezoterik vaat değil, günlük sistem", 12, False, RGBColor(196, 176, 204))

    # 2 HIZ NASIL GELIR
    s = blank(prs)
    header_bar(s, "Çerçeve", "Araba ‘gelsin’ diye beklemek neden yavaştır?", "Hız = direksiyon hissi + bugün atılan 1 araba adımı.")
    boxes = [
        (LILAC, "Yavaş yol", "20 model, 20 reel, ‘birden param gelir’ diye beklemek. Zihin dağılır, araba hayali kalır."),
        (BLUSH, "Hızlı yol", "7 gün sadece kendi araban. Aynı cümle. Aynı gece sahnesi. Her gün 10 dakikalık gerçek adım: bütçe, ilan, galeri, biriktirme."),
        (SAND, "Dürüst kural", "Anahtar evrene sipariş değildir. Dikkatini ve adımını arabaya kilitlersen fırsat, ilan ve cesaret daha çabuk görünür."),
    ]
    for i, (color, title, body) in enumerate(boxes):
        card(s, 0.4 + i * 4.25, 1.55, 4.05, 3.35, color)
        tb(s, 0.6 + i * 4.25, 1.75, 3.65, 0.4, title, 18, True, PLUM)
        tb(s, 0.6 + i * 4.25, 2.3, 3.65, 2.35, body, 15, False, INK)
    card(s, 0.4, 5.1, 12.5, 1.85, WHITE)
    tb(s, 0.65, 5.25, 12.1, 0.35, "Bu paketin formülü", 14, True, ROSE)
    tb(
        s,
        0.65,
        5.65,
        12.1,
        1.05,
        "Neville’in SATS’ı (uykuya yakın halde direksiyonda ‘bu benim’ hissi) + 369 (günde 18 kez aynı araba cümlesi) + WOOP (para korkusu ve ertelemeyi 2 dakikalık plana bağlamak). "
        "Hayal tek başına yetmez; araba, bütçe ve bir telefonla yaklaşır.",
        15,
        False,
        INK,
    )
    footer(s, 2)

    # 3 TEK ISTEK
    s = blank(prs)
    header_bar(s, "Kural 1", "Bu 7 günün tek isteği: kendi arabam", "Ev, iş, ilişki yok. Sadece araba. Model savaşını da 3 adaya indir.")
    card(s, 0.4, 1.55, 7.7, 5.35, WHITE)
    tb(s, 0.65, 1.75, 7.2, 0.35, "Cümle formülü (25 kelimeyi geçme)", 16, True, PLUM)
    tb(
        s,
        0.65,
        2.2,
        7.2,
        1.35,
        "Senin kilit cümlen:\n“Çok minnettarım, kendi arabamla yola çıkıyorum ve özgür hissediyorum.”\n\nŞimdi zamanı. ‘İstiyorum / olacak’ yok. Marka takıntısı yok; his ‘kendi arabam’.",
        15,
        False,
        INK,
    )
    examples = [
        ("Zayıf", "Araba istiyorum, bir an önce olsun."),
        ("Güçlü", "Çok minnettarım, kendi arabamla yola çıkıyorum ve özgür hissediyorum."),
        ("Zayıf", "Param yetmez, belki biri alır."),
        ("Güçlü", "Kendi arabamın anahtarı çantamda; her yere rahatça gidiyorum."),
    ]
    for i, (tag, line) in enumerate(examples):
        y = 3.7 + i * 0.72
        color = BLUSH if tag == "Zayıf" else MINT
        ink = CORAL if tag == "Zayıf" else GREEN
        card(s, 0.65, y, 7.2, 0.64, color)
        tb(s, 0.8, y + 0.05, 1.15, 0.5, tag, 13, True, ink, anchor=MSO_ANCHOR.MIDDLE)
        tb(s, 2.0, y + 0.05, 5.65, 0.5, line, 13, False, INK, anchor=MSO_ANCHOR.MIDDLE)
    card(s, 8.3, 1.55, 4.6, 5.35, LILAC)
    tb(s, 8.5, 1.75, 4.2, 0.4, "Seçim süzgeci", 16, True, PLUM)
    checks = [
        "90 günde peşinat / kredi / 2. el mümkün mü?",
        "Direksiyonda hayal edince vücut yumuşuyor mu?",
        "Bugün atabileceğin 1 araba adımı var mı?",
        "Başkasının sana araba almasını dayatmıyor musun?",
        "Ölçülebilir mi? (bütçe aralığı, 2. el / yeni)",
    ]
    for i, line in enumerate(checks):
        y = 2.35 + i * 0.8
        oval(s, 8.55, y + 0.05, 0.38, 0.38, ROSE)
        tb(s, 8.55, y + 0.1, 0.38, 0.3, str(i + 1), 12, True, WHITE, PP_ALIGN.CENTER)
        tb(s, 9.1, y, 3.55, 0.7, line, 14, False, INK)
    footer(s, 3)

    # 4 GUNLUK PROTOKOL
    s = blank(prs)
    header_bar(s, "Sistem", "Günde 20–25 dakika, dört katman", "Aynı sırayı 7 gün bozma. Yeni teknik ekleme.")
    layers = [
        ("Sabah", "5 dk", "Uyanır uyanmaz araba cümlenı 3 kez elle yaz. Bitince 10 saniye: anahtar elde, direksiyonda ‘bu benim’."),
        ("Gündüz", "10 dk", "Bugünün araba adımını bitir: bütçe, ilan, galeri, sigorta veya biriktirme. Bitirmeden kaydırma."),
        ("İkindi", "5 dk", "Aynı cümleyi 6 kez yaz. ‘Param yetmez’ gelirse yaz ve kapat; cümleyi tartışma."),
        ("Gece", "8 dk", "Cümleyi 9 kez yaz. Yatağa gir. Anahtarı çevirdiğin 5 saniyelik sahneyi uykuya kadar döngüle."),
    ]
    for i, (when, mins, body) in enumerate(layers):
        y = 1.5 + i * 1.3
        card(s, 0.4, y, 12.5, 1.18, WHITE if i % 2 == 0 else LILAC)
        pill(s, 0.6, y + 0.35, 1.7, 0.48, ROSE if i < 3 else GOLD)
        tb(s, 0.6, y + 0.42, 1.7, 0.35, when, 14, True, WHITE if i < 3 else PLUM, PP_ALIGN.CENTER)
        tb(s, 2.5, y + 0.18, 1.3, 0.8, mins, 20, True, PLUM, anchor=MSO_ANCHOR.MIDDLE)
        tb(s, 3.9, y + 0.2, 8.7, 0.8, body, 15, False, INK, anchor=MSO_ANCHOR.MIDDLE)
    footer(s, 4)

    # 5 369
    s = blank(prs)
    header_bar(s, "Teknik 1", "369: aynı cümleyi 3 + 6 + 9 yaz", "Tesla’ya ait sihirli bir formül değil. Dikkat kilidi. Elle yazmak ekrandan daha iyi işler.")
    card(s, 0.4, 1.55, 4.05, 5.35, ROSE)
    tb(s, 0.6, 1.75, 3.65, 0.4, "Sabah ×3", 20, True, WHITE)
    tb(s, 0.6, 2.25, 3.65, 4.3, "Yataktan kalkınca, ilan sitesini açmadan.\n\nAmaç: günün ilk izi ‘kendi arabam’ olsun.\n\nHer satırda 1 saniye direksiyon hissi: elin simitte, omuzlar düşük.", 15, False, WHITE)
    card(s, 4.65, 1.55, 4.05, 5.35, PLUM)
    tb(s, 4.85, 1.75, 3.65, 0.4, "Öğlen ×6", 20, True, GOLD)
    tb(s, 4.85, 2.25, 3.65, 4.3, "Günün ortasında ‘alamam’ gelir. 6 tekrar onu geri çağırır.\n\nŞüphe gelirse bir satır yaz: “Nasıl olacağını bilmiyorum, anahtar yine de benim.” Sonra 369’a dön.", 15, False, WHITE)
    card(s, 8.9, 1.55, 4.0, 5.35, GOLD)
    tb(s, 9.1, 1.75, 3.6, 0.4, "Gece ×9", 20, True, PLUM)
    tb(s, 9.1, 2.25, 3.6, 4.3, "Uyumadan 30 dakika içinde bitir.\n\n9. satırdan sonra ilan bakma. Defteri kapat. Hemen SATS: evin önünde park, anahtarı çevir, ‘geldik’.", 15, False, PLUM)
    footer(s, 5)

    # 6 SCRIPTING
    s = blank(prs)
    header_bar(s, "Teknik 2", "Scripting: olmuş bir günü mektup gibi yaz", "Haftada 2 kez, 8 dakika. 369’un uzun hali. Film değil, sıradan bir salı sabahı yaz.")
    card(s, 0.4, 1.55, 8.3, 5.35, WHITE)
    lines = [
        "Tarih at: “21 Eylül. Bugün …”",
        "Şimdiki veya geçmiş zaman: “uyandım / oturuyorum / attım”.",
        "5 duyu: koku, kumaş, motor sesi, simidin ısısı.",
        "Küçük ayrıntı: anahtarlık, ruhsat, park yeri, emniyet kemeri klik.",
        "Duygu: rahatlama, sıradanlık, ‘tabii ki benim arabam’.",
        "Bir teşekkür cümlesi ile bitir. Defteri kapat. Okuyup düzeltme.",
    ]
    for i, line in enumerate(lines):
        y = 1.75 + i * 0.8
        oval(s, 0.65, y, 0.42, 0.42, ROSE)
        tb(s, 0.65, y + 0.06, 0.42, 0.3, str(i + 1), 13, True, WHITE, PP_ALIGN.CENTER)
        tb(s, 1.25, y, 7.2, 0.5, line, 16, False, INK, anchor=MSO_ANCHOR.MIDDLE)
    card(s, 8.9, 1.55, 4.0, 5.35, SAND)
    tb(s, 9.1, 1.75, 3.6, 0.45, "Mini örnek", 16, True, PLUM)
    tb(
        s,
        9.1,
        2.3,
        3.6,
        4.2,
        "“Salı sabahı kendi arabamın kapısını açıyorum. Koltuk bana göre. Anahtarı çeviriyorum, motor tok çalışıyor. Evin önünden çıkıp yola karışıyorum. Teşekkür ederim, bu artık normalim.”",
        15,
        False,
        INK,
    )
    footer(s, 6)

    # 7 SATS
    s = blank(prs)
    header_bar(s, "Teknik 3", "SATS: uykunun eşiğinde 5 saniyelik sahne", "Neville Goddard. Feeling is the Secret. Sahne, dileğin gerçekleşmesinden SONRA olmalıdır.")
    steps = [
        ("Sahneyi gündüz kur", "Evin önünde park. Çantadan kendi anahtarın. Sürücü koltuğu. Anahtarı çevir. 5–10 saniye. Birinci tekil şahıs."),
        ("Bedeni bırak", "Yat. Telefon dışarı. Ayak ucundan çeneye kadar her bölgeyi ağırlaştır. Uykulu ol, uyanık analiz etme."),
        ("İçeriden yaşa", "Kendini dışarıdan izleme. Elin, ses, oda sıcaklığı, yüzündeki ifade. GIF gibi döngüle."),
        ("Hisle uyu", "Heyecan değil, doğallık. ‘Tabii ki benim’ hissi. Uyuyakalmak başarıdır. Sabah sahneyi zorlama."),
    ]
    for i, (title, body) in enumerate(steps):
        x = 0.4 + (i % 2) * 6.4
        y = 1.5 + (i // 2) * 2.55
        card(s, x, y, 6.15, 2.4, WHITE)
        oval(s, x + 0.25, y + 0.3, 0.55, 0.55, GOLD)
        tb(s, x + 0.25, y + 0.4, 0.55, 0.35, str(i + 1), 16, True, PLUM, PP_ALIGN.CENTER)
        tb(s, x + 1.0, y + 0.3, 4.85, 0.5, title, 18, True, PLUM)
        tb(s, x + 0.3, y + 1.0, 5.55, 1.15, body, 14, False, INK)
    footer(s, 7)

    # 8 WOOP
    s = blank(prs)
    header_bar(s, "Teknik 4", "WOOP: hayali eyleme çeviren bilimsel katman", "Gabriele Oettingen. woopmylife.org  •  Sadece olumlu fantezi, çabayı düşürebilir.")
    woop = [
        ("W", "Wish", "İstek", "Kendi arabam. 369 cümlenle aynı olsun. Marka savaşını 3 adaya bırak."),
        ("O", "Outcome", "Sonuç", "Kapıyı açıp koltuğa oturduğun an. Kemer klik. ‘Geldik’ hissi göğüste."),
        ("O", "Obstacle", "Engel", "Dış fiyat değil: ‘param yetmez’ kaydırması, ilanlara bakıp hiçbirini aramamak."),
        ("P", "Plan", "Plan", "Eğer ‘alamam’ gelirse, o zaman 2 dk: biriktirme notu veya 1 ilan mesajı."),
    ]
    for i, (letter, en, tr, body) in enumerate(woop):
        x = 0.4 + i * 3.2
        card(s, x, 1.55, 3.05, 4.0, WHITE)
        oval(s, x + 1.05, 1.75, 0.9, 0.9, ROSE if i % 2 == 0 else GOLD)
        tb(s, x + 1.05, 1.95, 0.9, 0.55, letter, 22, True, WHITE, PP_ALIGN.CENTER)
        tb(s, x + 0.15, 2.8, 2.75, 0.35, f"{en} · {tr}", 14, True, PLUM, PP_ALIGN.CENTER)
        tb(s, x + 0.2, 3.3, 2.65, 2.0, body, 14, False, INK)
    card(s, 0.4, 5.7, 12.5, 1.25, MINT)
    tb(s, 0.65, 5.85, 12.1, 0.3, "Hazır plan örneği", 13, True, GREEN)
    tb(
        s,
        0.65,
        6.2,
        12.1,
        0.55,
        "Eğer öğleden sonra ‘nasıl olsa araba alamam’ diye kaydırırsam, o zaman telefonu bırakır, bütçe satırını doldurur veya 1 satıcıya mesaj atarım.",
        15,
        False,
        INK,
    )
    footer(s, 8)

    # 9 YEDI GUN
    s = blank(prs)
    header_bar(s, "Takvim", "7 günde arabaya yaklaş", "Her gün: 369 + SATS + 1 araba adımı. Tema değişir, sistem değişmez.")
    days = [
        ("1", "Netleş", "Cümle + SATS sahnesi. Bütçe aralığı ve 2. el / yeni kararı. En fazla 3 model."),
        ("2", "Ritim", "Aynı cümle. Ehliyet, trafik sigortası, kasko için kaba fiyat. Biriktirme hesabı aç veya ayır."),
        ("3", "Hikâye", "8 dk scripting: salı sabahı kendi araban. 5 ilan kaydet, 2’sini yaz."),
        ("4", "Engel", "‘Param yetmez’i adlandır. İlk küçük transferi yap. WOOP planını sıkılaştır."),
        ("5", "Kimlik", "Galeride benzer bir arabaya otur veya park yerinden geç. ‘Zaten sürücüyüm’ günü."),
        ("6", "Kanıt", "1 satıcı / galeri ara. 1 ekspertiz veya fiyat sor. 3 küçük işaret not et."),
        ("7", "Mühürle", "3 adayı 1–2’ye indir. 21 güne kilit: her hafta 1 bakış + her hafta 1 biriktirme."),
    ]
    for i, (num, title, body) in enumerate(days):
        x = 0.35 + i * 1.85
        card(s, x, 1.5, 1.75, 5.4, WHITE if i % 2 == 0 else LILAC)
        oval(s, x + 0.55, 1.7, 0.65, 0.65, ROSE)
        tb(s, x + 0.55, 1.82, 0.65, 0.42, num, 18, True, WHITE, PP_ALIGN.CENTER)
        tb(s, x + 0.1, 2.5, 1.55, 0.7, title, 14, True, PLUM, PP_ALIGN.CENTER)
        tb(s, x + 0.1, 3.25, 1.55, 3.35, body, 12, False, INK, PP_ALIGN.CENTER)
    footer(s, 9)

    # 10 HATALAR
    s = blank(prs)
    header_bar(s, "Engel", "Hızı kesen yedi hata", "Bunları yaparsan teknikler çalışmaz gibi gelir. Çoğu zaman teknik değil, dağınıklık bozar.")
    mistakes = [
        ("20 model", "Her gün başka araba. En fazla 3 aday, sonra 1–2."),
        ("Gelecek zaman", "‘Araba olacak’ cümlesi anahtarı yarına iter."),
        ("İlan avı", "Saatlerce bakıp hiçbirini aramamak yokluk hissini büyütür."),
        ("Mucize peşinat", "Birinin sana almasını beklemek. Senin adımın: biriktir / kredi / 2. el."),
        ("Sadece hayal", "Direksiyon sahnesi var, galeri yok. WOOP atlanmış demektir."),
        ("Lüks eşiği", "Cümle alay ettiriyorsa önce sahibinden 2. el, sonra yükselt."),
        ("Teknik koleksiyonu", "Her gün yeni yöntem. 7 gün aynı araba protokolü."),
    ]
    for i, (title, body) in enumerate(mistakes):
        y = 1.5 + i * 0.75
        card(s, 0.4, y, 12.5, 0.68, WHITE if i % 2 == 0 else BLUSH)
        tb(s, 0.6, y + 0.08, 2.6, 0.5, title, 15, True, ROSE, anchor=MSO_ANCHOR.MIDDLE)
        tb(s, 3.3, y + 0.08, 9.3, 0.5, body, 15, False, INK, anchor=MSO_ANCHOR.MIDDLE)
    footer(s, 10)

    # 11 ARASTIRMA
    s = blank(prs)
    header_bar(s, "Harita", "Nereleri araştır, nerede takılma", "Önce kısa asıllar. Sonsuz reel değil. 7 gün pratik, sonra okuma.")
    cols = [
        (
            ROSE,
            WHITE,
            "Bu hafta oku (kısa)",
            "• Neville — Feeling is the Secret (SATS)\n"
            "• 369 cümlesi: kendi arabamla yola çıkıyorum\n"
            "• woopmylife.org — para korkusunu plana bağla\n"
            "• Sahibinden / galeri: 3 aday, gerçek fiyat",
        ),
        (
            PLUM,
            WHITE,
            "Sonra, istersen",
            "• The Power of Awareness (sürücü kimliği)\n"
            "• Rethinking Positive Thinking (WOOP kitabı)\n"
            "• 2. el: ekspertiz, tramer, kasko teklifi\n"
            "• Ehliyet / yetki belgesi eksikse onu da takvime al",
        ),
        (
            GOLD,
            PLUM,
            "Şimdilik uzak dur",
            "• ‘Evren bugün araba yollar’ reelleri\n"
            "• 10 modeli aynı anda hayal etmek\n"
            "• Marka takıntısı yüzünden 0 adım\n"
            "• Sadece hayal edip ilan / biriktirme yok",
        ),
    ]
    for i, (bg, fg, title, body) in enumerate(cols):
        x = 0.4 + i * 4.25
        card(s, x, 1.55, 4.05, 5.35, bg)
        tb(s, x + 0.2, 1.75, 3.65, 0.55, title, 18, True, fg)
        tb(s, x + 0.2, 2.45, 3.65, 4.15, body, 14, False, fg)
    footer(s, 11)

    # 12 BUGUN BASLA
    s = blank(prs)
    header_bar(s, "Bugün", "20 dakikada başla — sonra defteri kapat", "Mükemmel cümle arama. %80 netlik yeter. Hareket cümleyi düzeltir.")
    items = [
        ("0–3 dk", "Kilit cümleyi yaz: kendi arabamla yola çıkıyorum."),
        ("3–7 dk", "Bütçe alt–üst ve 2. el / yeni. En fazla 3 model."),
        ("7–12 dk", "SATS: evin önü, kendi anahtarın, çevir, kemer klik."),
        ("12–16 dk", "WOOP: ‘param yetmez’ → 2 dk biriktirme veya 1 mesaj."),
        ("16–20 dk", "Bugün 1 ilan kaydet veya 1 fiyat sor. Akşam 9 yazış + SATS."),
    ]
    for i, (mins, body) in enumerate(items):
        y = 1.48 + i * 0.78
        card(s, 0.4, y, 8.5, 0.7, WHITE)
        pill(s, 0.55, y + 0.16, 1.55, 0.38, ROSE)
        tb(s, 0.55, y + 0.2, 1.55, 0.3, mins, 12, True, WHITE, PP_ALIGN.CENTER)
        tb(s, 2.25, y + 0.1, 6.4, 0.5, body, 14, False, INK, anchor=MSO_ANCHOR.MIDDLE)
    card(s, 9.1, 1.48, 3.8, 5.4, PLUM)
    tb(s, 9.3, 1.7, 3.4, 0.7, "Kilit cümle", 16, True, GOLD)
    tb(
        s,
        9.3,
        2.5,
        3.4,
        3.9,
        "Kendi arabam.\nAynı cümle.\nAnahtarı çevir.\nHer gün 1 adım.\n\n7 gün sonra yeni teknik arama. 21 güne uzat.",
        16,
        True,
        WHITE,
    )
    footer(s, 12)

    prs.save(OUT)
    return OUT


if __name__ == "__main__":
    path = build()
    print(path)
