"""Abbildungen für Kap. 5 „Daten transformieren und Skalen bilden“ (BILDER.md §6). Werte aus den Buch-Chunks.

Alle Werte stammen aus ALLBUS 2023 (ALLBUS2023.sav), geprüft mit R 4.5.3 und mariposa 0.7.4, nach denselben
Schritten, die das Kapitel vor dem jeweiligen Chunk ausführt. Wo ein Bild „die ersten Werte“ zeigt, sind es die
ersten Zeilen des Datensatzes (head()); welche genau, steht beim Bild.
"""
from lego import (Canvas, R, P, text, rect, card, eyebrow, label_box, stein, schild, arrow, down_arrow, outline,
                  connector, vline, numdot, codebox, text_width, INK, GRAY, GREEN, ORANGE, CARDLINE, DARKORANGE,
                  WHITE, PALE, MONO, C, RT)
from kap03 import mono, notiz, platte
from kap04 import lstein, lstein_breite, saeule, kopf, punkte, codezeile


def code(zeilen, size=10.5, color=INK):
    """Code-Zeilen untereinander; jedes |> grün (auch am Zeilenende)."""
    ps = []
    for z in zeilen:
        teile = (z + " ").split(" |> ")
        runs = []
        for i, teil in enumerate(teile):
            if i:
                runs.append(R(" |>" if i == len(teile) - 1 and not teil.strip() else " |> ", font=MONO, size=size,
                              bold=True, color=GREEN))
            if teil.strip() or (i == 0 and teil):
                runs.append(R(teil.rstrip(" ") if i == len(teile) - 1 else teil, font=MONO, size=size, bold=True,
                              color=color))
        ps.append(P(*runs, ls=size * 1.4))
    return ps


# 5.2.1 mutate() aus dem Chunk `mutate`; die ersten drei Werte von age ------------------------
def mutate_fig():
    s = Canvas(6.6, 2.75)
    text(s, 0.15, 0.12, 6.4, 0.28,
         codezeile("allbus |> select(age) |> mutate(geburtsjahr = 2023 - age) |> head(3)", size=10.5))
    h, top, gap = 0.36, 1.05, 0.07
    ax, aw, gx, gw = 0.45, 0.8, 3.05, 1.0
    kopf(s, ax, aw, 0.5, "age", "<dbl+lbl>")
    kopf(s, gx, gw, 0.5, "geburtsjahr", "<dbl>")
    alter, jahr = ["50", "51", "69"], ["1973", "1972", "1954"]
    unten = saeule(s, ax, top, aw, h, "num", alter, size=12)
    saeule(s, gx, top, gw, h, "num", jahr, size=12)
    for i, a in enumerate(alter):
        y = top + i * (h + gap)
        text(s, ax + aw + 0.12, y, 1.0, h, mono(f"2023 - {a}", size=10.5, color=GRAY), anchor="middle")
        arrow(s, ax + aw + 1.17, y + h / 2 - 0.09, w=0.38, h=0.18, color=GRAY)
    platte(s, 0.3, unten + 0.07, gx + gw + 0.15 - 0.3)
    outline(s, gx - 0.07, top - 0.11, gw + 0.14, 3 * (h + gap) + 0.08, color=GREEN, lw=1.75)
    text(s, gx + gw + 0.25, top + h + gap - 0.02, 1.7, 0.4, notiz("neuer Turm", size=10.5, color=GREEN, align="start"),
         anchor="middle")
    return s


