#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# AI-Compass macOS All-in-One
# - Creates/updates .env (interactive)
# - Ensures Homebrew + Python + PostgreSQL
# - Creates/uses .venv, installs requirements
# - Creates DB user/db (idempotent)
# - Runs Alembic migrations
# - Starts FastAPI (uvicorn) + Streamlit (same terminal, deterministic)
#
# Usage:
#   ./macos_all_in_one.sh
# Optional env overrides:
#   STREAMLIT_PORT=8501 API_PORT=8000
# ==============================================================================

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

print_step(){ echo ""; echo -e "${GREEN}▶ $1${NC}"; echo "────────────────────────────────────────"; }
ok(){ echo -e "${GREEN}✓ $1${NC}"; }
warn(){ echo -e "${YELLOW}⚠ $1${NC}"; }
fail(){ echo -e "${RED}✗ $1${NC}"; exit 1; }

command_exists(){ command -v "$1" &>/dev/null; }

# ------------------------------------------------------------------------------
# 0) Preflight
# ------------------------------------------------------------------------------
print_step "Preflight"
[[ "$OSTYPE" == "darwin"* ]] || fail "This script is macOS only."

[[ -f "README.md" && -d "apps/api" && -d "apps/web" ]] || fail "Run from ai-compass root directory."
ok "Repo root detected: $ROOT_DIR"

# ------------------------------------------------------------------------------
# 1) Homebrew
# ------------------------------------------------------------------------------
print_step "Homebrew"
if ! command_exists brew; then
  warn "Homebrew not found. Installing..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  if [[ "$(uname -m)" == "arm64" ]]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
    grep -q 'brew shellenv' ~/.zprofile 2>/dev/null || echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
  fi
  ok "Homebrew installed"
else
  ok "Homebrew found"
  brew update >/dev/null || true
fi

# ------------------------------------------------------------------------------
# 2) Python
# ------------------------------------------------------------------------------
print_step "Python"
if ! command_exists python3; then
  warn "python3 not found. Installing python..."
  brew install python >/dev/null
fi

PY_OK="no"
python3 - <<'PY' >/dev/null 2>&1 && PY_OK="yes" || PY_OK="no"
import sys
major, minor = sys.version_info[:2]
assert (major, minor) >= (3, 10)
PY

if [[ "$PY_OK" != "yes" ]]; then
  warn "Python >= 3.10 required. Installing python@3.11..."
  brew install python@3.11 >/dev/null || true
  brew link --overwrite python@3.11 >/dev/null 2>&1 || true
fi

PY_VER="$(python3 --version 2>/dev/null || true)"
ok "Using $PY_VER"

python3 -m pip install --upgrade pip >/dev/null
ok "pip upgraded"

# ------------------------------------------------------------------------------
# 3) PostgreSQL
# ------------------------------------------------------------------------------
print_step "PostgreSQL"
if ! command_exists psql; then
  warn "psql not found. Installing PostgreSQL..."
  brew install postgresql >/dev/null
fi

# Start service (best-effort)
if command_exists brew; then
  brew services start postgresql >/dev/null 2>&1 || brew services restart postgresql >/dev/null 2>&1 || true
fi

if ! command_exists psql; then
  fail "PostgreSQL install/start failed (psql still missing)."
fi
ok "PostgreSQL available: $(psql --version | head -n1)"

# ------------------------------------------------------------------------------
# 4) Config Wizard (.env)
# ------------------------------------------------------------------------------
print_step "Config (.env)"
if [[ -f ".env" ]]; then
  warn ".env already exists."
  read -p "Overwrite .env? (y/N): " -r REPLY
  if [[ ! "$REPLY" =~ ^[Yy]$ ]]; then
    ok "Keeping existing .env"
  else
    cp .env .env.backup
    ok "Backup created: .env.backup"
    rm -f .env
  fi
fi

