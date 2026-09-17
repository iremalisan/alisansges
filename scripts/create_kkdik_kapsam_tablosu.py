#!/usr/bin/env python3
"""KKDİK kapsam kontrol ve eylem Excel tablosunu üretir."""

from __future__ import annotations

import html
import re
from io import BytesIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

OUTPUT_PATH = Path(__file__).resolve().parents[1] / "KKDIK_Kapsam_Kontrol.xlsx"

NAVY = "0C2040"
TEAL = "008C8E"
GOLD = "C9942A"
WHITE = "FFFFFF"
YELLOW = "FFF3BF"
GREEN = "1A8A63"
RED = "C44040"
SKY = "2478C4"
GRAY = "F3F4F6"
INK = "1C2736"
MUTED = "5A687A"
SOFT_RED = "FDECEC"
SOFT_GREEN = "E6F6EE"
SOFT_GOLD = "FFF4E0"
LIGHT_BLUE = "E8F4F7"
RESULT_GRAY = "F7F8FA"

IN_SCOPE = "KAYIT KAPSAMINDA"
EXEMPT = "Kayıt muaf"
NO_REG_DU = "Kayıt yok — alt kullanıcı / dağıtıcı"
NO_REG_OR = "Kayıt yok — tek temsilci sizi kapsar"
NO_REG_TON = "Kayıt yok — 1 ton altı"
NO_REG_ART = "Kayıt yok — eşyada kasıtlı salınım yok"
NOTIFY = "Bildirim (SVHC / eşya)"
CHECK_ROLE = "Rolü kontrol edin"

ROLES = [
    "İmalatçı",
    "İthalatçı",
    "Tek temsilci",
    "Alt kullanıcı",
    "Dağıtıcı",
    "Eşya üreticisi / ithalatçısı",
]
PRODUCT_TYPES = ["Madde", "Karışım", "Eşya"]
UNITS = ["ton", "kg"]
YES_NO = ["Evet", "Hayır"]
EXEMPTIONS = [
    "Yok",
    "Ek-4 madde",
    "Ek-5 muafiyet",
    "Polimer (kendisi)",
    "Atık",
    "Radyoaktif",
    "Transit / serbest bölge",
    "İlaç / gıda / yem amacı",
    "PPORD",
    "Savunma",
    "İzole edilmemiş ara madde",
]

FIRST_DATA_ROW = 11
LAST_DATA_ROW = 60
EXAMPLE_COUNT = 8

# örnek satırlar: (ad, cas, tip, rol, miktar, birim, %, TT, muafiyet, CMR, sucul, salınım, SVHC)
EXAMPLES: list[tuple] = [
    (
        "Stiren (reçine karışımı içinde)",
        "100-42-5",
        "Karışım",
        "İthalatçı",
        12,
        "ton",
        40,
        "Hayır",
        "Yok",
        "Hayır",
        "Hayır",
        "Hayır",
        "Hayır",
    ),
    (
        "Aseton — yurt içi tedarikçi",
        "67-64-1",
        "Madde",
        "Alt kullanıcı",
        20,
        "ton",
        100,
        "Hayır",
        "Yok",
        "Hayır",
        "Hayır",
        "Hayır",
        "Hayır",
    ),
    (
        "Katalizör (yıllık 400 kg ithalat)",
        "—",
        "Madde",
        "İthalatçı",
        400,
        "kg",
        100,
        "Hayır",
        "Yok",
        "Hayır",
        "Hayır",
        "Hayır",
        "Hayır",
    ),
    (
        "Yabancı üretici tek temsilci atadı",
        "108-88-3",
        "Madde",
        "İthalatçı",
        50,
        "ton",
        100,
        "Evet",
        "Yok",
        "Hayır",
        "Hayır",
        "Hayır",
        "Hayır",
    ),
    (
        "CMR 1B hammadde",
        "71-43-2",
        "Madde",
        "İmalatçı",
        2,
        "ton",
        100,
        "Hayır",
        "Yok",
        "Evet",
        "Hayır",
        "Hayır",
        "Hayır",
    ),
    (
        "Sucul Akut 1 boya aktifi",
        "—",
        "Madde",
        "İthalatçı",
        120,
        "ton",
        100,
        "Hayır",
        "Yok",
        "Hayır",
        "Evet",
        "Hayır",
        "Hayır",
    ),
    (
        "CTP boru (eşya, kasıtlı salınım yok)",
        "—",
        "Eşya",
        "Eşya üreticisi / ithalatçısı",
        800,
        "ton",
        100,
        "Hayır",
        "Yok",
        "Hayır",
        "Hayır",
        "Hayır",
        "Hayır",
    ),
    (
        "Ek-5 doğal madde (kayıt muaf)",
        "—",
        "Madde",
        "İthalatçı",
        30,
        "ton",
        100,
        "Hayır",
        "Ek-5 muafiyet",
        "Hayır",
        "Hayır",
        "Hayır",
        "Hayır",
    ),
]


def fill(color: str) -> PatternFill:
    return PatternFill("solid", fgColor=color)


def thin() -> Border:
    side = Side(style="thin", color="D0D5DD")
    return Border(left=side, right=side, top=side, bottom=side)


def apply_common(cell, *, font, fill_color=WHITE, align=None, border=True):
    cell.font = font
    cell.fill = fill(fill_color)
    cell.alignment = align or Alignment(vertical="center", wrap_text=True)
    cell.border = thin() if border else Border()


def substance_tonnage(product_type: str, qty, unit: str, pct) -> float | None:
    if qty in (None, ""):
        return None
    tons = float(qty) / 1000.0 if unit == "kg" else float(qty)
    if product_type == "Karışım":
        tons *= float(pct or 0) / 100.0
    return tons


def full_deadline(tons: float | None, cmr: str, aquatic: str) -> str:
    if tons is None or tons < 1:
        return ""
    if cmr == "Evet":
        return "31.12.2026"
    if aquatic == "Evet" and tons >= 100:
        return "31.12.2026"
    if tons >= 1000:
        return "31.12.2026"
    if tons >= 100:
        return "31.12.2028"
    return "31.12.2030"


