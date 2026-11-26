# Vergleicht ALLBUS2023.sav (ZA8831, deutsch) mit ALLBUS2023_en.sav (ZA8833,
# englisch): Fallzahl, Variablen, Wertecodes. Gibt nur Zusammenfassungen aus,
# keine Datenwerte und keine Labeltexte.
# Aufruf aus dem Projektordner: Rscript R/pruefe_daten_en.R

de <- haven::read_sav("ALLBUS2023.sav")
en <- haven::read_sav("ALLBUS2023_en.sav")

abweichungen <- character()

cat("Faelle:     de =", nrow(de), " en =", nrow(en), "\n")
cat("Variablen:  de =", ncol(de), " en =", ncol(en), "\n")
if (nrow(de) != nrow(en)) abweichungen <- c(abweichungen, "Fallzahl")
if (ncol(de) != ncol(en)) abweichungen <- c(abweichungen, "Variablenzahl")

nur_de <- setdiff(names(de), names(en))
nur_en <- setdiff(names(en), names(de))
cat("Namen nur in de:", length(nur_de), if (length(nur_de)) paste(nur_de, collapse = ", "), "\n")
cat("Namen nur in en:", length(nur_en), if (length(nur_en)) paste(nur_en, collapse = ", "), "\n")
if (length(nur_de) || length(nur_en)) abweichungen <- c(abweichungen, "Variablennamen")

codes <- function(x) {
  l <- attr(x, "labels")
  if (is.null(l)) numeric() else sort(unname(as.numeric(l)))
}
gemeinsam <- intersect(names(de), names(en))
codes_abw <- gemeinsam[!vapply(gemeinsam, function(v) {
  identical(codes(de[[v]]), codes(en[[v]]))
}, logical(1))]
cat("Variablen mit abweichenden Wertecodes:", length(codes_abw),
    if (length(codes_abw)) paste(codes_abw, collapse = ", "), "\n")
if (length(codes_abw)) abweichungen <- c(abweichungen, codes_abw)

if (length(abweichungen)) {
  cat("ABWEICHUNGEN:", paste(abweichungen, collapse = ", "), "\n")
} else {
  cat("ok: keine Abweichungen\n")
}
