# German Verb Learning - Verbformen 🇩🇪

A simple, stateless web application for practicing German verb conjugations. Test your knowledge of Präsens, Präteritum, and Perfekt forms!

## Features

- Choose how many verbs to practice (1-20) with an intuitive slider
- Random selection from a database of 20 common German verbs
- Practice 3rd person forms: Präsens (er/sie/es), Präteritum (er/sie/es), and Perfekt
- Perfekt form requires auxiliary verb (hat/ist) - helpful hints guide you
- Optional inputs - skip answers you don't know and see them in results
- Instant feedback with detailed results
- Color-coded scoring system with per-verb gradient colors (red→green based on 0-3 correct)
- Distinct visual grouping for each verb in the results table
- Clean, responsive interface
- Completely stateless - no login or tracking required
- CI/CD pipeline with automated linting and testing

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

### Running with Docker

Build the Docker image:
```bash
docker build -t verbformen .
```

Run the container:
```bash
docker run -p 8000:8000 verbformen
```

Or run in detached mode:
```bash
docker run -d -p 8000:8000 --name verbformen-app verbformen
```

Stop the container:
```bash
docker stop verbformen-app
```

The application will be available at `http://localhost:8000`.

## How to Use

1. **Choose Verb Count**: Use the slider to select how many verbs you want to practice (1-20)
2. **Start a Session**: Click the "Begin Session" button on the welcome screen
3. **Fill in Forms**: Enter the conjugated forms for each randomly selected verb
   - Präsens (3rd person: er/sie/es)
   - Präteritum (3rd person: er/sie/es)
   - Perfekt (include "hat" or "ist" - e.g., "hat gemacht" or "ist gegangen")
4. **Submit**: Click "Submit Answers" to see your results (empty answers are allowed)
5. **Review**: Check your score and see which answers were correct or incorrect
   - Each verb shows a color-coded score (red for 0/3, green for 3/3)
   - Verb groups are visually separated for easy reading
6. **Practice Again**: Start a new session to practice with different verbs

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
- **Linting/Formatting**: ruff (via pre-commit)
- **CI/CD**: GitHub Actions (lint, format check, tests)

## Project Structure

```
verbformen/
├── backend/                  # Python backend
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic models
│   ├── services.py          # Business logic
│   └── tests/               # Test suite
├── frontend/                # Static frontend files
│   ├── index.html          # Main page
│   ├── styles.css          # Styling
│   ├── app.js              # Application logic
│   └── api.js              # API client
├── data/                    # Verb database
│   └── verbs_forms.json
├── .pre-commit-config.yaml  # Pre-commit hooks configuration
├── pyproject.toml           # Project metadata and dependencies
└── uv.lock                  # Locked dependencies for reproducibility
```

## API Endpoints

- `GET /` - Serve the frontend application
- `GET /api/health` - Health check endpoint
- `GET /api/session/start?count=N` - Start a new learning session (count: 1-20, default 10)
- `POST /api/session/submit` - Submit answers and receive graded results

## Scoring System

- Each verb has 3 forms to fill in
- Total forms per session = selected verb count × 3 forms
- Exact string matching (case-sensitive)
- Whitespace is automatically trimmed
- Empty answers are allowed (counted as incorrect)
- Results are color-coded:
  - 🟢 Green (90%+): Excellent
  - 🔵 Blue (70-89%): Good
  - 🟡 Yellow (50-69%): Average
  - 🔴 Red (<50%): Needs practice
- Per-verb score gradient:
  - Red (0/3), Orange (1/3), Lime (2/3), Green (3/3)

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

All 29 tests should pass.

## Linting and Formatting

This project uses [ruff](https://github.com/astral-sh/ruff) for linting and formatting, enforced via pre-commit hooks.

### Setup (required once after cloning)

```bash
uv run pre-commit install
```

### Running Manually

```bash
# Run all pre-commit hooks
uv run pre-commit run --all-files

# Or run ruff directly
uv run ruff check backend/       # Lint
uv run ruff check backend/ --fix # Lint and auto-fix
uv run ruff format backend/      # Format
```

Pre-commit hooks run automatically on every `git commit`. If a hook fails, fix the issues and commit again.

## Continuous Integration

This project uses GitHub Actions for CI. On every push and pull request to `main`:

1. **Lint & Format**: Runs `ruff check` and `ruff format --check`
2. **Tests**: Runs the full pytest suite

See `.github/workflows/ci.yml` for the workflow configuration.

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
2. Run `uv run pre-commit install` to set up the linting hooks
3. Make your changes
4. Run the test suite to ensure nothing breaks
5. Commit your changes (pre-commit hooks will lint/format automatically)
6. Submit your changes

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
