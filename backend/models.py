"""Pydantic models for API request and response validation"""

from pydantic import BaseModel, Field


class VerbInfo(BaseModel):
    """Information about a verb for display in the quiz"""

    infinitive: str = Field(..., description="The verb in infinitive form")
    index: int = Field(..., description="Position in the quiz (0-9)")
    translations: list[str] = Field(
        default_factory=list, description="Russian translations of the verb"
    )
    example: str = Field(default="", description="Example sentence using the verb")


class SessionStart(BaseModel):
    """Response model for starting a new session"""

    session_id: str = Field(..., description="Unique identifier for this session")
    verbs: list[VerbInfo] = Field(..., description="List of 10 verbs for the quiz")
    total_verbs: int = Field(..., description="Total number of verbs in the session")


class UserAnswer(BaseModel):
    """User's answer for a single verb"""

    infinitive: str = Field(..., description="The verb in infinitive form")
    praesens: str = Field(..., description="Präsens form (3rd person)")
    praeteritum: str = Field(..., description="Präteritum form (3rd person)")
    perfekt: str = Field(..., description="Perfekt form")


class SubmitRequest(BaseModel):
    """Request model for submitting quiz answers"""

    session_id: str = Field(..., description="Session identifier")
    answers: list[UserAnswer] = Field(
        ..., description="List of user answers for all verbs"
    )


class VerbResult(BaseModel):
    """Result for a single verb"""

    infinitive: str = Field(..., description="The verb in infinitive form")
    correct: dict[str, bool] = Field(
        ..., description="Correctness for each form (praesens, praeteritum, perfekt)"
    )
    user_answers: dict[str, str] = Field(..., description="User's submitted answers")
    correct_answers: dict[str, str] = Field(..., description="Correct answers")
    all_correct: bool = Field(..., description="True if all three forms are correct")


class SessionResult(BaseModel):
    """Response model for graded session results"""

    session_id: str = Field(..., description="Session identifier")
    total_verbs: int = Field(..., description="Total number of verbs in the session")
    total_forms: int = Field(
        ..., description="Total number of forms checked (verbs × 3)"
    )
    correct_count: int = Field(..., description="Number of correct forms")
    score_percentage: float = Field(..., description="Percentage score (0-100)")
    results: list[VerbResult] = Field(..., description="Detailed results for each verb")
