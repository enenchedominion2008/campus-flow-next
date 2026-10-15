QUESTIONS = [
    {
        "question": (
            "Ticket T001 is open and unassigned. "
            "A user tries to move it to in_progress. What should happen?"
        ),
        "options": {
            "A": "Accept the change",
            "B": "Reject and preserve all data",
            "C": "Resolve it automatically",
            "D": "Remove the ticket",
        },
        "answer": "B",
    },
    {
        "question": (
            "The application has zero tickets. "
            "What should the resolution percentage display?"
        ),
        "options": {
            "A": "Crash",
            "B": "100%",
            "C": "0%",
            "D": "Divide by one without explanation",
        },
        "answer": "C",
    },
    {
        "question": (
            "A user searches for title='wifi', category='Network', "
            "and status='open'. Which tickets should match?"
        ),
        "options": {
            "A": "Tickets matching any one filter",
            "B": "Tickets matching all supplied filters",
            "C": "All Network tickets",
            "D": "All open tickets",
        },
        "answer": "B",
    },
    {
        "question": (
            "A user tries to add a note to a resolved ticket. "
            "What should happen?"
        ),
        "options": {
            "A": "Append the note anyway",
            "B": "Delete the ticket's old notes",
            "C": "Reject the action until the ticket is reopened",
            "D": "Change the ticket's status silently",
        },
        "answer": "C",
    },
    {
        "question": (
            "The JSON file contains two tickets with the same ID. "
            "What should loading the file do?"
        ),
        "options": {
            "A": "Keep both tickets",
            "B": "Load the duplicate records",
            "C": "Reject the load without changing current memory",
            "D": "Rename the IDs silently",
        },
        "answer": "C",
    },
    {
        "question": (
            "A pull request changes validation but has no negative-case "
            "tests. What is the best review action?"
        ),
        "options": {
            "A": "Approve because the code runs",
            "B": "Request focused tests and an explanation",
            "C": "Merge immediately",
            "D": "Ask AI to approve it",
        },
        "answer": "B",
    },
]


def score_answers(answers, questions=None):

    if questions is None:
        questions = QUESTIONS

    score = 0

    for question, answer in zip(questions, answers):
        if answer.strip().upper() == question["answer"]:
            score += 1

    return score


def ask_question(question, input_fn, output_fn):

    output_fn("\n" + question["question"])

    for letter, option in question["options"].items():
        output_fn(f"{letter}. {option}")

    while True:
        answer = input_fn("Your answer (A/B/C/D): ").strip().upper()

        if answer in question["options"]:
            return answer

        output_fn("Invalid choice. Please enter A, B, C or D.")


def run_quiz(input_fn=None, output_fn=None):

    if input_fn is None:
        input_fn = input

    if output_fn is None:
        output_fn = print

    output_fn("\nENGINEERING UNDERSTANDING CHECK")
    output_fn("=" * 40)
    output_fn("Answer all six questions.")
    output_fn("Each correct answer earns one point.")

    answers = []

    for number, question in enumerate(QUESTIONS, start=1):
        output_fn(f"\nQuestion {number} of {len(QUESTIONS)}")

        answer = ask_question(
            question,
            input_fn,
            output_fn,
        )

        answers.append(answer)

    score = score_answers(answers)

    output_fn("\n" + "=" * 40)
    output_fn(f"FINAL SCORE: {score}/{len(QUESTIONS)}")
    output_fn("=" * 40)

    output_fn("\nEXPLAIN YOUR REASONING")
    output_fn("Explain why your answers to Questions 1 and 2 are correct.")

    explanation_1 = input_fn(
        "Explanation for Question 1: "
    ).strip()

    explanation_2 = input_fn(
        "Explanation for Question 2: "
    ).strip()

    output_fn("\nYOUR EXPLANATIONS")
    output_fn(f"Question 1: {explanation_1 or '(No explanation provided)'}")
    output_fn(f"Question 2: {explanation_2 or '(No explanation provided)'}")

    output_fn(
        "\nDiscuss your explanations with your mentor. "
        "They are not automatically graded."
    )

    return score