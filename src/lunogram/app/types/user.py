from typing import TypedDict, NotRequired, Required
from identifier import Identifier

class FirstLastName(TypedDict):
    first_name: str
    last_name: str

class propertyName(TypedDict):
    propertyName: any

class UpsertUser(TypedDict):
    identifier: list[Identifier]
    data: list[FirstLastName]
    email: str
    locale: str
    phone: str
    timezone: str

class DeleteUser(TypedDict):
    Identifier: list[Identifier]

class UserEvents(TypedDict):
    identifier: list[Identifier]
    name: Required[str]
    data: object[propertyName]
    match: object[propertyName]

class UpsertUserScheduled(TypedDict):
    name: Required[str]
    data: NotRequired[object[propertyName]]
    identifier: list[Identifier]
    interval: NotRequired[str | None]
    scheduled_at: NotRequired[str | None]
    start_at: NotRequired[str | None]

class DeleteUserScheduled(TypedDict):
    name: Required[str]
    identifier: list[Identifier]