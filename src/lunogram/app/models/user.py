from objects import events, scheduled
from ..http import httphandler

from ...utils.reference import client
from src.lunogram.app.types.user import *

class user:
    def __init__(self, api_key):
        self.events = events(api_key, entity='user')
        self.scheduled = scheduled(api_key, entity='user')
        self.handler = httphandler(api_key)

    def upsert(self, data: UpsertUser):
        req = self.handler.post(client.user.base, data)

        return req

    def delete(self, data: DeleteUser):
        req = self.handler.delete(client.user.base, data)

        return req