# R Workshop – Sozialwissenschaften

**Einführung in die statistische Datenanalyse mit tidyverse und mariposa**

📖 **Online lesen:** <https://rloesung.github.io/RWorkshop/> · **English edition:** <https://rloesung.github.io/RWorkshop/en/>

Ein frei verfügbares, deutschsprachiges Lehrbuch für Studierende der Sozialwissenschaften, die R neu kennenlernen, oft mit Vorerfahrung in SPSS. Das Buch führt vom ersten Datenimport über deskriptive und inferenzstatistische Verfahren bis zu Faktorenanalyse und Regression. Der Werkzeugkasten ist bewusst klein gehalten: das [tidyverse](https://www.tidyverse.org/) für Datenmanipulation und Grafiken, [mariposa](https://yannickdiehl.github.io/mariposa/) für die statistische Analyse mit SPSS-artigen Ausgaben und [Quarto](https://quarto.org/) für reproduzierbare Berichte.

Durch alle Kapitel zieht sich eine Mini-Studie mit dem **ALLBUS 2023**:

> *Wer trägt islamfeindliche Einstellungen in Deutschland 2023, und wie hängen sie mit politischen Orientierungen und Soziostruktur zusammen?*

## English edition

The book is also available in English at <https://rloesung.github.io/RWorkshop/en/>, with the same chapters, code and exercises. The English chapters work with the English-language edition of the dataset, GESIS study [ZA8833](https://search.gesis.org/research_data/ZA8833) ("German General Social Survey – ALLBUScompact 2023"). Download it with a free GESIS account and save it as `ALLBUS2023.sav` in your project folder. This file does not mark missing values, so the English chapters declare them with `set_na()` when they read the data (Chapter 4).

In this repository the English chapters are the `*.en.qmd` files next to the German ones, and `R/prep_en.R` is the English version of the data preparation in `R/prep.R`.

## Inhalt

| Kap. | Thema | Schwerpunkte |
|---:|---|---|
| 0 | Vorwort | Ziele, Voraussetzungen, Datensatz, Aufbau der Kapitel |
| 1 | RStudio | Installation, Oberfläche, Projekte, Pakete, Hilfe finden |
| 2 | Quarto und reproduzierbare Wissenschaft | Markdown, YAML, Code-Chunks, Literaturverweise, Publizieren als HTML/PDF/Word |
| 3 | Programmiersprache R | Variablen, Funktionen, Operatoren, Datentypen, `NA`, die Pipe `\|>` |
| 4 | Datenimport und Inspektion | `read_spss()`, `find_var()`, `codebook()`, Labels, fehlende Werte |
| 5 | Daten transformieren und Skalen bilden | dplyr-Verben, `rec()`, Umpolen, `row_means()`, `pomps()` |
| 6 | Visualisierung — Grundlagen | Grammar of Graphics mit ggplot2, Facets, Themes |
| 7 | Uni- und bivariate Analyse | Gewichtung, Inferenz, Kreuztabellen, Korrelation, t-Test, ANOVA |
| 8 | Latente Strukturen | KMO, EFA, Cronbachs α und McDonalds ω, CFA-Ausblick |
| 9 | Erklärungsmodelle | lineare und logistische Regression, VIF, Residuen, ANCOVA, AME |
| 10 | Mit KI-Assistenten arbeiten | Kontext für Assistenten, Antworten prüfen, Datenschutz nach den GESIS-Bedingungen |

Jedes Kapitel folgt dem Dreischritt **Frage → Code → Lesart** und endet mit Übungen (Lösungen zum Aufklappen) und einer Mini-Forschungsfrage.

## Buch lokal rendern

**Voraussetzungen**

- R ≥ 4.3 (empfohlen ≥ 4.5) und Quarto. Quarto ist in aktuellen RStudio-Versionen enthalten; gerendert wird derzeit mit Quarto 1.8.
- Die R-Pakete, alle von CRAN:

  ```r
  install.packages(c("tidyverse", "mariposa", "patchwork", "lavaan", "semPlot"))
  ```

  Das Buch ist auf **mariposa ≥ 0.7.4** abgestimmt. Ältere Versionen liefern an einigen Stellen andere Ausgaben oder brechen ab.
- Der Datensatz **ALLBUS 2023** als `ALLBUS2023.sav` im Projektordner. Er liegt **nicht** im Repository, denn wir geben die Daten nicht weiter. Du lädst sie selbst aus dem [GESIS-Datenbestandskatalog, Studiennummer ZA8831](https://search.gesis.org/research_data/ZA8831) („ALLBUScompact 2023“) herunter. Dafür brauchst du einen kostenlosen GESIS-Account. Für die englische Fassung kommt die englischsprachige Ausgabe [ZA8833](https://search.gesis.org/research_data/ZA8833) als `ALLBUS2023_en.sav` dazu. `.gitignore` schließt `.sav`- und `.dta`-Dateien aus, damit sie nicht versehentlich committet werden.

**Rendern**

```bash
./render.sh                                           # ganzes Buch, deutsch nach docs/, englisch nach docs/en/
quarto render 07-Uni-Bivariate-Analyse.qmd            # ein Kapitel, deutsch
quarto render 07-Uni-Bivariate-Analyse.en.qmd --profile en   # ein Kapitel, englisch
```

Für das ganze Buch nimmst du `./render.sh`: Es baut erst die deutsche, dann die englische Fassung. Ein schlichtes `quarto render` baut nur die deutsche Fassung und leert dabei `docs/en/`.

Die englische Fassung liegt unter `docs/en/` und ist online unter <https://rloesung.github.io/RWorkshop/en/>. Auf jeder Seite führt ein Knopf zur selben Seite in der anderen Sprache.

Das Projekt nutzt `freeze: auto`: Beim Render des ganzen Buchs werden nur Kapitel neu gerechnet, deren Quelltext sich geändert hat. Alle anderen Kapitel kommen aus `_freeze/`. Wenn du ein einzelnes Kapitel gezielt renderst, wird es immer neu ausgeführt. Das ist der Weg nach einem Paket-Update.

Die Online-Fassung liefert GitHub Pages direkt aus `docs/` auf `main` aus. Nach dem Rendern werden deshalb `docs/` und `_freeze/` mit committet.

## Projektstruktur

```
├── index.qmd                 Vorwort (Kap. 0)
├── 01-RStudio.qmd … 10-KI-Assistenten.qmd   Kapitel
├── index.en.qmd, 01-RStudio.en.qmd …        englische Fassung (je eine Datei neben der deutschen)
├── R/
│   ├── _common.R             gemeinsames ggplot-Theme (theme_rworkshop)
│   ├── _common_en.R          dasselbe für die englische Fassung (liest ALLBUS2023_en.sav)
│   ├── prep.R                Datenpräp-Pipeline der Mini-Studie (Kap. 5)
│   └── prep_en.R             dieselbe Pipeline mit englischen Namen
├── figuren/                  Skripte für die Abbildungen, Prüfskripte und Tests
├── Bilder/                   Screenshots für Kap. 1 und die Abbildungen (Bilder/figuren/, englisch in en/)
├── _quarto.yml               Buch-Konfiguration (gemeinsamer Teil)
├── _quarto-de.yml            Kapitelliste und Optionen der deutschen Fassung
├── _quarto-en.yml            dasselbe für die englische Fassung (Profil en)
├── render.sh                 baut beide Sprachfassungen nacheinander
├── theme.scss                Theme-Anpassungen (auf Basis von cosmo)
├── ALLBUS2023.sav            Datensatz — nicht im Repo, selbst bei GESIS laden
├── ALLBUS2023_en.sav         englischsprachige Ausgabe (ZA8833) — ebenfalls nicht im Repo
├── _freeze/                  eingefrorene Rechenergebnisse (versioniert)
├── docs/                     gerendertes Buch für GitHub Pages (versioniert)
├── STYLE.md                  Stil- und Didaktik-Leitfaden
├── MIGRATION.md              Code-Konventionen und Funktions-Mapping (tidyverse + mariposa)
├── STUDIE.md                 Mini-Studie: Variablen, Pipeline, Methoden-Mapping, Befunde
└── NEWS.md                   Änderungsprotokoll
```

## Mitmachen

Fehler gefunden, etwas unklar, Idee für eine Übung? Über ein [Issue](https://github.com/RLoesung/RWorkshop/issues) oder einen Pull Request. Jede Kapitelseite hat rechts die Links „Seite editieren" und „Problem melden".

- Für Text- und Code-Korrekturen reicht eine Änderung an der jeweiligen `.qmd`-Datei. `docs/` und `_freeze/` musst du nicht mitliefern. Betrifft die Korrektur Inhalt, den es in beiden Sprachen gibt, ändere auch die `.en.qmd`-Datei oder schreib es dazu; wir ziehen die andere Sprache dann nach.
- Sprache, Kapitelaufbau und Callout-Typen regelt [`STYLE.md`](STYLE.md), die Code-Konventionen regelt [`MIGRATION.md`](MIGRATION.md).
- Viele Lesart-Texte zitieren konkrete Zahlen aus den Ausgaben. Wer Code ändert, prüft bitte, ob die Zahlen im Text noch stimmen.
- Probleme mit mariposa selbst gehören in den [mariposa-Issue-Tracker](https://github.com/YannickDiehl/mariposa/issues).

## Autor:innen

Yannick Diehl und Daniel Moosdorf.

Was sich wann geändert hat, steht in [`NEWS.md`](NEWS.md).
