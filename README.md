# German Verb Learning - Verbformen 🇩🇪

A simple, stateless web application for practicing German verb conjugations. Test your knowledge of Präsens, Präteritum, and Perfekt forms!

## Features

- Random selection of 10 verbs from a database of 20 common German verbs
- Practice 3rd person forms: Präsens (er/sie/es), Präteritum (er/sie/es), and Perfekt
- Instant feedback with detailed results
- Color-coded scoring system
- Clean, responsive interface
- Completely stateless - no login or tracking required

## Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

1. Clone or navigate to the project directory:
```bash
cd /Users/meacca/dev/verbformen
```

2. Initialize the project and install dependencies:
```bash
uv sync
```

This command will automatically create a virtual environment and install all dependencies.

### Running the Application

Start the server:
```bash
uv run uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

For development with auto-reload:
```bash
uv run uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

Open your browser and navigate to:
```
http://localhost:8000
```

## How to Use

1. **Start a Session**: Click the "Begin Session" button on the welcome screen
2. **Fill in Forms**: Enter the conjugated forms for each of the 10 randomly selected verbs
   - Präsens (3rd person: er/sie/es)
   - Präteritum (3rd person: er/sie/es)
   - Perfekt
3. **Submit**: Click "Submit Answers" to see your results
4. **Review**: Check your score and see which answers were correct or incorrect
5. **Practice Again**: Start a new session to practice with different verbs

## Available Verbs

The application includes 20 common German verbs:

| Infinitive | Präsens | Präteritum | Perfekt |
|-----------|---------|------------|---------|
| sein | ist | war | ist gewesen |
| haben | hat | hatte | hat gehabt |
| werden | wird | wurde | ist geworden |
| gehen | geht | ging | ist gegangen |
| kommen | kommt | kam | ist gekommen |
| machen | macht | machte | hat gemacht |
| sagen | sagt | sagte | hat gesagt |
| geben | gibt | gab | hat gegeben |
| können | kann | konnte | hat gekonnt |
| müssen | muss | musste | hat gemusst |
| wissen | weiß | wusste | hat gewusst |
| sehen | sieht | sah | hat gesehen |
| nehmen | nimmt | nahm | hat genommen |
| finden | findet | fand | hat gefunden |
| aufstehen | steht auf | stand auf | ist aufgestanden |
| fahren | fährt | fuhr | ist gefahren |
| schreiben | schreibt | schrieb | hat geschrieben |
| lesen | liest | las | hat gelesen |
| essen | isst | aß | hat gegessen |
| trinken | trinkt | trank | hat getrunken |

## Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Vanilla HTML, CSS, JavaScript
- **Package Manager**: uv
- **Testing**: pytest

## Project Structure

```
verbformen/
├── backend/              # Python backend
│   ├── main.py          # FastAPI application
│   ├── models.py        # Pydantic models
│   ├── services.py      # Business logic
│   └── tests/           # Test suite
├── frontend/            # Static frontend files
│   ├── index.html      # Main page
│   ├── styles.css      # Styling
│   ├── app.js          # Application logic
│   └── api.js          # API client
├── data/               # Verb database
│   └── verbs_forms.json
├── pyproject.toml      # Project metadata and dependencies
└── uv.lock            # Locked dependencies for reproducibility
```

## API Endpoints

- `GET /` - Serve the frontend application
- `GET /api/health` - Health check endpoint
- `GET /api/session/start` - Start a new learning session (returns 10 random verbs)
- `POST /api/session/submit` - Submit answers and receive graded results

## Scoring System

- Each verb has 3 forms to fill in
- Total of 30 forms per session (10 verbs × 3 forms)
- Exact string matching (case-sensitive)
- Whitespace is automatically trimmed
- Results are color-coded:
  - 🟢 Green (90%+): Excellent
  - 🔵 Blue (70-89%): Good
  - 🟡 Yellow (50-69%): Average
  - 🔴 Red (<50%): Needs practice

## Running Tests

Run the full test suite:
```bash
uv run pytest backend/tests/ -v
```

Run specific tests:
```bash
uv run pytest backend/tests/test_services.py -v
uv run pytest backend/tests/test_api.py -v
```

All 23 tests should pass.

## Adding More Verbs

To add more verbs to the learning database:

1. Open `data/verbs_forms.json`
2. Add a new entry with the infinitive as the key:
```json
{
  "schlafen": {
    "Präsens": "schläft",
    "Präteritum": "schlief",
    "Perfekt": "hat geschlafen"
  }
}
```
3. Save the file - no restart required!

## Development

For detailed development information, see [CLAUDE.md](CLAUDE.md).

### Key Points

- The application is completely stateless
- No database - verbs are stored in JSON
- Session IDs are generated but not stored
- Each quiz is independent

## Browser Compatibility

Works on all modern browsers:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

To contribute to this project:

1. Read [CLAUDE.md](CLAUDE.md) for development guidelines
2. Make your changes
3. Run the test suite to ensure nothing breaks
4. Submit your changes

## License

This is a simple educational project for learning German verbs.

## Acknowledgments

- Built with FastAPI and vanilla JavaScript
- Designed for German language learners
- Focuses on the most common German verbs

## Support

If you encounter any issues:
1. Check that all dependencies are installed with `uv sync`
2. Verify the server is running on port 8000
3. Check browser console for JavaScript errors
4. Review the API documentation at `http://localhost:8000/docs`

---

**Viel Erfolg beim Lernen! (Good luck learning!)** 📚
