# Migration Cheatsheet — RWorkshop 2026

**Zweck.** Verbindliches Mapping vom alten Funktions-Zoo (strengejacke, sjmisc, sjstats, sjlabelled, sjplot, descr, weights, psych, easystats, texreg, corrplot, gridExtra) auf das neue Zwei-Paket-Setup **tidyverse + mariposa**. Diese Datei ist der Vertrag, an den sich alle Kapitelmigrationen halten. Abweichungen nur mit Notiz hier unter „Restbedarf".

**Konventionen.**
- Pipe immer `|>` (native, R 4.6).
- Argumente in `snake_case`, Logik `TRUE`/`FALSE` (nie `T`/`F`).
- `library()` ausschließlich im Setup-Chunk, nie im Kapitel-Text.
- mariposa-Funktionen sind data-first und tidyselect-fähig — `data |> fn(var1, var2, weights = w)` ist die Standardform.

---

## 1 — Datenimport & -export

| Alt | Neu (mariposa) | Notiz |
|---|---|---|
| `sjlabelled::read_spss(file)` | `mariposa::read_spss(path)` | Identische Idee, SPSS-validiert, `tag.na = TRUE` als Default — Tagged NAs werden erhalten. |
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
| `sjlabelled::get_labels(x)` | `val_labels(data)` |
| `sjlabelled::set_na(x, na = c(-9, -42))` | `set_na(data, var, tag = TRUE)` |
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
allbus <- allbus |> set_na(sex, age, educ, tag = TRUE)
allbus <- allbus |> to_label(sex)
```

---

## 3 — Rekodierung & Transformation

| Alt | Neu (mariposa) |
|---|---|
| `sjmisc::rec(x, rec = "1=1; 2,3=2; else=NA")` | `rec(data, var, rules = "1=1; 2,3=2; else=NA")` |
| `sjmisc::to_dummy()` | `to_dummy(data, var)` |
| `dplyr::case_when()` (für simple Rekodierungen) | bleibt `case_when()` / neu `case_match()` |
| `scale(x)` / `sjmisc::std()` | `std(data, var)` (gewichtsfähig) |
| `sjmisc::center()` | `center(data, var)` |
| `sjmisc::row_means(data, var:var)` | `row_means(data, var1, var2, …, min_valid = 10)` |
| `psych::reverse.code()` | `rec(data, var, rules = "1=5; 2=4; 3=3; 4=2; 5=1")` |

**Wichtig.** `case_when()` hat seit dplyr 1.1 Lambda-Syntax und `case_match()` als Variante — beide bevorzugen, wo nicht-mariposa-Logik gemeint ist.

---

## 4 — Deskriptive Statistik

| Alt | Neu (mariposa) |
|---|---|
| `sjmisc::frq(data, var)` | `frequency(data, var)` (Alias `fre()`) |
| `sjmisc::descr(data, var)` | `describe(data, var)` |
| `descr::crosstab(row, col)` | `crosstab(data, row, col)` |
| `Hmisc::describe(data)` | `describe(data, everything())` oder `codebook(data)` für HTML |
| `summary(data)` | `describe(data, everything())` |
| `table(x, y)` (mit Tests) | `crosstab(data, x, y)` (Chi² wird optional ergänzt) |
| `prop.table(table(x))` | `frequency(data, x)` zeigt rel. Häufigkeiten by default |

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

---

## 6 — Hypothesentests

| Alt | Neu (mariposa) |
|---|---|
| `stats::chisq.test(x, y)` | `chi_square(data, x, y, weights = w)` |
| `sjstats::weighted_chisqtest()` | `chi_square(data, x, y, weights = w)` |
| `sjstats::crosstable_statistics()` | `chi_square(data, x, y)` (gibt φ, Cramérs V, Lambda direkt mit) |
| `stats::t.test(x ~ g)` | `t_test(data, x, group = g, weights = w)` |
| `stats::wilcox.test()` | `wilcoxon_test(data, var, group = g)` |
| `stats::aov(y ~ g)` | `oneway_anova(data, y, group = g, weights = w)` |
| `car::Anova()` (Typ III) | `factorial_anova(data, y, group = c(g1, g2))` |
| `stats::kruskal.test()` | `kruskal_wallis(data, y, group = g)` |
| `stats::TukeyHSD()` | `tukey_test(data, y, group = g)` |
| `stats::fisher.test()` | `fisher_test(data, x, y)` |
| `stats::mcnemar.test()` | `mcnemar_test(data, x, y)` |
| `car::leveneTest()` | `levene_test(data, y, group = g)` |

---

## 7 — Korrelation

| Alt | Neu (mariposa) |
|---|---|
| `stats::cor(x, y)` | `pearson_cor(data, x, y)` |
| `Hmisc::rcorr()` (Matrix) | `pearson_cor(data, starts_with("pt"))` |
| `psych::corr.test()` | `pearson_cor(data, …, conf.level = 0.95)` |
| `stats::cor(method = "spearman")` | `spearman_rho(data, x, y)` |
| `stats::cor(method = "kendall")` | `kendall_tau(data, x, y)` |

---

## 8 — Faktoranalyse, Reliabilität, Skalenbildung

| Alt | Neu (mariposa) |
|---|---|
| `psych::KMO()` + `psych::cortest.bartlett()` | in `efa()` integriert (gibt KMO + Bartlett im Output) |
| `psych::scree()` | aktuell: `efa()` zeigt Eigenwerte; Scree-Plot separat per ggplot2 |
| `psych::principal()` | `efa(data, …, method = "pca")` |
| `psych::fa()` | `efa(data, …, method = "ml")` (oder `"minres"`) |
| `psych::alpha()` | `reliability(data, item1, item2, …)` (Cronbachs α + Item-Statistiken) |
| `psych::pomp()` | `pomps(data, var)` |
| `semTools::reliability()` | `reliability()` (für klassisches α — CFA-basierte Reliability bleibt semTools-Restbedarf) |

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
| `easystats::model_parameters()` | `summary()` des mariposa-Modells (gibt Beta, SE, t/z, p, KI) |
| `easystats::model_performance()` | `summary()` enthält R², adj. R², F, AIC |
| `easystats::compare_performance()` | mehrere `linear_regression()`-Objekte vergleichen, manuell tabellieren |
| `texreg::screenreg(m1, m2)` | `summary()` der Einzelmodelle (Tabellen-Komposition aktuell offen — siehe Restbedarf) |
| `car::vif()` | aktuell **Restbedarf** (Diagnostik-Plots = ggplot2-Eigenbau) |

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

Diese Pakete bleiben begründet drin, weil mariposa hier (Stand 0.6.1) bewusst nicht anbietet:

- **`lavaan`** + **`semPlot`** — Konfirmatorische Faktorenanalyse, Strukturgleichungsmodelle (Kap. 5).
- **`patchwork`** — Multi-Plot-Komposition (Tidyverse-nahes Ersatz für gridExtra).
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
