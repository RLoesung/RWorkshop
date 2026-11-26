"""Kapitelkarten im Vorwort (Design „Baukasten“): je Kapitel Nummer, Titel und die ersten zwei Lernziele.

Baut den Abschnitt „Die Kapitel im Überblick“ in index.qmd aus den Kapitel-Dateien neu
(mit --en: „Overview of the chapters“ in index.en.qmd aus den *.en.qmd). Nach einer Änderung an
Kapiteltiteln oder Lernzielen aufrufen: python3 figuren/kapitelkarten.py [--en]
"""
import glob
import html
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
# Steinfarben je Kapitel, wie in theme.scss (body[data-kapitel])
FARBEN = ["#FFE7A3", "#BFE3F7", "#CDEFD9", "#DCD6F8", "#FFD2BC", "#F7C9DA", "#C6ECE8", "#FFE7A3", "#E6D3F2", "#D8EBC4", "#FFC9C2"]
FARBEN2 = ["#EFC867", "#86B9DE", "#8FCBA6", "#A79FE2", "#F0A27E", "#E39AB6", "#86CBC3", "#EFC867", "#BE9EDB", "#A8CC85", "#EC9286"]
TEXTE = {
    "de": dict(kopf="## Die Kapitel im Überblick {-}", danach="## Wie liest du dieses Buch? {-}",
               ziele="## Was du nach diesem Kapitel kannst", index="index.qmd", endung=".qmd"),
    "en": dict(kopf="## Overview of the chapters {-}", danach="## How to read this book {-}",
               ziele="## What you will be able to do after this chapter", index="index.en.qmd", endung=".en.qmd"),
}


def _inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    return re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)


def karten(sprache="de", root=ROOT):
    tx = TEXTE[sprache]
    dateien = sorted(f for f in glob.glob(os.path.join(root, "[0-9][0-9]-*.qmd")) if f.endswith(".en.qmd") == (sprache == "en"))
    out = []
    for i, f in enumerate(dateien, start=1):
        zeilen = open(f, encoding="utf-8").read().splitlines()
        kopf = next(z for z in zeilen if z.startswith("# "))
        titel = re.sub(r"\s*\{#.*\}\s*$", "", kopf.lstrip("# ")).strip()
        ziele, drin = [], False
        for z in zeilen:
            if z.startswith(tx["ziele"]):
                drin = True
                continue
            if drin and z.startswith("## "):
                break
            if drin and z.startswith("- "):
                ziele.append(_inline(z[2:].strip()))
            if len(ziele) == 2:
                break
        href = os.path.basename(f).replace(tx["endung"], ".html")
        lis = "".join(f"<li>{z}</li>" for z in ziele)
        out.append(f'<a class="kapitel-karte" href="{href}" style="--kk:{FARBEN[i]};--kk2:{FARBEN2[i]}">'
                   f'<span class="nr">{i}</span><div class="titel">{_inline(titel)}</div><ul>{lis}</ul></a>')
    return f'{tx["kopf"]}\n\n```{{=html}}\n<div class="kapitel-raster">{"".join(out)}</div>\n```\n\n'


def main(en=False, root=ROOT):
    tx = TEXTE["en" if en else "de"]
    p = os.path.join(root, tx["index"])
    t = open(p, encoding="utf-8").read()
    if tx["kopf"] in t:
        t = t[:t.index(tx["kopf"])] + t[t.index(tx["danach"]):]
    assert t.count(tx["danach"]) == 1
    t = t.replace(tx["danach"], karten("en" if en else "de", root) + tx["danach"])
    open(p, "w", encoding="utf-8").write(t)
    print(f"Kapitelkarten in {tx['index']} geschrieben")


if __name__ == "__main__":
    import sys
    main(en="--en" in sys.argv[1:])