# 5.2.1 Zuweisung: Chunk `mutate` ohne und mit `allbus <-`; die ersten drei Werte ---------------
def zuweisung():
    s = Canvas(7.6, 3.45)
    h, top, gap = 0.3, 1.95, 0.07
    for x0, titel, zeilen, gespeichert in [
            (0.15, "OHNE <-", ["allbus |>", "  mutate(geburtsjahr = 2023 - age)"], False),
            (3.95, "MIT <-", ["allbus <- allbus |>", "  mutate(geburtsjahr = 2023 - age)"], True)]:
        eyebrow(s, x0, 0.12, 3.4, titel, color=GREEN if gespeichert else GRAY)
        text(s, x0, 0.42, 3.5, 0.5, code(zeilen, size=10.5))
        schild(s, x0, 1.05, "allbus", w=1.0)
        text(s, x0 + 1.12, 1.08, 1.6, 0.3, mono("5,246 × 580" if gespeichert else "5,246 × 579", size=11,
                                                color=GRAY, align="start"))
        ax, gx = x0 + 0.2, x0 + 1.6
        kopf(s, ax, 0.7, 1.5, "age")
        kopf(s, gx, 0.9, 1.5, "geburtsjahr")
        unten = saeule(s, ax, top, 0.7, h, "num", ["50", "51", "69"], size=11)
        punkte(s, ax + 0.77, top + h + gap - 0.03, w=0.5)
        saeule(s, gx, top, 0.9, h, "num" if gespeichert else "dim", ["1973", "1972", "1954"], size=11)
        platte(s, x0 + 0.05, unten + 0.07, gx + 1.05 - x0)
        if gespeichert:
            outline(s, gx - 0.07, top - 0.11, 1.04, 3 * (h + gap) + 0.08, color=GREEN, lw=1.75)
        text(s, gx + 1.05, top + h + gap - 0.05, 1.0, h + 0.1,
             notiz("gespeichert" if gespeichert else "nur angezeigt", size=10.5,
                   color=GREEN if gespeichert else GRAY, align="start"), anchor="middle")
    vline(s, 3.8, 0.15, 3.3, color=CARDLINE, width=0.75)
    return s


# 5.2.2 Reihenfolge in case_when() aus dem Chunk `case-when-falle`; die ersten fünf Werte von age --
def case_when_fig():
    s = Canvas(7.6, 4.35)
    alter = ["50", "51", "69", "72", "18"]
    cx, cw, sw, sh = 2.7, 0.95, 0.88, 0.3
    faelle = [("FALSCH", DARKORANGE, ['age >= 18 ~ "erwachsen"', 'age >= 65 ~ "senior"', '.default = "unter 18"'],
               ["erwachsen", "senior", "unter 18"], lambda a: 0),
              ("RICHTIG", GREEN, ['age >= 65 ~ "senior"', 'age >= 18 ~ "erwachsen"', '.default = "unter 18"'],
               ["senior", "erwachsen", "unter 18"], lambda a: 0 if a >= 65 else 1)]
    for p, (titel, farbe, bedingungen, werte, tor) in enumerate(faelle):
        py = 0.12 + p * 2.18
        if p:
            connector(s, 0.1, py - 0.1, 7.5, py - 0.1, color=CARDLINE, width=0.75)
        eyebrow(s, 0.15, py + 0.08, 2.0, titel, color=farbe)
        text(s, cx - 0.75, py + 0.06, 0.6, 0.32, mono("age", size=10.5, color=GRAY, align=RT), anchor="middle")
        zeilen = [py + 0.62 + j * 0.46 for j in range(3)]
        for j, (bed, y) in enumerate(zip(bedingungen, zeilen)):
            card(s, 0.1, y, 7.4, 0.4)
            text(s, 0.25, y, 2.4, 0.4, mono(bed, size=10.5, align="start"), anchor="middle")
        treffer = {j: [] for j in range(3)}
        for k, a in enumerate(alter):
            x = cx + k * cw
            stein(s, x + (sw - 0.55) / 2, py + 0.08, 0.55, sh, "num", a, size=11)
            j = tor(int(a))
            treffer[j].append(k)
            ziel = zeilen[j] + 0.05
            connector(s, x + sw / 2, py + 0.08 + sh + 0.03, x + sw / 2, ziel - 0.08, color=GRAY, width=1.0, dash=True)
        for j, ks in treffer.items():
            for k in ks:
                stein(s, cx + k * cw, zeilen[j] + 0.05, sw, sh, "txt", werte[j], size=10)
        if titel == "FALSCH":
            text(s, cx, zeilen[1], 4.7, 0.4, notiz('"senior" wird nie erreicht', size=10.5, color=DARKORANGE),
                 anchor="middle")
    return s


