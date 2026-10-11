#!/usr/bin/env bash
# Rebuild every table and figure of the paper from the raw NetFlow v3 CSVs (GUARDRAILS B1/B2).
#
#   ./run_all.sh            # everything, in order (~10 h on an 8-core laptop; keep it on AC power)
#   ./run_all.sh e3 e5      # only the named stages (each stage needs the ones before it to have run once)
#
# Stages: data e1 e2 e3 e3shared e4 e5 ablation. Expects data/raw/{cic,unsw,ton,bot}_*.csv (see README).
# Long stages (e2, e3, e3shared) checkpoint after every seed and resume if re-run.
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-.venv/bin/python}
mkdir -p results
STAGES=("$@")
[ ${#STAGES[@]} -eq 0 ] && STAGES=(data e1 e2 e3 e3shared e4 e5 ablation)

run() {                       # run <log name> <script + args>: tee output into results/<log>_log.txt
  local log=$1; shift
  echo "== $(date +%H:%M) $*"
  "$PY" "$@" 2>&1 | tee "results/${log}_log.txt"
}

for s in "${STAGES[@]}"; do
  case $s in
    data)     run data     src/data_loader.py build
              run families src/data_loader.py families                  # attack-family sidecars for E5
              run dataset_table src/dataset_table.py ;;                 # Table 1
    e1)       run e1       src/e1_fewshot.py ;;                          # ~40 min: CIC<->UNSW, RF, ±TTL
    e2)       run e2       src/e2_transfer.py ;;                         # ~30 min: CIC<->UNSW, 3 models x 4 methods
    e3)       run e2_all   src/e2_transfer.py --datasets cic unsw ton bot --out all   # ~3 h: 12 pairs
              run e3       src/e3_analysis.py ;;
    e3shared) run e2_shared src/e2_transfer.py --datasets cic unsw ton bot --scaling shared --out all_shared  # ~2.5 h
              run e3_shared src/e3_analysis.py --tag shared ;;
    e4)       run e4       src/e4_checks.py all ;;                       # ~30 min: Atif & Ali zero-shot, TAN-IDS budget
    e5)       run e5       src/e5_mechanism.py all ;;                    # ~2.5 h: domain distance, attack families
    ablation) run e5_ablation src/e5_ablation.py ;;                      # ~1.2 h: greedy feature ablation
    *)        echo "unknown stage: $s (use: data e1 e2 e3 e3shared e4 e5 ablation)"; exit 1 ;;
  esac
done
echo "== $(date +%H:%M) done; outputs in results/"
