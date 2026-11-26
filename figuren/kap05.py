"""Abbildungen für Kap. 5 „Daten transformieren und Skalen bilden“ (BILDER.md §6). Werte aus den Buch-Chunks.

Alle Werte stammen aus ALLBUS 2023 (ALLBUS2023.sav), geprüft mit R 4.5.3 und mariposa 0.7.4, nach denselben
Schritten, die das Kapitel vor dem jeweiligen Chunk ausführt. Wo ein Bild „die ersten Werte“ zeigt, sind es die
ersten Zeilen des Datensatzes (head()); welche genau, steht beim Bild.
"""
from lego import (Canvas, R, P, text, rect, card, eyebrow, label_box, stein, schild, arrow, down_arrow, outline,
                  connector, vline, numdot, codebox, text_width, INK, GRAY, GREEN, ORANGE, CARDLINE, DARKORANGE,
                  WHITE, PALE, STEIN, MONO, C, RT)
from kap03 import mono, notiz, platte
from kap04 import lstein, lstein_breite, saeule, kopf, punkte, codezeile
import sprache
from sprache import t as tr

SPRACHFAEHIG = True  # alle Texte laufen über tr(); build.py --en baut dieses Modul
# en.EN ist ein Wörterbuch für alle Kapitel. Kap. 3 bildet "alter" auf "age" ab; Kap. 5 braucht diesen Schlüssel nicht,
# denn rename(alter = age) kommt in keiner Abbildung vor. Alle Schlüssel dieses Kapitels sind eigene Wörter.


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
         codezeile(tr("allbus |> select(age) |> mutate(geburtsjahr = 2023 - age) |> head(3)"), size=10.5))
    h, top, gap = 0.36, 1.05, 0.07
    ax, aw, gx, gw = 0.45, 0.8, 3.05, 1.0
    kopf(s, ax, aw, 0.5, "age", "<dbl+lbl>")
    kopf(s, gx, gw, 0.5, tr("geburtsjahr"), "<dbl>")
    alter, jahr = ["50", "51", "69"], ["1973", "1972", "1954"]
    unten = saeule(s, ax, top, aw, h, "num", alter, size=12)
    saeule(s, gx, top, gw, h, "num", jahr, size=12)
    for i, a in enumerate(alter):
        y = top + i * (h + gap)
        text(s, ax + aw + 0.12, y, 1.0, h, mono(f"2023 - {a}", size=10.5, color=GRAY), anchor="middle")
        arrow(s, ax + aw + 1.17, y + h / 2 - 0.09, w=0.38, h=0.18, color=GRAY)
    platte(s, 0.3, unten + 0.07, gx + gw + 0.15 - 0.3)
    outline(s, gx - 0.07, top - 0.11, gw + 0.14, 3 * (h + gap) + 0.08, color=GREEN, lw=1.75)
    text(s, gx + gw + 0.25, top + h + gap - 0.02, 1.7, 0.4, notiz(tr("neuer Turm"), size=10.5, color=GREEN, align="start"),
         anchor="middle")
    return s


# 5.2.1 Zuweisung: Chunk `mutate` ohne und mit `allbus <-`; die ersten drei Werte ---------------
def zuweisung():
    s = Canvas(7.6, 3.45)
    h, top, gap = 0.3, 1.95, 0.07
    for x0, titel, zeilen, gespeichert in [
            (0.15, tr("OHNE <-"), ["allbus |>", tr("  mutate(geburtsjahr = 2023 - age)")], False),
            (3.95, tr("MIT <-"), ["allbus <- allbus |>", tr("  mutate(geburtsjahr = 2023 - age)")], True)]:
        eyebrow(s, x0, 0.12, 3.4, titel, color=GREEN if gespeichert else GRAY)
        text(s, x0, 0.42, 3.5, 0.5, code(zeilen, size=10.5))
        schild(s, x0, 1.05, "allbus", w=1.0)
        text(s, x0 + 1.12, 1.08, 1.6, 0.3, mono("5,246 × 580" if gespeichert else "5,246 × 579", size=11,
                                                color=GRAY, align="start"))
        ax, gx = x0 + 0.2, x0 + 1.6
        kopf(s, ax, 0.7, 1.5, "age")
        kopf(s, gx, 0.9, 1.5, tr("geburtsjahr"))
        unten = saeule(s, ax, top, 0.7, h, "num", ["50", "51", "69"], size=11)
        punkte(s, ax + 0.77, top + h + gap - 0.03, w=0.5)
        saeule(s, gx, top, 0.9, h, "num" if gespeichert else "dim", ["1973", "1972", "1954"], size=11)
        platte(s, x0 + 0.05, unten + 0.07, gx + 1.05 - x0)
        if gespeichert:
            outline(s, gx - 0.07, top - 0.11, 1.04, 3 * (h + gap) + 0.08, color=GREEN, lw=1.75)
        text(s, gx + 1.05, top + h + gap - 0.05, 1.0, h + 0.1,
             notiz(tr("gespeichert") if gespeichert else tr("nur angezeigt"), size=10.5,
                   color=GREEN if gespeichert else GRAY, align="start"), anchor="middle")
    vline(s, 3.8, 0.15, 3.3, color=CARDLINE, width=0.75)
    return s


