# Claude Development Notes

## Important: Package Management

**ALWAYS use `uv` as the package manager for this project.**

When working with Python dependencies or running the application:
- Use `uv sync` to initialize the project and install all dependencies
- Use `uv add <package>` to add new dependencies (instead of `pip install`)
- Use `uv remove <package>` to remove dependencies
- Never use standard `pip` or `pip install` commands

## Project Overview

This is a German verb learning webapp built with:
- **Backend**: FastAPI (Python)
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Package Manager**: uv
- **Testing**: pytest
- **Linting/Formatting**: ruff (via pre-commit)

## Development Setup

### Initial Setup

```bash
cd /Users/meacca/dev/verbformen

# Initialize project and install all dependencies
# This creates a virtual environment and installs everything
uv sync

# Activate virtual environment (if needed for manual commands)
source .venv/bin/activate
```

### Running the Application

```bash
# Start the FastAPI server with uv
uv run uvicorn backend.main:app --host 0.0.0.0 --port 8000

# With auto-reload for development
uv run uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# Alternative: activate venv and run directly
source .venv/bin/activate
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

Access the application at: `http://localhost:8000`

### Running Tests

```bash
# Run all tests with uv
uv run pytest backend/tests/ -v

# Run specific test file
uv run pytest backend/tests/test_services.py -v

# Run with coverage (if coverage package is added)
uv run pytest backend/tests/ --cov=backend --cov-report=html
```

### Linting and Formatting (Pre-commit)

This project uses **ruff** for linting and formatting, enforced via **pre-commit** hooks.

```bash
# Install pre-commit hooks (required once after cloning)
uv run pre-commit install

# Run linting/formatting manually on all files
uv run pre-commit run --all-files

# Run ruff directly (without pre-commit)
uv run ruff check backend/       # Lint only
uv run ruff check backend/ --fix # Lint and auto-fix
uv run ruff format backend/      # Format code
```

**Pre-commit hooks run automatically** on every `git commit`:
- `ruff` - Lints code and auto-fixes issues
- `ruff-format` - Formats code consistently

If a hook fails, the commit is blocked. Fix the issues and try again.

## Project Structure

```
/Users/meacca/dev/verbformen/
├── data/
│   └── verbs_forms.json          # 20 German verbs with conjugations
├── backend/
│   ├── __init__.py
│   ├── main.py                   # FastAPI app & API routes
│   ├── models.py                 # Pydantic models for validation
│   ├── services.py               # Business logic (VerbService)
│   └── tests/
│       ├── __init__.py
│       ├── test_services.py      # Unit tests
│       └── test_api.py           # Integration tests
├── frontend/
│   ├── index.html                # Main UI
│   ├── styles.css                # Styling
│   ├── app.js                    # Application logic
│   └── api.js                    # API client
├── .venv/                        # Virtual environment (git ignored)
├── .pre-commit-config.yaml       # Pre-commit hooks configuration
├── pyproject.toml                # Project metadata and dependencies
├── uv.lock                       # Locked dependencies (committed to git)
├── README.md                     # User documentation
└── CLAUDE.md                     # This file
```

## Architecture

### Backend (FastAPI)

**Endpoints:**
- `GET /api/health` - Health check
- `GET /api/session/start` - Start new session, get 10 random verbs
- `POST /api/session/submit` - Submit answers, get graded results
- `GET /` - Serve frontend HTML

**Key Components:**

1. **VerbService** (`backend/services.py`)
   - `load_verbs()`: Load verbs from JSON, cache in memory
   - `get_random_verbs(count=10)`: Random selection
   - `check_answer()`: Compare user input (exact match, strips whitespace)
   - `grade_session()`: Grade all answers, calculate score

2. **Pydantic Models** (`backend/models.py`)
   - `SessionStart`: Response for starting session
   - `SubmitRequest`: Request body for submissions
   - `SessionResult`: Detailed grading results

### Frontend (Vanilla JS)

**Three main screens:**
1. **Start screen**: Welcome message, "Begin Session" button
2. **Quiz screen**: Form with 10 verbs × 3 input fields
3. **Results screen**: Score display + detailed table

**State management:**
- Simple object-based state in `app.js`
- No framework dependencies
- ES6 modules for code organization

### Data Format

`data/verbs_forms.json` stores 3rd person forms:

```json
{
  "infinitive": {
    "Präsens": "3rd person present",
    "Präteritum": "3rd person past",
    "Perfekt": "perfect form"
  }
}
```

Example:
```json
{
  "gehen": {
    "Präsens": "geht",
    "Präteritum": "ging",
    "Perfekt": "ist gegangen"
  }
}
```

## Testing

### Test Coverage

**Backend tests: 23 tests**

Unit tests (`test_services.py`):
- Verb loading and caching
- Random selection logic
- Answer checking (exact match, whitespace, case sensitivity)
- Session grading and scoring

