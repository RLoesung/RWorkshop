"""Erzeugt die Bausteine-Abbildungen nach Bilder/figuren/ (Vertrag: BILDER.md).

Jedes Modul figuren/kapNN.py hat ein Dict FIGUREN {dateiname: funktion → Canvas}.
Aufruf: python3 figuren/build.py [--en] [NAME …]   (ohne Namen: alle)
Mit --en entstehen die englischen Fassungen in Bilder/figuren/en/; dabei werden nur Module gebaut,
die SPRACHFAEHIG = True setzen (alle Texte laufen über sprache.t()).
"""
import glob
import importlib
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
ZIEL = os.path.join(os.path.dirname(HIER), "Bilder", "figuren")
sys.path.insert(0, HIER)

import sprache  # noqa: E402


def alle_figuren(nur_sprachfaehig=False):
    figs = {}
    for p in sorted(glob.glob(os.path.join(HIER, "kap[0-9][0-9].py"))):
        modul = importlib.import_module(os.path.basename(p)[:-3])
        if nur_sprachfaehig and not getattr(modul, "SPRACHFAEHIG", False):
            continue
        figs.update(modul.FIGUREN)
    return figs


def main(argv=None, ziel=None):
    namen = list(sys.argv[1:] if argv is None else argv)
    englisch = "--en" in namen
    namen = [n for n in namen if n != "--en"]
    if ziel is None:
        ziel = os.path.join(ZIEL, "en") if englisch else ZIEL
    os.makedirs(ziel, exist_ok=True)
    figs = alle_figuren(nur_sprachfaehig=englisch)
    sprache.setze("en" if englisch else "de")
    try:
        for name, fn in figs.items():
            if namen and name not in namen:
                continue
            pfad = os.path.join(ziel, f"{name}.svg")
            fn().save(pfad)
            print(f"{os.path.relpath(pfad, os.path.dirname(HIER))}")
    finally:
        sprache.setze("de")
    return 0


if __name__ == "__main__":
    sys.exit(main())
