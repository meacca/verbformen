/**
 * Main application logic for German Verb Learning webapp
 */

import { startSession, submitAnswers } from './api.js';

// Application state
const appState = {
    sessionId: null,
    currentVerbs: [],
    results: null,
    currentView: 'start' // 'start' | 'quiz' | 'results'
};

// DOM elements
const startScreen = document.getElementById('start-screen');
const quizScreen = document.getElementById('quiz-screen');
const resultsScreen = document.getElementById('results-screen');
const startBtn = document.getElementById('start-btn');
const restartBtn = document.getElementById('restart-btn');
const quizForm = document.getElementById('quiz-form');
const verbsContainer = document.getElementById('verbs-container');
const loadingIndicator = document.getElementById('loading');
const errorMessage = document.getElementById('error-message');
const errorText = document.getElementById('error-text');
const errorClose = document.getElementById('error-close');
const verbCountSlider = document.getElementById('verb-count');
const verbCountValue = document.getElementById('verb-count-value');
const verbCountDisplay = document.getElementById('verb-count-display');

/**
 * Initialize the application
 */
function init() {
    // Event listeners
    startBtn.addEventListener('click', handleStartSession);
    restartBtn.addEventListener('click', handleRestart);
    quizForm.addEventListener('submit', handleSubmitAnswers);
    errorClose.addEventListener('click', hideError);
    verbCountSlider.addEventListener('input', handleVerbCountChange);

    // Show start screen
    showScreen('start');
}

/**
 * Handle verb count slider change
 */
function handleVerbCountChange() {
    const count = verbCountSlider.value;
    verbCountValue.textContent = count;
    verbCountDisplay.textContent = count;
}

/**
 * Show a specific screen
 * @param {string} screenName - Name of the screen to show
 */
function showScreen(screenName) {
    startScreen.classList.remove('active');
    quizScreen.classList.remove('active');
    resultsScreen.classList.remove('active');

    switch (screenName) {
        case 'start':
            startScreen.classList.add('active');
            break;
        case 'quiz':
            quizScreen.classList.add('active');
            break;
        case 'results':
            resultsScreen.classList.add('active');
            break;
    }

    appState.currentView = screenName;
}

/**
 * Handle starting a new session
 */
async function handleStartSession() {
    try {
        startBtn.disabled = true;
        startBtn.textContent = 'Loading...';

        const count = parseInt(verbCountSlider.value, 10);
        const sessionData = await startSession(count);

        appState.sessionId = sessionData.session_id;
        appState.currentVerbs = sessionData.verbs;

        renderQuizForm(sessionData.verbs);
        showScreen('quiz');

    } catch (error) {
        showError('Failed to start session. Please try again.');
        console.error('Start session error:', error);
    } finally {
        startBtn.disabled = false;
        startBtn.textContent = 'Begin Session';
    }
}

/**
 * Render the quiz form with verb inputs
 * @param {Array<Object>} verbs - Array of verb objects
 */
function renderQuizForm(verbs) {
    verbsContainer.innerHTML = '';

    verbs.forEach((verb, index) => {
        const verbCard = document.createElement('div');
        verbCard.className = 'verb-card';
        verbCard.innerHTML = `
            <div class="verb-header">
                <span class="verb-number">${index + 1}.</span>
                <span class="verb-infinitive">${verb.infinitive}</span>
            </div>
            <div class="verb-forms">
                <div class="form-group">
                    <label for="praesens-${index}">Präsens (er/sie/es):</label>
                    <input
                        type="text"
                        id="praesens-${index}"
                        name="praesens-${index}"
                        data-verb="${verb.infinitive}"
                        data-form="praesens"
                        required
                        autocomplete="off"
                    >
                </div>
                <div class="form-group">
                    <label for="praeteritum-${index}">Präteritum (er/sie/es):</label>
                    <input
                        type="text"
                        id="praeteritum-${index}"
                        name="praeteritum-${index}"
                        data-verb="${verb.infinitive}"
                        data-form="praeteritum"
                        required
                        autocomplete="off"
                    >
                </div>
                <div class="form-group">
                    <label for="perfekt-${index}">Perfekt:</label>
                    <input
                        type="text"
                        id="perfekt-${index}"
                        name="perfekt-${index}"
                        data-verb="${verb.infinitive}"
                        data-form="perfekt"
                        required
                        autocomplete="off"
                    >
                </div>
            </div>
        `;

        verbsContainer.appendChild(verbCard);
    });

    // Focus on first input
    const firstInput = verbsContainer.querySelector('input');
    if (firstInput) {
        firstInput.focus();
    }
}

