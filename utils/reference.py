url = "https://console.lab.lunogram.io/"
api = "/api/client/"
destination = url + api

class _user:
    base = destination + 'users'
    events = destination + 'users/events'
    scheduled = destination + 'users/scheduled'

class _org:
    base = destination + 'organizations'
    events = destination + 'organizations/events'
    users = destination + 'organizations/users'
    scheduled = destination + 'organizations/scheduled'

class client:
    user = _user()
    organization = _org()