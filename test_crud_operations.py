# TODO: ADD TYPE HINTS FOR EACH FUNCTION

import unittest
from contacts import Contact
from addressbook import AddressBook


class TestAddressBook(unittest.TestCase):
    # TODO: Understand if is better to use setUP or setUpClass
    def setUp(self) -> None:
        # Instantiate an addressbook and a contact object before executing each test
        self.addressbook = AddressBook()

        self.contact = Contact(
            first_name="John",
            last_name="Carmack",
            phone_number="+39 329 3892918",
            email="john@testcrud.com",
        )

    def test_add_contact(self):
        self.addressbook.add_contact(self.contact)

        # Maybe this test case could be eliminated but leave it for now
        self.assertIsInstance(self.contact, Contact)
        self.assertIn(self.contact, self.addressbook.contacts.values())

    def test_exist(self):
        self.addressbook.add_contact(self.contact)
        self.assertTrue(self.addressbook.exists(self.contact))

if __name__ == "__main__":
    unittest.main()

