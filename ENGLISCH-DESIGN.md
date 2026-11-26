# Englische Fassung des R-Workshops: Design

Stand: 26.11.2026. Abgestimmt mit Yannick am 26.11.2026.

## 1 Wozu

Das Buch soll vollständig auf Englisch erscheinen, damit es ein englischsprachiges Publikum erreicht. Konkreter Anlass sind Yannicks Summer Schools in Essex und Lugano. Dort geht es um SEM, manchen Teilnehmenden fehlen aber die Grundlagen in R. Für sie ist das Buch ein Nachschlagewerk.

Daraus folgt: Englisch heißt hier nicht nur Fließtext. Auch Code, Kommentare, Achsenbeschriftungen, R-Ausgaben, Abbildungen und Bedienelemente der Seite sind englisch. Deutsche Labels wie „VOLKS-,HAUPTSCHULE“ in einer Tabelle würden diese Leser:innen ausbremsen.

## 2 Ziele, Nicht-Ziele, Anti-Ziele

Ziele

- Eine englische Fassung aller elf Seiten (Vorwort, Kap. 1–10) unter `https://rloesung.github.io/RWorkshop/en/`.
- Auf jeder Seite ein Knopf, der zur selben Seite in der anderen Sprache führt.
- Englische R-Ausgaben, weil die englischen Kapitel den englischen ALLBUS (ZA8833) einlesen.
- Beide Sprachen lassen sich wie bisher kapitelweise rendern, Freeze bleibt wirksam.

Nicht-Ziele

- Keine neuen Inhalte, auch kein zusätzliches SEM-Material für die Summer Schools. Die englische Fassung entspricht inhaltlich der deutschen.
- Keine neuen RStudio-Bildschirmfotos in diesem Schritt (siehe 5.7).
- Keine Übersetzung der Projektdokumente (`STYLE.md`, `MIGRATION.md`, `STUDIE.md`, `NEWS.md`, `BILDER*.md`). Sie bleiben deutsch.

Anti-Ziele (wäre ein Fehlschlag, auch wenn es technisch läuft)

- Die deutschen Adressen ändern sich oder deutsche Seiten gehen kaputt.
- Der englische Text klingt nach Maschinenübersetzung oder nach KI: Slogans, Pointen mit Gedankenstrich, „not X, but Y“-Figuren, Meta-Sätze über das Material. Für das Englische gelten dieselben Stilregeln wie für das Deutsche (`STYLE.md`, Rückmeldungen vom 16.11.2026).
- Zahlen in den Lesarten stimmen nicht mit den Ausgaben überein.
- Ein Kapitel ist halb deutsch, halb englisch (übersehene Labels, Kästen, Bildbeschriftungen, Alt-Texte).

## 3 Rahmenbedingungen

- Quarto 1.8.25 (in RStudio enthalten unter `/Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto`), R 4.6.2, mariposa 0.7.4.
- GitHub Pages liefert `docs/` aus `main` aus. `docs/` und `_freeze/` werden mit committet (Ablauf wie bisher: Commit auf `modernisierung-2026`, `main` vorspulen, `main` pushen).
- Die deutsche Datei im Projekt ist **ZA8831, ALLBUScompact 2023, Version 1.3.0** (2025-07-30), laut den Konstanten `za_nr`, `version` und `doi` in der Datei. `read_spss()` liest 5.246 Fälle und 579 Variablen; das Buch nennt 579. (Eine frühere Fassung dieses Dokuments nahm ZA8830 an; das deutsche Buch verweist an drei Stellen ebenfalls auf ZA8830.)
- Der englische ALLBUS ist das Gegenstück dazu: **ZA8833, „German General Social Survey – ALLBUScompact 2023“, Version 1.0.0** (2025-10-01). Geprüft am 26.11.2026: 5.246 Fälle, dieselben 579 Variablennamen wie die deutsche Datei. Die Datei liegt als `ALLBUS2023_en.sav` im Projektordner und wird nicht versioniert (`*.sav` steht in `.gitignore`).
- Die GESIS-Bedingungen verbieten die KI-Verarbeitung der Daten. Yannick hat am 26.11.2026 entschieden, dass Claude die Kapitel trotzdem rendert. Das gilt auch für ZA8833. Keine Datenzeilen bewusst in den Kontext holen; Variablennamen und Labels (Metadaten, auch im öffentlichen Codebuch) sind in Ordnung.
- Kapitel einzeln rendern. `quarto render a.qmd b.qmd` hat in diesem Projekt schon einmal Kapitel in `docs/index.html` zusammengelegt.

