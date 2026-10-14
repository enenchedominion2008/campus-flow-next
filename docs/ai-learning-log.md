# CampusFlow AI Learning Log

## Engineer A — Mariam Mohammed (Cherry-tech14)
**Responsibilities (CampusFlow Next):** Validation helpers, safe status/assignment mutations, note data layer, safe JSON load/save, ID continuity, tests.

---

## Part 1 — Original CampusFlow

### Log 1: Ticket Creation
**Problem:** Generate unique ticket IDs.
**AI Assistance:** Explained loops, slicing, f-strings for sequential IDs.
**Learned:** How `f"T{highest_id + 1:03d}"` works.
**Verification:** unittest for creation + unique IDs — passed.

### Log 2: Input Validation & Priority Engine
**Problem:** Validate ticket fields and compute priority correctly.
**AI Assistance:** Explained conditionals, ValueError, priority rules.
**Learned:** Rejecting invalid input; four priority levels.
**Verification:** Tests for valid/invalid inputs and all priorities — passed.

### Log 3: Automated Testing
**Problem:** Verify creation, validation, priority.
**AI Assistance:** Explained unittest, assertEqual, assertRaises, setUp.
**Learned:** Writing tests with expected results.
**Verification:** Full test suite passed.

---

## Part 2 — CampusFlow Next

### Log 4: Validate-before-mutate for collections
**Concept gap:** Old `load_tickets` accepted records missing keys, invalid values, and duplicate IDs. Didn't know how to reject a whole collection without damaging caller state.

**Question asked:** "Explain how to validate a dictionary BEFORE mutating it (book-library example). Then show how to validate a list of dicts and reject the load if any entry is invalid, without losing the caller's in-memory list."

**AI guidance:** Separate shape validation from business-rule validation. Return `(True, None)` / `(False, reason)`. Build candidate list, validate fully, only then swap the caller's reference.

**Mini experiment:** `isinstance(True, int)` → `True` (bool subclasses int). `type(True) is int` → `False`. Decision: reject bools explicitly with `isinstance(n, bool) or not isinstance(n, int)`.

**Verification:** Wrote `test_validation.py` covering `True`, `2.5`, `0`, `-1`, `"5"` as `affected_users` (all rejected). Wrote `test_failed_load_does_not_touch_caller_data` proving corrupt file leaves caller list unchanged.

**Decision:** Adopted result-tuple validators + pure-return `load_tickets`. Adjusted AI's bool check to be explicit rather than relying on `type(x) != int`.

---

### Log 5: Note ID generation without consuming IDs on rejection
**Concept gap:** Requirement B says a rejected note must not consume an ID. Worried about ID reuse if notes were deleted.

**Question asked:** "Compare (a) store a counter on the ticket vs (b) compute from max existing note_id. Which is safer for JSON-only projects where users may hand-edit files? I'll test both — don't implement my project."

**AI guidance:** Stored counters can desync from hand-edited files. Max-suffix is self-healing. Validate the candidate dict before appending — if invalid, discard and reuse the same ID next call.

**Mini experiment:** `"WI-FI".lower()` vs `"WI-FI".casefold()` — same for ASCII; casefold differs on ß (irrelevant here). Decision: use casefold in Engineer B's search, not in note IDs.

**Verification:** Wrote `test_blank_author_rejected_without_consuming_id` (next successful note is still `N001`) and `test_note_after_reopen_accepted` (next ID after reopen is `N002` when `N001` exists).

**Decision:** Adopted design (b) — compute from max suffix, validate candidate before appending. **Changed AI's first suggestion (counter) after testing showed it can desync from hand-edited JSON. Team's documented case of a rejected AI suggestion backed by evidence.**

---

## Summary
AI was most useful as a *design comparator* — asked for trade-offs, verified each claim with tests or Python docs. One AI suggestion (stored note counter) was changed after evidence showed max-suffix is safer for a JSON-only project.