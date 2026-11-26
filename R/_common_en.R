# Setup fuer die englische Fassung des Buchs.
# Die englischen Kapitel zeigen im Code read_spss("ALLBUS2023.sav"),
# lesen im Projekt aber die englische Datei (ALLBUS ZA8833).
# Die Funktion liegt im globalen Environment und verdeckt daher
# mariposa::read_spss auch nach einem spaeteren library(mariposa).

source("R/_common.R")

read_spss <- function(path, ...) {
  if (identical(path, "ALLBUS2023.sav")) {
    path <- "ALLBUS2023_en.sav"
  }
  mariposa::read_spss(path, ...)
}
