import unittest
from contacts import Contact
from contact_exceptions import (
    InvalidEmailError,
    InvalidPhoneError,
    MissingRequiredFieldError, 
)

# TODO: remove names from test cases and create like contact1, contact2 or find if there are best practices about naming

# TODO: correct errors name in the assertRaises functions after I complete the data validation and exceptions modules

class TestContact(unittest.TestCase):

    def test_invalid_email(self):
        with self.assertRaises(InvalidEmailError):
            contact = Contact(
                first_name="Linus",
                last_name="Torvalds",
                phone_number="+39 329 3892918",
                email="linus@.com",
            )

    def test_invalid_contact(self):
        with self.assertRaises(MissingRequiredFieldError):
            contact = Contact(
                first_name="Steve",
                last_name="",
                phone_number="+39 329 3892918",
                email="stevejobs@test.com",
            )
            contact = Contact(
                first_name="",
                last_name="Carmack",
                phone_number="+39 329 3892918",
                email="johncarmack@test.com",
            )

    def test_valid_contact(self):
        contact = Contact(
            first_name="Alan",
            last_name="Turing",
            phone_number="+39 329 3892918",
            email="alanturing@test.com",
        )

        self.assertEqual(contact.first_name, "Alan")
        self.assertEqual(contact.last_name, "Turing")
        self.assertEqual(contact.get_full_name(), "Alan Turing")

    def test_name_normalization(self):
        contact = Contact(
            first_name="    elon",
            last_name="musk   ",
            phone_number="+39 329 3892918",
            email="elonmusk@test.com",
        )

        self.assertEqual(contact.first_name, "Elon")
        self.assertEqual(contact.last_name, "Musk")

    def test_phone_number_normalization(self):
        contact = Contact(
            first_name="John",
            last_name="Carmack",
            phone_number="+39 329 3892918",
            email="john@test.com",
        )
        second_contact = Contact(
            first_name="Elon",
            last_name="Musk",
            phone_number="329 3892919",
            email="elon@test.com",
        )

        self.assertEqual(contact.phone_number, "+393293892918")
        self.assertEqual(second_contact.phone_number, "+393293892919")

        with self.assertRaises(InvalidPhoneError):
            contact = Contact(
                first_name="Pavel",
                last_name="Durov",
                phone_number="+39 329 389 291902934",
                email="pavel@telegram.com",
            )


if __name__ == "__main__":
    unittest.main()
