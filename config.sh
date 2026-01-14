#!/bin/bash

# ==============================================================================
# AI-Compass Configuration Script
# ==============================================================================
# This script helps you set up your environment configuration (.env file)
# by collecting all necessary credentials and settings interactively.
#
# Run with: bash config.sh
# ==============================================================================

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Clear screen for better presentation
clear

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                            ║${NC}"
echo -e "${BLUE}║         🔧 AI-Compass Configuration Wizard                ║${NC}"
echo -e "${BLUE}║                                                            ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}This wizard will help you create your .env configuration file.${NC}"
echo ""

# ==============================================================================
# Check if .env already exists
# ==============================================================================

if [ -f ".env" ]; then
    echo -e "${YELLOW}⚠  Warning: .env file already exists!${NC}"
    echo ""
    read -p "Do you want to overwrite it? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${CYAN}Configuration cancelled. Your existing .env file is unchanged.${NC}"
        exit 0
    fi
    # Backup existing .env
    cp .env .env.backup
    echo -e "${GREEN}✓ Existing .env backed up to .env.backup${NC}"
    echo ""
fi

# ==============================================================================
# Collect Database Configuration
# ==============================================================================

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  PostgreSQL Database Configuration${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${CYAN}Enter your PostgreSQL database credentials:${NC}"
echo ""

# Database User
read -p "Database username [default: aicompass_user]: " DB_USER
DB_USER=${DB_USER:-aicompass_user}

# Database Password
while true; do
    read -s -p "Database password [default: aicompass_pass]: " DB_PASS
    echo ""
    if [ -z "$DB_PASS" ]; then
        DB_PASS="aicompass_pass"
        break
    fi
    read -s -p "Confirm password: " DB_PASS_CONFIRM
    echo ""
    if [ "$DB_PASS" = "$DB_PASS_CONFIRM" ]; then
        break
    else
        echo -e "${RED}✗ Passwords don't match. Please try again.${NC}"
        echo ""
    fi
done

# Database Name
read -p "Database name [default: aicompass]: " DB_NAME
DB_NAME=${DB_NAME:-aicompass}

# Database Host
read -p "Database host [default: localhost]: " DB_HOST
DB_HOST=${DB_HOST:-localhost}

# Database Port
read -p "Database port [default: 5432]: " DB_PORT
DB_PORT=${DB_PORT:-5432}

echo ""
echo -e "${GREEN}✓ Database configuration collected${NC}"
echo ""

# ==============================================================================
# Collect API Keys
# ==============================================================================

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  API Keys Configuration${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${CYAN}Get your FREE Groq API key at:${NC} ${YELLOW}https://console.groq.com${NC}"
echo ""

# Groq API Key
while true; do
    read -p "Groq API Key (starts with 'gsk_'): " GROQ_API_KEY
    if [[ $GROQ_API_KEY =~ ^gsk_ ]]; then
        break
    else
        echo -e "${RED}✗ Invalid API key format. It should start with 'gsk_'${NC}"
        echo ""
        read -p "Do you want to skip this for now? (y/n) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            GROQ_API_KEY="your_groq_api_key_here"
            echo -e "${YELLOW}⚠  You'll need to add your API key later${NC}"
            break
        fi
    fi
done

echo ""
echo -e "${GREEN}✓ API configuration collected${NC}"
echo ""

# ==============================================================================
# Generate .env file
# ==============================================================================

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Generating Configuration File${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Construct DATABASE_URL
DATABASE_URL="postgresql://${DB_USER}:${DB_PASS}@${DB_HOST}:${DB_PORT}/${DB_NAME}"

# Create .env file
cat > .env << EOF
# ==============================================================================
# AI-Compass Environment Configuration
# ==============================================================================
# Generated by config.sh on $(date)
# ==============================================================================

# Database Configuration
DATABASE_URL=${DATABASE_URL}

# API Keys
GROQ_API_KEY=${GROQ_API_KEY}

# Application Settings
ENVIRONMENT=development
LOG_LEVEL=INFO

# Questionnaire Configuration
QUESTIONNAIRE_PATH=data/questionnaire.json
EOF

echo -e "${GREEN}✓ .env file created successfully!${NC}"
echo ""

# ==============================================================================
# Display Summary
# ==============================================================================

echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                            ║${NC}"
echo -e "${GREEN}║           ✓ Configuration Complete! 🎉                     ║${NC}"
echo -e "${GREEN}║                                                            ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📋 Configuration Summary:${NC}"
echo ""
echo -e "  Database User:    ${CYAN}${DB_USER}${NC}"
echo -e "  Database Name:    ${CYAN}${DB_NAME}${NC}"
echo -e "  Database Host:    ${CYAN}${DB_HOST}:${DB_PORT}${NC}"

if [[ $GROQ_API_KEY == "your_groq_api_key_here" ]]; then
    echo -e "  Groq API Key:     ${RED}NOT SET ⚠${NC}"
else
    # Show only first 12 chars of API key for security
    MASKED_KEY="${GROQ_API_KEY:0:12}***"
    echo -e "  Groq API Key:     ${GREEN}${MASKED_KEY}${NC}"
fi

echo ""
echo -e "${BLUE}📁 Configuration File:${NC}"
echo -e "  ${YELLOW}.env${NC} (created in current directory)"
echo ""

# Show warning if API key not set
if [[ $GROQ_API_KEY == "your_groq_api_key_here" ]]; then
    echo -e "${YELLOW}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║  ⚠  IMPORTANT: Add your Groq API Key                      ║${NC}"
    echo -e "${YELLOW}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "Edit ${YELLOW}.env${NC} and replace:"
    echo -e "  ${RED}GROQ_API_KEY=your_groq_api_key_here${NC}"
    echo ""
    echo -e "With your actual key from: ${BLUE}https://console.groq.com${NC}"
    echo ""
fi

echo -e "${GREEN}Next Steps:${NC}"
echo ""
echo "The setup script will now run automatically to install all dependencies..."
echo ""
read -p "Press Enter to continue with setup, or Ctrl+C to exit..."
echo ""

# Run the setup script automatically
if [ -f "setup_ubuntu.sh" ]; then
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  Starting Automated Setup...                              ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    bash setup_ubuntu.sh
else
    echo -e "${RED}✗ setup_ubuntu.sh not found in current directory${NC}"
    echo ""
    echo "Please run the setup manually:"
    echo -e "   ${YELLOW}bash setup_ubuntu.sh${NC}"
    echo ""
fi
