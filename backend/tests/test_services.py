"""Unit tests for VerbService"""

import json
from pathlib import Path

import pytest

from backend.services import VerbService

DATA_PATH = Path(__file__).parent.parent.parent / "data" / "verbs_forms.json"
TRANSLATIONS_RU_PATH = (
    Path(__file__).parent.parent.parent
    / "data"
    / "translations"
    / "verbs_translation_ru.json"
)
EXAMPLES_PATH = Path(__file__).parent.parent.parent / "data" / "verbs_examples.json"
EXPECTED_KEYS = {"Präsens", "Präteritum", "Perfekt"}


@pytest.fixture
def sample_verbs_file(tmp_path):
    """Create a temporary verbs JSON file for testing"""
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
    }

    file_path = tmp_path / "verbs.json"
    with open(file_path, "w", encoding="utf-8") as f:
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
    result = verb_service.check_answer("gehen", "geht", "ging", "ist gegangen")

    assert result["praesens"] is True
    assert result["praeteritum"] is True
    assert result["perfekt"] is True


def test_check_answer_all_incorrect(verb_service):
    """Test checking answers when all are incorrect"""
    result = verb_service.check_answer("gehen", "wrong1", "wrong2", "wrong3")

    assert result["praesens"] is False
    assert result["praeteritum"] is False
    assert result["perfekt"] is False


def test_check_answer_mixed(verb_service):
    """Test checking answers with mixed correct/incorrect"""
    result = verb_service.check_answer(
        "machen",
        "macht",  # correct
        "wrong",  # incorrect
        "hat gemacht",  # correct
    )

    assert result["praesens"] is True
    assert result["praeteritum"] is False
    assert result["perfekt"] is True


def test_check_answer_strips_whitespace(verb_service):
    """Test that whitespace is stripped from user answers"""
    result = verb_service.check_answer("gehen", "  geht  ", " ging ", "ist gegangen   ")

    assert result["praesens"] is True
    assert result["praeteritum"] is True
    assert result["perfekt"] is True


def test_check_answer_case_sensitive(verb_service):
    """Test that comparison is case-sensitive"""
    result = verb_service.check_answer(
        "gehen",
        "Geht",  # Wrong case
        "ging",
        "ist gegangen",
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
            "perfekt": "ist gegangen",
        },
        {
            "infinitive": "machen",
            "praesens": "macht",
            "praeteritum": "machte",
            "perfekt": "hat gemacht",
        },
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
            "perfekt": "ist gegangen",  # correct
        },
        {
            "infinitive": "machen",
            "praesens": "wrong",  # incorrect
            "praeteritum": "machte",  # correct
            "perfekt": "wrong",  # incorrect
        },
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
            "perfekt": "wrong",
        }
    ]

    result = verb_service.grade_session(answers)

    verb_result = result["results"][0]
    assert verb_result["correct_answers"]["praesens"] == "ist"
    assert verb_result["correct_answers"]["praeteritum"] == "war"
    assert verb_result["correct_answers"]["perfekt"] == "ist gewesen"
    assert verb_result["user_answers"]["praesens"] == "wrong"


