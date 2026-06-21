#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-manage}"
REPO="${2:-/Users/v/Work/workstation-ccc-mui}"

cd "${REPO}"

case "${TARGET}" in
  manage)
    pnpm --filter manage lint
    pnpm --filter manage build
    ;;
  agent-flow)
    pnpm --filter agent-flow lint
    pnpm --filter agent-flow test
    pnpm --filter agent-flow build
    ;;
  all)
    pnpm --filter manage lint
    pnpm --filter manage build
    pnpm --filter agent-flow lint
    pnpm --filter agent-flow test
    pnpm --filter agent-flow build
    ;;
  *)
    echo "usage: bash scripts/verify-visual-restore.sh [manage|agent-flow|all] [repo_path]"
    exit 2
    ;;
esac

echo "[ok] ${TARGET}"
