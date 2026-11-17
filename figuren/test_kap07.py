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
    # Chunk `freq-mm`, Tabelle zu mm01 (gewichtet): Wert 1, Total valid, Total missing, Total
    "k07-haeufigkeit": ["allbus |> frequency(mm01:mm06, weights = wghtpew)", "PROZENT", "GÜLTIGE PROZENT", "mm01",
                        "N = 1077", "Raw % = 20.53", "Valid % = 31.66", "Total", "5246", "Total valid", "3401",
                        "Total missing", "1845", "zählen nicht mit", "1", "2", "4", "5", "7"],
}


def zoll(e, k):
    return float(e.get(k)) / 96


def steine(svg):
    """Steinkörper (x, y, w, h, gefüllt) — ohne Noppen; leere Steine sind weiß und gestrichelt."""
    out = []
    for r in ET.fromstring(svg).iter(NS + "rect"):
        if r.get("fill") in ("#85B7EB", "#FFFFFF") and zoll(r, "width") > 0.3 and zoll(r, "height") < 0.3:
            if r.get("fill") == "#FFFFFF" and not r.get("stroke-dasharray"):
                continue
            out.append((zoll(r, "x"), zoll(r, "y"), zoll(r, "width"), zoll(r, "height"), r.get("fill") == "#85B7EB"))
    return out


def senkrechte(svg):
    """Senkrechte Linien (x, y oben, y unten) in Zoll."""
    out = []
    for e in ET.fromstring(svg).iter(NS + "line"):
        if e.get("x1") == e.get("x2"):
            y1, y2 = sorted((zoll(e, "y1"), zoll(e, "y2")))
            out.append((zoll(e, "x1"), y1, y2))
    return out


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

    def test_haeufigkeit_nenner(self):
        """Zweimal derselbe Turm mm01, nach Wert sortiert: zwei Steine 1 oben, vier leere unten. Bei Raw % umfasst
        die rechte Klammer alle Steine, bei Valid % nur die gefüllten; die linke Klammer die beiden Steine mit 1."""
        import kap07
        svg = kap07.haeufigkeit().svg()
        st = steine(svg)
        tuerme = {}
        for x, y, w, h, voll in st:
            tuerme.setdefault(round(x, 2), []).append((y, h, voll))
        self.assertEqual(len(tuerme), 2)
        texte = [("".join(e.itertext()), zoll(e, "x"), zoll(e, "y")) for e in ET.fromstring(svg).iter(NS + "text")]
        linien = senkrechte(svg)
        for k, (tx, reihe) in enumerate(sorted(tuerme.items())):
            reihe.sort()
            self.assertEqual([v for _, _, v in reihe], [True] * 6 + [False] * 4)
            werte = [t for t, x, y in sorted(texte, key=lambda t: t[2]) if abs(x - (tx + 0.275)) < 0.05
                     and t in {"1", "2", "4", "5", "7"}]
            self.assertEqual(werte, ["1", "1", "2", "4", "5", "7"])
            oben, unten_alle = reihe[0][0], reihe[-1][0] + reihe[-1][1]
            unten_1 = reihe[1][0] + reihe[1][1]
            unten_gueltig = reihe[5][0] + reihe[5][1]
            links = [l for l in linien if tx - 0.4 < l[0] < tx]
            rechts = [l for l in linien if tx + 0.55 < l[0] < tx + 1.0]
            self.assertTrue(any(abs(l[1] - oben) < 0.03 and abs(l[2] - unten_1) < 0.03 for l in links))
            soll = unten_alle if k == 0 else unten_gueltig
            self.assertTrue(any(abs(l[1] - oben) < 0.03 and abs(l[2] - soll) < 0.03 for l in rechts), k)
            if k == 1:                                     # keine Klammer bei Valid % reicht über die leeren Steine
                self.assertFalse(any(l[1] < unten_gueltig - 0.03 and l[2] > unten_gueltig + 0.1 for l in rechts))


if __name__ == "__main__":
    unittest.main()
