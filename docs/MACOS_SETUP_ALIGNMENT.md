# macOS Setup Scripts Alignment

**Last Updated:** 2026-01-12  
**Status:** ✅ Aligned

## Summary

This document tracks the alignment of all macOS setup and startup scripts for the AI-Compass project to ensure consistency across the ecosystem.

---

## ✅ Changes Completed

### 1. Virtual Environment Naming
**Changed from:** `venv`  
**Changed to:** `.venv`

**Files Updated:**
- ✅ `start.sh` - All 8 occurrences updated (macOS, Linux, fallback modes)
- ✅ `setup_macos.sh` - VENV_NAME variable and user instructions updated
- ✅ `macos_app_config_setup.sh` - Already using `.venv`
- ✅ `.gitignore` - Already includes both `venv/` and `.venv/`

**Rationale:** 
- The new all-in-one script uses `.venv` (convention for hidden Python virtual environments)
- Consistency across all scripts prevents user confusion
- Both names are already gitignored

---

## 📋 Script Ecosystem Overview

### Primary Setup Scripts

| Script | Purpose | Status | Notes |
|--------|---------|--------|-------|
| `macos_app_config_setup.sh` | **New all-in-one** setup & start | ✅ Complete | Interactive .env, runs in single terminal |
| `setup_macos.sh` | **Traditional** environment setup | ✅ Updated | Separate setup, uses `start.sh` to run |
| `macos_system_libs.sh` | **Optional** system libraries | ✅ Ready | Best-effort Homebrew package installation |
| `start.sh` | **Universal** startup script | ✅ Updated | Platform-aware (macOS/Linux/fallback) |
| `stop.sh` | **Universal** shutdown script | ⚠️ Check | May need .venv update |
| `config.sh` | Interactive .env generator | ⚠️ Check | Verify consistency |

### Platform Comparison

| Feature | macOS All-in-One | Traditional (setup_macos.sh) |
|---------|------------------|------------------------------|
| Homebrew check/install | ✅ Yes | ✅ Yes |
| Python ≥3.10 | ✅ Yes | ✅ Yes |
| PostgreSQL | ✅ Yes | ✅ Yes |
| System libraries | Optional separate script | ✅ Built-in |
| Virtual env name | `.venv` | ✅ Updated to `.venv` |
| .env creation | ✅ Interactive wizard | Template copy |
| DB bootstrap | ✅ Idempotent SQL | psql commands |
| Alembic migrations | ✅ Yes | ✅ Yes |
| Service startup | ✅ Built-in (1 terminal) | Uses `start.sh` (2 terminals) |
| Verification | ❌ No | ✅ `check_setup.py` |

---

## 🔧 Recommended Next Steps

### 1. **Verify `stop.sh`** (Priority: Medium)
Check if `stop.sh` has any references to `venv` that need updating:

```bash
grep -n "venv" stop.sh
```

### 2. **Review `config.sh`** (Priority: Low)
Ensure the standalone config script is consistent with the all-in-one `.env` wizard:

```bash
# Check if config.sh is still used or superseded
cat config.sh | grep -A5 "DB_USER\|GROQ"
```

### 3. **Add Verification to All-in-One** (Priority: Medium)
Consider adding `check_setup.py` to `macos_app_config_setup.sh`:

```bash
# At the end, before starting services:
print_step "Verifying Installation"
python check_setup.py || warn "Some checks failed"
```

### 4. **Document the Workflow Options** (Priority: High)
Users now have **two paths**:

#### Option A: All-in-One (Quickstart)
```bash
./macos_app_config_setup.sh
# Everything in one command + one terminal
```

#### Option B: Traditional (More Control)
```bash
# 1. Optional: Install system libraries
bash macos_system_libs.sh

# 2. Setup environment
bash setup_macos.sh

# 3. Activate venv
source .venv/bin/activate

# 4. Start services
bash start.sh
```

### 5. **Update Documentation** (Priority: High)
Update the following files to reflect the dual-path setup:

- [ ] `README.md` - Add macOS quickstart section
- [ ] `QUICKSTART.md` - Document both approaches
- [ ] `SETUP_GUIDE.md` - Clarify when to use each method
- [ ] `SETUP_SCRIPTS_README.md` - Update script descriptions

---

## 📊 Dependency Coverage Analysis

### Core Dependencies (All Scripts)

