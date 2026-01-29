"""Business logic for verb learning service"""

import json
import random
from pathlib import Path


class VerbService:
    """Service for managing German verb forms and quiz logic"""

    def __init__(self, data_path: str):
        """
        Initialize the verb service

        Args:
            data_path: Path to the JSON file containing verb data
        """
        self.data_path = Path(data_path)
        self._verbs: dict[str, dict[str, str]] | None = None
        self._translations: dict[str, list[str]] | None = None
        self._examples: dict[str, list[str]] | None = None

    def load_verbs(self) -> dict[str, dict[str, str]]:
        """
        Load verbs from JSON file (cached in memory)

        Returns:
            Dictionary mapping infinitive verbs to their forms

        Raises:
            FileNotFoundError: If the data file doesn't exist
            json.JSONDecodeError: If the file contains invalid JSON
        """
        if self._verbs is None:
            if not self.data_path.exists():
                raise FileNotFoundError(f"Verb data file not found: {self.data_path}")

            with open(self.data_path, encoding="utf-8") as f:
                self._verbs = json.load(f)

        return self._verbs

    def load_translations(self) -> dict[str, list[str]]:
        """
        Load Russian translations from JSON file (cached in memory)

        Returns:
            Dictionary mapping infinitive verbs to their translations

        Raises:
            FileNotFoundError: If the translations file doesn't exist
            json.JSONDecodeError: If the file contains invalid JSON
        """
        if self._translations is None:
            # Translations are in data/translations/verbs_translation_ru.json
            translations_path = (
                self.data_path.parent / "translations" / "verbs_translation_ru.json"
            )
            if not translations_path.exists():
                raise FileNotFoundError(
                    f"Translations file not found: {translations_path}"
                )

            with open(translations_path, encoding="utf-8") as f:
                self._translations = json.load(f)

        return self._translations

    def load_examples(self) -> dict[str, list[str]]:
        """
        Load example sentences from JSON file (cached in memory)

        Returns:
            Dictionary mapping infinitive verbs to their example sentences

        Raises:
            FileNotFoundError: If the examples file doesn't exist
            json.JSONDecodeError: If the file contains invalid JSON
        """
        if self._examples is None:
            # Examples are in data/verbs_examples.json
            examples_path = self.data_path.parent / "verbs_examples.json"
            if not examples_path.exists():
                raise FileNotFoundError(f"Examples file not found: {examples_path}")

            with open(examples_path, encoding="utf-8") as f:
                self._examples = json.load(f)

        return self._examples

    def get_verb_hints(self, infinitive: str) -> dict:
        """
        Get translations and one random example for a verb

        Args:
            infinitive: The verb in infinitive form

        Returns:
            Dictionary containing:
            - translations: list[str] - Russian translations
            - example: str - One random example sentence

        Raises:
            ValueError: If the verb is not found in translations or examples
        """
        translations = self.load_translations()
        examples = self.load_examples()

        if infinitive not in translations:
            raise ValueError(f"Verb '{infinitive}' not found in translations")

        if infinitive not in examples:
            raise ValueError(f"Verb '{infinitive}' not found in examples")

        return {
            "translations": translations[infinitive],
            "example": random.choice(examples[infinitive]),
        }

    def get_random_verbs(self, count: int = 10) -> list[str]:
        """
        Get a random selection of verb infinitives

        Args:
            count: Number of verbs to select (default: 10)

        Returns:
            List of infinitive verb forms

        Raises:
            ValueError: If requesting more verbs than available
        """
        verbs = self.load_verbs()
        available_verbs = list(verbs.keys())

        if len(available_verbs) < count:
            raise ValueError(
                f"Not enough verbs in database. Requested {count}, "
                f"but only {len(available_verbs)} available"
            )

        return random.sample(available_verbs, count)

    def check_answer(
        self,
        infinitive: str,
        user_praesens: str,
        user_praeteritum: str,
        user_perfekt: str,
    ) -> dict[str, bool]:
        """
        Check if user's answers match the correct forms

        Args:
            infinitive: The verb in infinitive form
            user_praesens: User's answer for Präsens (3rd person)
            user_praeteritum: User's answer for Präteritum (3rd person)
            user_perfekt: User's answer for Perfekt

        Returns:
            Dictionary with boolean values for each form:
            {"praesens": bool, "praeteritum": bool, "perfekt": bool}

        Raises:
            ValueError: If the verb is not found in the database
        """
        verbs = self.load_verbs()

        if infinitive not in verbs:
            raise ValueError(f"Verb '{infinitive}' not found in database")

        correct_forms = verbs[infinitive]

        return {
            "praesens": user_praesens.strip() == correct_forms["Präsens"],
            "praeteritum": user_praeteritum.strip() == correct_forms["Präteritum"],
            "perfekt": user_perfekt.strip() == correct_forms["Perfekt"],
        }

    def grade_session(self, answers: list[dict[str, str]]) -> dict:
        """
        Grade all answers in a session

        Args:
            answers: List of answer dictionaries, each containing:
                - infinitive: str
                - praesens: str
                - praeteritum: str
                - perfekt: str

        Returns:
            Dictionary containing:
            - total_verbs: int
            - total_forms: int (verbs × 3)
            - correct_count: int
            - score_percentage: float
            - results: List of detailed results per verb
        """
        if not answers:
            raise ValueError("No answers provided")

        verbs = self.load_verbs()
        results = []
        total_correct = 0
        total_forms = len(answers) * 3  # Each verb has 3 forms

        for answer in answers:
            infinitive = answer["infinitive"]

            if infinitive not in verbs:
                raise ValueError(f"Verb '{infinitive}' not found in database")

            # Check each form
            correctness = self.check_answer(
                infinitive, answer["praesens"], answer["praeteritum"], answer["perfekt"]
            )

            # Count correct answers
            forms_correct = sum(correctness.values())
            total_correct += forms_correct

            # Get correct forms for comparison
            correct_forms = verbs[infinitive]

            results.append(
                {
                    "infinitive": infinitive,
                    "correct": correctness,
                    "user_answers": {
                        "praesens": answer["praesens"],
                        "praeteritum": answer["praeteritum"],
                        "perfekt": answer["perfekt"],
                    },
                    "correct_answers": {
                        "praesens": correct_forms["Präsens"],
                        "praeteritum": correct_forms["Präteritum"],
                        "perfekt": correct_forms["Perfekt"],
                    },
                    "all_correct": all(correctness.values()),
                }
            )

        score_percentage = (total_correct / total_forms * 100) if total_forms > 0 else 0

        return {
            "total_verbs": len(answers),
            "total_forms": total_forms,
            "correct_count": total_correct,
            "score_percentage": round(score_percentage, 1),
            "results": results,
        }
