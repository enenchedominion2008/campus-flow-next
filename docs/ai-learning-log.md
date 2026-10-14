# CampusFlow AI Learning Log

## Engineer A — Mariam Mohammed (Cherry-tech14)
**Responsibilities (CampusFlow Next):** Centralized validation helpers, safe assignment/status mutations, follow-up note data operations, safe JSON load/save, ID continuity, and tests.

---

## Part 1 — Original CampusFlow (preserved)

### Log 1: Ticket Creation
**Problem:** Generate unique ticket IDs (T001, T002, etc.).
**AI Assistance:** AI explained loops, string slicing, and f-strings to generate sequential IDs.
**What I Learned:** How `f"T{highest_id + 1:03d}"` generates ticket IDs.
**Verification:** Tested ticket creation and unique IDs with unittest. Tests passed.

### Log 2: Input Validation and Priority Engine
**Problem:** Validate ticket information and calculate priority correctly.
**AI Assistance:** AI explained conditional statements, ValueError, and priority rules.
**What I Learned:** How to reject invalid inputs and calculate critical, high, medium, and low priorities.
**Verification:** Tested valid/invalid inputs and all four priority levels. Tests passed.

### Log 3: Automated Testing
**Problem:** Verify ticket creation, validation, and priority work correctly.
**AI Assistance:** AI explained unittest, assertEqual, assertRaises, and setUp.
**What I Learned:** How to write automated tests and check expected results.
**Verification:** `python3 -m unittest discover -s tests -v` — all ticket tests passed.

---

## Part 2 — CampusFlow Next Learning Cycles

### Log 4: Validate-before-mutate for ticket collections

**Concept gap:** My old `load_tickets` only checked that JSON was a list. It accepted
records missing keys, invalid categories, and duplicate ticket IDs. I did not understand
how to reject a whole collection *before* it reached the application without damaging
the caller's current data.

**Exact question asked to AI:**
"Explain how to validate a dictionary BEFORE mutating it, using a small book-library
example. Then show how to validate a whole list of dictionaries and reject the load
if any entry is invalid, without the caller losing their current in-memory list."

**Summary of AI guidance:**
- Separate *shape* validation (keys, types) from *business-rule* validation
  (allowed values, uniqueness).
- Return `(True, None)` or `(False, reason)` from validators so the caller collects
  the first failure without try/except everywhere.
- Build the candidate list first, validate it fully, and only then swap the caller's
  reference — never mutate in place while validating.

**Tiny unrelated experiment:**
Asked AI to explain `isinstance(True, int)` on a small book example. It returned
`True` because `bool` is a subclass of `int`. Confirmed in the Python REPL:
`isinstance(True, int)` → `True`, and `type(True) is int` → `False`.
Decision: reject booleans explicitly with `isinstance(n, bool) or not isinstance(n, int)`.

**Independent verification:**
Read Python docs on `bool` subclassing and `json` module behavior. Wrote
`tests/test_validation.py` covering `True`, `2.5`, `0`, `-1`, `"5"` as `affected_users`.
All rejected. Wrote `tests/test_storage.py::test_failed_load_does_not_touch_caller_data`
to prove a corrupt file leaves the caller's list unchanged.

**Final engineering decision:**
Adopted result-tuple validators and a pure-return `load_tickets` that cannot mutate
caller state. This satisfies Requirement E: "reject the load and keep current memory
unchanged." **Accepted AI's general pattern after testing; adjusted the boolean check
to be explicit rather than relying on `type(x) != int` alone, because a future
refactor might loosen the type.**

---

### Log 5: Note ID generation without consuming IDs on rejection

**Concept gap:** Requirement B says a rejected note must *not* consume a note ID.
I did not understand how to guarantee that when validation happens after the ID is
generated, and I was worried about ID reuse if notes were ever deleted.

**Exact question asked to AI:**
"Compare two designs for `next_note_id`: (a) store a counter on the ticket,
(b) compute from the max existing note_id each time. Which is safer for a JSON-only
project where users may edit the file by hand? I will test both — do not implement
my project."

**Summary of AI guidance:**
- A stored counter can desync from the notes list if someone edits JSON by hand.
- Computing from `max(existing note_ids)` is self-healing: it always produces the
  next safe number, even if the file was edited.
- Do not append the candidate note before validation; validate the *candidate dict*
  first and only then append. If validation fails, the candidate is discarded and
  the next call generates the same ID — which is exactly the required behavior.

**Tiny unrelated experiment:**
Asked AI to explain `lower` vs `casefold` on a small example
(`"WI-FI".lower()` vs `"WI-FI".casefold()`). Both returned `"wi-fi"` for ASCII.
casefold differs on German ß, which is irrelevant here. Decision: use `casefold`
in Engineer B's search, not in note IDs.

**Independent verification:**
Read Python docs on `str.casefold` and `format` mini-language (`:03d`).
Wrote `tests/test_notes.py::test_blank_author_rejected_without_consuming_id`,
which asserts that after a rejected note the next successful note is still `N001`.
Wrote `test_note_after_reopen_accepted` which asserts the next ID after reopen is
`N002` when `N001` already exists.

**Final engineering decision:**
Adopted design (b) — compute `next_note_id` from the max existing suffix — and
validate the candidate note *before* appending. **Changed AI's first suggestion
(store a counter) after testing showed it can desync from a hand-edited JSON file.
This is the team's documented case of a changed AI suggestion backed by evidence.**

---

## Summary

AI helped me understand Python concepts, improve my implementation, and write
automated tests. In CampusFlow Next, AI was most useful as a *design comparator* —
I asked it to explain trade-offs, then verified each claim with a test or the
Python docs. One AI suggestion (stored note counter) was changed after evidence
showed the max-suffix approach is safer for a JSON-only project.z