def action_text(status: str, deadline: str) -> str:
    if status == IN_SCOPE:
        return (
            "30.09.2026’ya kadar KKS’den geçici kayıt (lider yoksa bireysel + gerekçe). "
            f"Tam kayıt son tarihi {deadline}. KDU ile dosya, harç ve GBF."
        )
    if status == EXEMPT:
        return "Kayıt yok. Muafiyet dayanağını (Ek no) dosyada saklayın. GBF / SEA yükümlülüğü ayrı durabilir."
    if status == NO_REG_DU:
        return "Kayıt tedarikçinindir. Türkçe KKDİK GBF isteyin, kullanıma uyun, izin/kısıtlama kontrol edin."
    if status == NO_REG_OR:
        return "Tek temsilci kaydı sizi kapsamalı. Atama yazısını ve sizin ithalatınızın dahil olduğunu teyit edin."
    if status == NO_REG_TON:
        return "Kayıt eşiği altında. Yıl içinde tonajı izleyin; 1 tona ulaşırsa yükümlülük o anda doğar. GBF devam eder."
    if status == NO_REG_ART:
        return "Eşyada kasıtlı salınım yoksa kayıt yok. SVHC ≥ %0,1 ve ≥1 ton ise bildirim doğabilir."
    if status == NOTIFY:
        return "Eşya içi SVHC bildirimi değerlendirin (Madde 8). Müşteriye güvenli kullanım bilgisini verin."
    if status == CHECK_ROLE:
        return "Rol net değil. Gümrük beyannamesi, fatura ve tek temsilci yazısıyla ithalatçı mısınız bakın."
    return ""


def evaluate_row(
    product_type: str,
    role: str,
    qty,
    unit: str,
    pct,
    or_appointed: str,
    exemption: str,
    cmr: str,
    aquatic: str,
    release: str,
    svhc: str,
) -> dict[str, str | float | None]:
    tons = substance_tonnage(product_type, qty, unit, pct)
    if not role:
        return {"tons": tons, "status": "", "deadline": "", "provisional": "", "action": "", "reason": ""}

    if exemption and exemption != "Yok":
        status = EXEMPT
        reason = f"Muafiyet seçildi: {exemption}."
        return {
            "tons": tons,
            "status": status,
            "deadline": "",
            "provisional": "",
            "action": action_text(status, ""),
            "reason": reason,
        }

    if role in ("Alt kullanıcı", "Dağıtıcı"):
        status = NO_REG_DU
        return {
            "tons": tons,
            "status": status,
            "deadline": "",
            "provisional": "",
            "action": action_text(status, ""),
            "reason": "Yurt içi tedarik / dağıtım rolünde kayıt ettiren siz değilsiniz.",
        }

    if role == "İthalatçı" and or_appointed == "Evet":
        status = NO_REG_OR
        return {
            "tons": tons,
            "status": status,
            "deadline": "",
            "provisional": "",
            "action": action_text(status, ""),
            "reason": "Yabancı üreticinin tek temsilcisi ithalatçı yükümlülüğünü üstlenir.",
        }

    if role == "Eşya üreticisi / ithalatçısı":
        if tons is not None and tons >= 1 and release == "Evet":
            status = IN_SCOPE
            deadline = full_deadline(tons, cmr, aquatic)
            return {
                "tons": tons,
                "status": status,
                "deadline": deadline,
                "provisional": "30.09.2026",
                "action": action_text(status, deadline),
                "reason": "Eşyadan kasıtlı salınım + yıllık ≥1 ton madde.",
            }
        if tons is not None and tons >= 1 and svhc == "Evet":
            status = NOTIFY
            return {
                "tons": tons,
                "status": status,
                "deadline": "",
                "provisional": "",
                "action": action_text(status, ""),
                "reason": "Eşyada SVHC ≥ %0,1 ve madde ≥1 ton — bildirim değerlendirmesi.",
            }
        if tons is not None and tons >= 1:
            status = NO_REG_ART
            return {
                "tons": tons,
                "status": status,
                "deadline": "",
                "provisional": "",
                "action": action_text(status, ""),
                "reason": "Eşya kaydı yalnızca kasıtlı salınım tasarlanmışsa doğar.",
            }
        status = NO_REG_TON
        return {
            "tons": tons,
            "status": status,
            "deadline": "",
            "provisional": "",
            "action": action_text(status, ""),
            "reason": "Madde miktarı yıllık 1 tonun altında.",
        }

    if tons is None:
        return {"tons": None, "status": "", "deadline": "", "provisional": "", "action": "", "reason": ""}

    if tons < 1:
        status = NO_REG_TON
        return {
            "tons": tons,
            "status": status,
            "deadline": "",
            "provisional": "",
            "action": action_text(status, ""),
            "reason": "Kayıt eşiği: kayıt ettiren başına yılda 1 ton.",
        }

    if role in ("İmalatçı", "İthalatçı", "Tek temsilci"):
        status = IN_SCOPE
        deadline = full_deadline(tons, cmr, aquatic)
        reason = "Türkiye’de yerleşik imalatçı / ithalatçı / tek temsilci ve madde ≥1 t/yıl."
        if cmr == "Evet":
            reason += " CMR 1A/1B tam kaydı 31.12.2026’ya çeker."
        elif aquatic == "Evet" and tons >= 100:
            reason += " Sucul Akut/Kronik 1 ve ≥100 t tam kaydı 31.12.2026’ya çeker."
        return {
            "tons": tons,
            "status": status,
            "deadline": deadline,
            "provisional": "30.09.2026",
            "action": action_text(status, deadline),
            "reason": reason,
        }

    status = CHECK_ROLE
    return {
        "tons": tons,
        "status": status,
        "deadline": "",
        "provisional": "",
        "action": action_text(status, ""),
        "reason": "Rol listeden seçilmedi veya beklenmeyen değer.",
    }


def tonnage_formula(row: int) -> str:
    return (
        f'IF(OR(E{row}="",F{row}=""),"",'
        f'IF(F{row}="kg",E{row}/1000,E{row})*IF(C{row}="Karışım",IF(G{row}="",0,G{row}/100),1))'
    )


def status_formula(row: int) -> str:
    p = f"P{row}"
    return (
        f'IF(OR(D{row}="",E{row}=""),"",'
        f'IF(AND(I{row}<>"",I{row}<>"Yok"),"{EXEMPT}",'
        f'IF(OR(D{row}="Alt kullanıcı",D{row}="Dağıtıcı"),"{NO_REG_DU}",'
        f'IF(AND(D{row}="İthalatçı",H{row}="Evet"),"{NO_REG_OR}",'
        f'IF(D{row}="Eşya üreticisi / ithalatçısı",'
        f'IF(AND({p}>=1,L{row}="Evet"),"{IN_SCOPE}",'
        f'IF(AND({p}>=1,M{row}="Evet"),"{NOTIFY}",'
        f'IF({p}>=1,"{NO_REG_ART}","{NO_REG_TON}"))),'
        f'IF({p}<1,"{NO_REG_TON}",'
        f'IF(OR(D{row}="İmalatçı",D{row}="İthalatçı",D{row}="Tek temsilci"),"{IN_SCOPE}","{CHECK_ROLE}")))))))'
    )


