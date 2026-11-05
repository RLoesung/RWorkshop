# Style Guide — RWorkshop 2026

**Zweck.** Didaktischer und stilistischer Vertrag für die Modernisierung. Geltungsbereich: alle `.qmd`-Kapitel des RWorkshop. Code-Konventionen für die R-Snippets stehen in `MIGRATION.md`; *dieser* Guide regelt **Aufbau, Sprache und Vermittlung**.

---

## 1 — Leitprinzip: Frage → Code → Lesart

Jeder neue Begriff, jede neue Funktion folgt diesem Dreischritt:

1. **Frage.** Eine echte Forschungsfrage in einem Satz. *„Unterscheidet sich die Lebenszufriedenheit zwischen Ost- und Westdeutschland?"* — nicht: *„Wir lernen jetzt den t-Test."*
2. **Code.** Ein lauffähiger, kommentierter Chunk, der genau diese Frage beantwortet.
3. **Lesart.** Wie liest man den Output, was bedeutet das inhaltlich, welche Anschlussfrage ergibt sich?

Wo der Stoff es zulässt: gleiches Muster auf Kapitelebene (Kapitel-Frage → Methoden → Ergebnis-Interpretation).

---

## 2 — Kapitelstruktur (verbindlich)

Jedes Methoden-Kapitel hat **mindestens** diese Abschnitte, in dieser Reihenfolge:

```
# Kapitelthema

## Worum es geht
[2–4 Sätze, motivierende Frage]

## Was du nach diesem Kapitel kannst
[3–6 Bullets mit Lernzielen, im Du]

## [Methodische Abschnitte nach Frage → Code → Lesart]

## Übungen
[in der Regel vier Aufgaben, Lösungen als eingeklappte Callouts — siehe Abschnitt 7]

## Was du jetzt weißt
[knappe Wiederholung der Lernziele als Selbstcheck]

## Weiterführend
[1–3 Pointer auf Vertiefungsliteratur oder das nächste Kapitel]
```

---

## 3 — Sprache & Stil

