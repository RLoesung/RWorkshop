"""Tests für die Abbildungen von Kap. 9 „Erklärungsmodelle“ (BILDER.md §6)."""
import os
import sys
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

NS = "{http://www.w3.org/2000/svg}"
INK, GREEN, GRAY, ORANGE = "#1E2D3C", "#36A266", "#6E7882", "#E6A033"
SCHRIFT_NUM, SCHRIFT_TXT, SCHRIFT_DIM = "#042C53", "#26215C", "#A8A69E"

# Die ersten acht Reihen von allbus nach dem Setup-Chunk von Kap. 9 (respid 1 bis 8), wie tibble sie druckt;
# "" = NA. Spalten: islamophobie, educ_kat, age, eastwest, sex, populismus
ALT, NEU = "ALTE BUNDESLAENDER", "NEUE BUNDESLAENDER"
ACHT = [("3.33", "mittel", "50", ALT, "MANN", "2.29"), ("", "hoch", "51", ALT, "MANN", "3"),
        ("", "hoch", "69", ALT, "FRAU", "2.86"), ("", "mittel", "72", NEU, "MANN", "4.57"),
        ("4", "hoch", "18", ALT, "FRAU", ""), ("3.83", "hoch", "45", ALT, "FRAU", "3.71"),
        ("", "mittel", "26", ALT, "FRAU", ""), ("", "niedrig", "71", ALT, "FRAU", "4.14")]

# Werte aus den Chunks neben den Abbildungen (ALLBUS 2023, R 4.5.3, mariposa 0.7.4), nach dem Setup-Chunk von Kap. 9
ERWARTET_KAP09 = {
    # 9.3.1: Reihen 1, 2 und 8 von allbus; Dummies wie model.matrix(~ educ_kat); levels(allbus$educ_kat)
    "k09-dummy": ["educ_kat", "educ_katmittel", "educ_kathoch", "intern", "mittel", "hoch", "niedrig", "1", "0",
                  "2", "8", "levels(allbus$educ_kat)", '[1] "niedrig" "mittel"  "hoch"', "Referenz"],
    # 9.4.1: Chunk model-compare; Maße der Tibbles allbus und allbus_modell (N = 1881 im Chunk lm)
    "k09-fallset": ["allbus_modell <- allbus |>", "drop_na(islamophobie, educ_kat, age, eastwest, sex, populismus)",
                    "islamophobie", "educ_kat", "age", "eastwest", "sex", "populismus", "allbus", "allbus_modell",
                    "5,246 × 593", "1,881 × 593", "ohne drop_na():", "nur in m_basis", ALT, NEU, "MANN", "FRAU",
                    "niedrig"]
                   + [v for r in ACHT for v in r if v],
    # 9.6.3: Chunk augment-setup (Reihen 1 und 2 von diagnose_df, auf drei Stellen gerundet); Rechnung mit B aus
    # lm-summary
    "k09-augment": ["diagnose_df <- modell |> augment()", "islamophobie", "educ_kat", "age", "…", "populismus",
                    "(weights)", ".fitted", ".resid", ".hat", "3.333", "3.833", "mittel", "hoch", "50", "45", "2.286",
                    "3.714", "1.252", "3.400", "3.829", "-0.067", "0.004", "0.005", "0.003", "0.808", "0.012 · 1",
                    "0.024 · 50", "0.603 · 2.286", "3.40", "(Intercept)", "educ_katmittel"],
    # 9.7.3: Mittelwerte aus summary() von oneway_anova() (7.6.2), Randmittel aus Chunk ancova-summary
    # Zahlen nur an den ganzen Strichen; 3.5 und 4.5 sind kürzere Striche ohne Zahl
    "k09-randmittel": ["oneway_anova()", "ancova()", "covariate = age", "3", "4", "5",
                       "niedrig 4.68", "mittel 4.45", "hoch 3.48", "niedrig 4.41", "mittel 4.43", "hoch 3.60"],
    # 9.8.1: predict(modell_log, newdata, type = "response") für respid 1, 5, 6; AME aus Chunk logreg-ame
    "k09-ame": ["respid", "1", "5", "6", "educ_kat", "mittel", "hoch", "P(islam_hoch = 1)", "bei educ_kat =",
                "niedrig", "hoch - niedrig", "0.584", "0.394", "0.581", "0.316", "0.177", "0.314", "-0.27",
                "-0.22", "-0.252", "gewichteter Mittelwert", "modell_log |> marginal_effects()",
                "educ_kat: hoch vs. niedrig: AME = -0.252, p < 0.001 ***"],
}

