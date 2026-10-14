import unittest

from campusflow.workflow import assign_ticket, update_status

def make_ticket(
    ticket_id="T001",
    status="open",
    assigned_to=None,
):
    return {
        "id": ticket_id,
        "title": "Wi-Fi problem",
        "category": "Network",
        "urgency": "high",
        "affected_users": 10,
        "priority": "critical",
        "status": status,
        "assigned_to": assigned_to,
    }


class TestTicketWorkflow(unittest.TestCase):

    def test_assign_ticket_successfully(self):
        tickets = [make_ticket()]

        result = assign_ticket(tickets, "T001", "Dominion")

        self.assertEqual(result["assigned_to"], "Dominion")
        self.assertEqual(tickets[0]["assigned_to"], "Dominion")

    def test_assignment_strips_extra_spaces(self):
        tickets = [make_ticket()]

        assign_ticket(tickets, "T001", "  Mary  ")

        self.assertEqual(tickets[0]["assigned_to"], "Mary")

    def test_assignment_rejects_empty_staff_name(self):
        tickets = [make_ticket()]

        with self.assertRaises(ValueError):
            assign_ticket(tickets, "T001", "   ")

    def test_assignment_rejects_unknown_ticket(self):
        tickets = [make_ticket()]

        with self.assertRaises(ValueError):
            assign_ticket(tickets, "T999", "Mary")

    def test_cannot_assign_resolved_ticket(self):
        tickets = [
            make_ticket(status="resolved")
        ]

        with self.assertRaises(ValueError):
            assign_ticket(tickets, "T001", "Mary")

    def test_cannot_start_without_assignment(self):
        tickets = [make_ticket()]

        with self.assertRaises(ValueError):
            update_status(tickets, "T001", "in_progress")

        self.assertEqual(tickets[0]["status"], "open")

    def test_assigned_ticket_can_move_to_in_progress(self):
        tickets = [
            make_ticket(assigned_to="Mary")
        ]

        update_status(tickets, "T001", "in_progress")

        self.assertEqual(tickets[0]["status"], "in_progress")

    def test_in_progress_ticket_can_be_resolved(self):
        tickets = [
            make_ticket(
                status="in_progress",
                assigned_to="Mary",
            )
        ]

        update_status(tickets, "T001", "resolved")

        self.assertEqual(tickets[0]["status"], "resolved")

    def test_open_ticket_cannot_skip_to_resolved(self):
        tickets = [
            make_ticket(assigned_to="Mary")
        ]

        with self.assertRaises(ValueError):
            update_status(tickets, "T001", "resolved")

    def test_resolved_ticket_can_be_reopened(self):
        tickets = [
            make_ticket(status="resolved")
        ]

        update_status(tickets, "T001", "open")

        self.assertEqual(tickets[0]["status"], "open")

    def test_resolved_ticket_cannot_skip_reopening(self):
        tickets = [
            make_ticket(status="resolved")
        ]

        with self.assertRaises(ValueError):
            update_status(tickets, "T001", "in_progress")

    def test_invalid_status_is_rejected(self):
        tickets = [make_ticket()]

        with self.assertRaises(ValueError):
            update_status(tickets, "T001", "pending")

    def test_unknown_ticket_cannot_be_updated(self):
        tickets = [make_ticket()]

        with self.assertRaises(ValueError):
            update_status(tickets, "T999", "in_progress")


if __name__ == "__main__":
    unittest.main()
