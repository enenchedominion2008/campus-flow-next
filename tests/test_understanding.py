import unittest

from campusflow.understanding_check import (
    QUESTIONS,
    score_answers,
    ask_question,
    run_quiz,
)


class TestUnderstandingCheck(unittest.TestCase):

    def test_question_bank_contains_six_questions(self):
        self.assertEqual(len(QUESTIONS), 6)

    def test_each_question_has_four_options(self):
        for question in QUESTIONS:
            self.assertEqual(
                set(question["options"].keys()),
                {"A", "B", "C", "D"},
            )

    def test_all_correct_answers_score_six(self):
        answers = ["B", "C", "B", "C", "C", "B"]

        self.assertEqual(score_answers(answers), 6)

    def test_three_correct_answers_score_three(self):
        answers = ["A", "C", "B", "D", "C", "A"]

        self.assertEqual(score_answers(answers), 3)

    def test_all_wrong_answers_score_zero(self):
        answers = ["A", "A", "A", "A", "A", "A"]

        self.assertEqual(score_answers(answers), 0)

    def test_lowercase_answers_are_accepted_for_scoring(self):
        answers = ["b", "c", "b", "c", "c", "b"]

        self.assertEqual(score_answers(answers), 6)

    def test_invalid_answer_triggers_retry(self):
        answers = iter(["X", "B"])
        output = []

        result = ask_question(
            QUESTIONS[0],
            input_fn=lambda prompt: next(answers),
            output_fn=output.append,
        )

        self.assertEqual(result, "B")

        self.assertTrue(
            any("Invalid choice" in message for message in output)
        )

    def test_quiz_returns_final_score(self):
        answers = iter([
            "B", "C", "B", "C", "C", "B",
            "The ticket must be assigned first.",
            "Zero tickets means zero percent resolved.",
        ])

        output = []

        result = run_quiz(
            input_fn=lambda prompt: next(answers),
            output_fn=output.append,
        )

        self.assertEqual(result, 6)

        self.assertTrue(
            any("FINAL SCORE: 6/6" in message for message in output)
        )

    def test_quiz_retries_invalid_answer_and_scores_valid_choice(self):
        answers = iter([
            "X",  # Invalid response to Question 1
            "B",  # Valid response to Question 1
            "C",
            "B",
            "C",
            "C",
            "B",
            "Explanation for Question 1",
            "Explanation for Question 2",
        ])

        output = []

        result = run_quiz(
            input_fn=lambda prompt: next(answers),
            output_fn=output.append,
        )

        self.assertEqual(result, 6)

        self.assertTrue(
            any("Invalid choice" in message for message in output)
        )

    def test_quiz_displays_both_explanations(self):
        answers = iter([
            "B", "C", "B", "C", "C", "B",
            "Assignment is required before starting work.",
            "No tickets means the result is zero percent.",
        ])

        output = []

        run_quiz(
            input_fn=lambda prompt: next(answers),
            output_fn=output.append,
        )

        displayed_output = "\n".join(output)

        self.assertIn(
            "Assignment is required before starting work.",
            displayed_output,
        )

        self.assertIn(
            "No tickets means the result is zero percent.",
            displayed_output,
        )

class TestNotesBugHunter(unittest.TestCase):
    """Bug-hunter test — Engineer B against Engineer A's module (campusflow/notes.py)."""

    def test_bug_hunter_add_note_with_none_author_raises_value_error(self):
        """Bug-hunter (Engineer B) — add_note with author=None must raise
        ValueError, not crash with AttributeError on None.strip().

        Initial state: open ticket with empty notes list.
        Input: add_note("T001", None, "valid message here", [ticket]).
        Expected: ValueError raised; ticket["notes"] still empty.
        Actual: ValueError raised; notes unchanged — pass.
        """
        from campusflow.notes import add_note

        ticket = {
            "id": "T001",
            "title": "wifi down",
            "category": "Network",
            "urgency": "high",
            "affected_users": 12,
            "priority": "critical",
            "status": "open",
            "assigned_to": None,
            "notes": [],
        }

        with self.assertRaises(ValueError):
            add_note("T001", None, "valid message here", [ticket])

        # invariant: rejected note does not mutate the ticket
        self.assertEqual(ticket["notes"], [])

    def test_bug_hunter_next_note_id_skips_malformed_ids(self):
        """Bug-hunter (Engineer B) — next_note_id must not crash on a
        malformed note_id (e.g. "garbage") and must still return N002
        when N001 is present.

        Initial state: ticket has notes N001 and one malformed entry.
        Input: next_note_id(ticket).
        Expected: "N002".
        Actual: "N002" — pass.
        """
        from campusflow.notes import next_note_id

        ticket = {
            "id": "T001",
            "title": "wifi down",
            "category": "Network",
            "urgency": "high",
            "affected_users": 12,
            "priority": "critical",
            "status": "open",
            "assigned_to": None,
            "notes": [
                {"note_id": "N001", "author": "A", "message": "first note here"},
                {"note_id": "garbage", "author": "B", "message": "bad note id"},
            ],
        }

        self.assertEqual(next_note_id(ticket), "N002")
=======
    # ---------------------------------------------------------------
    # Bug-hunter tests (§06)
    # ---------------------------------------------------------------

    def test_bug_hunter_invalid_choice_never_scores(self):
        """Bug-hunter (Engineer A) — invalid answers must NEVER score as correct.

        Initial state: question bank loaded; score_answers available.
        Input: six "Z" answers (not A/B/C/D).
        Expected: score = 0.
        """
        answers = ["Z", "Z", "Z", "Z", "Z", "Z"]
        self.assertEqual(score_answers(answers), 0)

        # sanity: full correct answers still score 6
        correct = [q["answer"] for q in QUESTIONS]
        self.assertEqual(score_answers(correct), 6)

    def test_bug_hunter_score_does_not_exceed_question_count(self):
        """Bug-hunter (Engineer A) — score must never exceed the number of questions.

        Initial state: question bank loaded.
        Input: correct answer list plus 3 extra entries ("B","C","B").
        Expected: score <= len(QUESTIONS).
        """
        correct = [q["answer"] for q in QUESTIONS]
        extra = correct + ["B", "C", "B"]
        self.assertLessEqual(score_answers(extra), len(QUESTIONS))


if __name__ == "__main__":
    unittest.main()