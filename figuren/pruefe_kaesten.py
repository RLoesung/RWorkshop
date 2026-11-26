"""Prüft ein Kapitel auf die Kastenregeln vom 26.11.2026 (Prototyp „weniger Kästen“).

Aufruf: python3 figuren/pruefe_kaesten.py <kapitel.qmd>  (im Projektordner; vergleicht mit dem Stand vor dem Umbau, Commit 9267f80)

Regeln:
- Lehrkästen nur in vier Typen plus Forschungsjournal.
  offen:      ::: {.callout-warning}  **Vorsicht: Titel.** …
              ::: {.callout-tip}      **SPSS → R: Titel.** …
              ::: {.callout-note}     **Forschungsjournal: Titel** …
  zugeklappt: ::: {.callout-note collapse="true"}       + Zeile  ## Hintergrund: Titel
              ::: {.callout-important collapse="true"}  + Zeile  ## mariposa-Tipp: Titel
- Nie zwei Lehrkästen direkt untereinander (nur Leerzeilen dazwischen).
- Überschriften außerhalb von Kästen und Code bleiben wie in der Ausgangsfassung (Abschnittsnummern).
- Code-Chunks bleiben inhaltlich gleich (Verschieben erlaubt, Ändern nicht).
Übungen (title="Übung …"), Lösungen und Auflösungen zählen nicht als Lehrkästen.
"""
import re
import subprocess
import sys
from collections import Counter

BASIS = "9267f80"
OFFEN = {"Vorsicht": "warning", "SPSS → R": "tip", "Forschungsjournal": "note"}
ZU = {"Hintergrund": "note", "mariposa-Tipp": "important"}


def zerlege(text):
    zeilen = text.split("\n")
    kaesten, chunks, ueberschriften = [], [], []
    i, in_code, chunk = 0, False, None
    while i < len(zeilen):
        z = zeilen[i]
        if re.match(r"^\s*(```|~~~)", z):
            if not in_code:
                in_code, chunk = True, [z]
            else:
                in_code = False
                chunk.append(z)
                chunks.append("\n".join(chunk))
            i += 1
            continue
        if in_code:
            chunk.append(z)
            i += 1
            continue
        m = re.match(r"^(:{3,})\s*\{\.callout-(\w+)([^}]*)\}", z)
        if m:
            j, code = i + 1, False
            while j < len(zeilen):
                if re.match(r"^\s*(```|~~~)", zeilen[j]):
                    code = not code
                elif not code and re.match(r"^:{3,}\s*$", zeilen[j]):
                    break
                j += 1
            innen = zeilen[i + 1:j]
            # Chunks im Kasten mitzählen
            c_in, cc = False, []
            for zz in innen:
                if re.match(r"^\s*(```|~~~)", zz):
                    if not c_in:
                        c_in, cc = True, [zz]
                    else:
                        c_in = False
                        cc.append(zz)
                        chunks.append("\n".join(cc))
                elif c_in:
                    cc.append(zz)
            kaesten.append(dict(start=i, ende=j, klasse=m.group(2), attr=m.group(3), innen=innen))
            i = j + 1
            continue
        if re.match(r"^#{1,6}\s", z):
            ueberschriften.append(z.strip())
        i += 1
    return zeilen, kaesten, chunks, ueberschriften


def fett(text):
    ohne_code = re.sub(r"```.*?```", "", text, flags=re.S)
    ohne_code = re.sub(r"`[^`\n]*`", "", ohne_code)
    return re.findall(r"\*\*[^*\n]+\*\*", ohne_code)


def main(pfad):
    text = open(pfad, encoding="utf-8").read()
    alt = subprocess.run(["git", "show", f"{BASIS}:{pfad}"], capture_output=True, text=True).stdout
    zeilen, kaesten, chunks, ueb = zerlege(text)
    _, kaesten_alt, chunks_alt, ueb_alt = zerlege(alt)
    fehler = []
    lehr = []
    for k in kaesten:
        if re.search(r'title="(Übung|Lösung|Auflösung)', k["attr"]):
            continue
        lehr.append(k)
        erste = next((z for z in k["innen"] if z.strip()), "")
        zeile = k["start"] + 1
        if 'collapse="true"' in k["attr"]:
            m = re.match(r"^## (Hintergrund|mariposa-Tipp): \S", erste)
            if not m:
                fehler.append(f"Z.{zeile}: zugeklappter Kasten braucht als erste Zeile '## Hintergrund: …' oder '## mariposa-Tipp: …', ist: {erste[:60]!r}")
            elif ZU[m.group(1)] != k["klasse"]:
                fehler.append(f"Z.{zeile}: {m.group(1)} gehört in .callout-{ZU[m.group(1)]}, ist .callout-{k['klasse']}")
            k["typ"] = m.group(1) if m else "?"
        else:
            m = re.match(r"^\*\*(Vorsicht|SPSS → R|Forschungsjournal)[:.]", erste)
            if not m:
                fehler.append(f"Z.{zeile}: offener Kasten muss mit **Vorsicht: …**, **SPSS → R: …** oder **Forschungsjournal: …** beginnen, ist: {erste[:70]!r}")
                k["typ"] = "?"
            else:
                k["typ"] = m.group(1)
                if OFFEN[m.group(1)] != k["klasse"]:
                    fehler.append(f"Z.{zeile}: {m.group(1)} gehört in .callout-{OFFEN[m.group(1)]}, ist .callout-{k['klasse']}")
    for a, b in zip(lehr, lehr[1:]):
        if not "\n".join(zeilen[a["ende"] + 1:b["start"]]).strip():
            fehler.append(f"Z.{a['start'] + 1} und Z.{b['start'] + 1}: zwei Lehrkästen direkt untereinander ({a.get('typ')} / {b.get('typ')})")
    if alt and ueb != ueb_alt:
        weg = [u for u in ueb_alt if u not in ueb]
        neu = [u for u in ueb if u not in ueb_alt]
        fehler.append(f"Überschriften geändert. Fehlen: {weg} | neu: {neu}")
    if alt and Counter(chunks) != Counter(chunks_alt):
        weg = list((Counter(chunks_alt) - Counter(chunks)).elements())
        neu = list((Counter(chunks) - Counter(chunks_alt)).elements())
        fehler.append(f"Code-Chunks geändert. Fehlen: {[c.splitlines()[0] + ' …' + c.splitlines()[1][:40] if len(c.splitlines()) > 1 else c for c in weg]} | neu: {[c.splitlines()[0] for c in neu]}")
    typen = Counter(k.get("typ") for k in lehr)
    zu = sum(1 for k in lehr if 'collapse="true"' in k["attr"])
    lehr_alt = [k for k in kaesten_alt if not re.search(r'title="(Übung|Lösung|Auflösung)', k["attr"])]
    print(f"{pfad}: Lehrkästen {len(lehr_alt)} -> {len(lehr)} (offen {len(lehr) - zu}, zu {zu}) | Typen {dict(typen)} | fett {len(fett(alt))} -> {len(fett(text))}")
    for f in fehler:
        print("  FEHLER", f)
    print("  ok" if not fehler else f"  {len(fehler)} Fehler")
    return len(fehler)


if __name__ == "__main__":
    sys.exit(1 if sum(main(p) for p in sys.argv[1:]) else 0)
