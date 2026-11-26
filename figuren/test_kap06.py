"""Tests für die Abbildungen von Kap. 6 „Visualisierung — Grundlagen“ (BILDER.md §6)."""
import os
import sys
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

NS = "{http://www.w3.org/2000/svg}"

# ggplot2-Farben, wie layer_data() sie für die Chunks ausgibt (ggplot2 4.0.2)
HUE2 = ["#F8766D", "#00BFC4"]                    # zwei Stufen (MANN, FRAU in grammatik-vier)
HUE3 = ["#F8766D", "#00BA38", "#619CFF"]         # drei Stufen (sex mit DIVERS; educ_kat)
GREY50, STEELBLUE = "#7F7F7F", "#4682B4"


def alle_texte(svg):
    return "\n".join("".join(e.itertext()) for e in ET.fromstring(svg).iter(NS + "text"))


def zoll(e, k):
    return float(e.get(k)) / 96


# Werte aus den Chunks neben den Abbildungen (ALLBUS 2023, R 4.5.3, mariposa 0.7.4, ggplot2 4.0.2), nach dem
# Setup-Chunk von Kap. 6 (R/prep.R, educ_kat, to_label(eastwest, sex))
ERWARTET_KAP06 = {
    # neuer Chunk `grammatik-vier`: die ersten vier Reihen mit Werten in educ_kat, islamophobie und sex
    "k06-grammatik": ["vier |> ggplot(aes(x = educ_kat, y = islamophobie, color = sex)) +", "geom_point(size = 3)",
                      "respid", "educ_kat", "islamophobie", "sex", "<fct>", "<dbl>", "mittel", "hoch", "3.33", "4",
                      "3.83", "1.5", "MANN", "FRAU", "x", "y", "color", "1.5", "2.0", "2.5", "3.0", "3.5", "4.0",
                      "1", "5", "6", "9"],
    # Chunk `aes-vs-konstant` (eval=FALSE); Balken für 18 bis 24 Jahre aus layer_data()
    "k06-aes-konstante": ["INNERHALB aes()", "AUSSERHALB aes()",
                          "ggplot(allbus, aes(x = age, fill = sex)) + geom_bar()",
                          'ggplot(allbus, aes(x = age)) + geom_bar(fill = "steelblue")', "sex", "<fct>", "MANN",
                          "FRAU", "DIVERS", "NA", '"steelblue"', "fill", "18", "19", "20", "21", "22", "23", "24",
                          "keine Legende"],
    # Chunks `boxviolin` und `combo`
    "k06-ebenen": ["g_base", "<-", "allbus", "|>", "filter(", ", …)", "ggplot(", ", aes(…))", "geom_violin(",
                   "alpha = 0.4)", "geom_boxplot(", "width = 0.1,", 'fill = "white")', "niedrig", "mittel", "hoch",
                   "2", "4", "6", "+", "="],
    # Chunk `bar-prop`; count und prop aus layer_data(), die ersten zwei Befragten je Stufe (respid 8, 11 / 1, 4 / 2, 3)
    "k06-bar-zaehlt": ["ggplot(aes(x = educ_kat, weight = wghtpew)) +",
                       'geom_bar(aes(y = after_stat(prop), group = 1), fill = "steelblue")', "educ_kat",
                       "wghtpew", "<fct>", "<dbl+lbl>", "niedrig", "mittel", "hoch", "1.20", "1.25", "0.545", "count",
                       "prop", "1049.6", "1524.7", "2510.5", "0.206", "0.300", "0.494", "geom_bar()",
                       "weight = wghtpew", "y = after_stat(prop)", "0%", "10%", "20%", "30%", "40%", "50%"],
}

