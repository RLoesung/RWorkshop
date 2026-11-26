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
- Eigene Variablen- und Objektnamen werden englisch: `islamophobie` → `islamophobia`, `populismus` → `populism`, `islamophobie_p` → `islamophobia_p`, `populismus_p` → `populism_p`, und so weiter für alle im Buch gebildeten Variablen und Objekte. Verbindlich ist die Tabelle „Namen im Code“ am Ende dieses Abschnitts. ALLBUS-Variablennamen (`mm01`, `ls01`, `eastwest`, `wghtpew` …), `allbus`, Funktions- und Dateinamen bleiben.
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

### Namen im Code (verbindlich)

Diese Tabelle legt die englischen Namen für alles fest, was das Buch im Code selbst benennt: Variablen, Objekte, Spalten, Listenelemente, Modelle, Faktorstufen und Labels. Sie gilt für die `.en.qmd`-Dateien, für `R/prep_en.R` und für die englischen Abbildungen (`figuren/en.py`). Ein Name, der in mehreren Kapiteln vorkommt (etwa `educ_cat` in Kap. 6, 7 und 9), heißt überall gleich. Fehlt ein Name, trägst du ihn im selben Commit hier nach, nach diesen Regeln:

- snake_case, kurz, ohne Umlaute, mit derselben Bedeutung wie im Deutschen.
- Ein mit `<-` angelegtes Objekt heißt nicht wie eine Funktion aus base R oder dem tidyverse (deshalb `first_names`, nicht `names`); `data` bleibt Platzhalter wie in Kap. 4. Als Spaltenname ist ein Funktionsname erlaubt (`mean`, `factor`), so wie im Deutschen `sd`.
- Fiele der englische Name mit einem ALLBUS-Namen zusammen, bekommt er einen Zusatz (`rename(age_years = age)` in Kap. 5).

