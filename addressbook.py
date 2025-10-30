from contacts import Contact
from contact_exceptions import DuplicateContactError


class AddressBook:
    def __init__(self):
        self.contacts = {}
        # dictionary that stores phone_number -> id as second indexes
        # mapping phone -> id for fast searching if a contact exist because the invariant is same number = same contact
        self._phone_idx = {}

    def add_contact(self, contact: Contact) -> None:
        # TODO: understand if the check isinstance is ok here instead of doing it in the orchestrator and also if is necessary since I checked with type hint

        # I think I should assume that this class will receive a valid Contact, the check should be done in the orchestrator, so don't include checks about isisntance
        if self.exists(contact):
            raise DuplicateContactError("Contact already exist")

        self.contacts[contact.id] = contact
        self._phone_idx[contact.phone_number] = contact.id

    def delete_contact(self, contact: Contact) -> None:
        if self.exists(contact):
            del self.contacts[contact.id]
            del self._phone_idx[contact.phone_number]

        # I need to adjust this function both here and in the orchestrator

    def update_contact(self, contact: Contact):
        # here I need to understand the logic better because I have to create another object. It's not responsibility of this function to use the search function, this function should only replace the object in the self.contacts dict
        # in the orchestrator I have to create something that handles all, the thingsa and in the ui I need to ask for confirmation
        # basically the logic behind is to replace the object 
        # user select the option, user reprompt the fields, user decide to save
        # basically I can use the add function and delete function and replace the object completely 
        ...


    def list_all_contacts(self) -> list[Contact]:
        # TODO: understand if checks like if self.contacts and eventually raising error have to be done here, do the same for search contact
        # TODO: check this function
        # TODO: sort contacts before returning the list, options (DONE) next TODO: understand if the sorting should happen here and where handling errors
        return [contact for contact in sorted(self.contacts.values(), key= lambda contact: contact.last_name)]

    def search_contact(self, search_term: str) -> list[Contact]:
        # TODO: check this function
        # alternatives: raise ContactNotFound here or raising it in the Orchestrator
        return [
            contact
            for contact in self.contacts.values()
            if search_term.lower() in contact.first_name.lower()
            or search_term in contact.last_name.lower()
        ]

    # before submitting, try to create another function that is the same but with different implementation and profile it, in the documentation write a python cell to compare those two function and demonstrate what is the most efficient and why.
    def exists(self, contact: Contact) -> bool:
        if not self._phone_idx:
            return False

        return contact.phone_number in self._phone_idx

        # TODO: Understand if NotFoundError should be raised in this function or in other function. I mean, I could do: if not exists: raise NotFound..

        # I need to define some rules for existence, that's because even if two contats have the same data, they don't result equals because the id is different

        # TODO: Need to define existence logic
        # Possible approach: define __eq__ and __hash__ inside the contact class and use it for comparison so id are different in case of contacts that have the same name but different data


if __name__ == "__main__":
    addressbook = AddressBook()
    john = Contact(
        first_name="John",
        last_name="Carmack",
        phone_number="+39 329 3892918",
        email="john@testcrud.com",
    )
    elon = Contact(
        first_name="Elon ",
        last_name="Musk",
        phone_number="+39 329 3892919",
        email="elon@testcrud.com",
    )
    steven = Contact(
        first_name="Steven",
        last_name="Lott",
        phone_number="+39 329 3892919",
        email="steven@testcrud.com",
    )

    peter = Contact(
        first_name="Peter",
        last_name="Parker",
        phone_number="+39 339 3892919",
        email="steven@testcrud.com",
    )

    addressbook.add_contact(john)
    addressbook.add_contact(elon)
    addressbook.add_contact(peter)

    contacts = addressbook.list_all_contacts()
    for contact in contacts:
        print(f"{contact.first_name} {contact.last_name}: {contact.phone_number}")

