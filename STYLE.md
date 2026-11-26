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
- **Sonst kein Fettdruck** im Fließtext: keine fetten Betonungen (sparsam *kursiv*), keine fetten Listen-Einstiege, keine fetten Zahlen. Ausnahmen sind die Marken **Frage:** und **Lesart.** und der Einstieg offener Kästen (§ 4).
- **Englische Originalbegriffe** in *kursiv*, sofern Standard (z. B. *random sampling*, *missing at random*).
- **Keine Wir-Inflation.** „Wir" nur, wenn es ein gemeinsamer Erkenntnisweg ist, nicht als Füllwort.

---

## 4 — Callout-Boxen

Vier Typen, einheitlich gesetzt, jeweils in Quarto-Syntax `::: {.callout-…}`. Seit dem 26.11.2026 (Rückmeldung: zu viele Kästen, zu viel Fett) gilt:

- **Offen** stehen nur Vorsicht und SPSS → R, dazu das Forschungsjournal am Kapitelanfang und -ende. Einstieg fett: `**Vorsicht: Titel.** Text …`
- **Zugeklappt** sind Hintergrund und mariposa-Tipp. Der Titel steht als Überschrift in der ersten Zeile, der Kasten zeigt dann nur diese Zeile:

  ```
  ::: {.callout-note collapse="true"}
  ## Hintergrund: Titel ohne Schlusspunkt

  Text …
  :::
  ```

  (mariposa-Tipp: `::: {.callout-important collapse="true"}` mit `## mariposa-Tipp: …`)
- **Nie zwei Kästen direkt untereinander.** Ein Kasten steht bei dem Absatz, den er ergänzt. Was zum Verständnis des Kapitels nötig ist, gehört in den Fließtext, nicht in einen Kasten. Wiederholt ein Kasten nur den Text, fällt er weg.
- Andere Einstiege (Konzept, Forschungshintergrund, Reviewer-Hinweis, Tipp, Faustregel) gibt es nicht mehr; sie werden zu Hintergrund, Vorsicht, mariposa-Tipp oder Fließtext.
- Prüfen: `python3 figuren/pruefe_kaesten.py <kapitel.qmd>`.

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

**Kurz überlegen** (Absatz plus eingeklappter `.callout-tip`)
> Eine Denkpause an einer Stelle, an der Lernende das Ergebnis selbst vorhersagen können. Ein Absatz beginnt mit **Kurz überlegen.** und stellt eine Frage zu einem *neuen* Fall, den die Abbildung daneben nicht zeigt. Direkt darunter folgt die Auflösung als `::: {.callout-tip title="Auflösung" collapse="true"}` mit Text und Code, ohne Bild. Sparsam, höchstens eine pro Abschnitt (derzeit 14).

**Aussehen im Buch.** Im Design „Baukasten“ liest `seite.html` den fetten Einstieg eines Kastens und setzt ihn als eigenen Kastentyp mit Begleitfigur. Erkannt werden die Einstiege Hintergrund, Forschungshintergrund, Konzept, Forschungsjournal, Reviewer-Hinweis, SPSS → R, mariposa-Tipp, Vorsicht, Tipp und Faustregel, außerdem Übungen (`title="Übung …"`), Lösungen und „Kurz überlegen“ mit Auflösung. Ein neuer Einstieg gehört in die Liste `TYPEN` in `seite.html`, sonst bekommt der Kasten das schlichte Standardaussehen. Ohne JavaScript bleibt das Buch lesbar, nur schlichter.

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

---

## 12 — Abbildungen

Erklärgrafiken in der Bausteine-Bildsprache (Stein = Wert, Turm = Vektor, Bauplatte = Datensatz, Aufkleber = Label) regelt `BILDER.md`: Werkzeug, Aussehen, Einbindung und Liste. Kurz: Die Bilder entstehen mit `python3 figuren/build.py` als SVG in `Bilder/figuren/`, zeigen die Werte des Chunks, neben dem sie stehen, und werden mit `{#fig-… .lightbox fig-alt="…"}` eingebunden und im Text mit `@fig-…` angesprochen.

---

## 13 — Englische Fassung

Die englische Fassung (`*.en.qmd` neben den deutschen Dateien, gerendert nach `docs/en/`) ist für ein englischsprachiges Publikum gedacht, etwa für Teilnehmende der Summer Schools in Essex und Lugano, die das Buch als Nachschlagewerk nutzen. Die deutsche Fassung bleibt die Quelle: Wer ein deutsches Kapitel ändert, ändert die englische Fassung im selben Commit mit. Hintergrund und Entscheidungen stehen in `ENGLISCH-DESIGN.md`.