## 4 Ansätze

Drei Wege wurden betrachtet.

1. **Quarto-Profile (gewählt).** Die englischen Quelldateien liegen als `*.en.qmd` neben den deutschen. `_quarto-de.yml` und `_quarto-en.yml` legen Titel, Kapitelliste, Sprache und Ausgabeordner fest. Gemeinsames (Format, Theme, knitr, execute) steht in `_quarto.yml`. Vorteile: Bordmittel, keine neue Abhängigkeit; Freeze und Einzelkapitel-Rendern funktionieren in beiden Sprachen; Bilder, `R/`, Daten und Styles bleiben an einer Stelle; die Pfade im Code sind in beiden Sprachen gleich. Nachteil: Ein deutscher Komplett-Render löscht `docs/en/`. Das fängt ein Render-Skript ab.
2. **babelquarto (rOpenSci).** Gleiche Dateikonvention (`*.en.qmd`), fügt den Sprachumschalter selbst ein. Verworfen, weil es jedes Mal beide Sprachen komplett in einer Temp-Kopie rendert, `docs/` vorher löscht und `_freeze/` nicht zurückschreibt. Kap. 4–9 würden bei jedem Lauf neu gerechnet, und Einzelkapitel-Rendern geht nicht.
3. **Eigenes Quarto-Projekt in `en/`.** Verworfen, weil Bilder, `R/`-Skripte, Daten und Styles außerhalb des Projekts liegen und Pfade im sichtbaren Code (`../`) oder Symlinks nötig würden.

Mit einem Testbuch (Quarto 1.8.25) geprüft:

- Mit `output-file: 04-Datenimport.html` im Kopf der `.en.qmd` entsteht `docs/en/04-Datenimport.html`, also dieselben Dateinamen wie im Deutschen. Interne Links `[…](04-Datenimport.en.qmd)` werden zu `04-Datenimport.html`.
- Ein deutscher Komplett-Render (`quarto render`) leert `docs/` und damit auch `docs/en/`. Mit `--no-clean` bleibt `docs/en/` stehen.
- Freeze-Einträge der englischen Kapitel liegen getrennt unter `_freeze/<name>.en/`.
- `quarto render X.en.qmd --profile en` rendert nur dieses Kapitel nach `docs/en/`.
- Wer eine `.en.qmd` ohne Profil rendert (etwa mit dem Render-Knopf in RStudio), bekommt nur eine lose Vorschau `X.html` im Projektordner. `docs/` bleibt unverändert.
- `search.json` gibt es je Sprache (`docs/search.json`, `docs/en/search.json`); die Suche bleibt in ihrer Sprache.

## 5 Entscheidungen

### 5.1 Dateien und Konfiguration

- Englische Quellen: `index.en.qmd`, `01-RStudio.en.qmd` … `10-KI-Assistenten.en.qmd` neben den deutschen Dateien. Dateinamen bleiben deutsch, damit die Adressen in beiden Sprachen gleich sind (`/04-Datenimport.html` ↔ `/en/04-Datenimport.html`).
- Jede `.en.qmd` setzt `output-file: <deutscher Name>.html` im Kopf.
- `_quarto.yml`: `profile: default: de`, dazu alles, was beide Sprachen teilen. Kapitellisten stehen nur in den Profilen, weil Quarto Listen beim Zusammenführen der Konfiguration aneinanderhängt.
- `_quarto-de.yml`: `output-dir: docs`, deutscher Titel, Untertitel, Kapitelliste, `lang: de`, `toc-title`, Fußzeile, Datumsformat, Cover-Alt-Text, wie heute.
- `_quarto-en.yml`: `output-dir: docs/en`, englische Fassung derselben Angaben, `lang: en`.
- `render.sh`: rendert erst Deutsch, dann Englisch. Einzelkapitel: `quarto render X.qmd` bzw. `quarto render X.en.qmd --profile en`.
- Lose Vorschaudateien im Projektordner (`/[0-9][0-9]-*.html`, `/index.html`) kommen in `.gitignore`. `seite.html` muss versioniert bleiben.

