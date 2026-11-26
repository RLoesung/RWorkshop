"""Prüft die englische Fassung gegen die deutsche: Aufbau, Zahlen in Ausgaben, deutsche Reste.

Aufruf: python3 figuren/check_en.py [NAME ...]
NAME ist index oder z. B. 04-Datenimport; ohne Angabe werden alle *.en.qmd geprüft.
Vergleicht X.qmd mit X.en.qmd und, wenn beide da sind, die Freeze-Ausgaben.
"""
import glob
import json
import os
import re
import sys

KASTEN = ["callout-note", "callout-tip", "callout-important", "callout-warning", "callout-caution"]
ZAHL = re.compile(r"-?\d[\d.,]*")
DEUTSCHE_WOERTER = re.compile(r"\b(und|der|die|das|nicht|mit|ist)\b", re.I)
UMLAUT = re.compile(r"[äöüßÄÖÜ]")
ZAUN = re.compile(r"^\s*(`{3,}|~{3,})")


def ohne_code(qmd):
    """Liefert (Zeilennummer, Zeile) für alle Zeilen außerhalb von Code-Blöcken."""
    out = []
    zaun = None
    for nr, zeile in enumerate(qmd.splitlines(), 1):
        m = ZAUN.match(zeile)
        if m:
            z = m.group(1)
            if zaun is None:
                zaun = z[0] * 3
            elif z[0] == zaun[0]:
                zaun = None
            continue
        if zaun is None:
            out.append((nr, zeile))
    return out


def aufbau(qmd):
    a = {f"h{i}": 0 for i in range(1, 5)}
    a.update({k: 0 for k in KASTEN})
    a["abbildungen"] = 0
    a["kaesten-mit-titel"] = 0
    a["chunks"] = 0
    ids = set()
    for _, zeile in ohne_code(qmd):
        m = re.match(r"^(#{1,4})\s", zeile)
        if m:
            a[f"h{len(m.group(1))}"] += 1
        a["abbildungen"] += len(re.findall(r"!\[", zeile))
        if re.match(r"^\s*:{3,}", zeile):
            for k in KASTEN:
                if f".{k}" in zeile:
                    a[k] += 1
                    if "title=" in zeile:
                        a["kaesten-mit-titel"] += 1
        ids.update(re.findall(r"\{#([\w:.-]+)", zeile))
    for m in re.finditer(r"^\s*```\{r[ ,]*([^,}\s=]*)(?=[,}\s])", qmd, re.M):
        a["chunks"] += 1
        if m.group(1):
            ids.add(m.group(1))
    a["ids"] = ids
    return a


def vergleiche_aufbau(de, en):
    meldungen = []
    for k, v in de.items():
        if k == "ids":
            continue
        if en.get(k) != v:
            meldungen.append(f"Aufbau {k}: de {v}, en {en.get(k)}")
    fehlt = sorted(de["ids"] - en["ids"])
    zuviel = sorted(en["ids"] - de["ids"])
    if fehlt:
        meldungen.append("IDs fehlen in en: " + ", ".join(fehlt))
    if zuviel:
        meldungen.append("IDs nur in en: " + ", ".join(zuviel))
    return meldungen


def lies_freeze(pfad):
    with open(pfad, encoding="utf-8") as f:
        return json.load(f)["result"]["markdown"]


def ausgabe_zahlen(markdown):
    """Zahlen je Ausgabeblock (fenced div mit Klasse cell-output) in Reihenfolge."""
    bloecke = []
    offen = None
    tiefe = 0
    for zeile in markdown.splitlines():
        m = re.match(r"^\s*(:{3,})\s*(.*)$", zeile)
        if m and m.group(2):
            if offen is None and "cell-output" in m.group(2):
                offen = []
                tiefe = 1
            elif offen is not None:
                tiefe += 1
            continue
        if m and not m.group(2):
            if offen is not None:
                tiefe -= 1
                if tiefe == 0:
                    bloecke.append(offen)
                    offen = None
            continue
        if offen is not None and not ZAUN.match(zeile):
            zeile = re.sub(r"^\s*\[\d+\]", "", zeile)
            offen.extend(z.rstrip(".,") for z in ZAHL.findall(zeile))
    return bloecke


def vergleiche_zahlen(de, en):
    meldungen = []
    if len(de) != len(en):
        meldungen.append(f"Ausgabeblöcke: de {len(de)}, en {len(en)}")
    for i, (d, e) in enumerate(zip(de, en), 1):
        if d != e:
            diff = [(x, y) for x, y in zip(d, e) if x != y]
            n = f"{len(d)} vs. {len(e)} Zahlen" if len(d) != len(e) else ""
            meldungen.append(f"Ausgabeblock {i}: {n} {diff[:5]}".replace("  ", " ").strip())
    return meldungen


def deutsch_reste(qmd):
    meldungen = []
    for nr, zeile in ohne_code(qmd):
        text = re.sub(r"`[^`]*`", " ", zeile)
        text = re.sub(r"https?://\S+", " ", text)
        text = re.sub(r"\]\([^)]*\)", "] ", text)
        if UMLAUT.search(text) or DEUTSCHE_WOERTER.search(text):
            meldungen.append(f"Zeile {nr}: {zeile.strip()[:100]}")
    return meldungen


def pruefe(name, root):
    de = os.path.join(root, f"{name}.qmd")
    en = os.path.join(root, f"{name}.en.qmd")
    meldungen = []
    if not os.path.exists(de):
        return [f"{name}: {name}.qmd fehlt"]
    with open(de, encoding="utf-8") as f:
        text_de = f.read()
    with open(en, encoding="utf-8") as f:
        text_en = f.read()
    meldungen += vergleiche_aufbau(aufbau(text_de), aufbau(text_en))
    fd = os.path.join(root, "_freeze", name, "execute-results", "html.json")
    fe = os.path.join(root, "_freeze", f"{name}.en", "execute-results", "html.json")
    if os.path.exists(fd) and os.path.exists(fe):
        meldungen += vergleiche_zahlen(ausgabe_zahlen(lies_freeze(fd)), ausgabe_zahlen(lies_freeze(fe)))
    meldungen += ["Deutscher Rest, " + m for m in deutsch_reste(text_en)]
    return [f"{name}: {m}" for m in meldungen]


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if not args:
        args = [os.path.basename(p)[:-len(".en.qmd")]
                for p in sorted(glob.glob(os.path.join(root, "*.en.qmd")))]
    alle = []
    for name in args:
        alle += pruefe(name.removesuffix(".qmd").removesuffix(".en"), root)
    for m in alle:
        print(m)
    print(f"{len(alle)} Meldungen")
    return 1 if alle else 0


if __name__ == "__main__":
    sys.exit(main())
