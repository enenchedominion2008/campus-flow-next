
from campusflow.tickets import create_ticket
from campusflow.storage import save_tickets, load_tickets
from campusflow.workflow import assign_ticket, update_status
from campusflow.queue import get_work_queue
from campusflow.reports import generate_report


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
        print("8. Exit")
        print("=========================================")

        choice = input("Enter your choice: ").strip()

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

        # OPTION 3: ASSIGN TICKET - ENGINEER B
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

        # OPTION 4: CHANGE STATUS - ENGINEER B
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

        # OPTION 5: REOPEN RESOLVED TICKET - ENGINEER B
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

        # OPTION 6: VIEW WORK QUEUE - ENGINEER B
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

        # OPTION 7: VIEW REPORTS - ENGINEER B
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

                print("===================================")

            except (KeyError, TypeError) as error:
                print("Error generating report:", error)

        # OPTION 8: EXIT
        elif choice == "8":
            print("Thank you for using CampusFlow!")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()