# 5.2.3 summarise() je Gruppe aus dem Chunk `group-summarise`; die ersten drei Befragten aus West
# (Zeilen 1, 2, 3) und aus Ost (Zeilen 4, 14, 18) ------------------------------------------------
def summarise_fig():
    s = Canvas(7.6, 3.85)
    text(s, 0.15, 0.12, 7.4, 0.28,
         codezeile("group_by(eastwest) |> summarise(…, durchschnitt_alter = mean(age, na.rm = TRUE))", size=10.5))
    h, gap = 0.28, 0.06
    gruppen = [("1", "ALTE BUNDESLAENDER", ["50", "51", "69"], "3567", "51.7"),
               ("2", "NEUE BUNDESLAENDER", ["72", "44", "60"], "1679", "54.3")]
    lw = lstein_breite("NEUE BUNDESLAENDER")
    ex, axx, aw = 0.25, 0.25 + lw + 0.1, 0.6
    kopf(s, ex, lw, 0.5, "eastwest")
    kopf(s, axx, aw, 0.5, "age")
    top = 0.98
    for g, (code_, label, alter, n, _) in enumerate(gruppen):
        for i, a in enumerate(alter):
            y = top + i * (h + gap)
            lstein(s, ex, y, lw, h, "num", code_, label, size=11)
            stein(s, axx, y, aw, h, "num", a, size=11)
        unten = top + 3 * (h + gap) - gap
        punkte(s, axx - 0.1, unten - 0.02, w=aw + 0.2)
        text(s, ex, unten + 0.02, lw, 0.25, notiz(f"{n} Fälle", size=10.5, align=RT))
        top = unten + 0.42
    basis = top - 0.42 + 0.27
    platte(s, 0.15, basis, axx + aw + 0.1 - 0.15)
    # Ergebnis: eine Reihe je Gruppe
    rx = 4.45
    ry = (0.98 + basis) / 2 - (h + gap) - 0.05
    mitte = ry + h + gap / 2
    text(s, 3.3, mitte - 0.45, 0.9, 0.28, mono("mean()", size=10.5, color=GREEN))
    arrow(s, 3.4, mitte - 0.14, w=0.7, h=0.28, color=GREEN)
    text(s, rx, ry - 0.42, 1.0, 0.25, mono("eastwest", size=10.5, align="start"))
    text(s, 7.5 - 1.8, ry - 0.42, 1.8, 0.25, mono("durchschnitt_alter", size=10.5, align=RT))
    for g, (code_, label, _, _, mw) in enumerate(gruppen):
        y = ry + g * (h + 0.08)
        lstein(s, rx, y, lw, h + 0.02, "num", code_, label, size=11)
        stein(s, 7.5 - 0.75, y, 0.75, h + 0.02, "num", mw, size=11)
    platte(s, rx - 0.1, ry + 2 * (h + 0.08) + 0.0, 7.55 - rx + 0.05)
    return s


def klammer(s, x, y0, y1, color=GRAY, w=0.1):
    """Eckige Klammer rechts neben den Steinen von y0 bis y1."""
    connector(s, x, y0, x + w, y0, color=color, width=1.25)
    vline(s, x + w, y0, y1, color=color, width=1.25)
    connector(s, x, y1, x + w, y1, color=color, width=1.25)


# 5.3.1 rec() aus dem Chunk `rec-bildung` ----------------------------------------------------
def rec_fig():
    s = Canvas(7.0, 4.3)
    text(s, 0.15, 0.12, 6.8, 0.5, code(['rec(educ, rules = "1:2=1 [niedrig]; 3=2 [mittel]; 4:5=3 [hoch]; else=NA",',
                                        "    as_factor = TRUE)"], size=10))
    codes = [("1", "OHNE ABSCHLUSS"), ("2", "VOLKS-,HAUPTSCHULE"), ("3", "MITTLERE REIFE"), ("4", "FACHHOCHSCHULREIFE"),
             ("5", "HOCHSCHULREIFE"), ("6", "ANDERER ABSCHLUSS"), ("7", "NOCH SCHUELER"), ("", "")]
    gruppen = [((0, 1), "1:2=1 [niedrig]", "niedrig", "982"), ((2, 2), "3=2 [mittel]", "mittel", "1639"),
               ((3, 4), "4:5=3 [hoch]", "hoch", "2472"), ((5, 7), "else=NA", "", "153")]
    lw = lstein_breite("FACHHOCHSCHULREIFE")
    h, pitch, top = 0.28, 0.35, 1.35
    kopf(s, 0.15, lw, 0.78, "educ", "<dbl+lbl>")
    ox, ow, nx = 4.85, 0.95, 6.0
    kopf(s, ox, ow, 0.78, "educ", "<fct>")
    text(s, nx, 0.78, 0.6, 0.25, mono("n", size=11, align=RT))
    for i, (wert, label) in enumerate(codes):
        y = top + i * pitch
        if wert:
            lstein(s, 0.15, y, lw, h, "num", wert, label, size=11)
        else:
            stein(s, 0.15, y, lw, h, "na", "")
    for (a, b), regel, neu_, n in gruppen:
        y0, y1 = top + a * pitch, top + b * pitch + h
        mitte = (y0 + y1) / 2
        klammer(s, 0.15 + lw + 0.08, y0, y1)
        tw = text_width(regel, MONO, 10.5) + 0.14
        label_box(s, 2.62, mitte - 0.16, tw, 0.32, regel, PALE, color=INK, size=10.5, rounded=False, margin=0)
        arrow(s, 2.62 + tw + 0.1, mitte - 0.1, w=ox - 0.1 - (2.62 + tw + 0.1), h=0.2, color=GREEN)
        stein(s, ox, mitte - 0.16, ow, 0.32, "txt" if neu_ else "na", neu_, size=10.5)
        text(s, nx, mitte - 0.16, 0.6, 0.32, mono(n, size=11, align=RT), anchor="middle")
    return s


