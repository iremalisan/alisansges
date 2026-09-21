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
        "7 günde hızlı manifest  •  tek istek  •  369 + SATS + WOOP  •  her gün 1 somut adım",
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
    tb(s, 0.55, 1.65, 10.0, 1.2, "7 günde hızlı\nmanifest teknikleri", 40, True, WHITE)
    tb(
        s,
        0.55,
        3.35,
        9.8,
        0.7,
        "Tek istek seç. Aynı cümleyi 3-6-9 yaz. Gece olmuş gibi uyu.\nGündüz bir somut adım at. Hız buradan gelir.",
        18,
        False,
        RGBColor(236, 220, 232),
    )
    pill(s, 0.55, 4.3, 6.15, 0.5, GOLD)
    tb(s, 0.55, 4.38, 6.15, 0.36, "Hedef: 7 gün sonra otomatik alışkanlık", 15, True, PLUM, PP_ALIGN.CENTER)
    for i, (num, label) in enumerate([("01", "Netleş"), ("02", "Hisset"), ("03", "Hareket")]):
        y = 1.45 + i * 1.55
        oval(s, 11.5, y, 0.9, 0.9, GOLD if i == 2 else ROSE)
        tb(s, 11.5, y + 0.24, 0.9, 0.42, num, 18, True, WHITE, PP_ALIGN.CENTER)
        tb(s, 11.3, y + 0.96, 1.3, 0.35, label, 13, True, WHITE, PP_ALIGN.CENTER)
    tb(s, 0.55, 6.85, 9.5, 0.3, "Pratik protokol  •  ezoterik vaat değil, günlük sistem", 12, False, RGBColor(196, 176, 204))

    # 2 HIZ NASIL GELIR
    s = blank(prs)
    header_bar(s, "Çerçeve", "Hızlı sonuç isteyenler neyi yanlış anlıyor?", "Sadece hayal etmek yetmez. Hız = netlik + his + bugünkü adım.")
    boxes = [
        (LILAC, "Yavaş yol", "20 teknik birden denemek, sürekli video izlemek, ‘evren göndersin’ deyip beklemek. Zihin dağılır, istek bulanık kalır."),
        (BLUSH, "Hızlı yol", "7 gün boyunca tek istek. Aynı cümle. Aynı gece sahnesi. Her gün o isteği 10 dakikalık gerçek bir adımla ilerletmek."),
        (SAND, "Dürüst kural", "Manifest bir sihir garantisi değildir. Dikkatini ve davranışını aynı yöne kilitler. Kilitlenen şey daha çabuk görünür hale gelir."),
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
        "Neville Goddard’ın SATS’ı (uykuya yakın halde ‘oldu’ hissi) + 369 yazma (günde 18 kez aynı cümle) + WOOP (istek, sonuç, engel, eğer-o zaman planı). "
        "İlk ikisi zihni hizalar, üçüncüsü sonucu hızlandırır. Araştırmalarda tek başına pozitif hayal, eylemi bazen azaltır; WOOP ise eylemi artırır.",
        15,
        False,
        INK,
    )
    footer(s, 2)

    # 3 TEK ISTEK
    s = blank(prs)
    header_bar(s, "Kural 1", "7 gün boyunca sadece bir şey iste", "Birden fazla dilek = hiçbirinin enerjisi yetmez. Önce bir tanesini bitir.")
    card(s, 0.4, 1.55, 7.7, 5.35, WHITE)
    tb(s, 0.65, 1.75, 7.2, 0.35, "Cümle formülü (25 kelimeyi geçme)", 16, True, PLUM)
    tb(
        s,
        0.65,
        2.2,
        7.2,
        1.35,
        "Şablon:\n“Çok minnettarım, [somut sonuç] artık hayatımda ve kendimi [duygu] hissediyorum.”\n\nŞimdi zamanı. “İstiyorum / olacak” yok. Olumsuz yok. Rakam varsa yaz.",
        15,
        False,
        INK,
    )
    examples = [
        ("Zayıf", "Bol para istiyorum, stresim bitsin."),
        ("Güçlü", "Çok minnettarım, bu ay faturalarım rahat ödeniyor ve kendimi güvende hissediyorum."),
        ("Zayıf", "O beni özlesin, yazsın."),
        ("Güçlü", "Sakin ve seçilmiş hissediyorum; karşılıklı, net bir bağ içindeyim."),
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
        "90 gün içinde mümkün mü?",
        "Olduğunu hayal edince vücutta bir yumuşama var mı?",
        "Senin atabileceğin en az bir adım var mı?",
        "Başkasının iradesini zorlamıyor mu?",
        "Ölçülebilir mi? (tarih, tutar, olay)",
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
        ("Sabah", "5 dk", "Uyanır uyanmaz 369 cümlenı 3 kez elle yaz. Bitince 10 saniye gözün kapalı, ‘oldu’ hissini al."),
        ("Gündüz", "10 dk", "WOOP’taki eğer-o zaman planını çalıştır. Bugünün tek somut adımını bitirmeden telefonu açma."),
        ("İkindi", "5 dk", "Aynı cümleyi 6 kez yaz. Şüphe gelirse cümleyi tartışma; yaz ve kapat."),
        ("Gece", "8 dk", "Cümleyi 9 kez yaz. Yatağa gir. SATS sahnesini 5–10 saniyelik döngüde uykuya kadar tekrarla."),
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
    tb(s, 0.6, 2.25, 3.65, 4.3, "Yataktan kalkınca, telefonu eline almadan.\n\nAmaç: günün ilk izi ‘oldu’ olsun.\n\nYazarken acele etme. Her satırda nefes al, minnettarlığı bir saniye hisset.", 15, False, WHITE)
    card(s, 4.65, 1.55, 4.05, 5.35, PLUM)
    tb(s, 4.85, 1.75, 3.65, 0.4, "Öğlen ×6", 20, True, GOLD)
    tb(s, 4.85, 2.25, 3.65, 4.3, "Günün ortasında zihin dağılır. 6 tekrar onu geri çağırır.\n\nŞüphe gelirse yandaki sayfaya 1 cümle yaz: “Nasıl olacağını bilmiyorum, yine de oldu.” Sonra 369’a dön.", 15, False, WHITE)
    card(s, 8.9, 1.55, 4.0, 5.35, GOLD)
    tb(s, 9.1, 1.75, 3.6, 0.4, "Gece ×9", 20, True, PLUM)
    tb(s, 9.1, 2.25, 3.6, 4.3, "Uyumadan 30 dakika içinde bitir.\n\n9. satırdan sonra defteri kapat. Kanıt ara, mesaj kontrol etme, ‘çalıştı mı’ diye evrene bakma. Hemen SATS’a geç.", 15, False, PLUM)
    footer(s, 5)

    # 6 SCRIPTING
    s = blank(prs)
    header_bar(s, "Teknik 2", "Scripting: olmuş bir günü mektup gibi yaz", "Haftada 2 kez, 8 dakika. 369’un uzun hali. Film değil, sıradan bir salı sabahı yaz.")
    card(s, 0.4, 1.55, 8.3, 5.35, WHITE)
    lines = [
        "Tarih at: “21 Eylül. Bugün …”",
        "Şimdiki veya geçmiş zaman: “uyandım / oturuyorum / attım”.",
        "5 duyu: ne gördün, ne duydun, vücutta ne vardı?",
        "Küçük ayrıntı: kupa, ışık, bir cümle, bir imza.",
        "Duygu: rahatlama, sıradanlık, ‘tabii ki böyle’.",
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
        "“Salı sabahı masamda kahvemi içiyorum. Mail kutusunda onay var. Omuzlarım düşük, nefesim rahat. Anneme ‘oldu’ diye yazıyorum. Teşekkür ederim, bu artık normalim.”",
        15,
        False,
        INK,
    )
    footer(s, 6)

    # 7 SATS
    s = blank(prs)
    header_bar(s, "Teknik 3", "SATS: uykunun eşiğinde 5 saniyelik sahne", "Neville Goddard. Feeling is the Secret. Sahne, dileğin gerçekleşmesinden SONRA olmalıdır.")
    steps = [
        ("Sahneyi gündüz kur", "El sıkışma, anahtar çevirme, ‘tebrikler’ cümlesi, hesap bakiyesini görme. 5–10 saniye. Birinci tekil şahıs."),
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
        ("W", "Wish", "İstek", "Tek, net, senin için zor ama mümkün dilek. 3-6-9 cümlenle aynı olsun."),
        ("O", "Outcome", "Sonuç", "Olduğunda en güzel an. 30 saniye gözün kapalı yaşa. Göğüste ne açılıyor?"),
        ("O", "Obstacle", "Engel", "Dış dünya değil, içindeki asıl fren: erteleme, utanç, ‘hak etmiyorum’, gece telefon."),
        ("P", "Plan", "Plan", "Eğer [engel belirirse], o zaman [2 dakikalık davranış]. Önceden yaz, karar anında düşünme."),
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
        "Eğer öğleden sonra ‘nasıl olsa olmaz’ diye kaydırırsam, o zaman telefonu başka odaya koyar, 2 dakikalık adımı (mail / arama / dosya / fiyat) hemen bitiririm.",
        15,
        False,
        INK,
    )
    footer(s, 8)

    # 9 YEDI GUN
    s = blank(prs)
    header_bar(s, "Takvim", "7 günlük hız protokolü", "Her gün: 369 + SATS + 1 adım. Tema değişir, sistem değişmez.")
    days = [
        ("1", "Netleş", "Tek istek, 369 cümlesi, SATS sahnesi, WOOP. İlk somut adım bugün atılır."),
        ("2", "Ritim", "Aynı cümle. En küçük görünür hareket: bir mesaj, bir dosya, bir fiyat, bir yürüyüş."),
        ("3", "Hikâye", "8 dakikalık scripting. Bir insanla konuş veya bir kapı çal."),
        ("4", "Engel", "WOOP’u yeniden yaz. Asıl iç freni adlandır. Eğer-o zaman planını sıkılaştır."),
        ("5", "Kimlik", "Günü ‘bunu zaten yaşayan kişi’ olarak geçir. Kıyafet, masa, konuşma tonu uyumlu olsun."),
        ("6", "Kanıt", "3 küçük işaret not et (zorlama). Bir büyükçe adım: başvuru, teklif, ödeme, bitirme."),
        ("7", "Mühürle", "7 günü oku. Cümleyi gerekirse %10 netleştir. Önündeki 21 güne kilit at. Kontrolü bırak."),
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
        ("Çok dilek", "Aynı hafta para, ilişki, ev, iş. Birini seç."),
        ("Gelecek zaman", "‘Olacak’ cümlesi isteği sürekli yarına iter."),
        ("Kanıt avı", "Her saat ‘geldi mi’ diye bakmak, yokluk hissini büyütür."),
        ("Başkasını zorlamak", "Birinin seni seçmesini dayatmak. Serbest, karşılıklı hali iste."),
        ("Sadece hayal", "Gündüz sıfır adım. WOOP atlanmış demektir."),
        ("Teknik koleksiyonu", "Her gün yeni yöntem. 7 gün aynı protokol."),
        ("İnanç eşiğini aşmak", "Cümle alay ettiriyorsa küçült. İnanılır gerilim kalsın."),
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
            "• Neville Goddard — Feeling is the Secret (kısa, SATS’ın kaynağı)\n"
            "• Neville — The Power of Awareness (kimlik / varsayım)\n"
            "• woopmylife.org — WOOP’u 5 dakikada öğren\n"
            "• Gollwitzer: “eğer-o zaman” planları (uygulama niyeti)",
        ),
        (
            PLUM,
            WHITE,
            "Sonra, istersen",
            "• Neville — The Law and the Promise (örnek hikâyeler)\n"
            "• Gabriele Oettingen — Rethinking Positive Thinking\n"
            "• James Clear — Atomic Habits (küçük günlük adım)\n"
            "• r/NevilleGoddard — dikkat: başarı hikâyesi bağımlılığı yapma",
        ),
        (
            GOLD,
            PLUM,
            "Şimdilik uzak dur",
            "• Her gün başka koç, başka ‘anında zengin ol’ videosu\n"
            "• 10 tekniği aynı anda karıştıran listeler\n"
            "• Başkasının iradesini manipüle etme vaatleri\n"
            "• The Secret’i tek kaynak sanmak (çok genel kalır)",
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
        ("0–3 dk", "Tek isteği bir satıra yaz. Süzgeçten geçir."),
        ("3–7 dk", "369 cümlesini yaz. Sesli oku. Vücutta sıkışma varsa yumuşat."),
        ("7–12 dk", "SATS sahnesini 5 saniyeye indir. Kağıda 3 duyusal ayrıntı."),
        ("12–16 dk", "WOOP: istek / sonuç / iç engel / eğer-o zaman."),
        ("16–20 dk", "Bugünün 1 adımını bitir. Sonra akşam 9 yazış + SATS."),
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
        "Bir istek.\nAynı cümle.\nAynı sahne.\nHer gün bir adım.\n\n7 gün sonra yeni teknik arama. 21 güne uzat.",
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