class TestVerbsDataFile:
    """Tests for validating the structure of the verbs_forms.json data file"""

    def test_data_file_exists(self):
        """Test that the verbs data file exists"""
        assert DATA_PATH.exists(), f"Data file not found: {DATA_PATH}"

    def test_data_file_is_valid_json(self):
        """Test that the data file is valid JSON"""
        with open(DATA_PATH, encoding="utf-8") as f:
            data = json.load(f)
        assert isinstance(data, dict)

    def test_data_file_has_verbs(self):
        """Test that the data file contains at least one verb"""
        with open(DATA_PATH, encoding="utf-8") as f:
            data = json.load(f)
        assert len(data) > 0, "Data file contains no verbs"

    def test_each_verb_has_exactly_three_keys(self):
        """Test that each verb entry has exactly 3 keys: Präsens, Präteritum, Perfekt"""
        with open(DATA_PATH, encoding="utf-8") as f:
            data = json.load(f)

        for verb, forms in data.items():
            assert isinstance(forms, dict), f"Verb '{verb}' value is not a dict"
            assert set(forms.keys()) == EXPECTED_KEYS, (
                f"Verb '{verb}' has keys {set(forms.keys())}, expected {EXPECTED_KEYS}"
            )

    def test_all_verb_forms_are_non_empty_strings(self):
        """Test that all verb forms are non-empty strings"""
        with open(DATA_PATH, encoding="utf-8") as f:
            data = json.load(f)

        for verb, forms in data.items():
            for key, value in forms.items():
                assert isinstance(value, str), (
                    f"Verb '{verb}' form '{key}' is not a string"
                )
                assert len(value.strip()) > 0, f"Verb '{verb}' form '{key}' is empty"


class TestDataFilesConsistency:
    """Tests to verify all data files have consistent verb keys"""

    def test_translations_file_exists(self):
        """Test that the Russian translations file exists"""
        assert TRANSLATIONS_RU_PATH.exists(), (
            f"Translations file not found: {TRANSLATIONS_RU_PATH}"
        )

    def test_examples_file_exists(self):
        """Test that the examples file exists"""
        assert EXAMPLES_PATH.exists(), f"Examples file not found: {EXAMPLES_PATH}"

    def test_all_files_have_same_keys(self):
        """Test that all three data files have identical verb keys"""
        with open(DATA_PATH, encoding="utf-8") as f:
            verbs_forms = json.load(f)
        with open(TRANSLATIONS_RU_PATH, encoding="utf-8") as f:
            translations_ru = json.load(f)
        with open(EXAMPLES_PATH, encoding="utf-8") as f:
            examples = json.load(f)

        forms_keys = set(verbs_forms.keys())
        translations_keys = set(translations_ru.keys())
        examples_keys = set(examples.keys())

        # Check translations has same keys as forms
        missing_in_translations = forms_keys - translations_keys
        extra_in_translations = translations_keys - forms_keys
        assert not missing_in_translations, (
            f"Verbs missing in translations: {missing_in_translations}"
        )
        assert not extra_in_translations, (
            f"Extra verbs in translations: {extra_in_translations}"
        )

        # Check examples has same keys as forms
        missing_in_examples = forms_keys - examples_keys
        extra_in_examples = examples_keys - forms_keys
        assert not missing_in_examples, (
            f"Verbs missing in examples: {missing_in_examples}"
        )
        assert not extra_in_examples, f"Extra verbs in examples: {extra_in_examples}"

    def test_translations_format(self):
        """Test that each translation value is a non-empty list of strings"""
        with open(TRANSLATIONS_RU_PATH, encoding="utf-8") as f:
            translations = json.load(f)

        for verb, trans_list in translations.items():
            assert isinstance(trans_list, list), (
                f"Verb '{verb}' translations is not a list"
            )
            assert len(trans_list) > 0, f"Verb '{verb}' has no translations"
            for trans in trans_list:
                assert isinstance(trans, str), (
                    f"Verb '{verb}' has non-string translation: {trans}"
                )
                assert len(trans.strip()) > 0, f"Verb '{verb}' has empty translation"

    def test_examples_format(self):
        """Test that each example value is a list of 2-3 non-empty strings"""
        with open(EXAMPLES_PATH, encoding="utf-8") as f:
            examples = json.load(f)

        for verb, example_list in examples.items():
            assert isinstance(example_list, list), (
                f"Verb '{verb}' examples is not a list"
            )
            assert 2 <= len(example_list) <= 3, (
                f"Verb '{verb}' has {len(example_list)} examples, expected 2-3"
            )
            for example in example_list:
                assert isinstance(example, str), (
                    f"Verb '{verb}' has non-string example: {example}"
                )
                assert len(example.strip()) > 0, f"Verb '{verb}' has empty example"


