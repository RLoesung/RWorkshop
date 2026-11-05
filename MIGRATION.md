# Migration Cheatsheet — RWorkshop 2026

**Zweck.** Verbindliches Mapping vom alten Funktions-Zoo (strengejacke, sjmisc, sjstats, sjlabelled, sjplot, descr, weights, psych, easystats, texreg, corrplot, gridExtra) auf das neue Zwei-Paket-Setup **tidyverse + mariposa**. Diese Datei ist der Vertrag, an den sich alle Kapitelmigrationen halten. Abweichungen nur mit Notiz hier unter „Restbedarf".

**Stand: mariposa 0.7.4 (CRAN), dplyr 1.2.** Installation über `install.packages("mariposa")`.

**Konventionen.**
- Pipe immer `|>` (native, R 4.6).
- Argumente in `snake_case`, Logik `TRUE`/`FALSE` (nie `T`/`F`). mariposa verlangt seit 0.6.9 die snake_case-Namen (`as_factor`, `tag_na`, `sort_frq`, …) und seit 0.7.4 **ausgeschriebene** Argumentnamen — `as.factor =`, `weight =` oder `percent =` sind Fehler.
- mariposa-Ergebnisse drucken kompakt; die vollständigen SPSS-Tabellen kommen mit `summary()`. Lesart-Texte, die Tabellendetails zitieren (Gruppenmittelwerte, Ladungen, Item-Total-Statistiken, Post-Hoc-Paare), brauchen einen `summary()`-Chunk.
- `library()` ausschließlich im Setup-Chunk, nie im Kapitel-Text.
- mariposa-Funktionen sind data-first und tidyselect-fähig — `data |> fn(var1, var2, weights = w)` ist die Standardform.

---

## 1 — Datenimport & -export

| Alt | Neu (mariposa) | Notiz |
|---|---|---|
| `sjlabelled::read_spss(file)` | `mariposa::read_spss(path)` | Identische Idee, `tag_na = TRUE` als Default — Tagged NAs werden erhalten. |
| `haven::read_sav(file)` | `mariposa::read_spss(path)` | mariposa wrappt haven mit konsistentem Labels-/NA-Verhalten. |
| `foreign::read.spss()` | `mariposa::read_spss(path)` | foreign komplett raus. |
| `sjlabelled::write_spss(x, file)` | `mariposa::write_spss(data, path)` | — |
| `haven::read_dta()` | `mariposa::read_stata(path)` | — |
| `readxl::read_xlsx()` | `mariposa::read_xlsx(path)` | Falls Excel-Import nötig. |

**Beispiel:**
```r
# alt
allbus <- sjlabelled::read_spss("ALLBUS2023.sav") |> tibble::as_tibble()

# neu
allbus <- read_spss("ALLBUS2023.sav")
```

---

## 2 — Labels & fehlende Werte

| Alt | Neu (mariposa) |
|---|---|
| `sjlabelled::get_label(x)` | `var_label(data)` |
| `sjlabelled::set_label(x) <- "…"` | `var_label(data$var) <- "…"` bzw. `var_label(data) <- list(var = "…")` (Setter seit 0.7.4) |
| `sjlabelled::get_labels(x)` | `val_labels(data)` |
| `sjlabelled::set_na(x, na = c(-9, -42))` | `set_na(data, var = c(-9, -42))` (benannte Paare; unbenannte Werte gelten für alle numerischen Spalten) |
| `sjlabelled::drop_labels(x)` | `drop_labels(data)` |
| `sjlabelled::copy_labels(x, y)` | `copy_labels(data, source)` |
| `sjlabelled::to_label(x)` | `to_label(data, var)` |
| `sjlabelled::as_factor(x)` | `to_label(data, var, ordered = FALSE)` |
| `sjmisc::to_numeric()` | `to_numeric(data, var)` |
| `haven::as_factor()` | `to_label(data, var)` (Tidy-Workflow) |

**Beispiel:**
```r
# alt
allbus <- allbus |> sjlabelled::set_na(c(-9, -42))
geschlecht <- sjlabelled::to_label(allbus$sex)

# neu
allbus <- allbus |> set_na(educ = c(6, 7))      # Codes pro Variable als Name-Wert-Paar
allbus <- allbus |> to_label(sex)
```