# 5.3.2 dicho(50) aus dem Chunk `rec-dicho`; die ersten fünf Werte von age, nach Größe sortiert ----
def dicho_fig():
    s = Canvas(7.0, 3.7)
    text(s, 0.15, 0.12, 6.8, 0.28,
         codezeile('allbus |> rec(age, rules = "dicho(50)", suffix = "_d") |> count(age_d)', size=10.5))
    w = lstein_breite("NICHT GENERIERBAR", wert=False)
    ax, dx = 1.15, 1.15 + w + 0.55
    h, pitch, top, extra = 0.3, 0.37, 1.08, 0.16
    zy = lambda i: top + i * pitch + (extra if i >= 3 else 0)       # Lücke am Schnittpunkt
    kopf(s, ax, w, 0.55, "age")
    kopf(s, dx, w, 0.55, "age_d")
    reihen = [("72", "1"), ("69", "1"), ("51", "1"), ("50", "0"), ("18", "0")]
    for i, (a, d) in enumerate(reihen):
        y = zy(i)
        stein(s, ax, y, w, h, "num", a, size=11)
        arrow(s, ax + w + 0.12, y + h / 2 - 0.08, w=0.31, h=0.16, color=GRAY)
        stein(s, dx, y, w, h, "num", d, size=11)
    y = zy(5)
    lstein(s, ax, y, w, h, "na", "", "NICHT GENERIERBAR")
    arrow(s, ax + w + 0.12, y + h / 2 - 0.08, w=0.31, h=0.16, color=GRAY)
    lstein(s, dx, y, w, h, "na", "", "NICHT GENERIERBAR")
    platte(s, ax - 0.1, y + h + 0.07, dx + w + 0.1 - (ax - 0.1))
    schnitt = zy(2) + h + (pitch - h + extra) / 2 - 0.03
    connector(s, 0.15, schnitt, dx + w + 0.15, schnitt, color=ORANGE, width=2.0, dash=True)
    text(s, 0.1, schnitt - 0.32, 1.0, 0.28, mono("dicho(50)", size=10.5, color=DARKORANGE, align="start"))
    gx = dx + w + 0.25
    for (a, b), wort, n in [((0, 2), "über 50", "2942"), ((3, 4), "bis 50", "2281"), ((5, 5), "", "23")]:
        y0, y1 = zy(a), zy(b) + h
        if b > a:
            klammer(s, dx + w + 0.06, y0, y1)
        text(s, gx, y0, 0.75, y1 - y0, mono(n, size=11, align=RT), anchor="middle")
        if wort:
            text(s, gx + 0.85, y0, 1.0, y1 - y0, notiz(wort, size=10.5, align="start"), anchor="middle")
    text(s, gx, 0.55, 0.75, 0.25, mono("n", size=11, align=RT))
    return s