# If .env missing, create interactively
if [[ ! -f ".env" ]]; then
  echo -e "${CYAN}Enter PostgreSQL settings (defaults in brackets).${NC}"

  read -p "DB user [aicompass_user]: " DB_USER
  DB_USER="${DB_USER:-aicompass_user}"

  while true; do
    read -s -p "DB password [aicompass_pass]: " DB_PASS
    echo ""
    if [[ -z "$DB_PASS" ]]; then DB_PASS="aicompass_pass"; break; fi
    read -s -p "Confirm password: " DB_PASS2
    echo ""
    [[ "$DB_PASS" == "$DB_PASS2" ]] && break
    echo -e "${RED}Passwords do not match.${NC}"
  done

  read -p "DB name [aicompass]: " DB_NAME
  DB_NAME="${DB_NAME:-aicompass}"

  read -p "DB host [localhost]: " DB_HOST
  DB_HOST="${DB_HOST:-localhost}"

  read -p "DB port [5432]: " DB_PORT
  DB_PORT="${DB_PORT:-5432}"

  echo ""
  echo -e "${CYAN}Groq API Key (starts with gsk_). You can skip.${NC}"
  read -p "GROQ_API_KEY: " GROQ_API_KEY
  if [[ -z "${GROQ_API_KEY:-}" ]]; then
    GROQ_API_KEY="your_groq_api_key_here"
    warn "Groq key not set. App may run, but LLM features won’t work."
  fi

  DATABASE_URL="postgresql://${DB_USER}:${DB_PASS}@${DB_HOST}:${DB_PORT}/${DB_NAME}"

  cat > .env <<EOF
# Generated by macos_all_in_one.sh on $(date)
DATABASE_URL=${DATABASE_URL}
GROQ_API_KEY=${GROQ_API_KEY}
ENVIRONMENT=development
LOG_LEVEL=INFO
QUESTIONNAIRE_PATH=data/questionnaire.json
EOF

  ok ".env created"
else
  ok ".env present"
fi

# Load env vars for this script run
set -a
# shellcheck disable=SC1091
source "$ROOT_DIR/.env"
set +a

# Parse DB settings from DATABASE_URL (simple parse; expects standard format)
DB_USER_FROM_URL="$(python3 - <<'PY'
import os, re
url=os.environ.get("DATABASE_URL","")
m=re.match(r"postgresql:\/\/([^:]+):([^@]+)@([^:]+):(\d+)\/(.+)", url)
print(m.group(1) if m else "")
PY
)"
DB_PASS_FROM_URL="$(python3 - <<'PY'
import os, re
url=os.environ.get("DATABASE_URL","")
m=re.match(r"postgresql:\/\/([^:]+):([^@]+)@([^:]+):(\d+)\/(.+)", url)
print(m.group(2) if m else "")
PY
)"
DB_HOST_FROM_URL="$(python3 - <<'PY'
import os, re
url=os.environ.get("DATABASE_URL","")
m=re.match(r"postgresql:\/\/([^:]+):([^@]+)@([^:]+):(\d+)\/(.+)", url)
print(m.group(3) if m else "")
PY
)"
DB_PORT_FROM_URL="$(python3 - <<'PY'
import os, re
url=os.environ.get("DATABASE_URL","")
m=re.match(r"postgresql:\/\/([^:]+):([^@]+)@([^:]+):(\d+)\/(.+)", url)
print(m.group(4) if m else "")
PY
)"
DB_NAME_FROM_URL="$(python3 - <<'PY'
import os, re
url=os.environ.get("DATABASE_URL","")
m=re.match(r"postgresql:\/\/([^:]+):([^@]+)@([^:]+):(\d+)\/(.+)", url)
print(m.group(5) if m else "")
PY
)"

if [[ -z "$DB_USER_FROM_URL" || -z "$DB_NAME_FROM_URL" ]]; then
  fail "DATABASE_URL in .env has unexpected format. Expected: postgresql://user:pass@host:port/db"
fi

