#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# create_db_macos.sh
# Creates (idempotent) Postgres role + database using ADMIN credentials
# Works on macOS when local Postgres requires password (md5/scram).
#
# - Reads DATABASE_URL from .env if present (recommended)
# - Otherwise asks interactively for target DB settings
# - Always asks for ADMIN username + password (hidden)
#
# Usage:
#   bash create_db_macos.sh
#
# Optional (non-interactive-ish for target DB):
#   DATABASE_URL="postgresql://appuser:apppass@localhost:5432/aicompass" bash create_db_macos.sh
# ==============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

ok(){ echo -e "${GREEN}✓ $1${NC}"; }
warn(){ echo -e "${YELLOW}⚠ $1${NC}"; }
fail(){ echo -e "${RED}✗ $1${NC}"; exit 1; }
info(){ echo -e "${BLUE}▶ $1${NC}"; }

command_exists(){ command -v "$1" &>/dev/null; }

[[ "$OSTYPE" == "darwin"* ]] || fail "This script is intended for macOS."

command_exists psql || fail "psql not found. Install PostgreSQL first (Homebrew/Postgres.app)."

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

# ------------------------------------------------------------------------------
# 1) Load DATABASE_URL if available
# ------------------------------------------------------------------------------
if [[ -z "${DATABASE_URL:-}" && -f ".env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source ".env"
  set +a
fi

# ------------------------------------------------------------------------------
# 2) Determine target DB settings
# ------------------------------------------------------------------------------
DB_USER=""
DB_PASS=""
DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="aicompass"

if [[ -n "${DATABASE_URL:-}" ]]; then
  # Parse DATABASE_URL with python for reliability
  read -r DB_USER DB_PASS DB_HOST DB_PORT DB_NAME < <(python3 - <<'PY'
import os, re, sys
url=os.environ.get("DATABASE_URL","").strip()
m=re.match(r"^postgresql:\/\/([^:]+):([^@]+)@([^:\/]+):(\d+)\/(.+)$", url)
if not m:
    sys.exit(1)
print(m.group(1), m.group(2), m.group(3), m.group(4), m.group(5))
PY
) || fail "DATABASE_URL format not supported. Expected: postgresql://user:pass@host:port/db"
  ok "Using target DB settings from DATABASE_URL (.env or env var)."
else
  warn "DATABASE_URL not found. Please enter target DB settings."
  read -p "Target DB user [aicompass_user]: " DB_USER
  DB_USER="${DB_USER:-aicompass_user}"

  while true; do
    read -s -p "Target DB password [aicompass_pass]: " DB_PASS
    echo ""
    if [[ -z "$DB_PASS" ]]; then DB_PASS="aicompass_pass"; break; fi
    read -s -p "Confirm target DB password: " DB_PASS2
    echo ""
    [[ "$DB_PASS" == "$DB_PASS2" ]] && break
    echo -e "${RED}Passwords do not match.${NC}"
  done

  read -p "Target DB name [aicompass]: " DB_NAME
  DB_NAME="${DB_NAME:-aicompass}"

  read -p "Target DB host [localhost]: " DB_HOST
  DB_HOST="${DB_HOST:-localhost}"

  read -p "Target DB port [5432]: " DB_PORT
  DB_PORT="${DB_PORT:-5432}"
fi

# ------------------------------------------------------------------------------
# 3) Ask for ADMIN credentials (required)
# ------------------------------------------------------------------------------
echo ""
info "Admin credentials (used ONLY to create role/database)."
read -p "Admin username [postgres]: " ADMIN_USER
ADMIN_USER="${ADMIN_USER:-postgres}"

# Hidden password prompt (no echo)
read -s -p "Admin password: " ADMIN_PASS
echo ""
[[ -n "$ADMIN_PASS" ]] || fail "Admin password is required."

# ------------------------------------------------------------------------------
# 4) Connectivity check
# ------------------------------------------------------------------------------
info "Checking connection to Postgres (host=$DB_HOST port=$DB_PORT db=postgres user=$ADMIN_USER)..."

# Use PGPASSWORD for this process only (not stored)
export PGPASSWORD="$ADMIN_PASS"

if ! psql -h "$DB_HOST" -p "$DB_PORT" -U "$ADMIN_USER" -d postgres -c "SELECT 1;" >/dev/null 2>&1; then
  unset PGPASSWORD
  fail "Cannot connect as admin. Check host/port, admin user/password, and that Postgres is running."
fi
ok "Admin connection OK."

# ------------------------------------------------------------------------------
# 5) Create role + database (idempotent)
# ------------------------------------------------------------------------------
info "Creating role/database (idempotent)..."

# Escape single quotes for SQL literal
DB_PASS_SQL="${DB_PASS//\'/\'\'}"
DB_USER_SQL="${DB_USER//\"/\"\"}"
DB_NAME_SQL="${DB_NAME//\"/\"\"}"

SQL=$(cat <<EOF
DO \$\$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = '${DB_USER}') THEN
    CREATE ROLE "${DB_USER_SQL}" LOGIN PASSWORD '${DB_PASS_SQL}';
  END IF;
END
\$\$;

DO \$\$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = '${DB_NAME}') THEN
    CREATE DATABASE "${DB_NAME_SQL}" OWNER "${DB_USER_SQL}";
  END IF;
END
\$\$;

GRANT ALL PRIVILEGES ON DATABASE "${DB_NAME_SQL}" TO "${DB_USER_SQL}";
EOF
)

psql -v ON_ERROR_STOP=1 -h "$DB_HOST" -p "$DB_PORT" -U "$ADMIN_USER" -d postgres -c "$SQL" >/dev/null
ok "Role ensured: $DB_USER"
ok "Database ensured: $DB_NAME"

# ------------------------------------------------------------------------------
# 6) Optional: update password if role already existed
# ------------------------------------------------------------------------------
echo ""
read -p "If the role already existed, do you want to FORCE set its password now? (y/N): " -r FORCE_PW
if [[ "$FORCE_PW" =~ ^[Yy]$ ]]; then
  psql -v ON_ERROR_STOP=1 -h "$DB_HOST" -p "$DB_PORT" -U "$ADMIN_USER" -d postgres \
    -c "ALTER ROLE \"${DB_USER_SQL}\" WITH PASSWORD '${DB_PASS_SQL}';" >/dev/null
  ok "Password updated for role: $DB_USER"
fi

unset PGPASSWORD

echo ""
ok "Done."
echo "Target DB:"
echo "  postgresql://${DB_USER}:********@${DB_HOST}:${DB_PORT}/${DB_NAME}"
echo ""
echo "Next step (if your project uses Alembic):"
echo "  (cd apps/api && alembic upgrade head)"
