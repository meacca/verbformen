/**
 * API client for communicating with the backend
 */

const API_BASE_URL = '/api';

/**
 * Start a new learning session
 * @param {number} count - Number of verbs to practice (1-20, default 10)
 * @returns {Promise<Object>} Session data with verbs
 */
export async function startSession(count = 10) {
    try {
        const response = await fetch(`${API_BASE_URL}/session/start?count=${count}`);

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to start session');
        }

        return await response.json();
    } catch (error) {
        console.error('Error starting session:', error);
        throw error;
    }
}

/**
 * Submit answers and get results
 * @param {string} sessionId - The session ID
 * @param {Array<Object>} answers - Array of user answers
 * @returns {Promise<Object>} Grading results
 */
export async function submitAnswers(sessionId, answers) {
    try {
        const response = await fetch(`${API_BASE_URL}/session/submit`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                session_id: sessionId,
                answers: answers
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to submit answers');
        }

        return await response.json();
    } catch (error) {
        console.error('Error submitting answers:', error);
        throw error;
    }
}

/**
 * Check backend health
 * @returns {Promise<Object>} Health status
 */
export async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);

        if (!response.ok) {
            throw new Error('Backend is not healthy');
        }

        return await response.json();
    } catch (error) {
        console.error('Health check failed:', error);
        throw error;
    }
}
