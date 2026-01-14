#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# create_db_macos_interactive.sh
# macOS Postgres DB bootstrap (interactive like config.sh)
#
# What it does:
# - Asks for TARGET app DB user/password/db/host/port (with sane defaults)
# - Asks for ADMIN credentials (role that is allowed to CREATE ROLE/DB)
# - Connects via TCP (host/port) to avoid “local socket trust” surprises
# - Creates role + database idempotently
# - Optionally forces updating the role password
#
# Usage:
#   bash create_db_macos_interactive.sh
# ==============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

ok(){ echo -e "${GREEN}✓ $1${NC}"; }
warn(){ echo -e "${YELLOW}⚠ $1${NC}"; }
fail(){ echo -e "${RED}✗ $1${NC}"; exit 1; }
info(){ echo -e "${BLUE}▶ $1${NC}"; }

command -v psql >/dev/null 2>&1 || fail "psql not found. Install PostgreSQL first (Homebrew or Postgres.app)."
[[ "$OSTYPE" == "darwin"* ]] || fail "This script is intended for macOS."

clear || true
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                            ║${NC}"
echo -e "${BLUE}║        🐘 AI-Compass Database Creation (macOS)             ║${NC}"
echo -e "${BLUE}║                                                            ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ------------------------------------------------------------------------------
# 1) Target DB (app) settings (interactive like config.sh)
# ------------------------------------------------------------------------------
echo -e "${CYAN}Enter TARGET (app) database settings:${NC}"
echo ""

read -p "Target DB user [aicompass_user]: " DB_USER
DB_USER="${DB_USER:-aicompass_user}"

while true; do
  read -s -p "Target DB password [aicompass_pass]: " DB_PASS
  echo ""
  if [[ -z "$DB_PASS" ]]; then
    DB_PASS="aicompass_pass"
    break
  fi
  read -s -p "Confirm target DB password: " DB_PASS2
  echo ""
  if [[ "$DB_PASS" == "$DB_PASS2" ]]; then
    break
  fi
  echo -e "${RED}✗ Passwords don't match. Try again.${NC}"
done

read -p "Target DB name [aicompass]: " DB_NAME
DB_NAME="${DB_NAME:-aicompass}"

read -p "Target DB host [localhost]: " DB_HOST
DB_HOST="${DB_HOST:-localhost}"

read -p "Target DB port [5432]: " DB_PORT
DB_PORT="${DB_PORT:-5432}"

echo ""
ok "Target DB settings captured."

# ------------------------------------------------------------------------------
# 2) Admin credentials (must be able to CREATE ROLE/DB)
# ------------------------------------------------------------------------------
echo ""
echo -e "${CYAN}Now enter ADMIN credentials (used only to create role/database):${NC}"
echo -e "${YELLOW}Tip:${NC} On Homebrew Postgres the admin is often your macOS username (${USER})."
echo -e "${YELLOW}Tip:${NC} On some setups it’s 'postgres'. Use what works on you
