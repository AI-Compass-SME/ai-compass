#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# mac_start.sh (macOS)
# Starts FastAPI (uvicorn) + Streamlit using the project's .venv
#
# Usage:
#   bash mac_start.sh
#   bash mac_start.sh --background
#
# Optional env overrides:
#   API_HOST=127.0.0.1 API_PORT=8000 UI_HOST=127.0.0.1 UI_PORT=8501
# ==============================================================================

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

ok(){ echo -e "${GREEN}✓ $1${NC}"; }
info(){ echo -e "${BLUE}▶ $1${NC}"; }
warn(){ echo -e "${YELLOW}⚠ $1${NC}"; }
fail(){ echo -e "${RED}✗ $1${NC}"; exit 1; }

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

# --- Preflight ---
[[ "$OSTYPE" == "darwin"* ]] || fail "This script is for macOS only."
[[ -f "README.md" && -d "apps/api" && -d "apps/web" ]] || fail "Run this script from the ai-compass root directory."

[[ -d ".venv" ]] || fail ".venv not found. Run your macos_app_config_setup.sh (or setup) first."
# shellcheck disable=SC1091
source ".venv/bin/activate"
ok "Activated virtualenv: .venv"

# --- Config ---
API_HOST="${API_HOST:-127.0.0.1}"
API_PORT="${API_PORT:-8000}"
UI_HOST="${UI_HOST:-127.0.0.1}"
UI_PORT="${UI_PORT:-8501}"

export PYTHONPATH="$ROOT_DIR:$ROOT_DIR/apps/api"
ok "PYTHONPATH set"

# --- Port checks (best-effort) ---
if command -v lsof >/dev/null 2>&1; then
  if lsof -nP -iTCP:"$API_PORT" -sTCP:LISTEN >/dev/null 2>&1; then
    fail "API port $API_PORT is already in use. Stop the process or change API_PORT."
  fi
  if lsof -nP -iTCP:"$UI_PORT" -sTCP:LISTEN >/dev/null 2>&1; then
    fail "UI port $UI_PORT is already in use. Stop the process or change UI_PORT."
  fi
else
  warn "lsof not found; skipping port checks."
fi

API_LOG="$ROOT_DIR/api.log"
UI_LOG="$ROOT_DIR/streamlit.log"
PID_FILE="$ROOT_DIR/.mac_start.pids"

start_api() {
  (
    cd "$ROOT_DIR" && \
    uvicorn apps.api.main:app --host "$API_HOST" --port "$API_PORT" --reload
  )
}

start_ui() {
  streamlit run "$ROOT_DIR/apps/web/Home.py" \
    --server.address "$UI_HOST" \
    --server.port "$UI_PORT"
}

cleanup() {
  echo ""
  info "Stopping services..."
  if [[ -f "$PID_FILE" ]]; then
    # shellcheck disable=SC1090
    source "$PID_FILE" || true
    [[ -n "${API_PID:-}" ]] && kill "$API_PID" 2>/dev/null || true
    [[ -n "${UI_PID:-}"  ]] && kill "$UI_PID"  2>/dev/null || true
    rm -f "$PID_FILE" || true
  fi
  ok "Stopped."
}

# --- Mode ---
if [[ "${1:-}" == "--background" ]]; then
  info "Starting in background (logs: api.log, streamlit.log)"

  # Start API
  ( start_api ) >"$API_LOG" 2>&1 &
  API_PID=$!

  # Give API a moment (optional)
  sleep 1

  # Start UI
  ( start_ui ) >"$UI_LOG" 2>&1 &
  UI_PID=$!

  cat >"$PID_FILE" <<EOF
API_PID=$API_PID
UI_PID=$UI_PID
EOF

  ok "Started."
  echo ""
  echo -e "${GREEN}URLs:${NC}"
  echo "  Streamlit: http://localhost:${UI_PORT}"
  echo "  API:       http://localhost:${API_PORT}"
  echo "  Docs:      http://localhost:${API_PORT}/docs"
  echo ""
  echo "Stop:"
  echo "  bash -c 'source \"$PID_FILE\" && kill \$API_PID \$UI_PID' 2>/dev/null || true"
  echo "Logs:"
  echo "  tail -f \"$API_LOG\""
  echo "  tail -f \"$UI_LOG\""
  exit 0
fi

# Foreground mode: API background, Streamlit foreground
trap cleanup EXIT INT TERM

info "Starting FastAPI (background)..."
( start_api ) &
API_PID=$!

cat >"$PID_FILE" <<EOF
API_PID=$API_PID
EOF

echo ""
echo -e "${GREEN}URLs:${NC}"
echo "  Streamlit: http://localhost:${UI_PORT}"
echo "  API:       http://localhost:${API_PORT}"
echo "  Docs:      http://localhost:${API_PORT}/docs"
echo ""
info "Starting Streamlit (foreground)... (Ctrl+C stops everything)"

start_ui
