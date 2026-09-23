#!/bin/sh
# Vor jedem Push laufen lassen.
#
# Drei Stellen muessen zusammenpassen, sonst merkt niemand etwas von der neuen
# Fassung -- oder schlimmer: die Update-Sperre schlaegt zu und geht nicht mehr
# weg, weil die ausgelieferte Datei eine andere Version meldet als erwartet.
#   1. <meta name="heribert-version"> in index.html  -> der Vergleichswert
#   2. oberster CHANGELOG-Eintrag (de und en)        -> was die Leute lesen
#   3. CACHE_VERSION in sw.js                        -> loest die Sperre sofort aus
set -e
cd "$(dirname "$0")"

META=$(sed -n 's/.*name="heribert-version" content="\([^"]*\)".*/\1/p' index.html | head -1)
# Jeweils der ERSTE Eintrag nach "de: [" bzw. "en: [" -- nicht einfach die
# ersten zwei Treffer im File, das sind sonst beides deutsche Eintraege.
CL_DE=$(awk '/^  de: \[/{f=1;next} f&&/version:"/{sub(/.*version:"/,"");sub(/".*/,"");print;exit}' index.html)
CL_EN=$(awk '/^  en: \[/{f=1;next} f&&/version:"/{sub(/.*version:"/,"");sub(/".*/,"");print;exit}' index.html)
SW=$(sed -n 's/.*CACHE_VERSION = "\([^"]*\)".*/\1/p' sw.js | head -1)
SW_ALT=$(git show origin/main:sw.js 2>/dev/null | sed -n 's/.*CACHE_VERSION = "\([^"]*\)".*/\1/p' | head -1)

echo "meta            : $META"
echo "CHANGELOG de/en : $CL_DE / $CL_EN"
echo "CACHE_VERSION   : $SW  (auf origin/main: ${SW_ALT:-?})"

FEHLER=0
[ -n "$META" ] || { echo "FEHLER: keine Versionsmarke in index.html"; FEHLER=1; }
[ "$META" = "$CL_DE" ] || { echo "FEHLER: Versionsmarke ($META) != CHANGELOG de ($CL_DE)"; FEHLER=1; }
[ "$CL_DE" = "$CL_EN" ] || { echo "FEHLER: CHANGELOG de ($CL_DE) != en ($CL_EN)"; FEHLER=1; }
if [ -n "$SW_ALT" ] && [ "$SW" = "$SW_ALT" ]; then
  echo "WARNUNG: CACHE_VERSION unveraendert -- laufende Apps merken die neue Fassung"
  echo "         erst beim naechsten Versions-Abgleich (bis zu 10 Minuten), nicht sofort."
fi
[ "$FEHLER" = 0 ] && echo "OK" || exit 1
