from contacts import Contact  

class AddressBook:
    def __init__(self):
        self.contacts = {}

    def add_contact(self, contact: Contact) -> None:
        # TODO: understand if the check isinstance is ok here instead of doing it in the orchestrator and also if is necessary since I checked with type hint 

        if not isinstance(contact, Contact):
            raise ValueError("Invalid input")

        self.contacts[contact.id] = contact

    def update_contact(self):
        pass


    def list_all_contacts(self):
        pass


    def search_contact(self):
        pass

    def exists(self, contact: Contact) -> bool:
        return True if contact in self.contacts.values() else False