# 5.3.3 Umpolen aus den Chunks `reverse` und `reverse-check` ----------------------------------
def umpolen():
    s = Canvas(6.7, 4.35)
    text(s, 0.15, 0.12, 6.4, 0.28, code(['rec(mm02, rules = "rev", suffix = "r")'], size=10.5))
    lw = lstein_breite("STIMME GAR NICHT ZU")
    lx, rx, nx = 0.15, 0.15 + lw + 0.85, 0.15 + 2 * lw + 0.95
    h, pitch, top = 0.27, 0.33, 1.12
    kopf(s, lx, lw, 0.58, "mm02", "<dbl+lbl>")
    kopf(s, rx, lw, 0.58, "mm02r", "<dbl+lbl>")
    text(s, lx + lw, 0.62, 0.85, 0.3, mono("8 - x", size=11, color=GREEN))
    text(s, nx, 0.58, 0.6, 0.25, mono("n", size=11, align=RT))
    labels = {1: "STIMME GAR NICHT ZU", 7: "STIMME VOLL+GANZ ZU"}
    anzahl = ["954", "515", "494", "629", "350", "235", "227"]
    for i in range(7):
        alt_, neu_ = i + 1, 7 - i
        y = top + i * pitch
        for x, v in [(lx, alt_), (rx, neu_)]:
            # das Wertelabel gehört zum alten Wert und wandert mit
            if alt_ in labels:
                lstein(s, x, y, lw, h, "num", str(v), labels[alt_], size=11)
            else:
                stein(s, x, y, lw, h, "num", str(v), size=11)
        arrow(s, lx + lw + 0.2, y + h / 2 - 0.08, w=0.45, h=0.16, color=GREEN)
        text(s, nx, y, 0.6, h, mono(anzahl[i], size=10.5, align=RT), anchor="middle")
    y = top + 7 * pitch
    for x in (lx, rx):
        lstein(s, x, y, lw, h, "na", "", "TNZ: SPLIT")
    arrow(s, lx + lw + 0.2, y + h / 2 - 0.08, w=0.45, h=0.16, color=GRAY)
    text(s, nx, y, 0.6, h, mono("1842", size=10.5, align=RT), anchor="middle")
    platte(s, lx - 0.05, y + h + 0.07, rx + lw + 0.05 - (lx - 0.05))
    text(s, 0.15, y + h + 0.27, 6.4, 0.28, code(["allbus |> count(mm02, mm02r)"], size=10.5))
    return s


# 5.7.1 Skala aus dem Chunk `scale-islam`: die erste Person mit sechs, mit fünf und mit vier
# gültigen Antworten (respid 1, 53, 120) ------------------------------------------------------
def skala():
    s = Canvas(7.7, 2.15)
    items = ["mm01", "mm02r", "mm03", "mm04", "mm05r", "mm06"]
    reihen = [("1", ["5", "5", "4", "2", "2", "2"], "3.33", "6 gültig"),
              ("53", ["1", "", "4", "6", "1", "5"], "3.4", "5 gültig"),
              ("120", ["3", "4", "", "4", "5", ""], "", "4 gültig")]
    h, pitch, top, w, step, ix = 0.32, 0.4, 0.62, 0.52, 0.62, 1.0
    kopf(s, 0.15, 0.6, 0.15, "respid")
    for j, it in enumerate(items):
        kopf(s, ix + j * step, w, 0.15, it, size=10.5)
    rx, rw = 6.1, 0.75
    kopf(s, rx, rw, 0.15, "islamophobie", size=10.5)
    for i, (rid, werte, ergebnis, notiz_) in enumerate(reihen):
        y = top + i * pitch
        text(s, 0.15, y, 0.6, h, mono(rid, size=10.5, color=GRAY, align=RT), anchor="middle")
        for j, v in enumerate(werte):
            stein(s, ix + j * step, y, w, h, "num" if v else "na", v, size=11)
        stein(s, rx, y, rw, h, "num" if ergebnis else "na", ergebnis, size=11)
        text(s, rx + rw + 0.12, y, 0.9, h, notiz(notiz_, size=10.5, color=GRAY if ergebnis else DARKORANGE,
                                                 align="start"), anchor="middle")
    unten = top + 2 * pitch + h
    platte(s, 0.85, unten + 0.07, ix + 5 * step + w + 0.1 - 0.85)
    platte(s, rx - 0.1, unten + 0.07, rw + 0.2)
    mitte = (top + unten) / 2
    ax = ix + 5 * step + w + 0.2
    text(s, ax - 0.1, mitte - 0.45, rx - ax, 0.28, mono("row_means()", size=10.5, color=GREEN))
    arrow(s, ax, mitte - 0.14, w=rx - ax - 0.2, h=0.28, color=GREEN)
    text(s, ax - 0.1, mitte + 0.18, rx - ax, 0.28, mono("min_valid = 5", size=10, color=GREEN))
    return s