Integration tests (`test_api.py`):
- Health check endpoint
- Session start (random verbs, unique IDs)
- Answer submission (correct, incorrect, mixed)
- Error handling (empty answers, invalid verbs)

### Test Philosophy

- Use temporary files for test data
- Mock `DATA_PATH` in API tests
- Test both happy paths and error cases
- Verify exact string matching behavior
- Check whitespace stripping

## Adding New Verbs

To add more verbs to the dataset:

1. Edit `data/verbs_forms.json`
2. Add entry with infinitive as key
3. Provide all three forms (3rd person):
   ```json
   "schlafen": {
     "Präsens": "schläft",
     "Präteritum": "schlief",
     "Perfekt": "hat geschlossen"
   }
   ```
4. No code changes needed - app reads JSON dynamically

## Dependencies

Dependencies are managed in `pyproject.toml` and locked in `uv.lock`.

### Runtime Dependencies
- `fastapi` - Web framework
- `uvicorn[standard]` - ASGI server
- `pydantic` - Data validation

### Development Dependencies
- `pytest` - Testing framework
- `httpx` - HTTP client for testing
- `ruff` - Fast Python linter and formatter
- `pre-commit` - Git hooks framework

The `uv.lock` file ensures reproducible builds and should be committed to git.

## Common Development Tasks

### Add or remove Python dependencies

```bash
# Add a new package
uv add <package-name>

# Add a dev dependency
uv add --dev <package-name>

# Remove a package
uv remove <package-name>

# Sync dependencies (update venv to match lockfile)
uv sync
```

### Add a new API endpoint

1. Define Pydantic models in `backend/models.py`
2. Add endpoint function in `backend/main.py`
3. Add business logic to `backend/services.py` if needed
4. Write tests in `backend/tests/test_api.py`

### Modify answer checking logic

1. Update `VerbService.check_answer()` in `backend/services.py`
2. Update corresponding tests in `test_services.py`
3. Run tests to verify behavior

### Update frontend UI

1. Modify HTML structure in `frontend/index.html`
2. Update styles in `frontend/styles.css`
3. Adjust JavaScript logic in `frontend/app.js`
4. Test in browser at `http://localhost:8000`

## Performance Notes

- Verbs are loaded once and cached in memory
- No database queries - all data in JSON file
- Stateless design - no session storage needed
- Frontend is served directly by FastAPI (no separate server)

## Security Considerations

- Input validation via Pydantic models
- No user authentication (simple learning tool)
- CORS enabled for localhost development
- Exact string matching prevents injection attacks

## Future Enhancement Ideas

1. **Improved Matching**
   - Case-insensitive comparison
   - Accept alternate valid forms
   - Fuzzy matching with suggestions

2. **User Experience**
   - Progress indicator during quiz
   - Timer mode for practice
   - Show hints/tips
   - Keyboard shortcuts

3. **Content**
   - Difficulty levels (beginner/advanced)
   - Filter by verb type (regular/irregular)
   - Practice specific tenses only
   - More verbs (target 100+)

4. **Analytics**
   - Track commonly missed verbs (client-side)
   - Personal best scores (localStorage)
   - Study recommendations

5. **Deployment**
   - Docker container
   - Deploy to cloud (Railway, Fly.io, etc.)
   - Add CI/CD pipeline

## Troubleshooting

### Port already in use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Import errors
```bash
# Make sure you're in the project root
cd /Users/meacca/dev/verbformen

# Sync dependencies (recreates venv if needed)
uv sync

# Verify virtual environment is activated
which python  # Should show .venv path
```

### Tests failing
```bash
# Clear pytest cache
rm -rf .pytest_cache

# Run tests with verbose output
pytest backend/tests/ -v -s
```

### Frontend not loading
```bash
# Check if frontend directory exists
ls frontend/

# Verify FastAPI is serving static files
curl http://localhost:8000/static/app.js
```

## Git Workflow

The project uses Git for version control. Current branch: `main`

### Common Git Commands
```bash
# Check status
git status

# Stage changes
git add .

# Commit with message
git commit -m "Description of changes"

# Push to remote
git push origin main
```

## API Documentation

FastAPI provides automatic interactive API docs:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

These are generated automatically from the code and Pydantic models.

## Notes for Claude

When working on this project:
1. **Always use `uv`** for Python package management
2. Read existing code before making changes
3. Run tests after modifications
4. **Run `uv run ruff check backend/ --fix && uv run ruff format backend/`** before committing
5. Keep it simple - avoid over-engineering
6. The app is intentionally stateless
7. Frontend is vanilla JS - no build step needed
8. Data file can be edited directly (no migration needed)

## Contact & Feedback

For issues or suggestions, create an issue on the project repository.
