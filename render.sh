#!/bin/sh
# Baut beide Sprachfassungen: erst Deutsch (docs/), dann Englisch (docs/en/).
# Die Reihenfolge ist wichtig: ein vollständiger deutscher Build leert docs/ samt docs/en/.
# Einzelkapitel: quarto render X.qmd   bzw.   quarto render X.en.qmd --profile en
set -e
cd "$(dirname "$0")"
if command -v quarto >/dev/null 2>&1; then
  Q=quarto
else
  Q=/Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto
fi
"$Q" render
"$Q" render --profile en