- **Du-Form** durchgehend. Direkter, motivierender, weniger akademisch-distanziert.
- **Aktiv vor Passiv.** *„Wir wählen die Variable aus"* — nicht *„Die Variable wird ausgewählt"*.
- **Geschlechtersensible Sprache:** `:innen` (z. B. „Anwender:innen"), wie bisher im Skript etabliert.
- **Fachbegriffe** beim ersten Auftreten **fett** + 1-Satz-Definition. Danach normal.
- **Englische Originalbegriffe** in *kursiv*, sofern Standard (z. B. *random sampling*, *missing at random*).
- **Keine Wir-Inflation.** „Wir" nur, wenn es ein gemeinsamer Erkenntnisweg ist, nicht als Füllwort.

---

## 4 — Callout-Boxen

Vier Typen, einheitlich gesetzt, jeweils in Quarto-Syntax `::: {.callout-…}`.

**SPSS → R** (`.callout-tip` mit eigenem Icon-Override)
> Brücke für Umsteiger:innen aus SPSS. Direktvergleich Syntax/Output. Nicht inflationär — nur wo der Übergang nicht offensichtlich ist.
>
> *Beispiel: „In SPSS schreibst du `FREQUENCIES VARIABLES=sex.` — in R: `allbus |> frequency(sex)`."*

**Vorsicht** (`.callout-warning`)
> Typische Fallstricke. *Labelled-Vektoren ≠ Faktoren.* *Gewichtung pro Analyse, nicht session-wide.* *Tagged NAs verlieren beim `as.numeric()` ihre Information.* Sparsam, dafür wirksam.

**Hintergrund** (`.callout-note`)
> Kurze konzeptionelle Vertiefung ohne Mathematik. „Was misst Cronbachs α eigentlich?" — 3–5 Sätze, danach zurück zum Code.

**mariposa-Tipp** (`.callout-important` oder eigener Style)
> Wo mariposa eine besonders elegante Abkürzung bietet. Z. B. dass `pearson_cor()` Korrelations**matrix**, KIs und Sterne in einem Aufruf liefert. Erkennbarkeit schaffen, nicht Marketing.

**Verbot.** Keine weiteren Callout-Typen ohne Eintrag hier. Wildwuchs vermeiden.

---

## 5 — Code-Konvention im Lehrtext

- **Inline-Code** in Backticks: `frequency(allbus, sex)`.
- **Variablennamen** wie im Datensatz: `sex`, `eastwest`, `wghtpew`.
- **Paket-Präfix** nur im Lehrabschnitt, der genau diese Funktion einführt (`mariposa::frequency()` zur ersten Erklärung — danach ohne Präfix).
- **Argumente erklären** bei Erstkontakt, nicht bei jedem Auftreten.
- **Outputs** als Chunk-Output rendern, nicht im Text wiederholen (es sei denn, die Lesart bezieht sich auf konkrete Zahlen).

**Code-Annotation (Quarto-Feature).** Bei Erstkontakt komplexerer Pipelines:

````
```r
allbus |>                          # <1>
  filter(sex == "Frau") |>         # <2>
  describe(life_satisfaction)      # <3>
```
1. Datensatz als Pipe-Quelle
2. nur Frauen behalten
3. mariposa-Funktion für deskriptive Statistik
````

Statt `# kommentar`-Wüste im Chunk.

---

## 6 — ggplot2-Konvention

- Ein **zentrales Theme** `theme_rworkshop()`, einmal in `R/_common.R` definiert und dort per `theme_set()` global aktiv gesetzt. Die Kapitel laden die Datei im Setup-Chunk mit `source("R/_common.R")`.
- **Variablenlabels** auf Achsen, nicht technische Namen. Bei labelled-Variablen über `to_label()` lösen.
- **Farbskala** konsistent: kategoriale Variablen über eine ALLBUS-Palette (Ost/West, Geschlecht, Bildung — barrierearm getestet); kontinuierliche Variablen über `viridis`.
- **Patchwork** für Multi-Plots: `p1 + p2 / p3` statt `gridExtra::grid.arrange()`.
- **Gewichtung** explizit ausweisen, wenn benutzt: Caption „Gewichtet mit `wghtpew`, ALLBUS 2023".

**Beispiel (Skelett):**
```r
allbus |>
  to_label(sex) |>
  ggplot(aes(x = sex, y = ls01, weight = wghtpew)) +
  stat_summary(fun = mean, geom = "col", fill = "#1f77b4") +
  labs(x = NULL, y = "Lebenszufriedenheit (0–10)",
       caption = "ALLBUS 2023, gewichtet mit wghtpew") +
  theme_rworkshop()
```

---

## 7 — Übungsformat

Am Kapitelende stehen in der Regel vier Aufgaben mit ansteigender Schwierigkeit:

1. **Reproduktion** (meist zwei Aufgaben) — anwenden, was im Kapitel direkt gezeigt wurde, auf eine andere Variable.
2. **Transfer** — Kombination zweier Techniken aus dem Kapitel.
3. **Mini-Forschungsfrage** — kleine eigene Forschungsfrage, eigene Variablenwahl, offene Lesart. In der Regel ohne Musterlösung; über die Kapitel hinweg entsteht so ein eigenes kleines Projekt.

Jede Aufgabe ist ein `.callout-note` mit dem Titel „Übung *n* · *Thema* · *Typ*". Die Lösung folgt direkt darunter als eingeklappter `.callout-tip` (`title="Lösung" collapse="true"`), mit kurzem Interpretations-Satz. Lernende sollen erst selbst versuchen.

---

## 8 — Reproduzierbarkeit pro Kapitel

Jedes Kapitel muss **alleine** rendern können:

- Eigener Setup-Chunk (`echo = FALSE`) lädt Pakete und liest ALLBUS 2023 ein.
- Keine Abhängigkeit von Variablen, die in einem früheren Kapitel definiert wurden.
- Wenn ein Kapitel auf dem in Kap. 5 erstellten Analyse-Datensatz aufbaut, erzeugt es ihn am Kapitelanfang neu, und zwar per `source("R/prep.R")`. `R/prep.R` ist die einzige verbindliche Fassung der Datenpräp-Pipeline. Ändert sich die Pipeline in Kap. 5, wird `R/prep.R` mitgezogen.

---

## 9 — Cross-References

In Quarto über `@sec-…`-Tags. Beim Verweis im Fließtext:

> „Wir hatten in @sec-rekodierung gesehen, dass Werte unter 0 als fehlend deklariert werden."

Statt: *„wie oben/unten/in Kapitel 3.4 …"*.

---

## 10 — Was nicht ins Buch gehört

- **Anekdoten ohne Lehrwert.** „Damals als der Tidyverse-Pipe noch …" — nur, wenn es einen Punkt belegt.
- **Selbstreferenz.** Kein Lob für mariposa, das nicht auf einer demonstrierten Fähigkeit beruht. Die Funktion soll überzeugen, nicht der Werbetext.
- **Mathematik-Wand.** Wenn eine Formel kommt, dann *eine*, mit Erklärung jedes Symbols. Sonst Verweis auf Hintergrund-Callout oder Weiterführend-Liste.
- **„Best Practice" als Killer-Phrase.** Wenn eine Konvention erklärt wird, sagen wir *warum*. *„… weil Faktoren im Modell die Referenzgruppe automatisch setzen"* — nicht *„weil es Best Practice ist"*.

---

## 11 — Mini-Studie als roter Faden

Der gesamte Daten- und Methodenteil (Kap. 4–9) wird durch **eine** Forschungsfrage aus ALLBUS 2023 getragen. Variablenauswahl, Forschungsfrage und Methoden-Mapping siehe `STUDIE.md`. Andere Beispiele dürfen ergänzend kommen, aber die Mini-Studie ist der Anker, an dem jede Methode mindestens einmal demonstriert wird.
