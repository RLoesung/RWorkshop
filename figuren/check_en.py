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
CODE_WOERTER = re.compile(
    r"\b(und|der|die|das|nicht|mit|ist|sind|wird|oder|auch|wenn|für|nur|ohne|eine|einen|von|bei"
    r"|mittelwerte?|standardabweichung|häufigkeit(en)?|tabelle|anzahl|fehlende[nr]?|werte?|daten"
    r"|erstelle|berechne|zeige|zeigt|lade|spalten?|ergebnis(se)?|gruppen?|alter|geschlecht"
    r"|bildung|einkommen|auswahl|beispiel|kapitel|zeile|zeilen|filtere|sortiere|wähle|variablen)\b",
    re.I)
AUSGABE_WOERTER = re.compile(
    r"\b(STIMME|KEINE ANGABE|WEISS NICHT|WEIß NICHT|TNZ|MANN|FRAU|DATENFEHLER|VERWEIGERT"
    r"|TRIFFT|NICHT ERWERBSTÄTIG|ANGABE)\b")
ZAUN = re.compile(r"^\s*(`{3,}|~{3,})")


def abtasten(qmd):
    """Liefert (Zeilennummer, Zeile, art, info) je Zeile. art ist "text" (außerhalb von Code-Blöcken),
    "auf" (öffnender Zaun, info = Info-String), "code" (im Block, info = Info-String des Blocks)
    oder "zu" (schließender Zaun). Ein Zaun schließt nur mit gleich vielen oder mehr gleichen
    Zeichen und ohne Info-String; innere Zäune eines längeren Blocks sind Code."""
    offen = None  # (zeichen, anzahl, info)
    for nr, zeile in enumerate(qmd.splitlines(), 1):
        m = ZAUN.match(zeile)
        if offen is None:
            if m:
                info = zeile.strip()[len(m.group(1)):].strip()
                offen = (m.group(1)[0], len(m.group(1)), info)
                yield nr, zeile, "auf", info
            else:
                yield nr, zeile, "text", None
        elif m and m.group(1)[0] == offen[0] and len(m.group(1)) >= offen[1] \
                and zeile.strip() == m.group(1):
            offen = None
            yield nr, zeile, "zu", None
        else:
            yield nr, zeile, "code", offen[2]


def ohne_code(qmd):
    """Liefert (Zeilennummer, Zeile) für alle Zeilen außerhalb von Code-Blöcken."""
    return [(nr, z) for nr, z, art, _ in abtasten(qmd) if art == "text"]


def r_zeilen(qmd):
    """Liefert (Zeilennummer, Zeile) für alle Zeilen innerhalb von R-Chunks (```{r ...})."""
    return [(nr, z) for nr, z, art, info in abtasten(qmd)
            if art == "code" and re.match(r"\{r[\s,}]", info)]


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
    for _, _, art, info in abtasten(qmd):
        m = art == "auf" and re.match(r"\{r[ ,]*([^,}\s=]*)(?=[,}\s])", info)
        if m:
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


def _zellen(markdown):
    """Liefert je Ausgabeblock (fenced div mit Klasse cell-output) (erste Codezeile der Zelle, Textzeilen)."""
    bloecke = []
    offen = None
    tiefe = 0
    code = ""
    erwarte_code = False
    for zeile in markdown.splitlines():
        m = re.match(r"^\s*(:{3,})\s*(.*)$", zeile)
        if m and m.group(2):
            if offen is None and "cell-output" in m.group(2):
                offen = []
                tiefe = 1
            elif offen is not None:
                tiefe += 1
            elif re.match(r"\{\.cell[\s}]", m.group(2)):
                code = ""
            continue
        if m and not m.group(2):
            if offen is not None:
                tiefe -= 1
                if tiefe == 0:
                    bloecke.append((code, offen))
                    offen = None
            continue
        if ZAUN.match(zeile):
            erwarte_code = offen is None and ".cell-code" in zeile
            continue
        if offen is not None:
            offen.append(zeile)
        elif erwarte_code and zeile.strip():
            code = zeile.strip()[:60]
            erwarte_code = False
    return bloecke


def ausgabe_codes(markdown):
    """Erste Codezeile der Zelle je Ausgabeblock."""
    return [code for code, _ in _zellen(markdown)]


def ausgabe_zahlen(markdown):
    """Zahlen je Ausgabeblock (fenced div mit Klasse cell-output) in Reihenfolge."""
    bloecke = []
    for _, zeilen in _zellen(markdown):
        zahlen = []
        for zeile in zeilen:
            zeile = re.sub(r"^\s*\[\d+\]", "", zeile)
            zahlen.extend(z.rstrip(".,") for z in ZAHL.findall(zeile))
        bloecke.append(zahlen)
    return bloecke


def vergleiche_zahlen(de, en, codes=None):
    """Vergleicht die Zahlen je Block; codes nennt je englischem Block die erste Codezeile."""
    if len(de) != len(en):
        return [f"Ausgabeblöcke: de {len(de)}, en {len(en)}"]
    meldungen = []
    for i, (d, e) in enumerate(zip(de, en), 1):
        if d != e:
            diff = [(x, y) for x, y in zip(d, e) if x != y]
            n = f"{len(d)} vs. {len(e)} Zahlen" if len(d) != len(e) else ""
            wo = f" ({codes[i - 1]})" if codes and codes[i - 1] else ""
            meldungen.append(f"Ausgabeblock {i}{wo}: {n} {diff[:5]}".replace("  ", " ").strip())
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