# 5.2.2 Reihenfolge in case_when() aus dem Chunk `case-when-falle`; die ersten fünf Werte von age --
def case_when_fig():
    s = Canvas(7.6, 4.35)
    alter = ["50", "51", "69", "72", "18"]
    cx, cw, sw, sh = 2.7, 0.95, 0.88, 0.3
    faelle = [(tr("FALSCH"), DARKORANGE, [tr('age >= 18 ~ "erwachsen"'), 'age >= 65 ~ "senior"',
                                          tr('.default = "unter 18"')],
               [tr("erwachsen"), "senior", tr("unter 18")], lambda a: 0),
              (tr("RICHTIG"), GREEN, ['age >= 65 ~ "senior"', tr('age >= 18 ~ "erwachsen"'),
                                      tr('.default = "unter 18"')],
               ["senior", tr("erwachsen"), tr("unter 18")], lambda a: 0 if a >= 65 else 1)]
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
        if farbe == DARKORANGE:
            text(s, cx, zeilen[1], 4.7, 0.4, notiz(tr('"senior" wird nie erreicht'), size=10.5, color=DARKORANGE),
                 anchor="middle")
    return s


# 5.2.3 summarise() je Gruppe aus dem Chunk `group-summarise`; die ersten drei Befragten aus West
# (Zeilen 1, 2, 3) und aus Ost (Zeilen 4, 14, 18) ------------------------------------------------
def summarise_fig():
    s = Canvas(7.6, 3.85)
    text(s, 0.15, 0.12, 7.4, 0.28,
         codezeile(tr("group_by(eastwest) |> summarise(…, durchschnitt_alter = mean(age, na.rm = TRUE))"), size=10.5))
    h, gap = 0.28, 0.06
    gruppen = [("1", tr("ALTE BUNDESLAENDER"), ["50", "51", "69"], "3567", "51.7"),
               ("2", tr("NEUE BUNDESLAENDER"), ["72", "44", "60"], "1679", "54.3")]
    lw = lstein_breite(tr("NEUE BUNDESLAENDER"))
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
        text(s, ex, unten + 0.02, lw, 0.25, notiz(f"{n} {tr('Fälle')}", size=10.5, align=RT))
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
    text(s, 7.5 - 1.8, ry - 0.42, 1.8, 0.25, mono(tr("durchschnitt_alter"), size=10.5, align=RT))
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
    en = sprache.aktuell() == "en"
    zeilen = ["mutate(", tr('  educ = rec(educ, rules = "1:2=1 [niedrig]; 3=2 [mittel]; 4:5=3 [hoch]; else=NA",'),
              "             as_factor = TRUE)", ")"]
    dy = 0.4                                     # Platz für die zwei zusätzlichen Code-Zeilen
    s = Canvas(7.3, 4.3 + dy)
    text(s, 0.15, 0.12, 7.1, 0.9, code(zeilen, size=10))
    codes = [("1", tr("OHNE ABSCHLUSS")), ("2", tr("VOLKS-,HAUPTSCHULE")), ("3", tr("MITTLERE REIFE")),
             ("4", tr("FACHHOCHSCHULREIFE")), ("5", tr("HOCHSCHULREIFE")), ("6", tr("ANDERER ABSCHLUSS")),
             ("7", tr("NOCH SCHUELER")), ("", "")]
    gruppen = [((0, 1), tr("1:2=1 [niedrig]"), tr("niedrig"), "982"), ((2, 2), tr("3=2 [mittel]"), tr("mittel"), "1639"),
               ((3, 4), tr("4:5=3 [hoch]"), tr("hoch"), "2472"), ((5, 7), "else=NA", "", "153")]
    lw = max(lstein_breite(label) for _, label in codes if label)
    rx0 = max(2.62, 0.15 + lw + 0.45) if en else 2.62        # englische Labels sind länger: Regeln weiter rechts
    h, pitch, top = 0.28, 0.35, 1.35 + dy
    kopf(s, 0.15, lw, 0.78 + dy, "educ", "<dbl+lbl>")
    ox, ow, nx = 4.85, 0.95, 6.0
    kopf(s, ox, ow, 0.78 + dy, "educ", "<fct>")
    text(s, nx, 0.78 + dy, 0.6, 0.25, mono("n", size=11, align=RT))
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
        label_box(s, rx0, mitte - 0.16, tw, 0.32, regel, PALE, color=INK, size=10.5, rounded=False, margin=0)
        arrow(s, rx0 + tw + 0.1, mitte - 0.1, w=ox - 0.1 - (rx0 + tw + 0.1), h=0.2, color=GREEN)
        stein(s, ox, mitte - 0.16, ow, 0.32, "txt" if neu_ else "na", neu_, size=10.5)
        text(s, nx, mitte - 0.16, 0.6, 0.32, mono(n, size=11, align=RT), anchor="middle")
    return s