def deadline_formula(row: int) -> str:
    p, q = f"P{row}", f"Q{row}"
    return (
        f'IF({q}<>"{IN_SCOPE}","",'
        f'IF(J{row}="Evet","31.12.2026",'
        f'IF(AND(K{row}="Evet",{p}>=100),"31.12.2026",'
        f'IF({p}>=1000,"31.12.2026",'
        f'IF({p}>=100,"31.12.2028","31.12.2030")))))'
    )


def provisional_formula(row: int) -> str:
    return f'IF(Q{row}="{IN_SCOPE}","30.09.2026","")'


def action_formula(row: int) -> str:
    return (
        f'IF(Q{row}="","",'
        f'IF(Q{row}="{IN_SCOPE}",'
        f'"30.09.2026’ya kadar KKS’den geçici kayıt (lider yoksa bireysel + gerekçe). Tam kayıt son tarihi "&R{row}&". KDU ile dosya, harç ve GBF.",'
        f'IF(Q{row}="{EXEMPT}","Kayıt yok. Muafiyet dayanağını (Ek no) dosyada saklayın. GBF / SEA yükümlülüğü ayrı durabilir.",'
        f'IF(Q{row}="{NO_REG_DU}","Kayıt tedarikçinindir. Türkçe KKDİK GBF isteyin, kullanıma uyun, izin/kısıtlama kontrol edin.",'
        f'IF(Q{row}="{NO_REG_OR}","Tek temsilci kaydı sizi kapsamalı. Atama yazısını ve sizin ithalatınızın dahil olduğunu teyit edin.",'
        f'IF(Q{row}="{NO_REG_TON}","Kayıt eşiği altında. Yıl içinde tonajı izleyin; 1 tona ulaşırsa yükümlülük o anda doğar. GBF devam eder.",'
        f'IF(Q{row}="{NO_REG_ART}","Eşyada kasıtlı salınım yoksa kayıt yok. SVHC ≥ %0,1 ve ≥1 ton ise bildirim doğabilir.",'
        f'IF(Q{row}="{NOTIFY}","Eşya içi SVHC bildirimi değerlendirin (Madde 8). Müşteriye güvenli kullanım bilgisini verin.",'
        f'"Rol net değil. Gümrük beyannamesi, fatura ve tek temsilci yazısıyla ithalatçı mısınız bakın."))))))))'
    )


def reason_formula(row: int) -> str:
    p, q = f"P{row}", f"Q{row}"
    return (
        f'IF({q}="","",'
        f'IF({q}="{EXEMPT}","Muafiyet seçildi: "&I{row}&".",'
        f'IF({q}="{NO_REG_DU}","Yurt içi tedarik / dağıtım rolünde kayıt ettiren siz değilsiniz.",'
        f'IF({q}="{NO_REG_OR}","Yabancı üreticinin tek temsilcisi ithalatçı yükümlülüğünü üstlenir.",'
        f'IF({q}="{NO_REG_ART}","Eşya kaydı yalnızca kasıtlı salınım tasarlanmışsa doğar.",'
        f'IF({q}="{NOTIFY}","Eşyada SVHC ≥ %0,1 ve madde ≥1 ton — bildirim değerlendirmesi.",'
        f'IF({q}="{NO_REG_TON}","Kayıt eşiği: kayıt ettiren başına yılda 1 ton.",'
        f'IF({q}="{IN_SCOPE}",'
        f'IF(J{row}="Evet","Türkiye’de yerleşik kayıt ettiren, madde ≥1 t/yıl. CMR 1A/1B tam kaydı 31.12.2026’ya çeker.",'
        f'IF(AND(K{row}="Evet",{p}>=100),"Türkiye’de yerleşik kayıt ettiren, madde ≥1 t/yıl. Sucul Akut/Kronik 1 ve ≥100 t tam kaydı 31.12.2026’ya çeker.",'
        f'"Türkiye’de yerleşik imalatçı / ithalatçı / tek temsilci ve madde ≥1 t/yıl.")),'
        f'"Rol listeden seçilmedi veya beklenmeyen değer.")))))))))'
    )


def build_help_sheet(wb: Workbook) -> None:
    ws = wb.create_sheet("Nasıl Kullanılır")
    ws.sheet_properties.tabColor = GOLD
    ws.column_dimensions["A"].width = 118
    title = ws["A1"]
    title.value = "KKDİK Yönetmeliği — Kapsam Kontrol Tablosu Kullanım Kılavuzu"
    apply_common(
        title,
        font=Font(name="Calibri", size=16, bold=True, color=WHITE),
        fill_color=NAVY,
        align=Alignment(vertical="center", wrap_text=True),
        border=False,
    )
    ws.row_dimensions[1].height = 36
    blocks = [
        (
            "Ne işe yarar?",
            "Her kimyasal satırı için rolünüzü, tonajı ve muafiyeti yazın. Tablo madde tonajını hesaplar; "
            "kayıt kapsamını, 30.09.2026 geçici kayıt ihtiyacını, tam kayıt son tarihini (2026 / 2028 / 2030) "
            "ve yapılacak işi otomatik doldurur.",
        ),
        (
            "Nasıl doldurulur?",
            "Yalnızca sarı hücrelere yazın. Açılır listeler: ürün tipi, rol, birim, tek temsilci, muafiyet, CMR, sucul, salınım, SVHC.\n"
            "Karışımda “Madde %” alanına GBF bölüm 3’teki oranı yazın. Aynı CAS’ı birden fazla tedarikçiden alıyorsanız satırları toplayın veya tek satırda birleştirin.",
        ),
        (
            "Kayıt kuralı",
            "Kayıt ettiren = Türkiye’de yerleşik imalatçı, ithalatçı veya tek temsilci + madde kendi halinde veya karışımda ≥1 t/yıl + muafiyet yok.\n"
            "Tedarikçinizin kaydı sizin ithalat kaydınızın yerine geçmez. Tek temsilci ataması sizi kapsıyorsa ithalatçı alt kullanıcı konumuna geçer.",
        ),
        (
            "Renkler",
            "Kırmızı = KAYIT KAPSAMINDA (30.09.2026 geçici kayıt).\n"
            "Yeşil = kayıt yok / muaf / alt kullanıcı.\n"
            "Lacivert = eşya SVHC bildirimi.",
        ),
        (
            "Kaynak",
            "KKDİK Yönetmeliği RG 23.06.2017/30105 Mükerrer; değişiklik RG 23.12.2023/32408; "
            "Usul ve Esaslar 05.08.2025 (13216050). Sistem: KKS / EÇBS. İletişim: kimyasallar@csb.gov.tr\n"
            "Bu tablo genel tarama aracıdır; resmi karar ve başvuru KKS üzerinden, KDU ile yapılır.",
        ),
    ]
    row = 3
    for heading, body in blocks:
        h = ws.cell(row, 1, heading)
        apply_common(h, font=Font(name="Calibri", size=12, bold=True, color=NAVY), fill_color=LIGHT_BLUE, border=False)
        ws.row_dimensions[row].height = 22
        row += 1
        b = ws.cell(row, 1, body)
        apply_common(
            b,
            font=Font(name="Calibri", size=11, color=INK),
            fill_color=WHITE,
            align=Alignment(vertical="top", wrap_text=True),
            border=False,
        )
        ws.row_dimensions[row].height = 88
        row += 2
    ws.sheet_view.showGridLines = False


