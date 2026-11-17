"""Prüft, dass keine bestehende Abschnittsnummer des Buchs verschoben wurde.

Vergleicht die nummerierten Überschriften in docs/0*.html mit einem Referenzstand
(Standard: der Commit „Phase 6w“). Jede alte Nummer muss es noch geben, mit gleich
beginnendem Titel. Neue Nummern sind erlaubt.
Aufruf: python3 figuren/check_sections.py [--ref COMMIT]
"""
import glob
import html
import os
import re
import subprocess
import sys

H = re.compile(r'<h([2-5])[^>]*data-number="([\d.]+)"[^>]*>(.*?)</h\1>', re.S)


def sections(src):
    out = {}
    for m in H.finditer(src):
        t = html.unescape(re.sub(r"<[^>]+>", "", m.group(3)))
        out[m.group(2)] = re.sub(r"^\s*[\d.]+\s*", "", t).strip()
    return out


def compare(alt, neu):
    fehler = []
    for nr, titel in alt.items():
        t = neu.get(nr)
        if t is None or not t.startswith(titel[:12]):
            fehler.append(f"{nr}: vorher «{titel}», jetzt «{t}»")
    return fehler


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if args[:1] == ["--ref"]:
        ref = args[1]
    else:
        ref = subprocess.run(["git", "log", "--grep=Phase 6w", "-1", "--format=%H"], cwd=root,
                             capture_output=True, text=True).stdout.strip()
    fehler = []
    for p in sorted(glob.glob(os.path.join(root, "docs", "0*.html"))):
        rel = os.path.relpath(p, root)
        alt = subprocess.run(["git", "show", f"{ref}:{rel}"], cwd=root, capture_output=True, text=True).stdout
        neu = open(p, encoding="utf-8").read()
        fehler += [f"{os.path.basename(p)} {f}" for f in compare(sections(alt), sections(neu))]
    for f in fehler:
        print(f)
    print(f"{len(fehler)} verschobene Abschnitte (Referenz {ref[:7]})")
    return 1 if fehler else 0


if __name__ == "__main__":
    sys.exit(main())
