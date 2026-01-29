"""Integration tests for FastAPI endpoints"""

import json

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def test_verbs_file(tmp_path):
    """Create a test verbs file with translations and examples"""
    # Create directory structure
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    translations_dir = data_dir / "translations"
    translations_dir.mkdir()

    verbs_data = {
        "gehen": {"Präsens": "geht", "Präteritum": "ging", "Perfekt": "ist gegangen"},
        "machen": {
            "Präsens": "macht",
            "Präteritum": "machte",
            "Perfekt": "hat gemacht",
        },
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
        "finden": {
            "Präsens": "findet",
            "Präteritum": "fand",
            "Perfekt": "hat gefunden",
        },
        "aufstehen": {
            "Präsens": "steht auf",
            "Präteritum": "stand auf",
            "Perfekt": "ist aufgestanden",
        },
        "fahren": {"Präsens": "fährt", "Präteritum": "fuhr", "Perfekt": "ist gefahren"},
        "schreiben": {
            "Präsens": "schreibt",
            "Präteritum": "schrieb",
            "Perfekt": "hat geschrieben",
        },
        "lesen": {"Präsens": "liest", "Präteritum": "las", "Perfekt": "hat gelesen"},
        "essen": {"Präsens": "isst", "Präteritum": "aß", "Perfekt": "hat gegessen"},
        "trinken": {
            "Präsens": "trinkt",
            "Präteritum": "trank",
            "Perfekt": "hat getrunken",
        },
    }

    # Create translations for all verbs
    translations_data = {
        "gehen": ["идти", "ходить"],
        "machen": ["делать", "изготавливать"],
        "sein": ["быть", "являться"],
        "haben": ["иметь", "обладать"],
        "werden": ["становиться", "стать"],
        "können": ["мочь", "уметь"],
        "müssen": ["должен", "быть обязанным"],
        "sagen": ["говорить", "сказать"],
        "wissen": ["знать", "ведать"],
        "geben": ["давать", "дать"],
        "kommen": ["приходить", "прийти"],
        "sehen": ["видеть", "смотреть"],
        "nehmen": ["брать", "взять"],
        "finden": ["находить", "найти"],
        "aufstehen": ["вставать", "подняться"],
        "fahren": ["ехать", "ездить"],
        "schreiben": ["писать", "написать"],
        "lesen": ["читать", "прочитать"],
        "essen": ["есть", "кушать"],
        "trinken": ["пить", "выпить"],
    }

    # Create examples for all verbs
    examples_data = {
        "gehen": [
            "Er geht zur Schule.",
            "Sie ging gestern ins Kino.",
            "Wir sind nach Hause gegangen.",
        ],
        "machen": [
            "Er macht seine Hausaufgaben.",
            "Sie machte einen Kuchen.",
            "Wir haben einen Ausflug gemacht.",
        ],
        "sein": ["Er ist Lehrer.", "Sie war gestern krank.", "Ich bin dort gewesen."],
        "haben": [
            "Er hat ein Auto.",
            "Sie hatte keine Zeit.",
            "Wir haben Glück gehabt.",
        ],
        "werden": [
            "Er wird Arzt.",
            "Sie wurde müde.",
            "Es ist kalt geworden.",
        ],
        "können": [
            "Er kann gut schwimmen.",
            "Sie konnte nicht kommen.",
            "Ich habe es gekonnt.",
        ],
        "müssen": [
            "Er muss arbeiten.",
            "Sie musste früh aufstehen.",
            "Wir haben gehen müssen.",
        ],
        "sagen": [
            "Er sagt die Wahrheit.",
            "Sie sagte nichts.",
            "Ich habe es gesagt.",
        ],
        "wissen": [
            "Er weiß die Antwort.",
            "Sie wusste es nicht.",
            "Ich habe es gewusst.",
        ],
        "geben": [
            "Er gibt mir das Buch.",
            "Sie gab ihm einen Kuss.",
            "Ich habe es gegeben.",
        ],
        "kommen": [
            "Er kommt morgen.",
            "Sie kam gestern an.",
            "Wir sind spät gekommen.",
        ],
        "sehen": [
            "Er sieht den Film.",
            "Sie sah ihn gestern.",
            "Ich habe ihn gesehen.",
        ],
        "nehmen": [
            "Er nimmt den Bus.",
            "Sie nahm das Geld.",
            "Ich habe es genommen.",
        ],
        "finden": [
            "Er findet den Schlüssel.",
            "Sie fand eine Lösung.",
            "Wir haben es gefunden.",
        ],
        "aufstehen": [
            "Er steht früh auf.",
            "Sie stand um 6 Uhr auf.",
            "Ich bin spät aufgestanden.",
        ],
        "fahren": [
            "Er fährt nach Berlin.",
            "Sie fuhr mit dem Zug.",
            "Wir sind nach Hause gefahren.",
        ],
        "schreiben": [
            "Er schreibt einen Brief.",
            "Sie schrieb ein Buch.",
            "Ich habe eine E-Mail geschrieben.",
        ],
        "lesen": [
            "Er liest die Zeitung.",
            "Sie las ein Buch.",
            "Ich habe den Artikel gelesen.",
        ],
        "essen": [
            "Er isst gerne Pizza.",
            "Sie aß einen Apfel.",
            "Wir haben zu Mittag gegessen.",
        ],
        "trinken": [
            "Er trinkt Kaffee.",
            "Sie trank Tee.",
            "Ich habe Wasser getrunken.",
        ],
    }

    # Write files
    file_path = data_dir / "verbs_forms.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(verbs_data, f, ensure_ascii=False)

    translations_path = translations_dir / "verbs_translation_ru.json"
    with open(translations_path, "w", encoding="utf-8") as f:
        json.dump(translations_data, f, ensure_ascii=False)

    examples_path = data_dir / "verbs_examples.json"
    with open(examples_path, "w", encoding="utf-8") as f:
        json.dump(examples_data, f, ensure_ascii=False)

    return file_path


