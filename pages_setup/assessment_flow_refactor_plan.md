## Assessment Flow Refactor & Results Footer

**Goal**: Move the Company Snapshot to the end of the assessment, make email required, enforce a loading state, and add a disclaimer to the results page.

### 1. Backend Updates
*   **`backend/services/session_store.py`**: Add `update_company` method.
*   **`backend/routers/companies.py`**: Add `PUT /companies/{company_id}` endpoint to allow updating company details.

### 2. Frontend API
*   **`frontend/src/lib/api.js`**: Add `updateCompany(companyId, companyData)` method.

### 3. Frontend Flow Changes
*   **`LandingPage.jsx`**:
    *   On "Start Assessment", create a "Visitor" company and a new response.
    *   Store `current_company_id` and `current_response_id` in `localStorage`.
    *   Navigate to `/assessment/{responseId}`.
*   **`QuestionnaireWizard.jsx`**:
    *   On "Finish" (last question), **do not** call `completeAssessment`.
    *   Navigate to `/snapshot` (route will extract IDs from storage).
*   **`CompanySnapshot.jsx`**:
    *   **Validation**: Make `email` field required.
    *   **Logic**:
        *   Read `current_company_id` and `current_response_id` from `localStorage`.
        *   On Submit:
            *   Call `api.updateCompany` with form data.
            *   Call `api.completeAssessment`.
            *   **Loading State**: Show "Generating Report..." overlay for **minimum 3 seconds**.
            *   Navigate to `/results/{responseId}`.
    *   **UI**: 
        *   Change button text to "Generate Report".
        *   Add **Consent Checkbox**: "I agree to the processing of my data and to receive the analysis via email. I can withdraw my consent at any time." (Required for submission).
        *   Disable submit button until consent is checked.

### 4. Results Page Disclaimer
*   **`Footer.jsx`**:
    *   Detect if current route is `/results/*`.
    *   If yes, render the "Legal Disclaimer" section above the standard footer content.
    *   **Content**:
        *   **Methodology**: K-Means Clustering (Explainability).
        *   **No Relationship**: Usage does not create client relationship.
        *   **Human Expert**: Automated output requires expert review.
        *   **AI Badge**: "AI-Generated Report | Powered by AI Compass ML Engine".

### 5. Task List
- [ ] Implement `update_company` in backend
- [ ] Update `LandingPage` to start session
- [ ] Update `QuestionnaireWizard` navigation
- [ ] Update `CompanySnapshot` logic and UI
- [ ] Add Disclaimer to `Footer`
