"""Prüft, dass die committeten SVGs zum Quelltext passen, und dass figuren/en.py keine doppelten Schlüssel hat."""
import ast
import filecmp
import os
import sys
import contextlib
import io
import tempfile
import unittest
from collections import Counter

HIER = os.path.dirname(os.path.abspath(__file__))
PROJEKT = os.path.dirname(HIER)
sys.path.insert(0, HIER)

import build  # noqa: E402


def baue(argumente, ziel):
    with contextlib.redirect_stdout(io.StringIO()):
        build.main(argumente, ziel=ziel)


def vergleiche(ziel, vorhanden):
    abweichend = []
    for name in sorted(os.listdir(ziel)):
        if not name.endswith(".svg"):
            continue
        alt = os.path.join(vorhanden, name)
        if not os.path.exists(alt) or not filecmp.cmp(os.path.join(ziel, name), alt, shallow=False):
            abweichend.append(name)
    return abweichend


class FigurenAktuell(unittest.TestCase):
    def test_deutsche_svgs_sind_aktuell(self):
        with tempfile.TemporaryDirectory() as tmp:
            baue([], tmp)
            self.assertEqual(vergleiche(tmp, os.path.join(PROJEKT, "Bilder", "figuren")), [])

    def test_englische_svgs_sind_aktuell(self):
        with tempfile.TemporaryDirectory() as tmp:
            baue(["--en"], tmp)
            self.assertEqual(vergleiche(tmp, os.path.join(PROJEKT, "Bilder", "figuren", "en")), [])


class EnglischeTabelle(unittest.TestCase):
    def test_keine_doppelten_schluessel(self):
        with open(os.path.join(HIER, "en.py"), encoding="utf-8") as f:
            baum = ast.parse(f.read())
        doppelt = []
        for knoten in ast.walk(baum):
            if isinstance(knoten, ast.Dict):
                schluessel = [k.value for k in knoten.keys if isinstance(k, ast.Constant)]
                doppelt += [k for k, n in Counter(schluessel).items() if n > 1]
        self.assertEqual(doppelt, [])


if __name__ == "__main__":
    unittest.main()
