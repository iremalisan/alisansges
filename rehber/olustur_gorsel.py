#!/usr/bin/env python3
"""Sunum slaytlarını PNG ve tek PDF olarak çizer."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
PNG_DIR = ROOT / "gorseller"
PDF_PATH = ROOT / "Hizli_Manifest_Teknikleri.pdf"

W, H = 1920, 1080
PLUM = (42, 22, 58)
PLUM2 = (62, 34, 82)
ROSE = (196, 84, 118)
GOLD = (201, 154, 74)
CREAM = (251, 246, 238)
WHITE = (255, 255, 255)
LILAC = (237, 228, 245)
BLUSH = (248, 232, 238)
SAND = (255, 244, 224)
MINT = (232, 244, 236)
INK = (32, 24, 42)
MUTED = (110, 96, 118)
GREEN = (46, 128, 96)
CORAL = (176, 64, 72)
FONT_DIR = Path("/usr/share/fonts/truetype/macos")


def font(weight: str, size: int) -> ImageFont.FreeTypeFont:
    names = {
        "regular": "Inter-Regular.ttf",
        "medium": "Inter-Medium.ttf",
        "semibold": "Inter-SemiBold.ttf",
        "bold": "Inter-Bold.ttf",
        "italic": "Inter-Italic.ttf",
    }
    return ImageFont.truetype(str(FONT_DIR / names[weight]), size)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    for raw in text.split("\n"):
        if raw == "":
            lines.append("")
            continue
        current = ""
        for word in raw.split(" "):
            trial = (current + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= max_width:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
    return lines


def text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    content: str,
    fnt: ImageFont.FreeTypeFont,
    fill=INK,
    width: int | None = None,
    align: str = "left",
    line_gap: int = 8,
) -> int:
    x, y = xy
    lines = wrap(draw, content, fnt, width) if width else content.split("\n")
    for line in lines:
        w = draw.textlength(line, font=fnt)
        if align == "center" and width:
            tx = x + (width - w) / 2
        elif align == "right" and width:
            tx = x + width - w
        else:
            tx = x
        draw.text((tx, y), line, font=fnt, fill=fill)
        bbox = fnt.getbbox(line or "A")
        y += (bbox[3] - bbox[1]) + line_gap
    return y


def rrect(draw: ImageDraw.ImageDraw, box, fill, radius=28):
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def oval(draw: ImageDraw.ImageDraw, box, fill):
    draw.ellipse(box, fill=fill)


def header(draw: ImageDraw.ImageDraw, kicker: str, title: str, subtitle: str = ""):
    draw.rectangle((0, 0, W, 176), fill=PLUM)
    draw.rectangle((0, 176, W, 188), fill=GOLD)
    rrect(draw, (58, 24, 340, 64), ROSE, 20)
    text(draw, (58, 30), kicker, font("bold", 18), WHITE, width=282, align="center", line_gap=0)
    text(draw, (58, 78), title, font("bold", 36), WHITE, width=1780, line_gap=0)
    if subtitle:
        text(draw, (58, 130), subtitle, font("regular", 20), (230, 214, 236), width=1780, line_gap=0)


def footer(draw: ImageDraw.ImageDraw, page: int):
    text(
        draw,
        (58, 1028),
        "7 günde hızlı manifest  •  tek istek  •  369 + SATS + WOOP  •  her gün 1 somut adım",
        font("regular", 16),
        MUTED,
        width=1600,
        line_gap=0,
    )
    text(draw, (1720, 1028), f"{page}/12", font("semibold", 16), MUTED, width=140, align="right", line_gap=0)


def canvas(color=CREAM) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W, H), color)
    return img, ImageDraw.Draw(img)


def slide_cover() -> Image.Image:
    img, d = canvas(PLUM)
    d.rectangle((0, 0, 32, H), fill=GOLD)
    d.rectangle((1560, 0, W, H), fill=PLUM2)
    rrect(d, (80, 150, 640, 206), ROSE, 22)
    text(d, (80, 162), "NE YAP  •  NEREYE BAK  •  BUGÜN BAŞLA", font("bold", 18), WHITE, width=560, align="center")
    text(d, (80, 240), "7 günde hızlı\nmanifest teknikleri", font("bold", 72), WHITE, width=1400, line_gap=10)
    text(
        d,
        (80, 470),
        "Tek istek seç. Aynı cümleyi 3-6-9 yaz. Gece olmuş gibi uyu.\nGündüz bir somut adım at. Hız buradan gelir.",
        font("regular", 28),
        (236, 220, 232),
        width=1400,
        line_gap=10,
    )
    rrect(d, (80, 620, 920, 692), GOLD, 28)
    text(d, (80, 638), "Hedef: 7 gün sonra otomatik alışkanlık", font("bold", 24), PLUM, width=840, align="center")
    for i, (num, label, col) in enumerate([("01", "Netleş", ROSE), ("02", "Hisset", ROSE), ("03", "Hareket", GOLD)]):
        y = 210 + i * 220
        oval(d, (1630, y, 1760, y + 130), col)
        text(d, (1630, y + 38), num, font("bold", 28), WHITE, width=130, align="center")
        text(d, (1600, y + 145), label, font("semibold", 22), WHITE, width=190, align="center")
    text(d, (80, 980), "Pratik protokol  •  ezoterik vaat değil, günlük sistem", font("regular", 20), (196, 176, 204))
    return img


def slide_frame() -> Image.Image:
    img, d = canvas()
    header(d, "Çerçeve", "Hızlı sonuç isteyenler neyi yanlış anlıyor?", "Sadece hayal etmek yetmez. Hız = netlik + his + bugünkü adım.")
    boxes = [
        (LILAC, "Yavaş yol", "20 teknik birden denemek, sürekli video izlemek, “evren göndersin” deyip beklemek. Zihin dağılır, istek bulanık kalır."),
        (BLUSH, "Hızlı yol", "7 gün boyunca tek istek. Aynı cümle. Aynı gece sahnesi. Her gün o isteği 10 dakikalık gerçek bir adımla ilerletmek."),
        (SAND, "Dürüst kural", "Manifest bir sihir garantisi değildir. Dikkatini ve davranışını aynı yöne kilitler. Kilitlenen şey daha çabuk görünür hale gelir."),
    ]
    for i, (color, title, body) in enumerate(boxes):
        x = 58 + i * 612
        rrect(d, (x, 220, x + 580, 700), color)
        text(d, (x + 32, 250), title, font("bold", 28), PLUM, width=516)
        text(d, (x + 32, 320), body, font("regular", 22), INK, width=516, line_gap=8)
    rrect(d, (58, 730, 1862, 1000), WHITE)
    text(d, (90, 755), "Bu paketin formülü", font("bold", 22), ROSE)
    text(
        d,
        (90, 805),
        "Neville Goddard’ın SATS’ı (uykuya yakın halde “oldu” hissi) + 369 yazma (günde 18 kez aynı cümle) + WOOP (istek, sonuç, engel, eğer-o zaman planı). İlk ikisi zihni hizalar, üçüncüsü sonucu hızlandırır. Araştırmalarda tek başına pozitif hayal eylemi bazen azaltır; WOOP ise eylemi artırır.",
        font("regular", 22),
        INK,
        width=1720,
        line_gap=8,
    )
    footer(d, 2)
    return img


def slide_desire() -> Image.Image:
    img, d = canvas()
    header(d, "Kural 1", "7 gün boyunca sadece bir şey iste", "Birden fazla dilek = hiçbirinin enerjisi yetmez. Önce bir tanesini bitir.")
    rrect(d, (58, 220, 1160, 1000), WHITE)
    text(d, (90, 250), "Cümle formülü (25 kelimeyi geçme)", font("bold", 24), PLUM)
    text(
        d,
        (90, 310),
        "Şablon: “Çok minnettarım, [somut sonuç] artık hayatımda ve kendimi [duygu] hissediyorum.”\nŞimdi zamanı. “İstiyorum / olacak” yok. Olumsuz yok. Rakam varsa yaz.",
        font("regular", 22),
        INK,
        width=1020,
        line_gap=8,
    )
    examples = [
        (BLUSH, CORAL, "Zayıf", "Bol para istiyorum, stresim bitsin."),
        (MINT, GREEN, "Güçlü", "Çok minnettarım, bu ay faturalarım rahat ödeniyor ve kendimi güvende hissediyorum."),
        (BLUSH, CORAL, "Zayıf", "O beni özlesin, yazsın."),
        (MINT, GREEN, "Güçlü", "Sakin ve seçilmiş hissediyorum; karşılıklı, net bir bağ içindeyim."),
    ]
    y = 500
    for bg, ink, tag, line in examples:
        rrect(d, (90, y, 1130, y + 90), bg, 18)
        text(d, (110, y + 28), tag, font("bold", 20), ink, width=140)
        text(d, (270, y + 28), line, font("regular", 20), INK, width=820)
        y += 110
    rrect(d, (1195, 220, 1862, 1000), LILAC)
    text(d, (1230, 250), "Seçim süzgeci", font("bold", 24), PLUM)
    checks = [
        "90 gün içinde mümkün mü?",
        "Hayal edince vücutta yumuşama var mı?",
        "Atabileceğin en az bir adım var mı?",
        "Başkasının iradesini zorlamıyor mu?",
        "Ölçülebilir mi? (tarih, tutar, olay)",
    ]
    y = 330
    for i, line in enumerate(checks):
        oval(d, (1230, y, 1284, y + 54), ROSE)
        text(d, (1230, y + 12), str(i + 1), font("bold", 18), WHITE, width=54, align="center")
        text(d, (1306, y + 8), line, font("regular", 20), INK, width=520)
        y += 110
    footer(d, 3)
    return img


def slide_protocol() -> Image.Image:
    img, d = canvas()
    header(d, "Sistem", "Günde 20–25 dakika, dört katman", "Aynı sırayı 7 gün bozma. Yeni teknik ekleme.")
    layers = [
        (ROSE, WHITE, "Sabah", "5 dk", "Uyanır uyanmaz 369 cümlenı 3 kez elle yaz. Bitince 10 saniye gözün kapalı, “oldu” hissini al."),
        (ROSE, WHITE, "Gündüz", "10 dk", "WOOP’taki eğer-o zaman planını çalıştır. Bugünün tek somut adımını bitirmeden telefonu açma."),
        (ROSE, WHITE, "İkindi", "5 dk", "Aynı cümleyi 6 kez yaz. Şüphe gelirse cümleyi tartışma; yaz ve kapat."),
        (GOLD, PLUM, "Gece", "8 dk", "Cümleyi 9 kez yaz. Yatağa gir. SATS sahnesini 5–10 saniyelik döngüde uykuya kadar tekrarla."),
    ]
    y = 220
    for i, (pill, fg, when, mins, body) in enumerate(layers):
        bg = WHITE if i % 2 == 0 else LILAC
        rrect(d, (58, y, 1862, y + 170), bg, 24)
        rrect(d, (86, y + 50, 330, y + 120), pill, 24)
        text(d, (86, y + 68), when, font("bold", 22), fg, width=244, align="center")
        text(d, (360, y + 62), mins, font("bold", 32), PLUM, width=180)
        text(d, (560, y + 50), body, font("regular", 24), INK, width=1240, line_gap=8)
        y += 190
    footer(d, 4)
    return img


def slide_369() -> Image.Image:
    img, d = canvas()
    header(d, "Teknik 1", "369: aynı cümleyi 3 + 6 + 9 yaz", "Tesla’ya ait sihirli bir formül değil. Dikkat kilidi. Elle yazmak ekrandan daha iyi işler.")
    cols = [
        (ROSE, WHITE, "Sabah ×3", "Yataktan kalkınca, telefonu eline almadan.\n\nAmaç: günün ilk izi “oldu” olsun.\n\nYazarken acele etme. Her satırda nefes al, minnettarlığı bir saniye hisset."),
        (PLUM, GOLD, "Öğlen ×6", "Günün ortasında zihin dağılır. 6 tekrar onu geri çağırır.\n\nŞüphe gelirse yandaki sayfaya 1 cümle yaz: “Nasıl olacağını bilmiyorum, yine de oldu.” Sonra 369’a dön."),
        (GOLD, PLUM, "Gece ×9", "Uyumadan 30 dakika içinde bitir.\n\n9. satırdan sonra defteri kapat. Kanıt ara, mesaj kontrol etme. Hemen SATS’a geç."),
    ]
    for i, (bg, fg, title, body) in enumerate(cols):
        x = 58 + i * 612
        rrect(d, (x, 220, x + 580, 1000), bg)
        title_c = WHITE if i == 0 else fg
        body_c = WHITE if i < 2 else PLUM
        if i == 1:
            title_c = GOLD
            body_c = WHITE
        text(d, (x + 36, 260), title, font("bold", 32), title_c, width=508)
        text(d, (x + 36, 340), body, font("regular", 22), body_c, width=508, line_gap=10)
    footer(d, 5)
    return img


def slide_script() -> Image.Image:
    img, d = canvas()
    header(d, "Teknik 2", "Scripting: olmuş bir günü mektup gibi yaz", "Haftada 2 kez, 8 dakika. 369’un uzun hali. Film değil, sıradan bir salı sabahı yaz.")
    rrect(d, (58, 220, 1240, 1000), WHITE)
    lines = [
        "Tarih at: “21 Eylül. Bugün …”",
        "Şimdiki veya geçmiş zaman: “uyandım / oturuyorum / attım”.",
        "5 duyu: ne gördün, ne duydun, vücutta ne vardı?",
        "Küçük ayrıntı: kupa, ışık, bir cümle, bir imza.",
        "Duygu: rahatlama, sıradanlık, “tabii ki böyle”.",
        "Bir teşekkür cümlesi ile bitir. Defteri kapat. Okuyup düzeltme.",
    ]
    y = 255
    for i, line in enumerate(lines):
        oval(d, (90, y, 150, y + 60), ROSE)
        text(d, (90, y + 14), str(i + 1), font("bold", 20), WHITE, width=60, align="center")
        text(d, (180, y + 12), line, font("regular", 24), INK, width=1000)
        y += 115
    rrect(d, (1280, 220, 1862, 1000), SAND)
    text(d, (1315, 255), "Mini örnek", font("bold", 26), PLUM)
    text(
        d,
        (1315, 330),
        "“Salı sabahı masamda kahvemi içiyorum. Mail kutusunda onay var. Omuzlarım düşük, nefesim rahat. Anneme ‘oldu’ diye yazıyorum. Teşekkür ederim, bu artık normalim.”",
        font("regular", 22),
        INK,
        width=500,
        line_gap=10,
    )
    footer(d, 6)
    return img


def slide_sats() -> Image.Image:
    img, d = canvas()
    header(d, "Teknik 3", "SATS: uykunun eşiğinde 5 saniyelik sahne", "Neville Goddard. Feeling is the Secret. Sahne, dileğin gerçekleşmesinden SONRA olmalıdır.")
    steps = [
        ("Sahneyi gündüz kur", "El sıkışma, anahtar çevirme, “tebrikler” cümlesi, bakiyeyi görme. 5–10 saniye. Birinci tekil şahıs."),
        ("Bedeni bırak", "Yat. Telefon dışarı. Ayak ucundan çeneye kadar her bölgeyi ağırlaştır. Uykulu ol, analiz etme."),
        ("İçeriden yaşa", "Kendini dışarıdan izleme. Elin, ses, oda sıcaklığı, yüzündeki ifade. GIF gibi döngüle."),
        ("Hisle uyu", "Heyecan değil, doğallık. “Tabii ki benim.” Uyuyakalmak başarıdır. Sabah sahneyi zorlama."),
    ]
    for i, (title, body) in enumerate(steps):
        x = 58 + (i % 2) * 920
        y = 220 + (i // 2) * 380
        rrect(d, (x, y, x + 880, y + 350), WHITE)
        oval(d, (x + 36, y + 40, x + 116, y + 120), GOLD)
        text(d, (x + 36, y + 58), str(i + 1), font("bold", 26), PLUM, width=80, align="center")
        text(d, (x + 140, y + 50), title, font("bold", 28), PLUM, width=700)
        text(d, (x + 40, y + 150), body, font("regular", 22), INK, width=800, line_gap=8)
    footer(d, 7)
    return img


def slide_woop() -> Image.Image:
    img, d = canvas()
    header(d, "Teknik 4", "WOOP: hayali eyleme çeviren bilimsel katman", "Gabriele Oettingen. woopmylife.org  •  Sadece olumlu fantezi, çabayı düşürebilir.")
    woop = [
        ("W", ROSE, "Wish · İstek", "Tek, net, senin için zor ama mümkün dilek. 3-6-9 cümlenle aynı olsun."),
        ("O", GOLD, "Outcome · Sonuç", "Olduğunda en güzel an. 30 saniye gözün kapalı yaşa. Göğüste ne açılıyor?"),
        ("O", ROSE, "Obstacle · Engel", "Dış dünya değil, içindeki asıl fren: erteleme, utanç, “hak etmiyorum”, gece telefon."),
        ("P", GOLD, "Plan · Plan", "Eğer [engel belirirse], o zaman [2 dakikalık davranış]. Önceden yaz."),
    ]
    for i, (letter, col, title, body) in enumerate(woop):
        x = 58 + i * 460
        rrect(d, (x, 220, x + 430, 780), WHITE)
        oval(d, (x + 155, 250, x + 275, 370), col)
        text(d, (x + 155, 278), letter, font("bold", 36), WHITE, width=120, align="center")
        text(d, (x + 24, 400), title, font("bold", 22), PLUM, width=382, align="center")
        text(d, (x + 28, 470), body, font("regular", 20), INK, width=374, line_gap=8)
    rrect(d, (58, 810, 1862, 1000), MINT)
    text(d, (90, 835), "Hazır plan örneği", font("bold", 20), GREEN)
    text(
        d,
        (90, 880),
        "Eğer öğleden sonra “nasıl olsa olmaz” diye kaydırırsam, o zaman telefonu başka odaya koyar, 2 dakikalık adımı (mail / arama / dosya / fiyat) hemen bitiririm.",
        font("regular", 22),
        INK,
        width=1720,
        line_gap=8,
    )
    footer(d, 8)
    return img


def slide_week() -> Image.Image:
    img, d = canvas()
    header(d, "Takvim", "7 günlük hız protokolü", "Her gün: 369 + SATS + 1 adım. Tema değişir, sistem değişmez.")
    days = [
        ("1", "Netleş", "Tek istek, 369 cümlesi, SATS sahnesi, WOOP. İlk somut adım bugün atılır."),
        ("2", "Ritim", "Aynı cümle. En küçük görünür hareket: bir mesaj, bir dosya, bir fiyat."),
        ("3", "Hikâye", "8 dakikalık scripting. Bir insanla konuş veya bir kapı çal."),
        ("4", "Engel", "WOOP’u yeniden yaz. Asıl iç freni adlandır. Planı sıkılaştır."),
        ("5", "Kimlik", "Günü bunu zaten yaşayan kişi olarak geçir. Tonun uyumlu olsun."),
        ("6", "Kanıt", "3 küçük işaret not et. Bir büyükçe adım: başvuru, teklif, bitirme."),
        ("7", "Mühürle", "7 günü oku. Cümleyi %10 netleştir. 21 güne kilit at. Kontrolü bırak."),
    ]
    for i, (num, title, body) in enumerate(days):
        x = 50 + i * 266
        bg = WHITE if i % 2 == 0 else LILAC
        rrect(d, (x, 220, x + 248, 1000), bg, 22)
        oval(d, (x + 84, 250, x + 164, 330), ROSE)
        text(d, (x + 84, 268), num, font("bold", 26), WHITE, width=80, align="center")
        text(d, (x + 12, 360), title, font("bold", 22), PLUM, width=224, align="center")
        text(d, (x + 16, 430), body, font("regular", 18), INK, width=216, align="center", line_gap=6)
    footer(d, 9)
    return img


def slide_mistakes() -> Image.Image:
    img, d = canvas()
    header(d, "Engel", "Hızı kesen yedi hata", "Bunları yaparsan teknikler çalışmaz gibi gelir. Çoğu zaman teknik değil, dağınıklık bozar.")
    mistakes = [
        ("Çok dilek", "Aynı hafta para, ilişki, ev, iş. Birini seç."),
        ("Gelecek zaman", "“Olacak” cümlesi isteği sürekli yarına iter."),
        ("Kanıt avı", "Her saat “geldi mi” diye bakmak, yokluk hissini büyütür."),
        ("Başkasını zorlamak", "Birinin seni seçmesini dayatmak. Serbest, karşılıklı hali iste."),
        ("Sadece hayal", "Gündüz sıfır adım. WOOP atlanmış demektir."),
        ("Teknik koleksiyonu", "Her gün yeni yöntem. 7 gün aynı protokol."),
        ("İnanç eşiğini aşmak", "Cümle alay ettiriyorsa küçült. İnanılır gerilim kalsın."),
    ]
    y = 215
    for i, (title, body) in enumerate(mistakes):
        bg = WHITE if i % 2 == 0 else BLUSH
        rrect(d, (58, y, 1862, y + 100), bg, 18)
        text(d, (86, y + 32), title, font("bold", 22), ROSE, width=380)
        text(d, (490, y + 32), body, font("regular", 22), INK, width=1320)
        y += 110
    footer(d, 10)
    return img


def slide_research() -> Image.Image:
    img, d = canvas()
    header(d, "Harita", "Nereleri araştır, nerede takılma", "Önce kısa asıllar. Sonsuz reel değil. 7 gün pratik, sonra okuma.")
    cols = [
        (ROSE, WHITE, "Bu hafta oku (kısa)", "• Neville Goddard — Feeling is the Secret\n  (kısa, SATS’ın kaynağı)\n• Neville — The Power of Awareness\n  (kimlik / varsayım)\n• woopmylife.org — WOOP’u 5 dakikada öğren\n• Gollwitzer: “eğer-o zaman” planları"),
        (PLUM, WHITE, "Sonra, istersen", "• Neville — The Law and the Promise\n• Gabriele Oettingen — Rethinking Positive Thinking\n• James Clear — Atomic Habits\n• r/NevilleGoddard — başarı hikâyesi\n  bağımlılığı yapmadan oku"),
        (GOLD, PLUM, "Şimdilik uzak dur", "• Her gün başka koç, başka “anında zengin ol” videosu\n• 10 tekniği aynı anda karıştıran listeler\n• Başkasının iradesini manipüle etme vaatleri\n• The Secret’i tek kaynak sanmak"),
    ]
    for i, (bg, fg, title, body) in enumerate(cols):
        x = 58 + i * 612
        rrect(d, (x, 220, x + 580, 1000), bg)
        text(d, (x + 36, 260), title, font("bold", 28), fg, width=508)
        text(d, (x + 36, 340), body, font("regular", 22), fg, width=508, line_gap=10)
    footer(d, 11)
    return img


def slide_start() -> Image.Image:
    img, d = canvas()
    header(d, "Bugün", "20 dakikada başla — sonra defteri kapat", "Mükemmel cümle arama. %80 netlik yeter. Hareket cümleyi düzeltir.")
    items = [
        ("0–3 dk", "Tek isteği bir satıra yaz. Süzgeçten geçir."),
        ("3–7 dk", "369 cümlesini yaz. Sesli oku. Vücutta sıkışma varsa yumuşat."),
        ("7–12 dk", "SATS sahnesini 5 saniyeye indir. Kağıda 3 duyusal ayrıntı."),
        ("12–16 dk", "WOOP: istek / sonuç / iç engel / eğer-o zaman."),
        ("16–20 dk", "Bugünün 1 adımını bitir. Sonra akşam 9 yazış + SATS."),
    ]
    y = 215
    for mins, body in items:
        rrect(d, (58, y, 1280, y + 115), WHITE, 20)
        rrect(d, (80, y + 32, 300, y + 84), ROSE, 20)
        text(d, (80, y + 44), mins, font("bold", 18), WHITE, width=220, align="center")
        text(d, (330, y + 38), body, font("regular", 22), INK, width=900)
        y += 130
    rrect(d, (1320, 215, 1862, 1000), PLUM)
    text(d, (1355, 255), "Kilit cümle", font("bold", 26), GOLD, width=460)
    text(
        d,
        (1355, 340),
        "Bir istek.\nAynı cümle.\nAynı sahne.\nHer gün bir adım.\n\n7 gün sonra yeni teknik arama. 21 güne uzat.",
        font("semibold", 26),
        WHITE,
        width=460,
        line_gap=12,
    )
    footer(d, 12)
    return img


SLIDES = [
    ("01-kapak", slide_cover),
    ("02-cerceve", slide_frame),
    ("03-tek-istek", slide_desire),
    ("04-protokol", slide_protocol),
    ("05-369", slide_369),
    ("06-scripting", slide_script),
    ("07-sats", slide_sats),
    ("08-woop", slide_woop),
    ("09-yedi-gun", slide_week),
    ("10-hatalar", slide_mistakes),
    ("11-arastirma", slide_research),
    ("12-bugun-basla", slide_start),
]


def build() -> tuple[Path, list[Path]]:
    PNG_DIR.mkdir(parents=True, exist_ok=True)
    images: list[Image.Image] = []
    paths: list[Path] = []
    for name, fn in SLIDES:
        img = fn()
        path = PNG_DIR / f"{name}.png"
        img.save(path, "PNG", optimize=True)
        images.append(img)
        paths.append(path)
    images[0].save(PDF_PATH, save_all=True, append_images=images[1:], resolution=150)
    return PDF_PATH, paths


if __name__ == "__main__":
    pdf, pngs = build()
    print(pdf)
    for p in pngs:
        print(p)