**Hinweis (0.7.4).** `to_label()` auf den ganzen Datensatz wandelt nur *vollständig* gelabelte Variablen um — für einzelne Variablen sie immer explizit nennen.

---

## 3 — Rekodierung & Transformation

| Alt | Neu (mariposa) |
|---|---|
| `sjmisc::rec(x, rec = "1=1; 2,3=2; else=NA")` | `rec(data, var, rules = "1=1; 2,3=2; else=NA")` (Faktor-Ausgabe: `as_factor = TRUE`) |
| `sjmisc::to_dummy()` | `to_dummy(data, var)` |
| `dplyr::case_when()` (für simple Rekodierungen) | bleibt `case_when()` / für reine Wert-Mappings `recode_values()` |
| `scale(x)` / `sjmisc::std()` | `std(data, var)` (gewichtsfähig) |
| `sjmisc::center()` | `center(data, var)` |
| `sjmisc::row_means(data, var:var)` | `row_means(data, var1, var2, …, min_valid = 10)` |
| `psych::reverse.code()` | `rec(data, var, rules = "rev")` — Skalengrenzen aus den Wertelabels; ohne Labels `rules = "rev(1, 5)"` |

**Wichtig.** `case_when()` bleibt die Standardform für Bedingungslogik. `case_match()` ist seit dplyr 1.2 *deprecated* — Nachfolger ist `recode_values()` mit identischer Formelschreibweise.

**`rec()` seit 0.7.4.** `"rev"` polt anhand der Wertelabel-Spannweite um (nicht mehr anhand des beobachteten Bereichs) und spiegelt die Labels mit. Werte ohne passende Regel werden `NA` *mit Warnung* — `else=copy` oder `else=NA` immer explizit setzen. Neue Regelsyntax: Wertelisten `"1,2=1"`, explizite Grenzen `"rev(lo, hi)"`. Mehrere Variablen in einem Aufruf: `rec(pa29:pa35, rules = "rev", suffix = "r")`.

**Folge für `pivot_longer()`.** Umgepolte Items tragen gespiegelte Labels; vor dem Stapeln labelled-Spalten mit `unlabel()` ablegen, sonst „conflicting value labels"-Warnungen.

---

## 4 — Deskriptive Statistik

| Alt | Neu (mariposa) |
|---|---|
| `sjmisc::frq(data, var)` | `frequency(data, var)` (Alias `fre()`) |
| `sjmisc::descr(data, var)` | `describe(data, var)` |
| `descr::crosstab(row, col)` | `crosstab(data, row, col, percentages = "row")` (`"col"`, `"total"`, `"all"`, `"none"`) |
| — | `summary(crosstab(...), residuals = TRUE)` für adjustierte standardisierte Residuen |
| `Hmisc::describe(data)` | `describe(data, everything())` oder `codebook(data)` für HTML (wird in Quarto eingebettet) |
| `summary(data)` | `describe(data, everything())` |
| `table(x, y)` (mit Tests) | `crosstab(data, x, y)` + `chi_square(data, x, y)` |
| `prop.table(table(x))` | `frequency(data, x)` zeigt rel. Häufigkeiten by default |
| `psych::describe()` (Kurtosis) | `describe(data, var, show = c("mean", "sd", "skew", "kurtosis"))` bzw. `show = "all"` |

**Gewichtet (0.7.4).** `describe()` und `frequency()` berichten N und Missing als Summen der Gewichte (wie SPSS `WEIGHT BY`); gewichtete Kreuztabellen runden Zellhäufigkeiten wie `/COUNT ROUND CELL`.

**Beispiel — gewichtete Häufigkeit:**
```r
# alt: drei Pakete kombiniert
allbus |> sjmisc::frq(eastwest, weights = wghtpew)

# neu
allbus |> frequency(eastwest, weights = wghtpew)
```

---

## 5 — Gewichtete Statistik (Einzelkennwerte)

