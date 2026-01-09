#!/bin/bash

# ==============================================================================
# AI-Compass Setup Script for Ubuntu/Debian Linux
# ==============================================================================
# This script installs all dependencies and sets up the complete environment
# for the AI-Compass AI Maturity Assessment Platform
#
# Requirements: Ubuntu 20.04+ or Debian 11+
# Run with: bash setup_ubuntu.sh
# ==============================================================================

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
PYTHON_MIN_VERSION="3.10"
POSTGRES_VERSION="14"
VENV_NAME="venv"

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                            ║${NC}"
echo -e "${BLUE}║         🧭 AI-Compass Setup Script (Ubuntu/Linux)         ║${NC}"
echo -e "${BLUE}║                                                            ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ==============================================================================
# Helper Functions
# ==============================================================================

print_step() {
    echo ""
    echo -e "${GREEN}▶ $1${NC}"
    echo "────────────────────────────────────────────────────────────"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

command_exists() {
    command -v "$1" &> /dev/null
}

check_python_version() {
    if command_exists python3; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        REQUIRED_VERSION=$PYTHON_MIN_VERSION
        if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then
            return 0
        fi
    fi
    return 1
}

# ==============================================================================
# Pre-flight Checks
# ==============================================================================

print_step "Pre-flight Checks"

# Check if running as root (not recommended)
if [ "$EUID" -eq 0 ]; then
    print_warning "Running as root is not recommended. Consider running as a regular user."
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check internet connection
if ! ping -c 1 google.com &> /dev/null; then
    print_error "No internet connection detected. Please connect to the internet and try again."
    exit 1
fi
print_success "Internet connection verified"

# Check OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    print_success "Detected: $PRETTY_NAME"
else
    print_warning "Could not detect OS version"
fi

# ==============================================================================
# 1. Update System Packages
# ==============================================================================

print_step "Updating System Packages"

sudo apt-get update -qq
print_success "Package lists updated"

# ==============================================================================
# 2. Install System Dependencies
# ==============================================================================

print_step "Installing System Dependencies"

# Essential build tools
sudo apt-get install -y -qq \
    build-essential \
    curl \
    wget \
    git \
    software-properties-common \
    ca-certificates \
    gnupg \
    lsb-release

print_success "Essential build tools installed"

# ==============================================================================
# 3. Install Python 3.10+
# ==============================================================================

print_step "Installing Python ${PYTHON_MIN_VERSION}+"

if ! check_python_version; then
    print_warning "Python ${PYTHON_MIN_VERSION}+ not found. Installing..."
    
    # Add deadsnakes PPA for newer Python versions
    sudo add-apt-repository -y ppa:deadsnakes/ppa
    sudo apt-get update -qq
    
    # Install Python 3.10
    sudo apt-get install -y -qq \
        python3.10 \
        python3.10-venv \
        python3.10-dev \
        python3-pip
    
    # Set Python 3.10 as default python3 (optional)
    sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
else
    CURRENT_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python ${CURRENT_VERSION} already installed"
fi

# Ensure pip is installed and up to date
if ! command_exists pip3; then
    sudo apt-get install -y -qq python3-pip
fi
python3 -m pip install --upgrade pip --quiet
print_success "pip upgraded to latest version"

# ==============================================================================
# 4. Install PostgreSQL 14+
# ==============================================================================

print_step "Installing PostgreSQL ${POSTGRES_VERSION}+"

if ! command_exists psql; then
    print_warning "PostgreSQL not found. Installing..."
    
    # Add PostgreSQL APT repository
    sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
    
    sudo apt-get update -qq
    sudo apt-get install -y -qq postgresql-${POSTGRES_VERSION} postgresql-contrib-${POSTGRES_VERSION}
    
    # Start PostgreSQL service
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
    
    print_success "PostgreSQL ${POSTGRES_VERSION} installed and started"
else
    POSTGRES_CURRENT_VERSION=$(psql --version | awk '{print $3}' | cut -d'.' -f1)
    print_success "PostgreSQL ${POSTGRES_CURRENT_VERSION} already installed"
fi

# ==============================================================================
# 5. Create PostgreSQL Database
# ==============================================================================

print_step "Setting up PostgreSQL Database"

# Parse database credentials from .env file
if [ ! -f ".env" ]; then
    print_error ".env file not found. Please run config.sh first to create it."
    exit 1
fi

# Source .env and extract DATABASE_URL components
source .env

if [ -z "$DATABASE_URL" ]; then
    print_error "DATABASE_URL not found in .env file"
    exit 1
fi

# Parse DATABASE_URL (format: postgresql://user:password@host:port/dbname)
# Remove postgresql:// prefix
DB_STRING="${DATABASE_URL#postgresql://}"

# Extract user:password
DB_CREDENTIALS="${DB_STRING%%@*}"
DB_USER="${DB_CREDENTIALS%%:*}"
DB_PASS="${DB_CREDENTIALS#*:}"

# Extract host:port/dbname
DB_REMAINDER="${DB_STRING#*@}"
DB_HOST="${DB_REMAINDER%%:*}"

# Extract port/dbname
DB_PORT_AND_DB="${DB_REMAINDER#*:}"
DB_PORT="${DB_PORT_AND_DB%%/*}"
DB_NAME="${DB_PORT_AND_DB#*/}"

print_success "Database configuration loaded from .env"
echo "  Database: $DB_NAME"
echo "  User: $DB_USER"
echo "  Host: $DB_HOST:$DB_PORT"

# Create database user and database
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';" 2>/dev/null || print_warning "User might already exist"
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;" 2>/dev/null || print_warning "Database might already exist"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" 2>/dev/null

print_success "Database '$DB_NAME' created (or already exists)"

# ==============================================================================
# 6. Install Additional System Libraries
# ==============================================================================

print_step "Installing Additional System Libraries"

# Libraries needed for Python packages
sudo apt-get install -y -qq \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev

print_success "System libraries installed"

# ==============================================================================
# 7. Create Python Virtual Environment
# ==============================================================================

print_step "Creating Python Virtual Environment"

if [ -d "$VENV_NAME" ]; then
    print_warning "Virtual environment already exists. Removing..."
    rm -rf "$VENV_NAME"
fi

python3 -m venv "$VENV_NAME"
print_success "Virtual environment created: $VENV_NAME"

# Activate virtual environment
source "$VENV_NAME/bin/activate"
print_success "Virtual environment activated"

# ==============================================================================
# 8. Install Python Dependencies
# ==============================================================================

print_step "Installing Python Dependencies"

if [ ! -f "requirements.txt" ]; then
    print_error "requirements.txt not found. Are you in the ai-compass directory?"
    exit 1
fi

echo "This may take a few minutes..."
pip install --upgrade pip setuptools wheel --quiet
pip install -r requirements.txt --quiet

print_success "All Python packages installed"

# ==============================================================================
# 9. Setup Environment Variables
# ==============================================================================

print_step "Setting up Environment Variables"

if [ ! -f ".env" ]; then
    print_error ".env file not found. Please run config.sh first to create it."
    print_warning "Run: bash config.sh"
    exit 1
else
    print_success ".env file already exists"
fi

# ==============================================================================
# 10. Initialize Database Schema
# ==============================================================================

print_step "Initializing Database Schema"

cd apps/api

if [ ! -d "alembic/versions" ]; then
    print_error "Alembic migrations directory not found"
    cd ../..
else
    # Run migrations
    echo "Running database migrations..."
    alembic upgrade head || print_warning "Migration might have failed. Check manually."
    print_success "Database schema initialized"
    cd ../..
fi

# ==============================================================================
# 11. Verify Installation
# ==============================================================================

print_step "Verifying Installation"

echo "Running verification checks..."
python3 check_setup.py || print_warning "Some checks failed. Review output above."

# ==============================================================================
# 12. Setup Completion
# ==============================================================================

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                            ║${NC}"
echo -e "${GREEN}║           ✓ Setup Complete! 🎉                             ║${NC}"
echo -e "${GREEN}║                                                            ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo ""
echo "1. Configure your GROQ API Key:"
echo "   ${YELLOW}nano .env${NC}"
echo "   Add your key: GROQ_API_KEY=your_actual_key_here"
echo ""
echo "2. Activate the virtual environment:"
echo "   ${YELLOW}source venv/bin/activate${NC}"
echo ""
echo "3. Start the application:"
echo "   ${YELLOW}bash start.sh${NC}"
echo ""
echo "4. Access the application:"
echo "   📊 Streamlit UI:  http://localhost:8501"
echo "   🔌 API Server:    http://localhost:8000"
echo "   📖 API Docs:      http://localhost:8000/docs"
echo ""
echo -e "${BLUE}Useful Commands:${NC}"
echo "   • Activate env:     source venv/bin/activate"
echo "   • Deactivate env:   deactivate"
echo "   • Start app:        bash start.sh"
echo "   • Check status:     python3 check_setup.py"
echo "   • PostgreSQL CLI:   psql -U aicompass_user -d aicompass"
echo ""
echo -e "${YELLOW}⚠ Don't forget to get your free Groq API key at:${NC}"
echo "   https://console.groq.com"
echo ""
