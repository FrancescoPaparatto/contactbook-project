from contacts import Contact
from addressbook import AddressBook

# orchestrator and addressbook should never render data, they should return data or raise exceptions
# orchestrator in particular is more about handling and catching exceptions rather than raising them


class Orchestrator:
    def __init__(self):
        self.is_dirty = False

    def create_contact(self, contact: list[Contact], addressbook: AddressBook):
        # Basically this function should modify a state, so it should first create and add the contact, then it should have some flag to say that there was a modification
        # I think this flag should be resetted after savings
        ...

    def show_contact(self): ...


# An example of function in the orchestrator
# I don't know if has sense
def create_contact(contact: Contact, addressbook: AddressBook) -> dict[str, bool]:
    addressbook.add_contact(contact)
    return {"OK": True, "ERR": False}


# This function has more sense becaue take as input the list of the contact and show them but I think that is a repetition or I have to create a function like get_contacts that has the list and use this list to show all
# the idea was to separe the retrieve from the show
# In the orchestrator I need a function to render the output because I need to use it both in the list_all and search methods, so those function should also have similar structure in order to re-use the same
def show_all_contacts(contacts: list[Contact]) -> None:
    for contact in contacts:
        print(f"""First name: {contact.first_name}""")
