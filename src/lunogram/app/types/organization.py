from typing import TypedDict, NotRequired, Required
from identifier import Identifier


class OrganizationIdentifier(TypedDict):
    external_id: str
    metadata: NotRequired[None]
    source: str


class UpsertOrganizationScheduled(TypedDict):
    identifier: list[OrganizationIdentifier]
    name: Required[str]
    data: NotRequired[object]
    interval: NotRequired[str | None]
    scheduled_at: NotRequired[str | None]
    start_at: NotRequired[str | None]


class DeleteOrganizationScheduled(TypedDict):
    identifier: list[OrganizationIdentifier]
    name: Required[str]


class OrganizationEvent(TypedDict):
    identifier: list[OrganizationIdentifier]
    name: Required[str]
    data: NotRequired[object]
    match: NotRequired[object]