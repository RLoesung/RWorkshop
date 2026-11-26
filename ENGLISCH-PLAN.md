# Englische Fassung, Gerüst und Pilot: Umsetzungsplan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Das Buch bekommt eine zweite Sprachfassung unter `docs/en/` mit Sprachumschalter; als Pilot sind Vorwort und Kap. 4 vollständig englisch.

**Architecture:** Quarto-Profile (`_quarto-de.yml`, `_quarto-en.yml`) über einer gemeinsamen `_quarto.yml`. Englische Quellen liegen als `*.en.qmd` neben den deutschen und schreiben per `output-file` dieselben Dateinamen nach `docs/en/`. `seite.html` und `zusatz.scss` werden zweisprachig über `<html lang>`, die Abbildungsskripte bekommen einen Sprachschalter, ein Prüfskript vergleicht beide Fassungen.

**Tech Stack:** Quarto 1.8.25, R 4.6.2, mariposa 0.7.4, Python 3 (unittest), Vanilla-JS in `seite.html`, SCSS.

**Spec:** `ENGLISCH-DESIGN.md`

## Global Constraints

- Quarto: `quarto` aus dem PATH, sonst `/Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto`.
- Deutsche Adressen und deutsche Seiten bleiben unverändert (Design §2, Anti-Ziele).
- Kapitel einzeln rendern; nie mehrere Dateien in einem `quarto render`-Aufruf.
- Englische Dateien behalten alle IDs der deutschen: `{#sec-…}`, `{#fig-…}`, Chunk-Labels. Querverweise müssen in beiden Sprachen auflösen.
- Englische Dateien setzen `output-file: <deutscher Dateiname>.html`.
- Kapitellisten stehen nur in den Profilen, nie in `_quarto.yml` (Quarto hängt Listen beim Zusammenführen aneinander).
- `docs/en/` bleibt bis zur Veröffentlichung in `.gitignore` (Design §5.9). Deutsche `docs/` und `_freeze/` werden wie bisher mit committet.
- Commits auf `modernisierung-2026`, Nachrichten im Stil „Englische Fassung: …“. Nichts pushen.
- Daten: keine ALLBUS-Datenzeilen in Ausgaben von Skripten oder Tests. Kopf, Variablennamen und Labels sind erlaubt. Tests arbeiten mit erfundenen Daten.
- Text: britisches Englisch, *you*, schlicht; keine Slogans, keine Pointen mit Gedankenstrich, keine „not X, but Y“-Figuren, keine Meta-Sätze über das Material (Design §5.8, `STYLE.md`). Wer übersetzt (auch ein Subagent), bekommt diese Regeln und `STYLE.md` §12 ausdrücklich mit.
- Noch nicht übersetzte Kapitel stehen im englischen Profil mit ihrer deutschen `.qmd` in der Kapitelliste, damit die Nummerierung stimmt. Jede übersetzte Datei ersetzt dort ihre deutsche.

## Review Focus

1. Jemand rendert das deutsche Buch mit `quarto render` statt `./render.sh`: `docs/en/` ist danach weg. Erwartung: `./render.sh` stellt beides wieder her; README-Hinweis folgt mit der Veröffentlichung. Task 1 prüft, dass nach `./render.sh` beide Fassungen da sind.
2. Umschalter auf einer Seite ohne Gegenstück (deutsches Kapitel, das noch nicht übersetzt ist, oder live vor der Veröffentlichung): Es darf kein Knopf erscheinen, der ins Leere führt. Task 2 prüft das an einer deutschen Seite ohne englische Fassung.
3. Das Buch liegt online unter `/RWorkshop/`, lokal unter `/`: Die Zuordnung `X.html` ↔ `en/X.html` muss unter beiden Pfaden stimmen. Task 2 prüft mit einem lokalen Server, der `docs/` unter `/RWorkshop/` ausliefert.
4. Eine `.en.qmd` wird mit dem Render-Knopf in RStudio (ohne Profil) gerendert: Es entsteht eine lose `X.html` im Projektordner. Erwartung: Git sieht sie nicht. Task 1 prüft das.
5. Schmaler Bildschirm: Der Umschalter muss ohne aufgeklappte Seitenleiste erreichbar sein. Task 2 prüft bei 375 px Breite.

