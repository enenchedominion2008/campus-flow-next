"""Follow-up note operations (Engineer A)."""

from campusflow.validation import validate_note_shape


def next_note_id(ticket):
    """Return next note ID like N001, N002, based on max existing."""
    max_n = 0
    for note in ticket["notes"]:
        nid = note["note_id"]
        if isinstance(nid, str) and nid.startswith("N") and nid[1:].isdigit():
            max_n = max(max_n, int(nid[1:]))
    return f"N{max_n + 1:03d}"


def add_note(ticket_id, author, message, tickets):
    """
    Add a follow-up note. Validates before mutating.
    Raises ValueError on any failure; rejected note does not consume an ID.
    """
    target = None
    for t in tickets:
        if t["id"] == ticket_id:
            target = t
            break
    if target is None:
        raise ValueError(f"ticket {ticket_id} not found")

    if target["status"] not in ("open", "in_progress"):
        raise ValueError(
            f"cannot add note to {target['status']} ticket; reopen first"
        )

    candidate = {
        "note_id": next_note_id(target),
        "author": author.strip() if isinstance(author, str) else author,
        "message": message.strip() if isinstance(message, str) else message,
    }

    ok, reason = validate_note_shape(candidate)
    if not ok:
        raise ValueError(reason)

    target["notes"].append(candidate)
    return candidate