def build_process_sheet(wb: Workbook) -> None:
    ws = wb.create_sheet("Sistem ve Takvim")
    ws.sheet_properties.tabColor = TEAL
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 22
    ws.column_dimensions["B"].width = 38
    ws.column_dimensions["C"].width = 62
    ws.merge_cells("A1:C1")
    title = ws["A1"]
    title.value = "KKDİK  •  Sistem nasıl ilerler ve son tarihler"
    apply_common(
        title,
        font=Font(name="Calibri", size=16, bold=True, color=WHITE),
        fill_color=NAVY,
        align=Alignment(vertical="center"),
        border=False,
    )
    ws.row_dimensions[1].height = 32
    headers = ["Adım", "Ne", "Nasıl"]
    for col, header in enumerate(headers, 1):
        cell = ws.cell(3, col, header)
        apply_common(cell, font=Font(name="Calibri", size=11, bold=True, color=WHITE), fill_color=TEAL)
    steps = [
        ("1. Envanter", "CAS / EC, GBF, yıllık miktar", "Karışımı maddeye çevirin. Aynı CAS’ı toplayın."),
        ("2. EÇBS / KKS", "Bakanlık sistemi", "Yetkili kişi + KDU. kimyasallar.csb.gov.tr"),
        ("3. Ön-MBDF", "Madde Bilgisi Değişim Forumu", "Aynı maddeyi kaydedeceklerle veri paylaşımı."),
        ("4. Lider / üye", "Tek madde tek kayıt", "Ortak kayıt esastır. Ayrı dosya için yazılı gerekçe."),
        ("5. Geçici kayıt", "30.09.2026", "Üye veya gerekçeli bireysel. Harç + KKS ödeme teyidi."),
        ("6. Tam kayıt", "2026 / 2028 / 2030", "Ek-7…10, ≥10 t ise KGR. Veri yoksa en fazla +2 yıl ek süre."),
        ("7. GBF ve izleme", "Tedarik zinciri", "16 bölümlü Türkçe GBF, güncelleme, izin (Ek-14) ve kısıtlama (Ek-17)."),
    ]
    for i, row_vals in enumerate(steps, start=4):
        bg = WHITE if i % 2 else GRAY
        for col, value in enumerate(row_vals, 1):
            cell = ws.cell(i, col, value)
            apply_common(cell, font=Font(name="Calibri", size=11, bold=(col == 1), color=INK), fill_color=bg)
        ws.row_dimensions[i].height = 36
    ws.merge_cells("A12:C12")
    ws["A12"].value = "Tam kayıt son tarihleri (RG 23.12.2023/32408)"
    apply_common(ws["A12"], font=Font(name="Calibri", size=12, bold=True, color=WHITE), fill_color=NAVY, border=False)
    deadlines = [
        ("31.12.2026", "≥1.000 t/yıl; CMR kat. 1A/1B (≥1 t); Sucul Akut 1 / Kronik 1 ≥100 t (H400, H410)"),
        ("31.12.2028", "≥100 t/yıl (yukarıdaki özel zararlılık ölçütü olmayan maddeler)"),
        ("31.12.2030", "≥1 t/yıl (1–100 ton bandındaki standart maddeler)"),
        ("30.09.2026", "Geçici kayıt — tonajdan bağımsız, kayıt kapsamındaki her madde"),
    ]
    ws.cell(13, 1, "Tarih")
    ws.cell(13, 2, "Kimler")
    ws.merge_cells("B13:C13")
    for col in (1, 2, 3):
        apply_common(ws.cell(13, col), font=Font(name="Calibri", size=11, bold=True, color=WHITE), fill_color=TEAL)
    for i, (date, who) in enumerate(deadlines, start=14):
        ws.cell(i, 1, date)
        ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=3)
        ws.cell(i, 2, who)
        bg = SOFT_GOLD if "2026" in date and "09" in date else (WHITE if i % 2 else GRAY)
        apply_common(ws.cell(i, 1), font=Font(name="Calibri", size=11, bold=True, color=NAVY), fill_color=bg)
        apply_common(ws.cell(i, 2), font=Font(name="Calibri", size=11, color=INK), fill_color=bg)
        apply_common(ws.cell(i, 3), font=Font(name="Calibri", size=11, color=INK), fill_color=bg)
        ws.row_dimensions[i].height = 32


