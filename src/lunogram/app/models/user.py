from .objects import events, scheduled
from ..http import httphandler

from ...utils.reference import client as reference_client
from ..types.user import *

class user:
    def __init__(self, api_key, reference: reference_client):
        self.reference = reference
        self.events = events(api_key, reference, entity='user')
        self.scheduled = scheduled(api_key, reference, entity='user')
        self.handler = httphandler(api_key)

    def upsert(self, data: UpsertUser):
        req = self.handler.post(self.reference.user.base, data)

        return req

    def delete(self, data: DeleteUser):
        req = self.handler.delete(self.reference.user.base, data)

        return req
