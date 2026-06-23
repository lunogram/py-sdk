from typing import Literal, Union

from pydantic import BaseModel

from .http import httphandler
from ..utils.reference import client
from ..gen.models import (
    IdentifyRequest,
    DeleteUserRequest,
    OrganizationRequest,
    DeleteOrganizationRequest,
    Event,
    OrganizationEvent,
    UpsertUserScheduledRequest,
    UpsertOrganizationScheduledRequest,
    DeleteUserScheduledRequest,
    DeleteOrganizationScheduledRequest,
)

entities = Literal["user", "organization"]

# Request bodies accept either a generated Pydantic model or a plain dict.
Body = Union[BaseModel, dict]


def _serialize(data):
    # The generated models mirror the spec's snake_case payloads exactly, so a
    # model can be dumped straight to the JSON body with no key mapping. Plain
    # dicts are passed through unchanged.
    if isinstance(data, BaseModel):
        return data.model_dump(mode="json", exclude_none=True)
    return data


# .events and .scheduled objects are defined seperately and later integrated with the corresponding entities

class events:
    def __init__(self, api_key, reference: client, entity: entities):
        self.entity = entity
        self.reference = reference
        self.handler = httphandler(api_key)

    def post(self, data: Union[Event, OrganizationEvent, list, Body]):
        data = _serialize(data)
        match(self.entity):
            case 'user':
                req = self.handler.post(self.reference.user.events, data)
            case 'organization':
                req = self.handler.post(self.reference.organization.events, data)

        return req

class scheduled:
    def __init__(self, api_key, reference: client, entity: entities):
        self.entity = entity
        self.reference = reference
        self.handler = httphandler(api_key)

    def post(self, data: Union[UpsertUserScheduledRequest, UpsertOrganizationScheduledRequest, Body]):
        data = _serialize(data)
        match(self.entity):
            case 'user':
                req = self.handler.post(self.reference.user.scheduled, data)
            case 'organization':
                req = self.handler.post(self.reference.organization.scheduled, data)

        return req

    def delete(self, data: Union[DeleteUserScheduledRequest, DeleteOrganizationScheduledRequest, Body]):
        data = _serialize(data)
        match(self.entity):
            case 'user':
                req = self.handler.delete(self.reference.user.scheduled, data)
            case 'organization':
                req = self.handler.delete(self.reference.organization.scheduled, data)

        return req

class user:
    def __init__(self, api_key, reference: client):
        self.reference = reference
        self.events = events(api_key, reference, entity='user')
        self.scheduled = scheduled(api_key, reference, entity='user')
        self.handler = httphandler(api_key)

    def upsert(self, data: Union[IdentifyRequest, Body]):
        req = self.handler.post(self.reference.user.base, _serialize(data))

        return req

    def delete(self, data: Union[DeleteUserRequest, Body]):
        req = self.handler.delete(self.reference.user.base, _serialize(data))

        return req

class organization:
    def __init__(self, api_key, reference: client):
        self.reference = reference
        self.events = events(api_key, reference, entity='organization')
        self.scheduled = scheduled(api_key, reference, entity='organization')
        self.handler = httphandler(api_key)

    def upsert(self, data: Union[OrganizationRequest, Body]):
        req = self.handler.post(self.reference.organization.base, _serialize(data))

        return req

    def delete(self, data: Union[DeleteOrganizationRequest, Body]):
        req = self.handler.delete(self.reference.organization.base, _serialize(data))

        return req
