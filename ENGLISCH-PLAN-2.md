# Englische Fassung, übrige Kapitel: Umsetzungsplan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Kap. 1–3 und 5–10 erscheinen vollständig auf Englisch unter `docs/en/`, mit englischen Abbildungen, englischen Ausgaben und geschärften Prüfungen; dazu die vereinbarten Korrekturen am deutschen Buch.

**Architecture:** Wie im Pilot (Plan 1, `ENGLISCH-PLAN.md`): `X.en.qmd` neben `X.qmd`, Quarto-Profil `en`, `R/_common_en.R` im versteckten Setup, `set_na()` sichtbar beim Einlesen, Abbildungen über `figuren/sprache.t()` und `build.py --en`. Erst werden Prüfskript, Namenstabelle und `R/prep_en.R` fertig, dann je Kapitel Abbildungen und Text.

**Tech Stack:** Quarto 1.8.25, R 4.6.2, mariposa 0.7.4, Python 3 (unittest), Vanilla-JS, SCSS.

**Spec:** `ENGLISCH-DESIGN.md` (vor allem §5 und §8). Yannick hat den Pilot am 26.11.2026 abends freigegeben („gefällt mir richtig gut“) und die Umsetzung für alle Kapitel über Nacht beauftragt.

## Global Constraints

- Quarto: `/Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto` (nicht im PATH).
- Deutsche Adressen und deutsche Seiten bleiben unverändert, außer den Korrekturen aus Task 3.
- Nur ein `quarto render` gleichzeitig im Projekt, immer genau eine Datei je Aufruf (`quarto render X.en.qmd --profile en` bzw. `quarto render X.qmd`). `./render.sh` nur im Abschluss-Task.
- Git: nie `git add -A` oder `git commit -a`. Immer `git commit -m "<Nachricht>" -- <Pfade>` mit genau den eigenen Dateien (andere Subagenten arbeiten parallel). Bei `index.lock` kurz warten und wiederholen. Nachrichten „Englische Fassung: …“. Nichts pushen. `.claude/`, `.superpowers/`, `*.sav` nie committen. `docs/en/` bleibt in `.gitignore`.
- Englische Dateien: alle IDs der deutschen (`{#sec-…}`, `{#fig-…}`, Chunk-Labels) gleich; `output-file: <deutscher Name>.html`; versteckter Setup mit `source("R/_common_en.R")`, wo Deutsch `R/prep.R` lädt: `source("R/prep_en.R")`.
- Wo im sichtbaren Code der ALLBUS eingelesen wird: `read_spss("ALLBUS2023.sav") |> set_na(-56, -55, -54, -53, -51, -50, -42, -41, -33, -32, -15, -11, -10, -9, -8, -7, -6)` (Design §5.3). Abbildungen, die das Einlesen zeigen, nehmen den Schritt auf, bei Platzmangel als `|> set_na(-56, …, -6)`.
- Eigene Variablen- und Objektnamen nur nach der Tabelle in `STYLE.md` §13 (Task 2). ALLBUS-Namen, `allbus`, Funktions- und Dateinamen bleiben.
- Text: britisches Englisch, *you*, schlicht; keine Slogans, keine Pointen mit Gedankenstrich, keine „not X, but Y“-Figuren, keine Dreierfiguren als Effekt, keine Meta-Sätze über das Material, keine Germanismen („so-called“, „draw into“). Fett nur nach `STYLE.md`. UI-Wörter exakt nach `STYLE.md` §13. Der Inhalt wird übertragen, nicht erweitert.
- Lesarten zitieren Zahlen und Labels der englischen Ausgabe (ZA8833-Labels in Großbuchstaben, wie gedruckt).
- Daten: keine ALLBUS-Datenzeilen in Berichte oder Testausgaben; Labels, Variablennamen und die aggregierten Ausgaben, die das Buch selbst druckt, sind erlaubt. Tests mit erfundenen Daten oder mit TRUE/FALSE-Vergleichen.
- Vorbilder für Ton und Form: `index.en.qmd`, `04-Datenimport.en.qmd`.

## Review Focus

1. Ein englisches Kapitel lädt versehentlich die deutschen Daten (`R/_common.R`, `R/prep.R`) oder deutsche Abbildungen: Die Zahlen stimmen, Labels sind deutsch. Erwartung: `check_en.py` meldet es. Task 1 testet das.
2. Deutsche Reste in Code-Kommentaren, Achsentiteln, Kategorien und R-Ausgaben. Erwartung: `check_en.py` meldet sie. Task 1 testet das.
3. Kap. 9 nutzt Namen aus Kap. 4–8 (`islamophobia_high`, Bildungskategorien). Erwartung: dieselben Namen überall. Task 2 legt sie fest, jede Übersetzung prüft gegen die Tabelle.
4. Ein Kapitel mit Codeblöcken in vier Backticks (Kap. 1, 2) wird falsch gezählt. Task 1 testet das.
5. `check_en.py` meldet bekannte, begründete Abweichungen: Erwartung „0 Meldungen“, wenn jede in `figuren/erwartet_en.py` mit Begründung steht. Task 1 testet das.

