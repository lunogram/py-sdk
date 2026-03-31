from typing import Literal
from app.http import httphandler
from utils.reference import client

entities = Literal["user", "organization"]

def upsert(api_key, data, entity: entities):
    handler = httphandler(api_key)

    match(entity):
        case 'user':
            req = handler.post(client.user.base, data)
        case 'organization':
            req = handler.post(client.organization.base, data)
    
    return req

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