# AI-Compass Application Prototype (mvp_v1)

This directory contains the **v1 Working Prototype** of AI-Compass. It is a full-stack platform designed to provide SMEs (Mittelstand) with an automated AI maturity assessment, industry benchmarking, and a strategic transformation roadmap.

---

## 🚀 Overview

The prototype transforms traditional manual consulting into a scalable digital experience. It guides users through an assessment across 7 dimensions of AI maturity, processes their input using a trained **ML v5 Intelligence Engine**, and delivers a high-fidelity visual report (Web & PDF).

### Core Value Proposition
- **Explainable Maturity**: Scores from 1 to 5 across 7 core dimensions.
- **Accurate Benchmarking**: Comparative analysis against 5 semantic archetypes (Traditionalist → AI-Driven Leader).
- **Strategic Visualization**: Interactive "Cluster Profile" with dynamic "You are here" badging.
- **Actionable Roadmap**: A phased (90/180/360 days) roadmap derived from strategic gap analysis.
- **Instant PDF Report**: Downloadable executive summary with vector-perfect branding.

---

## 🛠 Technology Stack

### Frontend
- **Framework**: React 18 with Vite
- **Styling**: Tailwind CSS + shadcn/ui (Premium components)
- **State Management**: React Context API + SessionStorage (Persistence)
- **Visualizations**: 
    - Recharts (Radar charts, Bar charts)
    - Custom SVG components (Cluster Profile)
- **Routing**: React Router v6

### Backend
- **Framework**: FastAPI (Python 3.10+)
- **ORM**: SQLAlchemy (PostgreSQL integration)
- **Data Validation**: Pydantic v2
- **Persistence**: PostgreSQL (Supabase)
- **PDF Generation**: ReportLab (Vector-based, High-Res)

### Intelligence (ML v5)
- **ClusterEngine**: K-Means clustering (5 archetypes) with PCA visualization.
- **StrategicGapAnalyzer**: Identifies structural imbalances in company maturity.
- **RoadmapGenerator**: Generates prioritized transformation steps.
- **Inference Engine**: Dedicated wrapper in `benchmarking_ai/ml_v5/inference.py` for real-time analysis.

```text
┌─────────────────────────────────────────────────────────────┐
│                       ML v5 System                          │
│                                                             │
│  ┌────────────────┐   ┌─────────────────┐   ┌─────────────┐ │
│  │ Cluster Engine │   │  Strategic Gap  │   │ Roadmap Gen │ │
│  │    (K-Means)   │   │ Analyzer (Rule) │   │    (KNN)    │ │
│  └───────┬────────┘   └────────┬────────┘   └──────┬──────┘ │
│          │                     │                   │        │
│          └─────────────────────┼───────────────────┘        │
│                                │                            │
│                                ▼                            │
│                     ┌──────────────────┐                    │
│                     │ Inference Engine │                    │
│                     └────────┬─────────┘                    │
│                              │                              │
└──────────────────────────────┼──────────────────────────────┘
                               │
                               ▼
                     ┌───────────────────┐
                     │  FastAPI Backend  │
                     └─────────┬─────────┘
                               │
                               ▼
                     ┌───────────────────┐
                     │   React Frontend  │
                     └───────────────────┘
```

---

## 📂 Project Structure

```text
Application_Prototype/mvp_v1/
├── backend/                # FastAPI Application Layer
│   ├── main.py             # Server entry point
│   ├── routers/            # API endpoints
│   ├── services/           # Business logic
│   └── ...
├── frontend/               # React Application Layer
│   ├── src/                # Components, Pages, Hooks
│   └── ...
├── setup.sh / start.sh     # Automation Scripts
└── ...

../../benchmarking_ai/      # Intelligence Engines (External Module)
└── ml_v5/                  # ML Models (ClusterEngine, RoadmapGenerator)
```

---

## 📋 Key Features & Logic

### 1. Assessment Wizard
- **One-Question-Per-Screen**: Minimizes cognitive load.
- **Automated Autosave**: Responses are saved to both InMemory session (backend) and SessionStorage (frontend), surviving refreshes.
- **Progress Tracking**: Real-time progress bar across 7 dimensions.
- **Robust Cache**: Invalidation logic (v1 -> v2) ensures data freshness.

### 2. Scoring Methodology
- **Weighted Averaging**: Each question and dimension has specific weights defined in the DB.
- **Scale**: Normalized to a 1.0 - 5.0 scale for industry comparability.

### 3. Industry Benchmarking & Visualization
- **Cluster Profile**: Visualizes the 5 maturity archetypes with a dynamic bouncing badge indicating user position.
- **Maturity Radar**: 7-axis radar chart comparing User vs. Industry vs. Leader.
- **Percentile Ranking**: "Top X%" calculation against the global dataset.

### 4. Executive Reporting
- **Web View**: Interactive dashboard with gradients and animations.
- **PDF Export**: Server-side generated PDF (Vector quality) matching the web design's branding (Black titles, specific fonts).

---

## ⚙️ Development Guide

### Environment Variables
Both frontend and backend require `.env` files. The `setup` scripts attempt to handle this, but for manual config:

**Backend (`backend/.env`)**:
```env
DATABASE_URL=postgresql://... (Supabase URL)
CORS_ORIGINS=["http://localhost:5173"]
```

**Frontend (`frontend/.env`)**:
```env
VITE_API_URL=http://localhost:8000
```

### Automation Scripts (Recommended)
- **Setup**: `setup.bat` (Win) or `./setup.sh` (Mac) - Installs Python venv, Pip deps, and Npm modules.
- **Start**: `start.bat` (Win) or `./start.sh` (Mac) - Runs both servers in parallel.
- **Stop**: `stop.bat` (Win) or `./stop.sh` (Mac) - Frees up ports 8000 and 5173.

### Prerequisite: Model Training
The AI Engine requires trained artifacts to function. Before starting the app for the first time, you must run the training script:

```bash
# From the project root (cd ../.. if inside mvp_v1)
python -m benchmarking_ai.ml_v5.train_models
```
*Note: This generates artifacts in `benchmarking_ai/ml_v5/model_artifacts/v5`.*

---

## 📡 API Endpoints

- `GET /api/v1/questionnaire`: Fetches the full question bank with metadata.
- `POST /api/v1/companies`: Registers a new company profile.
- `POST /api/v1/responses`: Initializes an assessment session.
- `PATCH /api/v1/responses/{id}/items`: Updates individual question answers (Autosave).
- `POST /api/v1/responses/{id}/complete`: Finalizes the assessment and persists to DB.
- `GET /api/v1/results/{id}/results`: Triggers ML analysis and returns the full JSON report.
- `GET /api/v1/results/{id}/pdf`: Generates and downloads the specialized PDF report.

---

## 🔗 Documentation Links
- [Implementation Plan](implementation_plan_working_prototype_v1.md)
- [Scoring Methodology](../../doc/scoring_methodology.md)
- [ML v5 Explanation](../../model_explanation.md)
