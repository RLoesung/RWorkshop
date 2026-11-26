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
- ZA8833 erklärt keine Codes zu fehlenden Werten; ZA8831 erklärt alle negativen Codes dazu. Die Rohwerte sind in beiden Dateien identisch. Entscheidung Yannick (26.11.2026): Die englischen Kapitel deklarieren die fehlenden Werte sichtbar beim Einlesen:

  ```r
  allbus <- read_spss("ALLBUS2023.sav") |>
    set_na(-56, -55, -54, -53, -51, -50, -42, -41,
           -33, -32, -15, -11, -10, -9, -8, -7, -6)
  ```

  Das sind alle negativen Codes mit Label in ZA8833. Geprüft: Danach haben 575 von 577 numerischen Variablen dasselbe Muster fehlender Werte und dieselben gültigen Werte wie im deutschen Buch. Ausnahmen sind `za_nr` (Studiennummer) und `splt23_2`, bei dem -15 im Deutschen gültig ist; beide erscheinen in Kap. 4 im ersten Tibble-Ausdruck (`read-show`): Die englische Ausgabe zeigt dort `za_nr` 8833, `version` 1.0.0 und `splt23_2` als NA(k) [NAP: MODE] statt -15. Das ist so akzeptiert, es folgt aus dem `set_na()`-Schritt; Hinweis an den Autor. Die Kennbuchstaben der Missing-Typen weichen ab, weil `set_na()` sie über alle Codes vergibt (bei `mm01` g, l, n, o statt a, b, c, d). Englische Texte und Abbildungen nennen die Buchstaben aus der englischen Ausgabe. Kap. 4 erklärt den Schritt beim Einlesen in zwei Sätzen. Entscheidung Yannick (26.11.2026): Der Schritt steht in allen englischen Kapiteln sichtbar im Code, überall dort, wo der ALLBUS eingelesen wird, auch in Setup-Beispielen (Kap. 2), Übungen und Prompt-Vorlagen (Kap. 10) und in `R/prep_en.R`. Abbildungen, die das Einlesen zeigen, nehmen ihn ebenfalls auf, bei Platzmangel gekürzt (etwa `|> set_na(-56, …, -6)`).

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

- Erledigt (26.11.2026): ZA8833 hat dieselben Fälle, Variablennamen und Rohwerte wie ZA8831; Unterschied sind nur die fehlenden Missing-Deklarationen (siehe 5.3) und sechs zusätzliche Wertelabels bei `isco08a`.

## 8 Nach dem Pilot (Stand 26.11.2026)

Der Pilot (Vorwort, Kap. 4) ist fertig und geprüft. Die Gesamtprüfung hat Punkte ergeben, die vor den übrigen neun Seiten erledigt sein müssen. Sie sind die erste Aufgabe des nächsten Plans, zusammen mit Yannicks Rückmeldungen zum Pilot.

1. **`set_na()` überall (entschieden 26.11.2026, siehe 5.3):** Englischen Code und Abbildungen anpassen in Kap. 2 (Setup-Beispiele, `02-Quarto.qmd` um Zeile 243–270), Kap. 3 (`real-pipe`, um Zeile 534), Kap. 5 (versteckter Setup und `full-pipeline`, um Zeile 7 und 755), Kap. 10 (Übung um Zeile 243; die Prompt-Regel um Zeile 124 „Fehlende Werte sind beim Einlesen … schon als NA deklariert“ muss für ZA8833 lauten, dass sie mit `set_na()` deklariert werden), dazu die Abbildungen `k02-render-sitzung`, `k03-analyseplan`, `k05-pipeline` und im Pilot `k04-einlesen`.
2. **Prüfskript `figuren/check_en.py` erweitern:** deutsche Wörter und Umlaute auch in Code-Kommentaren, Zeichenketten und `#|`-Optionen; deutsche ALLBUS-Labels und Umlaute in den englischen Ausgaben (Freeze); jede `.en.qmd` lädt `R/_common_en.R`; Abbildungspfade zeigen nach `Bilder/figuren/en/`; `output-file` gesetzt. `ohne_code` muss Zäune mit vier Backticks richtig behandeln (Kap. 1, 2).
3. **Erwartete Abweichungen:** eine Liste je Kapitel, damit ein sauberer Lauf „0 Meldungen“ heißt; je Meldung die erste Codezeile der Zelle nennen; nach unterschiedlicher Blockzahl nicht weiter paarweise vergleichen. Bekannt für Kap. 4: Block 1 (`za_nr`, `version`, `splt23_2`), Blöcke 3 und 5 (`find_var()` mit englischen Labels), Block 27 (gleiche Zahlen, andere Reihenfolge).
4. **`STYLE.md` §13 ergänzen:** verbindliche Tabelle deutscher → englischer Namen für alle im Buch gebildeten Variablen und Objekte (schon festgelegt: `islam_hoch` → `islamophobia_high`; offen u. a. `educ_kat` mit niedrig/mittel/hoch, `geschlecht`, `region`, `geburtsjahr`, `modell`, `m_voll`, `m_basis`, `kontext_bl`); Checkliste je Kapitel (Setup mit `R/_common_en.R`, `set_na()`, Abbildungspfade, Kapitelliste in `_quarto-en.yml`, `t()` und `build.py --en`, Einzel-Render, `check_en.py`, `Rscript R/test_common_en.R`). `BILDER.md` um `--en` ergänzen.
5. **Kleineres:** `build.py --en` nur für Module, die `t()` nutzen, und den Test auf deutsche Reste für alle englischen SVGs; `R/_common_en.R` per `basename()` umleiten; `R/pruefe_daten_en.R` vergleicht auch Missing-Deklarationen und endet bei Abweichung mit Fehlercode.
6. **Vor der Veröffentlichung:** README auf `./render.sh` umstellen (ein schlichtes `quarto render` löscht `docs/en/`) und vor jedem Commit prüfen, dass unter `docs/en` nichts gelöscht wird; README-Abschnitt auf Englisch; NEWS-Eintrag; `/docs/en/` aus `.gitignore` nehmen.
7. **Deutsches Buch (vereinbart):** Verweise auf ZA8830/ZA8901 durch ZA8831 ersetzen (`index.qmd`, `04-Datenimport.qmd`, `10-KI-Assistenten.qmd`, README, `STUDIE.md`, `.gitignore`); bei „R for Data Science“ (2. Aufl.) fehlt Mine Çetinkaya-Rundel. Dieselbe Autorenliste in `index.en.qmd` und `04-Datenimport.en.qmd` im selben Commit korrigieren.
