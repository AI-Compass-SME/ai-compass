# AI-Compass MVP

**AI-Compass** is a consulting-ready AI maturity assessment tool built with FastAPI, Streamlit, and PostgreSQL. It provides SME decision-makers with clear, actionable insights into their AI readiness through deterministic scoring, ML-based peer benchmarking, and LLM-generated recommendations.

## Core Features

- **7-Dimension Maturity Assessment**: Strategy, Data, Tech, People, Processes, Governance, Use Cases
- **Deterministic Scoring**: Rule-based, explainable, reproducible (0-100 scale + levels 1-5)
- **Peer Benchmarking**: K-Means clustering against synthetic peer dataset
- **Executive Recommendations**: LLM-generated quick wins and roadmaps (cached)
- **Visual Reports**: Radar charts, bar charts, and PDF export
- **Schema-Driven**: Hot-swappable questionnaire via JSON configuration

## Architecture

```
[ Streamlit UI ] → [ FastAPI Backend ]
                    ├─ Deterministic Scoring Engine
                    ├─ ML Benchmarking (K-Means)
                    ├─ LLM Text Generation (Groq)
                    └─ PostgreSQL Database
```

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy 2.x, Alembic, Pydantic v2
- **Frontend**: Streamlit, Plotly
- **Database**: PostgreSQL
- **ML**: scikit-learn (K-Means)
- **LLM**: Groq API
- **PDF**: ReportLab

## Project Structure

```
ai-compass/
├─ apps/
│  ├─ api/              # FastAPI backend
│  └─ web/              # Streamlit frontend
├─ core/
│  ├─ questionnaire/    # JSON schema loader
│  ├─ scoring/          # Deterministic scoring engine
│  ├─ ml/               # Benchmarking (K-Means + synthetic data)
│  ├─ llm/              # Groq LLM service
│  └─ reporting/        # PDF generation
├─ data/
│  └─ questionnaire/
│     └─ questions.json # Hot-swappable questionnaire schema
├─ infra/
│  └─ .env.example
├─ requirements.txt
└─ README.md
```

## Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Groq API Key (free tier available at https://console.groq.com)

## Installation & Setup

### 1. Clone and Navigate

```bash
cd ai-compass
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp infra/.env.example .env
```

Edit `.env` and set:
- `DATABASE_URL`: PostgreSQL connection string (e.g., `postgresql://user:pass@localhost:5432/aicompass`)
- `GROQ_API_KEY`: Your Groq API key
- `API_HOST`: API host (default: `0.0.0.0`)
- `API_PORT`: API port (default: `8000`)

### 5. Setup Database

Create the PostgreSQL database:

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE aicompass;
\q
```

Run Alembic migrations:

```bash
cd apps/api
alembic upgrade head
cd ../..
```

### 6. Run the Application

**Terminal 1 - Start FastAPI Backend:**

```bash
cd apps/api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Start Streamlit Frontend:**

```bash
cd apps/web
streamlit run Home.py
```

### 7. Access the Application

- **Streamlit UI**: http://localhost:8501
- **FastAPI Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health

## Usage Workflow

1. **Home** → Introduction and overview
2. **Company Snapshot** → Enter company metadata (industry, size, etc.)
3. **Assessment Wizard** → Answer 7-dimension questionnaire (21 questions)
4. **Review** → Verify answers before submission
5. **Complete Assessment** → Submit and process results
6. **Results Dashboard** → View overall score, dimension breakdown, radar/bar charts
7. **Benchmark** → See peer comparison and cluster placement
8. **Roadmap** → Review LLM-generated recommendations
9. **PDF Export** → Download comprehensive report

## Key Design Principles

### 1. Deterministic Scoring
- All scores/levels computed via explicit rules and weights
- LLMs **never** influence scoring logic
- Fully reproducible and auditable

### 2. Schema-Driven Questionnaire
- All questions, options, weights defined in `data/questionnaire/questions.json`
- Code dynamically reads schema at runtime
- No hardcoded question IDs in codebase

