from typing import Literal

from ..http import httphandler
from ...utils.reference import client as reference_client, default_client

from src.lunogram.app.types.event import *
from src.lunogram.app.types.scheduled import *

entities = Literal["user", "organization"]

# .events and .scheduled objects are defined seperately and later integrated with the corresponding entities

class events:
    def __init__(self, api_key, entity: entities, reference: reference_client | None = None):
        self.entity = entity
        self.reference = reference or default_client
        self.handler = httphandler(api_key)
    
    def post(self, data: Event):
        match(self.entity):
            case 'user':
                req = self.handler.post(self.reference.user.events, data)
            case 'organization':
                req = self.handler.post(self.reference.organization.events, data)
        
        return req

class scheduled:
    def __init__(self, api_key, entity: entities, reference: reference_client | None = None):
        self.entity = entity
        self.reference = reference or default_client
        self.handler = httphandler(api_key)

    def post(self, data: UpsertScheduled):
        match(self.entity):
            case 'user':
                req = self.handler.post(self.reference.user.scheduled, data)
            case 'organization':
                req = self.handler.post(self.reference.organization.scheduled, data)

        return req
    
    def delete(self, data: DeleteScheduled):
        match(self.entity):
            case 'user':
                req = self.handler.delete(self.reference.user.scheduled, data)
            case 'organization':
                req = self.handler.delete(self.reference.organization.scheduled, data)

        return req