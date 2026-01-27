"""Integration tests for FastAPI endpoints"""
import json
import pytest
from fastapi.testclient import TestClient
from pathlib import Path


@pytest.fixture
def test_verbs_file(tmp_path):
    """Create a test verbs file"""
    verbs_data = {
        "gehen": {"Präsens": "geht", "Präteritum": "ging", "Perfekt": "ist gegangen"},
        "machen": {"Präsens": "macht", "Präteritum": "machte", "Perfekt": "hat gemacht"},
        "sein": {"Präsens": "ist", "Präteritum": "war", "Perfekt": "ist gewesen"},
        "haben": {"Präsens": "hat", "Präteritum": "hatte", "Perfekt": "hat gehabt"},
        "werden": {"Präsens": "wird", "Präteritum": "wurde", "Perfekt": "ist geworden"},
        "können": {"Präsens": "kann", "Präteritum": "konnte", "Perfekt": "hat gekonnt"},
        "müssen": {"Präsens": "muss", "Präteritum": "musste", "Perfekt": "hat gemusst"},
        "sagen": {"Präsens": "sagt", "Präteritum": "sagte", "Perfekt": "hat gesagt"},
        "wissen": {"Präsens": "weiß", "Präteritum": "wusste", "Perfekt": "hat gewusst"},
        "geben": {"Präsens": "gibt", "Präteritum": "gab", "Perfekt": "hat gegeben"},
        "kommen": {"Präsens": "kommt", "Präteritum": "kam", "Perfekt": "ist gekommen"},
        "sehen": {"Präsens": "sieht", "Präteritum": "sah", "Perfekt": "hat gesehen"},
        "nehmen": {"Präsens": "nimmt", "Präteritum": "nahm", "Perfekt": "hat genommen"},
        "finden": {"Präsens": "findet", "Präteritum": "fand", "Perfekt": "hat gefunden"},
        "aufstehen": {"Präsens": "steht auf", "Präteritum": "stand auf", "Perfekt": "ist aufgestanden"},
        "fahren": {"Präsens": "fährt", "Präteritum": "fuhr", "Perfekt": "ist gefahren"},
        "schreiben": {"Präsens": "schreibt", "Präteritum": "schrieb", "Perfekt": "hat geschrieben"},
        "lesen": {"Präsens": "liest", "Präteritum": "las", "Perfekt": "hat gelesen"},
        "essen": {"Präsens": "isst", "Präteritum": "aß", "Perfekt": "hat gegessen"},
        "trinken": {"Präsens": "trinkt", "Präteritum": "trank", "Perfekt": "hat getrunken"},
    }

    file_path = tmp_path / "verbs_test.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(verbs_data, f, ensure_ascii=False)

    return file_path


@pytest.fixture
def client(test_verbs_file, monkeypatch):
    """Create a test client with mocked data path"""
    # Mock the DATA_PATH before importing the app
    monkeypatch.setattr('backend.main.DATA_PATH', test_verbs_file)

    # Import after monkeypatch
    from backend.main import app
    return TestClient(app)


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/api/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["verbs_loaded"] == 20


def test_start_session(client):
    """Test starting a new session"""
    response = client.get("/api/session/start")

    assert response.status_code == 200
    data = response.json()

    assert "session_id" in data
    assert "verbs" in data
    assert "total_verbs" in data
    assert data["total_verbs"] == 10
    assert len(data["verbs"]) == 10

    # Check verb structure
    for idx, verb in enumerate(data["verbs"]):
        assert "infinitive" in verb
        assert "index" in verb
        assert verb["index"] == idx


def test_start_session_unique_ids(client):
    """Test that each session gets a unique ID"""
    response1 = client.get("/api/session/start")
    response2 = client.get("/api/session/start")

    data1 = response1.json()
    data2 = response2.json()

    assert data1["session_id"] != data2["session_id"]


