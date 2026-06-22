# Lunogram Python SDK

Python SDK for the Lunogram Client API.

## Installation

```bash
pip install lunogram-sdk
```

## Usage

Every authenticated Client API endpoint is scoped to a **project**. You supply
the project UUID **once**, when constructing the client, and the SDK injects it
into every request path automatically. You never pass the project per call.

```python
from lunogram import Lunogram, random_user

client = Lunogram(
    api_key="your-api-key",
    project_id="11111111-2222-3333-4444-555555555555",  # your project UUID
)

# Upsert a user
result = client.user.upsert(random_user())
print(result[0])  # API response

# Send a user event
client.user.events.post({
    "identifier": [{"source": "default", "external_id": "user_123"}],
    "name": "signed_in",
})

# Organizations work the same way
client.organization.upsert({
    "identifier": [{"source": "default", "external_id": "org_123"}],
    "name": "Acme Inc.",
})
```

> All SDK actions return a tuple: the API response on index `0`, and a possible
> error on index `1`.

## Project-scoped URLs

As of this release, every Client API path includes the project UUID as a path
segment:

```
/api/client/projects/<project_id>/...
```

| Resource | Path (under `/api/client/projects/<project_id>/`) |
| --- | --- |
| Users | `users` |
| User events | `users/events` |
| User scheduled | `users/scheduled` |
| User devices | `users/devices` |
| User inbox | `users/inbox` (`/count`, `/read`, `/archived`) |
| Organizations | `organizations` |
| Organization users | `organizations/users` |
| Organization events | `organizations/events` |
| Organization scheduled | `organizations/scheduled` |
| Organization inbox | `organizations/inbox` (`/count`, `/read`, `/archived`) |
| Push VAPID | `push/vapid` |
| Auth method sessions | `auth-methods/<auth_method_id>/sessions` |

Authentication is unchanged — the same API key / token is used. Only the URL
gained the project segment.