def build_roles_sheet(wb: Workbook) -> None:
    ws = wb.create_sheet("Rolüne Göre Ne Yapmalı")
    ws.sheet_properties.tabColor = SKY
    ws.sheet_view.showGridLines = False
    widths = [28, 42, 55]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.merge_cells("A1:C1")
    ws["A1"].value = "Rolünüze göre yapılacaklar"
    apply_common(
        ws["A1"],
        font=Font(name="Calibri", size=16, bold=True, color=WHITE),
        fill_color=NAVY,
        align=Alignment(vertical="center"),
        border=False,
    )
    ws.row_dimensions[1].height = 32
    headers = ["Rol", "Kapsama girer misiniz?", "Kapsamdaysanız / değilseniz ne yapmalısınız"]
    for col, header in enumerate(headers, 1):
        apply_common(ws.cell(3, col, header), font=Font(name="Calibri", size=11, bold=True, color=WHITE), fill_color=TEAL)
    rows = [
        (
            "İmalatçı",
            "Türkiye’de madde ≥1 t/yıl üretiliyorsa evet (muaf değilse).",
            "KKS envanteri, ön-MBDF, 30.09.2026 geçici kayıt, tonaj bandına göre tam kayıt, GBF, KDU.",
        ),
        (
            "İthalatçı",
            "Kendi adına ithal ≥1 t/yıl ve tek temsilci yoksa evet.",
            "Gümrük + GBF + CAS listesi. TT yazısı yoksa kayıt sizin. Karışımı bileşen tonajına çevirin.",
        ),
        (
            "Tek temsilci",
            "Yabancı üretici sizi atadıysa ithalatçı yükümlülüğü sizde.",
            "Kapsanan ithalatçıları ve tonajı tutun. Kayıt + GBF. Atama kapsamı dışındaki ithalatçı ayrı kaydeder.",
        ),
        (
            "Alt kullanıcı",
            "Kayıt hayır (yurt içi alım). Kullanım ve GBF evet.",
            "Tedarikçiden kayıt/geçici kayıt no ve Türkçe GBF. Kullanım senaryosuna uyun. İthalata geçerseniz rol değişir.",
        ),
        (
            "Dağıtıcı",
            "Kayıt hayır; bilgi aktarma evet.",
            "GBF ve etiket zincirini koparmayın. Yeniden ambalaj SEA’ya uygun olsun.",
        ),
        (
            "Eşya üreticisi / ithalatçısı",
            "Kasıtlı salınım + ≥1 t ise kayıt. SVHC ≥ %0,1 + ≥1 t ise bildirim.",
            "CTP/plastik eşyada monomer ve katkıları ayrı kontrol edin. Polimer kayıt dışı olsa da stiren kayıtlı olabilir.",
        ),
    ]
    for i, vals in enumerate(rows, start=4):
        bg = WHITE if i % 2 else GRAY
        for col, value in enumerate(vals, 1):
            apply_common(
                ws.cell(i, col, value),
                font=Font(name="Calibri", size=11, bold=(col == 1), color=INK),
                fill_color=bg,
            )
        ws.row_dimensions[i].height = 52


def build_exemption_sheet(wb: Workbook) -> None:
    ws = wb.create_sheet("Muafiyetler")
    ws.sheet_properties.tabColor = GREEN
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 36
    ws.column_dimensions["B"].width = 80
    ws.merge_cells("A1:B1")
    ws["A1"].value = "Sık karşılaşılan kapsam dışı / kayıt muaf durumlar"
    apply_common(
        ws["A1"],
        font=Font(name="Calibri", size=16, bold=True, color=WHITE),
        fill_color=NAVY,
        align=Alignment(vertical="center"),
        border=False,
    )
    ws.row_dimensions[1].height = 32
    for col, header in enumerate(("Durum", "Not"), 1):
        apply_common(ws.cell(3, col, header), font=Font(name="Calibri", size=11, bold=True, color=WHITE), fill_color=TEAL)
    for idx, name in enumerate(EXEMPTIONS, start=4):
        ws.cell(idx, 4, name)
        ws.cell(idx, 4).number_format = "@"
    ws.column_dimensions["D"].hidden = True

    items = [
        ("< 1 ton / yıl / kayıt ettiren", "Kayıt doğmaz. GBF, sınıflandırma ve etiket durur. Tonaj yıl içinde eşiği aşabilir."),
        ("Alt kullanıcı (yurt içi alım)", "Kayıt tedarikçide. Siz kullanım ve GBF yükümlüsüsünüz."),
        ("Tek temsilci kapsamı", "Atama sizin ithalatınızı kapsıyorsa kayıt TT’de. Yazıyı dosyada saklayın."),
        ("Ek-4 maddeler", "Yönetmelik ek listesindeki maddeler kayıttan muaf."),
        ("Ek-5 muafiyetler", "Belirli doğal maddeler, yan ürünler vb. Koşulları tek tek okuyun."),
        ("Polimerin kendisi", "Polimer kayıt yükümlülüğünden muaftır. %2+ monomer ve diğer bağlı maddeler ≥1 t ise onlar kayıtlıdır."),
        ("Atık", "Atık mevzuatındaki malzeme KKDİK maddesi değildir."),
        ("Radyoaktif / transit / savunma", "Yönetmelik kapsamı dışıdır (koşullu)."),
        ("İlaç, gıda, yem amacı", "Kayıt / alt kullanıcı / değerlendirme / izin kısımlarından kısmi muafiyet. GBF kısmı ayrı."),
        ("PPORD", "Ürün ve süreç odaklı Ar-Ge için bildirim; tam kayıt yerine geçmez."),
        ("Eşya, kasıtlı salınım yok", "Madde kaydı yok. SVHC bildirimi ayrıca bakılır."),
    ]
    for i, (a, b) in enumerate(items, start=4):
        bg = WHITE if i % 2 else GRAY
        apply_common(ws.cell(i, 1, a), font=Font(name="Calibri", size=11, bold=True, color=NAVY), fill_color=bg)
        apply_common(ws.cell(i, 2, b), font=Font(name="Calibri", size=11, color=INK), fill_color=bg)
        ws.row_dimensions[i].height = 36


def add_dropdown(ws, cell_range: str, options: list[str], title: str, prompt: str) -> None:
    formula = '"' + ",".join(options) + '"'
    dv = DataValidation(
        type="list",
        formula1=formula,
        allow_blank=True,
        showDropDown=False,
        showErrorMessage=False,
        showInputMessage=True,
        promptTitle=title,
        prompt=prompt,
    )
    dv.add(cell_range)
    ws.add_data_validation(dv)


