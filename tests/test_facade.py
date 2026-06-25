"""Facade tests: verify each resource hits the right method/URL/body.

These mock the underlying ``requests.request`` so no network is involved, and
assert the cross-cutting concerns the facade owns: the Bearer auth header, the
project-scoped paths, snake_case query params, and model/dict body serialization.
"""

import json
from unittest.mock import patch, MagicMock

import pytest

from lunogram import Lunogram
from lunogram.gen.models import CreateSession, IdentifyRequest

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


def test_user_crud_and_events(captured):
    client = Lunogram(API_KEY, PROJECT_ID)

    client.user.upsert({"identifier": [{"external_id": "u"}], "email": "a@b.com"})
    assert last(captured)["method"] == "POST"
    assert last(captured)["url"].endswith(f"{PREFIX}users")

    client.user.delete({"identifier": [{"external_id": "u"}]})
    assert last(captured)["method"] == "DELETE"
    assert last(captured)["url"].endswith(f"{PREFIX}users")

    client.user.events.post([{"name": "evt", "identifier": [{"external_id": "u"}], "data": {}}])
    assert last(captured)["method"] == "POST"
    assert last(captured)["url"].endswith(f"{PREFIX}users/events")


def test_user_scheduled(captured):
    client = Lunogram(API_KEY, PROJECT_ID)

    client.user.scheduled.post({"name": "r", "identifier": [{"external_id": "u"}]})
    assert last(captured)["method"] == "POST"
    assert last(captured)["url"].endswith(f"{PREFIX}users/scheduled")

    client.user.scheduled.delete({"name": "r", "identifier": [{"external_id": "u"}]})
    assert last(captured)["method"] == "DELETE"
    assert last(captured)["url"].endswith(f"{PREFIX}users/scheduled")


def test_organization_crud_events_scheduled(captured):
    client = Lunogram(API_KEY, PROJECT_ID)

    client.organization.upsert({"identifier": [{"external_id": "o"}], "name": "Acme"})
    assert last(captured)["method"] == "POST"
    assert last(captured)["url"].endswith(f"{PREFIX}organizations")

    client.organization.delete({"identifier": [{"external_id": "o"}]})
    assert last(captured)["method"] == "DELETE"
    assert last(captured)["url"].endswith(f"{PREFIX}organizations")

    client.organization.events.post([{"name": "evt", "identifier": [{"external_id": "o"}]}])
    assert last(captured)["url"].endswith(f"{PREFIX}organizations/events")

    client.organization.scheduled.post({"name": "s", "identifier": [{"external_id": "o"}]})
    assert last(captured)["method"] == "POST"
    assert last(captured)["url"].endswith(f"{PREFIX}organizations/scheduled")

    client.organization.scheduled.delete({"name": "s", "identifier": [{"external_id": "o"}]})
    assert last(captured)["method"] == "DELETE"
    assert last(captured)["url"].endswith(f"{PREFIX}organizations/scheduled")


def test_organization_inbox_write_endpoints(captured):
    client = Lunogram(API_KEY, PROJECT_ID)

    client.organization.inbox.create([
        {"target": [{"external_id": "o"}], "identifier": {"external_id": "m1"}, "channel": "inbox"},
    ])
    assert last(captured)["url"].endswith(f"{PREFIX}organizations/inbox")

    client.organization.inbox.count(source="default", external_id="o", channel="inbox")
    assert last(captured)["url"].endswith(f"{PREFIX}organizations/inbox/count")

    client.organization.inbox.mark_read([{"target": [{"external_id": "o"}], "message_id": "m1"}])
    assert last(captured)["url"].endswith(f"{PREFIX}organizations/inbox/read")

    client.organization.inbox.mark_archived([{"target": [{"external_id": "o"}], "message_id": "m1"}])
    assert last(captured)["url"].endswith(f"{PREFIX}organizations/inbox/archived")


def test_upsert_accepts_a_generated_model(captured):
    client = Lunogram(API_KEY, PROJECT_ID)
    client.user.upsert(IdentifyRequest.model_validate({
        "identifier": [{"source": "default", "external_id": "u"}],
        "email": "a@b.com",
    }))
    body = json.loads(last(captured)["data"])
    assert body["identifier"][0]["external_id"] == "u"
    assert body["email"] == "a@b.com"
    # exclude_none drops unset optional fields
    assert "phone" not in body


def test_empty_2xx_response_is_treated_as_success():
    # Async endpoints reply 202/204 with no body; that must not surface as the
    # "(response, error)" failure tuple.
    def fake_request(method, url, data=None, params=None, headers=None):
        resp = MagicMock()
        resp.status_code = 202
        resp.content = b""
        return resp

    with patch("lunogram.app.http.requests.request", side_effect=fake_request):
        client = Lunogram(API_KEY, PROJECT_ID)
        result = client.user.events.post([{"name": "e", "identifier": [{"external_id": "u"}], "data": {}}])
        assert not isinstance(result, tuple)
        assert result.status_code == 202