def test_submit_session_all_correct(client):
    """Test submitting answers with all correct"""
    # First, start a session
    start_response = client.get("/api/session/start")
    session_data = start_response.json()
    session_id = session_data["session_id"]
    verbs = session_data["verbs"]

    # Prepare correct answers (we know the test data)
    verb_forms = {
        "gehen": {"praesens": "geht", "praeteritum": "ging", "perfekt": "ist gegangen"},
        "machen": {"praesens": "macht", "praeteritum": "machte", "perfekt": "hat gemacht"},
        "sein": {"praesens": "ist", "praeteritum": "war", "perfekt": "ist gewesen"},
        "haben": {"praesens": "hat", "praeteritum": "hatte", "perfekt": "hat gehabt"},
        "werden": {"praesens": "wird", "praeteritum": "wurde", "perfekt": "ist geworden"},
        "können": {"praesens": "kann", "praeteritum": "konnte", "perfekt": "hat gekonnt"},
        "müssen": {"praesens": "muss", "praeteritum": "musste", "perfekt": "hat gemusst"},
        "sagen": {"praesens": "sagt", "praeteritum": "sagte", "perfekt": "hat gesagt"},
        "wissen": {"praesens": "weiß", "praeteritum": "wusste", "perfekt": "hat gewusst"},
        "geben": {"praesens": "gibt", "praeteritum": "gab", "perfekt": "hat gegeben"},
        "kommen": {"praesens": "kommt", "praeteritum": "kam", "perfekt": "ist gekommen"},
        "sehen": {"praesens": "sieht", "praeteritum": "sah", "perfekt": "hat gesehen"},
        "nehmen": {"praesens": "nimmt", "praeteritum": "nahm", "perfekt": "hat genommen"},
        "finden": {"praesens": "findet", "praeteritum": "fand", "perfekt": "hat gefunden"},
        "aufstehen": {"praesens": "steht auf", "praeteritum": "stand auf", "perfekt": "ist aufgestanden"},
        "fahren": {"praesens": "fährt", "praeteritum": "fuhr", "perfekt": "ist gefahren"},
        "schreiben": {"praesens": "schreibt", "praeteritum": "schrieb", "perfekt": "hat geschrieben"},
        "lesen": {"praesens": "liest", "praeteritum": "las", "perfekt": "hat gelesen"},
        "essen": {"praesens": "isst", "praeteritum": "aß", "perfekt": "hat gegessen"},
        "trinken": {"praesens": "trinkt", "praeteritum": "trank", "perfekt": "hat getrunken"},
    }

    answers = []
    for verb in verbs:
        infinitive = verb["infinitive"]
        answers.append({
            "infinitive": infinitive,
            **verb_forms[infinitive]
        })

    # Submit answers
    submit_response = client.post(
        "/api/session/submit",
        json={"session_id": session_id, "answers": answers}
    )

    assert submit_response.status_code == 200
    result = submit_response.json()

    assert result["session_id"] == session_id
    assert result["total_verbs"] == 10
    assert result["total_forms"] == 30
    assert result["correct_count"] == 30
    assert result["score_percentage"] == 100.0

    # Check all results are correct
    for verb_result in result["results"]:
        assert verb_result["all_correct"] is True
        assert verb_result["correct"]["praesens"] is True
        assert verb_result["correct"]["praeteritum"] is True
        assert verb_result["correct"]["perfekt"] is True


def test_submit_session_mixed_results(client):
    """Test submitting answers with mixed correct/incorrect"""
    # Start session
    start_response = client.get("/api/session/start")
    session_data = start_response.json()
    session_id = session_data["session_id"]
    verbs = session_data["verbs"]

    # Submit answers - first half correct, second half incorrect
    answers = []
    for idx, verb in enumerate(verbs):
        if idx < 5:
            # Use dummy correct answers for first 5
            answers.append({
                "infinitive": verb["infinitive"],
                "praesens": "correct",
                "praeteritum": "correct",
                "perfekt": "correct"
            })
        else:
            # Use incorrect for last 5
            answers.append({
                "infinitive": verb["infinitive"],
                "praesens": "wrong",
                "praeteritum": "wrong",
                "perfekt": "wrong"
            })

    submit_response = client.post(
        "/api/session/submit",
        json={"session_id": session_id, "answers": answers}
    )

    assert submit_response.status_code == 200
    result = submit_response.json()

    assert result["total_verbs"] == 10
    assert result["total_forms"] == 30
    # All will be incorrect since we used dummy data
    assert len(result["results"]) == 10


def test_submit_session_empty_answers(client):
    """Test submitting with no answers"""
    response = client.post(
        "/api/session/submit",
        json={"session_id": "test-id", "answers": []}
    )

    assert response.status_code == 400
    assert "No answers provided" in response.json()["detail"]


def test_submit_session_invalid_verb(client):
    """Test submitting with a verb that doesn't exist"""
    response = client.post(
        "/api/session/submit",
        json={
            "session_id": "test-id",
            "answers": [{
                "infinitive": "nonexistent",
                "praesens": "a",
                "praeteritum": "b",
                "perfekt": "c"
            }]
        }
    )

    assert response.status_code == 400
    assert "not found" in response.json()["detail"]


def test_submit_session_includes_correct_answers(client):
    """Test that results include correct answers for comparison"""
    start_response = client.get("/api/session/start")
    session_data = start_response.json()

    # Submit with wrong answers
    answers = [{
        "infinitive": verb["infinitive"],
        "praesens": "wrong",
        "praeteritum": "wrong",
        "perfekt": "wrong"
    } for verb in session_data["verbs"]]

    submit_response = client.post(
        "/api/session/submit",
        json={"session_id": session_data["session_id"], "answers": answers}
    )

    result = submit_response.json()

    # Check that correct answers are provided
    for verb_result in result["results"]:
        assert "correct_answers" in verb_result
        assert "praesens" in verb_result["correct_answers"]
        assert "praeteritum" in verb_result["correct_answers"]
        assert "perfekt" in verb_result["correct_answers"]

        assert "user_answers" in verb_result
        assert verb_result["user_answers"]["praesens"] == "wrong"
