from contact_exceptions import (
    ContactValidationError,
    InvalidEmailError,
    InvalidPhoneError,
)


def prompt_contact_fields() -> dict:
    while True:
        first_name = input("First name (required): ")
        last_name = input("Last name (required): ")
        phone_number = input("Phone (required): ")
        email = input("Email (optional): ")

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
        
