
# Deployment Guide: Render & Vercel (Production)

This guide takes you through deploying the code from your production repo (**`the-ai-compass.de`**) to the live web.

---

## Phase 1: Database (Supabase)
The production application will continue to use **Supabase** as the database, consistent with your development environment.

1.  Log in to your [Supabase Dashboard](https://supabase.com).
2.  Select your project for **AI Compass**.
3.  Go to **Project Settings** (gear icon) → **Database**.
4.  In the **Connection string** section, select **URI**.
5.  Copy the connection string. 
    *   *Note: Ensure you include your database password in the string (replace `[YOUR-PASSWORD]` if necessary).*
6.  You will use this as your `DATABASE_URL` in Phase 2.

---

## Phase 2: Render Backend (FastAPI)
1.  Log in to [Render.com](https://render.com).
2.  Click **New +** → **Web Service**.
3.  Select **Build and deploy from a Git repository**.
4.  Connect your **`the-ai-compass.de`** repository.
5.  **Name:** `ai-compass-backend`.
6.  **Root Directory:** `backend` (Crucial!).
7.  **Runtime:** `Python 3`.
8.  **Build Command:** `pip install -r requirements.txt`.
9.  **Start Command:** `uvicorn main:app --host 0.0.0.0 --port 10000`.
10. **Environment Variables:** Click "Advanced" and add:
    *   `DATABASE_URL`: (Paste your Supabase connection string from Phase 1).
    *   `CORS_ORIGINS`: `https://the-ai-compass.de`.
    *   `PYTHON_VERSION`: `3.11.0` (Recommended).
11. Click **Create Web Service**.
12. **Auto-Deploy Setup (Crucial):**
    *   Go to **Settings** (left sidebar of your new service).
    *   Scroll down to **Deploy Hook**.
    *   Copy the **Deploy Hook URL**.
    *   **Action:** Go to your **Dev Repo** (`ai-compass`) -> Settings -> Secrets -> Actions.
    *   Add a new secret named `RENDER_DEPLOY_HOOK` and paste this URL.

---

## Phase 3: Vercel Frontend (React) - Detailed Steps
1.  Log in to [Vercel.com](https://vercel.com).
2.  **Dashboard:** Click the **"Add New..."** button (top right) → select **"Project"**.
3.  **Import Git Repository:**
    *   Find **`AI-Compass-SME/the-ai-compass.de`** in the list.
    *   Click the **Import** button next to it.
    *   > [!WARNING]
    *   > **DO NOT** click "Create Git Repository". Only use the **Import** button next to your existing `the-ai-compass.de` repo.

4.  **Configure Project (Crucial Step):**
    *   **Project Name:**
        *   Vercel might default to `the-ai-compass-de`.
        *   **If it says "Name already used":** Change the **Project Name** field here (e.g., `ai-compass-prod-app`).
        *   *Note:* This does NOT create a new repo. It just names the Vercel dashboard item.
    *   **Framework Preset:** Ensure it says **Vite** (It should auto-detect this).
    *   **Root Directory:**
        *   Click **Edit** next to Root Directory.
        *   Select the **`frontend`** folder from the file browser popup.
        *   Click **Continue**.
5.  **Build and Output Settings:** (Leave these as default).
    *   Build Command: `npm run build`
    *   Output Directory: `dist`
    *   Install Command: `npm install`
6.  **Environment Variables:**
    *   Expand the **Environment Variables** section.
    *   Key: `VITE_API_URL`
    *   Value: `https://ai-compass-backend.onrender.com` (Copy this from your Render dashboard).
    *   Click **Add**.
7.  **Finalize:** Click **Deploy**.
    *   Wait for the build to finish (approx. 1 minute).
    *   You will see a "Congratulations!" screen with a preview.

---

## Phase 4: Connecting the Domain (the-ai-compass.de)
1.  In your new Vercel Project, go to **Settings** (top tab) → **Domains** (left sidebar).
2.  Type `the-ai-compass.de` in the box and click **Add**.
3.  Vercel will show a "Invalid Configuration" or "Config Required" status.
4.  **DNS Configuration:**
    *   Log in to your **Domain Registrar** (e.g., GoDaddy, Namecheap, Hostinger).
    *   Find the DNS Management area for your domain.
    *   Add an **A Record**:
        *   Host/Name: `@`
        *   Value: `76.76.21.21` (Vercel's IP).
    *   Add a **CNAME Record**:
        *   Host/Name: `www`
        *   Value: `cname.vercel-dns.com`.
5.  Return to Vercel and wait. It usually verifies in a few minutes, but can take up to 24-48 hours.

---

## Phase 5: Testing the Connection
1.  Visit `https://the-ai-compass.de`.
2.  If the page loads, the frontend is live.
3.  Try to perform an action that requires data (e.g., logging in or generating a report). 
4.  **Check Logs:**
    *   If Backend fails: Check Render's **Events** and **Logs** tabs.
    *   If Frontend fails: Open Browser Console (F12) and check for "CORS" or "Network" errors.