# 5.3.2 dicho(50) aus dem Chunk `rec-dicho`; die ersten fünf Werte von age, nach Größe sortiert ----
def dicho_fig():
    s = Canvas(7.45 if sprache.aktuell() == "en" else 7.0, 3.7)
    text(s, 0.15, 0.12, 6.8, 0.28,
         codezeile('allbus |> mutate(age_d = rec(age, rules = "dicho(50)")) |> count(age_d)', size=10.5))
    w = lstein_breite(tr("NICHT GENERIERBAR"), wert=False)
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
    lstein(s, ax, y, w, h, "na", "", tr("NICHT GENERIERBAR"))
    arrow(s, ax + w + 0.12, y + h / 2 - 0.08, w=0.31, h=0.16, color=GRAY)
    lstein(s, dx, y, w, h, "na", "", tr("NICHT GENERIERBAR"))
    platte(s, ax - 0.1, y + h + 0.07, dx + w + 0.1 - (ax - 0.1))
    schnitt = zy(2) + h + (pitch - h + extra) / 2 - 0.03
    connector(s, 0.15, schnitt, dx + w + 0.15, schnitt, color=ORANGE, width=2.0, dash=True)
    text(s, 0.1, schnitt - 0.32, 1.0, 0.28, mono("dicho(50)", size=10.5, color=DARKORANGE, align="start"))
    gx = dx + w + 0.25
    for (a, b), wort, n in [((0, 2), tr("über 50"), "2942"), ((3, 4), tr("bis 50"), "2281"), ((5, 5), "", "23")]:
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
    text(s, 0.15, 0.12, 6.4, 0.28, code(['mutate(mm02r = rec(mm02, rules = "rev"))'], size=10.5))
    lw = lstein_breite(tr("STIMME GAR NICHT ZU"))
    lx, rx, nx = 0.15, 0.15 + lw + 0.85, 0.15 + 2 * lw + 0.95
    h, pitch, top = 0.27, 0.33, 1.12
    kopf(s, lx, lw, 0.58, "mm02", "<dbl+lbl>")
    kopf(s, rx, lw, 0.58, "mm02r", "<dbl+lbl>")
    text(s, lx + lw, 0.62, 0.85, 0.3, mono("8 - x", size=11, color=GREEN))
    text(s, nx, 0.58, 0.6, 0.25, mono("n", size=11, align=RT))
    labels = {1: tr("STIMME GAR NICHT ZU"), 7: tr("STIMME VOLL+GANZ ZU")}
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
        lstein(s, x, y, lw, h, "na", "", tr("TNZ: SPLIT"))
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
    reihen = [("1", ["5", "5", "4", "2", "2", "2"], "3.33", tr("6 gültig")),
              ("53", ["1", "", "4", "6", "1", "5"], "3.4", tr("5 gültig")),
              ("120", ["3", "4", "", "4", "5", ""], "", tr("4 gültig"))]
    h, pitch, top, w, step, ix = 0.32, 0.4, 0.62, 0.52, 0.62, 1.0
    kopf(s, 0.15, 0.6, 0.15, "respid")
    for j, it in enumerate(items):
        kopf(s, ix + j * step, w, 0.15, it, size=10.5)
    rx, rw = 6.1, 0.75
    kopf(s, rx, rw, 0.15, tr("islamophobie"), size=10.5)
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


def skalenturm(s, x, top, labels, h=0.28, pitch=0.34, lsize=10, nw=0.42):
    """Werte 1 bis n untereinander, 1 oben; labels[k] ist das Wertelabel von k + 1 (None: ohne).
    Gibt Breite und Unterkante zurück."""
    w = max(lstein_breite(lab, lsize=lsize, nw=nw) for lab in labels if lab)
    for k, label in enumerate(labels):
        y = top + k * pitch
        if label:
            lstein(s, x, y, w, h, "num", str(k + 1), label, size=11, lsize=lsize, nw=nw)
        else:
            stein(s, x, y, w, h, "num", str(k + 1), size=11)
    unten = top + (len(labels) - 1) * pitch + h
    platte(s, x - 0.08, unten + 0.07, w + 0.16)
    return w, unten