| Dependency | macos_app_config_setup.sh | setup_macos.sh | Notes |
|------------|---------------------------|----------------|-------|
| **Homebrew** | ✅ Auto-install | ✅ Auto-install | Both handle Apple Silicon PATH |
| **Python 3.10+** | ✅ Yes | ✅ Yes | Both install if missing |
| **PostgreSQL** | ✅ Yes | ✅ v14 pinned | All-in-one uses default version |
| **Git** | ❌ No | ✅ Yes | Consider adding to all-in-one |
| **System Libs** | 🔗 Separate script | ✅ Built-in | See `macos_system_libs.sh` |

### System Libraries Comparison

**Traditional Setup (`setup_macos.sh`):**
```bash
openssl readline sqlite3 xz zlib jpeg freetype
```

**New Separate Script (`macos_system_libs.sh`):**
```bash
openssl@3 readline sqlite xz zlib jpeg freetype 
libpng libffi pkg-config cmake
```

**Recommendation:** The separate script is more comprehensive and has better error handling (best-effort).

---

## 🎯 Integration Options

### Recommended: Keep Both Approaches

**Why?**
1. **All-in-one** = Best for first-time users, demos, workshops
2. **Traditional** = Best for development, troubleshooting, CI/CD

### Optional Enhancement

Create a wrapper script that asks the user which approach they prefer:

```bash
#!/bin/bash
# macos_setup.sh (wrapper)

echo "How would you like to set up AI-Compass?"
echo "1) Quick setup (all-in-one, recommended for first time)"
echo "2) Step-by-step (traditional, more control)"
read -p "Choose [1/2]: " choice

case $choice in
  1) bash macos_app_config_setup.sh ;;
  2) 
    bash macos_system_libs.sh
    bash setup_macos.sh
    echo "✓ Setup complete. Run: source .venv/bin/activate && bash start.sh"
    ;;
  *) echo "Invalid choice" ;;
esac
```

---

## ⚠️ Known Differences

### Service Startup Behavior

| Aspect | All-in-One | start.sh |
|--------|------------|----------|
| API process | Background | New terminal (macOS) |
| Streamlit | Foreground | New terminal (macOS) |
| Terminal count | 1 | 3 (original + API + Streamlit) |
| Port conflicts | Checked with `lsof` | Not checked |
| Cleanup | Signal trap (EXIT/INT/TERM) | Manual Ctrl+C in each terminal |

**Implication:** Users may prefer different methods based on their workflow.

---

## 📝 Testing Checklist

Before releasing to users, verify:

- [ ] Fresh macOS install: Run all-in-one script
- [ ] Fresh macOS install: Run traditional flow
- [ ] Existing setup: Re-run all-in-one (idempotency)
- [ ] Verify `.venv` is created and activated correctly
- [ ] Verify both API and Streamlit start successfully
- [ ] Verify database migrations run
- [ ] Check port conflict detection
- [ ] Test stop.sh with `.venv`
- [ ] Update all markdown documentation

---

## 🔗 Related Files

- [macos_app_config_setup.sh](file:///wsl.localhost/Ubuntu/home/sinai/bootcamp/capstone/ai-compass/macos_app_config_setup.sh) - New all-in-one script
- [macos_system_libs.sh](file:///wsl.localhost/Ubuntu/home/sinai/bootcamp/capstone/ai-compass/macos_system_libs.sh) - System library installer
- [setup_macos.sh](file:///wsl.localhost/Ubuntu/home/sinai/bootcamp/capstone/ai-compass/setup_macos.sh) - Traditional setup script
- [start.sh](file:///wsl.localhost/Ubuntu/home/sinai/bootcamp/capstone/ai-compass/start.sh) - Universal startup script
- [.gitignore](file:///wsl.localhost/Ubuntu/home/sinai/bootcamp/capstone/ai-compass/.gitignore) - Includes both venv variations

---

## 🎓 Best Practices Applied

1. ✅ **Consistency** - All scripts now use `.venv`
2. ✅ **Idempotency** - Scripts can be safely re-run
3. ✅ **Error Handling** - Best-effort approach for optional components
4. ✅ **Platform Detection** - Scripts adapt to macOS/Linux
5. ✅ **User Feedback** - Color-coded output, clear steps
6. ✅ **Security** - .env files with password confirmation
7. ✅ **Flexibility** - Multiple setup paths for different use cases

---

**Question for User:** Should we create the wrapper script or document the two paths separately?
