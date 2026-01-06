#!/bin/bash

# ==============================================================================
# AI-Compass Setup Script for macOS
# ==============================================================================
# This script installs all dependencies and sets up the complete environment
# for the AI-Compass AI Maturity Assessment Platform
#
# Requirements: macOS 11 (Big Sur) or later
# Run with: bash setup_macos.sh
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
echo -e "${BLUE}║           🧭 AI-Compass Setup Script (macOS)               ║${NC}"
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

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "This script is for macOS only. Use setup_ubuntu.sh for Linux."
    exit 1
fi

# Detect macOS version
MACOS_VERSION=$(sw_vers -productVersion)
print_success "Detected macOS: $MACOS_VERSION"

# Check internet connection
if ! ping -c 1 google.com &> /dev/null; then
    print_error "No internet connection detected. Please connect to the internet and try again."
    exit 1
fi
print_success "Internet connection verified"

# ==============================================================================
# 1. Install Homebrew
# ==============================================================================

print_step "Installing Homebrew Package Manager"

if ! command_exists brew; then
    print_warning "Homebrew not found. Installing..."
    echo "This may require your password and will take a few minutes..."
    
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH for Apple Silicon Macs
    if [[ $(uname -m) == 'arm64' ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
    
    print_success "Homebrew installed"
else
    print_success "Homebrew already installed"
    brew update > /dev/null
fi

# ==============================================================================
# 2. Install Python 3.10+
# ==============================================================================

print_step "Installing Python ${PYTHON_MIN_VERSION}+"

if ! check_python_version; then
    print_warning "Python ${PYTHON_MIN_VERSION}+ not found. Installing..."
    
    brew install python@3.10
    
    # Link python3.10
    brew link python@3.10
    
    print_success "Python 3.10 installed"
else
    CURRENT_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python ${CURRENT_VERSION} already installed"
fi

# Ensure pip is up to date
python3 -m pip install --upgrade pip --quiet
print_success "pip upgraded to latest version"

# ==============================================================================
# 3. Install PostgreSQL 14+
# ==============================================================================

print_step "Installing PostgreSQL ${POSTGRES_VERSION}+"

if ! command_exists psql; then
    print_warning "PostgreSQL not found. Installing..."
    
    brew install postgresql@${POSTGRES_VERSION}
    
    # Add PostgreSQL to PATH
    echo 'export PATH="/opt/homebrew/opt/postgresql@14/bin:$PATH"' >> ~/.zprofile
    export PATH="/opt/homebrew/opt/postgresql@14/bin:$PATH"
    
    # Start PostgreSQL service
    brew services start postgresql@${POSTGRES_VERSION}
    
    # Wait for PostgreSQL to start
    echo "Waiting for PostgreSQL to start..."
    sleep 5
    
    print_success "PostgreSQL ${POSTGRES_VERSION} installed and started"
else
    POSTGRES_CURRENT_VERSION=$(psql --version | awk '{print $3}' | cut -d'.' -f1)
    print_success "PostgreSQL ${POSTGRES_CURRENT_VERSION} already installed"
    
    # Ensure it's running
    brew services start postgresql@${POSTGRES_VERSION} 2>/dev/null || brew services restart postgresql@${POSTGRES_VERSION} 2>/dev/null
fi

# ==============================================================================
# 4. Create PostgreSQL Database
# ==============================================================================

print_step "Setting up PostgreSQL Database"

# Wait a bit more for PostgreSQL to be fully ready
sleep 2

# Create database user and database
# On macOS, default postgres user might not exist, so we use current user
psql postgres -c "CREATE USER aicompass_user WITH PASSWORD 'aicompass_pass';" 2>/dev/null || print_warning "User might already exist"
psql postgres -c "CREATE DATABASE aicompass OWNER aicompass_user;" 2>/dev/null || print_warning "Database might already exist"
psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE aicompass TO aicompass_user;" 2>/dev/null

print_success "Database 'aicompass' created (or already exists)"

# ==============================================================================
# 5. Install Additional System Libraries
# ==============================================================================

print_step "Installing Additional System Libraries"

# Install libraries needed for Python packages
brew install \
    openssl \
    readline \
    sqlite3 \
    xz \
    zlib \
    jpeg \
    freetype

print_success "System libraries installed"

# ==============================================================================
# 6. Install Git (if not already installed)
# ==============================================================================

print_step "Checking Git Installation"

if ! command_exists git; then
    brew install git
    print_success "Git installed"
else
    print_success "Git already installed"
fi

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
    if [ -f "infra/.env.example" ]; then
        cp infra/.env.example .env
        print_success "Created .env from template"
        
        # Update DATABASE_URL
        sed -i '' 's|DATABASE_URL=.*|DATABASE_URL=postgresql://aicompass_user:aicompass_pass@localhost:5432/aicompass|g' .env
        
        print_warning "IMPORTANT: Edit .env and add your GROQ_API_KEY"
        print_warning "Get your free API key at: https://console.groq.com"
    else
        print_error "infra/.env.example not found"
    fi
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
echo "   • Stop app:         Press Ctrl+C in terminals"
echo "   • Check status:     python3 check_setup.py"
echo "   • PostgreSQL CLI:   psql -U aicompass_user -d aicompass"
echo "   • Start PostgreSQL: brew services start postgresql@14"
echo "   • Stop PostgreSQL:  brew services stop postgresql@14"
echo ""
echo -e "${BLUE}macOS Specific Notes:${NC}"
echo "   • PostgreSQL runs as a background service via Homebrew"
echo "   • start.sh will open new Terminal windows for API and Web"
echo "   • Python and PostgreSQL are managed by Homebrew"
echo ""
echo -e "${YELLOW}⚠ Don't forget to get your free Groq API key at:${NC}"
echo "   https://console.groq.com"
echo ""
