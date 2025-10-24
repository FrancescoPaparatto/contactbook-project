import unittest
from contacts import Contact


class TestContact(unittest.TestCase):
    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            contact = Contact(first_name="John", last_name="Carmack", phone_number="+39 329 3892918", email="john@.com")

    def test_valid_contact(self):
        contact = Contact(first_name="John", last_name="Carmack", phone_number="+39 329 3892918", email="john@test.com")

        self.assertEqual(contact.first_name, "John")
        self.assertEqual(contact.last_name, "Carmack")
        self.assertEqual(contact.get_full_name(), "John Carmack")


if __name__ == "__main__":
    unittest.main()
