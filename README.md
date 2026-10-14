# CampusFlow — Campus IT Helpdesk Ticketing System

## Project Overview

CampusFlow is a Python-based command-line application designed to help campus IT support teams manage technical support requests.

The system allows users to create support tickets, assign priorities, track ticket progress, and organize unresolved issues.

### Problem Statement

Campus IT departments receive technical complaints involving network connections, computer hardware, software, and other IT services.

Without a structured system, these complaints can be difficult to track, prioritize, and resolve.

CampusFlow provides a simple ticket management solution that helps IT support teams:

- Record technical issues.
- Automatically calculate ticket priorities.
- Assign tickets to support staff.
- Track ticket resolution progress.
- Organize outstanding support requests.
- Generate ticket reports.
- Save and retrieve ticket information.

The project was developed collaboratively using Python, Git, GitHub, and automated testing.

---

##  Team Members and Contributions

CampusFlow was developed by two engineers.

### Engineer A — Mariam Mohammed (Cherry-tech14)

**Responsibilities:**
- Ticket creation.
- Input validation.
- Priority calculation engine.
- Automated testing for ticket creation and validation.

**Contributions:**
- Implemented ticket creation with unique ticket IDs.
- Validated ticket titles, categories, urgency levels, and affected users.
- Implemented automatic priority calculation.
- Developed automated tests using Python's `unittest` framework.
- Contributed to project integration and documentation.

### Engineer B — Enenche Dominion [enenchedominion2008]

**Responsibilities:**
- Ticket assignment and status management.
- Work queue  
- reporting
- JSON data persistence and related tests.

**Contributions:**
- Implemented ticket assignment and workflow management.
- Developed the priority-based work queue.
- Implemented ticket reporting.
- Contributed to data storage and project integration.


##  Technologies Used

- Python 
- JSON 
- GitHub 
- VS Code



##  Project Structure


campusflow/
│
├── campusflow/
│   ├── __init__.py
│   ├── tickets.py
│   ├── workflow.py
│   ├── queue.py
│   ├── reports.py
│   └── storage.py
│
├── tests/
│   ├── test_tickets.py
│   ├── test_workflow.py
│   ├── test_queue.py
│   ├── test_reports.py
│   └── test_storage.py
│
├── data/
│   └── tickets.json
│
├── docs/
│   ├── design-decisions.md
│   └── ai-learning-log.md
│
├── main.py
├── README.md
└── .gitignore



## Running CampusFlow

From the project root directory, run:

python3 main.py



## icket Priority Rules

CampusFlow automatically calculates priority using urgency and the number of affected users.

| Priority | Condition |
|----------|-----------|
| Critical | High urgency AND at least 10 affected users |
| High | High urgency OR at least 10 affected users |
| Medium | Medium urgency OR at least 3 affected users |
| Low | All remaining valid cases |

**Important:** The rules are evaluated from top to bottom.

### Examples

| Urgency | Affected Users | Priority |
|---------|----------------|----------|
| high | 15 | critical |
| high | 2 | high |
| low | 12 | high |
| medium | 5 | medium |
| low | 4 | medium |
| low | 1 | low |



## Automated Testing

CampusFlow uses Python's built-in `unittest` framework.

### Run All Tests

From the project root directory:

```bash
python3 -m unittest discover -s tests -v
```

### Run Individual Tests

**Ticket creation and validation:**

```bash
python3 -m unittest discover -s tests -p "test_tickets.py" -v
```

**JSON storage:**

```bash
python3 -m unittest discover -s tests -p "test_storage.py" -v
```

**Ticket workflow:**

```bash
python3 -m unittest discover -s tests -p "test_workflow.py" -v
```

**Work queue:**

```bash
python3 -m unittest discover -s tests -p "test_queue.py" -v
```

**Ticket reports:**

```bash
python3 -m unittest discover -s tests -p "test_reports.py" -v
```


##  Known Limitations

The following limitations should be considered:

1. **Command-line interface:** CampusFlow currently uses a terminal interface rather than a graphical interface or website.

2. **Local storage:** Tickets are stored in a local JSON file rather than a database.

3. **Single-user design:** The application does not currently provide user authentication or role-based access control.

4. **Integration pending:** Some features may not be available until both engineers' contributions are merged.

5. **Testing:** The complete integrated application has not yet been verified to pass all automated tests.

### Future Improvements

Potential improvements include:

- Building a web-based interface.
- Adding user authentication.
- Using SQLite or PostgreSQL for data storage.
- Implementing ticket search and filtering.
- Adding notifications for high-priority tickets.
- Expanding automated integration testing.


### Repository

https://github.com/Cherry-tech14/campusflow

### Collaboration Process

1. Each engineer works on a separate feature branch.
2. Changes are committed and pushed to GitHub.
3. Pull requests are created for review.
4. The other engineer reviews the implementation.
5. Requested changes are addressed.
6. Approved pull requests are merged into `main`.
7. The integrated project is tested before submission.

### Pull Requests
Engineer A : https://github.com/Cherry-tech14/campusflow/pull/13
Engineer B: https://github.com/Cherry-tech14/campusflow/pull/10
All pull requests can also be viewed here:


Engineer B: https://github.com/Cherry-tech14/campusflow/pull/10

### All pull requests can also be viewed here:

https://github.com/Cherry-tech14/campusflow/pulls



### campus flow next
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