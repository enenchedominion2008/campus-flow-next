import unittest
from campusflow.notes import add_note, next_note_id


def ticket(status="open", notes=None, tid="T001"):
    return {
        "id": tid, "title": "wifi down", "category": "Network",
        "urgency": "high", "affected_users": 12, "priority": "critical",
        "status": status, "assigned_to": None, "notes": notes or [],
    }


class TestNotes(unittest.TestCase):

    def test_valid_note_added_with_correct_id(self):
        t = ticket()
        note = add_note("T001", "Mentor A", "Wi-Fi router rebooted", [t])
        self.assertEqual(note["note_id"], "N001")
        self.assertEqual(len(t["notes"]), 1)

    def test_blank_author_rejected_without_consuming_id(self):
        t = ticket()
        with self.assertRaises(ValueError):
            add_note("T001", "   ", "Some message here", [t])
        self.assertEqual(t["notes"], [])
        note = add_note("T001", "Mentor A", "Valid message", [t])
        self.assertEqual(note["note_id"], "N001")

    def test_short_message_rejected(self):
        t = ticket()
        with self.assertRaises(ValueError):
            add_note("T001", "Mentor A", "hi", [t])
        self.assertEqual(t["notes"], [])

    def test_note_on_resolved_rejected(self):
        t = ticket(status="resolved")
        with self.assertRaises(ValueError):
            add_note("T001", "Mentor A", "Trying anyway", [t])
        self.assertEqual(t["notes"], [])

    def test_note_after_reopen_accepted(self):
        t = ticket(status="resolved", notes=[
            {"note_id": "N001", "author": "A", "message": "first note here"}
        ])
        t["status"] = "open"
        note = add_note("T001", "Mentor B", "Investigated port", [t])
        self.assertEqual(note["note_id"], "N002")


if __name__ == "__main__":
    unittest.main()