# ------------------------------------------------------------------------------
# 5) Create / use .venv + install requirements
# ------------------------------------------------------------------------------
print_step "Python virtualenv (.venv) + dependencies"
if [[ ! -d ".venv" ]]; then
  python3 -m venv .venv
  ok ".venv created"
else
  ok ".venv exists"
fi

# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install -r requirements.txt
ok "Dependencies installed"

export PYTHONPATH="$ROOT_DIR:$ROOT_DIR/apps/api"

# ------------------------------------------------------------------------------
# 6) DB bootstrap (idempotent)
# ------------------------------------------------------------------------------
print_step "Database bootstrap (user/db)"
# Escape single quotes for SQL password literal
DB_PASS_SQL="${DB_PASS_FROM_URL//\'/\'\'}"

SQL=$(cat <<EOF
DO \$\$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = '${DB_USER_FROM_URL}') THEN
    CREATE ROLE ${DB_USER_FROM_URL} LOGIN PASSWORD '${DB_PASS_SQL}';
  END IF;
END
\$\$;

DO \$\$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = '${DB_NAME_FROM_URL}') THEN
    CREATE DATABASE ${DB_NAME_FROM_URL} OWNER ${DB_USER_FROM_URL};
  END IF;
END
\$\$;

GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME_FROM_URL} TO ${DB_USER_FROM_URL};
EOF
)

# Try to run against local postgres. On macOS this usually works with current user.
if psql -h "$DB_HOST_FROM_URL" -p "$DB_PORT_FROM_URL" -d postgres -c "SELECT 1" >/dev/null 2>&1; then
  echo "$SQL" | psql -h "$DB_HOST_FROM_URL" -p "$DB_PORT_FROM_URL" -d postgres >/dev/null
  ok "DB user/db ensured: ${DB_USER_FROM_URL} / ${DB_NAME_FROM_URL}"
else
  warn "Could not connect to postgres for bootstrap (auth/role issue)."
  warn "You may need to create role/db manually, then rerun this script."
fi

# ------------------------------------------------------------------------------
# 7) Alembic migrations
# ------------------------------------------------------------------------------
print_step "Alembic migrations"
if [[ -d "apps/api/alembic" ]]; then
  (cd apps/api && alembic upgrade head) || warn "Alembic upgrade failed. Check apps/api config & DB connectivity."
  ok "Migrations attempted"
else
  warn "No apps/api/alembic directory found. Skipping migrations."
fi

# ------------------------------------------------------------------------------
# 8) Start services (deterministic, same terminal)
# ------------------------------------------------------------------------------
print_step "Start services"
STREAMLIT_PORT="${STREAMLIT_PORT:-8501}"
API_PORT="${API_PORT:-8000}"

# Port sanity check (best-effort)
if command_exists lsof; then
  if lsof -nP -iTCP:"$STREAMLIT_PORT" -sTCP:LISTEN >/dev/null 2>&1; then
    fail "Port $STREAMLIT_PORT already in use. Stop the other process or change STREAMLIT_PORT."
  fi
  if lsof -nP -iTCP:"$API_PORT" -sTCP:LISTEN >/dev/null 2>&1; then
    fail "Port $API_PORT already in use. Stop the other process or change API_PORT."
  fi
fi

# Start API in background
( cd "$ROOT_DIR" && uvicorn apps.api.main:app --host 127.0.0.1 --port "$API_PORT" --reload ) &
API_PID=$!

cleanup() {
  echo ""
  echo "Stopping API (pid=$API_PID)..."
  kill "$API_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

echo ""
echo -e "${GREEN}AI-Compass running:${NC}"
echo "  Streamlit: http://localhost:${STREAMLIT_PORT}"
echo "  API:       http://localhost:${API_PORT}"
echo "  Docs:      http://localhost:${API_PORT}/docs"
echo ""

# Streamlit in foreground
streamlit run "$ROOT_DIR/apps/web/Home.py" --server.address 127.0.0.1 --server.port "$STREAMLIT_PORT"
