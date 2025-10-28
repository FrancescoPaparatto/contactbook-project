# TODO: this module should be checked again to understand if I have to write some code inside errror functions

# Notes about production code
# - in production don't show contact_exceptions.Error but handle in a better way


class ContactError(Exception):
    # this is the root class of my domain exceptions
    pass

class ContactValidationError(ContactError, ValueError):
    # This is about fields error, in this case orchestrator reprompts specific fields
    pass


class InvalidEmailError(ContactValidationError):
    pass


class InvalidPhoneError(ContactValidationError):
    pass


class MissingRequiredFieldError(ContactValidationError):
    pass


class DuplicateContactError(ContactError):
    # this block add/edit and reprompt
    pass


class NotFoundError(ContactError):
    # edit/delete target missing
    pass
