"""Tests für die Abbildungen von Kap. 8 „Latente Strukturen“ (BILDER.md §6)."""
import os
import sys
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

NS = "{http://www.w3.org/2000/svg}"
GREEN, GRAY, INK, CARD = "#36A266", "#6E7882", "#1E2D3C", "#FAF7F1"
SCHRIFT_NUM, SCHRIFT_DIM = "#042C53", "#A8A69E"

ITEMS = ["mm01", "mm02r", "mm03", "mm04", "mm05r", "mm06"]
# Antworten der ersten drei Befragten, die alle sechs Items beantwortet haben (nach R/prep.R, mm02 und mm05 umgepolt)
ANTWORTEN = {"1": ["5", "5", "4", "2", "2", "2"], "5": ["2", "4", "4", "3", "5", "6"],
             "6": ["3", "5", "3", "7", "2", "3"]}

# Werte aus den Chunks neben den Abbildungen (ALLBUS 2023, R 4.5.3, mariposa 0.7.4), nach dem Setup-Chunk von Kap. 8
ERWARTET_KAP08 = {
    # Konzept-Kasten in 8.1 (kein Chunk): respid 1, 5, 6
    "k08-latenter-faktor": ["Islamfeindlichkeit", "nicht gemessen", "gemessen", "respid"] + ITEMS,
    # Chunks efa-vor (KMO), efa-bartlett, efa-msa (per_item, gerundet), efa-1 (Eigenwerte, Ladungen)
    "k08-ergebnisobjekt": ["efa_vor", "$loadings", "$eigenvalues", "$kmo", "$bartlett", "$overall", "$per_item",
                           "$chi_sq", "$df", "$p_value", "PC1", "0.811", "0.664", "0.753", "0.769", "0.657",
                           "3.281", "0.833", "0.555", "0.479", "0.439", "0.412", "0.862", "0.857", "0.876",
                           "0.874", "0.849", "0.851", "0.867", "6532.633", "15", "0", "…",
                           "efa_vor$kmo$per_item"],
    # Chunk reliability-summary, Tabelle Item-Total Statistics, Zeile mm05r
    "k08-item-total": ["respid", "Summe ohne", "nicht in der Summe", "Corrected Item-Total", "0.520", "18", "19",
                       "21"] + ITEMS,
}


def alle_texte(svg):
    return "\n".join("".join(e.itertext()) for e in ET.fromstring(svg).iter(NS + "text"))


def zoll(e, k):
    return float(e.get(k)) / 96


def texte_pos(svg):
    """(Text, x, y, Farbe) je <text>, in Zoll; x ist bei zentrierten Texten die Mitte."""
    return [("".join(e.itertext()), zoll(e, "x"), zoll(e, "y"), e.get("fill"))
            for e in ET.fromstring(svg).iter(NS + "text")]


def spalten(svg, werte):
    """Gruppiert Texte aus `werte` nach x (Spalten von links nach rechts), je Spalte von oben nach unten."""
    sp = {}
    for t, x, y, _ in texte_pos(svg):
        if t in werte:
            sp.setdefault(round(x, 2), []).append((y, t))
    return [[t for _, t in sorted(v)] for _, v in sorted(sp.items())]


def rahmen(svg, stroke, fill=None):
    return [(zoll(r, "x"), zoll(r, "y"), zoll(r, "width"), zoll(r, "height"))
            for r in ET.fromstring(svg).iter(NS + "rect")
            if r.get("stroke") == stroke and (fill is None or r.get("fill") == fill)]


