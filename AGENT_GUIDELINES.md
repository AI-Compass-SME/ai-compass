
# AI Agent Guidelines & Project Context

> [!IMPORTANT]
> **To any AI Agent reading this:** You must adhere to these guidelines to ensure project consistency, architectural integrity, and production reliability.

---

## 1. Project Essence & Core Concept
**The AI Compass** is a strategic AI maturity assessment platform for SMEs (Mittelstand). It helps businesses understand their AI readiness through:
- **Structured Assessment**: Weighted questionnaire across 7 dimensions (one question per screen).
- **ML Inference (ml_v5)**: Hybrid K-Means clustering and Z-Score anomaly detection to identify strategic gaps and industry benchmarks (~500+ company profiles).
- **Dynamic Roadmaps**: A 3-phase prioritized roadmap generated using KNN peer analysis and LLM-enhanced explanations.
- **Bilingual Delivery**: Full EN / DE localization via `react-i18next`. Default language is **German**.

**Rule:** Do not deviate from this core SME-focused strategic assessment model unless explicitly instructed by the user.

---

## 2. Technical Architecture & Deployment

### Repository Strategy
The project uses a **Dual-Repository Strategy** to separate development from the production environment:

- **Development Repo (Source):** `AI-Compass-SME/ai-compass`
  - Active application code: `Application_Prototype/mvp_v1/`
  - ML logic: `benchmarking_ai/ml_v5/`
- **Production Repo (Target):** `AI-Compass-SME/the-ai-compass.de`
  - Flattened structure: `/backend`, `/frontend`, `/backend/modules/benchmarking_ai`
  - Synced automatically via GitHub Actions on merge to `main`

### The Production Sync Rule
> **Never make direct changes to the production repository.**
1. All code changes must happen in the `ai-compass` (dev) repo under `Application_Prototype/mvp_v1/`.
2. Changes are synchronized to production automatically via GitHub Actions when merged into `main`.
3. If asked to "fix production", apply the fix in the corresponding `Application_Prototype/mvp_v1` folder.

### Live Infrastructure
| Layer | Provider |
|---|---|
| Frontend | Vercel |
| Backend API | Render.com |
| Database | Supabase (PostgreSQL) |
| Email | Brevo (transactional only: verification + PDF delivery) |

---

## 3. Mandatory Agent Behaviors

### Technology Stack Stewardship
Do not introduce new dependencies or alternative libraries without user confirmation. The approved stack is:
- **Backend:** FastAPI, SQLAlchemy, Pydantic v2, ReportLab, Brevo SDK
- **Frontend:** React 18 + Vite, Tailwind CSS, shadcn/ui, react-i18next, Recharts
- **ML:** Scikit-learn (K-Means, KNN), Pandas, NumPy — all within `benchmarking_ai/ml_v5`
- **Infrastructure:** Render (backend), Vercel (frontend), Supabase (database)

### Localization Rules
- All user-facing strings must live in `frontend/src/locales/en.json` **and** `de.json`.
- Never hardcode UI text directly in React components. Always use `t('key')` or `<Trans>`.
- German is the default language. Do not remove or disable the language toggle.

### ML Integrity
- `benchmarking_ai/ml_v5/models.py` is the single source of truth for all analytical logic.
- Badge categorization (`impact_score` key), action item parsing (`**Action 1:**` format), and source tags must remain in English for frontend parsing, even for German-language reports.

### README Maintenance
- Update the root `README.md` only when significant architectural changes, new features, or major milestones are reached. Do not update for minor refactors.

### Core Values
- **Aesthetics Matter:** Frontend changes must look premium, modern, and high-quality.
- **GDPR Compliance:** Do not introduce analytics, tracking scripts, or cookies without explicit user consent.

---

## 4. How to Use This Project

When starting a new task:
1. Check `doc/deployment_plan.md` for infrastructure details.
2. Check `doc/github_workflow_guide.md` for sync logic.
3. Check `doc/render_vercel_deployment_guide.md` for cloud deployment specifics.
4. Read the root `README.md` for the current tech stack and structure.
