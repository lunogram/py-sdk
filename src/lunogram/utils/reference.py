from uuid import UUID

url = "https://console.lunogram.com/"
api = "/api/client/"
destination = url + api

# Every authenticated Client API endpoint is scoped to a single project. The
# project UUID is supplied once when the Lunogram client is constructed and is
# injected here as a `/projects/<project_id>/` path segment, so callers never
# pass it per request.


def _validate_project_id(project_id: str) -> str:
    if not isinstance(project_id, str) or not project_id.strip():
        raise ValueError("project_id is required and must be a non-empty string")

    try:
        UUID(project_id)
    except (ValueError, AttributeError, TypeError):
        raise ValueError(f"project_id must be a valid UUID, got: {project_id!r}")

    return project_id


# API reference

class _user:
    def __init__(self, project: str):
        self.base = project + 'users'
        self.events = project + 'users/events'
        self.scheduled = project + 'users/scheduled'
        self.devices = project + 'users/devices'
        self.inbox = project + 'users/inbox'
        self.inbox_count = project + 'users/inbox/count'
        self.inbox_read = project + 'users/inbox/read'
        self.inbox_archived = project + 'users/inbox/archived'

class _org:
    def __init__(self, project: str):
        self.base = project + 'organizations'
        self.events = project + 'organizations/events'
        self.users = project + 'organizations/users'
        self.scheduled = project + 'organizations/scheduled'
        self.inbox = project + 'organizations/inbox'
        self.inbox_count = project + 'organizations/inbox/count'
        self.inbox_read = project + 'organizations/inbox/read'
        self.inbox_archived = project + 'organizations/inbox/archived'

class _push:
    def __init__(self, project: str):
        self.vapid = project + 'push/vapid'

class _auth_methods:
    def __init__(self, project: str):
        self._project = project

    def sessions(self, auth_method_id: str) -> str:
        return self._project + f'auth-methods/{auth_method_id}/sessions'

class client:
    def __init__(self, project_id: str):
        self.project_id = _validate_project_id(project_id)
        # e.g. https://console.lunogram.com/api/client/projects/<project_id>/
        project = destination + f'projects/{self.project_id}/'

        self.user = _user(project)
        self.organization = _org(project)
        self.push = _push(project)
        self.auth_methods = _auth_methods(project)
