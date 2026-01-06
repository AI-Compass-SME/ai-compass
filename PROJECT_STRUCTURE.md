# AI-Compass Project Structure

```
ai-compass/
│
├── README.md                          # Main documentation
├── QUICKSTART.md                      # Setup guide
├── requirements.txt                   # Python dependencies
├── check_setup.py                     # Startup validation script
├── .gitignore                         # Git ignore rules
│
├── infra/                             # Infrastructure config
│   └── .env.example                   # Environment template
│
├── data/                              # Data files
│   └── questionnaire/
│       └── questions.json             # Assessment schema (HOT-SWAPPABLE)
│
├── core/                              # Core business logic
│   ├── __init__.py
│   │
│   ├── questionnaire/                 # Questionnaire loader
│   │   ├── __init__.py
│   │   └── loader.py                  # JSON loader + validation
│   │
│   ├── scoring/                       # Deterministic scoring
│   │   ├── __init__.py
│   │   └── engine.py                  # Pure rule-based scoring
│   │
│   ├── ml/                            # ML benchmarking
│   │   ├── __init__.py
│   │   ├── synthetic_data.py          # Synthetic peer generator
│   │   └── benchmark.py               # K-Means clustering
│   │
│   ├── llm/                           # LLM integration
│   │   ├── __init__.py
│   │   └── groq_service.py            # Groq API + caching
│   │
│   └── reporting/                     # PDF generation
│       ├── __init__.py
│       └── pdf_generator.py           # ReportLab PDF builder
│
├── apps/                              # Applications
│   │
│   ├── api/                           # FastAPI backend
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app entry point
│   │   ├── alembic.ini                # Alembic config
│   │   │
│   │   ├── db/                        # Database layer
│   │   │   ├── __init__.py
│   │   │   └── database.py            # SQLAlchemy setup
│   │   │
│   │   ├── models/                    # ORM models
│   │   │   ├── __init__.py
│   │   │   └── assessment.py          # Assessment tables (EAV)
│   │   │
│   │   ├── schemas/                   # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   └── assessment.py          # Request/response models
│   │   │
│   │   ├── routers/                   # API endpoints
│   │   │   ├── __init__.py
│   │   │   └── assessments.py         # All CRUD + complete logic
│   │   │
│   │   ├── alembic/                   # Database migrations
│   │   │   ├── env.py                 # Alembic environment
│   │   │   ├── script.py.mako         # Migration template
│   │   │   └── versions/
│   │   │       └── 001_initial_schema.py
│   │   │
│   │   └── tests/                     # Unit tests
│   │       └── test_scoring.py        # Smoke tests
│   │
│   └── web/                           # Streamlit frontend
│       ├── .env.example               # Web env template
│       ├── Home.py                    # Home page (entry point)
│       │
│       └── pages/                     # Streamlit pages
│           ├── 1_Company_Snapshot.py  # Company metadata form
│           ├── 2_Assessment.py        # Multi-step questionnaire
│           └── 3_Results.py           # Results dashboard + charts
│
└── [Not included but would be added:]
    ├── .agent/workflows/              # Agent workflows (if applicable)
    ├── docker-compose.yml             # Docker setup (future)
    └── deployment/                    # Deployment scripts (future)
```

## Key Files Explained

### Configuration
- **`infra/.env.example`**: Template for environment variables (DB, API keys, settings)
- **`data/questionnaire/questions.json`**: Complete assessment schema (dynamic, hot-swappable)

### Core Services (Isolated, Testable)
- **`core/questionnaire/loader.py`**: Loads & validates questions.json
- **`core/scoring/engine.py`**: Deterministic scoring engine (NO LLM influence)
- **`core/ml/benchmark.py`**: K-Means clustering vs synthetic peers
- **`core/llm/groq_service.py`**: LLM recommendations with caching & fallback
- **`core/reporting/pdf_generator.py`**: PDF report builder