def build_inventory_sheet(wb: Workbook) -> None:
    ws = wb.create_sheet("Madde Envanteri", 0)
    ws.sheet_properties.tabColor = RED
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "A11"

    widths = {
        "A": 38,
        "B": 14,
        "C": 14,
        "D": 28,
        "E": 12,
        "F": 10,
        "G": 12,
        "H": 14,
        "I": 22,
        "J": 12,
        "K": 14,
        "L": 16,
        "M": 12,
        "N": 14,
        "O": 14,
        "P": 14,
        "Q": 36,
        "R": 16,
        "S": 16,
        "T": 55,
        "U": 48,
    }
    for col, width in widths.items():
        ws.column_dimensions[col].width = width

    ws.merge_cells("A1:U2")
    title = ws["A1"]
    title.value = "KKDİK YÖNETMELİĞİ  •  MADDE KAPSAM KONTROLÜ VE YAPILACAKLAR"
    apply_common(
        title,
        font=Font(name="Calibri", size=20, bold=True, color=WHITE),
        fill_color=NAVY,
        align=Alignment(horizontal="center", vertical="center"),
        border=False,
    )
    for col in range(1, 22):
        for r in (1, 2):
            ws.cell(r, col).fill = fill(NAVY)
            ws.cell(r, col).border = Border()
    ws.row_dimensions[1].height = 28
    ws.row_dimensions[2].height = 18

    ws.merge_cells("A3:U3")
    ws["A3"].value = (
        "Sarı hücreleri doldurun. Kayıt = TR yerleşik imalatçı / ithalatçı / tek temsilci + madde ≥1 t/yıl + muafiyet yok.  "
        "Geçici kayıt son tarihi 30.09.2026  •  Tam kayıt 31.12.2026 / 2028 / 2030"
    )
    apply_common(
        ws["A3"],
        font=Font(name="Calibri", size=10, italic=True, color=NAVY),
        fill_color=LIGHT_BLUE,
        align=Alignment(vertical="center", wrap_text=True),
        border=False,
    )
    for col in range(1, 22):
        ws.cell(3, col).fill = fill(LIGHT_BLUE)
        ws.cell(3, col).border = Border()
    ws.row_dimensions[3].height = 22

    labels = [
        (5, "Kayıt kapsamındaki satır", f'=COUNTIF(Q{FIRST_DATA_ROW}:Q{LAST_DATA_ROW},"{IN_SCOPE}")'),
        (8, "Geçici kayıt (30.09.2026) gereken", f'=COUNTIF(S{FIRST_DATA_ROW}:S{LAST_DATA_ROW},"30.09.2026")'),
        (11, "Kayıt yok / muaf / alt kullanıcı", f'=COUNTA(Q{FIRST_DATA_ROW}:Q{LAST_DATA_ROW})-C5'),
        (14, "2026 tam kayıt bandı", f'=COUNTIF(R{FIRST_DATA_ROW}:R{LAST_DATA_ROW},"31.12.2026")'),
        (17, "2028 bandı", f'=COUNTIF(R{FIRST_DATA_ROW}:R{LAST_DATA_ROW},"31.12.2028")'),
        (20, "2030 bandı", f'=COUNTIF(R{FIRST_DATA_ROW}:R{LAST_DATA_ROW},"31.12.2030")'),
    ]
    for col, label, formula in labels:
        head = ws.cell(4, col, label)
        apply_common(
            head,
            font=Font(name="Calibri", size=9, bold=True, color=WHITE),
            fill_color=TEAL,
            align=Alignment(horizontal="center", vertical="center", wrap_text=True),
        )
        ws.merge_cells(start_row=4, start_column=col, end_row=4, end_column=col + 1)
        apply_common(ws.cell(4, col + 1), font=Font(name="Calibri", size=9, color=WHITE), fill_color=TEAL, border=False)
        val = ws.cell(5, col, formula)
        apply_common(
            val,
            font=Font(name="Calibri", size=16, bold=True, color=NAVY),
            fill_color=WHITE,
            align=Alignment(horizontal="center", vertical="center"),
        )
        ws.merge_cells(start_row=5, start_column=col, end_row=6, end_column=col + 1)
        apply_common(ws.cell(6, col), font=Font(name="Calibri", size=16, color=NAVY), fill_color=WHITE, border=False)
        apply_common(ws.cell(5, col + 1), font=Font(name="Calibri", size=16, color=NAVY), fill_color=WHITE, border=False)
        apply_common(ws.cell(6, col + 1), font=Font(name="Calibri", size=16, color=NAVY), fill_color=WHITE, border=False)
    ws.row_dimensions[4].height = 32
    ws.row_dimensions[5].height = 22
    ws.row_dimensions[6].height = 18

    ws.merge_cells("A8:U8")
    ws["A8"].value = (
        "İlk 8 satır örnek senaryodur; kendi maddelerinizle değiştirin. Formül sütunlarını (P–U) silmeyin. "
        "Kaynak: KKDİK RG 30105 Mükerrer, değişiklik 32408, Usul ve Esaslar 05.08.2025."
    )
    apply_common(
        ws["A8"],
        font=Font(name="Calibri", size=10, color=MUTED),
        fill_color=GRAY,
        align=Alignment(vertical="center"),
        border=False,
    )
    for col in range(1, 22):
        ws.cell(8, col).fill = fill(GRAY)
        ws.cell(8, col).border = Border()

    group_headers = [
        (1, 13, "GİRDİ (sarı)", TEAL),
        (14, 3, "HESAP", NAVY),
        (17, 5, "SONUÇ — KAPSAM VE YAPILACAK", GOLD),
    ]
    for start, span, text, color in group_headers:
        ws.merge_cells(start_row=9, start_column=start, end_row=9, end_column=start + span - 1)
        cell = ws.cell(9, start, text)
        apply_common(
            cell,
            font=Font(name="Calibri", size=10, bold=True, color=WHITE),
            fill_color=color,
            align=Alignment(horizontal="center"),
        )
        for extra in range(start + 1, start + span):
            ws.cell(9, extra).fill = fill(color)
            ws.cell(9, extra).font = Font(name="Calibri", size=10, color=WHITE)
            ws.cell(9, extra).border = thin()

    headers = [
        "Madde / ürün adı",
        "CAS",
        "Ürün tipi",
        "Rolünüz",
        "Yıllık miktar",
        "Birim",
        "Madde %",
        "Tek temsilci?",
        "Muafiyet",
        "CMR 1A/1B?",
        "Sucul A1/K1?",
        "Kasıtlı salınım?",
        "SVHC ≥%0,1 eşya?",
        "Madde t/yıl",
        "Kayıt durumu",
        "Tam kayıt son tarihi",
        "Geçici kayıt",
        "Ne yapmalısınız",
        "Gerekçe",
    ]
    # columns A-U but we skip some? Wait headers should match 21 columns A-U.
    # A-M inputs (13), N-P wait I planned P as tonnage.
    # Let me map:
    # A name, B CAS, C type, D role, E qty, F unit, G %, H OR, I exemption, J CMR, K aquatic, L release, M SVHC
    # P tons... I had N and O unused in formula. Looking at widths I had N, O as extra.
    # I need to fix: formulas use C, D, E, F, G, H, I, J, K, L, M, P, Q, R, S
    # So columns N and O are unused in my formula. Let me use N and O as unused/hidden OR remap.
    #
    # Looking at status_formula: C type, D role, E qty, F unit, G %, H OR, I exemption, J CMR, K aquatic, L release, M SVHC, P tons, Q status, R deadline, S provisional, T action, U reason
    #
    # I had N and O in widths as extra. I'll put "—" placeholders or use them as notes.
    # Better: headers list should be 21 items A-U. Insert two columns N, O as "Not (isteğe bağlı)" and "Tedarikçi".
    headers = [
        "Madde / ürün adı",
        "CAS",
        "Ürün tipi",
        "Rolünüz",
        "Yıllık miktar",
        "Birim",
        "Madde %",
        "Tek temsilci?",
        "Muafiyet",
        "CMR 1A/1B?",
        "Sucul A1/K1?",
        "Kasıtlı salınım?",
        "SVHC ≥%0,1 eşya?",
        "Tedarikçi (isteğe bağlı)",
        "Not",
        "Madde t/yıl",
        "Kayıt durumu",
        "Tam kayıt son tarihi",
        "Geçici kayıt",
        "Ne yapmalısınız",
        "Gerekçe",
    ]
    assert len(headers) == 21
    for col, header in enumerate(headers, 1):
        cell = ws.cell(10, col, header)
        apply_common(
            cell,
            font=Font(name="Calibri", size=10, bold=True, color=WHITE),
            fill_color=NAVY,
            align=Alignment(horizontal="center", vertical="center", wrap_text=True),
        )
    ws.row_dimensions[10].height = 36
    ws.auto_filter.ref = f"A10:U{LAST_DATA_ROW}"

    example_results: list[dict] = []
    for idx, row in enumerate(range(FIRST_DATA_ROW, LAST_DATA_ROW + 1)):
        example = EXAMPLES[idx] if idx < len(EXAMPLES) else None
        if example:
            name, cas, ptype, role, qty, unit, pct, or_app, exempt, cmr, aquatic, release, svhc = example
        else:
            name = cas = ptype = role = unit = or_app = exempt = cmr = aquatic = release = svhc = ""
            qty = pct = None

        values = {
            1: name,
            2: cas,
            3: ptype,
            4: role,
            5: qty,
            6: unit,
            7: pct if ptype == "Karışım" or (example and pct != 100) else (100 if example else None),
            8: or_app,
            9: exempt,
            10: cmr,
            11: aquatic,
            12: release,
            13: svhc,
            14: "",
            15: "",
        }
        for col, value in values.items():
            cell = ws.cell(row, col, value if value != "" else None)
            is_input = col <= 13
            apply_common(
                cell,
                font=Font(name="Calibri", size=10, color=INK),
                fill_color=YELLOW if is_input else RESULT_GRAY,
                align=Alignment(
                    horizontal="center" if col >= 3 else "left",
                    vertical="center",
                    wrap_text=True,
                ),
            )
            if col == 2:
                cell.number_format = "@"
            if col in (5, 7):
                cell.number_format = "0.00"

        ws.cell(row, 16, f"={tonnage_formula(row)}")
        ws.cell(row, 17, f"={status_formula(row)}")
        ws.cell(row, 18, f"={deadline_formula(row)}")
        ws.cell(row, 19, f"={provisional_formula(row)}")
        ws.cell(row, 20, f"={action_formula(row)}")
        ws.cell(row, 21, f"={reason_formula(row)}")

        result = (
            evaluate_row(ptype, role, qty, unit, pct, or_app, exempt, cmr, aquatic, release, svhc)
            if example
            else {"tons": None, "status": "", "deadline": "", "provisional": "", "action": "", "reason": ""}
        )
        example_results.append(result)

        for col in range(16, 22):
            cell = ws.cell(row, col)
            apply_common(
                cell,
                font=Font(name="Calibri", size=10, bold=(col == 17), color=INK),
                fill_color=WHITE if row % 2 else RESULT_GRAY,
                align=Alignment(horizontal="center" if col in (16, 18, 19) else "left", vertical="center", wrap_text=True),
            )
        if result["status"] == IN_SCOPE:
            ws.cell(row, 17).fill = fill(RED)
            ws.cell(row, 17).font = Font(name="Calibri", size=10, bold=True, color=WHITE)
        elif result["status"] == NOTIFY:
            ws.cell(row, 17).fill = fill(NAVY)
            ws.cell(row, 17).font = Font(name="Calibri", size=10, bold=True, color=WHITE)
        elif result["status"]:
            ws.cell(row, 17).fill = fill(GREEN)
            ws.cell(row, 17).font = Font(name="Calibri", size=10, bold=True, color=WHITE)
        if result["tons"] is not None:
            ws.cell(row, 16).number_format = "0.00"
        ws.row_dimensions[row].height = 48 if example else 28

    ws.conditional_formatting.add(
        f"Q{FIRST_DATA_ROW}:Q{LAST_DATA_ROW}",
        CellIsRule(
            operator="equal",
            formula=[f'"{IN_SCOPE}"'],
            fill=fill(RED),
            font=Font(name="Calibri", size=10, bold=True, color=WHITE),
        ),
    )
    ws.conditional_formatting.add(
        f"Q{FIRST_DATA_ROW}:Q{LAST_DATA_ROW}",
        CellIsRule(
            operator="equal",
            formula=[f'"{NOTIFY}"'],
            fill=fill(NAVY),
            font=Font(name="Calibri", size=10, bold=True, color=WHITE),
        ),
    )
    for status in (EXEMPT, NO_REG_DU, NO_REG_OR, NO_REG_TON, NO_REG_ART, CHECK_ROLE):
        ws.conditional_formatting.add(
            f"Q{FIRST_DATA_ROW}:Q{LAST_DATA_ROW}",
            CellIsRule(
                operator="equal",
                formula=[f'"{status}"'],
                fill=fill(GREEN),
                font=Font(name="Calibri", size=10, bold=True, color=WHITE),
            ),
        )
    ws.conditional_formatting.add(
        f"S{FIRST_DATA_ROW}:S{LAST_DATA_ROW}",
        CellIsRule(
            operator="equal",
            formula=['"30.09.2026"'],
            fill=fill(SOFT_GOLD),
            font=Font(name="Calibri", size=10, bold=True, color=NAVY),
        ),
    )

    add_dropdown(ws, f"C{FIRST_DATA_ROW}:C{LAST_DATA_ROW}", PRODUCT_TYPES, "Ürün tipi", "Madde, karışım veya eşya.")
    add_dropdown(ws, f"D{FIRST_DATA_ROW}:D{LAST_DATA_ROW}", ROLES, "Rol", "Tedarik zincirindeki konumunuz.")
    add_dropdown(ws, f"F{FIRST_DATA_ROW}:F{LAST_DATA_ROW}", UNITS, "Birim", "Yıllık miktarın birimi.")
    add_dropdown(ws, f"H{FIRST_DATA_ROW}:H{LAST_DATA_ROW}", YES_NO, "Tek temsilci", "Yabancı üretici sizi kapsayan TT atadı mı?")
    muaf_dv = DataValidation(
        type="list",
        formula1=f"='Muafiyetler'!$D$4:$D${3 + len(EXEMPTIONS)}",
        allow_blank=True,
        showDropDown=False,
        showErrorMessage=False,
        showInputMessage=True,
        promptTitle="Muafiyet",
        prompt="Yok ise kayıt kuralları işler.",
    )
    muaf_dv.add(f"I{FIRST_DATA_ROW}:I{LAST_DATA_ROW}")
    ws.add_data_validation(muaf_dv)
    for col, title in (("J", "CMR"), ("K", "Sucul"), ("L", "Salınım"), ("M", "SVHC")):
        add_dropdown(ws, f"{col}{FIRST_DATA_ROW}:{col}{LAST_DATA_ROW}", YES_NO, title, "GBF / SEA bilgisine göre.")

    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.page_setup.paperSize = ws.PAPERSIZE_A3
    ws.print_title_rows = "1:10"
    ws.oddHeader.left.text = "KKDİK madde kapsam kontrolü"
    ws.sheet_view.zoomScale = 100
    ws.sheet_view.tabSelected = True

    # cache summary counts in rows 5 using python
    in_scope_n = sum(1 for r in example_results if r["status"] == IN_SCOPE)
    prov_n = sum(1 for r in example_results if r["provisional"] == "30.09.2026")
    filled = sum(1 for r in example_results if r["status"])
    d2026 = sum(1 for r in example_results if r["deadline"] == "31.12.2026")
    d2028 = sum(1 for r in example_results if r["deadline"] == "31.12.2028")
    d2030 = sum(1 for r in example_results if r["deadline"] == "31.12.2030")
    ws._kkdik_cache = {
        "E5": in_scope_n,
        "H5": prov_n,
        "K5": filled - in_scope_n,
        "N5": d2026,
        "Q5": d2028,
        "T5": d2030,
        "rows": example_results,
    }


