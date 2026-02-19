
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

---

## Phase 3: Vercel Frontend (React)
1.  Log in to [Vercel.com](https://vercel.com).
2.  Click **Add New...** → **Project**.
3.  Import the **`the-ai-compass.de`** repository.
4.  **Framework Preset:** Vite (Should be auto-detected).
5.  **Root Directory:** `frontend` (Crucial!).
6.  **Environment Variables:** Add:
    *   `VITE_API_URL`: `https://ai-compass-backend.onrender.com` (Your Render URL).
7.  Click **Deploy**.

---

## Phase 4: Connecting the Domain (the-ai-compass.de)
1.  In **Vercel**, go to your Project Settings → **Domains**.
2.  Type `the-ai-compass.de` and click **Add**.
3.  Vercel will provide **A Records** and **CNAME** records.
4.  Log in to your **Domain Registrar** (e.g., GoDaddy, Namecheap, Hostinger) and enter those DNS values.

---

## Phase 5: Testing the Connection
1.  Visit `https://the-ai-compass.de`.
2.  If the page loads, the frontend is live.
3.  Try to perform an action that requires data (e.g., logging in or generating a report). 
4.  **Check Logs:**
    *   If Backend fails: Check Render's **Events** and **Logs** tabs.
    *   If Frontend fails: Open Browser Console (F12) and check for "CORS" or "Network" errors.

---

## Summary of URLs
*   **Repo:** `the-ai-compass.de`
*   **Backend:** `ai-compass-backend.onrender.com`
*   **Frontend:** `the-ai-compass.de`
*   **Database:** Supabase (Shared with Dev or separate Prod instance)
