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
    # 1.4.4: Pfad aus dem Chunk getwd-demo, Projekt R-Workshop (Übung 1), Skript aus der Checkliste, absoluter Pfad
    # aus dem Vorsicht-Kasten; der zweite Rechner (Boris, Windows) ist ein Beispiel
    "k01-arbeitsverzeichnis": ['read_spss("ALLBUS2023.sav")',
                               'read_spss("/Users/anna/Documents/R-Workshop/ALLBUS2023.sav")',
                               "RECHNER VON ANNA", "RECHNER VON BORIS", "getwd()",
                               '[1] "/Users/anna/Documents/R-Workshop"', '[1] "C:/Users/boris/Documents/R-Workshop"',
                               "R-Workshop", "R-Workshop.Rproj", "01-erste_schritte.R", "ALLBUS2023.sav",
                               "gefunden", "nicht gefunden"],
    # 1.7: ?mean in R 4.5.3 (Kopf, Überschriften, Usage und Examples wörtlich); Begriffe aus dem Satz in 1.7
    "k01-hilfeseite": ["mean {base}", "R Documentation", "Arithmetic Mean", "Description",
                       "Generic function for the (trimmed) arithmetic mean.", "Usage", "mean(x, ...)",
                       "## Default S3 method:", "trim = 0", "na.rm = FALSE", "Arguments", "na.rm", "trim",
                       "Value, References, See Also", "Examples", "x <- c(0:10, 50)", "xm <- mean(x)",
                       "c(xm, mean(x, trim = 0.10))", "Funktionsbeschreibung", "Default-Werte", "Argumente",
                       "Beispiele"],
}


def text_elemente(svg):
    """(Text, x, y) je <text>, in Zoll."""
    from lego import DPI
    return [("".join(e.itertext()), float(e.get("x")) / DPI, float(e.get("y")) / DPI)
            for e in ET.fromstring(svg).iter(NS + "text")]


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

    def test_arbeitsverzeichnis_ergebnisse(self):
        """Der Dateiname findet die Datei auf beiden Rechnern, der absolute Pfad nur bei Anna (links)."""
        import kap01
        s = kap01.arbeitsverzeichnis()
        els = text_elemente(s.svg())
        mitte = s.w / 2
        gefunden = [x for t, x, y in els if t == "gefunden"]
        nicht = [x for t, x, y in els if t == "nicht gefunden"]
        self.assertEqual(len(gefunden), 3)
        self.assertEqual(len(nicht), 1)
        self.assertEqual(sum(1 for x in gefunden if x < mitte), 2)          # Anna: beide Zeilen
        self.assertGreater(nicht[0], mitte)                               # Boris: der absolute Pfad
        anna = [x for t, x, y in els if t == "RECHNER VON ANNA"][0]
        boris = [x for t, x, y in els if t == "RECHNER VON BORIS"][0]
        self.assertLess(anna, mitte)
        self.assertGreater(boris, mitte)

    def test_hilfeseite_reihenfolge(self):
        """Abschnitte in der Reihenfolge der Hilfeseite; jede Beschriftung steht auf Höhe ihres Abschnitts."""
        import kap01
        els = text_elemente(kap01.hilfeseite().svg())
        y = {t: yy for t, x, yy in els}
        reihe = ["Arithmetic Mean", "Description", "Usage", "Arguments", "Value, References, See Also", "Examples"]
        self.assertEqual(sorted(reihe, key=y.get), reihe)
        for abschnitt, wort in [("Description", "Funktionsbeschreibung"), ("Usage", "Default-Werte"),
                                ("Arguments", "Argumente"), ("Examples", "Beispiele")]:
            self.assertLess(abs(y[abschnitt] - y[wort]), 0.1, wort)


if __name__ == "__main__":
    unittest.main()
