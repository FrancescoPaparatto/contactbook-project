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


# TODO: in the docs, specify that I have simplified email validation and not covered all possible use cases
EMAIL_PATTERN = r"^[\w\.]+@([\w]+\.)+[\w]{2,3}$"

@dataclass
class Contact: 
    phone_number: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    id: UUID = field(default_factory=uuid4)
    email: Optional[str] = None

    def _normalize_name(self, name: str) -> str | None:
        if name:
            return name.strip().capitalize()

    def get_full_name(self):
        # TODO: understand if this method is necessary or if there is a better way to do it.
        if self.first_name and self.last_name:
            return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"

    def __post_init__(self):
        # TODO: understand if there is a way to handle this better
        if self.email and not re.match(EMAIL_PATTERN, self.email):
                raise ValueError("Invalid email format")
    
        if self.first_name:
            self.first_name = self._normalize_name(self.first_name)

        if self.last_name:
            self.last_name = self._normalize_name(self.last_name)


if __name__ == "__main__":
    # I noticed that for optional parameters if I don't use positional arguments they are assigned randomly, for example 'Musk' could be assigned to the phone_number variable
    john = Contact(first_name="John", last_name="Carmack", phone_number="+39 329 3892918", email="john@test.com")
    sec= Contact(first_name="Elon", last_name="Musk", phone_number="+39 329 3892919", email="elon@test.com")





