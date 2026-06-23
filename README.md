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

### The spec is vendored (no platform release needed)

`spec/client.yaml` is copied verbatim from the platform repo at a **pinned
commit**. `spec/SOURCE.md` records the source repo, spec path and ref. Pinning to
a commit means any ref is fetchable from the public repo via the raw URL, so no
platform release is required (flip to a `v*.*.*` tag once the platform cuts one).

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
- **`spec-sync.yml`** (weekly cron + manual dispatch) — re-fetches the spec from
  the ref in `spec/SOURCE.md`, regenerates, and opens a PR via
  `peter-evans/create-pull-request` when anything changed.
