# data validation in this file
# fields
# - first name* (not a lot validation needed for my use case)
# - last name* (same as for first name)
# - phone number* (validation needed)
# - email (validation needed but not mandatory field)
# - date of birth (validation needed and standardized format)
# - address

import re
from uuid import uuid4, UUID
from typing import Optional
from dataclasses import dataclass, field
from contact_exceptions import (
    InvalidEmailError,
    InvalidPhoneError,
    MissingRequiredFieldError,
)


# TODO: in the docs, specify that I have simplified email validation and not covered all possible use cases
EMAIL_PATTERN = r"^[\w\.]+@([\w]+\.)+[\w]{2,3}$"
PHONE_NUMBER_PATTERN = r"^(?:\+39\s?)?3\d{2}\s?\d{3}\s?\d{4}$"
PREFIX = "+39"


@dataclass
class Contact:
    phone_number: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    id: UUID = field(default_factory=uuid4)
    email: Optional[str] = None

    def _normalize_name(self, name: str) -> str:
        # I should here only think to the logic of the function, in the post init check if the name exist
        return name.strip().capitalize()

    def _normalize_phone_number(self, phone_number: str) -> str:
        if not re.match(PHONE_NUMBER_PATTERN, self.phone_number):
            raise InvalidPhoneError(
                "Invalid phone: phone must contain only digits with optional leading + (e.g. +393491234567)"
            )

        # I am checking if the phone.strip() start with the italian prefix
        if not phone_number.strip().startswith(PREFIX):
            phone_number = PREFIX + phone_number

        phone_number_parts = phone_number.split()

        return "".join(phone_number_parts)

    def get_full_name(self) -> str | None:
        # TODO: the full name should be created only after normalization
        # TODO: if something is missed, I can't create the full name so I should only to use one field and in the list all, I should sort contacts so I need to understand components (I mean: lambda r: r[1] (first last_name), r[0] (then first)) but what happens if the user is saved only with one
        if self.first_name and self.last_name:
            return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"

    def __post_init__(self) -> None:
        # TODO: understand if there is a way to handle this better
        if not self.first_name and not self.last_name:
            raise MissingRequiredFieldError("Provide at least first or last name")
        if self.first_name:
            self.first_name = self._normalize_name(self.first_name)

        if self.last_name:
            self.last_name = self._normalize_name(self.last_name)

        self.phone_number = self._normalize_phone_number(self.phone_number)

        if self.email and not re.match(EMAIL_PATTERN, self.email):
            raise InvalidEmailError("Invalid email")


# first the user add fields
# those fields will be checked and normalized but first should be checked

if __name__ == "__main__":
    try:
        # this try/except block will be done when a contact is created, the only things I need to understand is if do I need to add it in a while loop
        elon = Contact(
            first_name="Elon",
            last_name="Musk",
            phone_number="329 3892919",
            email="elon@test.com",
        )
    except MissingRequiredFieldError as e:
        print(f"{type(e).__name__}: {e}")

    else:
        print(elon)
        print(elon.last_name)
