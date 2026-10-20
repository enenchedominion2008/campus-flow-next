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


### Engineer B → Engineer A's module: notes

**Test names:**
- `test_bug_hunter_add_note_with_none_author_raises_value_error`
- `test_bug_hunter_next_note_id_skips_malformed_ids`

**Test location:** `tests/test_notes.py`
**Module attacked:** `campusflow/notes.py` (Engineer A)
**File author:** Engineer B

**Initial state:** Open ticket with an empty `notes` list (for the first test);
for the second test, a ticket with valid `N001` and a malformed note id `"garbage"`.

**Input 1:** `add_note("T001", None, "valid message here", [ticket])` — author is `None`, not a string.
**Expected 1:** `ValueError` raised; `ticket["notes"]` unchanged.
**Actual 1:** `ValueError` raised; notes unchanged — pass.

**Input 2:** `next_note_id(ticket)` where notes contain `N001` and a `"garbage"` entry.
**Expected 2:** `"N002"` (malformed entry skipped, doesn't crash).
**Actual 2:** `"N002"` — pass.

**Code change made:** None needed — Engineer A's `next_note_id` already guards each
`note_id` with `isinstance(nid, str) and nid.startswith("N") and nid[1:].isdigit()`,
and `add_note` delegates author validation to `validate_note_shape`, which checks
`isinstance(author, str) and author.strip()`.

**Invariant protected:**
1. A rejected note (invalid author) leaves the ticket's notes list unchanged — no
   partial mutation.
2. `next_note_id` is robust to malformed note IDs in the JSON file and cannot be
   crashed by hand-edited data.