def create_workbook(path: Path = OUTPUT_PATH) -> Path:
    wb = Workbook()
    default = wb.active
    wb.remove(default)
    build_inventory_sheet(wb)
    build_roles_sheet(wb)
    build_process_sheet(wb)
    build_exemption_sheet(wb)
    build_help_sheet(wb)
    wb.properties.title = "KKDİK Kapsam Kontrolü"
    wb.properties.creator = "KKDİK Rehberi"
    wb.properties.subject = "Kimler kapsama girer, sistem nasıl ilerler, ne yapılmalı"
    wb.active = wb["Madde Envanteri"]
    path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)
    _make_excel_compatible(path, wb["Madde Envanteri"]._kkdik_cache)
    return path


def _make_excel_compatible(path: Path, cache: dict) -> None:
    with ZipFile(path, "r") as src:
        parts = {name: src.read(name) for name in src.namelist()}

    workbook = parts["xl/workbook.xml"].decode("utf-8")
    workbook = workbook.replace("<workbookProtection />", "").replace("<workbookProtection/>", "")
    workbook = re.sub(
        r"<calcPr[^/]*/>",
        '<calcPr calcMode="auto" calcId="0" fullCalcOnLoad="1"/>',
        workbook,
    )
    parts["xl/workbook.xml"] = workbook.encode("utf-8")

    for name, data in list(parts.items()):
        if not (name.startswith("xl/worksheets/sheet") and name.endswith(".xml")):
            continue
        text = data.decode("utf-8")
        if "<sheetProtection" in text:
            start = text.index("<sheetProtection")
            end = text.index("/>", start) + 2
            text = text[:start] + text[end:]
        text = text.replace("<v />", "").replace("<v/>", "")
        if name.endswith("sheet1.xml"):
            text = _inject_inventory_cache(text, cache)
        parts[name] = text.encode("utf-8")

    buffer = BytesIO()
    with ZipFile(buffer, "w", ZIP_DEFLATED) as dest:
        for name, data in parts.items():
            dest.writestr(name, data)
    path.write_bytes(buffer.getvalue())