/**
 * Handle form submission
 * @param {Event} event - Form submit event
 */
async function handleSubmitAnswers(event) {
    event.preventDefault();

    try {
        // Show loading indicator
        loadingIndicator.classList.remove('hidden');
        quizForm.querySelector('.btn-primary').disabled = true;

        // Collect answers
        const answers = [];
        const formData = new FormData(quizForm);

        appState.currentVerbs.forEach((verb) => {
            const praesensInput = quizForm.querySelector(`input[data-verb="${verb.infinitive}"][data-form="praesens"]`);
            const praeteritumInput = quizForm.querySelector(`input[data-verb="${verb.infinitive}"][data-form="praeteritum"]`);
            const perfektInput = quizForm.querySelector(`input[data-verb="${verb.infinitive}"][data-form="perfekt"]`);

            answers.push({
                infinitive: verb.infinitive,
                praesens: praesensInput.value.trim(),
                praeteritum: praeteritumInput.value.trim(),
                perfekt: perfektInput.value.trim()
            });
        });

        // Submit to backend
        const results = await submitAnswers(appState.sessionId, answers);

        // Store results and show results screen
        appState.results = results;
        renderResults(results);
        showScreen('results');

    } catch (error) {
        showError('Failed to submit answers. Please try again.');
        console.error('Submit error:', error);
    } finally {
        loadingIndicator.classList.add('hidden');
        quizForm.querySelector('.btn-primary').disabled = false;
    }
}

/**
 * Render the results table
 * @param {Object} results - Results object from backend
 */
function renderResults(results) {
    // Update score display
    const scorePercentage = document.getElementById('score-percentage');
    const scoreText = document.getElementById('score-text');

    scorePercentage.textContent = `${results.score_percentage}%`;

    const correctCount = results.correct_count;
    const totalForms = results.total_forms;
    scoreText.textContent = `You got ${correctCount} out of ${totalForms} forms correct!`;

    // Color code the score
    const scoreCircle = document.querySelector('.score-circle');
    if (results.score_percentage >= 90) {
        scoreCircle.className = 'score-circle excellent';
    } else if (results.score_percentage >= 70) {
        scoreCircle.className = 'score-circle good';
    } else if (results.score_percentage >= 50) {
        scoreCircle.className = 'score-circle average';
    } else {
        scoreCircle.className = 'score-circle poor';
    }

    // Render results table
    const tbody = document.getElementById('results-tbody');
    tbody.innerHTML = '';

    results.results.forEach((verbResult) => {
        const forms = ['praesens', 'praeteritum', 'perfekt'];
        const formLabels = ['Präsens', 'Präteritum', 'Perfekt'];

        forms.forEach((form, formIndex) => {
            const row = document.createElement('tr');
            const isCorrect = verbResult.correct[form];
            row.className = isCorrect ? 'correct-row' : 'incorrect-row';

            // Only show verb name on first row
            if (formIndex === 0) {
                const verbCell = document.createElement('td');
                verbCell.rowSpan = 3;
                verbCell.className = 'verb-cell';
                verbCell.textContent = verbResult.infinitive;
                row.appendChild(verbCell);
            }

            // Form name
            const formCell = document.createElement('td');
            formCell.textContent = formLabels[formIndex];
            row.appendChild(formCell);

            // User answer
            const userCell = document.createElement('td');
            userCell.textContent = verbResult.user_answers[form];
            row.appendChild(userCell);

            // Correct answer
            const correctCell = document.createElement('td');
            correctCell.textContent = verbResult.correct_answers[form];
            row.appendChild(correctCell);

            // Result indicator
            const resultCell = document.createElement('td');
            resultCell.className = 'result-indicator';
            resultCell.innerHTML = isCorrect
                ? '<span class="correct-mark">✓</span>'
                : '<span class="incorrect-mark">✗</span>';
            row.appendChild(resultCell);

            tbody.appendChild(row);
        });
    });
}

/**
 * Handle restart button click
 */
function handleRestart() {
    // Reset state
    appState.sessionId = null;
    appState.currentVerbs = [];
    appState.results = null;

    // Clear form
    quizForm.reset();
    verbsContainer.innerHTML = '';

    // Show start screen
    showScreen('start');
}

/**
 * Show error message
 * @param {string} message - Error message to display
 */
function showError(message) {
    errorText.textContent = message;
    errorMessage.classList.remove('hidden');
}

/**
 * Hide error message
 */
function hideError() {
    errorMessage.classList.add('hidden');
}

// Initialize the app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
