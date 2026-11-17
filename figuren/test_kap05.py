"""Tests für die Abbildungen von Kap. 5 „Daten transformieren und Skalen bilden“ (BILDER.md §6)."""
import os
import sys
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

NS = "{http://www.w3.org/2000/svg}"


def alle_texte(svg):
    return "\n".join("".join(e.itertext()) for e in ET.fromstring(svg).iter(NS + "text"))


# Werte aus den Chunks neben den Abbildungen (ALLBUS 2023, R 4.5.3, mariposa 0.7.4)
ERWARTET_KAP05 = {
    "k05-mutate": ["age", "<dbl+lbl>", "geburtsjahr", "<dbl>", "50", "51", "69", "1973", "1972", "1954",
                   "2023 - 50", "2023 - 51", "2023 - 69", "mutate", "geburtsjahr = 2023 - age",
                   "allbus |> select(age) |> mutate(geburtsjahr = 2023 - age) |> head(3)"],
    "k05-zuweisung": ["OHNE <-", "MIT <-", "allbus |>", "allbus <- allbus |>", "mutate(geburtsjahr = 2023 - age)",
                      "allbus", "5,246 × 579",
                      "5,246 × 580", "age", "geburtsjahr", "50", "51", "69", "1973", "1972", "1954",
                      "nur angezeigt", "gespeichert"],
    "k05-case-when": ["FALSCH", "RICHTIG", 'age >= 18 ~ "erwachsen"', 'age >= 65 ~ "senior"',
                      '.default = "unter 18"', "50", "51", "69", "72", "18"],
    "k05-summarise": ["eastwest", "age", "ALTE BUNDESLAENDER", "NEUE BUNDESLAENDER", "50", "51", "69", "72",
                      "44", "60", "durchschnitt_alter", "51.7", "54.3", "3567", "1679", "mean()",
                      "group_by(eastwest) |> summarise(…, durchschnitt_alter = mean(age, na.rm = TRUE))"],
    "k05-rec": ["educ", "1", "2", "3", "4", "5", "6", "7", "OHNE ABSCHLUSS", "VOLKS-,HAUPTSCHULE", "MITTLERE REIFE",
                "FACHHOCHSCHULREIFE", "HOCHSCHULREIFE", "ANDERER ABSCHLUSS", "NOCH SCHUELER", "1:2=1 [niedrig]",
                "3=2 [mittel]", "4:5=3 [hoch]", "else=NA", "niedrig", "mittel", "hoch", "982", "1639", "2472", "153",
                "<fct>"],
    "k05-dicho": ["age", "age_d", "72", "69", "51", "50", "18", "1", "0", "dicho(50)", "2942", "2281",
                  "NICHT GENERIERBAR", "23", "bis 50", "über 50"],
    "k05-umpolen": ["mm02", "mm02r", "1", "2", "3", "4", "5", "6", "7", "STIMME GAR NICHT ZU", "STIMME VOLL+GANZ ZU",
                    "TNZ: SPLIT", "954", "515", "494", "629", "350", "235", "227", "1842", "8 - x",
                    "allbus |> count(mm02, mm02r)"],
    "k05-skala": ["respid", "mm01", "mm02r", "mm03", "mm04", "mm05r", "mm06", "islamophobie", "1", "53", "120",
                  "5", "4", "2", "6", "3", "3.33", "3.4", "min_valid = 5", "6 gültig", "5 gültig", "4 gültig"],
    "k05-polung": ["mm01", "pa29", "pa29r", "STIMME GAR NICHT ZU", "STIMME VOLL+GANZ ZU", "STIMME VOLL ZU",
                   "LEHNE GANZ AB", "1", "5", "7", "hoch = islamophob", "niedrig = populistisch",
                   "hoch = populistisch", 'rec(pa29, rules = "rev", suffix = "r")'],
    "k05-pomps": ["islamophobie", "populismus", "islamophobie_p", "populismus_p", "4.11", "3.4", "51.9", "60.0",
                  "0", "25", "50", "75", "100", "1", "5", "7"],
    "k05-pipeline": ["1", "2", "3", "4", "5", "6", "R/prep.R", 'source("R/prep.R")', "4.3", "5.3.3", "5.7.1",
                     "5.7.3", "5.8", "read_spss()", "row_means()", "pomps()"],
    "k05-std": ["age", "age_c", "age_z", "center()", "std()", "50", "69", "52.51", "18.25", "-2.51", "16.49",
                "-0.138", "0.903", "30", "40", "60", "70", "-20", "-10", "0", "10", "20", "-1", "1",
                "- 52.51", "/ 18.25"],
    "k05-join": ["allbus", "kontext_bl", "allbus_mit_kontext", "eastwest", "age", "muslim_anteil", "bip_pro_kopf",
                 "1", "2", "50", "51", "69", "72", "7.2", "1.4", "45000", "32000", "left_join()",
                 'allbus_mit_kontext <- allbus |> left_join(kontext_bl, by = "eastwest")'],
    "k05-join-familie": ["x", "y", "id", "a", "b", "1", "2", "3", "4", "10", "20", "30", "A", "B", "D",
                         "left_join(x, y)", "inner_join(x, y)", "full_join(x, y)"],
    "k05-pivot-longer": ["mm01", "mm02r", "mm03", "mm04", "mm05r", "mm06", "item", "antwort", "<chr>", "<dbl>",
                         "5", "4", "2", "pivot_longer()", "5,246 × 6", "31,476 × 2",
                         "pivot_longer(cols = everything(),", 'names_to = "item",', 'values_to = "antwort")'],
    "k05-pivot-wider": ["eastwest", "item", "mw", "<fct>", "<chr>", "<dbl>", "ALTE BUNDESLAENDER",
                        "NEUE BUNDESLAENDER", "mm01", "mm03", "mm06", "3.19", "3.97", "4.14", "4.01", "4.63", "4.58",
                        "pivot_wider()", "pivot_wider(names_from = eastwest, values_from = mw)", "names_from",
                        "values_from"],
    "k05-row-count": ["respid", "1", "2", "95", "mm01", "mm02", "mm03", "mm04", "mm05", "mm06", "n_extrem", "<int>",
                      "0", "3", "7", "row_count()", "count = 7"],
}


