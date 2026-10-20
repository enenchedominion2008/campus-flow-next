# CampusFlow Design Decisions

## Engineer A: Ticket Creation

### 1. Ticket Creation
I used a dictionary to store ticket details and a list to store multiple tickets.

### 2. Input Validation
I used if statements and ValueError to prevent invalid inputs, such as empty titles, wrong categories, and negative numbers.

### 3. Priority Calculation
I used if, elif, and else to calculate ticket priority based on urgency and the number of affected users.

### 4. Ticket ID
I used a for loop to generate unique ticket IDs like T001, T002, and T003.

### 5. Testing
I used Python's unittest module to test ticket creation, priority calculation, and input validation.

### 6. Code Simplicity
I chose simple Python functions and loops because they are easier to understand, maintain, and explain.

# Engineer B design notes

- Ticket collection: list of dictionaries, passed into each business-logic function.
- Invalid assignment or lifecycle action: raise `TicketWorkflowError` (a `ValueError` subclass).
- Successful functions return the updated ticket; the queue returns a new sorted list.
- Reports return a dictionary so the CLI and tests can use the data independently of display formatting.
- Persistence is intentionally not implemented in these feature modules; it remains a shared integration task.
## Bug-hunter tests (§06)

### Engineer A → Engineer B's module: understanding_check

**Test name:** `test_invalid_choice_does_not_score_as_correct`
**Test location:** `tests/test_understanding.py`
**Module attacked:** `campusflow/understanding_check.py` (Engineer B)

**Initial state:** Question bank loaded; `score_answers` available.
**Input:** `["Z", "Z", "Z", "Z", "Z", "Z"]` — six invalid answers.
**Expected result:** score = 0 (invalid choices never match A/B/C/D).
**Actual result:** <fill in after running — 0 or reproduce failure>
**Code change made:** <none | describe fix if any>

**Invariant protected:** invalid quiz input cannot be scored as correct.

### Engineer B → Engineer A's module: <fill in>

**Test name:** <B fills in>
**Test location:** <B fills in>
**Module attacked:** <e.g. campusflow/notes.py>
**Initial state:** <B fills in>
**Input:** <B fills in>
**Expected result:** <B fills in>
**Actual result:** <B fills in>
**Code change made:** <B fills in>