| Alt | Neu (mariposa) |
|---|---|
| `sjstats::weighted_mean(x, w)` | `w_mean(data, var, weights = w)` |
| `sjstats::weighted_median(x, w)` | `w_median(data, var, weights = w)` |
| `sjstats::weighted_sd(x, w)` | `w_sd(data, var, weights = w)` |
| `sjstats::weighted_se(x, w)` | `w_se(data, var, weights = w)` |
| `weights::wtd.quantile(x, weights = w)` | `w_quantile(data, var, weights = w, probs = …)` |
| `weights::wtd.cor(x, y, w)` | `pearson_cor(data, x, y, weights = w)` |
| `Hmisc::wtd.var()` | `w_var(data, var, weights = w)` |
| — | `w_skew`, `w_kurtosis`, `w_iqr`, `w_range`, `w_modus` (neue Möglichkeiten) |

**Note.** mariposa rechnet SPSS-kongruent (z. B. ungerundete `sum(w)` im `t_test`, `floor(sum(w))` in `oneway_anova`) — siehe `vignette("survey-weights", package = "mariposa")`. Nicht überraschen lassen, wenn Output sich um Nachkommastellen von alten sjstats-Werten unterscheidet.

**Rückgabe (0.7.4).** Auf einen Datensatz angewendet, liefern die `w_*()`-Funktionen eine lange Tabelle (`Variable`, Statistik, N, Missing). Innerhalb von `summarise()` geben sie die nackte Zahl zurück — das ist die Standardform für Subgruppen-Tabellen.

---

## 6 — Hypothesentests

