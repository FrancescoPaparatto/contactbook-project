import re
from contact_exceptions import (
    InvalidEmailError,
    InvalidPhoneError,
    MissingRequiredFieldError,
)

EMAIL_PATTERN = r"^[\w\.]+@([\w]+\.)+[\w]{2,3}$"
PHONE_NUMBER_PATTERN = r"^(?:\+39\s?)?3\d{2}\s?\d{3}\s?\d{4}$"
PREFIX = "+39"


def validate_name(name: str) -> str:
    if not name:
        raise MissingRequiredFieldError("Missing required field: ")
    return name.strip().capitalize()


def validate_phone_number(phone_number: str) -> str:
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


def validate_email(email: str | None) -> str | None:
    if not email:
        return

    if not re.match(EMAIL_PATTERN, email):
        raise InvalidEmailError("Invalid email (expected email like name@example.com)")

    return email

def ask_first_name() -> str:
    while True:
        try:
            first_name = validate_name(input("First name (required): "))
        except MissingRequiredFieldError as e:
            print(f"{e} 'First name'")
            continue

        return first_name


def ask_last_name() -> str:
    while True:
        try:
            last_name = validate_name(input("Last name (required): "))
        except MissingRequiredFieldError as e:
            print(f"{e} 'Last name'.")
            continue

        return last_name


def ask_phone_number() -> str:
    while True:
        try:
            phone_number = validate_phone_number(input("Phone number (required): "))

        except MissingRequiredFieldError as e:
            print(e)
            continue

        except InvalidPhoneError as e:
            print(e)
            continue

        return phone_number


def ask_email() -> str | None:
    while True:
        try:
            email = validate_email(input("Email (optional): "))

        except InvalidEmailError as e:
            print(e)
            continue

        return email


def prompt_contact_fields() -> dict:
    while True:
        first_name = ask_first_name()
        last_name = ask_last_name()
        phone_number = ask_phone_number()
        email = ask_email()

        return {
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "email": email or None,
        }


def render_contacts(contacts):
    if not contacts:
        print("No contacts in address book.")
        return
    print(f"{'Last':15}  {'First':15}  {'Phone':17}  {'Email'}")
    print("-" * 90)
    for contact in contacts:
        # display phone number in international format so it's more readable
        render_phone_number = f"{contact.phone_number[:3]} {contact.phone_number[3:6]} {contact.phone_number[6:9]} {contact.phone_number[9:]}"
        print(
            f"{(contact.last_name):15}  {(contact.first_name):15}  {render_phone_number:17}  {contact.email or ''}"
        )
