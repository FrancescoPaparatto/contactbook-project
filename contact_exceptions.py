# TODO: this module should be checked again to understand if I have to write some code inside errror functions

# Notes about production code
# - in production don't show contact_exceptions.Error but handle in a better way


class ContactError(Exception):
    # this is the root class of my domain exceptions
    ...


class ContactValidationError(ContactError):
    # This is about fields error, in this case orchestrator reprompts specific fields
    ...


class InvalidEmailError(ContactValidationError): ...


class InvalidPhoneError(ContactValidationError): ...


class MissingRequiredFieldError(ContactValidationError): ...


class DuplicateContactError(ContactError):
    # this block add/edit and reprompt
    ...

class ContactNotFoundError(ContactError):
    # edit/delete target missing
    ...
