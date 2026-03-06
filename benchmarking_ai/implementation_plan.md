# Implementation Plan: 🚀 Project Status & Hard Launch Roadmap

This document outlines the current state of the AI Compass deployment and the remaining tasks required to transition from the "Coming Soon" phase to the live public launch.

## 🟩 Phase 1 & 2: Infrastructure & Deployment (Complete)

We have successfully implemented the "Dual-Repo Strategy" separating development from production.

*   **Backend (Render):** FastAPI containerized and running. Environment (`CORS`, `sys.path` for ML modules) stabilized.
*   **Frontend (Vercel):** React/Vite built and deployed. Custom domain (`the-ai-compass.de`) configured and verified.
*   **Database:** Connected to production Supabase instance.
*   **CI/CD:** GitHub Actions Auto-Sync pipeline is fully active.
*   **Pre-Launch Protection:** Deployed the `ComingSoonPage` interceptor. Production URLs are blocked, while `localhost` remains fully accessible.

---

## 🟧 Phase 3: Legal & Compliance Requirements (Pending)
> [!IMPORTANT]
> These steps are legally required before opening the platform to the public, especially in the EU region (GDPR/DDG).

### 1. Imprint (Impressum) - Private Individuals
*   Since this is launched by individuals (not a registered company), the requirements are simpler. Update `ImprintPage.jsx` to ensure accurate details for the responsible person(s):
    *   Full Name (Christian Miething as primary contact)
    *   Full Residential/Contact Address
    *   Contact Information (Email)
    *   *Note: VAT ID and Commercial Register entries are NOT required for private individuals.*

### 2. Privacy Policy (Datenschutzerklärung)
*   The current `PrivacyPage.jsx` is mostly accurate but needs a final review:
    *   **No Tracking:** Explicitly state that no tracking cookies, Google Analytics, or third-party analytics are used.
    *   **Data Handling:** Confirm the explanation of how Supabase stores assessment inputs (company data, scores) is accurate.

### 3. Secure Results Access (UUID Implementation)
*   Currently, `response_id` uses predictable sequential integers (e.g., `.../results/14`). This allows malicious users to guess URLs and view others' results.
*   **Database Update:** Add a new `result_hash` column to the `responses` table (e.g., PostgreSQL `varchar(32)` or `UUID` using `gen_random_uuid()`).
*   **Backend Update:** Update the `/{response_id}/results` and `/{response_id}/pdf` endpoints to query by `result_hash` instead of integer ID.
*   **Frontend Check:** Ensure the browser router `Route path="/results/:hash"` matches the new secure format.

### 4. Email Verification Workflow (Brevo)
*   **Pre-Results Block:** When a user completes the snapshot, they are blocked from immediately viewing results.
*   **Email Dispatch:** Backend generates a one-time verification token linked to the response and triggers an email via Brevo containing a magic link: `https://the-ai-compass.de/verify?token=XYZ`.
*   **Verification Endpoint:** The `/verify` route confirms the token, sets a verified flag on the response, and automatically redirects the user to their permanent `.../results/<UUID>` page.
*   **Attachment Delivery:** The backend pre-generates the PDF report and instructs Brevo to attach it to a "Welcome/Here are your results" confirmation email post-verification.

---

## 🟦 Phase 4: Final Polish & "Hard Launch" (Pending)

### 1. Language Switch (i18n) Feature & DB Translation Support
*   Integrate a localization library (e.g., `react-i18next`).
*   Extract all hardcoded static text from components into English (`en`) JSON translation files.
*   Create a German (`de`) translation file for all terminology.
*   Add a Language Toggle UI in the navigation bar to allow users to switch between English and Deutsch.
*   **Dynamic DB Translations for Questionnaire:** Since question data is retrieved from the backend, JSON map translations are brittle and unmaintainable if questions are altered later. Therefore, the architectural approach needs to shift to a pure DB-driven i18n structure:
    *   **Database Backup (SQL Dump):** Before making any schema changes, we will generate a complete structural and data copy of the production database using standard SQL output (e.g., `pg_dump` or Supabase Export producing a `.sql` file). This ensures it can be instantly uploaded to Supabase or executed in PostgreSQL to perfectly restore tables and data.
    *   **Database Schema Migration:** Add new columns to the live database (`dimension_name_de` in `dimensions`, `header_de` & `question_text_de` in `questions`, `answer_text_de` in `answers`).
    *   **Data Population Script:** Create a standalone Python database script (e.g., `migrate_translations.py`) using SQLAlchemy to directly `UPDATE` the newly created `_de` columns with the German translated strings based on their IDs, leaving the original CSV seed workflow completely untouched.
    *   **Frontend Logic:** Modify `QuestionnaireWizard.jsx` to conditionally render `{i18n.language === 'de' ? q.question_text_de : q.question_text}` and apply the same conditional rendering to dimension names and answers.
    *   **Sidebar Updates:** Add `Imprint` and `Privacy Policy` links to the bottom of the left sidebar in `QuestionnaireWizard.jsx` and make the AI Compass Logo clickable, taking the user back to the homepage.
    *   **Results Page Implications (Post-Generation Switching):** The `ResultsPage.jsx` relies on your ML model (`benchmarking_ai/ml_v5`) to dynamically generate narratives and roadmap actions using a K-Means/k-NN approach, *not an LLM*.
        *   **Dynamic Re-fetching:** We will update `ResultsPage.jsx` to listen to the `i18n.language` toggle. If the user swaps languages while viewing their results, the frontend will automatically re-call the backend API (`/api/{hash}/results?lang=de`).
        *   **Backend Translation Routing:** The backend API will intercept the `lang` parameter. When `lang=de`, it will pull the German `_de` columns from the database (so the ML model uses German question text and themes for the roadmap).
        *   **Template Localization:** We will update the hardcoded English string templates (e.g., `"Strategic Focus: {theme}"`, `"**Analysis**: ..."`) located inside `benchmarking_ai/ml_v5/models.py` and `utils.py` to also have German equivalents based on the active requested language.

### 2. Content & UX Review
*   Conduct a final pass over all text content, question phrasing, and dimension explanations in the frontend.
*   Ensure all `mailto:` links or external portfolio links resolve correctly in production.

### 3. The Hard Launch Sequence
*   Verify SSL propagation and domain health across all DNS registrars.
*   **Action:** Modify `App.jsx` to remove the `isLocalhost` blocker.
*   Push commit to trigger the final deployment, opening the application to the public.

---

## Verification Plan

### Manual Verification
Before executing Phase 4, the following steps must pass:
1.  **Legal Sign-off:** User confirms the Imprint and Privacy pages meet local regulations.
2.  **End-to-End Test:** Submitting a test assessment on `localhost` successfully populates the production Supabase database.
3.  **Visual Check:** The Coming Soon page displays correctly on mobile and desktop without layout breaks.