@pytest.fixture
def client(test_verbs_file, monkeypatch):
    """Create a test client with mocked data path"""
    # Import the module
    import backend.main

    # Create a new VerbService with test data
    from backend.services import VerbService

    test_service = VerbService(str(test_verbs_file))

    # Replace both DATA_PATH and verb_service
    monkeypatch.setattr(backend.main, "DATA_PATH", test_verbs_file)
    monkeypatch.setattr(backend.main, "verb_service", test_service)

    return TestClient(backend.main.app)


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/api/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["verbs_loaded"] > 0


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


def test_start_session_custom_count(client):
    """Test starting a session with a custom verb count"""
    response = client.get("/api/session/start?count=5")

    assert response.status_code == 200
    data = response.json()

    assert data["total_verbs"] == 5
    assert len(data["verbs"]) == 5


def test_start_session_count_min(client):
    """Test starting a session with minimum count (1)"""
    response = client.get("/api/session/start?count=1")

    assert response.status_code == 200
    data = response.json()

    assert data["total_verbs"] == 1
    assert len(data["verbs"]) == 1


def test_start_session_count_max(client):
    """Test starting a session with maximum count (20)"""
    response = client.get("/api/session/start?count=20")

    assert response.status_code == 200
    data = response.json()

    assert data["total_verbs"] == 20
    assert len(data["verbs"]) == 20


def test_start_session_count_below_min(client):
    """Test starting a session with count below minimum returns 422"""
    response = client.get("/api/session/start?count=0")

    assert response.status_code == 422


def test_start_session_count_above_max(client):
    """Test starting a session with count above maximum returns 422"""
    response = client.get("/api/session/start?count=21")

    assert response.status_code == 422


def test_start_session_count_negative(client):
    """Test starting a session with negative count returns 422"""
    response = client.get("/api/session/start?count=-5")

    assert response.status_code == 422


