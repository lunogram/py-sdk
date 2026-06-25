"""Facade tests: verify each resource hits the right method/URL/body.

These mock the underlying ``requests.request`` so no network is involved, and
assert the cross-cutting concerns the facade owns: the Bearer auth header, the
project-scoped paths, snake_case query params, and model/dict body serialization.
"""

import json
from unittest.mock import patch, MagicMock

import pytest

from lunogram import Lunogram
from lunogram.gen.models import CreateSession

PROJECT_ID = "11111111-2222-3333-4444-555555555555"
API_KEY = "test-key"
PREFIX = f"/projects/{PROJECT_ID}/"


@pytest.fixture
def captured():
    calls = []

    def fake_request(method, url, data=None, params=None, headers=None):
        calls.append({
            "method": method,
            "url": url,
            "data": data,
            "params": params,
            "headers": headers,
        })
        resp = MagicMock()
        resp.status_code = 200
        resp.content = b"{}"
        resp.json.return_value = {}
        return resp

    with patch("lunogram.app.http.requests.request", side_effect=fake_request):
        yield calls


def last(captured):
    return captured[-1]


def test_sends_bearer_auth_header(captured):
    client = Lunogram(API_KEY, PROJECT_ID)
    client.user.upsert({"identifier": [{"external_id": "u"}]})
    assert last(captured)["headers"]["Authorization"] == f"Bearer {API_KEY}"


def test_user_inbox_endpoints(captured):
    client = Lunogram(API_KEY, PROJECT_ID)

    client.user.inbox.create([
        {"target": [{"external_id": "u"}], "identifier": {"external_id": "m1"}, "channel": "inbox"},
    ])
    assert last(captured)["method"] == "POST"
    assert last(captured)["url"].endswith(f"{PREFIX}users/inbox")

    client.user.inbox.query(source="default", external_id="u", channel="inbox", message_source="campaign")
    assert last(captured)["method"] == "GET"
    assert last(captured)["url"].endswith(f"{PREFIX}users/inbox")
    assert last(captured)["params"]["external_id"] == "u"
    assert last(captured)["params"]["message_source"] == "campaign"
    # unset optionals are pruned from the query string
    assert "status" not in last(captured)["params"]

    client.user.inbox.count(source="default", external_id="u", channel="inbox")
    assert last(captured)["url"].endswith(f"{PREFIX}users/inbox/count")

    client.user.inbox.mark_read([{"target": [{"external_id": "u"}], "message_id": "m1"}])
    assert last(captured)["method"] == "POST"
    assert last(captured)["url"].endswith(f"{PREFIX}users/inbox/read")

    client.user.inbox.mark_archived([{"target": [{"external_id": "u"}], "message_id": "m1"}])
    assert last(captured)["url"].endswith(f"{PREFIX}users/inbox/archived")


def test_user_device_registration(captured):
    client = Lunogram(API_KEY, PROJECT_ID)
    client.user.devices.register({
        "identifier": [{"external_id": "u"}],
        "device_id": "device-1",
        "config": {"token": "tok"},
    })
    assert last(captured)["method"] == "POST"
    assert last(captured)["url"].endswith(f"{PREFIX}users/devices")


def test_organization_membership_and_inbox(captured):
    client = Lunogram(API_KEY, PROJECT_ID)

    client.organization.add_user({
        "organization": {"identifier": [{"external_id": "o"}]},
        "user": {"identifier": [{"external_id": "u"}]},
    })
    assert last(captured)["method"] == "POST"
    assert last(captured)["url"].endswith(f"{PREFIX}organizations/users")

    client.organization.remove_user({
        "organization": {"identifier": [{"external_id": "o"}]},
        "user": {"identifier": [{"external_id": "u"}]},
    })
    assert last(captured)["method"] == "DELETE"
    assert last(captured)["url"].endswith(f"{PREFIX}organizations/users")

    client.organization.inbox.query(source="default", external_id="o", channel="inbox")
    assert last(captured)["url"].endswith(f"{PREFIX}organizations/inbox")


def test_push_vapid_public_key(captured):
    client = Lunogram(API_KEY, PROJECT_ID)
    client.push.get_vapid_public_key()
    assert last(captured)["method"] == "GET"
    assert last(captured)["url"].endswith(f"{PREFIX}push/vapid")


def test_session_minting(captured):
    client = Lunogram(API_KEY, PROJECT_ID)
    client.sessions.create("auth-method-1", {"user_id": "user-1"})
    assert last(captured)["method"] == "POST"
    assert last(captured)["url"].endswith(f"{PREFIX}auth-methods/auth-method-1/sessions")
    assert json.loads(last(captured)["data"]) == {"user_id": "user-1"}


def test_session_minting_accepts_a_generated_model(captured):
    client = Lunogram(API_KEY, PROJECT_ID)
    client.sessions.create("auth-method-1", CreateSession(user_id="user-1"))
    assert json.loads(last(captured)["data"]) == {"user_id": "user-1"}
