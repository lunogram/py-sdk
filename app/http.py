import json
import requests
from typing import Literal

http_methods = Literal["GET", "POST", "DELETE"]

class httphandler:
    def __init__(self, api_key):
        self.api_key = api_key

    def request(self, method: http_methods, url, data = None):
        head = {
            'Content-Type': 'application/json',
            'Authorization': f"{self.api_key}",
        }

        req = requests.request(method, url, data=data, headers=head)

        try:
            return (req.json())
        except json.JSONDecodeError:
            return (req, "Couldn't detect response as JSON")
        except:
            return (req, )
        
    def get(self, url: str):
        req = self.request("GET", url)
    
        return req
    
    def post(self, url: str, data):
        req = self.request("POST", url, data)

        return req
    
    def delete(self, url: str, data):
        req = self.request("DELETE", url, data)

        return req
