# Änderungsprotokoll

Neueste Änderungen stehen oben. Die Online-Fassung unter <https://rloesung.github.io/RWorkshop/> entspricht immer dem Stand von `main`.

## November 2026 — mariposa 0.7.4

Das Buch ist auf **mariposa 0.7.4** umgestellt, die erste Version auf CRAN. Alle Kapitel wurden gegen 0.7.4 neu gerechnet, und jede Zahl in den Lesart-Texten wurde gegen die echte Ausgabe geprüft.

### Behoben

- Kap. 6, 7 und 9 renderten nicht mehr: `rec(..., as.factor = TRUE)` ist seit mariposa 0.6.9 ein Fehler und heißt jetzt `as_factor = TRUE`.
- Veraltete Aufrufe aktualisiert: `set_na(educ = c(6, 7))` (benannte Paare), `crosstab(percentages = …)`, Übung 2 in Kap. 4 ohne das nicht existierende Item `pt05`, Korrelationsmatrix in Kap. 7 ohne versehentlich mitgewähltes `mm02r`.
- Kap. 8: `library(lavaan)` überdeckt mariposas `efa()`. lavaan und semPlot werden jetzt mit Präfix aufgerufen (`lavaan::cfa()`), dazu kommt ein Warnhinweis.
- Lesarten korrigiert:
  - Die Interaktion Bildung × Region ist nicht signifikant (*p* = .19).
  - Der VIF wird auf der Modellstichprobe berechnet und stimmt jetzt mit `summary()` überein.
  - Gewichtete Fallzahlen, Split-Fallzahlen, `dicho()`, Bildungscodes und Beta korrigiert.
  - `phi()` und `cramers_v()` liefern nur die Effektgröße als einzelne Zahl.
- `summary()`-Chunks ergänzt, wo die Lesart Tabellen beschreibt, die die kompakte Ausgabe nicht mehr zeigt: t-Test, Tukey, EFA, Reliabilität, ANCOVA.
- `rec(rules = "rev")` nimmt die Skalengrenzen jetzt aus den Wertelabels. Kap. 5 zeigt dazu einen Kontroll-Chunk und ruft `unlabel()` vor `pivot_longer()` auf.

### Neu

- **Kap. 1 und Vorwort:** Installation von mariposa über CRAN, `packageVersion()` und `citation("mariposa")`.
- **Kap. 4:**
  - `find_var()` mit regulären Ausdrücken.
  - Variablenlabels per Zuweisung setzen (`var_label(data$var) <- "…"`).
  - `codebook()` exportieren.
  - Wertelabels setzen mit `val_labels()`, inklusive `.add = TRUE`, damit die Labels der Missing-Codes erhalten bleiben. Danke an Jakob Krüger ([#15](https://github.com/RLoesung/RWorkshop/pull/15)).
- **Kap. 5:**
  - `recode_values()` statt des seit dplyr 1.2 veralteten `case_match()`.
  - Neue `rec()`-Regeln `a,b=neu` und `"rev(lo, hi)"`.
  - `rec()` für mehrere Variablen in einem Aufruf.
- **Kap. 7:**
  - `describe(show = …)`.
  - Residuen in `crosstab()`.
  - `normality_test()`.
  - Neuer Abschnitt zur partiellen Korrelation mit `partial_cor()`.
- **Kap. 8:**
  - McDonalds ω neben Cronbachs α.
  - Die Zwei-Faktor-Lösung wird als Methodenfaktor der umgepolten Items gelesen.
  - Der Radial-Plot zeigt echte Faktorladungen.
  - Rotation mit den SPSS-Algorithmen, ohne Zusatzpaket.
- **Kap. 9:**
  - VIF und Toleranz direkt aus `summary()`.
  - Durchschnittliche marginale Effekte mit `marginal_effects()`.
  - Bereinigte Randmittel der ANCOVA.
  - Ergebnisse mit `write_xlsx()` exportieren.

### Projekt

- `README.md` neu geschrieben, `NEWS.md` angelegt.
- `STUDIE.md` auf die 9-Kapitel-Fassung und die tatsächlichen Befunde gebracht. `STYLE.md` und `MIGRATION.md` beschreiben den aktuellen Stand.
- Aufgeräumt:
  - Nicht verwendete Bilder entfernt.
  - Ungenutzte Literaturdateien aus der bookdown-Vorlage entfernt (`book.bib`, `packages.bib`).
  - Leere Render-Reste und iCloud-Duplikate gelöscht.
  - Bookdown-Einträge aus `.gitignore` entfernt.

## Mai 2026 — Modernisierung

Das Buch wurde grundlegend neu aufgebaut.

- **Werkzeuge:** Statt bookdown wird Quarto verwendet, mit cosmo-Theme, eigenem SCSS-Overlay und `freeze: auto`. Den alten Funktions-Zoo ersetzt ein Zwei-Paket-Setup aus **tidyverse + mariposa**. Abgelöst wurden strengejacke, sjmisc, sjlabelled, sjPlot, descr, weights, psych, texreg, corrplot und gridExtra. Durchgängig wird die native Pipe `|>` verwendet.
- **Daten:** ALLBUS 2023 statt ALLBUS 2018. Eine Mini-Studie zu Islamfeindlichkeit und Populismus zieht sich als roter Faden durch alle Methoden-Kapitel.
- **Struktur:** Aus 6 wurden 9 Kapitel.
  - Kap. 2 zu Quarto ist neu.
  - Die frühere Datenmodifikation ist aufgeteilt in Datenimport (Kap. 4) und Datentransformation (Kap. 5).
  - Die Grafik-Grundlagen kommen jetzt vor den Methoden (Kap. 6).
  - Die multivariate Analyse ist aufgeteilt in Latente Strukturen (Kap. 8) und Erklärungsmodelle (Kap. 9).
- **Didaktik:**
  - Jeder Abschnitt folgt Frage → Code → Lesart, alle Kapitel haben denselben Aufbau (Lernziele, Übungen, „Was du jetzt weißt", Weiterführend).
  - Lösungen zum Aufklappen, eine Mini-Forschungsfrage pro Kapitel und ein Forschungsjournal begleiten die eigene Studie.
  - Inferenz wird über Simulationen und Grafiken erklärt: p-Wert, Standardfehler, Konfidenzintervall.
  - VIF und Residuen-Diagnostik werden händisch aufgebaut.
  - Die KMO-Diagnose zeigt die MSA pro Item.
  - Ein einheitliches ggplot-Theme `theme_rworkshop()` wird verwendet.
- **Verträge für die Arbeit am Buch:** `STYLE.md` (Stil und Didaktik), `MIGRATION.md` (Code-Konventionen) und `STUDIE.md` (Mini-Studie).

## 2022 — Überarbeitung

- Erläuterungstexte für die Funktionen der Datenmodifikation, unter anderem `std()`, `group_var()`, `split_var()` und `distinct()`, sowie ein Text zur Gewichtung.
- Ausführlichere Texte zur uni-, bi- und multivariaten Datenanalyse, einschließlich CFA und Reliabilitätsanalyse.
- Das Grafik-Kapitel wurde stark ausgebaut (Abschnitte 6.2–6.8).

## 2021 — Erste Fassung

- Version 1.0 (Mai 2021) als bookdown-Buch, von Anfang an über GitHub Pages veröffentlicht.
- Sechs Kapitel: RStudio, Programmiersprache R, Datenmodifikation, uni- und bivariate Datenanalyse, multivariate Datenanalyse, Grafiken erstellen.
- Beispieldaten: ALLBUS 2018.
