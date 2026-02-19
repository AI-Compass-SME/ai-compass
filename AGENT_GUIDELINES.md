
# AI Agent Guidelines & Project Context

> [!IMPORTANT]
> **To any AI Agent reading this:** You must adhere to these guidelines to ensure project consistency, architectural integrity, and production reliability.

---

## 1. Project Essence & Core Concept
**The AI Compass** is a strategic maturity assessment platform for SMEs. It helps businesses understand their AI readiness through:
-   **Diagnostic Surveys**: Weighted assessment across 7 dimensions.
-   **ML Inference (ml_v5)**: Hybrid clustering and anomaly detection to identify strategic gaps and industry benchmarks.
-   **Dynamic Roadmaps**: A 3-phase actionable guide generated based on peer analysis and critical weaknesses.

**Rule:** Do not deviate from this core SME-focused strategic assessment model unless explicitly instructed by the user.

---

## 2. Technical Architecture & Deployment
The project uses a **Dual-Repository Strategy** to separate development from the production environment:

*   **Development Repo (Source):** `AI-Compass-SME/ai-compass`
    *   Path for active code: `Application_Prototype/mvp_v1/`
    *   Path for ML logic: `benchmarking_ai/ml_v5`
*   **Production Repo (Target):** `AI-Compass-SME/the-ai-compass.de`
    *   This repository is **Flattened**.
    *   Structure: `/backend`, `/frontend`, `/backend/modules/benchmarking_ai`.

### The Production Sync Rule
**Never make direct changes to the production repository logic.** 
1.  All code changes must happen in the `ai-compass` (Development) repo.
2.  Changes are synchronized to production automatically via GitHub Actions (`.github/workflows/deploy-prod.yml`) when merged into `main`.
3.  **Agent Instruction:** If requested to "fix production," apply the fix in the corresponding `Application_Prototype/mvp_v1` folder in the Dev repo.

---

## 3. Mandatory Agent Behaviors

### README Maintenance
-   **Rule:** Review and update the root `README.md` **ONLY** if significant new features, organizational changes, or relevant updates for the reader were added. 
-   **Focus:** Do not update for every minor run or refactor. Ensure the "Current Status" or "Key Features" sections accurately reflect major milestones.

### Technology Stack Stewardship
-   **Backend:** FastAPI (Python), Supabase (PostgreSQL), Scikit-learn (ML).
-   **Frontend:** React (Vite), Tailwind CSS.
-   **Infrastructure:** Render (Backend), Vercel (Frontend), Supabase (Database).

### Core Values
-   **Aesthetics Matter:** Frontend changes must look premium, modern, and high-quality.
-   **ML Integrity:** Keep `ml_v5` as the source of truth for all analytical logic.

---

## 4. Current Project Status (February 2026)
-   **Status:** Transitioning to Automated Production Deployment.
-   **Recently Completed:** Dual-repo setup, GitHub Actions synchronization logic, and comprehensive deployment documentation.
-   **Next Goals:** Finalizing the first automated sync, setting up Render and Vercel environments.

---

## 5. How to use this project
When starting a new task, always check:
1.  `doc/deployment_plan.md` for infrastructure details.
2.  `doc/github_workflow_guide.md` for sync logic.
3.  The current `task.md` (if in agentic mode) or the root `README.md` for the latest milestones.