ERWARTET_KAP06_EN = {
    "k06-grammatik": ["four |> ggplot(aes(x = educ_cat, y = islamophobia, color = sex)) +", "geom_point(size = 3)",
                      "respid", "educ_cat", "islamophobia", "sex", "<fct>", "<dbl>", "medium", "high", "3.33", "4",
                      "3.83", "1.5", "MALE", "FEMALE", "x", "y", "color", "1.5", "2.0", "2.5", "3.0", "3.5", "4.0",
                      "1", "5", "6", "9"],
    "k06-aes-konstante": ["INSIDE aes()", "OUTSIDE aes()",
                          "ggplot(allbus, aes(x = age, fill = sex)) + geom_bar()",
                          'ggplot(allbus, aes(x = age)) + geom_bar(fill = "steelblue")', "sex", "<fct>", "MALE",
                          "FEMALE", "NON-BINARY", "NA", '"steelblue"', "fill", "18", "19", "20", "21", "22", "23",
                          "24", "no legend"],
    "k06-ebenen": ["g_base", "<-", "allbus", "|>", "filter(", ", …)", "ggplot(", ", aes(…))", "geom_violin(",
                   "alpha = 0.4)", "geom_boxplot(", "width = 0.1,", 'fill = "white")', "low", "medium", "high",
                   "2", "4", "6", "+", "="],
    "k06-bar-zaehlt": ["ggplot(aes(x = educ_cat, weight = wghtpew)) +",
                       'geom_bar(aes(y = after_stat(prop), group = 1), fill = "steelblue")', "educ_cat",
                       "wghtpew", "<fct>", "<dbl+lbl>", "low", "medium", "high", "1.20", "1.25", "0.545", "count",
                       "prop", "1049.6", "1524.7", "2510.5", "0.206", "0.300", "0.494", "geom_bar()",
                       "weight = wghtpew", "y = after_stat(prop)", "0%", "10%", "20%", "30%", "40%", "50%"],
}


def kreise(svg):
    """(cx, cy, r, fill, stroke) je <circle>, in Zoll."""
    return [(zoll(c, "cx"), zoll(c, "cy"), zoll(c, "r"), c.get("fill"), c.get("stroke"))
            for c in ET.fromstring(svg).iter(NS + "circle")]


def rechtecke(svg, fill):
    return [(zoll(r, "x"), zoll(r, "y"), zoll(r, "width"), zoll(r, "height"))
            for r in ET.fromstring(svg).iter(NS + "rect") if r.get("fill") == fill]


