# Reproducible data preparation pipeline of the mini study (English edition).
# See Chapter 5 (section "The complete data preparation pipeline") and
# STUDIE.md section 3. Loaded with source("R/prep_en.R") in each
# methods chapter, so every .qmd file renders on its own.
#
# The English file ALLBUS2023_en.sav (ZA8833) declares no missing values.
# set_na() turns the negative codes into missing values (tagged NAs),
# as the German file does on import.
#
# Requirements: tidyverse and mariposa are loaded in the setup chunk.

allbus <- read_spss("ALLBUS2023.sav") |>
  set_na(-56, -55, -54, -53, -51, -50, -42, -41, -33, -32, -15, -11, -10, -9, -8, -7, -6) |>
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
    islamophobia   = row_means(pick(mm01, mm02r, mm03, mm04, mm05r, mm06),
                               min_valid = 5),
    populism       = row_means(pick(pa29r, pa30r, pa31r, pa32r, pa33r, pa34r, pa35r),
                               min_valid = 6),
    islamophobia_p = pomps(islamophobia, scale_min = 1, scale_max = 7),
    populism_p     = pomps(populism,     scale_min = 1, scale_max = 5)
  )
