# CampusFlow — Campus IT Helpdesk Ticketing System

## Project Overview

CampusFlow is a Python command-line application for campus IT support teams
to manage technical support requests. It supports ticket creation, automatic
priority calculation, assignment, status transitions, follow-up notes,
multi-filter search, reports, and JSON persistence.

This is **CampusFlow Next** — a reliability upgrade of the original project,
adding stronger validation, structured follow-up notes, safe JSON loading,
search/filtering, expanded reports, and an interactive Engineering
Understanding Check.

## Technologies Used

- Python (standard library only)
- JSON
- unittest
- Git / GitHub
- VS Code

---

## Team Members and Contributions (CampusFlow Next)

### Engineer A — Mariam Mohammed [Cherry-tech14]
**Role:** Ticket Safety and Storage Engineer

**Responsibilities:**
- Centralized validation helpers
- Safe assignment and status mutations
- Follow-up note data operations
- Safe JSON load/save and ID continuity
- Tests for validation, notes, storage

**Contributions:**
- Added `campusflow/validation.py` (validate_ticket, validate_ticket_collection, validate_note_shape)
- Added `campusflow/notes.py` (add_note, next_note_id)
- Extended `create_ticket` with `notes` field
- Strengthened `load_tickets` to validate the full collection and reject malformed records and duplicate IDs without losing caller state
- Migrated legacy tickets missing `notes` on load
- Fixed `get_work_queue` to include OPEN tickets only
- Made `workflow.py` the single source of state transitions
- Added tests: test_validation.py, test_notes.py, storage collection tests

### Engineer B — Enenche Dominion [enenchedominion2008]
**Role:** Search, Reporting and CLI Engineer

**Responsibilities:**
- Search interface and combined filters
- Reports and analytics
- Note CLI menus (calling A's APIs)
- Engineering Understanding Check
- Tests for search, reports, CLI, and quiz scoring

**Contributions:**
- Added `campusflow/search.py` (casefold title search + AND filters)
- Extended `campusflow/reports.py` (totals, counts by status/priority/category, unresolved/resolved, resolution %)
- Added `campusflow/understanding_check.py` (6-question interactive check with scoring)
- Added CLI note menus (add/view) in `main.py`
- Added tests: test_search.py, test_reports.py, test_understanding.py

---

## Project Structure

```
campusflow/
├── campusflow/
│   ├── __init__.py
│   ├── tickets.py
│   ├── validation.py
│   ├── workflow.py
│   ├── notes.py
│   ├── search.py
│   ├── reports.py
│   ├── queue.py
│   ├── storage.py
│   └── understanding_check.py
├── tests/
│   ├── test_tickets.py
│   ├── test_validation.py
│   ├── test_workflow.py
│   ├── test_notes.py
│   ├── test_search.py
│   ├── test_queue.py
│   ├── test_reports.py
│   ├── test_storage.py
│   └── test_understanding.py
├── data/
│   └── tickets.json
├── docs/
│   ├── baseline-check.md
│   ├── design-decisions.md
│   └── ai-learning-log.md
├── main.py
├── README.md
└── .gitignore
```

## Running CampusFlow

```bash
python3 main.py
```

## Ticket Priority Rules

| Priority | Condition |
|----------|-----------|
| Critical | High urgency AND at least 10 affected users |
| High | High urgency OR at least 10 affected users |
| Medium | Medium urgency OR at least 3 affected users |
| Low | All remaining valid cases |

Rules are evaluated top to bottom.

### Examples

| Urgency | Affected Users | Priority |
|---------|----------------|----------|
| high | 15 | critical |
| high | 2 | high |
| low | 12 | high |
| medium | 5 | medium |
| low | 4 | medium |
| low | 1 | low |

## Ticket Status Rules

- `open → in_progress` — only if the ticket is assigned
- `in_progress → resolved` — allowed
- `resolved → open` — allowed (reopen)
- All other transitions rejected

## Follow-up Notes

- Every ticket has a `notes` list, initially empty
- Notes may be added only when status is `open` or `in_progress`
- Each note has `note_id` (N001, N002, ...), `author`, and `message`
- Author must be non-blank; message must be 5–300 characters after trimming
- A rejected note does **not** consume a note ID
- Notes are preserved through resolve and reopen

## Open Work Queue

The original Open Work Queue shows **only open tickets**, ordered by:
1. Priority: critical > high > medium > low
2. Then by numeric ticket ID (earlier first)

`in_progress` and `resolved` tickets do not appear in this queue.

## Automated Testing

Run all tests:

```bash
python3 -m unittest discover -s tests -v
```

Run a single file:

```bash
python3 -m unittest discover -s tests -p "test_validation.py" -v
python3 -m unittest discover -s tests -p "test_notes.py" -v
python3 -m unittest discover -s tests -p "test_storage.py" -v
python3 -m unittest discover -s tests -p "test_search.py" -v
python3 -m unittest discover -s tests -p "test_reports.py" -v
python3 -m unittest discover -s tests -p "test_understanding.py" -v
```

## Data Format

Tickets are stored in `data/tickets.json` as a JSON list. Each ticket has the shape:

```json
{
  "id": "T001",
  "title": "Wi-Fi down in Block A",
  "category": "Network",
  "urgency": "high",
  "affected_users": 12,
  "priority": "critical",
  "status": "open",
  "assigned_to": null,
  "notes": [
    {"note_id": "N001", "author": "Mentor A", "message": "Router rebooted"}
  ]
}
```

**Validation on load:** the full collection is validated before replacing in-memory
state. Malformed records, invalid values, and duplicate ticket/note IDs cause the
load to be rejected with `ValueError`; existing memory is unchanged.

**Migration:** legacy tickets that lack the `notes` field are automatically given
`"notes": []` on load. All other validation still applies.

## Documentation

- `docs/baseline-check.md` — pre-change test results and identified gaps
- `docs/ai-learning-log.md` — AI learning cycles (both engineers)
- `docs/design-decisions.md` — design rationale

## Known Limitations

1. Command-line interface only (no GUI or web front-end)
2. Local JSON file storage (no database)
3. Single-user design (no authentication or roles)
4. Search uses substring matching only (no fuzzy spelling)

## Future Improvements

- Web-based interface
- User authentication and roles
- SQLite or PostgreSQL storage
- Fuzzy search and saved filters
- Notifications for critical tickets

## Repository

https://github.com/enenchedominion2008/campus-flow-next

## Collaboration Process

1. Each engineer works on a separate feature branch
2. Changes are committed and pushed to GitHub
3. Pull requests are opened for review
4. The other engineer reviews the implementation
5. Requested changes are addressed
6. Approved PRs are merged into `main`
7. Integrated project is tested before submission
8. 