@pytest.fixture
def verb_service_with_hints(tmp_path):
    """Create a VerbService instance with test data including translations and examples"""
    # Create data directory structure
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    translations_dir = data_dir / "translations"
    translations_dir.mkdir()

    # Create verbs file
    verbs_data = {
        "gehen": {"Präsens": "geht", "Präteritum": "ging", "Perfekt": "ist gegangen"},
        "machen": {
            "Präsens": "macht",
            "Präteritum": "machte",
            "Perfekt": "hat gemacht",
        },
        "sein": {"Präsens": "ist", "Präteritum": "war", "Perfekt": "ist gewesen"},
    }
    verbs_path = data_dir / "verbs_forms.json"
    with open(verbs_path, "w", encoding="utf-8") as f:
        json.dump(verbs_data, f, ensure_ascii=False)

    # Create translations file
    translations_data = {
        "gehen": ["идти", "ходить"],
        "machen": ["делать", "изготавливать"],
        "sein": ["быть", "являться"],
    }
    translations_path = translations_dir / "verbs_translation_ru.json"
    with open(translations_path, "w", encoding="utf-8") as f:
        json.dump(translations_data, f, ensure_ascii=False)

    # Create examples file
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
        "sein": [
            "Er ist Lehrer.",
            "Sie war gestern krank.",
            "Ich bin dort gewesen.",
        ],
    }
    examples_path = data_dir / "verbs_examples.json"
    with open(examples_path, "w", encoding="utf-8") as f:
        json.dump(examples_data, f, ensure_ascii=False)

    return VerbService(str(verbs_path))