| Deutsch | Englisch | Kapitel |
|---|---|---|
| `islamophobie` | `islamophobia` | `R/prep.R`, Vorwort, 3–9 |
| `populismus` | `populism` | `R/prep.R`, 4–7, 9 |
| `islamophobie_p` | `islamophobia_p` | `R/prep.R`, 5, 7 |
| `populismus_p` | `populism_p` | `R/prep.R`, 5, 7 |
| `islam_hoch` | `islamophobia_high` | 4, 9 |
| `educ_kat` | `educ_cat` | 6, 7, 9 |
| `ergebnis` (Zuweisung in Kap. 1, Liste in Kap. 3, Verweis in Kap. 8) | `result` | 1, 3, 8 |
| `mein-chunk` (Chunk-Label im Beispiel) | `my-chunk` | 2 |
| `mittelwert_alter`, `mittelwertAlter`, `Mittelwert.alter`, `mittelwertAlter_neu`, `mittelwert alter` (Beispiele für Namenskonventionen) | `mean_age`, `meanAge`, `Mean.age`, `meanAge_new`, `mean age` | 3 |
| `faktor_skala`, `islamophobie_skala` | `factor_scale`, `islamophobia_scale` | 3 |
| `n_befragte` | `n_respondents` | 3 |
| `funktionsname(arg1 = wert1, arg2 = wert2, ...)` | `function_name(arg1 = value1, arg2 = value2, ...)` | 3 |
| `zahlen` | `numbers` | 3 |
| `alter` (Vektor und Spalte von `befragte`; bewusste Ausnahme von der Zusatz-Regel, weil der ALLBUS in Kap. 3 nicht geladen ist) | `age` | 3 |
| `namen` | `first_names` | 3 |
| `geschlecht` (Faktor und Spalte von `befragte`; in Kap. 5 `rename(geschlecht = sex)`) | `gender` | 3, 5 |
| `befragte` | `respondents` | 3 |
| `spalte` | `column` | 3 |
| `koeffizient`, `p_wert`, `konfidenz`, `modell` (Elemente der Liste `ergebnis`) | `coefficient`, `p_value`, `conf_int`, `model` | 3 |
| `daten` (`daten$age`) | `data` | 3 |
| `wert` (Spalte in `demo` und in den Hilfstabellen für Grafiken) | `value` | 3, 7, 8, 9 |
| `bildung` (Faktor in Kap. 3, `case_when()` in Kap. 5) | `education` | 3, 5 |
| `vertrauen` | `trust` | 3 |
| `analyse` | `analysis` | 4 |
| `geburtsjahr` | `birth_year` | 5 |
| `allbus_neu` | `allbus_new` | 5 |
| `if_else(bedingung, wert_wenn_wahr, wert_wenn_falsch)` | `if_else(condition, value_if_true, value_if_false)` | 5 |
| `jung` | `young` | 5 |
| `n_faelle`, `n_einz_bildung`, `durchschnitt_alter` | `n_cases`, `n_distinct_educ`, `mean_age` | 5 |
| `alter` in `rename(alter = age)` | `age_years` | 5 |
| `neu`, `alt` (Platzhalter in `mutate(neu = rec(alt, …))` und in der Tabelle der Regel-Syntax: `alt=neu`, `lo:hi=neu`, `NA=neu` …) | `new`, `old` | 5 |
| `Wortlaut`, `Polung` (Spalten der Item-Tabelle; `Item` bleibt) | `Wording`, `Direction` | 5 |
| `kontext_bl` | `region_context` | 5 |
| `muslim_anteil`, `bip_pro_kopf` | `muslim_share`, `gdp_per_capita` | 5 |
| `allbus_mit_kontext` | `allbus_with_context` | 5 |
| `antwort` | `response` | 5 |
| `mittelwerte_long` | `means_long` | 5 |
| `mw` (Spalte oder Einzelwert „Mittelwert“) | `m` | 5, 7, 9 |
| `skala_4` | `scale_4` | 5 |
| `n_extrem` (Spalte in der Abbildung zu `row_count()`) | `n_extreme` | 5 |
| `polit_effizienz` | `pol_efficacy` | 5 |
| `vier` | `four` | 6 |
| `farben` | `color_values` | 6 |
| `sim_mw` | `sim_means` | 7 |
| `ziehung` | `draw` | 7 |
| `mittelwert` (Spalte) | `mean` | 7 |
| `wahrer_wert` | `true_value` | 7 |
| `sim_kis` | `sim_cis` | 7 |
| `studie` | `study` | 7 |
| `enthaelt` | `covers` | 7 |
| `linksschief`, `symmetrisch`, `rechtsschief` (Spalten, danach Stufen von `form`) | `left_skewed`, `symmetric`, `right_skewed` | 7 |
| `form` | `shape` | 7 |
| `gruppe` | `group` | 7, 9 |
| `efa_vor` | `efa_check` | 8 |
| `gemeinsam`, `partiell` (Spalten, danach Werte von `anteil`) | `shared`, `partial` | 8 |
| `anteil` | `share` | 8, 9 |
| `faktor` (Spalte im Scree-Plot) | `factor` | 8 |
| `eigenwert` | `eigenvalue` | 8 |
| `faktor_radial` | `factor_radial` | 8 |
| `ladung` | `loading` | 8 |
| `winkel` | `angle` | 8 |
| `modell_cfa` | `model_cfa` | 8 |
| `schwelle`, `richtung`, `erfuellt` | `threshold`, `direction`, `met` | 8 |
| `modell` (lavaan-Modell in Kap. 8, Regressionsmodell in Kap. 9) | `model` | 8, 9 |
| `gummi_demo`, `m_gummi` | `rubber_demo`, `m_rubber` | 9 |
| `m_einfach` | `m_simple` | 9 |
| `allbus_modell` | `allbus_model` | 9 |
| `m_basis`, `m_voll` | `m_base`, `m_full` | 9 |
| `hilfsmodell` | `aux_model` | 9 |
| `vif_populismus` | `vif_populism` | 9 |
| `diagnose_df` | `diag_df` | 9 |
| `wahrscheinlichkeit` | `probability` | 9 |
| `modell_log` | `model_log` | 9 |
| `hilfs_age` | `aux_age` | 9 |
| `demo_zufrieden` | `demo_satisfied` | 9 |
| `educ_katniedrig`, `educ_katmittel`, `educ_kathoch` (Koeffizientennamen, die R aus Variable und Stufe bildet) | `educ_catlow`, `educ_catmedium`, `educ_cathigh` | 9 |
| `beispiel` | `example_data` | 10 |
| `mittel` (Spalte in `summarise()`) | `mean` | 10 |
| `ost` | `east` | 10 |

