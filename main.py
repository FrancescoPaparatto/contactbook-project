from contacts import Contact
from addressbook import AddressBook
from storage import Storage, JsonStorage
from helper_functions import prompt_contact_fields, render_contacts
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
        print("""\nCommands: 
new: start a new contactbook
add: add a new contact
list: list all contacts
search: search a contact
edit: edit a contact
delete: delete a contact
load: load contacts from json file
save: save the changes
exit: exit from the application
""")
        cmd = input("> ").strip().lower()

        if cmd == "new":
            addressbook: AddressBook = AddressBook(storage)
            print("Started a new address book.")
        elif cmd == "load":
            path = input("Path to JSON: ").strip()
            try:
                addressbook.load(path)
                print(f"Loaded {len(addressbook)} contacts from {path}.")

            except StorageError as e:
                print(f"Error: {e}")

        elif cmd == "add":
            fields = prompt_contact_fields()

            try:
                contact = Contact(**fields)

            except ContactValidationError as e:
                print(f"Validation Error: {e}")
                continue

            addressbook.add_contact(contact)
            print(f"Added contact: {contact.get_full_name()}")

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
                    print("Changes saved correctly.")
            break

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
