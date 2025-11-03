import sys
from contacts import Contact
from addressbook import AddressBook
from storage import Storage, JsonStorage
from contact_exceptions import (
    ContactValidationError,
    InvalidEmailError,
    InvalidPhoneError,
    DuplicateContactError,
    ContactNotFoundError,
    StorageError,
    FileCorruptionError,
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
        

def main():
    storage: Storage = JsonStorage()
    addressbook: AddressBook = AddressBook(storage)

    while True:
        print("""\n Starting menu commands: 

new: start a new address book.
load: load from json file.
exit: exit from the program.
""")

        cmd = input("> ").strip().lower()

        if cmd == "new":
            addressbook: AddressBook = AddressBook(storage)
            print("Started a new address book.")
            break

        elif cmd == "load":
            path = input("Path to JSON: ").strip()

            try:
                addressbook.load(path)
                print(f"Loaded {len(addressbook)} contacts from {path}.")
                break
            except StorageError as e:
                print(f"Error: {e}")

        elif cmd == "exit":
            sys.exit()

        else:
            print("Invalid command.")

    while True:
        print("""\nCommands: 

add: add a new contact
list: list all contacts
search: search a contact
edit: edit a contact
delete: delete a contact
save: save the changes
exit: exit from the application
""")
        cmd = input("> ").strip().lower()

        if cmd == "add":
            fields = prompt_contact_fields()
            try:
                contact = Contact(**fields)

            except (InvalidPhoneError, InvalidEmailError, ContactValidationError) as e:
                print(f"Validation Error: {e}")
                continue

            addressbook.add_contact(contact)
            print(f"\nContact '{contact.get_full_name()}' added successfully.")

        elif cmd == "list":
            render_contacts(addressbook.list_contacts())

        elif cmd == "search":
            ...
        elif cmd == "edit":
            ...
        elif cmd == "delete":
            ...
        elif cmd == "save":
            path = input("Path to save JSON: ").strip()
            addressbook.save(path)
            print(f"Saved to '{path}'.")

            break
        elif cmd == "exit":
            if addressbook.is_changed:
                answer = (
                    input("You have unsaved changes. Save before exit? [y/N] ")
                    .strip()
                    .lower()
                )
                if answer == "y":
                    path = input("Path to save JSON: ").strip()
                    addressbook.save(path)
                    print("\nChanges saved correctly.")

            sys.exit()

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