class TestVerbServiceHints:
    """Tests for translations and examples loading"""

    def test_load_translations(self, verb_service_with_hints):
        """Test loading translations from JSON file"""
        translations = verb_service_with_hints.load_translations()

        assert len(translations) == 3
        assert "gehen" in translations
        assert translations["gehen"] == ["идти", "ходить"]
        assert translations["machen"] == ["делать", "изготавливать"]

    def test_load_translations_caching(self, verb_service_with_hints):
        """Test that translations are cached after first load"""
        translations1 = verb_service_with_hints.load_translations()
        translations2 = verb_service_with_hints.load_translations()

        # Should return the same object (cached)
        assert translations1 is translations2

    def test_load_translations_file_not_found(self, tmp_path):
        """Test error handling when translations file doesn't exist"""
        # Create only the verbs file, not translations
        data_dir = tmp_path / "data_no_trans"
        data_dir.mkdir()

        verbs_data = {
            "gehen": {
                "Präsens": "geht",
                "Präteritum": "ging",
                "Perfekt": "ist gegangen",
            }
        }
        verbs_path = data_dir / "verbs_forms.json"
        with open(verbs_path, "w", encoding="utf-8") as f:
            json.dump(verbs_data, f)

        service = VerbService(str(verbs_path))

        with pytest.raises(FileNotFoundError, match="Translations file not found"):
            service.load_translations()

    def test_load_examples(self, verb_service_with_hints):
        """Test loading examples from JSON file"""
        examples = verb_service_with_hints.load_examples()

        assert len(examples) == 3
        assert "gehen" in examples
        assert len(examples["gehen"]) == 3
        assert "Er geht zur Schule." in examples["gehen"]

    def test_load_examples_caching(self, verb_service_with_hints):
        """Test that examples are cached after first load"""
        examples1 = verb_service_with_hints.load_examples()
        examples2 = verb_service_with_hints.load_examples()

        # Should return the same object (cached)
        assert examples1 is examples2

    def test_load_examples_file_not_found(self, tmp_path):
        """Test error handling when examples file doesn't exist"""
        # Create only the verbs file, not examples
        data_dir = tmp_path / "data_no_examples"
        data_dir.mkdir()

        verbs_data = {
            "gehen": {
                "Präsens": "geht",
                "Präteritum": "ging",
                "Perfekt": "ist gegangen",
            }
        }
        verbs_path = data_dir / "verbs_forms.json"
        with open(verbs_path, "w", encoding="utf-8") as f:
            json.dump(verbs_data, f)

        service = VerbService(str(verbs_path))

        with pytest.raises(FileNotFoundError, match="Examples file not found"):
            service.load_examples()

    def test_get_verb_hints(self, verb_service_with_hints):
        """Test getting hints (translations + random example) for a verb"""
        hints = verb_service_with_hints.get_verb_hints("gehen")

        assert "translations" in hints
        assert "example" in hints
        assert hints["translations"] == ["идти", "ходить"]
        assert hints["example"] in [
            "Er geht zur Schule.",
            "Sie ging gestern ins Kino.",
            "Wir sind nach Hause gegangen.",
        ]

    def test_get_verb_hints_example_is_from_valid_set(self, verb_service_with_hints):
        """Test that example selection is from valid options"""
        valid_examples = [
            "Er macht seine Hausaufgaben.",
            "Sie machte einen Kuchen.",
            "Wir haben einen Ausflug gemacht.",
        ]

        # Call multiple times to check randomness
        for _ in range(10):
            hints = verb_service_with_hints.get_verb_hints("machen")
            assert hints["example"] in valid_examples

    def test_get_verb_hints_verb_not_in_translations(self, tmp_path):
        """Test error when verb doesn't exist in translations"""
        # Create files with mismatched verbs
        data_dir = tmp_path / "data_mismatch"
        data_dir.mkdir()
        translations_dir = data_dir / "translations"
        translations_dir.mkdir()

        verbs_data = {
            "gehen": {
                "Präsens": "geht",
                "Präteritum": "ging",
                "Perfekt": "ist gegangen",
            }
        }
        verbs_path = data_dir / "verbs_forms.json"
        with open(verbs_path, "w", encoding="utf-8") as f:
            json.dump(verbs_data, f)

        # Translations missing "gehen"
        translations_data = {"machen": ["делать"]}
        translations_path = translations_dir / "verbs_translation_ru.json"
        with open(translations_path, "w", encoding="utf-8") as f:
            json.dump(translations_data, f)

        examples_data = {"gehen": ["Er geht zur Schule."]}
        examples_path = data_dir / "verbs_examples.json"
        with open(examples_path, "w", encoding="utf-8") as f:
            json.dump(examples_data, f)

        service = VerbService(str(verbs_path))

        with pytest.raises(ValueError, match="not found in translations"):
            service.get_verb_hints("gehen")

    def test_get_verb_hints_verb_not_in_examples(self, tmp_path):
        """Test error when verb doesn't exist in examples"""
        # Create files with mismatched verbs
        data_dir = tmp_path / "data_mismatch2"
        data_dir.mkdir()
        translations_dir = data_dir / "translations"
        translations_dir.mkdir()

        verbs_data = {
            "gehen": {
                "Präsens": "geht",
                "Präteritum": "ging",
                "Perfekt": "ist gegangen",
            }
        }
        verbs_path = data_dir / "verbs_forms.json"
        with open(verbs_path, "w", encoding="utf-8") as f:
            json.dump(verbs_data, f)

        translations_data = {"gehen": ["идти"]}
        translations_path = translations_dir / "verbs_translation_ru.json"
        with open(translations_path, "w", encoding="utf-8") as f:
            json.dump(translations_data, f)

        # Examples missing "gehen"
        examples_data = {"machen": ["Er macht etwas."]}
        examples_path = data_dir / "verbs_examples.json"
        with open(examples_path, "w", encoding="utf-8") as f:
            json.dump(examples_data, f)

        service = VerbService(str(verbs_path))

        with pytest.raises(ValueError, match="not found in examples"):
            service.get_verb_hints("gehen")
