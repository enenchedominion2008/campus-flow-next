from campusflow.tickets import create_ticket
from campusflow.storage import save_tickets, load_tickets
from campusflow.workflow import assign_ticket, update_status
from campusflow.queue import get_work_queue
from campusflow.reports import generate_report
from campusflow.search import search_tickets


def main():

    try:
        tickets = load_tickets()

    except (ValueError, OSError) as error:
        print("Error loading tickets:", error)
        print("Please fix the data file before starting CampusFlow.")
        return

    while True:
        print("\n== CAMPUSFLOW HELPDESK ==")
        print("1. Create Ticket")
        print("2. View Tickets")
        print("3. Assign Ticket")
        print("4. Change Ticket Status")
        print("5. Reopen Resolved Ticket")
        print("6. View Work Queue")
        print("7. View Reports")
        print("8. Search Tickets")
        print("9. Exit")
        print("=========================================")

        choice = input("Enter your choice: ").strip()

        # OPTION 1: CREATE TICKET
        if choice == "1":
            print("\nCreate Ticket")

            title = input("Enter ticket title: ")
            category = input(
                "Enter category (Network/Hardware/Software/Other): "
            )
            urgency = input("Enter urgency (low/medium/high): ")
            users = input("Enter number of affected users: ")

            try:
                affected_users = int(users)

                ticket = create_ticket(
                    tickets,
                    title,
                    category,
                    urgency,
                    affected_users
                )

                save_tickets(tickets)

                print("\nTicket created successfully!")
                print("Ticket ID:", ticket["id"])
                print("Title:", ticket["title"])
                print("Priority:", ticket["priority"])
                print("Status:", ticket["status"])

            except ValueError as error:
                print("Error:", error)

            except OSError as error:
                print("Error saving ticket:", error)

        # OPTION 2: VIEW TICKETS
        elif choice == "2":
            print("\nAll Tickets")

            if not tickets:
                print("No tickets available.")

            else:
                for ticket in tickets:
                    print("\n-------------------------")
                    print("ID:", ticket["id"])
                    print("Title:", ticket["title"])
                    print("Category:", ticket["category"])
                    print("Urgency:", ticket["urgency"])
                    print("Affected users:", ticket["affected_users"])
                    print("Priority:", ticket["priority"])
                    print("Status:", ticket["status"])
                    print("Assigned to:", ticket.get("assigned_to"))

        # OPTION 3: ASSIGN TICKET
        elif choice == "3":
            print("\nAssign Ticket")

            ticket_id = input("Enter ticket ID: ").strip()
            staff_name = input("Enter staff member's name: ").strip()

            try:
                assign_ticket(tickets, ticket_id, staff_name)
                save_tickets(tickets)

                print("Ticket assigned successfully!")

            except ValueError as error:
                print("Error:", error)

            except OSError as error:
                print("Error saving ticket:", error)

        # OPTION 4: CHANGE TICKET STATUS
        elif choice == "4":
            print("\nChange Ticket Status")
            print("Available transitions:")
            print("open -> in_progress")
            print("in_progress -> resolved")

            ticket_id = input("Enter ticket ID: ").strip()
            new_status = input(
                "Enter new status (in_progress/resolved): "
            ).strip().lower()

            try:
                update_status(tickets, ticket_id, new_status)
                save_tickets(tickets)

                print("Ticket status updated successfully!")

            except ValueError as error:
                print("Error:", error)

            except OSError as error:
                print("Error saving ticket:", error)

        # OPTION 5: REOPEN RESOLVED TICKET
        elif choice == "5":
            print("\nReopen Resolved Ticket")

            ticket_id = input(
                "Enter the ID of the resolved ticket: "
            ).strip()

            try:
                update_status(tickets, ticket_id, "open")
                save_tickets(tickets)

                print("Ticket reopened successfully!")
                print("New status: open")

            except ValueError as error:
                print("Error:", error)

            except OSError as error:
                print("Error saving ticket:", error)

        # OPTION 6: VIEW WORK QUEUE
        elif choice == "6":
            print("\nWork Queue")

            try:
                queue = get_work_queue(tickets)

                if not queue:
                    print("There are no unresolved tickets.")

                else:
                    for ticket in queue:
                        print("\n-------------------------")
                        print("ID:", ticket["id"])
                        print("Title:", ticket["title"])
                        print("Priority:", ticket["priority"])
                        print("Status:", ticket["status"])
                        print("Assigned to:", ticket.get("assigned_to"))

            except (KeyError, ValueError) as error:
                print("Error displaying work queue:", error)

        # OPTION 7: VIEW REPORTS
        elif choice == "7":
            print("\n========== TICKET REPORT ==========")

            try:
                report = generate_report(tickets)

                print("Total tickets:", report["total"])

                print("\nTickets by status:")
                for status, count in report["by_status"].items():
                    print(f"{status}: {count}")

                print("\nTickets by priority:")
                for priority, count in report["by_priority"].items():
                    print(f"{priority}: {count}")

                print("\nTickets by category:")
                for category, count in report["by_category"].items():
                    print(f"{category}: {count}")

                print("\nUnresolved tickets:", report["unresolved"])
                print("Resolved tickets:", report["resolved"])
                print(
                    "Resolution percentage:",
                    f'{report["resolution_percentage"]:.1f}%'
                )
                
                print("===================================")
            except (KeyError, TypeError) as error:
                print("Error generating report:", error)

        # OPTION 8: SEARCH TICKETS
        elif choice == "8":
            print("\nSearch Tickets")

            search_term = input(
                "Enter title keyword (press Enter to skip): "
            ).strip()

            category = get_valid_filter(
                "Enter category (Network/Hardware/Software/Other), "
                "or press Enter to skip: ",
                ["Network", "Hardware", "Software", "Other"]
            )

            status = get_valid_filter(
                "Enter status (open/in_progress/resolved), "
                "or press Enter to skip: ",
                ["open", "in_progress", "resolved"]
            )

            priority = get_valid_filter(
                "Enter priority (critical/high/medium/low), "
                "or press Enter to skip: ",
                ["critical", "high", "medium", "low"]
            )

            try:
                results = search_tickets(
                    tickets,
                    search_term=search_term,
                    category=category,
                    status=status,
                    priority=priority
                )

                if not results:
                    print("No matching tickets found.")

                else:
                    print(
                        f"\nFound {len(results)} matching ticket(s):"
                    )

                    for ticket in results:
                        print("\n-------------------------")
                        print("ID:", ticket["id"])
                        print("Title:", ticket["title"])
                        print("Category:", ticket["category"])
                        print("Priority:", ticket["priority"])
                        print("Status:", ticket["status"])
                        print("Assigned to:", ticket.get("assigned_to"))

            except (KeyError, AttributeError) as error:
                print("Error searching tickets:", error)
        # OPTION 9: EXIT
        elif choice == "9":
            print("Thank you for using CampusFlow!")
            break

        # INVALID MENU CHOICE
        else:
            print("Invalid choice. Please enter a number from 1 to 9.")

def get_valid_filter(prompt, valid_options):
    while True:
        value = input(prompt).strip()

        # An empty value means the user wants to skip this filter
        if value == "":
            return None

        # Accept valid options without worrying about letter case
        for option in valid_options:
            if value.casefold() == option.casefold():
                return option

        print(
            "Invalid option. Please choose from: "
            + ", ".join(valid_options)
        )

if __name__ == "__main__":
    main()