from __future__ import annotations

import re
import unittest
from pathlib import Path

from openpyxl import load_workbook

from create_su_verimliligi_kapsam_tablosu import EK2_NACE, FIRMS, OUT_SCOPE, IN_SCOPE, create_workbook


def normalize_nace(value: object) -> str:
    digits = re.sub(r"\D", "", str(value or ""))
    if len(digits) < 4:
        return "GEÇERSİZ"
    return f"{digits[:2]}.{digits[2:4]}"


def scope_status(nace: object, employees: object) -> str:
    normalized = normalize_nace(nace)
    in_list = normalized in {code for code, *_ in EK2_NACE}
    enough_staff = isinstance(employees, (int, float)) and employees >= 50
    if in_list and enough_staff:
        return IN_SCOPE
    return OUT_SCOPE


class Ek2ListTests(unittest.TestCase):
    def test_list_has_148_unique_codes(self) -> None:
        codes = [item[0] for item in EK2_NACE]
        self.assertEqual(len(codes), 148)
        self.assertEqual(len(set(codes)), 148)

    def test_codes_are_four_digit_nace(self) -> None:
        for code, *_ in EK2_NACE:
            self.assertRegex(code, r"^\d{2}\.\d{2}$")


class ScopeLogicTests(unittest.TestCase):
    def test_listed_nace_with_50_or_more_is_in_scope(self) -> None:
        self.assertEqual(scope_status("10.11", 50), IN_SCOPE)
        self.assertEqual(scope_status("10.11.01", 120), IN_SCOPE)
        self.assertEqual(scope_status("10,11", 51), IN_SCOPE)
        self.assertEqual(scope_status("1011", 80), IN_SCOPE)

    def test_listed_nace_under_50_is_out_of_scope(self) -> None:
        self.assertEqual(scope_status("10.11", 49), OUT_SCOPE)
        self.assertEqual(scope_status("10.11", 30), OUT_SCOPE)

    def test_unlisted_nace_is_out_of_scope_even_with_many_employees(self) -> None:
        self.assertEqual(scope_status("47.11", 200), OUT_SCOPE)
        self.assertEqual(scope_status("85.20", 500), OUT_SCOPE)

    def test_known_ek2_codes_from_regulation(self) -> None:
        codes = {item[0] for item in EK2_NACE}
        for code in ("01.41", "10.81", "20.16", "24.10", "35.11", "42.12"):
            self.assertIn(code, codes)


class WorkbookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.path = Path("/tmp/su-verimliligi-kapsam-test.xlsx")
        create_workbook(cls.path)
        cls.wb = load_workbook(cls.path)

    def test_expected_sheets_exist(self) -> None:
        self.assertEqual(
            self.wb.sheetnames,
            ["Firma Kontrolü", "Ek-2 NACE Listesi", "Nasıl Kullanılır"],
        )

    def test_example_rows_and_formulas(self) -> None:
        ws = self.wb["Firma Kontrolü"]
        self.assertEqual(len(FIRMS), 66)
        self.assertEqual(ws["A10"].value, FIRMS[0])
        self.assertEqual(ws["A75"].value, FIRMS[-1])
        for idx, name in enumerate(FIRMS):
            self.assertEqual(ws.cell(10 + idx, 1).value, name)
        self.assertIn(ws["B10"].value, ("", None))
        self.assertIsNone(ws["C10"].value)
        self.assertIn(IN_SCOPE, ws["F10"].value)
        self.assertIn(OUT_SCOPE, ws["F11"].value)

    def test_conditional_formatting_covers_scope_column(self) -> None:
        ws = self.wb["Firma Kontrolü"]
        rules = list(ws.conditional_formatting._cf_rules.values())
        flat = [rule for group in rules for rule in group]
        formulas = [getattr(rule, "formula", None) for rule in flat]
        self.assertTrue(any(f == [f'"{IN_SCOPE}"'] for f in formulas))
        self.assertTrue(any(f == [f'"{OUT_SCOPE}"'] for f in formulas))

    def test_nace_sheet_row_count(self) -> None:
        ws = self.wb["Ek-2 NACE Listesi"]
        self.assertEqual(ws["B2"].value, "01.41")
        self.assertEqual(ws["B149"].value, "42.12")
        self.assertIsNone(ws["B150"].value)

    def test_scope_column_has_cached_results(self) -> None:
        import zipfile

        xml = zipfile.ZipFile(self.path).read("xl/worksheets/sheet1.xml").decode("utf-8")
        self.assertIn(IN_SCOPE, xml)
        self.assertIn(OUT_SCOPE, xml)
        self.assertIn("$AA$2:$AA$149", xml)
        self.assertNotIn("<v />", xml)

    def test_file_is_unlocked_excel_workbook(self) -> None:
        import zipfile

        z = zipfile.ZipFile(self.path)
        xml = z.read("xl/workbook.xml").decode("utf-8")
        self.assertNotIn("workbookProtection", xml)
        for name in z.namelist():
            if name.startswith("xl/worksheets/sheet") and name.endswith(".xml"):
                sheet = z.read(name).decode("utf-8")
                self.assertNotIn("sheetProtection", sheet)
        self.assertFalse(any(n.startswith("xl/comments") for n in z.namelist()))
        for ws in self.wb.worksheets:
            self.assertFalse(ws.protection.sheet)


if __name__ == "__main__":
    unittest.main()