def texte_pos(svg):
    """(Text, x, y, Farbe) je <text>, in Zoll; x ist bei zentrierten Steinwerten die Mitte."""
    from lego import DPI
    return [("".join(e.itertext()), float(e.get("x")) / DPI, float(e.get("y")) / DPI, e.get("fill"))
            for e in ET.fromstring(svg).iter(NS + "text")]


def spalten(svg, werte):
    """Gruppiert Texte aus `werte` nach x (Spalten von links nach rechts), je Spalte von oben nach unten."""
    sp = {}
    for t, x, y, _ in texte_pos(svg):
        if t in werte:
            sp.setdefault(round(x, 2), []).append((y, t))
    return [[t for _, t in sorted(v)] for _, v in sorted(sp.items())]


def rahmen(svg, farbe):
    """Rechtecke ohne Füllung mit Kante in `farbe`: (x, y, w, h) in Zoll."""
    from lego import DPI
    return [tuple(float(r.get(k)) / DPI for k in ("x", "y", "width", "height"))
            for r in ET.fromstring(svg).iter(NS + "rect") if r.get("stroke") == farbe and r.get("fill") == "none"]


def leere_steine(svg):
    """Anzahl leerer, gestrichelter Steine (NA)."""
    from lego import STEIN
    return len([r for r in ET.fromstring(svg).iter(NS + "rect")
                if r.get("fill") == STEIN["na"][0] and r.get("stroke-dasharray")
                and float(r.get("height")) > 15])


