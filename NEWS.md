# Änderungsprotokoll

Neueste Änderungen stehen oben. Die Online-Fassung unter <https://rloesung.github.io/RWorkshop/> entspricht immer dem Stand von `main`.

## 26. November 2026 — Korrekturen und englische Fassung vorbereitet

- Die Studiennummer des ALLBUS 2023 ist ZA8831, nicht ZA8830 und nicht ZA8901. Die Literaturangaben zu *R for Data Science* nennen jetzt auch Mine Çetinkaya-Rundel als Autorin (auch in Kap. 5).
- Kap. 2: Die Chunk-Option für Bildunterschriften heißt `fig.cap` (im `#|`-Stil `fig-cap`); die Beispiele mit Inline-R-Code im Quelltext werden als Text gezeigt und nicht ausgewertet; in der Übung steht der Dateiname ohne Formatierung im Titel.
- Kap. 7, 8, 9: Kleine Korrekturen an Abbildungen und Tabellen, etwa Achsenränder, ein zentrierter Titel, Beschriftungen mit Zeilenumbruch und die Tabelle der Ladungen in Kap. 8. In Kap. 8 stand in der Legende „verfehlt“ bei erfüllten Schwellen; jetzt stimmt die Beschriftung. In Kap. 9 nennt der Text die Spalte `B` statt `Estimate`, die Lesart nennt für hohe Bildung OR = 0,33 statt 0,34, und der Titel der Koeffizientengrafik steht vollständig im Bild. Die R-Ausgaben sind unverändert.
- Eine englische Fassung des Buchs ist vorbereitet, aber noch nicht veröffentlicht. `./render.sh` baut beide Sprachen; die englischen Seiten entstehen lokal unter `docs/en/`. Die Kapitelkarten im englischen Vorwort erzeugt `python3 figuren/kapitelkarten.py --en`, und `figuren/pruefe_kaesten.py` prüft jetzt auch englische Kapitel.

## 26. November 2026 — Neues Kap. 10: Mit KI-Assistenten arbeiten

- Neues Kapitel 10 über das Arbeiten mit KI-Assistenten, unabhängig von einem bestimmten Programm: warum Assistenten bei mariposa Funktionen erfinden, welchen Kontext eine Anfrage braucht (Versionen, die `llms.txt` von mariposa, Variablen, Fehlermeldung), eine Vorlage für Anfragen mit den Regeln des Buchs, wie man Antworten prüft und wie man Probleme mit erfundenen Beispieldaten nachstellt. Dazu vier Übungen.
- Das Kapitel erklärt, dass die Datennutzungsbedingungen von GESIS (gültig ab 4. Februar 2026) die Verarbeitung von ALLBUS-Daten mit KI-Systemen verbieten, und was man einem Assistenten deshalb zeigen darf. Es rechnet selbst nur mit erfundenen Beispieldaten.
- Das Vorwort nennt Kap. 10 in der Roadmap, in den Kapitelkarten und in der Liste der Etappen. Die Kapitelkarten zeigen die Lernziele jetzt ohne Fettdruck, wie in den Kapiteln.
- Korrigiert: Die Studiennummer des ALLBUS 2023 ist ZA8830. Vorwort, Kap. 4 und README verwiesen auf ZA8901, ein Flash Eurobarometer.

## 26. November 2026 — Weniger Kästen, weniger Fettdruck

- Das Buch hat weniger Kästen: statt 144 noch 92. Es gibt vier Arten (Hintergrund, Vorsicht, SPSS → R, mariposa-Tipp) und das Forschungsjournal am Kapitelanfang und -ende. Vorsicht und SPSS → R stehen offen; Hintergrund und mariposa-Tipp sind zugeklappt und zeigen nur eine farbige Zeile, die sich mit einem Klick öffnet. Zwei Kästen stehen nie mehr direkt untereinander.
- Was zum Verständnis eines Kapitels nötig ist, steht jetzt im Fließtext, etwa die latente Variable in Kap. 8 oder Wahrscheinlichkeit, Odds und Logit in Kap. 9. Kästen, die nur den Text davor wiederholten, sind weggefallen.
- Fett sind nur noch Fachbegriffe an der Stelle, wo sie eingeführt werden, die Marken „Frage“ und „Lesart“ und die Einstiege der offenen Kästen: statt 840 noch 265 Stellen.
- Dabei korrigiert: In Kap. 4 wird die Tabelle mit SPSS- und R-Befehlen zur Dateninspektion wieder als Tabelle gesetzt; in Kap. 3 zeigt der Kasten zu typografischen Anführungszeichen jetzt die richtigen Zeichen.
- Die Regeln stehen in `STYLE.md` § 4, `figuren/pruefe_kaesten.py` prüft sie. Alle R-Ausgaben sind unverändert.

## 17. November 2026 — Neues Aussehen: Design „Baukasten“

