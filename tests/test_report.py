
import unittest

from campusflow.reports import generate_report


def make_ticket(ticket_id, priority, status):
    return {
        "id": ticket_id,
        "title": f"Ticket {ticket_id}",
        "category": "Software",
        "urgency": "medium",
        "affected_users": 3,
        "priority": priority,
        "status": status,
        "assigned_to": None,
    }


class TestGenerateReport(unittest.TestCase):

    def test_empty_ticket_list(self):
        report = generate_report([])

        self.assertEqual(report["total"], 0)

        self.assertEqual(
            report["by_status"],
            {
                "open": 0,
                "in_progress": 0,
                "resolved": 0,
            },
        )

        self.assertEqual(
            report["by_priority"],
            {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
            },
        )

    def test_total_ticket_count(self):
        tickets = [
            make_ticket("T001", "critical", "open"),
            make_ticket("T002", "high", "in_progress"),
            make_ticket("T003", "low", "resolved"),
        ]

        report = generate_report(tickets)

        self.assertEqual(report["total"], 3)

    def test_counts_tickets_by_status(self):
        tickets = [
            make_ticket("T001", "high", "open"),
            make_ticket("T002", "medium", "open"),
            make_ticket("T003", "low", "in_progress"),
            make_ticket("T004", "critical", "resolved"),
        ]

        report = generate_report(tickets)

        self.assertEqual(
            report["by_status"],
            {
                "open": 2,
                "in_progress": 1,
                "resolved": 1,
            },
        )

    def test_counts_tickets_by_priority(self):
        tickets = [
            make_ticket("T001", "critical", "open"),
            make_ticket("T002", "high", "open"),
            make_ticket("T003", "high", "resolved"),
            make_ticket("T004", "medium", "in_progress"),
            make_ticket("T005", "low", "resolved"),
        ]

        report = generate_report(tickets)

        self.assertEqual(
            report["by_priority"],
            {
                "critical": 1,
                "high": 2,
                "medium": 1,
                "low": 1,
            },
        )

    def test_report_counts_match_total(self):
        tickets = [
            make_ticket("T001", "critical", "open"),
            make_ticket("T002", "high", "in_progress"),
            make_ticket("T003", "medium", "resolved"),
            make_ticket("T004", "low", "open"),
        ]

        report = generate_report(tickets)

        self.assertEqual(
            sum(report["by_status"].values()),
            report["total"],
        )

        self.assertEqual(
            sum(report["by_priority"].values()),
            report["total"],
        )


if __name__ == "__main__":
    unittest.main()
