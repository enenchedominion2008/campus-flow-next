import unittest

from campusflow.search import search_tickets


class TestSearchTickets(unittest.TestCase):

    def setUp(self):
        """Create sample tickets for each test."""
        self.tickets = [
            {
                "id": "T001",
                "title": "Campus Wi-Fi is down",
                "category": "Network",
                "priority": "critical",
                "status": "open",
                "assigned_to": None,
            },
            {
                "id": "T002",
                "title": "Laptop screen is broken",
                "category": "Hardware",
                "priority": "high",
                "status": "in_progress",
                "assigned_to": "dominion",
            },
            {
                "id": "T003",
                "title": "Python installation problem",
                "category": "Software",
                "priority": "medium",
                "status": "resolved",
                "assigned_to": "ada",
            },
        ]

    def test_search_by_title(self):
        results = search_tickets(self.tickets, search_term="laptop")
        self.assertEqual([ticket["id"] for ticket in results], ["T002"])

    def test_title_search_is_case_insensitive(self):
        results = search_tickets(self.tickets, search_term="LAPTOP")
        self.assertEqual([ticket["id"] for ticket in results], ["T002"])

    def test_filter_by_category(self):
        results = search_tickets(self.tickets, category="network")
        self.assertEqual([ticket["id"] for ticket in results], ["T001"])

    def test_filter_by_status(self):
        results = search_tickets(self.tickets, status="resolved")
        self.assertEqual([ticket["id"] for ticket in results], ["T003"])

    def test_filter_by_priority(self):
        results = search_tickets(self.tickets, priority="high")
        self.assertEqual([ticket["id"] for ticket in results], ["T002"])

    def test_filters_combine_with_and_logic(self):
        results = search_tickets(
            self.tickets,
            category="Network",
            status="open",
            priority="high",
        )
        self.assertEqual(results, [])

    def test_no_filters_returns_all_tickets(self):
        results = search_tickets(self.tickets)
        self.assertEqual(len(results), 3)

    def test_no_matches_returns_empty_list(self):
        results = search_tickets(self.tickets, search_term="nonexistent")
        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main() 