- Das Buch hat ein neues Aussehen in Pastelltönen mit runden Schriften (Fredoka für Überschriften, Nunito für den Text). Jedes Kapitel hat eine eigene Steinfarbe, oben auf jeder Kapitelseite steht eine Leiste mit einem Stein je Kapitel, und ein schmaler Balken zeigt, wie weit du im Kapitel bist.
- Die Kästen sind nach ihrer Art gesetzt (Hintergrund, SPSS → R, mariposa-Tipp, Vorsicht, Tipp, Forschungsjournal und weitere), jeweils mit einer kleinen Begleitfigur aus einem Baustein. Übungen, Lösungen und „Kurz überlegen“ stehen auf eigenen Karten. Die Punkte unter „Was du jetzt weißt“ lassen sich abhaken; das merkt sich nur der eigene Browser.
- Das Vorwort beginnt mit einem Satz nach John Chambers über Objekte und Funktionsaufrufe, die Forschungsfrage steht jetzt im ersten Absatz. Darunter zeigt es alle Kapitel als Karten mit je zwei Lernzielen. Das Buch hat ein Cover.
- Auf breiten Bildschirmen stehen Text und Inhaltsverzeichnis mittig im Platz neben der Kapitelleiste; vorher blieb rechts ein breiter leerer Streifen.
- Die Schriften kommen von Google Fonts. Die Begleitfiguren erzeugt `figuren/begleiter.py`, die Kapitelkarten `figuren/kapitelkarten.py`; das Aussehen der Kästen steuert `seite.html` (`STYLE.md` §4).

## 17. November 2026 — Kap. 1 mit Quarto-Dokumenten, neue Bildschirmfotos

- Kap. 1 arbeitet von Anfang an mit einem Quarto-Dokument statt mit einem R-Skript, so wie der Workshop. Der Abschnitt „Quarto-Dokument“ ersetzt den Abschnitt „R-Skript“: Das erste Beispiel steht in einem Chunk in `01-erste_schritte.qmd`, ein Absatz sagt, was in die Konsole und was ins Dokument gehört, und ein Satz erklärt, was ein R-Skript ist. Lernziel, Tastenkürzel, Checkliste, Übung 2 und Zusammenfassung sind angepasst, ebenso der Abschnitt „Dein erstes `.qmd`“ in Kap. 2 und zwei Sätze im Vorwort.
- Am Anfang von 1.4 zeigt eine neue Abbildung die vier Bereiche von RStudio mit grünen Nummern. Sie ersetzt das alte Bildschirmfoto der ganzen Oberfläche.
- Elf neue Bildschirmfotos aus RStudio 2026.01 mit R 4.6.2 im hellen Theme ersetzen die alten dunklen: Optionen, Konsole, Environment, Files, Projekt, Editor mit Chunk, drei Bilder zur Tab Completion, Packages und Help. Alle haben denselben Maßstab, einen dünnen Rahmen und oben rechts die Nummer des Bereichs. Die Tab Completion zeigt jetzt die mariposa-Funktionen von heute (`w_mean()` statt `weighted_mean()`).

## 17. November 2026 — Beispiele für Tidyselect-Helfer in Kap. 4

- In der Tabelle der Tidyselect-Helfer in Kap. 4 fand `select(contains("vertrau"))` keine Spalte, und `select(ends_with("r"))` fand nur `za_nr`, weil die umgepolten Items erst in Kap. 5 entstehen. Die Tabelle zeigt jetzt `select(ends_with("educ"))` (Schulabschluss von Befragten, Partner:in und Eltern) und `select(contains("wght"))` (die vier Gewichtungsvariablen).

## 17. November 2026 — `rec()` innerhalb von `mutate()`

- `rec()` steht im ganzen Buch jetzt innerhalb von `mutate()`, etwa `mutate(mm02r = rec(mm02, rules = "rev"))`. Der neue Name links vom `=` ersetzt das Argument `suffix`; mehrere Variablen stehen in einem `mutate()` mit einer Zeile je Variable. Das betrifft Kap. 3, 5, 6, 7 und 9, `R/prep.R` und fünf Abbildungen; die Ergebnisse im Buch bleiben gleich.

## 17. November 2026 — Abbildungen mit Bausteinen: Erweiterung auf alle Kapitel

- 31 weitere Abbildungen in derselben Bildsprache, jetzt in allen Kapiteln: Kap. 1 (2), Kap. 2 (3), Kap. 3 (5), Kap. 4 (2), Kap. 5 (6), Kap. 6 (4), Kap. 7 (1), Kap. 8 (3) und Kap. 9 (5). Zusammen hat das Buch 68 Bausteine-Abbildungen.
- Neue Bildelemente: eine Kiste mit Fächern für Listen und Ergebnisobjekte, blasse Steine für Werte, die R wiederholt, ein Schild für die Referenzkategorie eines Faktors, Folien für die Ebenen einer ggplot-Grafik und eine gestrichelte Ellipse für einen nicht gemessenen Faktor. `BILDER.md` §5.2 listet alle Elemente.
- Fünf neue Denkpausen „Kurz überlegen“ in 2.6.1, 3.5.2, 4.5.2, 6.3.2 und 9.3.1, zusammen sind es 14.
- Außerdem liegt `ALLBUS2023.sav` in 2.11 direkt im Projektordner, ohne Unterordner `data/`; 3.7.2 sagt, dass nur der Punkt hinter `data =` der Platzhalter ist; in 6.3.2 passen die Farbe der Balken bei einer Konstante in `aes()` und ein Kommentar im Chunk jetzt zur Ausgabe; 2.9 beschreibt, wo Quarto in HTML die Literaturliste einfügt.