### 3. Dynamic Answer Storage
- Answers stored in EAV/long format (one row per question)
- No fixed columns per question → future-proof
- JSONB used for flexible metadata storage

### 4. LLM for Explanation Only
- LLM generates executive summaries and recommendations
- Results cached in database to reduce API calls
- Fallback to deterministic templates if LLM fails

### 5. ML for Benchmarking Optics
- K-Means clusters user against 300-800 synthetic peers
- Provides context ("AI Laggards" vs "AI Scalers")
- Mismatch detection (high score but low cluster → outlier)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/questionnaire` | Get questionnaire schema + metadata |
| POST | `/assessments` | Create new assessment |
| POST | `/assessments/{id}/responses` | Submit answers |
| POST | `/assessments/{id}/complete` | Finalize & compute results |
| GET | `/assessments/{id}` | Retrieve assessment details |
| GET | `/assessments/{id}/pdf` | Download PDF report |

## Database Schema

### Core Tables

1. **company_assessment**: Assessment metadata
2. **questionnaire_response**: Dynamic answer storage (EAV)
3. **maturity_scores**: Computed scores and levels
4. **benchmark_cluster_result**: ML benchmarking results
5. **llm_enrichment_cache**: Cached LLM outputs

See `apps/api/models/` for full schema definitions.

## Configuration

### Questionnaire Schema (`data/questionnaire/questions.json`)

The questionnaire is fully configurable via JSON:
- **Dimensions**: Define domains with weights
- **Questions**: Specify text, type, render mode, weights
- **Options**: Set labels, points (0-4), tags
- **Scoring Rules**: Configure level thresholds, aggregation methods

**Example Structure:**

```json
{
  "questionnaire_id": "ai-compass-mvp",
  "questionnaire_version": "2026-01-06",
  "dimensions": [
    {
      "id": "strategy_business_vision",
      "title": "Strategy & Business Vision",
      "weight": 1.0,
      "questions": [
        {
          "id": "sbv_01_strategy_defined",
          "text": "...",
          "type": "single_choice",
          "weight": 1.0,
          "options": [...]
        }
      ]
    }
  ],
  "scoring": {
    "levels_1_to_5_thresholds": [...]
  }
}
```

To update the questionnaire, simply edit `data/questionnaire/questions.json` and restart the API.

## Development

### Running Tests

```bash
cd apps/api
pytest tests/
```

### Database Migrations

Create new migration:

```bash
cd apps/api
alembic revision --autogenerate -m "Description"
```

Apply migrations:

```bash
alembic upgrade head
```

### Adding New Dimensions

1. Edit `data/questionnaire/questions.json`
2. Add new dimension object with questions
3. Restart API (no code changes needed)

## Troubleshooting

### Database Connection Issues

- Verify PostgreSQL is running: `pg_isready`
- Check `DATABASE_URL` in `.env`
- Ensure database exists: `psql -l`

### Port Already in Use

```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn main:app --port 8001
```

### LLM API Errors

- Verify `GROQ_API_KEY` is set correctly
- Check API quota at https://console.groq.com
- App will fall back to deterministic templates on failure

### Migrations Failing

```bash
# Reset migrations (CAUTION: drops all tables)
cd apps/api
alembic downgrade base
alembic upgrade head
```

## Production Considerations

While this MVP is designed for stability and clarity, consider these enhancements for production:

- [ ] Add authentication/authorization
- [ ] Implement rate limiting
- [ ] Add request validation middleware
- [ ] Set up monitoring (e.g., Prometheus + Grafana)
- [ ] Configure CORS properly for frontend domain
- [ ] Use connection pooling for database
- [ ] Add comprehensive error logging
- [ ] Implement backup/restore procedures
- [ ] Add multi-language support beyond German
- [ ] Optimize PDF generation for large reports

## License

Proprietary - Internal consulting tool

## Support

For issues or questions, contact the development team.

---

**Built with focus on: Stability • Explainability • Speed • Decision Clarity**
