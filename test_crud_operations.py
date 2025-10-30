# TODO: ADD TYPE HINTS FOR EACH FUNCTION
# TODO: check each test and understand if all make sense and if I tested also edge cases and something like that

import unittest
from contacts import Contact
from addressbook import AddressBook
from contact_exceptions import ContactNotFoundError, DuplicateContactError


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

        self.addressbook.add_contact(self.contact)

    def test_add_contact(self):
        # Maybe this test case could be eliminated but leave it for now
        self.assertIsInstance(self.contact, Contact)
        self.assertIn(self.contact, self.addressbook.contacts.values())
        # check if this function goes here or if it's necessary a different test for second indexes
        self.assertIn(self.contact.phone_number, self.addressbook._phone_idx)

    def test_delete_contact(self):
        # first assert that contact has been added
        self.assertIn(self.contact, self.addressbook.contacts.values())

        self.addressbook.delete_contact(self.contact)
        self.assertDictEqual(self.addressbook.contacts, {})

    def test_exists(self): 
        self.assertIn(self.contact.phone_number, self.addressbook._phone_idx)


    def test_search_contact(self): ...


if __name__ == "__main__":
    unittest.main()
