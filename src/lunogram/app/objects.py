from typing import Literal, Union

from pydantic import BaseModel

from .http import httphandler
from ..utils.reference import client
from ..gen.models import (
    Channel,
    IdentifyRequest,
    DeleteUserRequest,
    OrganizationRequest,
    DeleteOrganizationRequest,
    OrganizationUserRequest,
    RemoveOrganizationUserRequest,
    Event,
    OrganizationEvent,
    UpsertUserScheduledRequest,
    UpsertOrganizationScheduledRequest,
    DeleteUserScheduledRequest,
    DeleteOrganizationScheduledRequest,
    InboxMessageCreate,
    OrganizationInboxMessageCreate,
    UserInboxMessageRef,
    OrganizationInboxMessageRef,
    DeviceRegistration,
    CreateSession,
)

entities = Literal["user", "organization"]

# Request bodies accept either a generated Pydantic model or a plain dict.
Body = Union[BaseModel, dict]


def _serialize(data):
    # The generated models mirror the spec's snake_case payloads exactly, so a
    # model can be dumped straight to the JSON body with no key mapping. Lists
    # are serialized element-wise (array request bodies), and plain dicts are
    # passed through unchanged.
    if isinstance(data, BaseModel):
        return data.model_dump(mode="json", exclude_none=True)
    if isinstance(data, list):
        return [_serialize(item) for item in data]
    return data


def _prune(params: dict) -> dict:
    # Drop unset query parameters so they never reach the query string.
    return {key: value for key, value in params.items() if value is not None}


def _channel(channel) -> str:
    # Accept either the generated Channel enum or a plain string.
    return channel.value if isinstance(channel, Channel) else channel


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


class inbox:
    def __init__(self, api_key, reference: client, entity: entities):
        self.entity = entity
        self.reference = reference
        self.handler = httphandler(api_key)

    def _ref(self):
        return self.reference.user if self.entity == 'user' else self.reference.organization

    def create(self, messages: Union[list, Body]):
        return self.handler.post(self._ref().inbox, _serialize(messages))

    def query(self, source, external_id, channel, status=None, tags=None,
              message_source=None, priority=None, limit=None, offset=None):
        params = _prune({
            'source': source,
            'external_id': external_id,
            'channel': _channel(channel),
            'status': status,
            'tags': tags,
            'message_source': message_source,
            'priority': priority,
            'limit': limit,
            'offset': offset,
        })
        return self.handler.get(self._ref().inbox, params=params)

    def count(self, source, external_id, channel):
        params = _prune({
            'source': source,
            'external_id': external_id,
            'channel': _channel(channel),
        })
        return self.handler.get(self._ref().inbox_count, params=params)

    def mark_read(self, messages: Union[list, Body]):
        return self.handler.post(self._ref().inbox_read, _serialize(messages))

    def mark_archived(self, messages: Union[list, Body]):
        return self.handler.post(self._ref().inbox_archived, _serialize(messages))


class devices:
    def __init__(self, api_key, reference: client):
        self.reference = reference
        self.handler = httphandler(api_key)

    def register(self, data: Union[DeviceRegistration, Body]):
        return self.handler.post(self.reference.user.devices, _serialize(data))


class push:
    def __init__(self, api_key, reference: client):
        self.reference = reference
        self.handler = httphandler(api_key)

    def get_vapid_public_key(self):
        return self.handler.get(self.reference.push.vapid)


class sessions:
    def __init__(self, api_key, reference: client):
        self.reference = reference
        self.handler = httphandler(api_key)

    def create(self, auth_method_id: str, data: Union[CreateSession, Body]):
        url = self.reference.auth_methods.sessions(auth_method_id)
        return self.handler.post(url, _serialize(data))


class user:
    def __init__(self, api_key, reference: client):
        self.reference = reference
        self.events = events(api_key, reference, entity='user')
        self.scheduled = scheduled(api_key, reference, entity='user')
        self.inbox = inbox(api_key, reference, entity='user')
        self.devices = devices(api_key, reference)
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
        self.inbox = inbox(api_key, reference, entity='organization')
        self.handler = httphandler(api_key)

    def upsert(self, data: Union[OrganizationRequest, Body]):
        req = self.handler.post(self.reference.organization.base, _serialize(data))

        return req

    def delete(self, data: Union[DeleteOrganizationRequest, Body]):
        req = self.handler.delete(self.reference.organization.base, _serialize(data))

        return req

    def add_user(self, data: Union[OrganizationUserRequest, Body]):
        req = self.handler.post(self.reference.organization.users, _serialize(data))

        return req

    def remove_user(self, data: Union[RemoveOrganizationUserRequest, Body]):
        req = self.handler.delete(self.reference.organization.users, _serialize(data))

        return req
