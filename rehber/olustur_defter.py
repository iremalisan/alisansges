#!/usr/bin/env python3
"""7 günlük doldurulabilir manifest defteri (Word)."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "Yedi_Gunluk_Manifest_Defteri.docx"

PLUM = RGBColor(42, 22, 58)
ROSE = RGBColor(196, 84, 118)
GOLD = RGBColor(201, 154, 74)
MUTED = RGBColor(110, 96, 118)


def shade(cell, hex_color: str) -> None:
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), hex_color)
    shd.set(qn("w:val"), "clear")
    tc_pr.append(shd)


def set_run(run, size=12, bold=False, color=PLUM, italic=False):
    run.font.name = "Calibri"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color


def p(doc, text, size=12, bold=False, color=PLUM, space_after=8, align="left", italic=False):
    para = doc.add_paragraph()
    para.paragraph_format.space_after = Pt(space_after)
    para.paragraph_format.space_before = Pt(0)
    if align == "center":
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run(text)
    set_run(run, size, bold, color, italic)
    return para


def lines(doc, n=4):
    for _ in range(n):
        para = doc.add_paragraph()
        para.paragraph_format.space_after = Pt(10)
        run = para.add_run("________________________________________________________________")
        set_run(run, 12, False, RGBColor(200, 188, 196))


def heading_bar(doc, kicker, title):
    p(doc, kicker.upper(), 11, True, ROSE, 2)
    p(doc, title, 22, True, PLUM, 10)


THEMES = [
    ("1. gün · Netleş", "Bugün: bütçe alt–üst + 2. el/yeni + en fazla 3 model."),
    ("2. gün · Ritim", "Bugün: ehliyet kontrolü, kasko/trafik kaba fiyat, biriktirme yeri."),
    ("3. gün · Hikâye", "Bugün: 8 dk araba scripting + 5 ilan kaydet, 2’sine yaz."),
    ("4. gün · Engel", "Bugün: ‘param yetmez’i yaz. İlk küçük transferi yap."),
    ("5. gün · Kimlik", "Bugün: galeride benzer arabaya otur veya park yerinden geç."),
    ("6. gün · Kanıt", "Bugün: 1 satıcı/galeri ara. 1 fiyat veya ekspertiz sor."),
    ("7. gün · Mühürle", "Bugün: 3 adayı 1–2’ye indir. 21 günlük bakış + biriktirme kilidi."),
]


def build() -> Path:
    doc = Document()
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.left_margin = Cm(1.8)
    section.right_margin = Cm(1.8)
    section.top_margin = Cm(1.6)
    section.bottom_margin = Cm(1.6)

    p(doc, "KENDİ ARABAM İÇİN 7 GÜNLÜK MANIFEST DEFTERİ", 11, True, GOLD, 4, "center")
    p(doc, "Anahtarı çevir. Bir adım at.", 26, True, PLUM, 8, "center")
    p(
        doc,
        "Tek istek: kendi arabam. Her gün aynı iskelet: sabah 3, öğlen 6, gece 9 yazış + direksiyon SATS + 1 araba adımı. "
        "Yeni teknik ekleme. 20 model karıştırma.",
        12,
        False,
        MUTED,
        14,
        "center",
    )

    table = doc.add_table(rows=3, cols=1)
    notes = [
        "Kural: 7 gün boyunca tek istek — kendi arabam.",
        "Kural: Cümle şimdiki zamanda. En fazla 3 model adayı.",
        "Kural: İlan avı yok. Defteri kapat, 1 gerçek adım at.",
    ]
    for i, note in enumerate(notes):
        cell = table.rows[i].cells[0]
        shade(cell, "F8E8EE" if i != 1 else "EDE4F5")
        cell.text = ""
        para = cell.paragraphs[0]
        run = para.add_run(note)
        set_run(run, 13, True, PLUM)

    p(doc, "", 8, space_after=6)
    heading_bar(doc, "Sayfa 1", "İstek kilidi — kendi arabam")
    p(doc, "Bu 7 günde tek isteğim:", 12, True)
    p(doc, "Kendi arabam. (Markayı 3 adaya indirmeden büyütme.)", 12, False, MUTED, 6, italic=True)
    lines(doc, 1)
    p(doc, "369 cümlem (her gün 3 + 6 + 9 kez elle yaz):", 12, True)
    p(doc, "Çok minnettarım, kendi arabamla yola çıkıyorum ve özgür hissediyorum.", 13, True, ROSE, 8)
    p(doc, "Yedek cümle (daha somut istersen): Kendi arabamın anahtarı çantamda; her yere rahatça gidiyorum.", 11, False, MUTED, 10, italic=True)
    p(doc, "Bütçe aralığım (alt – üst) ve 2. el / yeni:", 12, True)
    lines(doc, 2)
    p(doc, "En fazla 3 model adayı:", 12, True)
    lines(doc, 2)

    doc.add_page_break()
    heading_bar(doc, "Sayfa 2", "SATS sahnesi — anahtarı çevir")
    p(doc, "Sahne, arabaya bindikten SONRA olmalıdır. 5–10 saniye, birinci tekil şahıs, GIF gibi döngü. Uyuyakalmak başarıdır.", 12, False, MUTED, 10)
    prompts = [
        "Hazır sahne: Evin önünde kendi arabam park halinde. Çantamdan anahtarı alıyorum, kapıyı açıyorum, koltuğa oturuyorum, anahtarı çeviriyorum, kemer klik, ‘geldik’.",
        "Neredeyim, saat kaç? (ör. salı 08:40, evin önü)",
        "Elimde / kulağımda / burnumda ne var? (anahtarlık, motor sesi, kumaş kokusu)",
        "Vücutta hangi ‘tabii ki benim arabam’ hissi var?",
    ]
    for prompt in prompts:
        p(doc, prompt, 12, True)
        lines(doc, 2)

    doc.add_page_break()
    heading_bar(doc, "Sayfa 3", "WOOP")
    labels = [
        ("W · Wish / İstek", "Kendi arabam. 369 cümlesiyle aynı."),
        ("O · Outcome / Sonuç", "Kapıyı açıp koltuğa oturduğun an. Kemer klik. Geldik."),
        ("O · Obstacle / Engel", "Dış fiyat değil: ‘param yetmez’ kaydırması, ilan bakıp hiç aramamak."),
        ("P · Plan", "Eğer ‘alamam’ dersem, o zaman 2 dk biriktirme notu veya 1 satıcı mesajı."),
    ]
    for title, hint in labels:
        p(doc, title, 14, True, ROSE, 2)
        p(doc, hint, 11, False, MUTED, 4, italic=True)
        lines(doc, 3)

    for day, theme in THEMES:
        doc.add_page_break()
        heading_bar(doc, day.split("·")[0].strip(), day)
        p(doc, theme, 12, False, MUTED, 10, italic=True)

        grid = doc.add_table(rows=4, cols=2)
        grid.style = "Table Grid"
        cells = [
            ("Sabah ×3 bitti mi?", "Evet / Hayır    saat: ______"),
            ("Öğlen ×6 bitti mi?", "Evet / Hayır    saat: ______"),
            ("Gece ×9 bitti mi?", "Evet / Hayır    saat: ______"),
            ("SATS ile mi uyudum?", "Evet / Hayır    his (1–10): ______"),
        ]
        for i, (a, b) in enumerate(cells):
            grid.rows[i].cells[0].text = a
            grid.rows[i].cells[1].text = b
            shade(grid.rows[i].cells[0], "EDE4F5")
            for cell in grid.rows[i].cells:
                for para in cell.paragraphs:
                    for run in para.runs:
                        set_run(run, 12, True, PLUM)

        p(doc, "", 6, space_after=8)
        p(doc, "Bugünün tek araba adımı (10 dakikayı geçmesin):", 12, True)
        lines(doc, 2)
        p(doc, "Adımı attım mı, ne oldu?", 12, True)
        lines(doc, 2)
        p(doc, "Şüphe geldiyse yaz ve bırak (tartışma):", 12, True)
        lines(doc, 2)
        p(doc, "Bugün ‘oldu’ hissine en çok yaklaştığım an:", 12, True)
        lines(doc, 2)
        if "3. gün" in day:
            p(doc, "Scripting (salı sabahı kendi araban, 8 dakika):", 12, True, ROSE)
            p(doc, "Kapıyı açıyorum… koltuk… anahtar… motor… evin önünden çıkıyorum…", 11, False, MUTED, 6, italic=True)
            lines(doc, 8)
        if "7. gün" in day:
            p(doc, "7 günün özeti + 21 güne kilit (her hafta 1 bakış + 1 biriktirme):", 12, True, ROSE)
            lines(doc, 6)

    p(doc, "", 8)
    p(
        doc,
        "Kapanış: Kendi arabam. Aynı cümle. Anahtarı çevir. Her gün 1 adım.",
        12,
        True,
        PLUM,
        6,
        "center",
    )
    p(doc, "Kaynak omurga: Neville Goddard — Feeling is the Secret  •  woopmylife.org  •  369 yazma ritmi", 10, False, MUTED, 0, "center")

    doc.save(OUT)
    return OUT


if __name__ == "__main__":
    print(build())
