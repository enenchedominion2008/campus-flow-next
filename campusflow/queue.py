def get_work_queue(tickets):

    priority_order = {
        "critical": 0,
        "high": 1,
        "medium": 2,
        "low": 3
    }

    unresolved_tickets = []

    for ticket in tickets:
        if ticket["status"] != "resolved":
            unresolved_tickets.append(ticket)

    sorted_tickets = sorted(
        unresolved_tickets,
        key=lambda ticket: (
            priority_order[ticket["priority"]],
            int(ticket["id"][1:])
        )
    )

    return sorted_tickets