def skalenturm(s, x, top, labels, h=0.28, pitch=0.34):
    """Werte 1 bis n untereinander, 1 oben; labels[k] ist das Wertelabel von k + 1 (None: ohne).
    Gibt Breite und Unterkante zurück."""
    w = max(lstein_breite(lab) for lab in labels if lab)
    for k, label in enumerate(labels):
        y = top + k * pitch
        if label:
            lstein(s, x, y, w, h, "num", str(k + 1), label, size=11)
        else:
            stein(s, x, y, w, h, "num", str(k + 1), size=11)
    unten = top + (len(labels) - 1) * pitch + h
    platte(s, x - 0.08, unten + 0.07, w + 0.16)
    return w, unten


# 5.7.3 Polung aus dem Chunk `pa-labels` (mm01: Wertelabels aus Kap. 4.7) und `scale-pop` ----------
def polung():
    s = Canvas(7.5, 3.35)
    top = 0.55
    pa = ["STIMME VOLL ZU", "STIMME EHER ZU", "TEILS/TEILS", "LEHNE EHER AB", "LEHNE GANZ AB"]
    tuerme = [(0.15, "mm01", ["STIMME GAR NICHT ZU", None, None, None, None, None, "STIMME VOLL+GANZ ZU"],
               "hoch = islamophob", GRAY),
              (2.85, "pa29", pa, "niedrig = populistisch", DARKORANGE),
              (5.45, "pa29r", pa[::-1], "hoch = populistisch", GREEN)]
    for x, name, labels, lesart, farbe in tuerme:
        w, unten = skalenturm(s, x, top, labels)
        kopf(s, x, w, 0.15, name)
        text(s, x - 0.1, unten + 0.17, w + 0.2, 0.25, notiz(lesart, size=10.5, color=farbe))
    vline(s, 2.62, 0.15, 3.2, color=CARDLINE, width=0.75)
    ax = 2.85 + lstein_breite("STIMME VOLL ZU") + 0.1
    mitte = top + 2 * 0.34 + 0.14
    text(s, ax - 0.1, mitte - 0.42, 5.45 - ax, 0.28, mono("6 - x", size=10.5, color=GREEN))
    arrow(s, ax, mitte - 0.13, w=5.45 - ax - 0.1, h=0.26, color=GREEN)
    text(s, 2.85, 2.9, 4.6, 0.28, mono('rec(pa29, rules = "rev", suffix = "r")', size=10.5, color=INK))
    return s

def lineal(s, x0, y, laenge, lo, hi, step=1, color=INK):
    """Lineal von lo bis hi mit Strichen und Zahlen darunter."""
    connector(s, x0, y, x0 + laenge, y, color=color, width=2.0)
    for v in range(lo, hi + 1, step):
        x = x0 + (v - lo) / (hi - lo) * laenge
        connector(s, x, y - 0.07, x, y + 0.07, color=color, width=1.25)
        text(s, x - 0.3, y + 0.1, 0.6, 0.25, mono(str(v), size=10, color=GRAY))


def marke(s, x, y, t, color, rechts=True):
    """Pfeil von oben auf das Lineal, Wert daneben."""
    down_arrow(s, x - 0.09, y - 0.33, w=0.18, h=0.28, color=color)
    if rechts:
        text(s, x + 0.12, y - 0.4, 0.9, 0.28, mono(t, size=11, color=color, align="start"))
    else:
        text(s, x - 1.02, y - 0.4, 0.9, 0.28, mono(t, size=11, color=color, align=RT))


# 5.8 pomps() aus dem Chunk `pomps-demo` ------------------------------------------------------
def pomps_fig():
    s = Canvas(7.2, 3.15)
    x0, u = 2.0, 0.8
    ia, pb = DARKORANGE, GREEN
    ya, yb, yc = 0.62, 1.47, 2.62
    text(s, 0.15, ya - 0.14, 1.75, 0.28, mono("islamophobie", size=10.5, color=ia, align="start"))
    lineal(s, x0, ya, 6 * u, 1, 7)
    marke(s, x0 + (4.11 - 1) * u, ya, "4.11", ia)
    text(s, 0.15, yb - 0.14, 1.75, 0.28, mono("populismus", size=10.5, color=pb, align="start"))
    lineal(s, x0, yb, 4 * u, 1, 5)
    marke(s, x0 + (3.4 - 1) * u, yb, "3.4", pb)
    # Hilfslinien von den Enden beider Lineale zu 0 und 100: 1 → 0 senkrecht, 7 → 100 senkrecht, 5 → 100 schräg
    for xa, y0_, y1_ in [(x0, ya + 0.38, yb - 0.12), (x0, yb + 0.38, yc - 0.12), (x0 + 6 * u, ya + 0.38, yc - 0.12)]:
        connector(s, xa, y0_, xa, y1_, color=CARDLINE, width=1.0, dash=True)
    connector(s, x0 + 4 * u, yb + 0.38, x0 + 6 * u, yc - 0.12, color=CARDLINE, width=1.0, dash=True)
    label_box(s, 0.15, yb + 0.32, 0.95, 0.3, "pomps()", GREEN, size=10.5)
    text(s, 0.15, yc - 0.36, 1.85, 0.28, mono("islamophobie_p", size=10.5, color=ia, align="start"))
    text(s, 0.15, yc - 0.12, 1.85, 0.28, mono("populismus_p", size=10.5, color=pb, align="start"))
    lineal(s, x0, yc, 6 * u, 0, 100, step=25)
    marke(s, x0 + 0.519 * 6 * u, yc, "51.9", ia, rechts=False)
    marke(s, x0 + 0.600 * 6 * u, yc, "60.0", pb)
    return s