# 5.7.3 Polung aus dem Chunk `pa-labels` (mm01: Wertelabels aus Kap. 4.7) und `scale-pop` ----------
def polung():
    en = sprache.aktuell() == "en"           # englisch: längere Labels, schmalere Wertspalte, Türme rücken
    top = 0.55
    pa = [tr("STIMME VOLL ZU"), tr("STIMME EHER ZU"), tr("TEILS/TEILS"), tr("LEHNE EHER AB"), tr("LEHNE GANZ AB")]
    ls = dict(nw=0.3) if en else {}
    if en:
        w1 = lstein_breite(tr("STIMME GAR NICHT ZU"), **ls)
        w2 = max(lstein_breite(lab, **ls) for lab in pa)
        x2 = 0.15 + w1 + 0.3
        x3 = x2 + w2 + 0.75
        s = Canvas(x3 + w2 + 0.15, 3.35)
    else:
        x2, x3 = 2.85, 5.45
        s = Canvas(7.5, 3.35)
    tuerme = [(0.15, "mm01", [tr("STIMME GAR NICHT ZU"), None, None, None, None, None, tr("STIMME VOLL+GANZ ZU")],
               tr("hoch = islamophob"), GRAY),
              (x2, "pa29", pa, tr("niedrig = populistisch"), DARKORANGE),
              (x3, "pa29r", pa[::-1], tr("hoch = populistisch"), GREEN)]
    for x, name, labels, lesart, farbe in tuerme:
        w, unten = skalenturm(s, x, top, labels, **ls)
        kopf(s, x, w, 0.15, name)
        text(s, x - 0.1, unten + 0.17, w + 0.2, 0.25, notiz(lesart, size=10.5, color=farbe))
    vline(s, x2 - 0.23, 0.15, 3.2, color=CARDLINE, width=0.75)
    ax = x2 + max(lstein_breite(lab, **ls) for lab in pa) + 0.1
    mitte = top + 2 * 0.34 + 0.14
    text(s, ax - 0.1, mitte - 0.42, x3 - ax, 0.28, mono("6 - x", size=10.5, color=GREEN))
    arrow(s, ax, mitte - 0.13, w=x3 - ax - 0.1, h=0.26, color=GREEN)
    text(s, x2, 2.9, 4.6, 0.28, mono('mutate(pa29r = rec(pa29, rules = "rev"))', size=10.5, color=INK))
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
    text(s, 0.15, ya - 0.14, 1.75, 0.28, mono(tr("islamophobie"), size=10.5, color=ia, align="start"))
    lineal(s, x0, ya, 6 * u, 1, 7)
    marke(s, x0 + (4.11 - 1) * u, ya, "4.11", ia)
    text(s, 0.15, yb - 0.14, 1.75, 0.28, mono(tr("populismus"), size=10.5, color=pb, align="start"))
    lineal(s, x0, yb, 4 * u, 1, 5)
    marke(s, x0 + (3.4 - 1) * u, yb, "3.4", pb)
    # Hilfslinien von den Enden beider Lineale zu 0 und 100: 1 → 0 senkrecht, 7 → 100 senkrecht, 5 → 100 schräg
    for xa, y0_, y1_ in [(x0, ya + 0.38, yb - 0.12), (x0, yb + 0.38, yc - 0.12), (x0 + 6 * u, ya + 0.38, yc - 0.12)]:
        connector(s, xa, y0_, xa, y1_, color=CARDLINE, width=1.0, dash=True)
    connector(s, x0 + 4 * u, yb + 0.38, x0 + 6 * u, yc - 0.12, color=CARDLINE, width=1.0, dash=True)
    label_box(s, 0.15, yb + 0.32, 0.95, 0.3, "pomps()", GREEN, size=10.5)
    text(s, 0.15, yc - 0.36, 1.85, 0.28, mono(tr("islamophobie_p"), size=10.5, color=ia, align="start"))
    text(s, 0.15, yc - 0.12, 1.85, 0.28, mono(tr("populismus_p"), size=10.5, color=pb, align="start"))
    lineal(s, x0, yc, 6 * u, 0, 100, step=25)
    marke(s, x0 + 0.519 * 6 * u, yc, "51.9", ia, rechts=False)
    marke(s, x0 + 0.600 * 6 * u, yc, "60.0", pb)
    return s


# 5.9 Pipeline aus dem Chunk `full-pipeline` (Nummern wie dort) und R/prep.R ----------------------
def pipeline():
    en = sprache.aktuell() == "en"           # englisch: set_na() als zweite Funktion unter Schritt 1
    ex = 0.2 if en else 0                    # Platz für die zweite Funktion
    s = Canvas(7.6, 3.55 + ex)
    schritte = [(tr("einlesen"), "read_spss()", "4.3"), (tr("mm02, mm05 umpolen"), "rec()", "5.3.3"),
                (tr("pa29 bis pa35 umpolen"), "rec()", "5.7.3"), (tr("Skala islamophobie"), "row_means()", "5.7.1"),
                (tr("Skala populismus"), "row_means()", "5.7.3"), (tr("POMPS-Versionen"), "pomps()", "5.8")]
    ly, x0, dx = 0.3, 0.72, 1.2
    mitte = x0 + 2.5 * dx
    connector(s, x0, ly, x0 + 5 * dx, ly, color=INK, width=2.0)
    for k, (was, fn, abschnitt) in enumerate(schritte):
        cx = x0 + k * dx
        numdot(s, cx - 0.16, ly - 0.16, k + 1, fill=GREEN, d=0.32, size=11)
        text(s, cx - 0.6, ly + 0.25, 1.2, 0.45, [P(R(was, size=11, bold=True), align=C, ls=1.0)])
        text(s, cx - 0.6, ly + 0.72, 1.2, 0.25, mono(fn, size=10, color=GREEN))
        if en and k == 0:
            text(s, cx - 0.6, ly + 0.92, 1.2, 0.25, mono("set_na()", size=10, color=GREEN))
        text(s, cx - 0.6, ly + 0.95 + ex, 1.2, 0.25, mono(abschnitt, size=10, color=GRAY, bold=False))
    hl = ly + 1.32 + ex
    connector(s, x0, hl, x0 + 5 * dx, hl, color=CARDLINE, width=1.25)
    for k in range(6):
        connector(s, x0 + k * dx, hl - 0.08, x0 + k * dx, hl, color=CARDLINE, width=1.25)
    tw, ty = 1.3, 2.3 + ex
    tx = mitte - tw / 2
    down_arrow(s, mitte - 0.13, hl + 0.05, w=0.26, h=ty - hl - 0.12, color=GREEN)
    rect(s, tx, ty, tw, 0.5, WHITE, CARDLINE, 0.75)
    text(s, tx, ty, tw, 0.5, mono("R/prep.R", size=11), anchor="middle")
    text(s, tx - 0.4, ty + 0.58, tw + 0.8, 0.25, notiz(tr("Skript im Projektordner"), size=10.5))
    bx = tx + tw + 0.75
    arrow(s, tx + tw + 0.15, ty + 0.11, w=0.45, h=0.28, color=GRAY)
    bh = codebox(s, bx, ty - 0.27, 7.5 - bx, ["library(tidyverse)", "library(mariposa)", 'source("R/_common.R")',
                                              'source("R/prep.R")'], size=10)
    text(s, bx - 0.2, ty - 0.27 + bh + 0.08, 7.5 - bx + 0.4, 0.25, notiz(tr("Setup-Chunk in Kap. 6 bis 9"), size=10.5))
    return s

