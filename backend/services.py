"""Business logic for verb learning service"""
import json
import random
from pathlib import Path
from typing import Dict, List, Optional


class VerbService:
    """Service for managing German verb forms and quiz logic"""

    def __init__(self, data_path: str):
        """
        Initialize the verb service

        Args:
            data_path: Path to the JSON file containing verb data
        """
        self.data_path = Path(data_path)
        self._verbs: Optional[Dict[str, Dict[str, str]]] = None

    def load_verbs(self) -> Dict[str, Dict[str, str]]:
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

            with open(self.data_path, 'r', encoding='utf-8') as f:
                self._verbs = json.load(f)

        return self._verbs

    def get_random_verbs(self, count: int = 10) -> List[str]:
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
        user_perfekt: str
    ) -> Dict[str, bool]:
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
            "perfekt": user_perfekt.strip() == correct_forms["Perfekt"]
        }

    def grade_session(
        self,
        answers: List[Dict[str, str]]
    ) -> Dict:
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
                infinitive,
                answer["praesens"],
                answer["praeteritum"],
                answer["perfekt"]
            )

            # Count correct answers
            forms_correct = sum(correctness.values())
            total_correct += forms_correct

            # Get correct forms for comparison
            correct_forms = verbs[infinitive]

            results.append({
                "infinitive": infinitive,
                "correct": correctness,
                "user_answers": {
                    "praesens": answer["praesens"],
                    "praeteritum": answer["praeteritum"],
                    "perfekt": answer["perfekt"]
                },
                "correct_answers": {
                    "praesens": correct_forms["Präsens"],
                    "praeteritum": correct_forms["Präteritum"],
                    "perfekt": correct_forms["Perfekt"]
                },
                "all_correct": all(correctness.values())
            })

        score_percentage = (total_correct / total_forms * 100) if total_forms > 0 else 0

        return {
            "total_verbs": len(answers),
            "total_forms": total_forms,
            "correct_count": total_correct,
            "score_percentage": round(score_percentage, 1),
            "results": results
        }
