# now I will understand how to structure the code
# the idea is:
# - first implement the simplest version of the program
# - then improve it by adding some checks
# - then looks for data integrity and security

import os
import json
from typing import Dict, Protocol
from contact_exceptions import StorageError, FileCorruptionError


class Storage(Protocol):
    # TODO: add type hints for return values
    def save(self, data: Dict[str, dict], path: str): ...
    def load(self, path: str) -> Dict[str, dict]: ...
    def rotate_backups(self): ...


class JsonStorage:
    # I need to understand if a dict[str, dict] is the best way to do that
    def save(self, data: Dict[str, dict], path: str) -> None:

        if not path:
            raise StorageError("Save path is empty.")

        # ensure the directory exists
        dirpath = os.path.dirname(path) or "."

        try:
            os.makedirs(dirpath, exist_ok=True)
            # first open a file and then in that file write data
            with open(path, "w") as file:
                json.dump(data, file, indent=4)

        except Exception as e:
            raise StorageError(f"Could not save the file to'{path}': {e}") from e

    def load(self, path: str) -> Dict[str, dict]: 
        if not os.path.isfile(path):
            raise StorageError("Invalid path.")
        
        with open(path, "r") as contacts_file:
            contacts = json.load(contacts_file)

        return contacts






    def rotate_backups(self): ...