---

### Task 1: Prüfskript schärfen, Abbildungs-Build absichern, Datenprüfung vervollständigen

**Files:** Modify `figuren/check_en.py`, `figuren/test_check_en.py`, `figuren/build.py`, `figuren/test_sprache.py`, `R/_common_en.R`, `R/test_common_en.R`, `R/pruefe_daten_en.R`. Create `figuren/erwartet_en.py`.

**Interfaces (Produces):**
- `check_en.code_reste(qmd: str) -> list[str]`: deutsche Wörter/Umlaute in `#`-Kommentaren, Zeichenketten und `#|`-Optionen innerhalb von R-Chunks (Codezeilen ohne Kommentar und Zeichenkette bleiben unberührt).
- `check_en.ausgabe_reste(markdown: str) -> list[str]`: Umlaute und deutsche ALLBUS-Label-Wörter (u. a. STIMME, KEINE ANGABE, WEISS NICHT, TNZ, MANN, FRAU, DATENFEHLER) in den Ausgabeblöcken der englischen Freeze-Datei.
- `check_en.mechanik(qmd: str) -> list[str]`: meldet `source("R/_common.R")`, `source("R/prep.R")`, Abbildungspfade `Bilder/figuren/k…` ohne `/en/`, fehlendes `output-file`.
- `ohne_code` behandelt Zäune mit vier oder mehr Backticks: ein Zaun schließt nur mit gleich vielen oder mehr Backticks und ohne Info-String.
- Zahlvergleich: je Meldung die erste Codezeile der zugehörigen Zelle; sind die Blockzahlen verschieden, nur eine Meldung und kein paarweiser Vergleich danach.
- `figuren/erwartet_en.py`: `ERWARTET: dict[str, list[tuple[str, str]]]` — Kapitelname → Liste (Teilstring der Meldung, Begründung). Passende Meldungen zählen nicht; der CLI-Lauf druckt sie als „erwartet: …“ und endet mit 0, wenn nur erwartete übrig sind. Einträge für `04-Datenimport` für die vier bekannten Meldungen (Design §8.3).
- `build.py --en` baut nur Module mit `SPRACHFAEHIG = True` (Modulkonstante; in `kap04.py` setzen); ein Test prüft `deutsch_reste` auf allen SVG-Texten in `Bilder/figuren/en/`.
- `R/_common_en.R` leitet per `basename(path) == "ALLBUS2023.sav"` um; `R/pruefe_daten_en.R` vergleicht auch `na_values`/`na_range` (ZA8833 hat keine: als bekannt ausweisen) und endet mit `quit(status = 1)` bei unerwarteten Abweichungen.

