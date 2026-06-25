from uuid import UUID

# Default Client API endpoint. Includes the `/api` prefix; the `/client/...`
# path is appended onto it. Override per-client with `url_endpoint` (e.g. to
# point at a staging environment) — the same role as the JS SDK's `urlEndpoint`.
DEFAULT_ENDPOINT = "https://console.lunogram.com/api"

# Every authenticated Client API endpoint is scoped to a single project. The
# project UUID is supplied once when the Lunogram client is constructed and is
# injected here as a `/projects/<project_id>/` path segment, so callers never
# pass it per request.


def _client_base(url_endpoint: str | None) -> str:
    # The Client API always lives under `/api/client/...`. Accept the endpoint
    # with or without a trailing `/api` (mirrors the JS SDK's `urlEndpoint`
    # handling) and always re-add it, so the resource paths join cleanly with no
    # missing or doubled segments.
    endpoint = (url_endpoint or DEFAULT_ENDPOINT).rstrip("/")
    if endpoint.endswith("/api"):
        endpoint = endpoint[: -len("/api")]
    return f"{endpoint}/api/client/"


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
    def __init__(self, project_id: str, url_endpoint: str | None = None):
        self.project_id = _validate_project_id(project_id)
        # e.g. https://console.lunogram.com/api/client/projects/<project_id>/
        project = _client_base(url_endpoint) + f'projects/{self.project_id}/'

        self.user = _user(project)
        self.organization = _org(project)
        self.push = _push(project)
        self.auth_methods = _auth_methods(project)
