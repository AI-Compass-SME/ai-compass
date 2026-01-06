# MASTER PROMPT — Build AI-Compass MVP (FastAPI + Streamlit + Postgres)

You are my senior engineering partner. Build a “consulting-ready” AI maturity assessment MVP called **AI-Compass**. Be ruthless about scope: **stability, explainability, speed > novelty**. The product’s differentiation is **decision clarity**, not “AI magic”.

## Core Principles (NON-NEGOTIABLE)
1) **Scoring is deterministic** (rule/weight-based).  
   - LLMs must **never** influence scores, levels, or benchmarking.
2) **ML is only for benchmarking optics** (peer grouping), not “truth”.  
   - Use **K-Means** on a synthetic dataset and the user’s structured answers.
3) **LLMs explain — they do not decide.**  
   - Use LLM only to generate executive-readable text (summary, recommendations), and cache results.
4) **Questionnaire is schema-driven and hot-swappable**:  
   - All questions/options/weights live in a JSON file in the repo.
   - We will replace that JSON later without code changes. Your code must not assume any fixed IDs beyond what it reads from the JSON.
5) **FastAPI is required** (clean API contracts, async, OpenAPI docs).
6) **Postgres is required** (team decision).
7) **DB must not use fixed columns per question**. Answers must be stored dynamically using question IDs (EAV/long-format + JSONB where helpful).

---

## Product Definition (MVP)

### Target user
SME decision makers (CEO/COO/Head of IT/Digital). They want clarity and a first roadmap.

### Dimensions (final)
- Strategy & Business Vision
- Data Maturity
- Tech Infrastructure
- People & Culture
- Processes & Scaling
- Governance & Compliance
- Use Cases & Business Value

### Questionnaire Rules
- For each dimension: **min 3, max 5** questions.
- Answers are **multiple choice**, **radio**, or **selectable tag-like buttons** (no free text required in MVP).
- Each option has a **points value** (0..4) and each question has a **weight**.
- Dimension score = weighted average (normalized to 0–100).
- Level mapping (1–5) via thresholds (config-driven; read from JSON).
- Overall score = weighted average of dimension scores (dimension weights read from JSON).

### Outputs (what user gets)
- Overall score (0–100) + overall level (1–5)
- Dimension scores (7) + levels (1–5) + “drivers” (top reasons)
- Peer benchmark:
  - cluster label (e.g., “AI Laggards / Curious / Experimenters / Scalers”)
  - percentile vs synthetic peers
  - **mismatch detection**: “You score high but cluster with lower peers” (or vice versa)
- Recommendations:
  - Quick Wins (0–30 days)
  - Roadmap: 90 days / 6 months / 12 months
- PDF report export

---

## Architecture (Simple, defensible)

[ Streamlit UI ]  → calls →  [ FastAPI ]
                         |-> deterministic scoring engine
                         |-> ML benchmarking (K-Means)
                         |-> LLM text generation (Groq) + cache
                         └-> Postgres persistence

Do NOT build React. Do NOT build RAG. Do NOT use embeddings/deep learning.

---

## Tech Stack

### Backend
- FastAPI (async)
- SQLAlchemy 2.x + Alembic migrations
- Postgres
- Pydantic v2 models

### UI
- Streamlit multi-page app (exec-friendly layout)
- Plotly:
  - **Radar/Spider chart** for the 7 dimensions overview
  - **Bar chart** sorted by score (low → high) for readability
- Tag-like selectable buttons for certain questions (UI only; stored as option IDs)

### ML
- scikit-learn K-Means
- Synthetic dataset generator (seeded, reproducible)

### LLM
- Groq client (`groq`) for text only
- `httpx` for HTTP needs
- `tenacity` for retries
- Cache LLM results in DB (table: llm_enrichment_cache)

### PDF
- reportlab (simple, consistent)

---

## Repository Deliverables (Generate all files)

### Folder structure
.
├─ apps/
│  ├─ api/                      # FastAPI
│  │  ├─ main.py
│  │  ├─ routers/
│  │  ├─ services/
│  │  ├─ models/
│  │  ├─ schemas/
│  │  ├─ db/
│  │  └─ tests/
│  └─ web/                      # Streamlit
│     ├─ Home.py
│     ├─ pages/
│     └─ components/
├─ core/
│  ├─ questionnaire/            # JSON loader + validation
│  ├─ scoring/                  # deterministic scoring
│  ├─ ml/                       # synthetic data + KMeans benchmarking
│  ├─ llm/                      # groq text generation + caching
│  └─ reporting/                # PDF report builder
├─ data/
│  └─ questionnaire/
│     └─ questions.json         # PROVIDED BY USER (hot-swappable)
├─ infra/
│  └─ .env.example
├─ requirements.txt
└─ README.md

IMPORTANT:
- `data/questionnaire/questions.json` is provided. Load it at runtime.
- Never hardcode question IDs, dimension IDs, or option IDs in code.

---

## Database Design (Postgres; dynamic answers; NO fixed question columns)

### Tables (minimum)
1) company_assessment
- id (uuid pk)
- company_meta (jsonb)   # industry, employee_band, etc.
- questionnaire_id (text)
- questionnaire_version (text)
- questionnaire_hash (text)
- status (text: draft|completed)
- created_at, completed_at

2) questionnaire_response  (EAV / long format; one row per answered question)
- id (uuid pk)
- assessment_id (uuid fk)
- dimension_id (text)
- question_id (text)
- answer_type (text)
- selected_option_ids (jsonb)   # array of option IDs (works for single & multi & tags)
- points_snapshot (numeric)     # aggregated points after selection
- weight_snapshot (numeric)     # question weight at time of answering
- answered_at (timestamptz)

