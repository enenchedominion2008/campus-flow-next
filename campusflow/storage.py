import json
from pathlib import Path


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

    return tickets


def find_ticket(tickets, ticket_id):
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket

    raise ValueError("Ticket not found")


def assign_ticket(tickets, ticket_id, staff_name):
    ticket = find_ticket(tickets, ticket_id)

    if ticket["status"] == "resolved":
        raise ValueError("Cannot assign a resolved ticket")

    if not isinstance(staff_name, str) or staff_name.strip() == "":
        raise ValueError("Staff name cannot be empty")

    ticket["assigned_to"] = staff_name.strip()

    return ticket


def update_status(tickets, ticket_id, new_status):
    ticket = find_ticket(tickets, ticket_id)

    if not isinstance(new_status, str):
        raise ValueError("Invalid status")

    new_status = new_status.strip().lower()

    valid_statuses = ["open", "in_progress", "resolved"]

    if new_status not in valid_statuses:
        raise ValueError("Invalid status")

    current_status = ticket["status"]

    if current_status == "resolved":
        if new_status != "open":
            raise ValueError("Resolved tickets must be reopened first")

    elif current_status == "open":
        if new_status != "in_progress":
            raise ValueError(
                "Open tickets can only move to in_progress"
            )

        if ticket.get("assigned_to") is None:
            raise ValueError("Assign the ticket before starting work")

    elif current_status == "in_progress":
        if new_status != "resolved":
            raise ValueError(
                "In-progress tickets can only move to resolved"
            )

    else:
        raise ValueError("Invalid current ticket status")

    ticket["status"] = new_status

    return ticket

