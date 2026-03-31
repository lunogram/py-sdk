from typing import Literal

from .http import httphandler
from ..utils.reference import client

entities = Literal["user", "organization"]

# .events and .scheduled objects are defined seperately and later integrated with the corresponding entities

class events:
    def __init__(self, api_key, entity: entities):
        self.entity = entity
        self.handler = httphandler(api_key)
    
    def post(self, data):
        match(self.entity):
            case 'user':
                req = self.handler.post(client.user.events, data)
            case 'organization':
                req = self.handler.post(client.organization.events, data)
        
        return req

class scheduled:
    def __init__(self, api_key, entity: entities):
        self.entity = entity
        self.handler = httphandler(api_key)

    def post(self, data):
        match(self.entity):
            case 'user':
                req = self.handler.post(client.user.scheduled, data)
            case 'organization':
                req = self.handler.post(client.organization.scheduled, data)

        return req
    
    def delete(self, data):
        match(self.entity):
            case 'user':
                req = self.handler.delete(client.user.scheduled, data)
            case 'organization':
                req = self.handler.delete(client.organization.scheduled, data)

        return req
    
class user:
    def __init__(self, api_key):
        self.events = events(api_key, entity='user')
        self.scheduled = scheduled(api_key, entity='user')
        self.handler = httphandler(api_key)

    def upsert(self, data):
        req = self.handler.post(client.user.base, data)

        return req

    def delete(self, data):
        req = self.handler.delete(client.user.base, data)

        return req

class organization:
    def __init__(self, api_key):
        self.events = events(api_key, entity='organization')
        self.scheduled = scheduled(api_key, entity='organization')
        self.handler = httphandler(api_key)

    def upsert(self, data):
        req = self.handler.post(client.organization.base, data)

        return req
    
    def delete(self, data):
        req = self.handler.delete(client.organization.base, data)

        return req