---

### Task 1: Profile und Render-Skript

**Files:**
- Modify: `_quarto.yml`
- Create: `_quarto-de.yml`, `_quarto-en.yml`, `index.en.qmd` (Platzhalter), `render.sh`
- Modify: `.gitignore`

**Interfaces:**
- Produces: `quarto render --profile en` baut nach `docs/en/`; `./render.sh` baut beide Sprachen; Profilname `en`.

- [ ] **Step 1: Ist-Stand festhalten.** `git status --short docs _freeze` ist leer (sonst erst klären).
- [ ] **Step 2: `_quarto.yml` aufteilen.** In `_quarto.yml` bleiben: `project.type: book`, `profile: default: de`, `book.author`, `book.date: today`, `search`, `reader-mode`, `repo-url`, `repo-actions`, `sidebar`, der ganze `format`-Block außer `toc-title`, `execute`, `knitr`. In `_quarto-de.yml` wandern unverändert: `project.output-dir: docs`, `book.title`, `subtitle`, `date-format`, `language`, `cover-image`, `cover-image-alt`, `page-footer`, `chapters`, `format.html.toc-title`, `lang: de`.
- [ ] **Step 3: `_quarto-en.yml` anlegen** mit `project.output-dir: docs/en`, `lang: en`, `book.language: en`, `title: "R Workshop – Social Sciences"`, `subtitle: "An introduction to statistical data analysis with tidyverse and mariposa"`, `date-format: "D MMMM YYYY"`, `page-footer` (left: „R Workshop – Social Sciences · Yannick Diehl and Daniel Moosdorf“, right: „Built with [Quarto](https://quarto.org/)“), `format.html.toc-title: "On this page"`, Cover wie Deutsch (Task 5 tauscht es), englischer Cover-Alt-Text, `chapters`: `{href: index.en.qmd, text: "0  Preface"}`, danach `01-RStudio.qmd` … `10-KI-Assistenten.qmd` (deutsch, siehe Global Constraints).
- [ ] **Step 4: `index.en.qmd` als Platzhalter**: Kopf mit `output-file: index.html`, darunter `# Preface {.unnumbered}` und ein Satz. Task 7 ersetzt den Inhalt.
- [ ] **Step 5: `render.sh`** (ausführbar): findet `quarto` wie in Global Constraints, ruft `quarto render` und danach `quarto render --profile en` auf, bricht bei Fehler ab (`set -e`). Kommentar oben: Einzelkapitel mit `quarto render X.qmd` bzw. `quarto render X.en.qmd --profile en`.
- [ ] **Step 6: `.gitignore` ergänzen**: `/docs/en/` (mit Kommentar „bis zur Veröffentlichung“), `/[0-9][0-9]-*.html`, `/index.html`.
- [ ] **Step 7: Prüfen, dass Deutsch unverändert ist.** Run: `./render.sh`. Dann `git diff --word-diff=porcelain -- 'docs/*.html' | grep -E '^[-+][^-+]'`. Expected: höchstens die Datumszeile. `python3 figuren/check_sections.py` ohne Meldung. `ls docs/en/index.html docs/en/04-Datenimport.html` existieren.
- [ ] **Step 8: Lose Vorschau prüfen.** Run: `quarto render index.en.qmd` (ohne Profil), dann `git status --short`. Expected: keine neue Datei sichtbar; `docs/index.html` unverändert. Lose Datei löschen.
- [ ] **Step 9: Commit** `_quarto*.yml`, `index.en.qmd`, `render.sh`, `.gitignore`, `docs/`, `_freeze/`: „Englische Fassung: Quarto-Profile und Render-Skript“.

### Task 2: Umschalter und zweisprachiges Seitenskript

**Files:**
- Modify: `seite.html`, `zusatz.scss`
- Create: `.claude/launch.json` (Eintrag `buch-unterpfad`, nur lokal)

**Interfaces:**
- Consumes: `<html lang>` aus den Profilen (Task 1).
- Produces: Knopf mit Klasse `sprachwahl` (Link mit `hreflang`, `lang`), `<link rel="alternate" hreflang>` im Kopf; Wörterbuch `WORT[lang]` in `seite.html` mit den Schlüsseln aus Design §5.5.

- [ ] **Step 1: Wörterbuch einführen.** In `seite.html` ein Objekt `WORT = {de: {…}, en: {…}}`, ausgewählt über `document.documentElement.lang` (Fallback `de`). Alle deutschen Wörter des Skripts laufen darüber: `TYPEN`-Wörter (nur Hintergrund, Vorsicht, mariposa-Tipp, SPSS → R, Forschungsjournal), `Übung`, `Lösung`, `Kurz überlegen.`, `Auflösung`, die drei Karten-Überschriften, `aria-label`. Englische Werte exakt aus Design §5.5.
- [ ] **Step 2: SCSS.** In `zusatz.scss` für `html[lang="en"]`: `section.selbstcheck > h2::after { content: "tick off"; }` und `.code-copy-outer-scaffold + .cell-output::before { content: "Output"; }`.
- [ ] **Step 3: Umschalter.** `gegenstueck(pfad, lang) -> string`: Englisch → letztes `/en/` durch `/` ersetzen; Deutsch → `en/` hinter dem letzten `/` einfügen. Der Knopf („English“ auf deutschen, „Deutsch“ auf englischen Seiten) und `<link rel="alternate">` werden erst eingefügt, wenn `fetch(ziel, {method: "HEAD"})` mit `ok` antwortet. Platz und Aussehen nach Design §5.2 und §6; Baukasten-Farben.
- [ ] **Step 4: Rendern.** `./render.sh`.
- [ ] **Step 5: Im Browser prüfen.** `.claude/launch.json`-Eintrag, der einen statischen Server so startet, dass `docs/` unter `/RWorkshop/` liegt (z. B. Temp-Ordner mit Symlink `RWorkshop → docs`, `python3 -m http.server`). Prüfen:
  - `/RWorkshop/index.html`: Knopf „English“ → `/RWorkshop/en/index.html`; dort Knopf „Deutsch“ → zurück.
  - `/RWorkshop/04-Datenimport.html`: deutsche Kästen sehen aus wie vorher (Etiketten „Hintergrund“, „Vorsicht“, Übungen, Lösungen, „Ausgabe“, „zum Abhaken“).
  - Englische Seite eines noch deutschen Kapitels hat ein Gegenstück, also Knopf da. Danach `docs/en/04-Datenimport.html` testweise umbenennen: auf `/RWorkshop/04-Datenimport.html` erscheint kein Knopf. Wieder zurückbenennen.
  - Bei 375 px Breite ist der Knopf ohne Aufklappen der Seitenleiste erreichbar.
  - Konsole ohne Fehler.
- [ ] **Step 6: Commit** `seite.html`, `zusatz.scss`, `docs/`, `_freeze/`: „Englische Fassung: Sprachumschalter, Seitenskript zweisprachig“. `.claude/` nicht committen.

### Task 3: Prüfskript für beide Fassungen

**Files:**
- Create: `figuren/check_en.py`, `figuren/test_check_en.py`

**Interfaces:**
- Produces:
  - `aufbau(qmd: str) -> dict[str, object]`: Anzahl Überschriften je Ebene (`h1`–`h4`, ohne Zeilen in Code-Blöcken), Anzahl R-Chunks, Kästen je Klasse (`callout-note`, `-tip`, `-important`, `-warning`, `-caution`), Abbildungen (`![`), Kästen mit `title=`, und die Menge aller IDs `{#…}` und Chunk-Labels.
  - `vergleiche_aufbau(de: dict, en: dict) -> list[str]`: eine Meldung je Unterschied.
  - `ausgabe_zahlen(freeze_json: str) -> list[list[str]]`: je Ausgabeblock (`.cell-output`) im `result.markdown` der Freeze-Datei die Zahlen (`-?\d[\d.,]*`) in Reihenfolge.
  - `vergleiche_zahlen(de: list, en: list) -> list[str]`.
  - `deutsch_reste(qmd: str) -> list[str]`: Zeilen außerhalb von Code-Blöcken, Inline-Code und URLs mit ä/ö/ü/ß oder den Wörtern „und“, „der“, „die“, „das“, „nicht“, „mit“, „ist“ als ganze Wörter; mit Zeilennummer.
  - CLI `python3 figuren/check_en.py [NAME …]`: für jede `X.en.qmd` (oder die genannten) alle Prüfungen gegen `X.qmd` und `_freeze/X/execute-results/html.json` ↔ `_freeze/X.en/execute-results/html.json` (Zahlen nur, wenn beide da sind). Exit 1 bei Meldungen.

- [ ] **Step 1: Tests schreiben** in `test_check_en.py` mit kleinen Text-Fixtures:
  - `test_aufbau_zaehlt_ueberschriften_ohne_code`: `## A` im Text zählt, `## B` in einem ```` ``` ````-Block nicht.
  - `test_aufbau_ids`: `## X {#sec-x}` und ```` ```{r foo} ```` ergeben `{"sec-x", "foo"}`.
  - `test_vergleich_meldet_fehlenden_kasten`: de mit zwei `callout-note`, en mit einem → eine Meldung, die `callout-note` nennt.
  - `test_zahlen_gleich_trotz_labels`: Ausgabe `MANN 2574 49.1` vs. `MALE 2574 49.1` → keine Meldung; `49.2` statt `49.1` → eine Meldung.
  - `test_deutsch_reste`: „The data und the code“ → gemeldet; „`und`“ in Inline-Code und „Universität“ in einer URL → nicht gemeldet.
- [ ] **Step 2: Tests laufen lassen.** Run: `python3 -m unittest discover figuren -p "test_check_en.py" -v`. Expected: FAIL (Modul fehlt).
- [ ] **Step 3: `check_en.py` implementieren** nach den Interfaces.
- [ ] **Step 4: Tests grün.** Run wie Step 2 und `python3 -m unittest discover figuren`. Expected: alle OK.
- [ ] **Step 5: Commit** „Englische Fassung: Prüfskript für Aufbau, Zahlen und deutsche Reste“.

### Task 4: Sprachschalter für die Abbildungsskripte

**Files:**
- Create: `figuren/sprache.py`, `figuren/en.py`, `figuren/test_sprache.py`
- Modify: `figuren/build.py`

**Interfaces:**
- Produces:
  - `sprache.setze(sprache: str) -> None` (`"de"` oder `"en"`, sonst `ValueError`), `sprache.aktuell() -> str`.
  - `sprache.t(text: str) -> str`: Deutsch → `text`; Englisch → `en.EN[text]`, fehlt der Eintrag: `KeyError` mit dem deutschen Text in der Meldung.
  - `en.EN: dict[str, str]` (deutscher Text → englischer Text).
  - `python3 figuren/build.py --en [NAME …]` schreibt nach `Bilder/figuren/en/`; ohne `--en` wie bisher nach `Bilder/figuren/`.

- [ ] **Step 1: Tests** in `test_sprache.py`: `test_deutsch_unveraendert`, `test_englisch_aus_tabelle` (mit temporär ergänztem `EN`-Eintrag), `test_fehlender_eintrag_ist_fehler`, `test_unbekannte_sprache`, `test_build_en_zielordner` (baut eine Abbildung mit `--en` in ein Temp-Ziel; dafür bekommt `build.main` einen Parameter `ziel: str | None = None`).
- [ ] **Step 2: Tests laufen lassen.** Run: `python3 -m unittest discover figuren -p "test_sprache.py" -v`. Expected: FAIL.
- [ ] **Step 3: `sprache.py`, `en.py`, `build.py --en` implementieren.** `build.py` setzt die Sprache vor dem Erzeugen und danach zurück auf `de`.
- [ ] **Step 4: Tests grün**, `python3 -m unittest discover figuren` OK, `python3 figuren/build.py` erzeugt unveränderte deutsche SVGs (`git status --short Bilder/figuren` leer).
- [ ] **Step 5: Commit** „Englische Fassung: Sprachschalter für die Abbildungen“.

### Task 5: Englische Daten einbinden und prüfen

Braucht `ALLBUS2023_en.sav` (ZA8833) im Projektordner. Fehlt sie, hier anhalten und Yannick fragen.

**Files:**
- Create: `R/_common_en.R`, `R/pruefe_daten_en.R`, `R/test_common_en.R`

**Interfaces:**
- Produces: `R/_common_en.R` lädt `R/_common.R` und definiert `read_spss(path, ...)`, das `"ALLBUS2023.sav"` auf `"ALLBUS2023_en.sav"` umleitet und sonst `mariposa::read_spss()` aufruft. Englische Kapitel binden es im versteckten Setup-Chunk ein (`source("R/_common_en.R")` statt `source("R/_common.R")`).

- [ ] **Step 1: Test** `R/test_common_en.R`: legt in einem Temp-Ordner `R/` (Kopie) und zwei erfundene Dateien an (`haven::write_sav`, `ALLBUS2023.sav` mit Spalte `x = 1:3`, `ALLBUS2023_en.sav` mit `x = 4:6`), sourct `R/_common_en.R` dort, lädt mariposa und prüft mit `stopifnot`, dass `read_spss("ALLBUS2023.sav")$x` gleich `4:6` ist und `read_spss("andere.sav")` normal gelesen wird.
- [ ] **Step 2:** Run: `Rscript R/test_common_en.R`. Expected: Fehler (Datei fehlt).
- [ ] **Step 3: `R/_common_en.R` schreiben.**
- [ ] **Step 4:** Run: `Rscript R/test_common_en.R`. Expected: ohne Fehler, Ausgabe „ok“.
- [ ] **Step 5: `R/pruefe_daten_en.R`** vergleicht beide Dateien und gibt nur Zusammenfassungen aus: Fallzahl, Variablenzahl, Namen nur in einer Datei, Variablen mit abweichenden Wertecodes (Codes der Wertelabels, nicht die Texte). Run: `Rscript R/pruefe_daten_en.R`. Expected: gleiche Fall- und Variablenzahl, keine abweichenden Namen oder Codes. Weicht etwas ab: anhalten, Yannick fragen (Design §7).
- [ ] **Step 6: Commit** „Englische Fassung: englischer ALLBUS (ZA8833) im Buchprojekt“.

### Task 6: Englische Abbildungen für Kap. 4 und Titelbild

**Files:**
- Modify: `figuren/kap04.py`, `figuren/cover.py`, `figuren/en.py`, `figuren/test_kap04.py`, `_quarto-en.yml` (Cover)
- Create: `Bilder/figuren/en/k04-*.svg`, `Bilder/cover-en.svg`

**Interfaces:**
- Consumes: `sprache.t()`, `build.py --en` (Task 4); englische Labels aus ZA8833 (Task 5).

- [ ] **Step 1: Englische Labels holen.** Variablen- und Wertelabels der in `kap04.py` gezeigten Variablen (`sex`, `educ`, `mm01`, `mm06`, fehlende Codes −42, −11, −9, −8) aus `ALLBUS2023_en.sav` lesen (nur Labels, `n_max = 0`).
- [ ] **Step 2: Tests** in `test_kap04.py`: `ERWARTET_KAP04_EN` mit denselben Schlüsseln wie `ERWARTET_KAP04`; Zahlen, Code und Namen gleich, Beschriftungen englisch, Wertelabels exakt wie in ZA8833. Ein Test baut jede Kap.-4-Abbildung mit `setze("en")` und prüft die erwarteten Texte; ein zweiter prüft, dass keine deutsche Beschriftung übrig ist (`check_en.deutsch_reste` auf den SVG-Texten).
- [ ] **Step 3: Tests laufen lassen.** Expected: FAIL.
- [ ] **Step 4: Texte in `kap04.py` und `cover.py` durch `t()` führen**, Einträge in `en.EN` ergänzen. Cover: „R Workshop“, „Social Sciences“, „An introduction to statistical / data analysis with tidyverse and / mariposa“.
- [ ] **Step 5: Tests grün**, `python3 -m unittest discover figuren` OK; `python3 figuren/build.py` lässt deutsche SVGs unverändert; `python3 figuren/build.py --en k04-…` (alle zwölf) und Cover nach `Bilder/cover-en.svg` erzeugen. SVGs ansehen (Read) auf Überlauf langer englischer Labels.
- [ ] **Step 6:** `_quarto-en.yml`: `cover-image: Bilder/cover-en.svg`.
- [ ] **Step 7: Commit** „Englische Fassung: Abbildungen Kap. 4 und Titelbild“.

### Task 7: Englische Stilregeln und Vorwort

**Files:**
- Modify: `STYLE.md` (neuer Abschnitt „12 — Englische Fassung“), `index.en.qmd`

- [ ] **Step 1: `STYLE.md` §12** mit den Regeln aus Design §5.8 und den Anti-Zielen aus §2, der Begriffsliste (Question:/Interpretation., mini study, research journal, exercise, solution, mini research question, Kastennamen aus §5.5) und dem Hinweis, dass der Pilot diese Liste noch ändert.
- [ ] **Step 2: `index.en.qmd` übersetzen** aus `index.qmd`: alle IDs und Chunk-Labels gleich; Roadmap-Chunk mit englischen Beschriftungen; ALLBUS als „German General Social Survey (ALLBUS)“ einführen; Download-Anleitung für ZA8833, Datei als `ALLBUS2023.sav` speichern; Codebeispiele mit `islamophobia` statt `islamophobie`.
- [ ] **Step 3: Prüfen.** Run: `python3 figuren/check_en.py index`. Expected: keine Meldung.
- [ ] **Step 4: Rendern** `quarto render index.en.qmd --profile en`; im Browser `/RWorkshop/en/index.html` ansehen: Titelblock, Cover, Roadmap, Umschalter.
- [ ] **Step 5: Commit** „Englische Fassung: Stilregeln und Vorwort“.

### Task 8: Kap. 4 auf Englisch

**Files:**
- Create: `04-Datenimport.en.qmd`, `_freeze/04-Datenimport.en/`
- Modify: `_quarto-en.yml` (Kapitelliste)

**Interfaces:**
- Consumes: `R/_common_en.R` (Task 5), `Bilder/figuren/en/k04-*.svg` (Task 6), `STYLE.md` §12 (Task 7), `check_en.py` (Task 3).

- [ ] **Step 1: Übersetzen** aus `04-Datenimport.qmd`: Setup-Chunk mit `source("R/_common_en.R")`; Abbildungspfade `Bilder/figuren/en/…`; Bildunterschriften und `fig-alt` englisch; Kommentare und Kategorien im Code englisch; alle IDs gleich; `output-file: 04-Datenimport.html`.
- [ ] **Step 2: Kapitelliste** in `_quarto-en.yml`: `04-Datenimport.qmd` → `04-Datenimport.en.qmd`.
- [ ] **Step 3: Rendern** `quarto render 04-Datenimport.en.qmd --profile en`.
- [ ] **Step 4: Lesarten abgleichen.** Jede Lesart und jedes zitierte Label mit der gerenderten Ausgabe vergleichen; zitiert werden die englischen Labels aus ZA8833.
- [ ] **Step 5: Prüfen.** Run: `python3 figuren/check_en.py 04-Datenimport`. Expected: keine Meldung zu Aufbau, Zahlen oder deutschen Resten. Zahlenabweichungen, die nicht aus der Übersetzung kommen: anhalten, Yannick fragen.
- [ ] **Step 6: Im Browser prüfen** (`/RWorkshop/en/04-Datenimport.html`): englische Kastenetiketten, Übungen und Lösungen, „Output“, „tick off“, Abbildungen, Querverweise, Umschalter in beide Richtungen; Konsole ohne Fehler.
- [ ] **Step 7: Commit** „Englische Fassung: Kap. 4 (Pilot)“.

### Task 9: Pilot übergeben

- [ ] **Step 1:** `./render.sh`, dann `python3 figuren/check_en.py` und `python3 -m unittest discover figuren`. Expected: alles ohne Meldung.
- [ ] **Step 2:** Lokalen Server aus Task 2 starten, Yannick Vorwort und Kap. 4 zeigen und um Durchsicht von Ton und Begriffen bitten. Seine Korrekturen gehen in `STYLE.md` §12 und in die beiden Seiten; erst danach beginnt der Plan für die übrigen neun Seiten.

## Nicht in diesem Plan

Kap. 1–3 und 5–10, `R/prep_en.R`, englische Abbildungen der übrigen Kapitel, README-Abschnitt, NEWS-Eintrag, Veröffentlichung (`/docs/en/` aus `.gitignore` nehmen, `main` vorspulen und pushen). Dafür kommt nach dem Pilot ein eigener Plan.
