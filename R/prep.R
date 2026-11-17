# Reproduzierbare Datenpraep-Pipeline der Mini-Studie.
# Siehe Kap. 5 (Abschnitt "Die komplette Datenpraep-Pipeline") und
# STUDIE.md Abschnitt 3. Per source("R/prep.R") in jedem
# Methoden-Kapitel eingebunden, damit jedes .qmd-File eigenstaendig
# rendert (STYLE.md Abschnitt 8).
#
# Voraussetzungen: tidyverse und mariposa sind im Setup-Chunk geladen.

allbus <- read_spss("ALLBUS2023.sav") |>
  mutate(
    mm02r = rec(mm02, rules = "rev"),
    mm05r = rec(mm05, rules = "rev"),
    pa29r = rec(pa29, rules = "rev"),
    pa30r = rec(pa30, rules = "rev"),
    pa31r = rec(pa31, rules = "rev"),
    pa32r = rec(pa32, rules = "rev"),
    pa33r = rec(pa33, rules = "rev"),
    pa34r = rec(pa34, rules = "rev"),
    pa35r = rec(pa35, rules = "rev")
  ) |>
  mutate(
    islamophobie   = row_means(pick(mm01, mm02r, mm03, mm04, mm05r, mm06),
                               min_valid = 5),
    populismus     = row_means(pick(pa29r, pa30r, pa31r, pa32r, pa33r, pa34r, pa35r),
                               min_valid = 6),
    islamophobie_p = pomps(islamophobie, scale_min = 1, scale_max = 7),
    populismus_p   = pomps(populismus,   scale_min = 1, scale_max = 5)
  )