STUFE_EN = {"niedrig": "low", "mittel": "medium", "hoch": "high"}
ALT_EN, NEU_EN = "OLD FEDERAL STATES", "NEW FEDERAL STATES"
ACHT_EN = [(a, STUFE_EN.get(b, b), c, {ALT: ALT_EN, NEU: NEU_EN}[d], {"MANN": "MALE", "FRAU": "FEMALE"}[e], f)
           for a, b, c, d, e, f in ACHT]

# Englische Fassung: Namen nach STYLE.md §13, Labels aus ZA8833, Koeffizientennamen wie R sie mit den englischen Labels
# druckt (Setup mit R/_common_en.R und R/prep_en.R); Zahlen wie im Deutschen
ERWARTET_KAP09_EN = {
    "k09-dummy": ["educ_cat", "educ_catmedium", "educ_cathigh", "internal", "medium", "high", "low", "1", "0",
                  "2", "8", "levels(allbus$educ_cat)", '[1] "low"    "medium" "high"', "Reference"],
    "k09-fallset": ["allbus_model <- allbus |>", "drop_na(islamophobia, educ_cat, age, eastwest, sex, populism)",
                    "islamophobia", "educ_cat", "age", "eastwest", "sex", "populism", "allbus", "allbus_model",
                    "5,246 × 593", "1,881 × 593", "without drop_na():", "only in m_base", ALT_EN, NEU_EN, "MALE",
                    "FEMALE", "low"]
                   + [v for r in ACHT_EN for v in r if v],
    "k09-augment": ["diag_df <- model |> augment()", "islamophobia", "educ_cat", "age", "…", "populism",
                    "(weights)", ".fitted", ".resid", ".hat", "3.333", "3.833", "medium", "high", "50", "45", "2.286",
                    "3.714", "1.252", "3.400", "3.829", "-0.067", "0.004", "0.005", "0.003", "0.808", "0.012 · 1",
                    "0.024 · 50", "0.603 · 2.286", "3.40", "(Intercept)", "educ_catmedium"],
    "k09-randmittel": ["oneway_anova()", "ancova()", "covariate = age", "3", "4", "5", "means", "marginal means",
                       "low 4.68", "medium 4.45", "high 3.48", "low 4.41", "medium 4.43", "high 3.60"],
    "k09-ame": ["respid", "1", "5", "6", "educ_cat", "medium", "high", "P(islamophobia_high = 1)", "at educ_cat =",
                "low", "high - low", "0.584", "0.394", "0.581", "0.316", "0.177", "0.314", "-0.27",
                "-0.22", "-0.252", "weighted mean", "model_log |> marginal_effects()",
                "educ_cat: high vs. low: AME = -0.252, p < 0.001 ***"],
}


def alle_texte(svg):
    return "\n".join("".join(e.itertext()) for e in ET.fromstring(svg).iter(NS + "text"))


def zoll(e, k):
    return float(e.get(k)) / 96


def texte_pos(svg):
    """(Text, x, y, Farbe) je <text>, in Zoll; x ist bei zentrierten Texten die Mitte."""
    return [("".join(e.itertext()), zoll(e, "x"), zoll(e, "y"), e.get("fill"))
            for e in ET.fromstring(svg).iter(NS + "text")]


def spalten(svg, werte, farben=None):
    """Gruppiert Texte aus `werte` (wahlweise nur in `farben`) nach x, je Spalte von oben nach unten."""
    sp = {}
    for t, x, y, f in texte_pos(svg):
        if t in werte and (farben is None or f in farben):
            sp.setdefault(round(x, 2), []).append((y, t))
    return [[t for _, t in sorted(v)] for _, v in sorted(sp.items())]


