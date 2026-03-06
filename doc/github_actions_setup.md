
# GitHub Actions Automation: Organization Setup Guide

This guide provides step-by-step instructions for setting up automated synchronization between two repositories within a **GitHub Organization**.

---

## Step 1: Create a Personal Access Token (PAT)
For organizations, GitHub now uses a fine-grained token system that requires specific category selection.

1.  Log in to GitHub → Click **Profile Picture** → **Settings**.
2.  Left sidebar (scroll to bottom): **Developer settings**.
3.  Left sidebar: **Personal access tokens** → **Fine-grained tokens**.
4.  Click **Generate new token**.
5.  **Token name:** `Prod-Deploy-Sync`.
6.  **Resource owner:** Select your **Organization** (e.g., `AI-Compass-SME`).
7.  **Repository access:** Select **Only select repositories** and pick both:
    *   `ai-compass` (Source)
    *   `the-ai-compass.de` (Target)
8.  **Permissions Section:**
    *   You will see a card with two tabs: **Repositories** and **Organizations**.
    *   Make sure you are on the **Repositories** tab.
    *   Click the **+ Add permissions** button.
    *   In the list that appears, search for or find **Contents**.
    *   Click **Contents** to select it.
    *   In the dropdown that appears (often to the right of the permission name), change the level to **Read and write**.
    *   *(Note: **Metadata** access is usually added automatically as Read-only, which is correct).*
9.  Scroll to the bottom and click **Generate token**.
10. **Copy the token immediately.**

---

## Step 2: Add the Token to the Source Repository
You must save this token in the **Source repo** so the script can use it.

1.  Go to the **Source Repo** (`ai-compass`) on GitHub.
2.  Top bar: **Settings** → Left sidebar: **Secrets and variables** → **Actions**.
3.  Click **New repository secret**.
4.  **Name:** `PROD_REPO_TOKEN`.
5.  **Secret:** Paste the token from Step 1.
6.  Click **Add secret**.

---

## Step 3: Organization Settings (Troubleshooting)
If the token setup works but the Github Action fails, check these Org-level settings:

1.  Go to your **Organization Settings** page.
2.  Left sidebar: **Actions** → **General**.
3.  Ensure **Workflow permissions** allows "Read and write".
4.  Left sidebar: **Personal access tokens** → **Settings**.
5.  Ensure **Allow access via fine-grained personal access tokens** is on.

---

## Step 4: The Workflow File
Create `.github/workflows/deploy-prod.yml` in your `ai-compass` repo:

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
          
          # Copy Backend & Frontend
          mkdir -p prod-repo/backend/modules/benchmarking_ai
          cp -r Application_Prototype/mvp_v1/backend/* prod-repo/backend/
          cp -r Application_Prototype/mvp_v1/frontend/* prod-repo/frontend/
          
          # Copy ML Logic (ml_v5)
          cp -r benchmarking_ai/ml_v5 prod-repo/backend/modules/benchmarking_ai/ml_v5
          
          # Cleanup
          rm -rf prod-repo/backend/venv
          rm -rf prod-repo/backend/__pycache__

      - name: Commit and Push
        working-directory: prod-repo
        run: |
          git config user.name "GitHub Action [Bot]"
          git config user.email "actions@github.com"
          git add .
          git diff --quiet && git diff --staged --quiet || (git commit -m "Deploy: ${{ github.event.head_commit.message }}" && git push origin main)
```