3) maturity_scores
- assessment_id (uuid pk fk)
- overall_score (numeric)
- overall_level (int)
- dimension_scores (jsonb)  # {dimension_id: {title, score, level, drivers[]}}
- created_at

4) benchmark_cluster_result (optional but recommended)
- assessment_id (uuid pk fk)
- model_version (text)
- cluster_id (int)
- cluster_label (text)
- percentile (numeric)
- mismatch_flag (bool)
- mismatch_note (text)

5) llm_enrichment_cache
- id (uuid pk)
- cache_key (text unique)
- payload (jsonb)          # LLM output JSON
- created_at

### Indexes
- questionnaire_response: (assessment_id), (question_id), (dimension_id)
- llm_enrichment_cache: unique(cache_key)

---

## Backend API Requirements (FastAPI)

### Endpoints
- GET  /health
- GET  /questionnaire
  - returns the loaded questions.json + metadata (id/version/hash)
- POST /assessments
  - body: company_meta
  - server computes questionnaire_id/version/hash from loaded JSON
  - returns: assessment_id
- POST /assessments/{assessment_id}/responses
  - body: list of answers (dimension_id, question_id, selected_option_ids)
  - persists into questionnaire_response (upsert allowed)
- POST /assessments/{assessment_id}/complete
  - runs deterministic scoring
  - runs benchmarking (KMeans) using synthetic peers
  - runs LLM text generation for executive copy (cached)
  - stores maturity_scores + benchmark_cluster_result
  - returns results payload (see “UI-ready response”)
- GET  /assessments/{assessment_id}
  - returns assessment header + answers + results
- GET  /assessments/{assessment_id}/pdf
  - generates PDF and streams it (or fetches stored if you store PDFs)

NOTE:
- `uvicorn` is OPTIONAL (dev convenience). If you use it, include it; otherwise run FastAPI via your preferred method.

---

## UI-Ready Response Requirement (Charts must render without extra logic)
The `complete` and `get assessment` response must include:

- `overall`: { score_0_100, level_1_5 }
- `dimension_scores`: array of objects (already includes display titles), example:
  - { dimension_id, title, score_0_100, level_1_5, drivers: [{question_id, question_text, selected_label, points}] }
- `chart_data`:
  - `radar`: { labels: [titles...], values: [scores...], min: 0, max: 100 }
  - `bars`:  { labels: [titles sorted low→high], values: [scores sorted], min: 0, max: 100 }
- `benchmark`: { cluster_label, percentile, mismatch_flag, mismatch_note }
- `recommendations`: { executive_summary, quick_wins[], roadmap:{days_90[], months_6[], months_12[]}, risks[] }

This way Streamlit can directly render Radar + Bar charts via Plotly.

---

## Deterministic Scoring Service
- Load questionnaire JSON
- Validate answered IDs exist
- Compute:
  - question score = option points (multi-choice/tags aggregation via average)
  - dimension score = weighted avg of questions (normalize 0–100)
  - overall score = weighted avg of dimensions (dimension weights)
  - levels via thresholds from JSON
- Drivers (explainability):
  - per dimension: pick 2–3 lowest-scoring questions
  - include question text + selected option label + points

---

## ML Benchmark Service (K-Means)
- Feature vector from answers:
  - one feature per question_id (0..4 points), stable ordering by sorting question_id
- Synthetic peers:
  - Generate N=300–800 synthetic profiles with realistic distributions
  - seeded generator (reproducible)
- Train KMeans on synthetic features
- Predict user cluster
- Percentile:
  - compare overall_score to synthetic distribution (simple + explainable)
- Cluster labels by centroid maturity:
  - lowest -> “AI Laggards”
  - next -> “AI Curious”
  - next -> “AI Experimenters”
  - highest -> “AI Scalers”
- Mismatch detection (deterministic):
  - high score but low cluster (or vice versa) → mismatch_flag + short note

---

## LLM Service (Groq) — Text only
- Inputs:
  - company_meta
  - dimension scores + drivers
  - benchmark summary (cluster label + mismatch note)
- Output must be strict JSON:
  - executive_summary (max 2 sentences)
  - quick_wins (3–5 items)
  - roadmap (90d, 6m, 12m; 3–5 items each)
  - risks (3–5 items)
- Temperature low, strict prompts, no buzzwords
- Cache by stable key
- Failure fallback: deterministic templates so app always works

---

## Streamlit App Requirements (pages + workflow)

### Workflow
Home → Company Snapshot → Assessment Wizard (7 steps) → Review → Results Dashboard → Benchmark → Roadmap → PDF Export → History

### Results Dashboard MUST include:
- Plotly **Radar/Spider** chart for all 7 dimensions
- Plotly **Bar** chart sorted low→high
- “Top Focus Areas” (lowest 3 dimensions)
- “Why?” drivers per dimension

---

## Infrastructure (No Docker)
- Provide `.env.example` with DATABASE_URL, GROQ_API_KEY, settings
- Provide local run instructions in README:
  - run migrations
  - run API
  - run Streamlit

---

## requirements.txt
Include:
streamlit, plotly, fastapi, sqlalchemy, psycopg[binary], alembic, pydantic, python-dotenv, pandas, numpy, scikit-learn, groq, httpx, tenacity, rich, reportlab
Optional:
uvicorn (only if used for dev server)

---

## Quality Bar / Testing
- Unit tests for scoring (known answers → known score)
- JSON validation tests
- Feature vector consistency test (ordering by question_id)
- Smoke test: create assessment → answer → complete → results → charts → PDF

---

## Output Expectations
1) Generate all code + configs + README.
2) Keep code readable and minimal.
3) No feature creep beyond defined MVP.
4) Ensure OpenAPI docs are clean and demonstrate endpoints.
