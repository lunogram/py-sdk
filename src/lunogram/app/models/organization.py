from src.lunogram.app.models.objects import events, scheduled
from src.lunogram.app.http import httphandler
from src.lunogram.app.types.organization import *

from ...utils.reference import client

class organization:
    def __init__(self, api_key):
        self.events = events(api_key, entity='organization')
        self.scheduled = scheduled(api_key, entity='organization')
        self.handler = httphandler(api_key)

    def upsert(self, data: UpsertOrganization):
        req = self.handler.post(client.organization.base, data)

        return req
    
    def delete(self, data: DeleteOrganization):
        req = self.handler.delete(client.organization.base, data)

        return req