### 5.2 Sprachumschalter

- Ein Knopf „English“ auf deutschen Seiten, „Deutsch“ auf englischen. Er führt zur selben Seite in der anderen Sprache (`/X.html` ↔ `/en/X.html`), nicht zur Startseite. Abschnittsanker werden nicht mitgenommen, weil die Überschriften-IDs je Sprache verschieden sind.
- Sichtbar auf großen Bildschirmen und auf dem Handy. Er fügt sich in das Baukasten-Design ein (Farben bleiben, siehe Rückmeldung vom 26.11.2026).
- Seiten verweisen per `<link rel="alternate" hreflang>` aufeinander.
- Der Knopf erscheint nur, wenn es die Seite in der anderen Sprache gibt. So zeigen die deutschen Seiten online keinen Knopf, solange die englische Fassung nicht veröffentlicht ist, und nicht übersetzte Kapitel haben keinen.

### 5.3 Daten und Code

- Die englischen Kapitel zeigen im Code `read_spss("ALLBUS2023.sav")`, wie die deutschen. Wer das englische Buch liest, lädt ZA8833 herunter und speichert die Datei unter diesem Namen in seinem Projektordner. Im Buchprojekt liegt die englische Datei als `ALLBUS2023_en.sav`; ein unsichtbarer Setup-Schritt nur in den englischen Kapiteln leitet `read_spss("ALLBUS2023.sav")` auf diese Datei um. So bleiben Code und Abbildungen mit dem Dateinamen in beiden Sprachen gleich.
- Eigene Variablennamen werden englisch: `islamophobie` → `islamophobia`, `populismus` → `populism`, `islamophobie_p` → `islamophobia_p`, `populismus_p` → `populism_p`, und so weiter für alle im Buch gebildeten Variablen und Objekte. ALLBUS-Variablennamen (`mm01`, `pa29`, `sex`, `age` …) und `allbus` bleiben.
- `R/prep_en.R` ist die englische Fassung von `R/prep.R`. `R/_common.R` bleibt gemeinsam.
- Kommentare im Code, Achsentitel, Legenden, Kategorien in `rec()`- und `labels = c(…)`-Aufrufen, Prompt-Vorlagen (Kap. 10) und YAML-Beispiele (Kap. 2, etwa `lang: en`) werden englisch.
- Die Lesarten zitieren die tatsächlichen englischen Labels aus ZA8833, nicht eigene Übersetzungen der deutschen Labels.

### 5.4 Prüfung der Zahlen

- Jede Zahl einer englischen Ausgabe muss der deutschen Ausgabe desselben Chunks entsprechen. Ein Prüfskript vergleicht die Zahlen der Chunk-Ausgaben aus `_freeze/<name>/` und `_freeze/<name>.en/` Chunk für Chunk und meldet Abweichungen.
- Erwartet werden keine Abweichungen, weil ZA8833 dieselben Fälle und Variablen hat wie ZA8831. Weicht doch etwas ab, das nicht aus der Übersetzung kommt (andere Fallzahl, andere Variablenzahl, andere Werte), ist das ein Haltepunkt: erst Yannick fragen, nicht anpassen.
- Bausteine-Abbildungen mit echten Datenwerten (etwa `k04-platte` mit `respid`, `age`, `mm01`) behalten in beiden Sprachen dieselben Werte; übersetzt werden nur Beschriftungen und Wertelabels.
- Ein zweites Prüfskript vergleicht den Aufbau beider Sprachen je Kapitel: Zahl der Überschriften je Ebene, Chunks, Kästen je Typ, Abbildungen, Übungen. Es dient auch später, damit Änderungen nicht nur in einer Fassung landen.

### 5.5 Seitenskript und Styles

`seite.html` und `zusatz.scss` erkennen heute deutsche Wörter. Sie sollen beide Sprachen kennen, gesteuert über `<html lang>`:

| Deutsch | Englisch |
|---|---|
| Hintergrund | Background |
| Vorsicht | Caution |
| mariposa-Tipp | mariposa tip |
| SPSS → R | SPSS → R |
| Forschungsjournal | Research journal |
| Übung · Titel · Typ | Exercise · Title · Type |
| Lösung | Solution |
| Kurz überlegen. / Auflösung | Stop and think. / Answer |
| Was du nach diesem Kapitel/Buch kannst | What you will be able to do after this chapter/book |
| Was du jetzt weißt | What you know now |
| Weiterführend | Further reading |
| zum Abhaken (CSS) | tick off |
| Ausgabe (CSS) | Output |
| aria-label „Kapitel“ | Chapters |

