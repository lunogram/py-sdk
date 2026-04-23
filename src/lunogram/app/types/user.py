from typing import TypedDict, NotRequired, Required
from identifier import Identifier

class FirstLastName(TypedDict):
    first_name: str
    last_name: str

class UpsertUser(TypedDict):
    identifier: list[Identifier]
    data: list[FirstLastName]
    email: str
    locale: str
    phone: str
    timezone: str

class DeleteUser(TypedDict):
    Identifier: list[Identifier]