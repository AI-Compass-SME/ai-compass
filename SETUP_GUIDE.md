# 🛠️ Setup Guide for AI-Compass

This guide provides detailed instructions for setting up AI-Compass on Ubuntu/Linux and macOS.

---

## 📋 Prerequisites

### Common Requirements
- **Internet Connection**: Required for downloading packages
- **Disk Space**: At least 2GB free space
- **RAM**: Minimum 4GB recommended

### Ubuntu/Linux
- Ubuntu 20.04+ or Debian 11+
- sudo access

### macOS
- macOS 11 (Big Sur) or later
- Admin privileges

---

## 🚀 Quick Setup

### Ubuntu/Linux

```bash
# 1. Navigate to project directory
cd ai-compass

# 2. Make setup script executable
chmod +x setup_ubuntu.sh

# 3. Run setup (this will take 5-10 minutes)
bash setup_ubuntu.sh

# 4. Configure your Groq API key
nano .env
# Add: GROQ_API_KEY=your_actual_key_here

# 5. Activate virtual environment
source venv/bin/activate

# 6. Start the application
bash start.sh
```

### macOS

```bash
# 1. Navigate to project directory
cd ai-compass

# 2. Make setup script executable
chmod +x setup_macos.sh

# 3. Run setup (this will take 10-15 minutes)
bash setup_macos.sh

# 4. Configure your Groq API key
nano .env
# Add: GROQ_API_KEY=your_actual_key_here

# 5. Activate virtual environment
source venv/bin/activate

# 6. Start the application
bash start.sh
```

---

## 📦 What the Setup Scripts Install

### Ubuntu/Linux (`setup_ubuntu.sh`)
1. **System Updates**: Updates package lists
2. **Python 3.10+**: Via deadsnakes PPA
3. **PostgreSQL 14+**: Database server
4. **System Libraries**: 
   - build-essential, curl, wget, git
   - libpq-dev, libssl-dev, libffi-dev
   - libjpeg-dev, zlib1g-dev
5. **Python Virtual Environment**: Isolated environment
6. **Python Packages**: All requirements.txt dependencies
7. **Database Setup**: Creates `aicompass` database
8. **Database Schema**: Runs Alembic migrations

### macOS (`setup_macos.sh`)
1. **Homebrew**: Package manager (if not installed)
2. **Python 3.10+**: Via Homebrew
3. **PostgreSQL 14+**: Database server
4. **System Libraries**: 
   - openssl, readline, sqlite3
   - xz, zlib, jpeg, freetype
5. **Git**: Version control (if not installed)
6. **Python Virtual Environment**: Isolated environment
7. **Python Packages**: All requirements.txt dependencies
8. **Database Setup**: Creates `aicompass` database
9. **Database Schema**: Runs Alembic migrations

---

## 🔧 Manual Setup (if scripts fail)

### 1. Install Python 3.10+

**Ubuntu:**
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip
```

**macOS:**
```bash
brew install python@3.10
```

### 2. Install PostgreSQL 14+

**Ubuntu:**
```bash
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt update
sudo apt install postgresql-14
```

**macOS:**
```bash
brew install postgresql@14
brew services start postgresql@14
```

### 3. Create Database

**Ubuntu:**
```bash
sudo -u postgres psql -c "CREATE USER aicompass_user WITH PASSWORD 'aicompass_pass';"
sudo -u postgres psql -c "CREATE DATABASE aicompass OWNER aicompass_user;"
```

**macOS:**
```bash
psql postgres -c "CREATE USER aicompass_user WITH PASSWORD 'aicompass_pass';"
psql postgres -c "CREATE DATABASE aicompass OWNER aicompass_user;"
```

### 4. Setup Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure Environment

```bash
cp infra/.env.example .env
# Edit .env and set DATABASE_URL and GROQ_API_KEY
nano .env
```

### 6. Run Database Migrations

```bash
cd apps/api
alembic upgrade head
cd ../..
```

### 7. Verify Setup

```bash
python3 check_setup.py
```

---

## 🎯 Post-Setup Configuration

### 1. Get Groq API Key

1. Visit https://console.groq.com
2. Sign up for free account
3. Navigate to API Keys section
4. Create new API key
5. Copy the key

### 2. Update .env File

```bash
nano .env
```

Update the following:
```env
# Required
GROQ_API_KEY=gsk_your_actual_key_here

# Database (already configured by setup script)
DATABASE_URL=postgresql://aicompass_user:aicompass_pass@localhost:5432/aicompass

# Optional: Adjust these if needed
GROQ_MODEL=llama-3.1-70b-versatile
GROQ_TEMPERATURE=0.2
SYNTHETIC_PEER_COUNT=500
KMEANS_CLUSTERS=4
```

---

## 🚦 Starting the Application

### Using start.sh (Recommended)

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Start both API and Streamlit
bash start.sh
```

This will:
- **Ubuntu**: Open two new gnome-terminal windows (or konsole)
- **macOS**: Open two new Terminal windows
- One for FastAPI backend (port 8000)
- One for Streamlit frontend (port 8501)

### Manual Start (Alternative)

