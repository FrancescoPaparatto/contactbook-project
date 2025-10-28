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
                first_name="John",
                last_name="Carmack",
                phone_number="+39 329 3892918",
                email="john@.com",
            )

    def test_invalid_contact(self):
        with self.assertRaises(MissingRequiredFieldError):
            contact = Contact(
                first_name="",
                last_name="",
                phone_number="+39 329 3892918",
                email="john@test.com",
            )

    def test_valid_contact(self):
        contact = Contact(
            first_name="John",
            last_name="Carmack",
            phone_number="+39 329 3892918",
            email="john@test.com",
        )

        self.assertEqual(contact.first_name, "John")
        self.assertEqual(contact.last_name, "Carmack")
        self.assertEqual(contact.get_full_name(), "John Carmack")

    def test_name_normalization(self):
        contact = Contact(
            first_name="    john",
            last_name="Carmack   ",
            phone_number="+39 329 3892918",
            email="john@test.com",
        )

        self.assertEqual(contact.first_name, "John")
        self.assertEqual(contact.last_name, "Carmack")

    def test_phone_number_normalization(self):
        john = Contact(
            first_name="John",
            last_name="Carmack",
            phone_number="+39 329 3892918",
            email="john@test.com",
        )
        elon = Contact(
            first_name="Elon",
            last_name="Musk",
            phone_number="329 3892919",
            email="elon@test.com",
        )

        self.assertEqual(john.phone_number, "+393293892918")
        self.assertEqual(elon.phone_number, "+393293892919")

        with self.assertRaises(InvalidPhoneError):
            pavel = Contact(
                first_name="Pavel",
                last_name="Durov",
                phone_number="+39 329 389 291902934",
                email="pavel@telegram.com",
            )


if __name__ == "__main__":
    unittest.main()