Die Regeln und Begriffe in diesem Abschnitt sind vorläufig. Yannick liest den Pilot (Vorwort und Kap. 4) und korrigiert Ton und Begriffe; seine Korrekturen kommen hierher und gelten dann für alle weiteren Kapitel.

**Sprache.**

- Britisches Englisch im Fließtext (*colour*, *analyse*, *visualisation*, *organisation*, *licence* als Nomen). Code und Funktionsargumente folgen den Paketen.
- Du-Form als *you*. Schlicht und sachlich: direkt sagen, was eine Funktion tut oder was zu sehen ist.
- Alle Regeln aus §1–12 gelten auch im Englischen, besonders §3 und §10: aktiv vor passiv, keine Wir-Inflation, kein Werbeton. Fett nur Fachbegriffe beim ersten Auftreten, die Marken und die Einstiege der Kästen. Kursiv sparsam; die Regel „englische Originalbegriffe kursiv“ entfällt.
- Geschlechtsneutral ohne Sonderzeichen: neutrale Wörter (*people switching from SPSS*, *users*, *participants*), wo nötig singular *they*. Das ersetzt `:innen`.
- Anführungszeichen typografisch doppelt “…”, innen einfach ‘…’.
- Zahlen im Text wie in den Ausgaben: Dezimalpunkt, keine Tausendertrennung, wo die Ausgabe keine hat (5246). Datumsangaben ausgeschrieben (26 November 2026).
- Kapitelverweise im Fließtext als „Chapter 4“, „Chapters 4–5“; „Ch. 4“ nur, wo der Platz knapp ist (Grafiken, Tabellen).
- Tasten unter Windows mit englischer Beschriftung: `ctrl` statt `strg`.

**Anti-Ziele** (`ENGLISCH-DESIGN.md` §2). Der englische Text darf nicht nach Maschinenübersetzung oder nach KI klingen. Also keine Slogans und Paarformeln (*Three findings, three sentences*), keine Pointen mit Gedankenstrich (*– and nobody notices*), keine „not X, but Y“-Figuren (auch kein „not only … but also“ als Effekt), keine Dreierfiguren als Effekt, keine Meta-Sätze über das Material (*The five green signs …*), keine verspielten Etiketten. Bilder aus der Bausteine-Sprache (§12) sind erwünscht, Wortspiele darum herum nicht. Gedankenstriche aus dem Deutschen werden meist zu Komma, Doppelpunkt, Semikolon oder einem neuen Satz. Ebenfalls ein Fehlschlag: Zahlen in den Lesarten passen nicht zu den Ausgaben, oder ein Kapitel ist halb deutsch (übersehene Labels, Kästen, Bildunterschriften, Alt-Texte).

**Übertragen, nicht umschreiben.** Inhalt, Reihenfolge und Umfang bleiben wie im Deutschen; nichts kommt dazu, nichts fällt weg. Wo der deutsche Text ein deutsches Publikum voraussetzt (SPSS-Gewohnheiten an deutschen Unis, deutsche Studiengänge, „Seminararbeit“, Datum- und Zahlenformate, deutsche Tastaturbeschriftung), passt die englische Fassung das an.

**Daten und Code** (`ENGLISCH-DESIGN.md` §5.3).

