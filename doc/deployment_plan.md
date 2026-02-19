
# Deployment Plan: Automated Dual-Repo Strategy

## 1. Project Configuration
This strategy automates the synchronization between your **Development** and **Production** repositories.

*   **Development Repo (Source):** `https://github.com/AI-Compass-SME/ai-compass.git`
*   **Production Repo (Target):** `https://github.com/AI-Compass-SME/the-ai-compass.de.git`
*   **Production Domain:** `the-ai-compass.de`

---

## 2. Automated Production Sync (GitHub Actions)
To automate the release, we will use a GitHub Action in the **ai-compass** (Dev) repository. Every time you merge into `main`, it will automatically:
1.  Restructure the code (Backend/Frontend/ML).
2.  Clean up the Production repo.
3.  Push the "Production-Ready" code to `the-ai-compass.de`.

### Phase 1: Setup GitHub Secrets
In your `ai-compass` [Settings > Secrets and variables > Actions], add:
*   `PROD_REPO_TOKEN`: A Personal Access Token (PAT) with `repo` scope to allow pushing to the other repository.

### Phase 2: The Workflow File
Create `.github/workflows/deploy-prod.yml` in the `ai-compass` repo:

```yaml
name: Sync to Production Repository
on:
  push:
    branches: [ main ]

jobs:
  sync-prod:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Development Repo
        uses: actions/checkout@v4

      - name: Checkout Production Repo
        uses: actions/checkout@v4
        with:
          repository: AI-Compass-SME/the-ai-compass.de
          token: ${{ secrets.PROD_REPO_TOKEN }}
          path: prod-repo

      - name: Restructure and Sync
        run: |
          # Clean old prod files
          rm -rf prod-repo/backend prod-repo/frontend
          
          # Copy from Dev to Prod-Repo
          mkdir -p prod-repo/backend/modules/benchmarking_ai
          cp -r Application_Prototype/mvp_v1/backend/* prod-repo/backend/
          cp -r Application_Prototype/mvp_v1/frontend/* prod-repo/frontend/
          cp -r benchmarking_ai/ml_v5 prod-repo/backend/modules/benchmarking_ai/ml_v5
          
          # Remove dev scripts from prod backend
          rm -rf prod-repo/backend/venv
          rm -rf prod-repo/backend/__pycache__

      - name: Commit and Push to Production
        working-directory: prod-repo
        run: |
          git config user.name "GitHub Action"
          git config user.email "action@github.com"
          git add .
          git commit -m "Automated Sync: ${{ github.event.head_commit.message }}" || echo "No changes to commit"
          git push origin main
```

---

## 3. Deployment Checklist (PaaS)

### Backend (Render)
- [ ] Connect to `the-ai-compass.de` repo.
- [ ] **Root Directory:** `backend`
- [ ] **Build:** `pip install -r requirements.txt`
- [ ] **Start:** `uvicorn main:app --host 0.0.0.0 --port 10000`
- [ ] **Environment Variables:** `DATABASE_URL` (Supabase connection string), `CORS_ORIGINS=https://the-ai-compass.de`.

### Frontend (Vercel)
- [ ] Connect to `the-ai-compass.de` repo.
- [ ] **Root Directory:** `frontend`
- [ ] **Framework:** Vite.

---

## 4. Key Considerations
*   **Merge Safety:** Changes only go to production when you merge into `main`. You can work on other branches without affecting the live site.
*   **Refactoring Script:** If we need to modify imports during the sync, we can add a simple Python line to the GitHub Action `run` block.
*   **Zero Manual Work:** After the initial setup, you never have to manually copy files or restructuring folders again.
