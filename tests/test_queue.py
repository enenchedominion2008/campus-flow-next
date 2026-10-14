
import unittest

from campusflow.queue import get_work_queue


def make_ticket(ticket_id, priority, status="open"):
    return {
        "id": ticket_id,
        "title": f"Ticket {ticket_id}",
        "category": "Network",
        "urgency": "medium",
        "affected_users": 3,
        "priority": priority,
        "status": status,
        "assigned_to": None,
    }


class TestWorkQueue(unittest.TestCase):

    def test_critical_tickets_come_first(self):
        tickets = [
            make_ticket("T001", "low"),
            make_ticket("T002", "critical"),
            make_ticket("T003", "high"),
        ]

        result = get_work_queue(tickets)

        self.assertEqual(
            [ticket["id"] for ticket in result],
            ["T002", "T003", "T001"],
        )

    def test_tickets_are_sorted_by_priority(self):
        tickets = [
            make_ticket("T001", "medium"),
            make_ticket("T002", "low"),
            make_ticket("T003", "high"),
            make_ticket("T004", "critical"),
        ]

        result = get_work_queue(tickets)

        self.assertEqual(
            [ticket["priority"] for ticket in result],
            ["critical", "high", "medium", "low"],
        )

    def test_same_priority_uses_numeric_ticket_id(self):
        tickets = [
            make_ticket("T010", "high"),
            make_ticket("T002", "high"),
            make_ticket("T001", "high"),
        ]

        result = get_work_queue(tickets)

        self.assertEqual(
            [ticket["id"] for ticket in result],
            ["T001", "T002", "T010"],
        )

    def test_only_open_tickets_in_queue(self):
        tickets = [
            make_ticket("T001", "critical", "resolved"),
            make_ticket("T002", "high", "open"),
            make_ticket("T003", "medium", "in_progress"),
        ]

        result = get_work_queue(tickets)

        self.assertEqual(
            [ticket["id"] for ticket in result],
            ["T002"],
        )
    def test_empty_ticket_list_returns_empty_list(self):
        self.assertEqual(get_work_queue([]), [])

    def test_original_ticket_list_is_not_reordered(self):
        tickets = [
            make_ticket("T003", "low"),
            make_ticket("T001", "critical"),
            make_ticket("T002", "high"),
        ]

        original_ids = [ticket["id"] for ticket in tickets]

        get_work_queue(tickets)

        self.assertEqual(
            [ticket["id"] for ticket in tickets],
            original_ids,
        )


if __name__ == "__main__":
    unittest.main()
