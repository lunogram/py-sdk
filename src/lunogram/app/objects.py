from typing import Literal

from .http import httphandler
from ..utils.reference import client

entities = Literal["user", "organization"]

# .events and .scheduled objects are defined seperately and later integrated with the corresponding entities

class events:
    def __init__(self, api_key, reference: client, entity: entities):
        self.entity = entity
        self.reference = reference
        self.handler = httphandler(api_key)

    def post(self, data):
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

    def post(self, data):
        match(self.entity):
            case 'user':
                req = self.handler.post(self.reference.user.scheduled, data)
            case 'organization':
                req = self.handler.post(self.reference.organization.scheduled, data)

        return req

    def delete(self, data):
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

    def upsert(self, data):
        req = self.handler.post(self.reference.user.base, data)

        return req

    def delete(self, data):
        req = self.handler.delete(self.reference.user.base, data)

        return req

class organization:
    def __init__(self, api_key, reference: client):
        self.reference = reference
        self.events = events(api_key, reference, entity='organization')
        self.scheduled = scheduled(api_key, reference, entity='organization')
        self.handler = httphandler(api_key)

    def upsert(self, data):
        req = self.handler.post(self.reference.organization.base, data)

        return req

    def delete(self, data):
        req = self.handler.delete(self.reference.organization.base, data)

        return req
