import unittest
import tempfile

from pathlib import Path

from campusflow.storage import save_tickets, load_tickets
from campusflow.tickets import create_ticket


class TestStorage(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = Path(self.temp_dir.name) / "tickets.json"

        self.tickets = []

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_save_tickets(self):

        create_ticket(
            self.tickets, "Wi-Fi down", "Network", "high", 12
        )

        save_tickets(self.tickets, self.file_path)

        self.assertTrue(self.file_path.exists())

    def test_load_tickets(self):

        create_ticket(
            self.tickets, "Laptop fault", "Hardware", "low", 2
        )

        save_tickets(self.tickets, self.file_path)

        loaded_tickets = load_tickets(self.file_path)

        self.assertEqual(loaded_tickets, self.tickets)

    def test_missing_file(self):

        loaded_tickets = load_tickets(self.file_path)

        self.assertEqual(loaded_tickets, [])

    def test_invalid_json(self):

        self.file_path.write_text(
            "{invalid json}",
            encoding="utf-8"
        )

        with self.assertRaises(ValueError):
            load_tickets(self.file_path)

    def test_invalid_data_structure(self):

        self.file_path.write_text(
            '{"id": "T001"}',
            encoding="utf-8"
        )

        with self.assertRaises(ValueError):
            load_tickets(self.file_path)

    def test_unique_id_after_loading(self):

        create_ticket(
            self.tickets, "Wi-Fi down", "Network", "high", 12
        )

        save_tickets(self.tickets, self.file_path)

        loaded_tickets = load_tickets(self.file_path)

        new_ticket = create_ticket(
            loaded_tickets, "Laptop fault", "Hardware", "low", 2
        )

        self.assertEqual(new_ticket["id"], "T002")

    def test_save_empty_tickets(self):

        save_tickets([], self.file_path)

        loaded_tickets = load_tickets(self.file_path)

        self.assertEqual(loaded_tickets, [])

    def test_invalid_json_is_not_modified(self):

        invalid_content = "{invalid json}"

        self.file_path.write_text(
            invalid_content,
            encoding="utf-8"
        )

        with self.assertRaises(ValueError):
            load_tickets(self.file_path)

        self.assertEqual(
            self.file_path.read_text(encoding="utf-8"),
            invalid_content
        )


if __name__ == "__main__":
    unittest.main()