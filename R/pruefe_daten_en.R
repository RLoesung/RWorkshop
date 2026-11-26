# Vergleicht ALLBUS2023.sav (ZA8831, deutsch) mit ALLBUS2023_en.sav (ZA8833,
# englisch): Fallzahl, Variablen, Wertecodes. Gibt nur Zusammenfassungen aus,
# keine Datenwerte und keine Labeltexte.
# Aufruf aus dem Projektordner: Rscript R/pruefe_daten_en.R
# Endet mit Status 1, wenn Abweichungen auftreten, die nicht als bekannt ausgewiesen sind.

# user_na = TRUE liest die benutzerdefinierten Missing-Werte (na_values, na_range) mit.
de <- haven::read_sav("ALLBUS2023.sav", user_na = TRUE)
en <- haven::read_sav("ALLBUS2023_en.sav", user_na = TRUE)

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

# Bekannte Abweichungen der Wertecodes:
# - za_nr: die Studiennummer ist 8831 bzw. 8833.
# - isco08a: ZA8833 hat zusaetzliche Wertelabels; alle deutschen Codes sind enthalten.
bekannt_codes <- character()
if ("za_nr" %in% codes_abw) bekannt_codes <- c(bekannt_codes, "za_nr")
if ("isco08a" %in% codes_abw &&
    length(setdiff(codes(de[["isco08a"]]), codes(en[["isco08a"]]))) == 0) {
  bekannt_codes <- c(bekannt_codes, "isco08a")
}
cat("  davon bekannt:", length(bekannt_codes),
    if (length(bekannt_codes)) paste(bekannt_codes, collapse = ", "), "\n")
unerwartet_codes <- setdiff(codes_abw, bekannt_codes)
if (length(unerwartet_codes)) abweichungen <- c(abweichungen, unerwartet_codes)

# Benutzerdefinierte Missing-Werte: ZA8833 hat keine, ZA8831 setzt na_range.
# Die englische Fassung deklariert sie im Buch mit set_na(); das ist bekannt.
anzahl <- function(d, a) sum(vapply(d, function(x) !is.null(attr(x, a)), logical(1)))
for (a in c("na_values", "na_range")) {
  cat(sprintf("%-10s Variablen: de = %d  en = %d\n", a, anzahl(de, a), anzahl(en, a)))
  if (anzahl(en, a) == 0) {
    if (anzahl(de, a) > 0) cat("  bekannt: ZA8833 definiert", a, "nicht\n")
  } else {
    abw <- gemeinsam[!vapply(gemeinsam, function(v) {
      identical(attr(de[[v]], a), attr(en[[v]], a))
    }, logical(1))]
    cat("  Variablen mit abweichendem", a, ":", length(abw), "\n")
    if (length(abw)) abweichungen <- c(abweichungen, paste0(a, ":", abw))
  }
}

if (length(abweichungen)) {
  cat("ABWEICHUNGEN:", paste(abweichungen, collapse = ", "), "\n")
  quit(status = 1)
} else {
  cat("ok: keine unerwarteten Abweichungen\n")
}
