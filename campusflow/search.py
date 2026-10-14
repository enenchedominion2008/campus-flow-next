def search_tickets(
    tickets,
    search_term="",
    category=None,
    status=None,
    priority=None
):
    results = []

    # Normalize the search term
    normalized_search = search_term.strip().casefold()

    # Loop through tickets
    for ticket in tickets:
        title = ticket["title"]

        # Filter by title
        if normalized_search and normalized_search not in title.casefold():
            continue

        # Filter by category
        if category is not None:
            if ticket["category"].casefold() != category.casefold():
                continue

        # Filter by status
        if status is not None:
            if ticket["status"].casefold() != status.casefold():
                continue

        # Filter by priority
        if priority is not None:
            if ticket["priority"].casefold() != priority.casefold():
                continue

        # Include tickets that pass every supplied filter
        results.append(ticket)

    return results