# Reproduzierbare Datenpraep-Pipeline der Mini-Studie.
# Siehe Kap. 4 (Abschnitt "Die komplette Datenpraep-Pipeline") und
# STUDIE.md Abschnitt 3. Per source("R/prep.R") in jedem
# Methoden-Kapitel eingebunden, damit jedes .qmd-File eigenstaendig
# rendert (STYLE.md Abschnitt 8).
#
# Voraussetzungen: tidyverse und mariposa sind im Setup-Chunk geladen.

allbus <- read_spss("ALLBUS2023.sav") |>
  rec(mm02, rules = "rev", suffix = "r") |>
  rec(mm05, rules = "rev", suffix = "r") |>
  rec(pa29, rules = "rev", suffix = "r") |>
  rec(pa30, rules = "rev", suffix = "r") |>
  rec(pa31, rules = "rev", suffix = "r") |>
  rec(pa32, rules = "rev", suffix = "r") |>
  rec(pa33, rules = "rev", suffix = "r") |>
  rec(pa34, rules = "rev", suffix = "r") |>
  rec(pa35, rules = "rev", suffix = "r") |>
  mutate(
    islamophobie   = row_means(pick(mm01, mm02r, mm03, mm04, mm05r, mm06),
                               min_valid = 5),
    populismus     = row_means(pick(pa29r, pa30r, pa31r, pa32r, pa33r, pa34r, pa35r),
                               min_valid = 6),
    islamophobie_p = pomps(islamophobie, scale_min = 1, scale_max = 7),
    populismus_p   = pomps(populismus,   scale_min = 1, scale_max = 5)
  )
