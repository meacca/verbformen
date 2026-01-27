"""FastAPI application for German verb learning webapp"""

import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.models import (
    SessionResult,
    SessionStart,
    SubmitRequest,
    VerbInfo,
    VerbResult,
)
from backend.services import VerbService

# Initialize FastAPI app
app = FastAPI(
    title="German Verb Learning API",
    description="API for learning German verb forms",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://localhost:3000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize verb service
DATA_PATH = Path(__file__).parent.parent / "data" / "verbs_forms.json"
verb_service = VerbService(str(DATA_PATH))


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    try:
        verbs = verb_service.load_verbs()
        return {"status": "healthy", "verbs_loaded": len(verbs)}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Service unhealthy: {str(e)}"
        ) from e


@app.get("/api/session/start", response_model=SessionStart)
async def start_session(count: int = Query(default=10, ge=1, le=20)):
    """
    Start a new learning session

    Args:
        count: Number of verbs to practice (1-20, default 10)

    Returns randomly selected verbs in infinitive form
    """
    try:
        # Generate unique session ID
        session_id = str(uuid.uuid4())

        # Get random verbs
        infinitives = verb_service.get_random_verbs(count=count)

        # Create verb info objects with indices
        verbs = [
            VerbInfo(infinitive=infinitive, index=idx)
            for idx, infinitive in enumerate(infinitives)
        ]

        return SessionStart(session_id=session_id, verbs=verbs, total_verbs=len(verbs))

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to start session: {str(e)}"
        ) from e


@app.post("/api/session/submit", response_model=SessionResult)
async def submit_session(request: SubmitRequest):
    """
    Submit answers for grading

    Accepts user answers and returns detailed results with scores
    """
    try:
        # Validate that we have answers
        if not request.answers:
            raise ValueError("No answers provided")

        # Convert Pydantic models to dictionaries for service layer
        answers_dict = [
            {
                "infinitive": answer.infinitive,
                "praesens": answer.praesens,
                "praeteritum": answer.praeteritum,
                "perfekt": answer.perfekt,
            }
            for answer in request.answers
        ]

        # Grade the session
        grading_result = verb_service.grade_session(answers_dict)

        # Convert results to Pydantic models
        verb_results = [
            VerbResult(
                infinitive=result["infinitive"],
                correct=result["correct"],
                user_answers=result["user_answers"],
                correct_answers=result["correct_answers"],
                all_correct=result["all_correct"],
            )
            for result in grading_result["results"]
        ]

        return SessionResult(
            session_id=request.session_id,
            total_verbs=grading_result["total_verbs"],
            total_forms=grading_result["total_forms"],
            correct_count=grading_result["correct_count"],
            score_percentage=grading_result["score_percentage"],
            results=verb_results,
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to grade session: {str(e)}"
        ) from e


# Mount static files (frontend)
FRONTEND_PATH = Path(__file__).parent.parent / "frontend"
if FRONTEND_PATH.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_PATH)), name="static")

    @app.get("/")
    async def serve_frontend():
        """Serve the main HTML page"""
        index_path = FRONTEND_PATH / "index.html"
        if index_path.exists():
            return FileResponse(index_path)
        raise HTTPException(status_code=404, detail="Frontend not found")
