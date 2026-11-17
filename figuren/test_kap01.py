"""Tests für die Abbildungen von Kap. 1 „RStudio“ (BILDER.md §6)."""
import os
import sys
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

NS = "{http://www.w3.org/2000/svg}"


def alle_texte(svg):
    return "\n".join("".join(e.itertext()) for e in ET.fromstring(svg).iter(NS + "text"))


# Namen aus dem Kapitel (Abschnitt 1.6 und die Chunks in 1.6.1, 1.6.2); nur Pakete und Funktionen, die Kap. 1 nennt
ERWARTET_KAP01 = {
    "k01-oekosystem": ["tidyverse", "dplyr", "tidyr", "ggplot2", "readr", "purrr", "tibble", "stringr", "forcats",
                       "lubridate", "mariposa", "read_spss()", "w_mean()", "Funktion", "Paket", "Ökosystem"],
    "k01-regal-werkbank": ["REGAL: INSTALLIERT", "WERKBANK: AKTIV", "tidyverse", "mariposa", "patchwork",
                           'install.packages("tidyverse")', 'install.packages("mariposa")',
                           'install.packages("patchwork")', "library(tidyverse)", "library(mariposa)",
                           "library(patchwork)", "einmal pro Rechner", "einmal pro R-Sitzung"],
}


class TestKap01(unittest.TestCase):
    def test_kap01_constraints(self):
        import kap01
        self.assertEqual(set(kap01.FIGUREN), set(ERWARTET_KAP01))
        for name, fn in kap01.FIGUREN.items():
            svg = fn().svg()
            root = ET.fromstring(svg)
            breite = float(root.get("viewBox").split()[2])
            self.assertLessEqual(breite, 768, name)
            texte = alle_texte(svg)
            for wert in ERWARTET_KAP01[name]:
                self.assertIn(wert, texte, f"{name}: {wert}")
            self.assertNotIn("Package", texte, f"{name}: Fachbegriff im Buch ist „Paket“")


if __name__ == "__main__":
    unittest.main()