# 5.4 std() und center() aus den Chunks `std-center` und `center` (eval=FALSE): die erste und die dritte Person der
# Ausgabe (age 50 und 69). Mittelwert 52.51 und SD 18.25 von age (5.223 gültige Werte) druckt kein Chunk; der Text
# nennt sie, ebenso die Werte von age_c (-2.51 und 16.49). -------------------------------------------------------
def std_fig():
    s = Canvas(7.6, 3.45)
    mw, sd = 52.51063, 18.25121
    x0, lo, hi = 1.9, 30, 75
    X = lambda a: x0 + (a - lo) * 5.4 / (hi - lo)
    blau, tinte = STEIN["num"]
    y1, y2, y3 = 0.6, 1.9, 3.05
    lineale = [(y1, "age", None, [(v, str(v)) for v in range(30, 80, 10)]),
               (y2, "age_c", "center()", [(mw + d, str(d)) for d in (-20, -10, 0, 10, 20)]),
               (y3, "age_z", "std()", [(mw + k * sd, t) for k, t in ((-1, "-1"), (-0.5, "-0.5"), (0, "0"),
                                                                    (0.5, "0.5"), (1, "1"))])]
    personen = [(50, ["50", "-2.51", "-0.138"]), (69, ["69", "16.49", "0.903"])]
    # Hilfslinien bei Mittelwert und +1 SD, von Lineal zu Lineal (unter den Zahlen unterbrochen)
    for a in (mw, mw + sd):
        for ya, yb in ((y1 + 0.38, y2 - 0.05), (y2 + 0.38, y3 - 0.05)):
            connector(s, X(a), ya, X(a), yb, color=CARDLINE, width=1.0, dash=True)
    for k, (y, name, fn, striche) in enumerate(lineale):
        connector(s, X(lo), y, X(hi), y, color=INK, width=2.0)
        for a, t in striche:
            connector(s, X(a), y - 0.07, X(a), y + 0.07, color=INK, width=1.25)
            text(s, X(a) - 0.3, y + 0.1, 0.6, 0.25, mono(t, size=10, color=GRAY, bold=False))
        text(s, 0.15, y - 0.14, 1.5, 0.28, mono(name, size=11, align="start"), anchor="middle")
        if fn:
            text(s, 0.15, y + 0.12, 1.5, 0.28, mono(fn, size=10.5, color=GREEN, align="start"))
        for a, werte in personen:
            down_arrow(s, X(a) - 0.09, y - 0.33, w=0.18, h=0.28, color=blau)
            text(s, X(a) - 1.02, y - 0.4, 0.9, 0.28, mono(werte[k], size=11, color=tinte, align=RT))
    # Mittelwert und SD auf dem ersten Lineal
    down_arrow(s, X(mw) - 0.09, y1 - 0.33, w=0.18, h=0.28, color=DARKORANGE)
    text(s, X(mw) + 0.12, y1 - 0.4, 1.6, 0.28, [P(R(tr("Mittelwert "), size=10.5, italic=True, color=DARKORANGE),
                                                  R("52.51", font=MONO, size=11, bold=True, color=DARKORANGE))])
    yb = y1 + 0.47
    connector(s, X(mw), yb, X(mw + sd), yb, color=GRAY, width=1.25)
    for a in (mw, mw + sd):
        connector(s, X(a), yb - 0.06, X(a), yb + 0.06, color=GRAY, width=1.25)
    text(s, X(mw), yb + 0.03, X(mw + sd) - X(mw), 0.28, [P(R("SD ", size=10.5, italic=True, color=GRAY),
                                                         R("18.25", font=MONO, size=11, bold=True, color=GRAY),
                                                         align=C)])
    # Rechenschritte zwischen den Linealen
    for ya, yb, t in ((y1 + 0.25, y2 - 0.22, "- 52.51"), (y2 + 0.45, y3 - 0.22, "/ 18.25")):
        down_arrow(s, 0.2, ya, w=0.2, h=yb - ya, color=GRAY)
        text(s, 0.48, ya, 1.2, yb - ya, mono(t, size=10.5, color=GRAY, align="start"), anchor="middle")
    return s


def tuerme(s, x0, top, spalten, h=0.28, pitch=0.34, size=11, gap=0.1, kopf_y=None, typen=None):
    """Bauplatte von oben: spalten = [(name, breite, [(kind, wert), …])]; leerer Wert = NA.
    Gibt die x-Positionen der Türme und die Grundlinie zurück."""
    xs, x = [], x0
    for j, (name, w, steine) in enumerate(spalten):
        if kopf_y is not None:
            kopf(s, x, w, kopf_y, name, typen[j] if typen else None, size=10.5)
        for i, (kind, wert) in enumerate(steine):
            stein(s, x, top + i * pitch, w, h, kind if wert else "na", wert, size=size)
        xs.append(x)
        x += w + gap
    n = max(len(st) for _, _, st in spalten)
    return xs, top + (n - 1) * pitch + h + 0.07


