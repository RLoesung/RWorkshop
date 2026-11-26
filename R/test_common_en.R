# Test fuer R/_common_en.R: Umleitung von ALLBUS2023.sav auf ALLBUS2023_en.sav.
# Arbeitet nur mit erfundenen Daten in einem Temp-Ordner.
# Aufruf aus dem Projektordner: Rscript R/test_common_en.R

projekt <- normalizePath(getwd())
tmp <- tempfile("common_en_")
dir.create(file.path(tmp, "R"), recursive = TRUE)
file.copy(file.path(projekt, "R", c("_common.R", "_common_en.R")),
          file.path(tmp, "R"))

haven::write_sav(data.frame(x = 1:3), file.path(tmp, "ALLBUS2023.sav"))
haven::write_sav(data.frame(x = 4:6), file.path(tmp, "ALLBUS2023_en.sav"))
haven::write_sav(data.frame(x = 7:9), file.path(tmp, "andere.sav"))

setwd(tmp)
source("R/_common_en.R")
library(mariposa)

stopifnot(
  identical(as.integer(read_spss("ALLBUS2023.sav")$x), 4:6),
  identical(as.integer(read_spss("andere.sav")$x), 7:9),
  identical(environment(read_spss), globalenv())
)
cat("ok\n")