class TestKap05(unittest.TestCase):
    def test_kap05_constraints(self):
        import kap05
        self.assertEqual(set(kap05.FIGUREN), set(ERWARTET_KAP05))
        for name, fn in kap05.FIGUREN.items():
            svg = fn().svg()
            root = ET.fromstring(svg)
            breite = float(root.get("viewBox").split()[2])
            self.assertLessEqual(breite, 768, name)
            texte = alle_texte(svg)
            for wert in ERWARTET_KAP05[name]:
                self.assertIn(wert, texte, f"{name}: {wert}")

    def test_std_lineale(self):
        """Die Personen 50 und 69 stehen auf allen drei Linealen an derselben Stelle; nur die Skala ändert sich."""
        import kap05
        from lego import STEIN, DPI
        root = ET.fromstring(kap05.std_fig().svg())
        marken = []
        for p in root.iter(NS + "polygon"):
            if p.get("fill") == STEIN["num"][0]:
                xs = [float(v.split(",")[0]) / DPI for v in p.get("points").split()]
                marken.append(round((min(xs) + max(xs)) / 2, 2))
        self.assertEqual(len(marken), 6)
        self.assertEqual(len(set(marken)), 2)
        pos = texte_pos(kap05.std_fig().svg())
        reihe = lambda t: [y for s_, _, y, _ in pos if s_ == t]
        self.assertLess(reihe("69")[0], reihe("16.49")[0])
        self.assertLess(reihe("16.49")[0], reihe("0.903")[0])

    def test_join_andocken(self):
        """Die Kontextwerte stehen genau über den neuen Türmen; West bekommt 7.2/45000, Ost 1.4/32000."""
        import kap05
        from lego import ORANGE, GREEN
        svg = kap05.join_fig().svg()
        self.assertIn(["7.2", "1.4", "7.2", "7.2", "7.2", "1.4"], spalten(svg, {"7.2", "1.4"}))
        self.assertIn(["45000", "32000", "45000", "45000", "45000", "32000"], spalten(svg, {"45000", "32000"}))
        self.assertIn(["1", "1", "1", "2"], spalten(svg, {"1", "2"}))
        self.assertEqual(len(rahmen(svg, ORANGE)), 2)          # Ost-Reihe in kontext_bl und im Ergebnis
        self.assertEqual(len(rahmen(svg, GREEN)), 2)           # zwei neue Türme

    def test_join_familie(self):
        """left behält 1–3 (b bei 3 leer), inner nur 1 und 2, full 1–4 mit zwei leeren Steinen."""
        import kap05
        svg = kap05.join_familie().svg()
        ids = spalten(svg, {"1", "2", "3", "4"})
        self.assertEqual(sorted(map(tuple, ids)), sorted([("1", "2", "3"), ("1", "2", "4"), ("1", "2", "3"),
                                                         ("1", "2"), ("1", "2", "3", "4")]))
        self.assertIn(["A", "B", "D"], spalten(svg, {"A", "B", "D"}))
        self.assertIn(["A", "B"], spalten(svg, {"A", "B", "D"}))
        self.assertEqual(leere_steine(svg), 3)

    def test_pivot_longer_schilder_werden_steine(self):
        """Sechs dunkle Namensschilder oben, im Turm item dieselben Namen als lila Steine (zwei Personen)."""
        import kap05
        from lego import INK, STEIN, ORANGE
        svg = kap05.pivot_longer_fig().svg()
        items = ["mm01", "mm02r", "mm03", "mm04", "mm05r", "mm06"]
        pos = texte_pos(svg)
        schilder = [t for t, _, _, f in pos if t in items and f == "#FFFFFF"]
        steine = [t for t, _, _, f in pos if t in items and f == STEIN["txt"][1]]
        self.assertEqual(schilder, items)
        self.assertEqual(steine, items + items[:2])
        self.assertIn(["5", "5", "4", "2", "2", "2"], spalten(svg, {"5", "4", "2"}))
        self.assertEqual(len(rahmen(svg, ORANGE)), 2)          # Person 1: eine Reihe breit, sechs Reihen lang
        self.assertEqual(leere_steine(svg), 8)                  # Person 2: sechs Lücken breit, zwei lang gezeigt

    def test_pivot_wider_steine_werden_schilder(self):
        """Die Stufen von eastwest werden zwei Namensschilder, darunter die Mittelwerte."""
        import kap05
        from lego import STEIN
        svg = kap05.pivot_wider_fig().svg()
        pos = texte_pos(svg)
        regionen = ["ALTE BUNDESLAENDER", "NEUE BUNDESLAENDER"]
        self.assertEqual([t for t, _, _, f in pos if t in regionen and f == "#FFFFFF"], regionen)
        self.assertEqual([t for t, _, _, f in pos if t in regionen and f == STEIN["txt"][1]], [regionen[0]] * 3 +
                         [regionen[1]] * 3)
        mw = spalten(svg, {"3.19", "3.97", "4.14", "4.01", "4.63", "4.58"})
        self.assertEqual(mw, [["3.19", "3.97", "4.14", "4.01", "4.63", "4.58"], ["3.19", "3.97", "4.14"],
                              ["4.01", "4.63", "4.58"]])

    def test_row_count_luecken_null(self):
        """Gezählt werden nur die Siebener; sechs Lücken ergeben 0, keinen leeren Stein."""
        import kap05
        from lego import STEIN
        svg = kap05.row_count_fig().svg()
        pos = texte_pos(svg)
        self.assertIn(["0", "0", "3"], spalten(svg, {"0", "3"}))
        grau = sorted(t for t, _, _, f in pos if f == STEIN["dim"][1])
        self.assertEqual(grau, sorted(["5", "3", "4", "2", "6", "2", "1", "6", "4"]))
        self.assertEqual(sorted(t for t, _, _, f in pos if f == STEIN["num"][1]), ["0", "0", "3", "7", "7", "7"])
        self.assertEqual(leere_steine(svg), 6)


if __name__ == "__main__":
    unittest.main()
