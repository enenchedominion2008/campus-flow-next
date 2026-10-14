"""Centralized validation helpers (Engineer A)."""

VALID_CATEGORIES = {"Network", "Hardware", "Software", "Other"}
VALID_URGENCIES  = {"low", "medium", "high"}
VALID_STATUSES   = {"open", "in_progress", "resolved"}
VALID_PRIORITIES = {"low", "medium", "high", "critical"}
REQUIRED_TICKET_KEYS = {
    "id", "title", "category", "urgency", "affected_users",
    "priority", "status", "assigned_to", "notes",
}


def validate_note_shape(note):
    if not isinstance(note, dict):
        return False, "note is not a dictionary"
    if set(note) != {"note_id", "author", "message"}:
        return False, f"note has wrong keys: {sorted(note)}"
    nid = note["note_id"]
    if not (isinstance(nid, str) and nid.startswith("N") and nid[1:].isdigit()):
        return False, f"invalid note_id: {nid!r}"
    if not (isinstance(note["author"], str) and note["author"].strip()):
        return False, "note author must be non-blank"
    msg = note["message"]
    if not (isinstance(msg, str) and 5 <= len(msg.strip()) <= 300):
        return False, "note message must be 5-300 chars"
    return True, None


def validate_ticket(ticket):
    if not isinstance(ticket, dict):
        return False, "ticket is not a dictionary"
    missing = REQUIRED_TICKET_KEYS - ticket.keys()
    if missing:
        return False, f"missing keys: {sorted(missing)}"
    tid = ticket["id"]
    if not (isinstance(tid, str) and tid.startswith("T") and tid[1:].isdigit()):
        return False, f"invalid ticket id: {tid!r}"
    if not (isinstance(ticket["title"], str) and ticket["title"].strip()):
        return False, "title must be non-blank"
    if ticket["category"] not in VALID_CATEGORIES:
        return False, f"invalid category: {ticket['category']!r}"
    if ticket["urgency"] not in VALID_URGENCIES:
        return False, f"invalid urgency: {ticket['urgency']!r}"
    n = ticket["affected_users"]
    if isinstance(n, bool) or not isinstance(n, int) or n <= 0:
        return False, f"invalid affected_users: {n!r}"
    if ticket["priority"] not in VALID_PRIORITIES:
        return False, f"invalid priority: {ticket['priority']!r}"
    if ticket["status"] not in VALID_STATUSES:
        return False, f"invalid status: {ticket['status']!r}"
    a = ticket["assigned_to"]
    if a is not None and (not isinstance(a, str) or not a.strip()):
        return False, f"invalid assigned_to: {a!r}"
    if not isinstance(ticket["notes"], list):
        return False, "notes must be a list"
    seen = set()
    for note in ticket["notes"]:
        ok, reason = validate_note_shape(note)
        if not ok:
            return False, reason
        if note["note_id"] in seen:
            return False, f"duplicate note_id {note['note_id']}"
        seen.add(note["note_id"])
    return True, None


def validate_ticket_collection(tickets):
    if not isinstance(tickets, list):
        return False, "top-level JSON must be a list"
    seen = set()
    for i, t in enumerate(tickets):
        ok, reason = validate_ticket(t)
        if not ok:
            return False, f"ticket {i}: {reason}"
        if t["id"] in seen:
            return False, f"duplicate ticket id: {t['id']}"
        seen.add(t["id"])
    return True, None