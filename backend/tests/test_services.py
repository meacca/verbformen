"""Unit tests for VerbService"""
import json
import pytest
from pathlib import Path
from backend.services import VerbService


@pytest.fixture
def sample_verbs_file(tmp_path):
    """Create a temporary verbs JSON file for testing"""
    verbs_data = {
        "gehen": {
            "Präsens": "geht",
            "Präteritum": "ging",
            "Perfekt": "ist gegangen"
        },
        "machen": {
            "Präsens": "macht",
            "Präteritum": "machte",
            "Perfekt": "hat gemacht"
        },
        "sein": {
            "Präsens": "ist",
            "Präteritum": "war",
            "Perfekt": "ist gewesen"
        },
        "haben": {
            "Präsens": "hat",
            "Präteritum": "hatte",
            "Perfekt": "hat gehabt"
        },
        "werden": {
            "Präsens": "wird",
            "Präteritum": "wurde",
            "Perfekt": "ist geworden"
        }
    }

    file_path = tmp_path / "verbs.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(verbs_data, f, ensure_ascii=False)

    return file_path


@pytest.fixture
def verb_service(sample_verbs_file):
    """Create a VerbService instance with test data"""
    return VerbService(str(sample_verbs_file))


def test_load_verbs(verb_service):
    """Test loading verbs from JSON file"""
    verbs = verb_service.load_verbs()

    assert len(verbs) == 5
    assert "gehen" in verbs
    assert verbs["gehen"]["Präsens"] == "geht"


def test_load_verbs_caching(verb_service):
    """Test that verbs are cached after first load"""
    verbs1 = verb_service.load_verbs()
    verbs2 = verb_service.load_verbs()

    # Should return the same object (cached)
    assert verbs1 is verbs2


def test_load_verbs_file_not_found():
    """Test error handling when file doesn't exist"""
    service = VerbService("/nonexistent/path.json")

    with pytest.raises(FileNotFoundError):
        service.load_verbs()


def test_get_random_verbs(verb_service):
    """Test getting random verb selection"""
    verbs = verb_service.get_random_verbs(count=3)

    assert len(verbs) == 3
    assert all(isinstance(v, str) for v in verbs)
    assert len(set(verbs)) == 3  # All unique


def test_get_random_verbs_all(verb_service):
    """Test getting all verbs"""
    verbs = verb_service.get_random_verbs(count=5)

    assert len(verbs) == 5


def test_get_random_verbs_too_many(verb_service):
    """Test error when requesting more verbs than available"""
    with pytest.raises(ValueError, match="Not enough verbs"):
        verb_service.get_random_verbs(count=10)


def test_check_answer_all_correct(verb_service):
    """Test checking answers when all are correct"""
    result = verb_service.check_answer(
        "gehen",
        "geht",
        "ging",
        "ist gegangen"
    )

    assert result["praesens"] is True
    assert result["praeteritum"] is True
    assert result["perfekt"] is True


def test_check_answer_all_incorrect(verb_service):
    """Test checking answers when all are incorrect"""
    result = verb_service.check_answer(
        "gehen",
        "wrong1",
        "wrong2",
        "wrong3"
    )

    assert result["praesens"] is False
    assert result["praeteritum"] is False
    assert result["perfekt"] is False


def test_check_answer_mixed(verb_service):
    """Test checking answers with mixed correct/incorrect"""
    result = verb_service.check_answer(
        "machen",
        "macht",  # correct
        "wrong",  # incorrect
        "hat gemacht"  # correct
    )

    assert result["praesens"] is True
    assert result["praeteritum"] is False
    assert result["perfekt"] is True


def test_check_answer_strips_whitespace(verb_service):
    """Test that whitespace is stripped from user answers"""
    result = verb_service.check_answer(
        "gehen",
        "  geht  ",
        " ging ",
        "ist gegangen   "
    )

    assert result["praesens"] is True
    assert result["praeteritum"] is True
    assert result["perfekt"] is True


def test_check_answer_case_sensitive(verb_service):
    """Test that comparison is case-sensitive"""
    result = verb_service.check_answer(
        "gehen",
        "Geht",  # Wrong case
        "ging",
        "ist gegangen"
    )

    assert result["praesens"] is False
    assert result["praeteritum"] is True


def test_check_answer_verb_not_found(verb_service):
    """Test error when verb doesn't exist"""
    with pytest.raises(ValueError, match="not found"):
        verb_service.check_answer("nonexistent", "a", "b", "c")


def test_grade_session_all_correct(verb_service):
    """Test grading a session with all correct answers"""
    answers = [
        {
            "infinitive": "gehen",
            "praesens": "geht",
            "praeteritum": "ging",
            "perfekt": "ist gegangen"
        },
        {
            "infinitive": "machen",
            "praesens": "macht",
            "praeteritum": "machte",
            "perfekt": "hat gemacht"
        }
    ]

    result = verb_service.grade_session(answers)

    assert result["total_verbs"] == 2
    assert result["total_forms"] == 6
    assert result["correct_count"] == 6
    assert result["score_percentage"] == 100.0
    assert len(result["results"]) == 2
    assert result["results"][0]["all_correct"] is True


def test_grade_session_mixed(verb_service):
    """Test grading a session with mixed results"""
    answers = [
        {
            "infinitive": "gehen",
            "praesens": "geht",  # correct
            "praeteritum": "wrong",  # incorrect
            "perfekt": "ist gegangen"  # correct
        },
        {
            "infinitive": "machen",
            "praesens": "wrong",  # incorrect
            "praeteritum": "machte",  # correct
            "perfekt": "wrong"  # incorrect
        }
    ]

    result = verb_service.grade_session(answers)

    assert result["total_verbs"] == 2
    assert result["total_forms"] == 6
    assert result["correct_count"] == 3
    assert result["score_percentage"] == 50.0
    assert result["results"][0]["all_correct"] is False
    assert result["results"][1]["all_correct"] is False


def test_grade_session_includes_correct_answers(verb_service):
    """Test that grading result includes correct answers for comparison"""
    answers = [
        {
            "infinitive": "sein",
            "praesens": "wrong",
            "praeteritum": "wrong",
            "perfekt": "wrong"
        }
    ]

    result = verb_service.grade_session(answers)

    verb_result = result["results"][0]
    assert verb_result["correct_answers"]["praesens"] == "ist"
    assert verb_result["correct_answers"]["praeteritum"] == "war"
    assert verb_result["correct_answers"]["perfekt"] == "ist gewesen"
    assert verb_result["user_answers"]["praesens"] == "wrong"
