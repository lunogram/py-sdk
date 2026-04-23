from typing import TypedDict, Required, NotRequired
from identifier import Identifier

class UpsertScheduled(TypedDict):
    identifier: list[Identifier]
    name: Required[str]
    data: NotRequired[object]
    interval: NotRequired[str | None]
    scheduled_at: NotRequired[str | None]
    start_at: NotRequired[str | None]

class DeleteScheduled(TypedDict):
    name: Required[str]
    identifier: list[Identifier]