from typing import TypedDict, Required, NotRequired
from identifier import Identifier

class Event(TypedDict):
    identifier: list[Identifier]
    name: Required[str]
    data: NotRequired[object]
    match: NotRequired[object]