class TestKap06(unittest.TestCase):
    def test_kap06_constraints(self):
        import kap06
        self.assertEqual(set(kap06.FIGUREN), set(ERWARTET_KAP06))
        for name, fn in kap06.FIGUREN.items():
            svg = fn().svg()
            root = ET.fromstring(svg)
            breite = float(root.get("viewBox").split()[2])
            self.assertLessEqual(breite, 768, name)
            texte = alle_texte(svg)
            for wert in ERWARTET_KAP06[name]:
                self.assertIn(wert, texte, f"{name}: {wert}")

    def test_grammatik_reihe_wird_punkt(self):
        """Vier Punkte: Höhe nach islamophobie, Spalte nach educ_kat, Farbe nach sex; Reihe 1 orange markiert."""
        import kap06
        from lego import ORANGE
        svg = kap06.grammatik().svg()
        punkte = [k for k in kreise(svg) if k[3] in HUE2 and k[4] is None]
        r_punkt = max(k[2] for k in punkte)
        daten = sorted((k for k in punkte if k[2] == r_punkt), key=lambda k: k[1])     # von oben nach unten
        self.assertEqual(len(daten), 4)
        # von oben: 4 (FRAU, hoch), 3.83 (FRAU, hoch), 3.33 (MANN, mittel), 1.5 (MANN, hoch)
        self.assertEqual([k[3] for k in daten], [HUE2[1], HUE2[1], HUE2[0], HUE2[0]])
        x_hoch = daten[0][0]
        self.assertAlmostEqual(daten[1][0], x_hoch, places=3)
        self.assertAlmostEqual(daten[3][0], x_hoch, places=3)
        self.assertLess(daten[2][0], x_hoch - 0.3)                                   # mittel links von hoch
        anteil = (daten[2][1] - daten[0][1]) / (daten[3][1] - daten[0][1])
        self.assertAlmostEqual(anteil, (4 - 10 / 3) / (4 - 1.5), places=2)
        # Legende: je ein Punkt für MANN und FRAU
        self.assertEqual(sorted(k[3] for k in punkte if k[2] < r_punkt), sorted(HUE2))
        # Reihe 1 (respid 1) im Rahmen, ihr Punkt im Ring
        ringe = [k for k in kreise(svg) if k[4] == ORANGE]
        self.assertEqual(len(ringe), 1)
        self.assertAlmostEqual(ringe[0][0], daten[2][0], places=3)
        self.assertAlmostEqual(ringe[0][1], daten[2][1], places=3)
        rahmen = [r for r in ET.fromstring(svg).iter(NS + "rect") if r.get("stroke") == ORANGE and r.get("fill") == "none"]
        self.assertEqual(len(rahmen), 1)
        y_333 = [float(t.get("y")) / 96 for t in ET.fromstring(svg).iter(NS + "text") if "".join(t.itertext()) == "3.33"]
        self.assertEqual(len(y_333), 1)
        self.assertTrue(zoll(rahmen[0], "y") < y_333[0] < zoll(rahmen[0], "y") + zoll(rahmen[0], "height"))
        # die Zuordnungen x, y, color stehen je zweimal im Bild: unter dem Turm und an der Grafik
        texte = ["".join(t.itertext()) for t in ET.fromstring(svg).iter(NS + "text")]
        for a in ("x", "y", "color"):
            self.assertEqual(texte.count(a), 2, a)

    def test_aes_konstante_balken(self):
        """Oben je Alter ein Balken, nach sex gestapelt (von unten DIVERS, FRAU, MANN), mit Legende;
        unten dieselben Balkenhöhen, alle steelblue, ohne Legende."""
        import kap06
        svg = kap06.aes_konstante().svg()
        # 18 bis 24 Jahre, Zählung je sex aus layer_data(), von oben: MANN, FRAU, DIVERS
        soll = [[20, 21], [25, 31, 1], [26, 28], [19, 24, 1], [31, 28, 2], [30, 30], [29, 26, 1]]
        teile = {}
        for f in HUE3:
            for x, y, w, h in rechtecke(svg, f):
                if w > 0.2:                                          # Balken, keine Legendenfelder
                    teile.setdefault(round(x, 3), []).append((y, h, f))
        self.assertEqual(len(teile), 7)
        hoehen, einheit = [], None
        for x, zaehlung in zip(sorted(teile), soll):
            stapel = sorted(teile[x])                                # von oben nach unten
            self.assertEqual([f for _, _, f in stapel], HUE3[:len(zaehlung)])
            for (y1, h1, _), (y2, _, _) in zip(stapel, stapel[1:]):
                self.assertAlmostEqual(y1 + h1, y2, places=3)        # lückenlos gestapelt
            einheit = einheit or stapel[0][1] / zaehlung[0]
            for (_, h, _), n in zip(stapel, zaehlung):
                self.assertAlmostEqual(h, n * einheit, places=3)
            hoehen.append(sum(h for _, h, _ in stapel))
        blau = sorted(rechtecke(svg, STEELBLUE))
        self.assertEqual(len(blau), 7)
        for (x, y, w, h), soll in zip(blau, hoehen):
            self.assertAlmostEqual(h, soll, places=3)               # gleiche Höhen wie oben
        legende = [r for f in HUE3 + [GREY50] for r in rechtecke(svg, f) if r[2] <= 0.2]
        self.assertEqual(len(legende), 4)
        self.assertTrue(all(r[1] < blau[0][1] for r in legende))     # Legende nur im oberen Teil

    def test_ebenen_folien(self):
        """Zwei Folien (Violinen, Boxplots) und das Ergebnis, in dem die Boxen über den Violinen liegen."""
        import kap06
        svg = kap06.ebenen().svg()
        root = ET.fromstring(svg)
        folien = [r for r in root.iter(NS + "rect") if r.get("fill") == kap06.FOLIE]
        self.assertEqual(len(folien), 2)
        reihenfolge = []
        for e in root.iter():
            if e.tag == NS + "polygon" and e.get("fill") in HUE3:
                self.assertEqual(e.get("fill-opacity"), "0.4")
                reihenfolge.append(("violine", float(e.get("points").split()[0].split(",")[0]) / 96, e.get("fill")))
            elif e.tag == NS + "rect" and e.get("fill") == "#FFFFFF" and e.get("stroke") == kap06.GRAU20:
                reihenfolge.append(("box", zoll(e, "x"), None))
        violinen = [r for r in reihenfolge if r[0] == "violine"]
        boxen = [r for r in reihenfolge if r[0] == "box"]
        self.assertEqual([f for *_, f in violinen], HUE3 * 2)          # Folie und Ergebnis
        self.assertEqual(len(boxen), 6)
        # Folie 1 enthält nur Violinen, Folie 2 nur Boxen
        f1, f2 = sorted(folien, key=lambda r: zoll(r, "x"))
        innen = lambda x, f: zoll(f, "x") < x < zoll(f, "x") + zoll(f, "width")     # noqa: E731
        self.assertEqual(sum(innen(x, f1) for _, x, _ in violinen), 3)
        self.assertEqual(sum(innen(x, f1) for _, x, _ in boxen), 0)
        self.assertEqual(sum(innen(x, f2) for _, x, _ in boxen), 3)
        self.assertEqual(sum(innen(x, f2) for _, x, _ in violinen), 0)
        # im Ergebnis (rechts von Folie 2) kommen die Boxen nach den Violinen, liegen also oben
        rechts = zoll(f2, "x") + zoll(f2, "width")
        ergebnis = [art for art, x, _ in reihenfolge if x > rechts]
        self.assertEqual(ergebnis, ["violine"] * 3 + ["box"] * 3)

    def test_bar_zaehlt_anteile(self):
        """Drei Balken in steelblue, so hoch wie prop (0.206, 0.300, 0.494), auf einer Grundlinie."""
        import kap06
        svg = kap06.bar_zaehlt().svg()
        balken = sorted(rechtecke(svg, STEELBLUE))
        self.assertEqual(len(balken), 3)
        props = [1049.630 / 5084.858, 1524.693 / 5084.858, 2510.535 / 5084.858]
        for (x, y, w, h), p in zip(balken, props):
            self.assertAlmostEqual(h / balken[2][3], p / props[2], places=3)
            self.assertAlmostEqual(y + h, balken[0][1] + balken[0][3], places=3)

    def test_en_schluessel_gleich(self):
        self.assertEqual(set(ERWARTET_KAP06_EN), set(ERWARTET_KAP06))

    def test_englische_texte(self):
        import kap06
        import sprache
        sprache.setze("en")
        try:
            for name, fn in kap06.FIGUREN.items():
                svg = fn().svg()
                breite = float(ET.fromstring(svg).get("viewBox").split()[2])
                self.assertLessEqual(breite, 768, name)
                texte = alle_texte(svg)
                for wert in ERWARTET_KAP06_EN[name]:
                    self.assertIn(wert, texte, f"{name}: {wert}")
        finally:
            sprache.setze("de")

    def test_kein_deutscher_rest(self):
        import check_en
        import kap06
        import sprache
        sprache.setze("en")
        try:
            for name, fn in kap06.FIGUREN.items():
                self.assertEqual(check_en.deutsch_reste(alle_texte(fn().svg())), [], name)
        finally:
            sprache.setze("de")

    def test_en_ohne_deutsche_namen(self):
        """Keine deutschen Namen aus STYLE.md §13 in den englischen Abbildungen."""
        import re
        import kap06
        import sprache
        sprache.setze("en")
        try:
            for name, fn in kap06.FIGUREN.items():
                texte = alle_texte(fn().svg())
                for alt in ("vier", "educ_kat", "islamophobie", "niedrig", "mittel", "hoch"):
                    self.assertIsNone(re.search(rf"\b{alt}\b", texte), f"{name}: {alt}")
        finally:
            sprache.setze("de")

    def test_deutsch_unveraendert(self):
        import kap06
        import sprache
        sprache.setze("de")
        for name, fn in kap06.FIGUREN.items():
            texte = alle_texte(fn().svg())
            for wert in ERWARTET_KAP06[name]:
                self.assertIn(wert, texte, f"{name}: {wert}")


if __name__ == "__main__":
    unittest.main()