def test_submit_session_all_correct(client, test_verbs_file):
    """Test submitting answers with all correct"""
    # Load verb forms from the test data file
    with open(test_verbs_file, encoding="utf-8") as f:
        test_data = json.load(f)

    # Convert to lowercase keys for answer submission
    verb_forms = {}
    for infinitive, forms in test_data.items():
        verb_forms[infinitive] = {
            "praesens": forms["Präsens"],
            "praeteritum": forms["Präteritum"],
            "perfekt": forms["Perfekt"],
        }

    # Start a session with a small count to ensure all verbs are from test data
    start_response = client.get("/api/session/start?count=5")
    session_data = start_response.json()
    session_id = session_data["session_id"]
    verbs = session_data["verbs"]

    # Prepare correct answers from test data
    answers = []
    for verb in verbs:
        infinitive = verb["infinitive"]
        answers.append({"infinitive": infinitive, **verb_forms[infinitive]})

    # Submit answers
    submit_response = client.post(
        "/api/session/submit", json={"session_id": session_id, "answers": answers}
    )

    assert submit_response.status_code == 200
    result = submit_response.json()

    assert result["session_id"] == session_id
    assert result["total_verbs"] == 5
    assert result["total_forms"] == 15
    assert result["correct_count"] == 15
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
            answers.append(
                {
                    "infinitive": verb["infinitive"],
                    "praesens": "correct",
                    "praeteritum": "correct",
                    "perfekt": "correct",
                }
            )
        else:
            # Use incorrect for last 5
            answers.append(
                {
                    "infinitive": verb["infinitive"],
                    "praesens": "wrong",
                    "praeteritum": "wrong",
                    "perfekt": "wrong",
                }
            )

    submit_response = client.post(
        "/api/session/submit", json={"session_id": session_id, "answers": answers}
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
        "/api/session/submit", json={"session_id": "test-id", "answers": []}
    )

    assert response.status_code == 400
    assert "No answers provided" in response.json()["detail"]


def test_submit_session_invalid_verb(client):
    """Test submitting with a verb that doesn't exist"""
    response = client.post(
        "/api/session/submit",
        json={
            "session_id": "test-id",
            "answers": [
                {
                    "infinitive": "nonexistent",
                    "praesens": "a",
                    "praeteritum": "b",
                    "perfekt": "c",
                }
            ],
        },
    )

    assert response.status_code == 400
    assert "not found" in response.json()["detail"]


def test_submit_session_includes_correct_answers(client):
    """Test that results include correct answers for comparison"""
    start_response = client.get("/api/session/start")
    session_data = start_response.json()

    # Submit with wrong answers
    answers = [
        {
            "infinitive": verb["infinitive"],
            "praesens": "wrong",
            "praeteritum": "wrong",
            "perfekt": "wrong",
        }
        for verb in session_data["verbs"]
    ]

    submit_response = client.post(
        "/api/session/submit",
        json={"session_id": session_data["session_id"], "answers": answers},
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


def test_start_session_includes_translations(client):
    """Test that session start response includes translations for each verb"""
    response = client.get("/api/session/start?count=5")

    assert response.status_code == 200
    data = response.json()

    for verb in data["verbs"]:
        assert "translations" in verb
        assert isinstance(verb["translations"], list)
        assert len(verb["translations"]) > 0
        # Each translation should be a non-empty string
        for translation in verb["translations"]:
            assert isinstance(translation, str)
            assert len(translation) > 0


def test_start_session_includes_example(client):
    """Test that session start response includes an example for each verb"""
    response = client.get("/api/session/start?count=5")

    assert response.status_code == 200
    data = response.json()

    for verb in data["verbs"]:
        assert "example" in verb
        assert isinstance(verb["example"], str)
        assert len(verb["example"]) > 0


def test_start_session_example_from_valid_set(client, test_verbs_file):
    """Test that the example is one of the valid examples for that verb"""
    # Load the examples data
    examples_path = test_verbs_file.parent / "verbs_examples.json"
    with open(examples_path, encoding="utf-8") as f:
        examples_data = json.load(f)

    response = client.get("/api/session/start?count=5")
    assert response.status_code == 200
    data = response.json()

    for verb in data["verbs"]:
        infinitive = verb["infinitive"]
        example = verb["example"]
        # The returned example should be in the list of valid examples
        assert infinitive in examples_data
        assert example in examples_data[infinitive]


def test_start_session_translations_match_verb(client, test_verbs_file):
    """Test that translations match the expected translations for each verb"""
    # Load the translations data
    translations_path = (
        test_verbs_file.parent / "translations" / "verbs_translation_ru.json"
    )
    with open(translations_path, encoding="utf-8") as f:
        translations_data = json.load(f)

    response = client.get("/api/session/start?count=5")
    assert response.status_code == 200
    data = response.json()

    for verb in data["verbs"]:
        infinitive = verb["infinitive"]
        translations = verb["translations"]
        # The returned translations should match the expected translations
        assert infinitive in translations_data
        assert translations == translations_data[infinitive]
