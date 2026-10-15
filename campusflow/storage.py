import json
from pathlib import Path
from campusflow.validation import validate_ticket_collection

FILE_PATH = "data/tickets.json"


def save_tickets(tickets, path=FILE_PATH):
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4)


def load_tickets(path=FILE_PATH):
    file_path = Path(path)

    if not file_path.exists():
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            tickets = json.load(file)
    except json.JSONDecodeError:
        raise ValueError("Ticket data file contains invalid JSON")

    if not isinstance(tickets, list):
        raise ValueError("Ticket data must be a list")

    
    for t in tickets:
        if isinstance(t, dict) and "notes" not in t:
            t["notes"] = []

    ok, reason = validate_ticket_collection(tickets)
    if not ok:
        raise ValueError(f"Invalid ticket data: {reason}")

    return tickets
