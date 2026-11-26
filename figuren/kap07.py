"""Abbildungen für Kap. 7 „Uni- und Bivariate Analyse“ (BILDER.md §6). Werte aus den Buch-Chunks.

Alle Werte stammen aus ALLBUS 2023 (ALLBUS2023.sav), geprüft mit R 4.5.3 und mariposa 0.7.4, nach dem
Setup-Chunk von Kap. 7 (R/prep.R, educ_kat, eastwest als Faktor). Kap. 7 rechnet gewichtet; jede Zahl kommt aus
der Ausgabe des Chunks neben dem Bild.
"""
from lego import (Canvas, R, P, text, rect, stein, eyebrow, connector, vline, INK, GRAY, CARDLINE, PALE, LIGHT,
                  ORANGE, MONO, RT)
from kap03 import mono, notiz, platte
from kap04 import codezeile, kopf
from kap05 import klammer
import sprache
from sprache import t as tr

SPRACHFAEHIG = True  # alle Texte laufen über tr(); build.py --en baut dieses Modul


# 7.2 Gewichtung aus dem neuen Chunk `gewichtung-eastwest`. Die Steine sind die ersten sechs Befragten aus dem
# Westen (Zeilen 1, 2, 3, 5, 6, 7) und die ersten drei aus dem Osten (Zeilen 4, 14, 18) mit ihrem wghtpew;
# zusammen sind das alle sechs Werte, die distinct(eastwest, wghtpew) zeigt. N und Prozente aus frequency().
WEST = ["1.25", "1.20", "1.20", "1.21", "1.25", "1.20"]
OST = ["0.545", "0.501", "0.541"]


def gewichtung():
    s = Canvas(7.9, 4.0)
    einheit, h, pitch = 1.15, 0.22, 0.29
    tops = [0.98 + i * pitch for i in range(6)]
    ost0 = tops[-1] + h + 0.27
    tops += [ost0 + i * pitch for i in range(3)]
    unten = tops[-1] + h
    gruppen = [("ALTE BUNDESLAENDER", tops[0], tops[5] + h), ("NEUE BUNDESLAENDER", tops[6], unten)]
    for name, y0, y1 in gruppen:
        text(s, 0.1, y0, 1.7, y1 - y0, mono(tr(name), size=10, align=RT), anchor="middle")
    spalten = [(1.95, tr("UNGEWICHTET"), "frequency(eastwest)", ["1"] * 9, [("3567", "67.99 %"), ("1679", "32.01 %")]),
               (4.55, tr("GEWICHTET"), "frequency(eastwest, weights = wghtpew)", WEST + OST,
                [("4363", "83.16 %"), ("883", "16.84 %")])]
    for x, titel, code, werte, ergebnis in spalten:
        eyebrow(s, x, 0.12, 3.3, titel, size=10.5)
        text(s, x, 0.42, 3.35, 0.28, mono(code, size=10, align="start"))
        breiten = [einheit * float(w) for w in werte]
        for y, w, t in zip(tops, breiten, werte):
            stein(s, x, y, w, h, "num", t, size=10)
        rechts = x + max(breiten)
        platte(s, x - 0.1, unten + 0.07, rechts - x + 0.2)
        for (name, y0, y1), (n, prozent) in zip(gruppen, ergebnis):
            klammer(s, rechts + 0.1, y0, y1)
            text(s, rechts + 0.3, y0, 1.1, y1 - y0, [P(R(prozent, size=12, bold=True)),
                                                     P(R(f"N = {n}", font=MONO, size=10, color=GRAY), sb=2)],
                 anchor="middle")
    return s


# 7.5.1 Zeilenprozente aus dem Chunk `crosstab` --------------------------------------------------
STUFEN = [("niedrig", PALE), ("mittel", LIGHT), ("hoch", ORANGE)]
ZEILEN = [("ALTE BUNDESLAENDER", [22.2, 27.6, 50.3]), ("NEUE BUNDESLAENDER", [13.3, 41.8, 44.9]),
          ("Total", [20.6, 30.0, 49.4])]


