/**
 * API Client for AI-Compass Backend
 */

const API_BASE_URL = (import.meta.env.VITE_API_URL || '/api/v1').replace(/\/$/, '');

/**
 * Helper to handle API responses
 */
async function handleResponse(response) {
    if (!response.ok) {
        const errorBody = await response.json().catch(() => ({}));
        const errorMessage = errorBody.detail || response.statusText || 'API Error';
        throw new Error(errorMessage);
    }
    return response.json();
}

export const api = {
    /**
     * Fetch questionnaire with all questions
     */
    getQuestionnaire: async () => {
        const response = await fetch(`${API_BASE_URL}/questionnaire`);
        return handleResponse(response);
    },

    /**
     * Create a new company profile
     * @param {Object} companyData 
     */
    createCompany: async (companyData) => {
        const response = await fetch(`${API_BASE_URL}/companies`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(companyData),
        });
        return handleResponse(response);
    },

    /**
     * Initialize a new response session
     * @param {number} companyId 
     */
    createResponse: async (companyId) => {
        const response = await fetch(`${API_BASE_URL}/responses`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ company_id: companyId }),
        });
        return handleResponse(response);
    },

    /**
     * Autosave an answer
     * @param {number} responseId 
     * @param {number} questionId 
     * @param {Array<number>} answerIds 
     */
    saveAnswer: async (responseId, questionId, answerIds) => {
        const response = await fetch(`${API_BASE_URL}/responses/${responseId}/items`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                question_id: questionId,
                answer_ids: answerIds
            }),
        });
        return handleResponse(response);
    },

    /**
     * Complete the assessment
     * @param {number} responseId 
     * @param {Object} companyDetails 
     */
    completeAssessment: async (responseId, companyDetails) => {
        const response = await fetch(`${API_BASE_URL}/responses/${responseId}/complete`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ company_details: companyDetails }),
        });
        return handleResponse(response);
    },

    /**
     * Get results
     * @param {number} responseId 
     */
    getResults: async (responseId) => {
        const response = await fetch(`${API_BASE_URL}/responses/${responseId}/results`);
        return handleResponse(response);
    },

    /**
     * Download PDF Report
     * @param {number} responseId
     */
    downloadPDF: async (responseId) => {
        const response = await fetch(`${API_BASE_URL}/responses/${responseId}/pdf`);
        if (!response.ok) throw new Error("PDF Generation Failed");
        return response.blob();
    },
};