`mean_age` (Kap. 3, 5), `mean` (Kap. 7, 10) und `model` (Kap. 3, 8, 9) kommen mehrfach vor, jeweils als Name, der nur im eigenen Kapitel gilt.

Die Dummies von `sex` (`sexFRAU`, `sexDIVERS` in Kap. 9) übersetzt du nicht selbst; sie heißen so, wie R sie aus den ZA8833-Labels bildet, und werden aus der englischen Ausgabe abgeschrieben.

**Stufen, Kategorien und Labels im Code.** Englische Stufen sind klein, wie die deutschen Adjektive (`low`, `medium`, `high`); auch Substantive werden klein (`male`, `men`). Groß bleiben Himmelsrichtungen als Regionsnamen (`West`, `East`), Bezeichnungen mit Kennbuchstaben (`Group A`) und die ALLBUS-Labels aus ZA8833 (`MALE`, `OLD FEDERAL STATES`), die nie selbst übersetzt werden.

| Deutsch | Englisch | Kapitel |
|---|---|---|
| `[niedrig]`, `[mittel]`, `[hoch]` in `rec()` (`educ_kat`, `educ`, `isced97`) | `[low]`, `[medium]`, `[high]` | 5, 6, 7, 9 |
| `"niedrig"`, `"mittel"`, `"hoch"` (Faktor `bildung` in Kap. 3, `case_when()` in Kap. 5, `fct_relevel(educ_kat, "mittel")` in Kap. 9) | `"low"`, `"medium"`, `"high"` | 3, 5, 9 |
| `c("niedrig" = 0, "hoch" = 1)` in `val_labels()` | `c("low" = 0, "high" = 1)` | 4 |
| `"stimme gar nicht zu"`, `"stimme voll zu"` in `val_labels()` | `"completely disagree"`, `"completely agree"` | 4 |
| `"Mann"`, `"Frau"`, `"Divers"` | `"male"`, `"female"`, `"non-binary"` | 3 |
| `"ja"` | `"yes"` | 3 |
| `"hoch = islamophob"`, `"hoch = TOLERANT — umpolen"` (Item-Tabelle) | `"high = Islamophobic"`, `"high = TOLERANT, reverse-code"` | 5 |
| `"erwachsen"`, `"senior"`, `"unter 18"` | `"adult"`, `"senior"`, `"under 18"` | 5 |
| `"jung"`, `"30+"` | `"young"`, `"30+"` | 5 |
| `"West"`, `"Ost"` | `"West"`, `"East"` | 5, 10 |
| `"KI verfehlt wahren Wert"`, `"KI enthält wahren Wert"` | `"CI misses true value"`, `"CI contains true value"` | 7 |
| `` `Gruppe A (M = 2)` ``, `` `Gruppe B (M = 4)` `` | `` `Group A (M = 2)` ``, `` `Group B (M = 4)` `` | 7 |
| `"Gruppe A"`, `"Gruppe B"`, `"Gruppe C"` | `"Group A"`, `"Group B"`, `"Group C"` | 7 |
| `"gemeinsame Varianz (MSA)"`, `"partielle Varianz"` | `"shared variance (MSA)"`, `"partial variance"` | 8 |
| `"höher = besser"`, `"niedriger = besser"` | `"higher = better"`, `"lower = better"` | 8 |
| `"verfehlt"`, `"Schwelle erfüllt"` | `"missed"`, `"threshold met"` | 8 |
| `"erklärt durch Modell (R²)"`, `"unerklärt (Residuen)"` | `"explained by model (R²)"`, `"unexplained (residuals)"` | 9 |
| `"Männer"`, `"Frauen"` | `"men"`, `"women"` | 9 |

