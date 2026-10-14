import unittest
from campusflow.validation import (
    validate_ticket, validate_ticket_collection, validate_note_shape,
)


def valid_ticket(tid="T001"):
    return {
        "id": tid, "title": "wifi down", "category": "Network",
        "urgency": "low", "affected_users": 1, "priority": "low",
        "status": "open", "assigned_to": None, "notes": [],
    }


class TestValidation(unittest.TestCase):

    def test_valid_ticket_passes(self):
        ok, _ = validate_ticket(valid_ticket())
        self.assertTrue(ok)

    def test_bool_affected_users_rejected(self):
        t = valid_ticket(); t["affected_users"] = True
        ok, _ = validate_ticket(t)
        self.assertFalse(ok)

    def test_float_affected_users_rejected(self):
        t = valid_ticket(); t["affected_users"] = 2.5
        ok, _ = validate_ticket(t)
        self.assertFalse(ok)

    def test_zero_affected_users_rejected(self):
        t = valid_ticket(); t["affected_users"] = 0
        ok, _ = validate_ticket(t)
        self.assertFalse(ok)

    def test_invalid_category_rejected(self):
        t = valid_ticket(); t["category"] = "banana"
        ok, _ = validate_ticket(t)
        self.assertFalse(ok)

    def test_blank_title_rejected(self):
        t = valid_ticket(); t["title"] = "   "
        ok, _ = validate_ticket(t)
        self.assertFalse(ok)

    def test_duplicate_ticket_id_rejected(self):
        ok, _ = validate_ticket_collection([valid_ticket("T001"), valid_ticket("T001")])
        self.assertFalse(ok)

    def test_non_dict_entry_rejected(self):
        ok, _ = validate_ticket_collection(["not a ticket"])
        self.assertFalse(ok)

    def test_note_shape_too_short_rejected(self):
        ok, _ = validate_note_shape({"note_id": "N001", "author": "A", "message": "hi"})
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()