# 5.5 left_join() aus den Chunks `join-kontext` und `join-demo`: die ersten vier Reihen der Ausgabe -------------
def join_fig():
    s = Canvas(7.7, 4.15)
    h, pitch = 0.28, 0.4                                   # Fuge 0.12: Platz für den Rahmen um eine Reihe
    west, ost = ("7.2", "45000"), ("1.4", "32000")
    reihen = [("1", "50"), ("1", "51"), ("1", "69"), ("2", "72")]
    # Ergebnis unten: eastwest, age, …, und die zwei neuen Türme genau unter den Spalten von kontext_bl
    ex, ax, mx, bx = 3.05, 3.7, 5.2, 6.55
    mwid, bwid = 0.75, 0.9
    top = 2.0
    for x, w, name in [(ex, 0.55, "eastwest"), (ax, 0.55, "age"), (mx, mwid, tr("muslim_anteil")),
                       (bx, bwid, tr("bip_pro_kopf"))]:
        kopf(s, x, w, top - 0.33, name, size=10.5)
    for i, (e, a) in enumerate(reihen):
        y = top + i * pitch
        m, b = west if e == "1" else ost
        stein(s, ex, y, 0.55, h, "num", e, size=11)
        stein(s, ax, y, 0.55, h, "num", a, size=11)
        stein(s, mx, y, mwid, h, "num", m, size=11)
        stein(s, bx, y, bwid, h, "num", b, size=11)
    unten = top + 3 * pitch + h
    base = unten + 0.1
    punkte(s, ax + 0.6, top + pitch - 0.05, w=0.8)
    platte(s, ex - 0.1, base, bx + bwid + 0.1 - (ex - 0.1))
    for x, w in [(mx, mwid), (bx, bwid)]:
        outline(s, x - 0.07, top - 0.13, w + 0.14, unten + 0.06 - (top - 0.13), color=GREEN, lw=1.75)
    y_ost = top + 3 * pitch
    outline(s, ex - 0.1, y_ost - 0.09, bx + bwid + 0.1 - (ex - 0.1), h + 0.13, color=ORANGE, lw=1.75)
    # kontext_bl oben rechts
    kx, ktop = 4.15, 0.45
    kopf(s, kx, 0.55, 0.12, "eastwest", size=10.5)
    kopf(s, mx, mwid, 0.12, tr("muslim_anteil"), size=10.5)
    kopf(s, bx, bwid, 0.12, tr("bip_pro_kopf"), size=10.5)
    for i, (e, (m, b)) in enumerate([("1", west), ("2", ost)]):
        y = ktop + i * pitch
        stein(s, kx, y, 0.55, h, "num", e, size=11)
        stein(s, mx, y, mwid, h, "num", m, size=11)
        stein(s, bx, y, bwid, h, "num", b, size=11)
    kunten = ktop + pitch + h
    platte(s, kx - 0.1, kunten + 0.1, bx + bwid + 0.1 - (kx - 0.1))
    outline(s, kx - 0.1, ktop + pitch - 0.09, bx + bwid + 0.1 - (kx - 0.1), h + 0.13, color=ORANGE, lw=1.75)
    if sprache.aktuell() == "en":                           # längerer Name: Schild breiter, weiter links
        schild(s, kx - 1.95, ktop + pitch / 2 - 0.04, tr("kontext_bl"), w=1.7)
    else:
        schild(s, kx - 1.5, ktop + pitch / 2 - 0.04, "kontext_bl", w=1.25)
    for x, w in [(mx, mwid), (bx, bwid)]:
        down_arrow(s, x + w / 2 - 0.11, kunten + 0.25, w=0.22, h=top - 0.36 - (kunten + 0.25), color=GREEN)
    # allbus links, Reihen auf derselben Höhe wie im Ergebnis
    schild(s, 0.2, top - 0.85, "allbus", w=1.0)
    kopf(s, 0.3, 0.55, top - 0.33, "eastwest", size=10.5)
    kopf(s, 0.95, 0.55, top - 0.33, "age", size=10.5)
    for i, (e, a) in enumerate(reihen):
        stein(s, 0.3, top + i * pitch, 0.55, h, "num", e, size=11)
        stein(s, 0.95, top + i * pitch, 0.55, h, "num", a, size=11)
    punkte(s, 1.52, top + pitch - 0.05, w=0.3)
    platte(s, 0.2, base, 1.7)
    mitte = top + 1.5 * pitch + h / 2
    arrow(s, 2.0, mitte - 0.14, w=0.8, h=0.28, color=GREEN)
    text(s, 1.8, mitte - 0.45, 1.2, 0.28, mono("left_join()", size=10.5, color=GREEN))
    text(s, 0.15, base + 0.2, 7.3, 0.28,
         codezeile(tr('allbus_mit_kontext <- allbus |> left_join(kontext_bl, by = "eastwest")'), size=10.5))
    return s


