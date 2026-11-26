"""Tests für den Sprachschalter der Abbildungsskripte (sprache.py, en.py, build.py --en)."""
import os
import sys
import tempfile
import unittest

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)

import build
import en
import sprache


class SpracheTest(unittest.TestCase):
    def tearDown(self):
        sprache.setze("de")

    def test_deutsch_unveraendert(self):
        sprache.setze("de")
        self.assertEqual(sprache.aktuell(), "de")
        self.assertEqual(sprache.t("Einlesen"), "Einlesen")

    def test_englisch_aus_tabelle(self):
        en.EN["Einlesen (Test)"] = "Reading in"
        try:
            sprache.setze("en")
            self.assertEqual(sprache.aktuell(), "en")
            self.assertEqual(sprache.t("Einlesen (Test)"), "Reading in")
        finally:
            del en.EN["Einlesen (Test)"]

    def test_fehlender_eintrag_ist_fehler(self):
        sprache.setze("en")
        with self.assertRaises(KeyError) as ctx:
            sprache.t("Gibt es nicht (Test)")
        self.assertIn("Gibt es nicht (Test)", str(ctx.exception))

    def test_unbekannte_sprache(self):
        with self.assertRaises(ValueError):
            sprache.setze("fr")
        self.assertEqual(sprache.aktuell(), "de")

    def test_build_en_zielordner(self):
        echtes_ziel = os.path.join(os.path.dirname(HIER), "Bilder", "figuren", "en")
        vorher = sorted(os.listdir(echtes_ziel)) if os.path.isdir(echtes_ziel) else None
        with tempfile.TemporaryDirectory() as tmp:
            rc = build.main(["--en", "k04-einlesen"], ziel=tmp)
            self.assertEqual(rc, 0)
            self.assertTrue(os.path.isfile(os.path.join(tmp, "k04-einlesen.svg")))
        nachher = sorted(os.listdir(echtes_ziel)) if os.path.isdir(echtes_ziel) else None
        self.assertEqual(vorher, nachher)
        self.assertEqual(sprache.aktuell(), "de")

    def test_build_en_baut_nur_sprachfaehige_module(self):
        import kap01
        import kap02
        import kap03
        import kap04
        import kap05
        import kap06
        import kap07
        import kap08
        namen = {**kap01.FIGUREN, **kap02.FIGUREN, **kap03.FIGUREN, **kap04.FIGUREN, **kap05.FIGUREN,
                 **kap06.FIGUREN, **kap07.FIGUREN, **kap08.FIGUREN}     # sprachfähige Module
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(build.main(["--en"], ziel=tmp), 0)
            self.assertEqual(sorted(os.listdir(tmp)), sorted(f"{n}.svg" for n in namen))
        for modul in (kap01, kap02, kap03, kap04, kap05, kap06, kap07, kap08):
            self.assertTrue(modul.SPRACHFAEHIG)
        self.assertEqual(sprache.aktuell(), "de")

    def test_englische_svgs_ohne_deutsche_reste(self):
        import re
        import check_en
        ordner = os.path.join(os.path.dirname(HIER), "Bilder", "figuren", "en")
        zeilen = []
        for datei in sorted(os.listdir(ordner)):
            if not datei.endswith(".svg"):
                continue
            with open(os.path.join(ordner, datei), encoding="utf-8") as f:
                svg = f.read()
            for m in re.finditer(r"<text[^>]*>(.*?)</text>", svg, re.S):
                zeilen.append(re.sub(r"<[^>]+>", "", m.group(1)))
        self.assertTrue(zeilen)
        self.assertEqual(check_en.deutsch_reste("\n".join(zeilen)), [])


if __name__ == "__main__":
    unittest.main()