def zeilenprozente():
    s = Canvas(7.6, 2.85)
    text(s, 0.15, 0.12, 7.4, 0.28, codezeile(tr("allbus |> crosstab(eastwest, educ_kat, weights = wghtpew)"), size=10.5))
    bx, bw, bh = 1.95, 4.6, 0.42
    lx = bx
    for name, farbe in STUFEN:
        rect(s, lx, 0.62, 0.22, 0.2, farbe, INK, 0.5)
        text(s, lx + 0.3, 0.57, 1.0, 0.3, [P(R(tr(name), size=11))], anchor="middle")
        lx += 1.2
    for k, (name, prozente) in enumerate(ZEILEN):
        y = 1.0 + k * 0.6 + (0.12 if name == "Total" else 0)
        if name == "Total":
            connector(s, 0.15, y - 0.15, 7.45, y - 0.15, color=CARDLINE, width=0.75)
        text(s, 0.1, y, 1.75, bh, mono(tr(name) if name != "Total" else name, size=10, align=RT), anchor="middle")
        x = bx
        for (stufe, farbe), p in zip(STUFEN, prozente):
            w = bw * p / 100
            rect(s, x, y, w, bh, farbe, INK, 0.75)
            text(s, x, y, w, bh, mono(f"{p:.1f}%", size=10.5), anchor="middle")
            x += w
        text(s, bx + bw + 0.1, y, 0.9, bh, mono("100.0%", size=10.5, color=GRAY, align="start"), anchor="middle")
    return s


# 7.4.1 Häufigkeiten aus dem Chunk `freq-mm`, Tabelle zu mm01 ---------------------------------------
# Der Turm ist ein Schema: zehn Steine, nach Wert sortiert wie die Zeilen der Tabelle. Anteile wie in der Ausgabe:
# 2 von 10 Steinen haben den Wert 1 (Raw % 20.53), 2 von 6 gefüllten (Valid % 31.66), 4 von 10 sind leer (35.16 %).
# N und Totals sind gewichtete Summen, gerundet; 1077.005 / 3401.347 = 31.66 % (mit den gerundeten Zahlen 31.67).
MM01 = ["1", "1", "2", "4", "5", "7", "", "", "", ""]


def klammer_links(s, x, y0, y1, color=GRAY, w=0.1):
    """Eckige Klammer links neben den Steinen von y0 bis y1 (öffnet nach rechts)."""
    connector(s, x + w, y0, x, y0, color=color, width=1.25)
    vline(s, x, y0, y1, color=color, width=1.25)
    connector(s, x + w, y1, x, y1, color=color, width=1.25)


def haeufigkeit():
    s = Canvas(7.5, 4.05)
    text(s, 0.15, 0.12, 7.3, 0.28, codezeile("allbus |> frequency(mm01:mm06, weights = wghtpew)", size=10.5))
    h, pitch, top, w = 0.2, 0.27, 1.12, 0.55
    ys = [top + i * pitch for i in range(len(MM01))]
    unten_1, unten_gueltig, unten = ys[1] + h, ys[5] + h, ys[-1] + h
    spalten = [(0.15, "PROZENT", "Raw % = 20.53", [("Total", "5246", ys[0], unten, INK)]),
               (3.7, "GÜLTIGE PROZENT", "Valid % = 31.66",
                [("Total valid", "3401", ys[0], unten_gueltig, INK), ("Total missing", "1845", ys[6], unten, GRAY)])]
    for x0, titel, prozent, klammern in spalten:
        eyebrow(s, x0, 0.5, 3.3, tr(titel), size=10.5)
        tx = x0 + 1.65
        kopf(s, tx, w, 0.8, "mm01")
        for y, v in zip(ys, MM01):
            stein(s, tx, y, w, h, "num" if v else "na", v, size=10)
        platte(s, tx - 0.1, unten + 0.07, w + 0.2)
        klammer_links(s, tx - 0.2, ys[0], unten_1, color=INK)
        text(s, x0 - 0.05, ys[0] - 0.08, tx - 0.25 - x0, unten_1 - ys[0] + 0.16,
             [P(R("N = 1077", font=MONO, size=10.5, bold=True), align=RT),
              P(R(prozent, font=MONO, size=10.5, bold=True, color=INK), align=RT, sb=1)], anchor="middle")
        for name, n, y0, y1, farbe in klammern:
            klammer(s, tx + w + 0.1, y0, y1, color=farbe)
            zeilen = [P(R(name, font=MONO, size=10, color=GRAY)), P(R(n, font=MONO, size=11, bold=True, color=farbe))]
            if name == "Total missing":
                zeilen.append(P(R(tr("zählen nicht mit"), size=10.5, italic=True, color=GRAY), sb=2))
            text(s, tx + w + 0.32, y0, 1.6, y1 - y0, zeilen, anchor="middle")
    vline(s, 3.55, 0.5, unten + 0.1, color=CARDLINE, width=0.75)
    return s


FIGUREN = {
    "k07-gewichtung": gewichtung,
    "k07-zeilenprozente": zeilenprozente,
    "k07-haeufigkeit": haeufigkeit,
}
