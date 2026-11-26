# Test: R/prep_en.R reproduces the derived variables of R/prep.R.
# Run from the project root: Rscript R/test_prep_en.R
# Each pipeline runs in its own Rscript process, because R/_common_en.R
# defines a global read_spss() wrapper and sets the language; a shared
# session would redirect the German read as well. Results go through
# temporary .rds files. Only "ok" or variable names are printed, no data.

stopifnot(file.exists("R/prep.R"), file.exists("R/prep_en.R"))

# German name -> English name
map <- c(
  mm02r = "mm02r", mm05r = "mm05r",
  pa29r = "pa29r", pa30r = "pa30r", pa31r = "pa31r", pa32r = "pa32r",
  pa33r = "pa33r", pa34r = "pa34r", pa35r = "pa35r",
  islamophobie = "islamophobia", populismus = "populism",
  islamophobie_p = "islamophobia_p", populismus_p = "populism_p"
)

run_pipeline <- function(common, prep, vars, out) {
  code <- sprintf(
    paste0(
      "suppressMessages({library(tidyverse); library(mariposa)});",
      "source('%s'); source('%s');",
      "res <- lapply(setNames(nm = c(%s)), function(v)",
      "  as.numeric(haven::zap_labels(allbus[[v]])));",
      "res$.n <- nrow(allbus); saveRDS(res, '%s')"
    ),
    common, prep, paste0("'", vars, "'", collapse = ","), out
  )
  status <- system2("Rscript", c("-e", shQuote(code)), stdout = FALSE, stderr = FALSE)
  stopifnot(status == 0, file.exists(out))
  readRDS(out)
}

f_de <- tempfile(fileext = ".rds")
f_en <- tempfile(fileext = ".rds")
de <- run_pipeline("R/_common.R", "R/prep.R", names(map), f_de)
en <- run_pipeline("R/_common_en.R", "R/prep_en.R", unname(map), f_en)
unlink(c(f_de, f_en))

differs <- names(map)[!vapply(names(map), function(g) {
  isTRUE(all.equal(de[[g]], en[[map[[g]]]]))
}, logical(1))]
if (!identical(de$.n, en$.n)) differs <- c(differs, ".nrow")

if (length(differs) == 0) cat("ok\n") else cat("differ:", differs, "\n")
quit(status = as.integer(length(differs) > 0))
