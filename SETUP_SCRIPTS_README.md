# 📋 Setup Scripts Summary

This document explains the setup and startup scripts for AI-Compass.

---

## 📂 Files Created

### 1. **setup_ubuntu.sh** - Ubuntu/Linux Setup Script
- **Purpose**: Complete automated setup for Ubuntu/Debian systems
- **What it does**:
  - ✅ Updates system packages
  - ✅ Installs Python 3.10+ (via deadsnakes PPA)
  - ✅ Installs PostgreSQL 14+
  - ✅ Installs system libraries (libpq-dev, etc.)
  - ✅ Creates PostgreSQL database and user
  - ✅ Creates Python virtual environment
  - ✅ Installs all Python dependencies
  - ✅ Sets up .env file from template
  - ✅ Runs database migrations
  - ✅ Verifies installation
- **Usage**:
  ```bash
  chmod +x setup_ubuntu.sh
  bash setup_ubuntu.sh
  ```
- **Time**: ~5-10 minutes

### 2. **setup_macos.sh** - macOS Setup Script
- **Purpose**: Complete automated setup for macOS systems
- **What it does**:
  - ✅ Installs Homebrew (if not present)
  - ✅ Installs Python 3.10+ (via Homebrew)
  - ✅ Installs PostgreSQL 14+ (via Homebrew)
  - ✅ Installs system libraries (openssl, zlib, etc.)
  - ✅ Creates PostgreSQL database and user
  - ✅ Creates Python virtual environment
  - ✅ Installs all Python dependencies
  - ✅ Sets up .env file from template
  - ✅ Runs database migrations
  - ✅ Verifies installation
- **Usage**:
  ```bash
  chmod +x setup_macos.sh
  bash setup_macos.sh
  ```
- **Time**: ~10-15 minutes

### 3. **start.sh** - Application Startup Script (Existing)
- **Purpose**: Start both FastAPI and Streamlit in separate terminals
- **Multi-platform**: Works on macOS, Linux, and WSL
- **What it does**:
  - ✅ Checks if in correct directory
  - ✅ Warns if virtual environment not activated
  - ✅ Detects OS (macOS/Linux)
  - ✅ Opens separate terminal windows:
    - Terminal 1: FastAPI backend (port 8000)
    - Terminal 2: Streamlit frontend (port 8501)
  - ✅ Shows access URLs
- **Platform-specific behavior**:
  - **macOS**: Uses `osascript` to open Terminal.app windows
  - **Linux**: Uses `gnome-terminal` or `konsole`
  - **Fallback**: Uses `tmux` or manual instructions
- **Usage**:
  ```bash
  source venv/bin/activate
  bash start.sh
  ```
- **No separate mac_start.sh needed**: The existing start.sh handles both macOS and Linux!

### 4. **SETUP_GUIDE.md** - Comprehensive Documentation
- **Purpose**: Detailed setup instructions and troubleshooting
- **Contains**:
  - ✅ Prerequisites for each platform
  - ✅ Quick setup commands
  - ✅ Manual setup steps (if scripts fail)
  - ✅ Post-setup configuration
  - ✅ Verification steps
  - ✅ Troubleshooting guide
  - ✅ Update procedures
  - ✅ Uninstallation steps

---

## 🔄 Complete Workflow

### First-Time Setup (Ubuntu)

```bash
# 1. Clone repository (if from GitHub)
git clone https://github.com/YOUR_USERNAME/ai-compass.git
cd ai-compass

# 2. Run setup script
chmod +x setup_ubuntu.sh
bash setup_ubuntu.sh

# 3. Add Groq API key
nano .env
# Set: GROQ_API_KEY=your_actual_key_here

# 4. Activate environment
source venv/bin/activate

# 5. Start application
bash start.sh
```

### First-Time Setup (macOS)

```bash
# 1. Clone repository (if from GitHub)
git clone https://github.com/YOUR_USERNAME/ai-compass.git
cd ai-compass

# 2. Run setup script
chmod +x setup_macos.sh
bash setup_macos.sh

# 3. Add Groq API key
nano .env
# Set: GROQ_API_KEY=your_actual_key_here

# 4. Activate environment
source venv/bin/activate

# 5. Start application
bash start.sh
```

### Daily Usage

```bash
# 1. Navigate to project
cd ai-compass

# 2. Activate environment
source venv/bin/activate

# 3. Start application
bash start.sh

# The script will open two terminal windows automatically!
```

---

## 🎯 Scripts Comparison

| Feature | setup_ubuntu.sh | setup_macos.sh | start.sh |
|---------|----------------|----------------|----------|
| **Purpose** | First-time setup | First-time setup | Daily startup |
| **Installs System Packages** | ✅ Yes | ✅ Yes | ❌ No |
| **Installs Python** | ✅ Yes (apt) | ✅ Yes (brew) | ❌ No |
| **Installs PostgreSQL** | ✅ Yes (apt) | ✅ Yes (brew) | ❌ No |
| **Creates venv** | ✅ Yes | ✅ Yes | ❌ No |
| **Installs Python Packages** | ✅ Yes | ✅ Yes | ❌ No |
| **Creates Database** | ✅ Yes | ✅ Yes | ❌ No |
| **Runs Migrations** | ✅ Yes | ✅ Yes | ❌ No |
| **Sets up .env** | ✅ Yes | ✅ Yes | ❌ No |
| **Starts API** | ❌ No | ❌ No | ✅ Yes |
| **Starts Streamlit** | ❌ No | ❌ No | ✅ Yes |
| **Run Once** | ✅ Once | ✅ Once | 🔄 Every time |
| **Requires sudo** | ✅ Yes | ❌ No* | ❌ No |
| **Time Required** | ~5-10 min | ~10-15 min | ~5 sec |

