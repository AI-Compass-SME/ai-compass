#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# AI-Compass macOS System Libraries (best-effort)
# - Installs common build/runtime libs via Homebrew
# - Does NOT fail the whole run if a package can't be installed
#
# Usage:
#   bash macos_system_libs.sh
# Optional:
#   BREW_NO_UPDATE=1 bash macos_system_libs.sh
# ==============================================================================

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

ok(){ echo -e "${GREEN}✓ $1${NC}"; }
warn(){ echo -e "${YELLOW}⚠ $1${NC}"; }
fail(){ echo -e "${RED}✗ $1${NC}"; exit 1; }
info(){ echo -e "${BLUE}▶ $1${NC}"; }

command_exists(){ command -v "$1" &>/dev/null; }

[[ "$OSTYPE" == "darwin"* ]] || fail "This script is macOS only."

if ! command_exists brew; then
  fail "Homebrew not found. Install Homebrew first: https://brew.sh/"
fi

# Ensure brew is on PATH (Apple Silicon)
if [[ "$(uname -m)" == "arm64" ]] && [[ -x "/opt/homebrew/bin/brew" ]]; then
  eval "$(/opt/homebrew/bin/brew shellenv)"
fi

info "Installing system libraries (best-effort)"

if [[ "${BREW_NO_UPDATE:-0}" != "1" ]]; then
  info "brew update"
  brew update >/dev/null 2>&1 || warn "brew update failed (continuing)"
else
  warn "Skipping brew update (BREW_NO_UPDATE=1)"
fi

# Minimal, practical set for common Python/native deps (Pillow, SSL, compression, etc.)
PACKAGES=(
  openssl@3
  readline
  sqlite
  xz
  zlib
  jpeg
  freetype
  libpng
  libffi
  pkg-config
  cmake
)

FAILED=()

for pkg in "${PACKAGES[@]}"; do
  if brew list --versions "$pkg" >/dev/null 2>&1; then
    ok "$pkg already installed"
    continue
  fi

  info "brew install $pkg"
  if brew install "$pkg" >/dev/null 2>&1; then
    ok "$pkg installed"
  else
    warn "Failed to install $pkg (continuing)"
    FAILED+=("$pkg")
  fi
done

echo ""
if [[ "${#FAILED[@]}" -gt 0 ]]; then
  warn "Some packages failed to install:"
  for p in "${FAILED[@]}"; do
    echo "  - $p"
  done
  echo ""
  warn "This is usually not fatal. If you hit build errors later, rerun this script or install the missing packages manually."
else
  ok "All system libraries installed successfully"
fi

echo ""
ok "Done"
