import { api } from './api';

/**
 * Initializes a visitor session for the assessment.
 * Creates a placeholder company and a new response.
 * @returns {Promise<{companyId: number, responseId: number}>}
 */
export async function initializeVisitorSession() {
    try {
        // 1. Create a placeholder company
        // Backend requires specific fields, so we provide dummy "Visitor" data
        // This will be updated later with real data in CompanySnapshot
        const placeholderCompany = {
            company_name: "Visitor",
            industry: "Other",
            number_of_employees: "1-10", // Dummy value
            website: "",
            city: "",
            email: "visitor@example.com"
        };

        const company = await api.createCompany(placeholderCompany);

        if (!company || !company.company_id) {
            throw new Error("Failed to create visitor session (Company)");
        }

        // 2. Create a response for this company
        const response = await api.createResponse(company.company_id);

        if (!response || !response.response_id) {
            throw new Error("Failed to create visitor session (Response)");
        }

        // 3. Store in Session Storage
        sessionStorage.setItem('ai_compass_company_id', company.company_id);
        sessionStorage.setItem('ai_compass_response_id', response.response_id);

        // Clear any previous questionnaire state if starting fresh
        sessionStorage.removeItem('ai_compass_answers');

        return {
            companyId: company.company_id,
            responseId: response.response_id
        };

    } catch (error) {
        console.error("Failed to initialize visitor session:", error);
        throw error;
    }
}

/**
 * Retrieves current session data.
 */
export function getSession() {
    return {
        companyId: sessionStorage.getItem('ai_compass_company_id'),
        responseId: sessionStorage.getItem('ai_compass_response_id')
    };
}