- ALLBUS heißt beim ersten Auftreten „German General Social Survey (ALLBUS)“, danach „ALLBUS“ oder „ALLBUS 2023“.
- Die Anleitung zum Herunterladen nennt die englische Ausgabe bei GESIS: Studiennummer ZA8833, „German General Social Survey – ALLBUScompact 2023“ (<https://search.gesis.org/research_data/ZA8833>). Gespeichert wird die Datei wie im Deutschen als `ALLBUS2023.sav`, und der sichtbare Code zeigt `read_spss("ALLBUS2023.sav")`. Im Buchprojekt liegt die englische Datei als `ALLBUS2023_en.sav`; ein unsichtbarer Setup-Schritt in den englischen Kapiteln leitet darauf um.
- Eigene Variablen- und Objektnamen werden englisch: `islamophobie` → `islamophobia`, `populismus` → `populism`, `islamophobie_p` → `islamophobia_p`, `populismus_p` → `populism_p`, und so weiter für alle im Buch gebildeten Variablen und Objekte. ALLBUS-Variablennamen (`mm01`, `ls01`, `eastwest`, `wghtpew` …), `allbus`, Funktions- und Dateinamen bleiben.
- Englisch werden Kommentare im Code, Achsentitel, Legenden, Kategorien in `rec()`- und `labels = c(…)`-Aufrufen, Prompt-Vorlagen (Kap. 10) und YAML-Beispiele (Kap. 2).
- Die Lesarten zitieren die tatsächlichen englischen Labels aus ZA8833, keine eigenen Übersetzungen der deutschen Labels.

**Aufbau und IDs.**

- Jede `.en.qmd` setzt `output-file: <deutscher Dateiname>.html` im Kopf.
- Gleicher Aufbau wie im Deutschen: dieselben Überschriften auf denselben Ebenen, dieselbe Zahl an Chunks, Kästen derselben Klassen, dieselben Abbildungen und Übungen.
- Alle IDs bleiben gleich: `{#sec-…}`, `{#fig-…}`, Chunk-Labels. Überschriften ohne eigene ID bekommen ihren Anker aus dem englischen Text; das ist so gewollt.
- Prüfen mit `python3 figuren/check_en.py <name>` (Aufbau, Zahlen in den Ausgaben, deutsche Reste), rendern einzeln mit `quarto render <name>.en.qmd --profile en`.

**Feste Wörter für Kästen und Karten.** `seite.html` erkennt genau diese Wörter (§4, `ENGLISCH-DESIGN.md` §5.5). Sie werden wörtlich so geschrieben.

| Deutsch | Englisch | Wo |
|---|---|---|
| **Frage:** | **Question:** | Marke (§1) |
| **Lesart.** | **Interpretation.** | Marke (§1) |
| Hintergrund: | Background: | zugeklappt, `## Background: …` |
| Forschungshintergrund: | Research background: | wie Hintergrund; derzeit in keinem Kapitel, `seite.html` kennt das englische Wort noch nicht |
| Vorsicht: | Caution: | offen, `**Caution: Title.** …` |
| mariposa-Tipp: | mariposa tip: | zugeklappt, `## mariposa tip: …` |
| SPSS → R | SPSS → R | offen, `**SPSS → R.** …` oder `**SPSS → R: Title.** …` |
| Forschungsjournal: | Research journal: | offen, Kapitelanfang und -ende |
| Übung *n* · *Thema* · *Typ* | Exercise *n* · *Topic* · *Type* | Titel der Übung |
| Lösung | Solution | Titel der Lösung |
| **Kurz überlegen.** | **Stop and think.** | fetter Absatzeinstieg |
| Auflösung | Answer | Titel des eingeklappten Kastens darunter |
| Was du nach diesem Kapitel kannst | What you will be able to do after this chapter | H2 (im Vorwort: … after this book) |
| Was du jetzt weißt | What you know now | H2 |
| Weiterführend | Further reading | H2 |
| Reproduktion | Reproduction | Übungstyp (§7) |
| Transfer | Transfer | Übungstyp (§7) |
| Mini-Forschungsfrage | Mini research question | Übungstyp (§7) |

**Weitere Begriffe** (Vorschläge, der Pilot ändert sie noch).

| Deutsch | Englisch |
|---|---|
| Mini-Studie | mini study |
| Forschungsjournal, Übung, Lösung, Mini-Forschungsfrage im Fließtext | research journal, exercise, solution, mini research question |
| Musterlösung | model solution |
| Kasten | box |
| Methoden-Kapitel | methods chapter |
| Worum es geht | What this chapter is about |
| Übungen (H2) | Exercises |
| Datensatz | dataset |
| Variablenlabel, Wertelabel | variable label, value label |
| fehlende Werte | missing values |
| umpolen | reverse-code (*reverse coding* als Begriff) |
| Gewichtung | weighting |
| Islamfeindlichkeit, islamfeindlich | Islamophobia, Islamophobic |
| Stein, Turm, Bauplatte, Aufkleber | brick, tower, baseplate, sticker |
| Begleitfigur | companion figure |
| Umsteiger:innen aus SPSS | people switching from SPSS |

**Kapiteltitel** (Vorschlag, so in den Kapitelkarten des englischen Vorworts): 1 RStudio · 2 Quarto and reproducible research · 3 The R programming language · 4 Data import and inspection · 5 Transforming data and building scales · 6 Visualisation basics · 7 Univariate and bivariate analysis · 8 Latent structures · 9 Explanatory models · 10 Working with AI assistants.