Wo R Stufen alphabetisch ordnet (`factor()` ohne `levels` in Kap. 3), ändert sich mit den englischen Wörtern die Reihenfolge: `high`, `low`, `medium` statt `hoch`, `mittel`, `niedrig`, und `female`, `male`, `non-binary` statt `Divers`, `Frau`, `Mann`. Text und Lesart folgen dann der englischen Ausgabe.

**Beispielnamen für Dateien.** Dateien, die es im Buchprojekt gibt oder die auf den RStudio-Bildschirmfotos stehen, behalten ihren Namen: `ALLBUS2023.sav`, `R/prep.R`, `R/_common.R`, die Kapiteldateien und der Projektordner `R-Workshop` (`ENGLISCH-DESIGN.md` §5.7). Namen für Dateien, die die Lesenden in einem Beispiel selbst anlegen, werden englisch:

| Deutsch | Englisch | Kapitel |
|---|---|---|
| `01-erste_schritte.qmd` | `01-first_steps.qmd` in Text und Abbildungen; die RStudio-Bildschirmfotos behalten den deutschen Namen, Kap. 1 sagt das in einem Satz | 1 |
| `mein-projekt/`, `mein-projekt.Rproj` | `my-project/`, `my-project.Rproj` | 2 |
| `analyse.qmd` | `analysis.qmd` | 2 |
| `literatur.bib` | `references.bib` | 2 |
| `befunde_mini_studie.png` | `mini_study_findings.png` | 9 |

**Bleiben unverändert** und stehen deshalb nicht in der Tabelle:

- ALLBUS-Variablennamen, `allbus` und Namen, die aus ALLBUS-Namen mit einem Kürzel entstehen: `mm02r`, `mm05r`, `pa29r` … `pa35r`, `pe05r`, `pe07r`, `age_d`, `age_q`, `age_z`, `age_c`, `allbus_mm`, `allbus_long`, `allbus_dummy`.
- Namen, die schon englisch oder sprachneutral sind: `var1`, `var2`, `x`, `y`, `a`, `n`, `d`, `z`, `r`, `se`, `sd`, `flags`, `demo`, `id`, `item`, `Item`, `Item1`, `Item2`, `MSA`, `index`, `label`, `region`, `outcome`, `logit`, `intercept`, `slope`, `r2`, `r2_age`, `y_hat`, `lower`, `upper`, `g`, `g_base`, `p`, `p1` … `p3`, `p_rf`, `p_qq`, `p_sl`, `p_rl`, `p_data`, `t_data`, `sim_cor`, `r_label`, `anova_demo`, `means`, `grand_mean`, `cor_obj`, `efa_obj`, `efa_1`, `rel_obj`, `items_unrot`, `items_rot`, `F1`, `F2`, `baseplot`, `ttl`, `sub`, `fit`.
- Die Kurzformen `islam_orig`, `islam_p`, `pop_orig`, `pop_p`, `islam` und `pop` (Kap. 5) und der latente Faktor `islam` im lavaan-Modell (Kap. 8). Die Kurzformen halten die Übersichtstabellen in Kap. 5 schmal; der latente Faktor bleibt wie im Deutschen kürzer als die gemessene Skala `islamophobia`, damit beide nicht verwechselt werden.
- Personennamen in Beispielen (`"Anna"`, `"Boris"`, `"Carla"`, Anna Schmidt, Boris Müller, `/Users/anna/…`), Funktionsnamen wie `theme_rworkshop()` und das Beispiel der R-Hilfe in Kap. 1 (`xm <- mean(x)`).

### Ein Kapitel übersetzen

