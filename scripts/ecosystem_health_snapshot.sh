#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UTC_TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

count_tests_in_dir() {
  local dir="$1"
  if [[ ! -d "$dir" ]]; then
    echo 0
    return 0
  fi
  find "$dir" -type f -name "test_*.py" | wc -l | tr -d '[:space:]'
}

count_tests_under_tests_dirs() {
  local base_dir="$1"
  if [[ ! -d "$base_dir" ]]; then
    echo 0
    return 0
  fi
  find "$base_dir" -type f -path '*/tests/*' -name 'test_*.py' | wc -l | tr -d '[:space:]'
}

total_tests="$(count_tests_under_tests_dirs "$ROOT")"
root_tests="$(count_tests_in_dir "$ROOT/tests")"
operator_tests="$(count_tests_in_dir "$ROOT/agents/operator-agent/tests")"
test_agent_tests="$(count_tests_in_dir "$ROOT/agents/test-agent/tests")"
lam_nested_tests="$(count_tests_under_tests_dirs "$ROOT/agents/test-agent/LAM_Test/agents")"

cat <<EOF
{
  "ts_utc": "$UTC_TS",
  "repo_root": "$ROOT",
  "runtime_scripts": [
    "scripts/aess_autostart.sh",
    "scripts/ecosystem_health_snapshot.sh",
    "scripts/ecosystem_soak.sh",
    "scripts/gateway_io.sh",
    "scripts/test_entrypoint.sh",
    "agents/test-agent/scripts/aess_autostart.sh",
    "agents/test-agent/scripts/bootstrap_submodules.sh",
    "agents/test-agent/scripts/gateway_io.sh",
    "agents/test-agent/scripts/test_entrypoint.sh",
    "agents/test-agent/LAM_Test/agents/codex-agent/run_tests_wsl.sh"
  ],
  "test_inventory": {
    "total_test_files": $total_tests,
    "root_tests": $root_tests,
    "operator_agent_tests": $operator_tests,
    "test_agent_tests": $test_agent_tests,
    "lam_nested_agent_tests": $lam_nested_tests
  }
}
EOF
