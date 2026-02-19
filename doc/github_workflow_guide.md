
# GitHub Actions: Workflow File Guide (Robust Version)

If the action is still failing with **"exit code 1"**, it is likely because one of the copy commands cannot find a folder or the destination hasn't been created yet.

Here is a **more robust and verbose version** of the code for your `.github/workflows/deploy-prod.yml`. This version includes `mkdir` commands for every target and handles empty production folders more safely.

### Use this Updated Code:

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
          echo "Starting sync..."
          
          # 1. Clean existing folders in production repo copy
          rm -rf prod-repo/backend prod-repo/frontend
          
          # 2. Re-create production folder structure
          mkdir -p prod-repo/backend/modules/benchmarking_ai/ml_v5
          mkdir -p prod-repo/frontend
          
          # 3. Sync Content (Using /. to copy contents including hidden files)
          echo "Copying Backend..."
          cp -r Application_Prototype/mvp_v1/backend/. prod-repo/backend/
          
          echo "Copying Frontend..."
          cp -r Application_Prototype/mvp_v1/frontend/. prod-repo/frontend/
          
          echo "Copying ML logic..."
          cp -r benchmarking_ai/ml_v5/. prod-repo/backend/modules/benchmarking_ai/ml_v5/
          
          # 4. Final Cleanup of unneeded production files
          rm -rf prod-repo/backend/venv
          rm -rf prod-repo/backend/__pycache__
          echo "Sync completed successfully."

      - name: Commit and Push
        working-directory: prod-repo
        run: |
          git config user.name "GitHub Action [Bot]"
          git config user.email "actions@github.com"
          git add .
          # This check prevents "nothing to commit" from failing the build
          if [ -n "$(git status --porcelain)" ]; then
            git commit -m "Deploy: ${{ github.event.head_commit.message }}"
            git push origin main
          else
            echo "No changes detect, skipping commit."
          fi
```

### Why this is better:
1.  **Explicit Directory Creation:** Every destination folder is created with `mkdir -p` before the `cp` command runs.
2.  **Safer Copy:** Using `source/.` ensures that you copy the *contents* of the folder (including hidden files like `.gitignore`) into the destination correctly.
3.  **Better Git Check:** Uses a safer `if` statement to check if there are actually changes before trying to commit.
4.  **Logging:** Added `echo` statements so you can see exactly where it fails in the "Actions" log.

**Next Step:** Update the file on GitHub and check the logs. If it still fails, please look at the **"Restructure and Sync"** step in the logs and tell me which line it stops on!
