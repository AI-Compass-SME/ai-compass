#!/usr/bin/env python3
"""
AI-Compass Startup Checker
Validates that all prerequisites are met before starting the application.
"""
import sys
import os
from pathlib import Path
import subprocess

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_check(message, status=True):
    """Print check result with color."""
    symbol = f"{Colors.GREEN}✓{Colors.END}" if status else f"{Colors.RED}✗{Colors.END}"
    print(f"{symbol} {message}")

def print_section(title):
    """Print section header."""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}{title}{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")

def check_python_version():
    """Check Python version >= 3.10."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print_check(f"Python {version.major}.{version.minor}.{version.micro}", True)
        return True
    else:
        print_check(f"Python {version.major}.{version.minor}.{version.micro} (need 3.10+)", False)
        return False

def check_file_exists(filepath, description):
    """Check if file exists."""
    exists = Path(filepath).exists()
    print_check(f"{description}: {filepath}", exists)
    return exists

def check_command_available(command, description):
    """Check if command is available."""
    try:
        subprocess.run([command, "--version"], capture_output=True, check=True)
        print_check(description, True)
        return True
    except:
        print_check(f"{description} (not found)", False)
        return False

def check_env_file():
    """Check if .env file exists and has required keys."""
    env_path = Path(".env")
    if not env_path.exists():
        print_check(".env file", False)
        print(f"  {Colors.YELLOW}Run: cp infra/.env.example .env{Colors.END}")
        return False
    
    # Check for required keys
    with open(env_path) as f:
        content = f.read()
    
    required = ["DATABASE_URL", "GROQ_API_KEY"]
    missing = []
    
    for key in required:
        if key not in content or f"{key}=" in content and "your_" in content:
            missing.append(key)
    
    if missing:
        print_check(f".env file (missing: {', '.join(missing)})", False)
        return False
    else:
        print_check(".env file", True)
        return True

def check_postgresql():
    """Check if PostgreSQL is running."""
    try:
        result = subprocess.run(
            ["pg_isready"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print_check("PostgreSQL", True)
            return True
        else:
            print_check("PostgreSQL (not running)", False)
            return False
    except FileNotFoundError:
        print_check("PostgreSQL (pg_isready not found)", False)
        return False

def main():
    """Run all checks."""
    print(f"{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║          AI-COMPASS STARTUP CHECKER                        ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")
    
    all_passed = True
    
    # Python version
    print_section("Python Environment")
    all_passed &= check_python_version()
    
    # Critical files
    print_section("Critical Files")
    all_passed &= check_file_exists("data/questionnaire/questions.json", "Questionnaire")
    all_passed &= check_file_exists("requirements.txt", "Requirements")
    all_passed &= check_file_exists("apps/api/main.py", "API Main")
    all_passed &= check_file_exists("apps/web/Home.py", "Web Home")
    
    # Configuration
    print_section("Configuration")
    all_passed &= check_env_file()
    
    # Dependencies (commands)
    print_section("System Dependencies")
    all_passed &= check_postgresql()
    
    # Database migrations
    print_section("Database")
    migration_exists = check_file_exists(
        "apps/api/alembic/versions/001_initial_schema.py",
        "Initial migration"
    )
    all_passed &= migration_exists
    
    # Python packages (check a few key ones)
    print_section("Python Packages")
    try:
        import fastapi
        print_check("fastapi", True)
    except:
        print_check("fastapi", False)
        all_passed = False
    
    try:
        import streamlit
        print_check("streamlit", True)
    except:
        print_check("streamlit", False)
        all_passed = False
    
    try:
        import sqlalchemy
        print_check("sqlalchemy", True)
    except:
        print_check("sqlalchemy", False)
        all_passed = False
    
    try:
        import groq
        print_check("groq", True)
    except:
        print_check("groq", False)
        all_passed = False
    
    # Summary
    print_section("Summary")
    
    if all_passed:
        print(f"\n{Colors.GREEN}✓ All checks passed! You're ready to start AI-Compass.{Colors.END}\n")
        print("Next steps:")
        print("  1. Terminal 1: cd apps/api && uvicorn main:app --reload")
        print("  2. Terminal 2: cd apps/web && streamlit run Home.py")
        print()
        return 0
    else:
        print(f"\n{Colors.RED}✗ Some checks failed. Please fix the issues above.{Colors.END}\n")
        print("Common fixes:")
        print("  • Install dependencies: pip install -r requirements.txt")
        print("  • Configure .env: cp infra/.env.example .env (and edit)")
        print("  • Start PostgreSQL: brew services start postgresql (Mac) or sudo systemctl start postgresql (Linux)")
        print("  • Run migrations: cd apps/api && alembic upgrade head")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())