class TestKap08(unittest.TestCase):
    def test_kap08_constraints(self):
        import kap08
        self.assertEqual(set(kap08.FIGUREN), set(ERWARTET_KAP08))
        for name, fn in kap08.FIGUREN.items():
            svg = fn().svg()
            root = ET.fromstring(svg)
            breite = float(root.get("viewBox").split()[2])
            self.assertLessEqual(breite, 768, name)
            texte = alle_texte(svg)
            for wert in ERWARTET_KAP08[name]:
                self.assertIn(wert, texte, f"{name}: {wert}")

    def test_latenter_faktor(self):
        """Sechs Item-Türme mit den Antworten von respid 1, 5, 6; der Faktor ist eine gestrichelte Ellipse ohne Werte
        (weder weiß noch eckig wie ein leerer Stein), von der je ein Pfeil auf jeden Turm zeigt."""
        import kap08
        svg = kap08.latenter_faktor().svg()
        ziffern = {str(i) for i in range(1, 8)}
        soll = [["1", "5", "6"]] + [[ANTWORTEN[r][j] for r in ("1", "5", "6")] for j in range(6)]
        self.assertEqual(spalten(svg, ziffern), soll)
        root = ET.fromstring(svg)
        ell = list(root.iter(NS + "ellipse"))
        self.assertEqual(len(ell), 1)
        e = ell[0]
        self.assertTrue(e.get("stroke-dasharray"))
        self.assertNotEqual(e.get("fill"), "#FFFFFF")
        cx, cy, rx, ry = (zoll(e, k) for k in ("cx", "cy", "rx", "ry"))
        drin = [t for t, x, y, _ in texte_pos(svg) if abs(x - cx) < rx and abs(y - cy) < ry]
        self.assertEqual(drin, ["Islamfeindlichkeit"])
        koepfe = {t: (x, y) for t, x, y, _ in texte_pos(svg) if t in ITEMS}
        spitzen = []
        for p in root.iter(NS + "polygon"):
            pts = [tuple(float(v) / 96 for v in q.split(",")) for q in p.get("points").split()]
            if len(pts) == 3:                              # Spitze: die Ecke gegenüber der kürzesten Seite
                gegen = lambda i: (pts[(i + 1) % 3][0] - pts[(i + 2) % 3][0]) ** 2 + \
                    (pts[(i + 1) % 3][1] - pts[(i + 2) % 3][1]) ** 2   # noqa: E731
                spitzen.append(pts[min(range(3), key=gegen)])
        self.assertEqual(len(spitzen), 6)
        for it in ITEMS:
            kx, ky = koepfe[it]
            treffer = [q for q in spitzen if abs(q[0] - kx) < 0.06 and cy + ry < q[1] < ky]
            self.assertEqual(len(treffer), 1, it)

    def test_ergebnisobjekt(self):
        """efa_vor als Kiste: Fächer in Listenreihenfolge, danach graue Auslassungspunkte; $kmo und $bartlett sind
        selbst Kisten; der Turm $per_item ist grün umrandet."""
        import kap08
        svg = kap08.ergebnisobjekt().svg()
        pos = texte_pos(svg)
        dollar = [(t, x, y) for t, x, y, _ in pos if t.startswith("$")]
        y_oben = min(y for _, _, y in dollar)
        aussen = [t for t, x, y in sorted(dollar, key=lambda d: d[1]) if abs(y - y_oben) < 0.01]
        self.assertEqual(aussen, ["$loadings", "$eigenvalues", "$kmo", "$bartlett"])
        x_bart = [x for t, x, y in dollar if t == "$bartlett"][0]
        punkte = [(x, f) for t, x, y, f in pos if t == "…"]
        self.assertEqual(len(punkte), 1)
        self.assertGreater(punkte[0][0], x_bart)
        self.assertEqual(punkte[0][1], GRAY)
        kisten = sorted(rahmen(svg, INK, CARD), key=lambda r: -r[2])
        self.assertEqual(len(kisten), 3)                                    # außen, $kmo, $bartlett
        ax, ay, aw, ah = kisten[0]
        for innen, kopf, namen in [(None, "$kmo", ["$overall", "$per_item"]),
                                   (None, "$bartlett", ["$chi_sq", "$df", "$p_value"])]:
            xk = [x for t, x, y in dollar if t == kopf][0]
            ik = [k for k in kisten[1:] if abs(k[0] + k[2] / 2 - xk) < 0.05]
            self.assertEqual(len(ik), 1, kopf)
            ix, iy, iw, ih = ik[0]
            self.assertTrue(ax < ix and ix + iw < ax + aw and ay < iy and iy + ih <= ay + ah + 1e-6)
            drin = [t for t, x, y in sorted(dollar, key=lambda d: d[1]) if ix < x < ix + iw and iy < y < iy + ih]
            self.assertEqual(drin, namen)
        self.assertEqual(spalten(svg, {"0.857", "0.876", "0.874", "0.849", "0.851", "0.867"}),
                         [["0.857", "0.876", "0.874", "0.849", "0.851", "0.867"]])
        self.assertEqual(spalten(svg, {"0.811", "0.664", "0.753", "0.769", "0.657"}),
                         [["0.811", "0.664", "0.753", "0.769", "0.657", "0.769"]])
        self.assertEqual(spalten(svg, {"3.281", "0.833", "0.555", "0.479", "0.439", "0.412"}),
                         [["3.281", "0.833", "0.555", "0.479", "0.439", "0.412"]])
        gruen = rahmen(svg, GREEN)
        self.assertEqual(len(gruen), 1)
        gx, gy, gw, gh = gruen[0]
        per_item = [(x, y) for t, x, y, _ in pos if t in {"0.857", "0.876", "0.874", "0.849", "0.851", "0.867"}]
        self.assertTrue(all(gx < x < gx + gw and gy < y < gy + gh for x, y in per_item))
        self.assertFalse(any(gx < x < gx + gw and gy < y < gy + gh for t, x, y, _ in pos if t in {"0.862", "0.811"}))

    def test_item_total(self):
        """Die Summe der anderen fünf Items je Reihe steht neben mm05r; in der Platte ist mm05r grau (nicht in der
        Summe), daneben blau als zweiter Turm der Korrelation."""
        import kap08
        svg = kap08.item_total().svg()
        zahlen = {str(i) for i in range(1, 30)}
        sp = spalten(svg, zahlen)
        soll = [["1", "5", "6"]] + [[ANTWORTEN[r][j] for r in ("1", "5", "6")] for j in range(6)]
        summen = [str(sum(int(v) for j, v in enumerate(ANTWORTEN[r]) if j != 4)) for r in ("1", "5", "6")]
        self.assertEqual(summen, ["18", "19", "21"])
        self.assertEqual(sp, soll + [summen, soll[5]])
        pos = texte_pos(svg)
        xs = sorted({round(x, 2) for t, x, y, _ in pos if t in zahlen})
        farbe = lambda xx: {f for t, x, y, f in pos if t in zahlen and round(x, 2) == xx}   # noqa: E731
        self.assertEqual(farbe(xs[5]), {SCHRIFT_DIM})                      # mm05r in der Platte: grau
        self.assertEqual(farbe(xs[8]), {SCHRIFT_NUM})                      # mm05r rechts: blau
        self.assertEqual(farbe(xs[7]), {SCHRIFT_NUM})                      # Summe
        y_wert = [y for t, x, y, _ in pos if t == "0.520"][0]
        y_steine = max(y for t, x, y, _ in pos if t in zahlen)
        self.assertGreater(y_wert, y_steine)


if __name__ == "__main__":
    unittest.main()