Die Schritte für jedes Kapitel `NN-Name.qmd` → `NN-Name.en.qmd`. Vorbilder sind `index.en.qmd` und `04-Datenimport.en.qmd`.

1. **Abbildungen zuerst.** Die englischen SVGs des Kapitels entstehen vor dem Text: Texte in `figuren/kapNN.py` laufen über `sprache.t()`, die englischen Einträge stehen in `figuren/en.py`, das Modul setzt `SPRACHFAEHIG = True`, gebaut wird mit `python3 figuren/build.py --en NAME …` (`BILDER.md` §10). Eigene Namen im Bild nach der Tabelle oben.
2. **Kopf und Setup.** Im Kopf `output-file: NN-Name.html`. Der versteckte Setup-Chunk (Kap. 1 hat keinen) lädt `source("R/_common_en.R")` statt `source("R/_common.R")`; wo das deutsche Kapitel `source("R/prep.R")` lädt, steht `source("R/prep_en.R")`. Kapitelspezifische Ergänzungen im Setup (etwa `educ_cat` mit `[low]`, `[medium]`, `[high]`) folgen der Tabelle.
3. **Einlesen mit `set_na()`.** Wo der Code den ALLBUS einliest, sichtbar oder im versteckten Setup, steht `read_spss("ALLBUS2023.sav") |> set_na(-56, -55, -54, -53, -51, -50, -42, -41, -33, -32, -15, -11, -10, -9, -8, -7, -6)` (`ENGLISCH-DESIGN.md` §5.3). Abbildungen, die das Einlesen zeigen, nehmen den Schritt auf, bei Platzmangel als `|> set_na(-56, …, -6)`.
4. **Text und Code.** Übertragen nach den Regeln dieses Abschnitts: alle IDs und Chunk-Labels gleich, gleicher Aufbau, Kommentare, Achsentitel, Legenden und Kategorien englisch, eigene Namen nach der Tabelle, feste Wörter für Kästen und Karten wie oben.
5. **Abbildungspfade.** Jede Abbildung wird aus `Bilder/figuren/en/` eingebunden (`![…](Bilder/figuren/en/kNN-name.svg){#fig-… .lightbox fig-alt="…"}`), mit englischer Bildunterschrift und englischem `fig-alt`.
6. **Kapitelliste.** In `_quarto-en.yml` den Eintrag `NN-Name.qmd` durch `NN-Name.en.qmd` ersetzen.
7. **Rendern.** Einzeln und nur ein Render gleichzeitig: `quarto render NN-Name.en.qmd --profile en` (Quarto liegt unter `/Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto`).
8. **Lesarten abgleichen.** Jede Zahl und jedes zitierte Label gegen die gerenderte englische Ausgabe prüfen; ALLBUS-Labels in Großbuchstaben, wie ZA8833 sie druckt.
9. **Prüfen.** `python3 figuren/check_en.py NN-Name` muss 0 Meldungen ergeben. Bekannte, begründete Abweichungen (etwa andere Treffer von `find_var()`, andere Zeilenreihenfolge, Studiennummer und Version, `splt23_2` als `NA`) stehen mit einem Teilstring der Meldung und der Begründung in `figuren/erwartet_en.py`. Weicht eine Zahl ohne Grund in der Übersetzung ab: anhalten und melden.
10. **Tests.** `Rscript R/test_common_en.R` ergibt „ok“; bei Kapiteln mit `R/prep_en.R` auch `Rscript R/test_prep_en.R`.
11. **Im Browser ansehen.** `/RWorkshop/en/NN-Name.html`: Kästen, Übungen und Lösungen, Abbildungen, Querverweise, Sprachumschalter, Konsole ohne Fehler.
12. **Commit.** `git commit -m "Englische Fassung: Kap. N" -- NN-Name.en.qmd _quarto-en.yml _freeze/NN-Name.en/` und gegebenenfalls `figuren/erwartet_en.py` und `STYLE.md`; nie `git add -A` oder `git commit -a`.
