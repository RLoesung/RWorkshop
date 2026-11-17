"""Erzeugt die Bausteine-Abbildungen nach Bilder/figuren/ (Vertrag: BILDER.md).

Jedes Modul figuren/kapNN.py hat ein Dict FIGUREN {dateiname: funktion → Canvas}.
Aufruf: python3 figuren/build.py [NAME …]   (ohne Namen: alle)
"""
import glob
import importlib
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
ZIEL = os.path.join(os.path.dirname(HIER), "Bilder", "figuren")
sys.path.insert(0, HIER)


def alle_figuren():
    figs = {}
    for p in sorted(glob.glob(os.path.join(HIER, "kap[0-9][0-9].py"))):
        figs.update(importlib.import_module(os.path.basename(p)[:-3]).FIGUREN)
    return figs


def main(argv=None):
    namen = list(sys.argv[1:] if argv is None else argv)
    os.makedirs(ZIEL, exist_ok=True)
    figs = alle_figuren()
    for name, fn in figs.items():
        if namen and name not in namen:
            continue
        pfad = os.path.join(ZIEL, f"{name}.svg")
        fn().save(pfad)
        print(f"{os.path.relpath(pfad, os.path.dirname(HIER))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