def rahmen(svg, stroke, fill=None):
    return [(zoll(r, "x"), zoll(r, "y"), zoll(r, "width"), zoll(r, "height"))
            for r in ET.fromstring(svg).iter(NS + "rect")
            if r.get("stroke") == stroke and (fill is None or r.get("fill") == fill)]


def innen(punkt, r):
    x, y = punkt
    rx, ry, rw, rh = r
    return rx < x < rx + rw and ry < y < ry + rh


def pfeile(svg):
    """Senkrechte Pfeile (Form wie lego.down_arrow: Polygon mit sieben Ecken) als (Spitze, Richtung, Umriss).
    Richtung "ab": Spitze = einziger Punkt mit größtem y; "auf": einziger Punkt mit kleinstem y.
    Umriss = (x0, y0, x1, y1) in Zoll."""
    out = []
    for p in ET.fromstring(svg).iter(NS + "polygon"):
        pts = [tuple(float(v) / 96 for v in q.split(",")) for q in p.get("points").split()]
        if len(pts) != 7:
            continue
        xs, ys = [q[0] for q in pts], [q[1] for q in pts]
        umriss = (min(xs), min(ys), max(xs), max(ys))
        for richtung, wahl in (("ab", max), ("auf", min)):
            spitze = wahl(pts, key=lambda q: q[1])
            if sum(1 for q in pts if abs(q[1] - spitze[1]) < 1e-6) == 1:
                out.append((spitze, richtung, umriss))
    return out


