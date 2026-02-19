
# Deployment Plan: PaaS (Render + Vercel)

## 1. Project Configuration
This plan covers the deployment of the AI Compass application to a production environment using a PaaS (Platform as a Service) architecture.

*   **Deployment Repository:** `https://github.com/AI-Compass-SME/the-ai-compass.de.git`
*   **Production Domain:** `the-ai-compass.de`
*   **Backend Hosting:** Render (Web Service + PostgreSQL)
*   **Frontend Hosting:** Vercel

---

## 2. Essential Pre-Deployment Restructuring
To ensure reliable deployment on Render/Vercel, the backend must be self-contained within the forked repository.

### Structural Goal
Move the `benchmarking_ai` logic *inside* the backend folder so it can be deployed as a single unit.

**Current (in fork):**
```text
the-ai-compass.de/
├── benchmarking_ai/
└── Application_Prototype/
    └── mvp_v1/
        ├── backend/
        └── frontend/
```

**Required Structure:**
```text
the-ai-compass.de/
└── Application_Prototype/
    └── mvp_v1/
        ├── backend/
        │   ├── main.py
        │   └── modules/
        │       └── benchmarking_ai/  <-- MOVED/COPIED HERE
        └── frontend/
```

### Required Code Changes
1.  **Imports:** Update `config.py` and `routers/results.py` to use local module imports (e.g., `from .modules.benchmarking_ai import ...`) instead of `sys.path` hacks.
2.  **Model Paths:** Update `ML_MODELS_PATH` in `config.py` to point to the new internal location.

---

## 3. Deployment Checklist

### Phase 1: local Cleanup & Push
- [ ] **Restructure:** Move `benchmarking_ai` into `backend/modules/`.
- [ ] **Refactor:** Clean up all imports to be relative/local.
- [ ] **Verify:** Run `uvicorn main:app` locally within the `backend` folder to ensure it starts without error.
- [ ] **Push:** Commit and push these changes to `https://github.com/AI-Compass-SME/the-ai-compass.de.git`.

### Phase 2: Backend & Database (Render)
- [ ] **Database:**
    *   Create a **PostgreSQL** instance on Render.
    *   Copy the `Internal Database URL`.
- [ ] **Web Service:**
    *   Create a New Web Service connected to the GitHub repo.
    *   **Root Directory:** `Application_Prototype/mvp_v1/backend`
    *   **Runtime:** `Python 3`
    *   **Build Command:** `pip install -r requirements.txt`
    *   **Start Command:** `uvicorn main:app --host 0.0.0.0 --port 10000`
- [ ] **Environment Variables:**
    *   `DATABASE_URL`: (Your Render Postgres URL)
    *   `CORS_ORIGINS`: `https://the-ai-compass.de`

### Phase 3: Frontend (Vercel)
- [ ] **Project Setup:**
    *   Import the GitHub repo into Vercel.
    *   **Root Directory:** `Application_Prototype/mvp_v1/frontend`
    *   **Framework Preset:** Vite
- [ ] **Environment Variables:**
    *   `VITE_API_URL`: (Your Render Backend URL, e.g., `https://ai-compass-api.onrender.com`)

### Phase 4: Domain Configuration
- [ ] **Vercel Custom Domain:**
    *   Add `the-ai-compass.de` in Vercel project settings.
    *   Configure DNS (A/CNAME records) at your domain registrar.
- [ ] **Backend Custom Subdomain (Optional):**
    *   Add `api.the-ai-compass.de` in Render settings if desired, or use the default `.onrender.com` URL.

---

## 4. Maintenance
*   **Auto-Deploy:** Once configured, any push to the `main` branch of the fork will automatically trigger builds on Render and Vercel.
*   **Logs:** Use the "Logs" tab in both platforms to debug any startup or runtime errors.
