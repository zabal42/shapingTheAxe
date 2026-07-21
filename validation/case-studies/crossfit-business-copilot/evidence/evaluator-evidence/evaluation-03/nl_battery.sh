#!/usr/bin/env bash
# Evaluator-generated natural-language adversarial battery.
# Applies the SAME set of tricky questions to whichever candidate CLI is given.
#
# Usage:
#   nl_battery.sh x /path/to/candidate-x     # Node CLI
#   nl_battery.sh y /path/to/candidate-y     # Python CLI
set -u
mode="$1"; root="$2"

ask() {
  if [ "$mode" = "x" ]; then
    ( cd "$root" && node src/cli.js "$1" )
  else
    ( cd "$root" && PYTHONPATH=src python3 -m copilot.cli "$1" )
  fi
}

questions=(
  "¿Qué entrenador consigue mayor fidelidad de clientes?"     # N1 unsupported (US-07)
  "Enséñame las clases con menos ocupación este mes."          # N2 paraphrase of lowest-occupancy (US-08)
  "¿Qué clases funcionan peor este mes?"                       # N3 paraphrase of lowest-occupancy
  "¿Cuáles son los horarios menos aprovechados?"              # N4 ambiguous slot wording
  "Compara las cancelaciones de este mes con el mes anterior." # N5 unsupported comparison metric
  "Compara la ocupación."                                      # N6 comparison with no periods
  "¿Qué usuarios llevan sin asistir?"                          # N7 inactivity, no threshold
  ""                                                           # N8 empty question
  "Dame las 2 clases con menor ocupación entre 2026-05-01 y 2026-05-31" # N9 explicit period+limit
)

i=1
for q in "${questions[@]}"; do
  echo "################## N$i: [$q]"
  ask "$q"
  echo ""
  i=$((i+1))
done
