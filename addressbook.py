from typing import Dict, List, Optional
from contacts import Contact
from contact_exceptions import DuplicateContactError, ContactNotFoundError


class AddressBook:
    def __init__(self):
        self.contacts: Dict[str, Contact] = {}
        # Dictionaries created for duplicates check in order to search faster
        self._phone_idx: Dict[str, str] = {}  # maps phone -> id
        self._email_idx: Dict[str, str] = {}  # maps email -> id

        # Flag used to keep track of the changes
        self.is_changed = False

    def add_contact(self, contact: Contact) -> Contact:
        self._check_duplicate_contact(contact)

        self.contacts[contact.id] = contact
        self._phone_idx[contact.phone_number] = contact.id

        if contact.email:
            self._email_idx[contact.email] = contact.id

        self.is_changed = True

        # return the contact object in order to make easier to show the user changes
        return contact

    def delete_contact(self, contact: Contact) -> None:
        deleted_contact = self.contacts.pop(contact.id, None)

        if deleted_contact is None:
            raise ContactNotFoundError("Contact not found.")

        # Remove it also from second indexes dictionaries
        self._phone_idx.pop(contact.phone_number, None)

        if contact.email:
            self._email_idx.pop(contact.email, None)

        self.is_changed = True

    def update_contact(
        self, contact_to_update: Contact, updated_contact: Contact
    ) -> Contact:
        # TODO: check this function better

        if contact_to_update.id not in self.contacts:
            raise ContactNotFoundError("Contact not found.")

        new_contact = Contact(
            id=contact_to_update.id,
            first_name=updated_contact.first_name,
            last_name=updated_contact.last_name,
            phone_number=updated_contact.phone_number,
            email=updated_contact.email,
        )

        self._check_duplicate_contact(new_contact, exclude_id=contact_to_update.id)
        self._replace_contact(contact_to_update, new_contact)
        self.is_changed = True

        return new_contact

    def list_all_contacts(self) -> List[Contact]:
        return [
            contact
            for contact in sorted(
                # sort first for last name, then for first name and then for id
                self.contacts.values(),
                key=lambda contact: (contact.last_name, contact.first_name, contact.id),
            )
        ]

    def search_contact(self, search_term: str) -> List[Contact]:
        # TODO: check this function
        # alternatives: raise ContactNotFound here or raising it in the Orchestrator
        return [
            contact
            for contact in self.contacts.values()
            if search_term.lower() in contact.first_name.lower()
            or search_term in contact.last_name.lower()
        ]

    # I created two helper functions for simplify the processes of other functions: check duplicate and replace
    def _check_duplicate_contact(
        self, contact: Contact, exclude_id: Optional[str] = None
    ) -> None:
        id = self._phone_idx.get(contact.phone_number)

        if id is not None and id != exclude_id:
            raise DuplicateContactError("Phone number already used by another contact")

        if contact.email:
            id = self._email_idx.get(contact.email)

            if id is not None and id != exclude_id:
                raise DuplicateContactError("Email already used by another contact")

    def _replace_contact(self, old_contact: Contact, new_contact: Contact) -> Contact:
        self.contacts[new_contact.id] = new_contact
        if new_contact.phone_number != old_contact.phone_number:
            self._phone_idx.pop(old_contact.phone_number, None)
            self._phone_idx[new_contact.phone_number] = new_contact.id

        if (old_contact.email or None) != (new_contact.email or None):
            if old_contact.email:
                self._email_idx.pop(old_contact.email, None)

            if new_contact.email:
                self._email_idx[new_contact.email] = new_contact.id
        return new_contact