# 5.5 Kasten „Die Join-Familie“: Schema mit zwei kleinen Platten x und y (Schlüssel id); die Ergebnisse sind mit
# R geprüft (left_join(), inner_join(), full_join() aus dplyr) ------------------------------------------------------
def join_familie():
    s = Canvas(7.3, 2.45)
    w, gap, top = 0.4, 0.06, 0.85
    x_ = [("num", "1", "num", "10"), ("num", "2", "num", "20"), ("num", "3", "num", "30")]
    y_ = [("num", "1", "txt", "A"), ("num", "2", "txt", "B"), ("num", "4", "txt", "D")]
    ergebnisse = [("left_join(x, y)", [("1", "10", "A"), ("2", "20", "B"), ("3", "30", "")]),
                  ("inner_join(x, y)", [("1", "10", "A"), ("2", "20", "B")]),
                  ("full_join(x, y)", [("1", "10", "A"), ("2", "20", "B"), ("3", "30", ""), ("4", "", "D")])]
    x = 0.15
    for name, zeilen, spalte2 in [("x", x_, "a"), ("y", y_, "b")]:
        schild(s, x, 0.1, name, w=0.45)
        _, base = tuerme(s, x, top, [("id", w, [(k, v) for k, v, _, _ in zeilen]),
                                     (spalte2, w, [(k, v) for _, _, k, v in zeilen])], gap=gap, kopf_y=0.5)
        platte(s, x - 0.06, base, 2 * w + gap + 0.12)
        x += 2 * w + gap + 0.25
    vline(s, x, 0.15, 2.3, color=CARDLINE, width=0.75)
    x += 0.23
    breite = 3 * w + 2 * gap
    for fn, zeilen in ergebnisse:
        text(s, x - 0.2, 0.12, breite + 0.4, 0.28, mono(fn, size=10, color=GREEN))
        _, base = tuerme(s, x, top, [("id", w, [("num", z[0]) for z in zeilen]),
                                     ("a", w, [("num", z[1]) for z in zeilen]),
                                     ("b", w, [("txt", z[2]) for z in zeilen])], gap=gap, kopf_y=0.5)
        platte(s, x - 0.06, base, breite + 0.12)
        x += breite + 0.28
    return s


# 5.6.1 pivot_longer() aus den Chunks `pivot-wide-show` und `pivot-longer-demo`: Person 1 und 2 (wide) und die
# ersten acht Reihen (long) ---------------------------------------------------------------------------------------
def pivot_longer_fig():
    s = Canvas(7.7, 3.75)
    items = ["mm01", "mm02r", "mm03", "mm04", "mm05r", "mm06"]
    person1 = ["5", "5", "4", "2", "2", "2"]
    h, pitch, fuge = 0.28, 0.34, 0.1                      # breitere Fuge unter Person 1 für den Rahmen
    # wide: Spaltennamen als dunkle Namensschilder
    x0, sw, step, sh = 0.15, 0.62, 0.7, 0.32
    top = 0.62
    for j, it in enumerate(items):
        x = x0 + j * step
        label_box(s, x, 0.12, sw, sh, it, INK, size=10.5, rounded=False, margin=0.04)
        stein(s, x + 0.06, top, sw - 0.12, h, "num", person1[j], size=11)
        stein(s, x + 0.06, top + pitch + fuge, sw - 0.12, h, "na", "")
    breite = 5 * step + sw
    base = top + pitch + fuge + h + 0.07
    platte(s, x0 - 0.05, base, breite + 0.1)
    outline(s, x0 - 0.03, top - 0.1, breite + 0.06, h + 0.14, color=ORANGE, lw=1.75)
    text(s, x0, base + 0.12, breite, 0.25, mono("5,246 × 6", size=10.5, color=GRAY, bold=False))
    # long: item und antwort; Person 1 sind die ersten sechs Reihen
    lx, iw, aw = 5.75, 0.85, 0.6
    ax = lx + iw + 0.12
    ltop = 0.62
    kopf(s, lx, iw, 0.08, "item", "<chr>", size=10.5)
    kopf(s, ax, aw, 0.08, tr("antwort"), "<dbl>", size=10.5)
    werte = person1 + ["", ""]
    ly = [ltop + i * pitch + (fuge if i >= 6 else 0) for i in range(8)]
    for i, y in enumerate(ly):
        stein(s, lx, y, iw, h, "txt", items[i % 6], size=11)
        stein(s, ax, y, aw, h, "num" if werte[i] else "na", werte[i], size=11)
    lbase = ly[-1] + h + 0.07
    platte(s, lx - 0.1, lbase, iw + aw + 0.32)
    outline(s, lx - 0.07, ltop - 0.1, iw + aw + 0.26, ly[5] + h + 0.04 - (ltop - 0.1), color=ORANGE, lw=1.75)
    text(s, lx - 0.3, lbase + 0.12, iw + aw + 0.72, 0.25, mono("31,476 × 2", size=10.5, color=GRAY, bold=False))
    mitte = top + h / 2
    pa = x0 + breite + 0.2
    arrow(s, pa, mitte - 0.14, w=lx - 0.25 - pa, h=0.28, color=GREEN)
    text(s, pa - 0.1, mitte + 0.2, lx - 0.25 - pa + 0.2, 0.28, mono("pivot_longer()", size=10.5, color=GREEN))
    text(s, 0.15, 2.0, 5.0, 0.9, code(["pivot_longer(cols = everything(),",
                                       '             names_to = "item",',
                                       tr('             values_to = "antwort")')], size=10.5))
    return s