Die alten Kastentypen in `TYPEN` (Konzept, Reviewer-Hinweis, Tipp, Faustregel) gibt es laut `STYLE.md` nicht mehr; sie brauchen keine englische Entsprechung.

### 5.6 Abbildungen

- Die 69 Bausteine-Abbildungen bekommen englische Fassungen in `Bilder/figuren/en/`, erzeugt von denselben Skripten in `figuren/` mit einem Sprachschalter. Wertelabels in den Abbildungen stammen aus ZA8833.
- Das Titelbild bekommt eine englische Fassung (`figuren/cover.py`).
- Bildunterschriften und `fig-alt`-Texte werden übersetzt.

### 5.7 Bildschirmfotos

Die elf RStudio-Bildschirmfotos (`Bilder/rstudio/`) werden übernommen. Die Oberfläche von RStudio ist englisch; deutsch sind nur Beispielnamen wie `01-erste_schritte.qmd`. Neue Fotos sind ein späterer Schritt.

### 5.8 Sprache und Stil

- Britisches Englisch im Fließtext (Essex), Du-Form als *you*. Code folgt den Paketen.
- Feste Begriffe: **Question:** und **Interpretation.** als Marken (für **Frage:** und **Lesart.**), *mini study*, *research journal*, *exercise*, *solution*, *mini research question*, ALLBUS beim ersten Auftreten als „German General Social Survey (ALLBUS)“.
- Der Inhalt wird übertragen, nicht umgeschrieben. Wo das Deutsche ein deutsches Publikum voraussetzt (SPSS-Gewohnheiten an deutschen Unis, deutsche Studiengänge, Datum- und Zahlenformate), passt die englische Fassung das an.
- Zahlenformat im Text wie in den Ausgaben (Dezimalpunkt).

### 5.9 Pflege

- Die deutsche Fassung bleibt die Quelle. Wer ein deutsches Kapitel ändert, ändert die englische Fassung im selben Commit mit; das Aufbau-Prüfskript zeigt Abweichungen.
- README bekommt einen englischen Abschnitt (Lesen, ZA8833 herunterladen, Rendern). NEWS bekommt einen Eintrag.
- Veröffentlicht wird die englische Fassung erst, wenn alle elf Seiten übersetzt und geprüft sind. Bis dahin steht `/docs/en/` in `.gitignore`.

### 5.10 Ablauf mit Pilot

1. Gerüst: Profile, Render-Skript, Umschalter, zweisprachiges Seitenskript und Styles, Prüfskripte.
2. Pilot: Vorwort und Kap. 4 auf Englisch, mit englischen Abbildungen und gerendert gegen ZA8833. Kap. 4 enthält Daten, Abbildungen, alle Kastentypen und Übungen.
3. Yannick liest den Pilot und korrigiert Ton und Begriffe. Die Korrekturen kommen als englische Stilregeln in `STYLE.md` (eigener Abschnitt) und gelten für alle weiteren Kapitel.
4. Erst danach die übrigen neun Seiten.

## 6 Was dem Umsetzenden überlassen bleibt

- Wie der Umschalter genau aussieht und wo er sitzt, solange 5.2 erfüllt ist.
- Wie die Umleitung auf `ALLBUS2023_en.sav` technisch gebaut ist (etwa eine Hülle um `read_spss()` in einem versteckten Chunk oder per Option), solange der sichtbare Code `read_spss("ALLBUS2023.sav")` zeigt.
- Wie der Sprachschalter in `figuren/` gebaut ist.
- Reihenfolge der Kapitel beim Übersetzen und wie die Arbeit auf Durchgänge verteilt wird.
- Englische Titel der Kapitel und Abschnitte.

## 7 Offene Punkte

- Sobald `ALLBUS2023_en.sav` vorliegt: prüfen, dass Fallzahl, Variablennamen und Wertecodes mit der deutschen Datei übereinstimmen (nur Kopf und Metadaten lesen). Weichen sie ab, betrifft das 5.3 und 5.4 und muss mit Yannick neu entschieden werden.
