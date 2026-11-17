"""Prüft die Einbindung der Bausteine-Abbildungen in den Kapiteln (BILDER.md §5.5).

Jede Bildzeile mit Bilder/figuren/ braucht #fig-…, .lightbox, ein nicht leeres fig-alt,
eine vorhandene Datei und einen Verweis @fig-… im selben Kapitel.
Aufruf: python3 figuren/check_qmd.py [--root DIR] [DATEI …]   (ohne Dateien: alle 0*.qmd)
"""
import glob
import os
import re
import sys

BILD = re.compile(r"!\[[^\]]*\]\((Bilder/figuren/[^)\s]+)\)(\{[^}]*\})?")


def check(path, root):
    fehler = []
    inhalt = open(path, encoding="utf-8").read()
    for m in BILD.finditer(inhalt):
        datei, attr = m.group(1), m.group(2) or ""
        wo = f"{os.path.basename(path)}: {datei}"
        idm = re.search(r"#(fig-[\w-]+)", attr)
        if not idm:
            fehler.append(f"{wo}: kein #fig-…")
        elif f"@{idm.group(1)}" not in inhalt:
            fehler.append(f"{wo}: kein Verweis @{idm.group(1)} im Kapitel")
        if ".lightbox" not in attr:
            fehler.append(f"{wo}: keine Klasse .lightbox")
        alt = re.search(r'fig-alt="([^"]*)"', attr)
        if not alt or not alt.group(1).strip():
            fehler.append(f"{wo}: fig-alt fehlt oder ist leer")
        if not os.path.exists(os.path.join(root, datei)):
            fehler.append(f"{wo}: Datei fehlt")
    return fehler


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if args[:1] == ["--root"]:
        root, args = args[1], args[2:]
    dateien = args or sorted(glob.glob(os.path.join(root, "0*.qmd")))
    fehler = [f for p in dateien for f in check(p, root)]
    for f in fehler:
        print(f)
    print(f"{len(fehler)} Fehler in {len(dateien)} Dateien")
    return 1 if fehler else 0


if __name__ == "__main__":
    sys.exit(main())
