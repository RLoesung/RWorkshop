# Englische Fassung: Bericht nach der Nacht vom 26. auf den 27.11.2026

## Stand

Alle elf Seiten (Vorwort, Kap. 1–10) liegen auf Englisch vor, mit englischen Abbildungen, englischen R-Ausgaben (ZA8833) und Sprachumschalter. Jedes Kapitel wurde einzeln übersetzt, gerendert, gegen die deutschen Zahlen geprüft und von einem zweiten Durchgang auf Ton und Fachbegriffe gegengelesen; danach kam eine Gesamtprüfung. Alles ist auf `modernisierung-2026` committet. Nichts ist gepusht, `docs/en/` steht weiter in `.gitignore`.

Lesen: `./render.sh` ist gelaufen; mit dem lokalen Server (in `.claude/launch.json` als `buch-unterpfad`) liegt die englische Startseite unter `http://localhost:8780/RWorkshop/en/index.html`. Der Knopf „Deutsch“/„English“ wechselt die Sprache.

## Entscheidungen, die ich nachts getroffen habe

Inhaltlich (bitte beim Lesen prüfen):

- **Eigene Namen im Code:** verbindliche Tabelle in `STYLE.md` §13, z. B. `educ_kat` → `educ_cat` (low/medium/high), `islam_hoch` → `islamophobia_high`, `m_basis`/`m_voll` → `m_base`/`m_full`, `farben` → `color_values`, `beispiel` → `example_data`. In Kap. 3 heißt das Spielzeug-Objekt `alter` bewusst `age` (ALLBUS ist dort nicht geladen); in Kap. 5 wird daraus `age_years`. Die kurzen Tabellennamen `islam_p`, `pop_p` und der lavaan-Faktor `islam` bleiben.
- **`set_na()`** steht überall, wo der ALLBUS sichtbar eingelesen wird; nur die Pfad-Beispiele in Kap. 1 zeigen bloß `read_spss()`. Kap. 3 hat im Hintergrund-Kasten zu fehlenden Werten einen Halbsatz dazu bekommen, Kap. 2 einen Verweis auf Kap. 4.
- **Beispieldateien:** `01-first_steps.qmd`, `analysis.qmd`, `references.bib`, `my-project/`. Die RStudio-Fotos zeigen weiter `01-erste_schritte.qmd`; Kap. 1 sagt das in einem Satz („The screenshots come from the German edition …“). Wenn dich der Satz stört: streichen.
- **`R/prep.R` im Text von Kap. 5** bleibt der Name der eigenen Datei der Leser:innen; ein Satz nennt `R/prep_en.R` als englische Fassung im Repository.
- **Kap. 6:** Damit die Legende „Education: low, medium, high“ nicht abgeschnitten wird, setzt der versteckte Setup-Chunk `var_label(educ_cat = "Education")`.
- **Kap. 8:** eine zusätzliche Zeile `fct_relevel(share, "shared")` in der KMO-Grafik (sonst kippt die Stapelreihenfolge mit englischen Namen).
- **Kap. 10:** Link und Wortlaut folgen der offiziellen englischen Fassung der GESIS-Nutzungsbedingungen (https://www.gesis.org/en/institute/data-usage-terms, Abschnitt 4).
- **Begriffe:** „Interpretation.“ für „Lesart.“, „continuous“ statt „metric“, „dialog box“ (RStudio-Vokabular), britische Schreibung.

Am deutschen Buch (eindeutige Fehler, die beim Übersetzen auffielen; die Zahlen der R-Ausgaben sind unverändert):

- Studiennummer ZA8831 statt ZA8830/ZA8901; Mine Çetinkaya-Rundel bei „R for Data Science“ ergänzt (Vorwort, Kap. 2, 4, 5).
- Kap. 2: Inline-Code in den Markdown-Beispielen wurde ausgeführt („32 Fahrzeuge“ statt Quelltext); ungültiger Chunk-Kopf (`fig-cap=` → `fig.cap=`); `fig-cap` an einem Chunk ohne Grafik; Backticks im Titel von Übung 1; „private Repositories für Studierende“.
- Kap. 7: abgeschnittene Beschriftung in der ANOVA-Grafik.
- Kap. 8: Legende der Fit-Grafik zeigte „verfehlt“ bei erfüllten Schwellen; Tabellenkopf `|Ladung|` verschluckte die Spalte „Lesart“; drei abgeschnittene Beschriftungen.
- Kap. 9: Lesart nannte OR = 0,34 (Ausgabe: 0,330); „unter `Estimate`“ statt `B`; zwei abgeschnittene Bildunterschriften; abgeschnittener Titel der Koeffizientengrafik.

## Fundstellen im deutschen Original, die du entscheiden solltest

Nicht geändert, weil es um Inhalt oder Stil geht. Die englische Fassung übernimmt sie, bis du entscheidest.

- **Vorwort:** „Jedes Kapitel endet mit vier Übungen“, Kap. 3 und 7 haben fünf.
- **Kap. 2:** Schlüssel `Schulz2017` mit `year = {2018}`, Kap. 5 zitiert 2017 (online 2017, Heft 2018: eins wählen). „Wie @Goodman2016 zeigt“ → „zeigen“ (auch im `fig-alt`).
- **Kap. 3:** Übung 5 nennt für `pt03` eine Skala 0–10, codiert ist 1–7. Die Musterlösung filtert per Index, die „Pipe“ hat einen Schritt. „Modern R with the Tidyverse“ ist ein Buch, kein Kurs. `[[]]` und `[[ ]]` gemischt.
- **Kap. 5:** Z. 34 „diese sechs Items“ nach drei Zitaten; Z. 78 schreibt `mutate()` „mariposa/dplyr“ zu; Z. 706 „leicht mittig“ für den exakten Mittelpunkt 4; Z. 790 `cronbachs α` klein. Die Abbildung `k05-pipeline` sagt „POMPS-Versionen“, die englische nun ebenfalls.
- **Kap. 6:** Pointen Z. 29/31, Dreierfigur Z. 350, Werbeton Z. 352; Z. 203 „dünne Outlines … leere Fläche“ stimmt nicht (die Balken bleiben grau gefüllt); Z. 452 verweist auf den versteckten Setup; Z. 95 unwahrscheinliches Fehlerbeispiel; Z. 491 „gefiltert“ passt nicht zu `facet_wrap()`; Legende in `to-label-axis` abgeschnitten (englisch per `var_label` gelöst).
- **Kap. 7:** Münzbeispiel: p = 0,057 ist zweiseitig, P(≥ 60 Kopf) ≈ 0,028. p-Wert-Formulierung Z. 127 und Z. 593 widerspricht dem eigenen Vorsicht-Kasten. Hedges' g ist biaskorrigiert, nicht „robuster bei kleinem N“. Glossar „gepoolter SE“, Standard ist Welch. Die BETWEEN-Beschriftung wird von der Linie des Gesamtmittels durchgestrichen.
- **Kap. 8:** RMSEA-Grenze ≤ 0,06 im Text, ≤ 0,08 in Übung 4. KMO-Stufen im Glossar passen nicht zu Kaisers Tabelle. „Jedes Item MSA ≥ 0,85“, aber mm04 = 0,849. „Deutlich über 0,3“ bei einem Minimum von 0,34. Bartlett „konservativ“. Reliabilität als „Validitäts-Pfeiler“. λ für Eigenwerte und Ladungen. Das Schluss-Journal sagt, die CFA passe gut, der CFA-Chunk läuft aber nicht (`eval=FALSE`). Beschriftungen in der Rotationsgrafik überlappen.
- **Kap. 9:** Z. 934 „β̂ als standardisierte Kovarianz“ ist die Korrelation. Die Koeffizientengrafik zeigt unstandardisierte B auf verschiedenen Skalen, der Text liest daraus den stärksten Effekt ab (Alter liegt bei ≈ 0, das KI von `sexDIVERS` streckt die Achse). Beschriftungen im Patchwork-Boxplot überlappen. In `r2-anteil` ist der 100-%-Strich abgeschnitten. Die Achse „Residuals vs Leverage“ reicht bis 1,0 (ein Fall mit Leverage 1). Fett in den Übungen über STYLE hinaus. Z. 546 „beide wirken in beiden Regionen ähnlich“ unklar. Nagelkerke „grob vergleichbar“ im Text, „nicht direkt vergleichbar“ im Glossar.

## Nächste Pflegeschritte (nicht mehr erledigt)

- `check_en.py` vergleicht Aufbau und Ausgabezahlen, aber keine Zahlen im Fließtext. Ein Vergleich der Zahlen im Fließtext beider Sprachen würde Lesarten absichern, die nur in einer Sprache geändert werden.
- Einträge in `figuren/erwartet_en.py` passen über Blocknummer und erste Codezeile; genauer wäre die vollständige Meldung.
- `R/test_prep_en.R` prüft die 13 bekannten Variablen; eine neue Variable in `R/prep.R` ohne englisches Gegenstück fiele nicht auf.
- Die Jitter-Grafiken haben kein `set.seed()`; ihre PNGs ändern sich bei jedem Render (beide Sprachen).

## Veröffentlichen

1. Lesen, Korrekturen in deutsch und englisch einarbeiten (Checkliste „Ein Kapitel ändern (beide Sprachen)“ in `STYLE.md` §13).
2. README um einen englischen Abschnitt ergänzen (lesen unter `/en/`, ZA8833 laden und als `ALLBUS2023.sav` speichern).
3. `/docs/en/` aus `.gitignore` nehmen (die Zeilen für lose Vorschauen bleiben).
4. `./render.sh`, dann `python3 figuren/check_en.py`.
5. NEWS-Eintrag anpassen („noch nicht veröffentlicht“ ersetzen).
6. Committen, inklusive `docs/en/`; prüfen, dass unter `docs/en` nichts als gelöscht erscheint.
7. `main` vorspulen (`git merge --ff-only`) und pushen. Der Knopf „English“ erscheint auf den deutschen Seiten von selbst, sobald `/en/X.html` erreichbar ist.

Die Korrekturen am deutschen Buch können auch allein online gehen: dieselben Schritte ohne Punkt 2–3; der Knopf bleibt dann verborgen.