- [ ] Tests zuerst (je Interface mindestens ein Fall, darunter: englische `.qmd` mit `source("R/_common.R")` → Meldung; deutscher Kommentar `# Mittelwert` im Chunk → Meldung; Ausgabe mit `KEINE ANGABE` → Meldung; Vier-Backtick-Block mit innerem ```` ```{r} ```` → Überschrift darin zählt nicht; erwartete Meldung → Exit 0). Rot sehen.
- [ ] Umsetzen, `python3 -m unittest discover figuren` grün, `Rscript R/test_common_en.R` → ok.
- [ ] `python3 figuren/check_en.py` (alle) → für `index` und `04-Datenimport` 0 Meldungen. Echte Funde in den Pilotdateien (z. B. deutsche Kommentare) nicht ins Erwartet-Verzeichnis schieben, sondern im Bericht nennen; Task 3 behebt sie.
- [ ] Commit „Englische Fassung: Prüfskript sieht Code, Ausgaben und Mechanik“.

### Task 2: Namenstabelle und Checkliste in `STYLE.md` §13

**Files:** Modify `STYLE.md`, `BILDER.md`.

- [ ] Alle im Buch gebildeten Variablen, Objekte, Faktorstufen und Modellnamen aus `R/prep.R` und Kap. 3, 5–10 sammeln (Zuweisungen `<-`, `mutate(name = …)`, `rec(… [label])`, `labels = c(…)`, `levels`). Für jeden einen englischen Namen festlegen; bereits vergeben: `islamophobie` → `islamophobia`, `populismus` → `populism`, `islamophobie_p` → `islamophobia_p`, `populismus_p` → `populism_p`, `islam_hoch` → `islamophobia_high`. snake_case, kurz, ohne Umlaute; Faktorstufen englisch klein (niedrig/mittel/hoch → low/medium/high).
- [ ] Tabelle „Namen im Code (verbindlich)“ in §13: deutsch → englisch → wo verwendet (Kapitel).
- [ ] Checkliste „Ein Kapitel übersetzen“ in §13: Setup mit `R/_common_en.R`/`R/prep_en.R`, `set_na()` beim sichtbaren Einlesen, Abbildungspfade `Bilder/figuren/en/`, Kapitel in `_quarto-en.yml` tauschen, Abbildungen über `t()` und `build.py --en`, Einzel-Render, `check_en.py`, erwartete Abweichungen mit Begründung in `figuren/erwartet_en.py`, `Rscript R/test_common_en.R`.
- [ ] `BILDER.md`: Abschnitt zu englischen Fassungen (`t()`, `en.EN`, `SPRACHFAEHIG`, `build.py --en`, Wertelabels aus ZA8833).
- [ ] Commit „Englische Fassung: Namenstabelle und Kapitel-Checkliste“.

### Task 3: Korrekturen im deutschen Buch und im Pilot

**Files:** Modify `index.qmd`, `04-Datenimport.qmd`, `10-KI-Assistenten.qmd`, `README.md`, `STUDIE.md`, `.gitignore`, `index.en.qmd`, `04-Datenimport.en.qmd`, `figuren/kap04.py`, `figuren/en.py`, `figuren/test_kap04.py`, `Bilder/figuren/en/k04-einlesen.svg`, `figuren/erwartet_en.py` (nur falls nötig).

- [ ] ZA8830/ZA8901 → ZA8831 mit Link `https://search.gesis.org/research_data/ZA8831` und dem Namen „ALLBUScompact 2023“ in den deutschen Dateien (Design §8.7). „R for Data Science“ 2. Aufl.: Mine Çetinkaya-Rundel ergänzen, deutsch und englisch.
- [ ] `k04-einlesen` (nur englisch) zeigt den Einlese-Schritt mit `|> set_na(-56, …, -6)`; deutsch byte-gleich; Test in `test_kap04.py` angepasst; Bildunterschrift/Alt-Text in `04-Datenimport.en.qmd` passend.
- [ ] Funde aus Task 1 in den Pilotdateien beheben.
- [ ] Rendern einzeln: `index.qmd`, `04-Datenimport.qmd`, `10-KI-Assistenten.qmd` (deutsch), dann `index.en.qmd`, `04-Datenimport.en.qmd` (`--profile en`). Deutsche Zahlen dürfen sich nicht ändern (`git diff --stat _freeze/` nur bei den drei Kapiteln; Ausgaben identisch).
- [ ] `python3 figuren/check_en.py index 04-Datenimport` → 0 Meldungen; `python3 figuren/check_sections.py` wie vorher.
- [ ] Commit „Deutsches Buch: Studiennummer ZA8831, Autorenliste R4DS; Englisch: Einlesen mit set_na() im Bild“.

### Task 4: `R/prep_en.R`

**Files:** Create `R/prep_en.R`, `R/test_prep_en.R`.

- [ ] `R/prep_en.R` = `R/prep.R` mit `set_na()` beim Einlesen, englischen Namen aus §13, englischen Kommentaren (ASCII). Liest `read_spss("ALLBUS2023.sav")` (Umleitung durch `R/_common_en.R`).
- [ ] `R/test_prep_en.R`: sourct `R/_common.R`+`R/prep.R` in einer Umgebung und `R/_common_en.R`+`R/prep_en.R` in einer zweiten; prüft mit `stopifnot`, dass jede gebildete Variable numerisch gleich ist (`isTRUE(all.equal(...))` nach `zap_labels`), und gibt nur „ok“ oder die Namen abweichender Variablen aus.
- [ ] `Rscript R/test_prep_en.R` → ok. Commit „Englische Fassung: R/prep_en.R“.

### Tasks F1–F5: Englische Abbildungen (je eine Kapitelgruppe)

F1: `kap01.py`, `kap02.py` (9 Abbildungen). F2: `kap03.py` (16). F3: `kap05.py` (17). F4: `kap06.py`, `kap07.py`, `kap08.py` (10). F5: `kap09.py` (5).

Je Task, nach dem Vorbild von Task 6 aus Plan 1:
- [ ] Alle menschenlesbaren deutschen Texte über `sprache.t()` (als `tr` importiert, falls `t` belegt ist), Einträge in `figuren/en.py`, `SPRACHFAEHIG = True`. Code, Namen, Zahlen und R-Ausgabeformate bleiben; eigene Namen nach §13; ALLBUS-Labels exakt aus ZA8833; Missing-Buchstaben und Ausgaben, die eine Abbildung nachbildet, aus der englischen Ausgabe (Daten wie Design §5.3 einlesen). Einlese-Abbildungen (`k02-render-sitzung`, `k03-analyseplan`, `k05-pipeline`) mit `set_na()`-Schritt.
- [ ] Tests: in vorhandenen `test_kapNN.py` ein `ERWARTET_KAPNN_EN` mit denselben Schlüsseln und einen Bautest im Englischen; für `kap03` eine neue `test_kap03.py` mit mindestens dem Bautest und der Prüfung auf deutsche Reste. Erst rot, dann grün; ganze Suite grün; deutsche SVGs byte-gleich (`git status --short Bilder/figuren`).
- [ ] `python3 figuren/build.py --en <Namen>`; jede englische SVG mit `qlmanage -t -s 900` als PNG ansehen; Überlauf zuerst durch kürzere Wörter beheben, Maße nur fürs Englische ändern.
- [ ] Commit „Englische Fassung: Abbildungen Kap. NN“ (nur `figuren/…`, `Bilder/figuren/en/…`).

### Tasks K1, K2, K3, K5, K6, K7, K8, K9, K10: Kapitel übersetzen

Je Kapitel `NN-Name.qmd` → `NN-Name.en.qmd`, nach dem Vorbild von Task 8 aus Plan 1 und der Checkliste in `STYLE.md` §13. Voraussetzung: Tasks 1–4 und die Abbildungen des Kapitels (F-Task) sind fertig; K10 hat keine Abbildungen.

- [ ] Übersetzen nach Global Constraints. Besonderheiten: K1 (RStudio-Bildschirmfotos bleiben, Design §5.7; Tastenkürzel Strg → Ctrl), K2 (YAML-Beispiele englisch, etwa `lang: en`, `date-format`; Setup-Beispiele mit `set_na()`), K3 (`real-pipe` mit `set_na()`), K5 (versteckter Setup und `full-pipeline` mit `set_na()` und Namen aus §13; die Pipeline entspricht `R/prep_en.R`), K6–K9 (`source("R/prep_en.R")`), K10 (Prompt-Vorlagen englisch; die Prompt-Regel zu fehlenden Werten nennt den `set_na()`-Schritt; GESIS-Hinweis für ZA8833; werkzeugneutral, keine Produkt-Klickanleitungen).
- [ ] `_quarto-en.yml`: deutschen Eintrag durch `.en.qmd` ersetzen.
- [ ] `quarto render NN-Name.en.qmd --profile en`.
- [ ] Lesarten gegen die englische Ausgabe abgleichen; `python3 figuren/check_en.py NN-Name` → 0 Meldungen, begründete Abweichungen (andere `find_var()`-Treffer, Reihenfolge, Studiennummer/Version, `splt23_2`) in `figuren/erwartet_en.py` mit Begründung. Zahlenabweichungen ohne Grund in der Übersetzung: anhalten und melden.
- [ ] Im Browser (`buch-unterpfad`, `http://localhost:8780/RWorkshop/en/NN-Name.html`): Kästen, Übungen, Lösungen, Karten, Abbildungen, Querverweise, Umschalter, Konsole.
- [ ] Commit „Englische Fassung: Kap. N“ (`NN-Name.en.qmd`, `_quarto-en.yml`, `_freeze/NN-Name.en/`, ggf. `figuren/erwartet_en.py`).

### Task Z: Abschluss

- [ ] `figuren/kapitelkarten.py` um `--en` erweitern (liest `*.en.qmd`, schreibt den Überblick in `index.en.qmd`), damit die Kapitelkarten im englischen Vorwort zu den englischen Kapiteln passen; deutsch unverändert.
- [ ] `./render.sh`; `python3 figuren/check_en.py` → 0 Meldungen für alle elf Seiten; `python3 -m unittest discover figuren`; `Rscript R/test_common_en.R`; `Rscript R/test_prep_en.R`; `python3 figuren/check_sections.py` wie vorher.
- [ ] Im Browser jede englische Seite einmal öffnen (Konsole, Umschalter, Kästen).
- [ ] Commit „Englische Fassung: Kapitelkarten, Gesamt-Render“.

## Nicht in diesem Plan

Veröffentlichung (`/docs/en/` aus `.gitignore`, README auf `./render.sh` und englischer Abschnitt, NEWS, `main` vorspulen und pushen) — das entscheidet Yannick nach dem Lesen. Neue RStudio-Bildschirmfotos.