*macOS setup only needs sudo for Homebrew installation if not present

---

## 🔍 Key Differences: Ubuntu vs macOS Scripts

### Package Manager
- **Ubuntu**: apt (native)
- **macOS**: Homebrew (installed by script if missing)

### PostgreSQL Setup
- **Ubuntu**: 
  - Uses `sudo -u postgres` to create database
  - System service via `systemctl`
- **macOS**: 
  - Uses current user to create database
  - Service via `brew services`

### sed Command
- **Ubuntu**: `sed -i` (in-place edit)
- **macOS**: `sed -i ''` (requires empty string for backup)

### Python Installation
- **Ubuntu**: Via PPA (deadsnakes)
- **macOS**: Via Homebrew

---

## 🚀 Why start.sh Works for Both Platforms

The `start.sh` script includes OS detection:

```bash
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS - uses osascript for Terminal.app
    osascript -e 'tell application "Terminal" to do script ...'
    
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux - uses gnome-terminal or konsole
    gnome-terminal -- bash -c "..."
    
else
    # Fallback - uses tmux or manual start
    tmux new-session -d -s aicompass-api
fi
```

**Conclusion**: **No separate mac_start.sh needed!** ✅

---

## 📝 What Each Script Does NOT Do

### Setup Scripts DON'T:
- ❌ Start the application (use `start.sh` for that)
- ❌ Configure Groq API key (you must do this manually)
- ❌ Modify system-wide Python/PostgreSQL settings
- ❌ Install Docker or other optional tools

### Start Script DOESN'T:
- ❌ Install any packages
- ❌ Create virtual environment
- ❌ Run database migrations
- ❌ Check if PostgreSQL is running (assumes setup is complete)

---

## ✅ Prerequisites Before Running Scripts

### Both Platforms
- ✅ Internet connection
- ✅ At least 2GB free disk space
- ✅ Admin/sudo privileges

### Ubuntu
- ✅ Ubuntu 20.04+ or Debian 11+
- ✅ `sudo` access

### macOS
- ✅ macOS 11 (Big Sur) or later
- ✅ Xcode Command Line Tools (installed by script if missing)

---

## 🔧 Making Scripts Executable

Before running for the first time:

```bash
# Make all scripts executable
chmod +x setup_ubuntu.sh
chmod +x setup_macos.sh
chmod +x start.sh
chmod +x apps/web/run.sh
```

Or all at once:
```bash
find . -name "*.sh" -type f -exec chmod +x {} \;
```

---

## 🎓 Advanced Usage

### Run Setup in Silent Mode (Less Output)

```bash
# Ubuntu
bash setup_ubuntu.sh 2>&1 | grep -E "(✓|✗|▶)"

# macOS
bash setup_macos.sh 2>&1 | grep -E "(✓|✗|▶)"
```

### Start in Background

```bash
bash start.sh --background
```

### Environment-Specific Setup

```bash
# Development
cp infra/.env.example .env.dev
sed -i 's/LOG_LEVEL=INFO/LOG_LEVEL=DEBUG/' .env.dev

# Production
cp infra/.env.example .env.prod
sed -i 's/API_RELOAD=true/API_RELOAD=false/' .env.prod
```

---

## 🐛 Common Issues

### "Permission denied" on setup scripts
```bash
chmod +x setup_*.sh
```

### "Virtual environment not activated" when starting
```bash
source venv/bin/activate
bash start.sh
```

### PostgreSQL not running after setup
```bash
# Ubuntu
sudo systemctl start postgresql

# macOS
brew services start postgresql@14
```

### Port already in use
```bash
# Kill processes on ports
lsof -ti:8000 | xargs kill -9  # API
lsof -ti:8501 | xargs kill -9  # Streamlit
```

---

## 📊 Script Execution Time

| Script | Ubuntu | macOS | Notes |
|--------|--------|-------|-------|
| setup_ubuntu.sh | 5-10 min | N/A | Depends on internet speed |
| setup_macos.sh | N/A | 10-15 min | Homebrew install adds time |
| start.sh | ~5 sec | ~5 sec | Opens terminals only |

---

## 🔄 Update Workflow

After pulling new code:

```bash
# 1. Activate environment
source venv/bin/activate

# 2. Update dependencies
pip install -r requirements.txt

# 3. Run new migrations
cd apps/api
alembic upgrade head
cd ../..

# 4. Restart application
bash start.sh
```

No need to re-run full setup script!

---

## 📚 Related Documentation

- **README.md** - Project overview
- **QUICKSTART.md** - Fast setup guide
- **SETUP_GUIDE.md** - Detailed setup manual (this document's companion)
- **PROJECT_STRUCTURE.md** - Architecture details
- **API_REFERENCE.md** - API documentation

---

## ✨ Summary

**You have 2 setup scripts:**
1. ✅ **setup_ubuntu.sh** - For Ubuntu/Linux (first-time setup)
2. ✅ **setup_macos.sh** - For macOS (first-time setup)

**You have 1 startup script:**
3. ✅ **start.sh** - For both platforms (daily use)

**No separate mac_start.sh needed** - the existing `start.sh` handles both macOS and Linux perfectly!

Run setup once, then use `start.sh` every time you want to run the application. 🚀