## 17. November 2026 — Abbildungen mit Bausteinen

- 37 neue Abbildungen erklären Grundbegriffe von R mit Bausteinen: Ein Wert ist ein Stein, seine Farbe der Datentyp, ein Vektor ein Turm, ein Datensatz eine Bauplatte mit Türmen, ein Wertelabel ein Aufkleber. Die Bildsprache stammt aus dem Workshop „Reading Week“ vom November 2026 und wird am Anfang von Abschnitt 3.5 erklärt. Die Abbildungen stehen in Kap. 1 (2), Kap. 2 (1), Kap. 3 (11), Kap. 4 (10), Kap. 5 (11) und Kap. 7 (2).
- Neues Format „Kurz überlegen“: An neun Stellen stellt das Buch eine Frage zu einem neuen Fall, die Auflösung steht eingeklappt darunter. Das Format ist in `STYLE.md` §4 beschrieben.
- Die Abbildungen liegen als SVG-Dateien in `Bilder/figuren/`. Gebaut werden sie mit den Skripten im Ordner `figuren/`; `python3 figuren/build.py` erzeugt alle neu. Zum Rendern des Buchs braucht man Python nicht. Was in die Bilder gehört und wie sie aussehen, regelt `BILDER.md`.
- Außerdem nennen Vorwort und Kap. 1 das tidyverse jetzt ein Ökosystem und mariposa ein Paket. In Kap. 4 erscheint die Meldung von `set_na(verbose = TRUE)` jetzt im Buch.

## 17. November 2026 — Tastenkürzel im Vorwort, Funktionsnamen in den Überschriften

- Das Vorwort endet mit einer Tabelle der wichtigsten Tastenkürzel, getrennt nach macOS und Windows und abgestimmt auf die Arbeit mit Quarto-Dokumenten (Chunk einfügen, Chunk ausführen, Rendern). Sie verlinkt auf den Abschnitt „Nützliche Tastenbefehle" in Kap. 1.
- Die Überschriften nennen wieder die Funktionen, die ein Abschnitt erklärt, zum Beispiel „Datensatz einlesen mit `read_spss()`“ oder „Fehlende Werte deklarieren mit `na_frequencies()`, `set_na()` und `drop_na()`“. So lässt sich das Buch über das Inhaltsverzeichnis und die Suche wieder als Nachschlagewerk nutzen. Wo ein Abschnitt viele Funktionen erklärt, gibt es neue Unterabschnitte (etwa 3.4.1–3.4.3 zu den Operatoren); bestehende Abschnittsnummern bleiben gleich.

## 15. November 2026 — Texte an die Ausgabe angeglichen

Beim Abgleich mit R 4.5.3 und mariposa 0.7.4 sind Stellen aufgefallen, an denen der Text nicht mehr zur Ausgabe passte.

### Behoben

- **Kap. 4:**
  - `allbus$sex |> head(5)` wird jetzt ausgeführt statt mit einer veralteten Ausgabe im Kommentar gezeigt.
  - Der ALLBUS 2023 hat 17 Missing-Codes, das Buch sprach von vier. Die Tabelle zeigt jetzt die vier Codes der `mm`-Items, weitere Codes werden genannt.
  - Die `relocate()`-Beispiele laufen jetzt in Kap. 4: Die Skalen gibt es dort noch nicht, und die ID-Variable heißt `respid`.
- **Kap. 5:**
  - `rec()`: Tagged NAs behalten ihren Missing-Typ nur, wenn keine `else=`- oder `NA=`-Regel sie erfasst. Mit `else=NA` werden sie zu einfachen `NA`.
  - `row_means()` bildet eine ungewichtete Mittelwert-Skala; „gewichtet" ist aus Lernziel und Rückblick gestrichen.
  - „Vier Verben" passte nicht zur Tabelle mit sieben Funktionen.
- **Kap. 7:**
  - Die Subgruppen-Tabelle (und Lösung 2) zählt mit `n = sum(!is.na(islamophobie))` nur Befragte mit Skalenwert, nicht mehr alle Befragten der Gruppe.
  - Die Chunks der Übungslösungen heißen jetzt `ex*-kap7-loesung`.

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

- Der ALLBUS-Datensatz liegt nicht mehr im Repository. Wer das Buch selbst rendert, lädt `ALLBUS2023.sav` bei GESIS herunter (ZA8901). `.gitignore` schließt `.sav`- und `.dta`-Dateien künftig aus.
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
