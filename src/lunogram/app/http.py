import json
import requests
from typing import Literal

http_methods = Literal["GET", "POST", "DELETE"]

# state of the art http handler
class httphandler:
    def __init__(self, api_key):
        self.api_key = api_key

    def request(self, method: http_methods, url, data=None, params=None):
        head = {
            'Content-Type': 'application/json',
            # The Client API authenticates with a JWT bearer token.
            'Authorization': f"Bearer {self.api_key}",
        }

        # Only send a JSON body when there is one; GET requests carry their
        # arguments as query params instead.
        body = None if data is None else json.dumps(data)
        req = requests.request(method, url, data=body, params=params, headers=head)

        if not (200 <= req.status_code < 300):
            return (req, f"HTTP {req.status_code}")

        # Many Client API endpoints accept work for async processing and reply
        # 202/204 with no body; treat an empty success body as success.
        if not req.content:
            return req

        try:
            return (req.json())
        except json.JSONDecodeError:
            return (req, "Response is not a JSON object")
        except Exception as e:
            return (req, e)

    def get(self, url: str, params=None):
        req = self.request("GET", url, params=params)

        return req

    def post(self, url: str, data):
        req = self.request("POST", url, data)

        return req

    def delete(self, url: str, data):
        req = self.request("DELETE", url, data)

        return req