### Backend API (FastAPI)
- **`apps/api/main.py`**: Entry point, startup, health check
- **`apps/api/models/assessment.py`**: ORM models (EAV pattern for dynamic answers)
- **`apps/api/schemas/assessment.py`**: Pydantic models for API validation
- **`apps/api/routers/assessments.py`**: All endpoints (7 routes)
- **`apps/api/alembic/`**: Database migration system

### Frontend (Streamlit)
- **`apps/web/Home.py`**: Landing page + navigation
- **`apps/web/pages/1_Company_Snapshot.py`**: Collect company info
- **`apps/web/pages/2_Assessment.py`**: Multi-step wizard (7 dimensions, 21 questions)
- **`apps/web/pages/3_Results.py`**: Dashboard with charts, benchmark, recommendations, PDF download

## Data Flow

```
User → Streamlit UI
         ↓
    POST /assessments (create)
         ↓
    POST /assessments/{id}/responses (submit answers)
         ↓
    POST /assessments/{id}/complete
         ↓
    Core Services:
      1. ScoringEngine → dimension/overall scores
      2. BenchmarkService → K-Means clustering
      3. LLMService → groq recommendations (cached)
         ↓
    Save to PostgreSQL (EAV tables)
         ↓
    Return results to UI
         ↓
    Display: Charts (Plotly) + Recommendations
         ↓
    GET /assessments/{id}/pdf → Download report
```

## Database Schema

```
company_assessment (1)
  ├── id (UUID, PK)
  ├── company_meta (JSONB)
  ├── questionnaire_id, version, hash
  ├── status (draft|completed)
  └── timestamps

questionnaire_response (N) ← EAV pattern
  ├── id (UUID, PK)
  ├── assessment_id (FK)
  ├── dimension_id, question_id (from JSON)
  ├── selected_option_ids (JSONB array)
  ├── points_snapshot, weight_snapshot
  └── answered_at

maturity_scores (1)
  ├── assessment_id (PK, FK)
  ├── overall_score, overall_level
  ├── dimension_scores (JSONB)
  └── created_at

benchmark_cluster_result (1)
  ├── assessment_id (PK, FK)
  ├── model_version
  ├── cluster_id, cluster_label
  ├── percentile, mismatch_flag
  └── created_at

llm_enrichment_cache (N)
  ├── id (UUID, PK)
  ├── cache_key (unique)
  ├── payload (JSONB)
  └── created_at
```

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Health check |
| GET | `/questionnaire` | Get schema + metadata |
| POST | `/assessments` | Create new assessment |
| POST | `/assessments/{id}/responses` | Submit answers |
| POST | `/assessments/{id}/complete` | Compute results |
| GET | `/assessments/{id}` | Get full assessment |
| GET | `/assessments/{id}/pdf` | Download PDF |

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | FastAPI | Async REST API |
| **Frontend** | Streamlit | Rapid UI prototyping |
| **Database** | PostgreSQL | Relational storage |
| **ORM** | SQLAlchemy 2.x | Database abstraction |
| **Migrations** | Alembic | Schema versioning |
| **Validation** | Pydantic v2 | Type safety |
| **ML** | scikit-learn | K-Means clustering |
| **LLM** | Groq (Llama 3.1) | Text generation |
| **Charts** | Plotly | Interactive visualizations |
| **PDF** | ReportLab | Report generation |

## Design Principles In Action

1. **Schema-Driven**: questions.json is loaded at runtime, no hardcoded IDs
2. **EAV Storage**: Dynamic answer tables adapt to schema changes
3. **Deterministic Scoring**: Pure functions, fully reproducible
4. **LLM as Tool**: Only for text, with caching & fallback
5. **API-First**: Clean contracts, OpenAPI docs
6. **Separation of Concerns**: Core logic isolated from API/UI

---

**This structure ensures the codebase is maintainable, testable, and ready for production hardening.**