def r_teile(zeile):
    """Zerlegt eine R-Zeile in die Texte von Zeichenketten und den Kommentar.
    Code außerhalb davon bleibt unberücksichtigt. Zeilen mit #| sind ganz Option und zählen als Text."""
    if zeile.lstrip().startswith("#|"):
        return [zeile.lstrip()[2:]]
    teile = []
    i = 0
    n = len(zeile)
    while i < n:
        c = zeile[i]
        if c in "\"'":
            j = i + 1
            while j < n and zeile[j] != c:
                j += 2 if zeile[j] == "\\" else 1
            teile.append(zeile[i + 1:j])
            i = j + 1
        elif c == "`":
            j = zeile.find("`", i + 1)
            i = n if j < 0 else j + 1
        elif c == "#":
            teile.append(zeile[i + 1:])
            break
        else:
            i += 1
    return teile


def code_reste(qmd):
    """Deutsche Wörter und Umlaute in Kommentaren, Zeichenketten und #|-Optionen von R-Chunks."""
    meldungen = []
    for nr, zeile in r_zeilen(qmd):
        for teil in r_teile(zeile):
            if UMLAUT.search(teil) or CODE_WOERTER.search(teil):
                meldungen.append(f"Zeile {nr}: {zeile.strip()[:100]}")
                break
    return meldungen


def ausgabe_reste(markdown):
    """Umlaute und deutsche ALLBUS-Label-Wörter in den Ausgabeblöcken einer Freeze-Datei."""
    meldungen = []
    for i, (code, zeilen) in enumerate(_zellen(markdown), 1):
        for zeile in zeilen:
            if UMLAUT.search(zeile) or AUSGABE_WOERTER.search(zeile):
                meldungen.append(f"Ausgabeblock {i} ({code}): {zeile.strip()[:100]}")
                break
    return meldungen


def mechanik(qmd):
    """Meldet deutsche Setup-Dateien, Abbildungspfade ohne /en/ und ein fehlendes output-file."""
    meldungen = []
    for nr, zeile in enumerate(qmd.splitlines(), 1):
        if re.search(r"source\(\s*[\"']R/(_common|prep)\.R[\"']", zeile):
            meldungen.append(f"Zeile {nr}: deutsche Setup-Datei: {zeile.strip()[:100]}")
        for m in re.finditer(r"Bilder/figuren/(?!en/)(k[^\s)\"']*)", zeile):
            meldungen.append(f"Zeile {nr}: Abbildung ohne /en/: {m.group(1)}")
    kopf = re.match(r"---\n(.*?)\n---", qmd, re.S)
    if not (kopf and re.search(r"^output-file:\s*\S", kopf.group(1), re.M)):
        meldungen.append("output-file fehlt im YAML-Kopf")
    return meldungen


def filtere(name, meldungen, erwartet):
    """Trennt Meldungen in offene und erwartete (Teilstring-Treffer aus erwartet[name])."""
    offen, bekannt = [], []
    for m in meldungen:
        grund = next((g for teil, g in erwartet.get(name, []) if teil in m), None)
        if grund is None:
            offen.append(m)
        else:
            bekannt.append((m, grund))
    return offen, bekannt


def pruefe(name, root):
    de = os.path.join(root, f"{name}.qmd")
    en = os.path.join(root, f"{name}.en.qmd")
    meldungen = []
    if not os.path.exists(de):
        return [f"{name}: {name}.qmd fehlt"]
    if not os.path.exists(en):
        return [f"{name}: {name}.en.qmd fehlt"]
    with open(de, encoding="utf-8") as f:
        text_de = f.read()
    with open(en, encoding="utf-8") as f:
        text_en = f.read()
    meldungen += vergleiche_aufbau(aufbau(text_de), aufbau(text_en))
    fd = os.path.join(root, "_freeze", name, "execute-results", "html.json")
    fe = os.path.join(root, "_freeze", f"{name}.en", "execute-results", "html.json")
    if os.path.exists(fd) and os.path.exists(fe):
        md_de, md_en = lies_freeze(fd), lies_freeze(fe)
        meldungen += vergleiche_zahlen(ausgabe_zahlen(md_de), ausgabe_zahlen(md_en), ausgabe_codes(md_en))
        meldungen += ["Deutscher Rest in der Ausgabe, " + m for m in ausgabe_reste(md_en)]
    meldungen += ["Deutscher Rest, " + m for m in deutsch_reste(text_en)]
    meldungen += ["Deutscher Rest im Code, " + m for m in code_reste(text_en)]
    meldungen += ["Mechanik, " + m for m in mechanik(text_en)]
    return [f"{name}: {m}" for m in meldungen]


def main(argv=None, root=None, erwartet=None):
    args = list(sys.argv[1:] if argv is None else argv)
    root = root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if erwartet is None:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from erwartet_en import ERWARTET as erwartet
    if not args:
        args = [os.path.basename(p)[:-len(".en.qmd")]
                for p in sorted(glob.glob(os.path.join(root, "*.en.qmd")))]
    offen, bekannt = [], []
    for name in args:
        name = name.removesuffix(".qmd").removesuffix(".en")
        o, b = filtere(name, pruefe(name, root), erwartet)
        offen += o
        bekannt += b
    for m in offen:
        print(m)
    for m, grund in bekannt:
        print(f"erwartet: {m}  [{grund}]")
    print(f"{len(offen)} Meldungen, {len(bekannt)} erwartet")
    return 1 if offen else 0


if __name__ == "__main__":
    sys.exit(main())
