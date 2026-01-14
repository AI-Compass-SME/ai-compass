# AI-Compass Quick Start Guide

## Prerequisites Check

Before starting, ensure you have:

- [ ] Python 3.10+ installed (`python --version`)
- [ ] PostgreSQL 14+ installed and running
- [ ] Groq API key (get free at https://console.groq.com)
- [ ] Git (optional, for version control)

## Step-by-Step Setup

### 1. Create PostgreSQL Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE aicompass;

# Create user (optional)
CREATE USER aicompass_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE aicompass TO aicompass_user;

# Exit
\q
```

### 2. Setup Python Environment

```bash
# Navigate to project
cd ai-compass

# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy environment template
cp infra/.env.example .env

# Edit .env file
nano .env  # or use your preferred editor
```

**Required .env values:**

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/aicompass
GROQ_API_KEY=gsk_your_groq_api_key_here
```

### 4. Run Database Migrations

```bash
cd apps/api

# Run Alembic migrations
alembic upgrade head

# Verify tables created
psql -U postgres -d aicompass -c "\dt"

# Go back to project root
cd ../..
```

Expected output: You should see tables listed:
- company_assessment
- questionnaire_response
- maturity_scores
- benchmark_cluster_result
- llm_enrichment_cache
- alembic_version

### 5. Test Core Modules (Optional but Recommended)

```bash
# Run smoke tests
cd apps/api
python tests/test_scoring.py

# Expected output: All tests passed
cd ../..
```

### 6. Start the Backend API

**Terminal 1 - FastAPI:**

```bash
cd apps/api

# Start with uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or run directly (if configured in main.py)
python main.py
```

**Verify API is running:**
- Open browser: http://localhost:8000/health
- Expected: `{"status": "healthy", ...}`
- API docs: http://localhost:8000/docs

### 7. Start the Frontend (Streamlit)

**Terminal 2 - Streamlit:**

```bash
cd apps/web

# Copy env template (if not done)
cp .env.example .env

# Start Streamlit
streamlit run Home.py
```

**Access the app:**
- Streamlit will auto-open browser at: http://localhost:8501

### 8. Complete Your First Assessment

1. Click **"🚀 Assessment starten"**
2. Fill Company Snapshot form
3. Answer 21 questions across 7 dimensions (~12 min)
4. View your results:
   - Overall score & level
   - Dimension breakdown
   - Radar & bar charts
   - Benchmark cluster
   - LLM recommendations
5. Download PDF report

## Troubleshooting

### Database Connection Error

**Error:** `sqlalchemy.exc.OperationalError: could not connect to server`

**Solutions:**
1. Check PostgreSQL is running: `pg_isready`
2. Verify DATABASE_URL in `.env`
3. Check PostgreSQL logs: `tail -f /var/log/postgresql/postgresql-14-main.log`

### API Won't Start

**Error:** `ModuleNotFoundError: No module named 'core'`

**Solutions:**
1. Ensure you're in the right directory: `pwd` should show `.../ai-compass/apps/api`
2. Check Python path is set correctly
3. Reinstall dependencies: `pip install -r ../../requirements.txt`

### Questionnaire Not Loading

**Error:** `FileNotFoundError: Questionnaire file not found`

**Solutions:**
1. Check `QUESTIONNAIRE_PATH` in `.env` or use default
2. Verify file exists: `ls -la ../../data/questionnaire/questions.json`
3. Check file permissions

### Groq API Errors

**Error:** `Authentication failed` or `Invalid API key`

**Solutions:**
1. Verify GROQ_API_KEY in `.env`
2. Check quota at https://console.groq.com
3. App will fall back to deterministic templates if LLM fails (this is intentional)

### Port Already in Use

**Error:** `Address already in use`

**Solutions:**

```bash
# Find process using port 8000
lsof -ti:8000

# Kill it
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn main:app --port 8001
```

### Streamlit Won't Connect to API

**Error:** API offline message in sidebar

**Solutions:**
1. Check API is running on port 8000
2. Verify `API_URL` in `apps/web/.env` is `http://localhost:8000`
3. Check firewall settings

## Verification Checklist

After setup, verify everything works:

- [ ] Database accessible: `psql -U postgres -d aicompass -c "SELECT 1"`
- [ ] Migrations applied: Tables exist in database
- [ ] API health check: http://localhost:8000/health returns 200
- [ ] API docs accessible: http://localhost:8000/docs
- [ ] Streamlit loads: http://localhost:8501
- [ ] Questionnaire loaded: Check API sidebar or /questionnaire endpoint
- [ ] Can create assessment via UI
- [ ] Can submit answers
- [ ] Results calculate successfully
- [ ] PDF downloads

## Next Steps

Once running:

1. **Explore the API:** http://localhost:8000/docs
2. **Customize questionnaire:** Edit `data/questionnaire/questions.json` and restart API
3. **Review results:** Check database tables for stored assessments
4. **Adjust scoring:** Modify weights/thresholds in questions.json
5. **Tune ML:** Change synthetic peer count or cluster count in `.env`

## Development Tips

### Hot Reload

- **API:** Use `--reload` flag (already in instructions)
- **Streamlit:** Auto-reloads on file changes
- **Questionnaire:** Restart API after editing questions.json

### Database Inspection

```bash
# Connect to database
psql -U postgres -d aicompass

# List tables
\dt

# View assessments
SELECT id, status, created_at FROM company_assessment;

# View scores
SELECT assessment_id, overall_score, overall_level FROM maturity_scores;

# Exit
\q
```

### Reset Database (CAUTION: Deletes all data!)

```bash
cd apps/api

# Downgrade all migrations
alembic downgrade base

# Re-run migrations
alembic upgrade head

cd ../..
```

## Production Deployment (Future)

This MVP is designed for local/demo use. For production:

1. Use environment-specific .env files
2. Configure CORS properly in main.py
3. Add authentication/authorization
4. Use production WSGI server (gunicorn/uvicorn workers)
5. Set up Nginx reverse proxy
6. Enable SSL/TLS
7. Configure database connection pooling
8. Add monitoring (Prometheus/Grafana)
9. Implement rate limiting
10. Set up automated backups

## Support & Issues

- Check logs: Both API and Streamlit print helpful error messages
- Review code comments for implementation details
- Consult README.md for architecture overview

---

**Congratulations! You now have AI-Compass running locally.** 🎉
