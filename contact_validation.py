# data validation in this file
# fields
# - first name* (not a lot validation needed for my use case)
# - last name* (same as for first name)
# - phone number* (validation needed)
# - email (validation needed but not mandatory field)
# - date of birth (validation needed and standardized format)
# - address

import re
from uuid import uuid4
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

def _validate_phone_number(phone_number: str) -> str:
    if not phone_number:
        raise MissingRequiredFieldError("Phone is require")

    if not re.match(PHONE_NUMBER_PATTERN, phone_number):
        raise InvalidPhoneError(
            "Invalid phone: phone must contain only digits with optional leading + (e.g. +393491234567)"
        )

    if not phone_number.strip().startswith(PREFIX):
        phone_number = PREFIX + phone_number

    phone_number_parts = phone_number.split()

    return "".join(phone_number_parts)

def _validate_email(email: str | None) -> None:
    if not email:
        return 

    if not re.match(EMAIL_PATTERN, email):
        raise InvalidEmailError("Invalid email (expected email like name@example.com)")

@dataclass
class Contact:
    first_name: str
    last_name: str
    _phone_number: str
    # TODO: understand why do i need lambda instead of using directly str()
    id: str = field(default_factory=lambda: str(uuid4()))
    _email: Optional[str] = None

    def __init__(self, first_name: str, last_name: str, phone_number: str, email: str | None) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email

    @property
    def phone_number(self) -> str:
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value: str) -> None:
        self._phone_number = _validate_phone_number(value)

    @property
    def email(self) -> str | None:
        return self._email

    @email.setter
    def email(self, value: str | None) -> None:
        self.emailj = _validate_email(value)

    def get_full_name(self) -> str:
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"

    def __post_init__(self) -> None:
        self.first_name = self.first_name.strip().capitalize()
        self.last_name = self.last_name.strip().capitalize()


    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": self.phone_number,
            "email": self.email,
        }

    @staticmethod
    def from_dict(d: dict) -> "Contact":
        return Contact(
            first_name=d["first_name"],
            last_name=d["last_name"],
            phone_number=d["phone"],
            email=d.get("email")
        )

