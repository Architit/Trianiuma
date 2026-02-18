#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ITERATIONS="${1:-3}"
PYTHON_BIN=""
LOG_PREFIX="${SOAK_LOG_PREFIX:-ecosystem_soak_run}"

if ! [[ "$ITERATIONS" =~ ^[0-9]+$ ]] || [[ "$ITERATIONS" -lt 1 ]]; then
  echo "usage: $0 [iterations>=1]" >&2
  exit 2
fi

resolve_python() {
  local candidates=(
    "$ROOT/.venv/bin/python"
    "${ECO_PYTHON_BIN:-}"
    "python3"
  )
  local candidate
  for candidate in "${candidates[@]}"; do
    [[ -z "$candidate" ]] && continue
    if [[ "$candidate" == */* ]]; then
      if [[ -x "$candidate" ]] && "$candidate" -c "import pytest" >/dev/null 2>&1; then
        echo "$candidate"
        return 0
      fi
      continue
    fi
    if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c "import pytest" >/dev/null 2>&1; then
      echo "$candidate"
      return 0
    fi
  done
  return 1
}

PYTHON_BIN="$(resolve_python || true)"
if [[ -z "$PYTHON_BIN" ]]; then
  echo "[ecosystem-soak] pytest unavailable" >&2
  exit 2
fi

if [[ -n "${SOAK_TEST_ARGS:-}" ]]; then
  read -r -a TEST_ARGS <<< "${SOAK_TEST_ARGS}"
else
  TEST_ARGS=(
    agents/operator-agent/tests
    agents/test-agent/tests
    agents/test-agent/LAM_Test/agents/operator-agent/tests
    agents/test-agent/LAM_Test/agents/comm-agent/tests
    agents/test-agent/LAM_Test/agents/codex-agent/tests
    tests
  )
fi

last_summary=""
status="ok"
exit_code=0
tmp_logs=()
cleanup() {
  local f
  for f in "${tmp_logs[@]}"; do
    rm -f "$f"
  done
}
trap cleanup EXIT

for ((i=1; i<=ITERATIONS; i++)); do
  log_file="$(mktemp "/tmp/${LOG_PREFIX}_${i}_XXXXXX.log")"
  tmp_logs+=("$log_file")
  if (
    cd "$ROOT"
    "$PYTHON_BIN" -m pytest -q "${TEST_ARGS[@]}"
  ) >"$log_file" 2>&1; then
    :
  else
    exit_code=$?
    status="fail"
  fi
  last_summary="$(tail -n 1 "$log_file" | tr -d '\r')"
  if [[ "$status" != "ok" ]]; then
    break
  fi
done

last_summary_json="$(printf '%s' "$last_summary" | "$PYTHON_BIN" -c 'import json,sys; print(json.dumps(sys.stdin.read()))')"

cat <<EOF
{
  "ts_utc": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "repo_root": "$ROOT",
  "iterations": $ITERATIONS,
  "status": "$status",
  "exit_code": $exit_code,
  "last_summary": $last_summary_json
}
EOF

if [[ "$status" != "ok" ]]; then
  exit "$exit_code"
fi