def ueberlappt(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


class TestKap09(unittest.TestCase):
    def test_kap09_constraints(self):
        import kap09
        self.assertEqual(set(kap09.FIGUREN), set(ERWARTET_KAP09))
        for name, fn in kap09.FIGUREN.items():
            svg = fn().svg()
            root = ET.fromstring(svg)
            breite = float(root.get("viewBox").split()[2])
            self.assertLessEqual(breite, 768, name)
            texte = alle_texte(svg)
            for wert in ERWARTET_KAP09[name]:
                self.assertIn(wert, texte, f"{name}: {wert}")

    def test_dummy(self):
        """Lila Turm educ_kat (Reihen 1, 2, 8) → zwei blaue 0/1-Türme, je grün umrandet; die Stufenleiste rechts
        nennt niedrig, mittel, hoch, das Schild Referenz steht neben niedrig."""
        import kap09
        svg = kap09.dummy().svg()
        stufen = {"niedrig", "mittel", "hoch"}
        self.assertEqual(spalten(svg, stufen), [["mittel", "hoch", "niedrig"], ["niedrig", "mittel", "hoch"]])
        self.assertEqual(spalten(svg, stufen, {SCHRIFT_TXT}), [["mittel", "hoch", "niedrig"],
                                                               ["niedrig", "mittel", "hoch"]])
        self.assertEqual(spalten(svg, {"0", "1"}, {SCHRIFT_NUM}), [["1", "0", "0"], ["0", "1", "0"]])
        self.assertEqual(spalten(svg, {"1", "2", "8"}, {GRAY}), [["1", "2", "8"]])
        pos = texte_pos(svg)
        kopf = {t: x for t, x, y, _ in pos if t in ("educ_katmittel", "educ_kathoch")}
        werte_x = sorted({round(x, 2) for t, x, y, f in pos if t in ("0", "1") and f == SCHRIFT_NUM})
        self.assertEqual(len(werte_x), 2)
        self.assertAlmostEqual(kopf["educ_katmittel"], werte_x[0], delta=0.05)
        self.assertAlmostEqual(kopf["educ_kathoch"], werte_x[1], delta=0.05)
        gruen = rahmen(svg, GREEN)
        self.assertEqual(len(gruen), 2)
        for wx in werte_x:
            drin = [r for r in gruen if all(innen((x, y - 0.05), r) for t, x, y, f in pos
                                            if t in ("0", "1") and f == SCHRIFT_NUM and round(x, 2) == wx)]
            self.assertEqual(len(drin), 1)
        ref = [(x, y) for t, x, y, _ in pos if t == "Referenz"]
        niedrig_leiste = max((x, y) for t, x, y, _ in pos if t == "niedrig")
        self.assertEqual(len(ref), 1)
        self.assertAlmostEqual(ref[0][1], niedrig_leiste[1], delta=0.05)
        self.assertGreater(ref[0][0], niedrig_leiste[0])

    def test_fallset(self):
        """Acht Reihen, sechs Türme; leere Steine wie in allbus; nur die Reihen 1 und 6 bleiben farbig, die anderen
        sind grau; Reihe 5 (nur populismus fehlt) ist orange umrandet."""
        import kap09
        svg = kap09.fallset().svg()
        pos = texte_pos(svg)
        nummern = sorted(((y, t) for t, x, y, f in pos if f == GRAY and t in {str(i) for i in range(1, 9)}
                          and x < 0.6))
        self.assertEqual([t for _, t in nummern], [str(i) for i in range(1, 9)])
        zeilen_y = [y for y, _ in nummern]
        werte = {v for r in ACHT for v in r if v}
        for i, reihe in enumerate(ACHT):
            in_reihe = [(x, t, f) for t, x, y, f in pos if t in werte and abs(y - zeilen_y[i]) < 0.05 and x > 0.6]
            self.assertEqual([t for _, t, _ in sorted(in_reihe)], [v for v in reihe if v], f"Reihe {i + 1}")
            farben = {f for _, _, f in in_reihe}
            if i in (0, 5):
                self.assertEqual(farben, {SCHRIFT_NUM, SCHRIFT_TXT}, f"Reihe {i + 1}")
            else:
                self.assertEqual(farben, {SCHRIFT_DIM}, f"Reihe {i + 1}")
        gestrichelt = [r for r in ET.fromstring(svg).iter(NS + "rect") if r.get("stroke-dasharray")]
        self.assertEqual(len(gestrichelt), sum(1 for r in ACHT for v in r if not v))
        orange = rahmen(svg, ORANGE)
        self.assertEqual(len(orange), 1)
        ox, oy, ow, oh = orange[0]
        self.assertTrue(oy < zeilen_y[4] < oy + oh)
        self.assertFalse(oy < zeilen_y[3] < oy + oh or oy < zeilen_y[5] < oy + oh)
        # die Notiz neben Reihe 5 ist eine Bedingung: ohne drop_na() wäre die Reihe nur in m_basis
        notiz = sorted((y, t) for t, x, y, _ in pos if x > ox + ow and oy - 0.3 < y < oy + oh + 0.3)
        self.assertEqual([t for _, t in notiz], ["ohne drop_na():", "nur in m_basis"])
        vorher = [(x, y) for t, x, y, _ in pos if t == "5,246 × 593"][0]
        nachher = [(x, y) for t, x, y, _ in pos if t == "1,881 × 593"][0]
        self.assertGreater(nachher[0], vorher[0])                          # allbus → drop_na() → allbus_modell
        self.assertLess(max(vorher[1], nachher[1]), min(zeilen_y))

    def test_augment(self):
        """Zwei Reihen von diagnose_df; .fitted und .resid je grün umrandet, .hat grau; Reihe 1 orange; darunter die
        Rechnung für Reihe 1, die mit den gezeigten Zahlen aufgeht."""
        import kap09
        svg = kap09.augment().svg()
        pos = texte_pos(svg)
        self.assertEqual(spalten(svg, {"3.400", "3.829"}, {SCHRIFT_NUM}), [["3.400", "3.829"]])
        self.assertEqual(spalten(svg, {"-0.067", "0.004"}, {SCHRIFT_NUM}), [["-0.067", "0.004"]])
        self.assertEqual(spalten(svg, {"0.005", "0.003"}, {SCHRIFT_DIM}), [["0.005", "0.003"]])
        self.assertEqual(spalten(svg, {"1.252"}, {SCHRIFT_DIM}), [["1.252", "1.252"]])
        self.assertEqual(spalten(svg, {"3.333", "3.833", "mittel", "hoch", "50", "45", "2.286", "3.714"},
                                 {SCHRIFT_NUM, SCHRIFT_TXT}),
                         [["3.333", "3.833"], ["mittel", "hoch"], ["50", "45"], ["2.286", "3.714"]])
        namen = ["islamophobie", "educ_kat", "age", "populismus", "(weights)", ".fitted", ".resid", ".hat"]
        y_stein = min(y for t, x, y, f in pos if f == SCHRIFT_NUM)
        koepfe = {t: x for t, x, y, _ in pos if t in namen and y < y_stein}         # Spaltenköpfe über den Steinen
        self.assertEqual(sorted(koepfe, key=koepfe.get), namen)
        punkte = sorted({round(x, 2) for t, x, y, f in pos if t == "…" and f == GRAY})
        self.assertEqual(len(punkte), 2)                    # eastwest und sex; .sigma, .cooksd, .std.resid
        self.assertTrue(koepfe["age"] < punkte[0] < koepfe["populismus"])
        self.assertGreater(punkte[1], koepfe[".hat"])
        gruen = rahmen(svg, GREEN)
        self.assertEqual(len(gruen), 2)
        for paar in (("3.400", "3.829"), ("-0.067", "0.004")):
            punkte = [(x, y - 0.05) for t, x, y, f in pos if t in paar and f == SCHRIFT_NUM]
            self.assertEqual(len([r for r in gruen if all(innen(p, r) for p in punkte)]), 1, paar)
        orange = rahmen(svg, ORANGE)
        self.assertEqual(len(orange), 1)
        y1 = [y for t, x, y, f in pos if t == "3.333" and f == SCHRIFT_NUM][0]
        y2 = [y for t, x, y, f in pos if t == "3.833"][0]
        self.assertTrue(innen((4.0, y1 - 0.05), orange[0]) and not innen((4.0, y2 - 0.05), orange[0]))
        # Rechenzeilen unter der Platte: Werte und Operatoren von links nach rechts, Beschriftungen grau darunter
        y_fit =[y for t, x, y, _ in pos if t == ".fitted" and y > y2][0]
        fit = [t for t, x, y, _ in sorted(pos, key=lambda p: p[1]) if abs(y - y_fit) < 0.02]
        self.assertEqual(fit, [".fitted", "=", "0.808", "+", "0.012 · 1", "+", "0.024 · 50", "+", "0.603 · 2.286",
                               "≈", "3.40"])
        y_res = [y for t, x, y, _ in pos if t == ".resid" and y > y2][0]
        res = [t for t, x, y, _ in sorted(pos, key=lambda p: p[1]) if abs(y - y_res) < 0.02]
        self.assertEqual(res, [".resid", "=", "3.333", "-", "3.400", "=", "-0.067"])
        for wert, lab, y0 in (("0.808", "(Intercept)", y_fit), ("0.012 · 1", "educ_katmittel", y_fit),
                              ("0.024 · 50", "age", y_fit), ("0.603 · 2.286", "populismus", y_fit),
                              ("3.333", "islamophobie", y_res), ("3.400", ".fitted", y_res)):
            xw = [x for t, x, y, _ in pos if t == wert and abs(y - y0) < 0.02][0]
            unter = [(x, f) for t, x, y, f in pos if t == lab and 0.1 < y - y0 < 0.4]
            self.assertEqual(len(unter), 1, lab)
            self.assertAlmostEqual(unter[0][0], xw, delta=0.01)
            self.assertEqual(unter[0][1], GRAY)
        self.assertEqual(round(0.808 + 0.012 * 1 + 0.024 * 50 + 0.603 * 2.286, 2), 3.40)
        self.assertAlmostEqual(3.333 - 3.400, -0.067, places=6)
        self.assertGreater(y_fit, y2)
        self.assertGreater(y_res, y_fit)

    def test_randmittel(self):
        """Zwei Lineale mit derselben Skala 3 bis 5; die Pfeile stehen genau bei den Mittelwerten, oben ohne, unten
        mit Kontrolle für Alter. Unten liegen niedrig (4.41) und mittel (4.43) fast gleich: niedrig zeigt von oben,
        mittel von unten auf das Lineal, kein Pfeil überdeckt einen anderen. Die gestrichelten Linien sind grau und
        führen für jede Gruppe vom oberen zum unteren Pfeil."""
        import kap09
        svg = kap09.randmittel().svg()
        root = ET.fromstring(svg)
        pos = texte_pos(svg)
        lineale = sorted(zoll(e, "y1") for e in root.iter(NS + "line")
                         if e.get("stroke") == INK and e.get("y1") == e.get("y2")
                         and zoll(e, "x2") - zoll(e, "x1") > 4)
        self.assertEqual(len(lineale), 2)
        striche = {t: (x, y) for t, x, y, f in pos if t in {"3", "4", "5"}}
        self.assertEqual(sorted(t for t, x, y, f in pos if t in {"3", "4", "5"}), ["3", "3", "4", "4", "5", "5"])
        x3, x5 = striche["3"][0], striche["5"][0]
        X = lambda v: x3 + (v - 3) / 2 * (x5 - x3)                      # noqa: E731
        pf = pfeile(svg)
        self.assertEqual(len(pf), 6)
        erwartet = [(lineale[0], [("hoch 3.48", 3.48, "ab"), ("mittel 4.45", 4.45, "ab"), ("niedrig 4.68", 4.68, "ab")]),
                    (lineale[1], [("hoch 3.60", 3.60, "ab"), ("niedrig 4.41", 4.41, "ab"), ("mittel 4.43", 4.43, "auf")])]
        spitze_von = {}
        for ly, gruppen in erwartet:
            hier = sorted((p for p in pf if abs(p[0][1] - ly) < 0.1), key=lambda p: p[0][0])
            self.assertEqual(len(hier), 3)
            for (spitze, richtung, umriss), (t, v, soll) in zip(hier, gruppen):
                self.assertAlmostEqual(spitze[0], X(v), delta=0.01, msg=t)
                self.assertEqual(richtung, soll, t)
                self.assertTrue(spitze[1] < ly if richtung == "ab" else spitze[1] > ly, t)
                lx, lyy = [(x, y) for tt, x, y, _ in pos if tt == t][0]
                self.assertTrue(umriss[1] - 0.05 < lyy < umriss[3] + 0.25, t)       # Beschriftung neben dem Pfeil
                spitze_von[t] = (spitze, richtung, umriss)
        for i, a in enumerate(pf):
            for b in pf[i + 1:]:
                self.assertFalse(ueberlappt(a[2], b[2]), (a[0], b[0]))
        # gestrichelte Linien: grau, je Gruppe vom oberen Pfeil zum unteren
        linien = [e for e in root.iter(NS + "line") if e.get("stroke-dasharray")]
        self.assertEqual(len(linien), 3)
        self.assertEqual({e.get("stroke") for e in linien}, {GRAY})
        enden = [sorted(((zoll(e, "x1"), zoll(e, "y1")), (zoll(e, "x2"), zoll(e, "y2"))), key=lambda q: q[1])
                 for e in linien]
        for gruppe, v1, v2 in (("hoch", 3.48, 3.60), ("mittel", 4.45, 4.43), ("niedrig", 4.68, 4.41)):
            treffer = [(o, u) for o, u in enden
                       if abs(o[0] - X(v1)) < 0.01 and abs(u[0] - X(v2)) < 0.01 and o[1] < lineale[1]]
            self.assertEqual(len(treffer), 1, gruppe)
            o, u = treffer[0]
            self.assertGreater(o[1], lineale[0])
            unten_t = [t for t in spitze_von if t.startswith(gruppe) and abs(spitze_von[t][0][1] - lineale[1]) < 0.1][0]
            spitze, richtung, umriss = spitze_von[unten_t]
            if richtung == "ab":
                self.assertLessEqual(u[1], umriss[1] + 0.01, gruppe)                # endet über dem Pfeil
            else:
                self.assertAlmostEqual(u[1], lineale[1], delta=0.03, msg=gruppe)    # endet am Lineal

    def test_ame(self):
        """Je Person die vorhergesagte Wahrscheinlichkeit mit niedriger und mit hoher Bildung, die Differenz als neuer,
        grün umrandeter Turm; rechts der gewichtete Mittelwert -0.252."""
        import kap09
        svg = kap09.ame().svg()
        pos = texte_pos(svg)
        niedrig, hoch = ["0.584", "0.394", "0.581"], ["0.316", "0.177", "0.314"]
        diff = ["-0.27", "-0.22", "-0.27"]
        self.assertEqual(spalten(svg, set(niedrig + hoch)), [niedrig, hoch])
        self.assertEqual(spalten(svg, set(diff)), [diff])
        self.assertEqual(diff, [f"{float(h) - float(n):.2f}" for n, h in zip(niedrig, hoch)])
        self.assertEqual(spalten(svg, {"1", "5", "6"}, {GRAY}), [["1", "5", "6"]])
        self.assertEqual(spalten(svg, {"mittel", "hoch"}, {SCHRIFT_TXT}), [["mittel", "hoch", "hoch"]])
        gruen = rahmen(svg, GREEN)
        self.assertEqual(len(gruen), 1)
        punkte = [(x, y - 0.05) for t, x, y, _ in pos if t in diff]
        self.assertTrue(all(innen(p, gruen[0]) for p in punkte))
        ame = [(x, y, f) for t, x, y, f in pos if t == "-0.252"]
        self.assertEqual(len(ame), 1)
        self.assertGreater(ame[0][0], max(x for x, _ in punkte))
        # die Kopfzeile steht in zwei Zeilen mittig über den Spalten niedrig und hoch und ist nicht breiter als sie
        from lego import text_width, MONO
        steine = [(zoll(r, "x"), zoll(r, "x") + zoll(r, "width")) for r in ET.fromstring(svg).iter(NS + "rect")
                  if r.get("fill") == "#85B7EB" and any(zoll(r, "x") < x < zoll(r, "x") + zoll(r, "width")
                                                        for t, x, y, _ in pos if t in ("0.584", "0.316"))]
        links, rechts = min(a for a, _ in steine), max(b for _, b in steine)
        kopf = sorted((y, t, x) for t, x, y, f in pos if t in ("P(islam_hoch = 1)", "bei educ_kat ="))
        self.assertEqual([t for _, t, _ in kopf], ["P(islam_hoch = 1)", "bei educ_kat ="])
        for _, t, x in kopf:
            self.assertAlmostEqual(x, (links + rechts) / 2, delta=0.02, msg=t)
            self.assertLessEqual(text_width(t, MONO, 10), rechts - links, t)
        y_spalten = min(y for t, x, y, _ in pos if t == "niedrig")
        self.assertLess(kopf[-1][0], y_spalten)

    def test_en_schluessel_gleich(self):
        self.assertEqual(set(ERWARTET_KAP09_EN), set(ERWARTET_KAP09))

    def test_englische_texte(self):
        import kap09
        import sprache
        sprache.setze("en")
        try:
            for name, fn in kap09.FIGUREN.items():
                svg = fn().svg()
                breite = float(ET.fromstring(svg).get("viewBox").split()[2])
                self.assertLessEqual(breite, 768, name)
                texte = alle_texte(svg)
                for wert in ERWARTET_KAP09_EN[name]:
                    self.assertIn(wert, texte, f"{name}: {wert}")
        finally:
            sprache.setze("de")

    def test_kein_deutscher_rest(self):
        import check_en
        import kap09
        import sprache
        sprache.setze("en")
        try:
            for name, fn in kap09.FIGUREN.items():
                self.assertEqual(check_en.deutsch_reste(alle_texte(fn().svg())), [], name)
        finally:
            sprache.setze("de")

    def test_en_ohne_deutsche_namen(self):
        """Keine deutschen Namen aus STYLE.md §13 in den englischen Abbildungen."""
        import re
        import kap09
        import sprache
        sprache.setze("en")
        try:
            for name, fn in kap09.FIGUREN.items():
                texte = alle_texte(fn().svg())
                for alt in ("educ_kat", "islamophobie", "populismus", "allbus_modell", "m_basis", "diagnose_df",
                            "modell_log", "islam_hoch", "Referenz", "niedrig", "mittel", "hoch"):
                    self.assertIsNone(re.search(rf"\b{alt}", texte), f"{name}: {alt}")
        finally:
            sprache.setze("de")

    def test_deutsch_unveraendert(self):
        import kap09
        import sprache
        sprache.setze("de")
        for name, fn in kap09.FIGUREN.items():
            texte = alle_texte(fn().svg())
            for wert in ERWARTET_KAP09[name]:
                self.assertIn(wert, texte, f"{name}: {wert}")


if __name__ == "__main__":
    unittest.main()
