"""Tests für die Abbildungen von Kap. 4 „Datenimport und Inspektion“ (BILDER.md §6)."""
import os
import sys
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

NS = "{http://www.w3.org/2000/svg}"


def alle_texte(svg):
    return "\n".join("".join(e.itertext()) for e in ET.fromstring(svg).iter(NS + "text"))


# Werte aus den Chunks neben den Abbildungen (ALLBUS 2023, R 4.5.3, mariposa 0.7.4)
ERWARTET_KAP04 = {
    "k04-einlesen": ["ALLBUS2023.sav", "read_spss()", "allbus", "5,246 × 579", "<-", "read_spss",
                     '"ALLBUS2023.sav"'],
    "k04-platte": ["allbus", "respid", "age", "mm01", "1", "5", "50", "51", "69", "72", "18", "2",
                   "nrow(allbus)", "[1] 5246", "ncol(allbus)", "[1] 579"],
    "k04-select": ["allbus", "5,246 × 579", "respid", "mm01", "mm02", "mm03", "mm04", "5,246 × 3",
                   "allbus |> select(mm01, mm02, mm03)", "5", "3", "4", "2"],
    "k04-dollar-select": ["allbus$age |> head(5)", "allbus |> select(age) |> head(5)", "[1] 50 51 69 72 18",
                          "# A tibble: 5 × 1", "age", "<dbl+lbl>", "50", "51", "69", "72", "18"],
    "k04-filter": ["allbus", "sex", "age", "educ", "MANN", "FRAU", "50", "51", "69", "72", "18", "45", "3", "4", "5",
                   "sex == 2", "2,672 × 3", "allbus |> filter(sex == 2) |> select(sex, age, educ)"],
    "k04-dbl-lbl": ["1", "MANN", "double", "haven_labelled", "<dbl+lbl>", "dbl", "lbl", "class(allbus$sex)",
                    '[1] "haven_labelled" "vctrs_vctr"     "double"'],
    "k04-to-label": ["sex", "<dbl+lbl>", "<fct>", "<dbl>", "to_label()", "to_numeric()", "MANN", "FRAU", "1", "2"],
    "k04-labels": ["mm01", '"ISLAMAUSUEBUNG IN DEUTSCHL. BESCHRAENKEN"', "STIMME GAR NICHT ZU",
                   "STIMME VOLL+GANZ ZU", "1", "7", "Variablenname", "Variablenlabel", "Wertelabels",
                   "var_label()", "val_labels()"],
    "k04-missing-codes": ["-42", "-11", "-9", "-8", "DATENFEHLER: MFN", "TNZ: SPLIT", "KEINE ANGABE", "WEISS NICHT",
                          "2", "1647", "73", "123", "NA(a)", "NA(b)", "NA(c)", "NA(d)", "code", "n", "tag",
                          "na_frequencies(allbus$mm01)", "mm01", "mm06", "SPLIT-DESIGN"],
    "k04-set-na": ["6", "7", "ANDERER ABSCHLUSS", "NOCH SCHUELER", "18", "26", "set_na", "educ = c(6, 7)",
                   "# total N=5246 valid N=5093", "GÜLTIG", "FEHLEND"],
}


class TestKap04(unittest.TestCase):
    def test_kap04_constraints(self):
        import kap04
        self.assertEqual(set(kap04.FIGUREN), set(ERWARTET_KAP04))
        for name, fn in kap04.FIGUREN.items():
            svg = fn().svg()
            root = ET.fromstring(svg)
            breite = float(root.get("viewBox").split()[2])
            self.assertLessEqual(breite, 768, name)
            texte = alle_texte(svg)
            for wert in ERWARTET_KAP04[name]:
                self.assertIn(wert, texte, f"{name}: {wert}")


if __name__ == "__main__":
    unittest.main()
