from .objects import events, scheduled
from ..http import httphandler
from ..types.organization import *

from ...utils.reference import client as reference_client

class organization:
    def __init__(self, api_key, reference: reference_client):
        self.reference = reference
        self.events = events(api_key, reference, entity='organization')
        self.scheduled = scheduled(api_key, reference, entity='organization')
        self.handler = httphandler(api_key)

    def upsert(self, data: UpsertOrganization):
        req = self.handler.post(self.reference.organization.base, data)

        return req

    def delete(self, data: DeleteOrganization):
        req = self.handler.delete(self.reference.organization.base, data)

        return req
