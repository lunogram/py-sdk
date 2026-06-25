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

## More resources

The same `Lunogram` client exposes the full Client API surface. Every method
accepts either a plain dict or the matching generated model from
`lunogram.gen.models`.

```python
# Inbox — users and organizations share the same surface
# (client.organization.inbox.* mirrors client.user.inbox.*)
client.user.inbox.create([
    {
        "target": [{"external_id": "user_123"}],
        "identifier": {"external_id": "msg-1"},
        "channel": "inbox",
        "content": {"title": "Welcome", "body": "Thanks for joining!"},
    },
])
messages = client.user.inbox.query(source="default", external_id="user_123", channel="inbox", status="unread")
counts = client.user.inbox.count(source="default", external_id="user_123", channel="inbox")
client.user.inbox.mark_read([{"target": [{"external_id": "user_123"}], "message_id": "msg-1"}])
client.user.inbox.mark_archived([{"target": [{"external_id": "user_123"}], "message_id": "msg-1"}])

# Organization membership
client.organization.add_user({
    "organization": {"identifier": [{"external_id": "org_123"}]},
    "user": {"identifier": [{"external_id": "user_123"}]},
})
client.organization.remove_user({
    "organization": {"identifier": [{"external_id": "org_123"}]},
    "user": {"identifier": [{"external_id": "user_123"}]},
})

# Devices & push
vapid = client.push.get_vapid_public_key()
client.user.devices.register({
    "identifier": [{"external_id": "user_123"}],
    "device_id": "device-1",
    "os": "web",
    "config": {"endpoint": "https://push.example.com/...", "keys": {"p256dh": "...", "auth": "..."}},
})

# Sessions — mint a short-lived token for an end user (server-side)
session = client.sessions.create("auth-method-uuid", {"user_id": "user_123"})
```

## Architecture: spec-driven, layered

The SDK is split into a **generated low-level layer** and a **hand-written
facade**:

| Layer | Location | How it's produced |
| --- | --- | --- |
| Models / payload types | `src/lunogram/gen/models.py` | **Generated** from the OpenAPI spec (Pydantic v2 models) |
| Facade (`Lunogram`, path factory, UUID validation, auth header, transport) | `src/lunogram/client.py`, `app/**`, `utils/reference.py` | **Hand-written** |

Cross-cutting concerns live in the facade in a single place: the
`/api/client/projects/{project_id}` prefix (in `utils/reference.py`) and the
`Bearer`-style auth header (in `app/http.py`). Resource methods never repeat the
project scoping.

Because Python is snake_case end-to-end — matching the spec — the generated
models flow straight through to the request body with **no camelCase↔snake_case
mapping layer**. A generated model and a plain dict are both accepted by every
method; models are dumped with `model_dump(mode="json", exclude_none=True)`.

### The spec is vendored from a platform release

`spec/client.yaml` is copied verbatim from a Lunogram platform **release**.
`spec/SOURCE.md` records the source repo, pinned tag and asset URL. Every tagged
release publishes the client OpenAPI spec as a `client.yaml` asset, so the spec
is fetched from a stable, versioned, immutable source. Bumping the pin is a
manual edit to `spec/SOURCE.md` followed by `make generate`.

### Regenerating the models

The generator is [`datamodel-code-generator`](https://github.com/koxudaxi/datamodel-code-generator)
(pinned in the `dev` extra). Install it and run the generate step:

```bash
make install      # pip install -e ".[dev]"
make generate     # ./scripts/generate.sh  ->  src/lunogram/gen/models.py
```

`scripts/generate.sh` is the single source of truth for the generator flags;
the `make generate` target and CI both call it. The output carries a
"`DO NOT EDIT`" header — never hand-edit it; change the spec (or the script) and
regenerate.

### CI

- **`ci.yml`** (push / PR, Python 3.12) — installs deps, regenerates, runs
  `git diff --exit-code src/lunogram/gen` as a **drift check** (fails if the
  committed generated code is stale), builds the wheel, import-smoke-tests, and
  runs `pytest`.
