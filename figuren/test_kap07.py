"""Tests für die Abbildungen von Kap. 7 „Uni- und Bivariate Analyse“ (BILDER.md §6)."""
import os
import sys
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

NS = "{http://www.w3.org/2000/svg}"


def alle_texte(svg):
    return "\n".join("".join(e.itertext()) for e in ET.fromstring(svg).iter(NS + "text"))


# Werte aus den Chunks neben den Abbildungen (ALLBUS 2023, R 4.5.3, mariposa 0.7.4), nach dem Setup-Chunk von Kap. 7
ERWARTET_KAP07 = {
    # Chunk `gewichtung-eastwest`; Gewichte der ersten sechs Befragten aus dem Westen (Zeilen 1, 2, 3, 5, 6, 7)
    # und der ersten drei aus dem Osten (Zeilen 4, 14, 18), wie distinct(eastwest, wghtpew) sie druckt
    "k07-gewichtung": ["UNGEWICHTET", "GEWICHTET", "frequency(eastwest)", "frequency(eastwest, weights = wghtpew)",
                       "ALTE BUNDESLAENDER", "NEUE BUNDESLAENDER", "1", "1.25", "1.20", "1.21", "0.545", "0.501",
                       "0.541", "3567", "1679", "67.99 %", "32.01 %", "4363", "883", "83.16 %", "16.84 %"],
    # Chunk `crosstab`: Zeilenprozente
    "k07-zeilenprozente": ["allbus |> crosstab(eastwest, educ_kat, weights = wghtpew)", "ALTE BUNDESLAENDER",
                           "NEUE BUNDESLAENDER", "Total", "niedrig", "mittel", "hoch", "22.2%", "27.6%", "50.3%",
                           "13.3%", "41.8%", "44.9%", "20.6%", "30.0%", "49.4%", "100.0%"],
}


class TestKap07(unittest.TestCase):
    def test_kap07_constraints(self):
        import kap07
        self.assertEqual(set(kap07.FIGUREN), set(ERWARTET_KAP07))
        for name, fn in kap07.FIGUREN.items():
            svg = fn().svg()
            root = ET.fromstring(svg)
            breite = float(root.get("viewBox").split()[2])
            self.assertLessEqual(breite, 768, name)
            texte = alle_texte(svg)
            for wert in ERWARTET_KAP07[name]:
                self.assertIn(wert, texte, f"{name}: {wert}")


if __name__ == "__main__":
    unittest.main()
