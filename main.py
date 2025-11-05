import sys
from os import name, system
from contacts import Contact
from addressbook import AddressBook
from storage import Storage, JsonStorage
from helpers import (
    prompt_contact_fields,
    render_contacts,
    get_contact,
    validate_email,
    validate_phone_number,
)
from contact_exceptions import (
    ContactValidationError,
    DuplicateContactError, 
    ContactNotFoundError,
    StorageError,
    FileCorruptionError,
)


def main():
    storage: Storage = JsonStorage()
    addressbook: AddressBook = AddressBook(storage)

    while True:
        print("""\nStarting menu commands: 

new: start a new address book.
load: load from json file.
clear: clear the screen
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

            except FileCorruptionError as e:
                print(f"Error: {e}")

            except StorageError as e:

                print(f"Error: {e}")

        elif cmd == "clear":
            if name == "nt":
                system("cls")
            else: 
                system("clear")

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
clear: clear the screen
exit: exit from the application
""")
        cmd = input("> ").strip().lower()

        if cmd == "add":
            fields = prompt_contact_fields()
            try:
                contact = Contact(**fields)

            except DuplicateContactError as e:
                print(e)
                continue

            except ContactValidationError as e:
                print(f"Validation Error: {e}")
                continue

            addressbook.add_contact(contact)
            print(f"\nContact '{contact.get_full_name()}' added successfully.")

        elif cmd == "list":
            render_contacts(addressbook.list_contacts())

        elif cmd == "search":
            query = input("\nSearch contact: ")
            contact_found = get_contact(query, addressbook)

            render_contacts([contact_found])

        elif cmd == "edit":
            query = input("Select the contact you want to edit: ")

            contact_to_update = get_contact(query, addressbook)
            print("\nCurrent contact informations:")
            print(f"First: {contact_to_update.first_name}")
            print(f"Last:  {contact_to_update.last_name}")
            print(f"Phone: {contact_to_update.phone_number}")
            print(f"Email: {contact_to_update.email or ''}")

            print("\nAdd new contact data (leave blank to keep): ")

            first_name = input("First name: ").title().strip() or contact_to_update.first_name
            last_name = input("Last name: ").title().strip() or contact_to_update.last_name
            phone_number = validate_phone_number(
                input("Phone number: ").strip() or contact_to_update.phone_number
            )
            email = validate_email(input("Email: ")) or (contact_to_update.email or None)
            

            try:
                updated_contact = Contact(
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number,
                    email=email,
                )
                addressbook.update_contact(contact_to_update, updated_contact)
                print(f"\nContact '{updated_contact.get_full_name()}' updated successfully.")

            except ContactNotFoundError as e:
                print(e)

        elif cmd == "delete":
            query = input("Search contact: ")
            contact_found = get_contact(query, addressbook)

            render_contacts([contact_found])
            choice = input(
                f"\nAre you sure to remove '{contact_found.get_full_name()}'? [y/N]: "
            )

            if choice.strip().lower() not in ["", "y", "n"]:
                print("Invalid choice.")
                continue

            if choice == "y":
                try:
                    addressbook.delete_contact(contact_found)
                except KeyError as e:
                    print(e)
                    continue

                print(
                    f"\nContact '{contact_found.get_full_name()}' removed successfully."
                )

        elif cmd == "save":
            path = input("Path to save JSON: ").strip()
            addressbook.save(path)
            print(f"Saved to '{path}'.")

            break

        elif cmd == "clear":
            if name == "nt":
                system("cls")
            else: 
                system("clear")

        elif cmd == "exit":
            if addressbook.is_changed:
                answer = (
                    input("You have unsaved changes. Save before exit? [y/N] ")
                    .strip()
                    .lower()
                )

                if answer.strip().lower() not in ["", "y", "n"]:
                    print("Invalid choice.")
                    continue

                if answer == "y":
                    path = input("Path to save JSON: ").strip()
                    addressbook.save(path)
                    print("\nChanges saved correctly.")

            sys.exit()

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
