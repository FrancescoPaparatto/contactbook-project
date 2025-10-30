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


@dataclass
class Contact:
    first_name: str 
    last_name: str
    phone_number: str
    id: str = field(default_factory=lambda: str(uuid4()))
    email: Optional[str] = None

    def _normalize_name(self, name: str) -> str:
        return name.strip().capitalize()

    def _validate_phone_number(self, phone_number: str) -> str:
        if not phone_number:
            raise MissingRequiredFieldError("Phone is require")

        if not re.match(PHONE_NUMBER_PATTERN, self.phone_number):
            raise InvalidPhoneError(
                "Invalid phone: phone must contain only digits with optional leading + (e.g. +393491234567)"
            )

        if not phone_number.strip().startswith(PREFIX):
            phone_number = PREFIX + phone_number

        phone_number_parts = phone_number.split()

        return "".join(phone_number_parts)

    def _validate_email(self, email: str | None) -> None:
        if not email:
            return 

        if not re.match(EMAIL_PATTERN, email):
            raise InvalidEmailError("Invalid email (expected email like name@example.com)")

    def get_full_name(self) -> str:
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"

    def __post_init__(self) -> None:
        if not self.first_name or not self.last_name:
            raise MissingRequiredFieldError("Provide first and last name.")

        self.first_name = self._normalize_name(self.first_name)
        self.last_name = self._normalize_name(self.last_name)
        self.phone_number = self._validate_phone_number(self.phone_number)
        self._validate_email(self.email)


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