def _inject_inventory_cache(xml: str, cache: dict) -> str:
    for ref, value in cache.items():
        if ref == "rows":
            continue
        xml = _set_formula_cache(xml, ref, value, as_str=False)
    for idx, result in enumerate(cache["rows"]):
        row = FIRST_DATA_ROW + idx
        if result["tons"] is not None:
            xml = _set_formula_cache(xml, f"P{row}", f"{result['tons']:.4f}", as_str=False)
        if result["status"]:
            xml = _set_formula_cache(xml, f"Q{row}", result["status"], as_str=True)
        if result["deadline"]:
            xml = _set_formula_cache(xml, f"R{row}", result["deadline"], as_str=True)
        if result["provisional"]:
            xml = _set_formula_cache(xml, f"S{row}", result["provisional"], as_str=True)
        if result["action"]:
            xml = _set_formula_cache(xml, f"T{row}", result["action"], as_str=True)
        if result["reason"]:
            xml = _set_formula_cache(xml, f"U{row}", result["reason"], as_str=True)
    return xml


def _set_formula_cache(xml: str, ref: str, value: object, *, as_str: bool) -> str:
    pattern = re.compile(rf'<c r="{ref}"[^>]*>.*?</c>')
    match = pattern.search(xml)
    if not match or value in (None, ""):
        return xml
    formula = re.search(r"<f>.*?</f>", match.group(0))
    if not formula:
        return xml
    style = re.search(r' s="(\d+)"', match.group(0))
    style_attr = f' s="{style.group(1)}"' if style else ""
    type_attr = ' t="str"' if as_str else ""
    cached = html.escape(str(value), quote=False)
    new_cell = f'<c r="{ref}"{style_attr}{type_attr}>{formula.group(0)}<v>{cached}</v></c>'
    return xml[: match.start()] + new_cell + xml[match.end() :]


if __name__ == "__main__":
    output = create_workbook()
    print(f"Excel oluşturuldu: {output}")
