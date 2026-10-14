categories = ["Network", "Hardware", "Software", "Other"]
urgencies = ["low", "medium", "high"]

def calculate_priority(urgency, affected_users):

    if not isinstance(urgency, str):
        raise ValueError("Invalid urgency")

    urgency = urgency.strip().lower()

    if urgency not in urgencies:
        raise ValueError("Invalid urgency")

    if type(affected_users) != int or affected_users <= 0:
        raise ValueError("Affected users must be a positive integer")

    if urgency == "high" and affected_users >= 10:
        return "critical"

    elif urgency == "high" or affected_users >= 10:
        return "high"

    elif urgency == "medium" or affected_users >= 3:
        return "medium"

    else:
        return "low"


def create_ticket(tickets, title, category, urgency, affected_users):

    
    if not isinstance(title, str) or title.strip() == "":
        raise ValueError("Title cannot be empty")

    
    if not isinstance(category, str):
        raise ValueError("Invalid category")

    category = category.strip().capitalize()

    if category not in categories:
        raise ValueError("Invalid category")

    if not isinstance(urgency, str):
        raise ValueError("Invalid urgency")

    urgency = urgency.strip().lower()

    if urgency not in urgencies:
        raise ValueError("Invalid urgency")

    
    if type(affected_users) != int or affected_users <= 0:
        raise ValueError("Affected users must be a positive integer")

    
    priority = calculate_priority(urgency, affected_users)

    
    highest_id = 0

    for ticket in tickets:
        number = int(ticket["id"][1:])

        if number > highest_id:
            highest_id = number

    
    new_id = f"T{highest_id + 1:03d}"

    
    new_ticket = {
        "id": new_id,
        "title": title.strip(),
        "category": category,
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": priority,
        "status": "open",
        "assigned_to": None
    }

    
    tickets.append(new_ticket)

    return new_ticket