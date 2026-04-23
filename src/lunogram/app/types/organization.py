from typing import TypedDict, NotRequired, Required
from identifier import Identifier

class UpsertOrganization(TypedDict):
    identifier: list[Identifier]
    data: NotRequired[object | None]
    name: NotRequired[str | None]

class DeleteOrganization(TypedDict):
    identifier: list[Identifier]