# 5.9 Pipeline aus dem Chunk `full-pipeline` (Nummern wie dort) und R/prep.R ----------------------
def pipeline():
    s = Canvas(7.6, 3.55)
    schritte = [("einlesen", "read_spss()", "4.3"), ("mm02, mm05 umpolen", "rec()", "5.3.3"),
                ("pa29 bis pa35 umpolen", "rec()", "5.7.3"), ("Skala islamophobie", "row_means()", "5.7.1"),
                ("Skala populismus", "row_means()", "5.7.3"), ("POMPS-Versionen", "pomps()", "5.8")]
    ly, x0, dx = 0.3, 0.72, 1.2
    mitte = x0 + 2.5 * dx
    connector(s, x0, ly, x0 + 5 * dx, ly, color=INK, width=2.0)
    for k, (was, fn, abschnitt) in enumerate(schritte):
        cx = x0 + k * dx
        numdot(s, cx - 0.16, ly - 0.16, k + 1, fill=GREEN, d=0.32, size=11)
        text(s, cx - 0.6, ly + 0.25, 1.2, 0.45, [P(R(was, size=11, bold=True), align=C, ls=1.0)])
        text(s, cx - 0.6, ly + 0.72, 1.2, 0.25, mono(fn, size=10, color=GREEN))
        text(s, cx - 0.6, ly + 0.95, 1.2, 0.25, mono(abschnitt, size=10, color=GRAY, bold=False))
    hl = ly + 1.32
    connector(s, x0, hl, x0 + 5 * dx, hl, color=CARDLINE, width=1.25)
    for k in range(6):
        connector(s, x0 + k * dx, hl - 0.08, x0 + k * dx, hl, color=CARDLINE, width=1.25)
    tw, ty = 1.3, 2.3
    tx = mitte - tw / 2
    down_arrow(s, mitte - 0.13, hl + 0.05, w=0.26, h=ty - hl - 0.12, color=GREEN)
    rect(s, tx, ty, tw, 0.5, WHITE, CARDLINE, 0.75)
    text(s, tx, ty, tw, 0.5, mono("R/prep.R", size=11), anchor="middle")
    text(s, tx - 0.4, ty + 0.58, tw + 0.8, 0.25, notiz("Skript im Projektordner", size=10.5))
    bx = tx + tw + 0.75
    arrow(s, tx + tw + 0.15, ty + 0.11, w=0.45, h=0.28, color=GRAY)
    bh = codebox(s, bx, ty - 0.27, 7.5 - bx, ["library(tidyverse)", "library(mariposa)", 'source("R/_common.R")',
                                              'source("R/prep.R")'], size=10)
    text(s, bx - 0.2, ty - 0.27 + bh + 0.08, 7.5 - bx + 0.4, 0.25, notiz("Setup-Chunk in Kap. 6 bis 9", size=10.5))
    return s

FIGUREN = {
    "k05-mutate": mutate_fig,
    "k05-zuweisung": zuweisung,
    "k05-case-when": case_when_fig,
    "k05-summarise": summarise_fig,
    "k05-rec": rec_fig,
    "k05-dicho": dicho_fig,
    "k05-umpolen": umpolen,
    "k05-skala": skala,
    "k05-polung": polung,
    "k05-pomps": pomps_fig,
    "k05-pipeline": pipeline,
}