**Terminal 1 - API:**
```bash
source venv/bin/activate
cd apps/api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Streamlit:**
```bash
source venv/bin/activate
cd apps/web
streamlit run Home.py
```

---

## 🌐 Accessing the Application

Once started, access these URLs:

- **📊 Streamlit UI**: http://localhost:8501
  - Main application interface
  - Complete assessment workflow
  - Results dashboard

- **🔌 API Server**: http://localhost:8000
  - REST API endpoints
  - Health check available

- **📖 API Documentation**: http://localhost:8000/docs
  - Interactive Swagger UI
  - Test endpoints directly

---

## ✅ Verification Steps

### 1. Check Database Connection

```bash
psql -U aicompass_user -d aicompass -h localhost
# Password: aicompass_pass
```

Inside psql:
```sql
\dt                          -- List tables
SELECT COUNT(*) FROM company_assessment;  -- Should return 0 initially
\q                           -- Quit
```

### 2. Check API Health

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2026-01-06T...",
  "database": "connected",
  "questionnaire_loaded": true
}
```

### 3. Check Questionnaire

```bash
curl http://localhost:8000/api/v1/questionnaire | jq '.metadata'
```

Expected:
```json
{
  "questionnaire_id": "ai-compass-mvp",
  "questionnaire_version": "2026-01-06",
  "dimensions_count": 7,
  "questions_count": 21
}
```

### 4. Run Setup Validator

```bash
python3 check_setup.py
```

All checks should pass with ✓ marks.

---

## 🐛 Troubleshooting

### PostgreSQL Connection Errors

**Problem**: `could not connect to server`

**Solution (Ubuntu):**
```bash
sudo systemctl status postgresql
sudo systemctl start postgresql
```

**Solution (macOS):**
```bash
brew services list
brew services start postgresql@14
```

---

### Port Already in Use

**Problem**: `Address already in use`

**Solution (Find and kill process):**
```bash
# For port 8000 (API)
lsof -ti:8000 | xargs kill -9

# For port 8501 (Streamlit)
lsof -ti:8501 | xargs kill -9
```

---

### Virtual Environment Not Activated

**Problem**: `No module named 'fastapi'`

**Solution:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

### Alembic Migration Errors

**Problem**: `Target database is not up to date.`

**Solution:**
```bash
cd apps/api
alembic downgrade base   # CAUTION: Drops all tables
alembic upgrade head
cd ../..
```

---

### Groq API Errors

**Problem**: `401 Unauthorized` from Groq

**Solution:**
1. Check your API key in `.env`
2. Verify key is active at https://console.groq.com
3. The app has fallback templates if LLM fails (intentional)

---

### Permission Denied on Scripts

**Problem**: `Permission denied: ./setup_ubuntu.sh`

**Solution:**
```bash
chmod +x setup_ubuntu.sh
chmod +x setup_macos.sh
chmod +x start.sh
```

---

### Python Version Issues

**Problem**: Python version too old

**Ubuntu:**
```bash
python3 --version    # Check current version
sudo update-alternatives --config python3  # Select 3.10
```

**macOS:**
```bash
brew unlink python
brew link python@3.10
```

---

## 🔄 Updating the Application

### Update Python Dependencies

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

### Update Database Schema

```bash
cd apps/api
alembic upgrade head
cd ../..
```

### Pull Latest Code (if using Git)

```bash
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
cd apps/api && alembic upgrade head && cd ../..
```

---

## 🗑️ Uninstallation

### Remove Virtual Environment

```bash
deactivate  # If activated
rm -rf venv/
```

### Remove Database

**Ubuntu:**
```bash
sudo -u postgres psql -c "DROP DATABASE aicompass;"
sudo -u postgres psql -c "DROP USER aicompass_user;"
```

**macOS:**
```bash
psql postgres -c "DROP DATABASE aicompass;"
psql postgres -c "DROP USER aicompass_user;"
```

### Remove PostgreSQL (Optional)

**Ubuntu:**
```bash
sudo apt remove postgresql-14
```

**macOS:**
```bash
brew uninstall postgresql@14
```

---

## 📚 Additional Resources

- **Main Documentation**: `README.md`
- **Quick Start Guide**: `QUICKSTART.md`
- **Project Structure**: `PROJECT_STRUCTURE.md`
- **API Reference**: `API_REFERENCE.md`
- **Code Analysis**: `ai-compas.md`
- **GitHub Guide**: `GIT_PUSH_GUIDE.md`

---

## 🆘 Getting Help

If you encounter issues:

1. **Check setup validator**: `python3 check_setup.py`
2. **Review logs**: Check terminal output for errors
3. **Verify prerequisites**: Ensure Python 3.10+ and PostgreSQL 14+ are installed
4. **Database status**: Confirm PostgreSQL is running
5. **Environment file**: Verify `.env` has correct values
6. **Clean reinstall**: Remove `venv/` and run setup script again

---

## ✅ Setup Checklist

- [ ] Python 3.10+ installed
- [ ] PostgreSQL 14+ installed and running
- [ ] Virtual environment created (`venv/`)
- [ ] Python packages installed (`pip install -r requirements.txt`)
- [ ] Database created (`aicompass`)
- [ ] `.env` file configured with GROQ_API_KEY
- [ ] Database migrations run (`alembic upgrade head`)
- [ ] Setup validator passes (`python3 check_setup.py`)
- [ ] Application starts successfully (`bash start.sh`)
- [ ] Can access http://localhost:8501
- [ ] Can access http://localhost:8000/docs

---

**Once all items are checked, you're ready to use AI-Compass! 🎉**
