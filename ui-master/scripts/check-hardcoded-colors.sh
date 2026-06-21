#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-/Users/v/Work/workstation-ccc-mui}"

echo "[scan] ${ROOT}"
rg -n --no-heading --glob '!**/dist/**' --glob '!**/node_modules/**' \
  "#[0-9a-fA-F]{3,8}|rgba?\(|hsla?\(|border-radius:\s*[0-9]+px" \
  "${ROOT}/packages/apps/manage/src" "${ROOT}/packages/apps/agent-flow/src" || true

echo "[done]"
