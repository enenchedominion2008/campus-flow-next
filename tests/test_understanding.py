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


if __name__ == "__main__":
    unittest.main()