| Alt | Neu (mariposa) |
|---|---|
| `stats::chisq.test(x, y)` | `chi_square(data, x, y, weights = w)` |
| `sjstats::weighted_chisqtest()` | `chi_square(data, x, y, weights = w)` |
| `sjstats::crosstable_statistics()` | `chi_square(data, x, y)` — Phi und Cramérs V in `summary()`; Gamma nur bei zwei ordinalen Variablen |
| Effektgröße als Zahl | `cramers_v()`, `phi()`, `goodman_gamma()` geben seit 0.6.4 *nur die Zahl* zurück (keine Aliase für den Test) |
| `stats::t.test(x ~ g)` | `t_test(data, x, group = g, weights = w)` (Welch; `summary()` zeigt beide SPSS-Zeilen) |
| `stats::t.test(x, y, paired = TRUE)` | kein mariposa-Pendant — base R; nicht-parametrisch `wilcoxon_test(data, x, y)` |
| `stats::wilcox.test(y ~ g)` (unabhängig) | `mann_whitney(data, y, group = g)` |
| `stats::wilcox.test(x, y, paired = TRUE)` | `wilcoxon_test(data, x, y)` |
| `stats::aov(y ~ g)` | `oneway_anova(data, y, group = g, weights = w)` |
| `car::Anova()` (Typ III) | `factorial_anova(data, y, between = c(g1, g2))` / `ancova(data, y, between = g, covariate = z)` |
| `stats::kruskal.test()` | `kruskal_wallis(data, y, group = g)` |
| `stats::TukeyHSD()` | `oneway_anova(...) \|> tukey_test()` (Paare in `summary()`, Orientierung „(I) − (J)") |
| `stats::fisher.test()` | `fisher_test(data, row, col)` (2×2: Odds Ratio + KI) |
| `stats::mcnemar.test()` | `mcnemar_test(data, var1, var2)` |
| `car::leveneTest()` | `t_test(...) \|> levene_test()` bzw. `oneway_anova(...) \|> levene_test()` |
| `stats::shapiro.test()` / `nortest::lillie.test()` | `normality_test(data, var)` (KS mit Lilliefors + Shapiro-Wilk, ohne Gewichte) |

**Achtung `ancova()`.** Parameter Estimates nutzen seit 0.7.4 die SPSS-Kodierung mit der **letzten** Kategorie als Referenz — anders als `linear_regression()` (erste Kategorie).

---

## 7 — Korrelation

| Alt | Neu (mariposa) |
|---|---|
| `stats::cor(x, y)` | `pearson_cor(data, x, y)` |
| `Hmisc::rcorr()` (Matrix) | `pearson_cor(data, starts_with("pt"))` — Matrix in `summary()`; tidyselect-Muster vorher prüfen (`mm0*` erwischt auch `mm02r`) |
| `psych::corr.test()` | `pearson_cor(data, …, conf.level = 0.95)` |
| `stats::cor(method = "spearman")` | `spearman_rho(data, x, y)` |
| `stats::cor(method = "kendall")` | `kendall_tau(data, x, y)` |
| `ppcor::pcor.test()` | `partial_cor(data, x, y, controls = c(z1, z2), weights = w)` (numerische Kontrollvariablen) |

---

## 8 — Faktoranalyse, Reliabilität, Skalenbildung

| Alt | Neu (mariposa) |
|---|---|
| `psych::KMO()` + `psych::cortest.bartlett()` | in `efa()` integriert (gibt KMO + Bartlett im Output) |
| `psych::scree()` | aktuell: `efa()` zeigt Eigenwerte; Scree-Plot separat per ggplot2 |
| `psych::principal()` | `efa(data, …, extraction = "pca")` (Default) |
| `psych::fa()` | `efa(data, …, extraction = "ml")` |
| Rotation | `rotation = "varimax"` / `"oblimin"` / `"promax"` / `"none"` — SPSS-Algorithmen, kein GPArotation nötig |
| Ladungen, Kommunalitäten | `summary(efa(...))`; programmatisch `$loadings`, `$eigenvalues`, `$kmo$per_item`, `$bartlett` |
| `psych::alpha()` | `reliability(data, item1, item2, …)` (Cronbachs α + McDonalds ω; Item-Statistiken in `summary()`) |
| `psych::pomp()` | `pomps(x, scale_min = …, scale_max = …)` (Vektor-Funktion, in `mutate()`) |
| `semTools::reliability()` / `psych::omega()` | `reliability()` liefert ω aus einem Ein-Faktor-ML-Modell (ω nicht gegen SPSS geprüft) |

**Achtung `lavaan`.** `library(lavaan)` maskiert `mariposa::efa()`. lavaan im Buch nur mit Präfix aufrufen (`lavaan::cfa()`, `lavaan::fitMeasures()`, `semPlot::semPaths()`).

**Beispiel — Vertrauens-Skala:**
```r
# alt
psych::alpha(allbus[, paste0("pt0", 1:9)])

# neu
allbus |> reliability(pt01, pt02, pt03, pt04, pt06:pt12, weights = wghtpew)
```

---

## 9 — Regression

| Alt | Neu (mariposa) |
|---|---|
| `stats::lm(y ~ x, data, weights = w)` | `linear_regression(data, formula = y ~ x, weights = w)` |
| `stats::glm(y ~ x, family = binomial)` | `logistic_regression(data, formula = y ~ x)` |
| `easystats::model_parameters()` | `summary()` des mariposa-Modells (gibt B, SE, Beta, t, p, 95 %-KI) |
| `easystats::model_performance()` | `summary()` enthält R², adj. R², F; `broom::glance()` für AIC/BIC |
| `easystats::compare_performance()` | `anova(m1, m2)` auf identischem Fall-Set; Kennzahlen manuell tabellieren |
| `texreg::screenreg(m1, m2)` | `summary()` der Einzelmodelle; Export mit `write_xlsx(modell, "datei.xlsx")` |
| `car::vif()` | `summary()` — Tabelle *Collinearity Statistics* (Tolerance + VIF je Term), Spalten `Tolerance`/`VIF` in `$coef_table` |
| `margins::margins()` | `marginal_effects(logistic_model)` — AMEs in Prozentpunkten (Delta-Methode) |
| `glm(..., family = binomial)` mit 1/2-Codes | `logistic_regression()` akzeptiert jede zweiwertige AV; Codierung steht in *Dependent Variable Encoding* |

**Ergebnis-Export (0.7.4).** `as.data.frame()` / `tibble::as_tibble()` für alle Ergebnisklassen, `broom::tidy()` für alle Tests, `write_xlsx()` für Ergebnisse (Kreuztabellen im SPSS-Layout).

---

## 10 — Plotting

mariposa hat **bewusst keine Plot-Funktionen**. Alle Grafik-Wrapper aus sjPlot/corrplot/gridExtra werden durch direktes ggplot2 + patchwork ersetzt. Das ist didaktisch sauberer (Anfänger lernen die Grammatik der Grafik).

| Alt | Neu |
|---|---|
| `sjplot::plot_frq(data, var)` | `data \|> frequency(var) \|> as_tibble() \|> ggplot(aes(value, freq)) + geom_col()` |
| `sjplot::plot_grpfrq(data, var, group)` | `ggplot(data, aes(var, fill = group)) + geom_bar(position = "dodge")` |
| `sjplot::plot_likert()` | ggplot2 `geom_col()` mit `position = "stack"` und divergierender Farbskala (Helper-Funktion lokal definieren, falls mehrfach genutzt) |
| `sjplot::plot_xtab()` | `crosstab()` als Tabelle + ggplot2-Heatmap |
| `sjplot::plot_model()` | aktuell ggplot2-Eigenbau (Koeffizienten-Plot via `summary(model)` → tibble → `geom_pointrange`) |
| `sjplot::check_model()` | ggplot2-Eigenbau (Residuen vs. Fitted, QQ-Plot) — **Restbedarf** für automatisierte Diagnostik |
| `corrplot::corrplot()` | ggplot2 `geom_tile()` aus `pearson_cor()`-Output |
| `gridExtra::grid.arrange(p1, p2)` | `library(patchwork); p1 + p2` |
| `gridExtra::arrangeGrob()` | `patchwork::wrap_plots()` |

---

## 11 — Restbedarf (außerhalb tidyverse + mariposa)

Diese Pakete bleiben begründet drin, weil mariposa hier (Stand 0.7.4) bewusst nichts anbietet. `car` wird für VIF nicht mehr gebraucht (siehe Abschnitt 9):

- **`lavaan`** + **`semPlot`** — Konfirmatorische Faktorenanalyse, Strukturgleichungsmodelle (Kap. 8).
- **`patchwork`** — Multi-Plot-Komposition (Tidyverse-nahes Ersatz für gridExtra).
- **`broom`** — Modell-Output → Tibble. In Kap. 9 für `augment()` (Residuen-Diagnostik) und `tidy()` (Coefficient-Plot) als Brücke zwischen `lm`-Objekt und ggplot2. Gehört zur tidymodels-Familie und wird im Lehrtext explizit als „nicht Teil des Kern-Stacks, aber tidyverse-nah" eingeführt.
- **`haven`** — wird transitiv über mariposa benutzt; explizites `library(haven)` nur, wenn `as_factor()` direkt verwendet wird (eher nicht).

Alles andere fliegt raus.

---

## 12 — Verbotene Pattern

Wenn ein Migrator-Pass das im Code-Output produziert, ist es ein Style-Fehler:

- `library()` oder `require()` außerhalb des Setup-Chunks.
- `%>%` (außer in dem einen Lehrabschnitt in Kap. 2, der den Unterschied zu `|>` erklärt).
- `T` / `F` statt `TRUE` / `FALSE`.
- `detach("package:…")` als Konflikt-Workaround.
- `attach(data)`.
- `=` für Zuweisung (außer in Argumenten).
- `data.frame()` wenn `tibble()` möglich.
- `aggregate()` wenn `summarise(.by = …)` reicht.
- `gather()` / `spread()` — durch `pivot_longer()` / `pivot_wider()` ersetzen.
- `mutate_at()`, `mutate_all()`, `funs()` — durch `across()` / `pick()` ersetzen.

---

## 13 — Verifikations-Checkliste pro Migrationspass

Bevor ein Kapitel-PR durchgewinkt wird:

- [ ] Kein verbotenes Pattern aus Abschnitt 12 mehr im Code.
- [ ] Alle library()-Calls im zentralen Setup-Chunk in `index.Rmd` aufgehoben (oder Kapitel-Setup wenn unvermeidbar).
- [ ] Chunks rendern fehlerfrei (Validator-Pass).
- [ ] Outputs semantisch vergleichbar mit Alt-Version (Stichproben-Check).
- [ ] Frage→Code→Lesart-Struktur eingehalten (siehe `STYLE.md`).
- [ ] Callouts nach Schema gesetzt (`STYLE.md`).
- [ ] Lernziele am Kapitelanfang.