# 5.6.2 pivot_wider() aus den Chunks `pivot-mw-long` und `pivot-wider-demo` -------------------------------------
def pivot_wider_fig():
    s = Canvas(7.8, 3.7)
    h, pitch = 0.28, 0.34
    alt, neu = tr("ALTE BUNDESLAENDER"), tr("NEUE BUNDESLAENDER")
    mw = {(alt, "mm01"): "3.19", (alt, "mm03"): "3.97", (alt, "mm06"): "4.14",
          (neu, "mm01"): "4.01", (neu, "mm03"): "4.63", (neu, "mm06"): "4.58"}
    items = ["mm01", "mm03", "mm06"]
    lang = [(r, it, mw[(r, it)]) for r in (alt, neu) for it in items]
    ew = text_width(alt, MONO, 10, True) + 0.1
    # long
    ex, ix, mx, w = 0.12, 0.12 + ew + 0.08, 0.12 + ew + 0.71, 0.55
    top = 0.72
    kopf(s, ex, ew, 0.12, "eastwest", "<fct>", size=10.5)
    kopf(s, ix, w, 0.12, "item", "<chr>", size=10.5)
    kopf(s, mx, w, 0.12, tr("mw"), "<dbl>", size=10.5)
    for i, (r, it, m) in enumerate(lang):
        y = top + i * pitch
        stein(s, ex, y, ew, h, "txt", r, size=10)
        stein(s, ix, y, w, h, "txt", it, size=11)
        stein(s, mx, y, w, h, "num", m, size=11)
    base = top + 5 * pitch + h + 0.07
    platte(s, ex - 0.06, base, mx + w + 0.06 - (ex - 0.06))
    for x, bw, t in [(ex, ew, "names_from"), (mx, w, "values_from")]:
        tw = text_width(t, MONO, 10.5, True) + 0.14
        label_box(s, x + bw / 2 - tw / 2, base + 0.17, tw, 0.3, t, PALE, color=INK, size=10.5, rounded=False,
                  margin=0)
    # wide: der Funktionsname steht über dem Ergebnis (zwischen den Platten ist für ihn kein Platz)
    pa = mx + w + 0.1
    wx = pa + 0.6
    wt = 0.45                                              # Oberkante der Spaltenköpfe
    text(s, wx, 0.12, 2.0, 0.28, mono("pivot_wider()", size=10.5, color=GREEN, align="start"))
    kopf(s, wx, w, wt, "item", "<chr>", size=10.5)
    sx = [wx + w + 0.08, wx + w + 0.16 + ew]
    for x, r in zip(sx, (alt, neu)):
        label_box(s, x, wt - 0.02, ew, 0.32, r, INK, size=10, rounded=False, margin=0.03)
        text(s, x, wt + 0.32, ew, 0.22, mono("<dbl>", size=10, color=GRAY, bold=False))
    wtop = wt + 0.62
    for i, it in enumerate(items):
        y = wtop + i * pitch
        stein(s, wx, y, w, h, "txt", it, size=11)
        for x, r in zip(sx, (alt, neu)):
            stein(s, x + (ew - w) / 2, y, w, h, "num", mw[(r, it)], size=11)
    wbase = wtop + 2 * pitch + h + 0.07
    platte(s, wx - 0.06, wbase, sx[1] + ew + 0.06 - (wx - 0.06))
    mitte = wtop + pitch + h / 2
    arrow(s, pa, mitte - 0.14, w=0.5, h=0.28, color=GREEN)
    text(s, 0.12, base + 0.57, 7.5, 0.28, code([tr("pivot_wider(names_from = eastwest, values_from = mw)")], size=10.5))
    return s


# 5.7.2 row_count() aus dem Chunk `row-count-demo`: respid 1 (keine 7), 2 (keine Antwort) und 95, die erste Person
# mit genau drei Siebenern ------------------------------------------------------------------------------------------
def row_count_fig():
    s = Canvas(7.75, 2.15)
    items = ["mm01", "mm02", "mm03", "mm04", "mm05", "mm06"]
    reihen = [("1", ["5", "3", "4", "2", "6", "2"], "0", tr("keine 7")),
              ("2", ["", "", "", "", "", ""], "0", tr("keine Antwort")),
              ("95", ["7", "1", "6", "7", "4", "7"], "3", tr("dreimal 7"))]
    h, pitch, top, w, step, ix = 0.32, 0.4, 0.62, 0.52, 0.62, 1.0
    kopf(s, 0.15, 0.6, 0.15, "respid")
    for j, it in enumerate(items):
        kopf(s, ix + j * step, w, 0.15, it, size=10.5)
    rx, rw = 5.95, 0.6
    kopf(s, rx, rw, 0.08, tr("n_extrem"), "<int>", size=10.5)
    for i, (rid, werte, n, notiz_) in enumerate(reihen):
        y = top + i * pitch
        text(s, 0.15, y, 0.6, h, mono(rid, size=10.5, color=GRAY, align=RT), anchor="middle")
        for j, v in enumerate(werte):
            stein(s, ix + j * step, y, w, h, "num" if v == "7" else ("dim" if v else "na"), v, size=11)
        stein(s, rx, y, rw, h, "num", n, size=11)
        text(s, rx + rw + 0.12, y, 1.0, h, notiz(notiz_, size=10.5, color=GRAY, align="start"), anchor="middle")
    unten = top + 2 * pitch + h
    platte(s, 0.85, unten + 0.07, ix + 5 * step + w + 0.1 - 0.85)
    platte(s, rx - 0.1, unten + 0.07, rw + 0.2)
    mitte = (top + unten) / 2
    ax = ix + 5 * step + w + 0.2
    text(s, ax - 0.1, mitte - 0.45, rx - ax, 0.28, mono("row_count()", size=10.5, color=GREEN))
    arrow(s, ax, mitte - 0.14, w=rx - ax - 0.2, h=0.28, color=GREEN)
    text(s, ax - 0.1, mitte + 0.18, rx - ax, 0.28, mono("count = 7", size=10, color=GREEN))
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
    "k05-std": std_fig,
    "k05-join": join_fig,
    "k05-join-familie": join_familie,
    "k05-pivot-longer": pivot_longer_fig,
    "k05-pivot-wider": pivot_wider_fig,
    "k05-row-count": row_count_fig,
}
