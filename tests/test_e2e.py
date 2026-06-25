"""Live integration tests against a real Lunogram Client API.

Mirrors the JS SDK's e2e suite. These run only when live credentials are
configured (``LUNOGRAM_API_KEY`` + ``LUNOGRAM_PROJECT_ID``); otherwise the whole
module is skipped, so the regular unit `pytest` run stays offline and green. The
dedicated `e2e.yml` workflow supplies the secrets.
"""

import os
import time
from datetime import datetime, timedelta, timezone

import pytest

from lunogram import Lunogram

API_KEY = os.environ.get("LUNOGRAM_API_KEY")
PROJECT_ID = os.environ.get("LUNOGRAM_PROJECT_ID")
API_URL = os.environ.get("LUNOGRAM_API_URL")

pytestmark = pytest.mark.skipif(
    not (API_KEY and PROJECT_ID),
    reason="live credentials (LUNOGRAM_API_KEY, LUNOGRAM_PROJECT_ID) not configured",
)

_STAMP = int(time.time())
USER_ID = f"test-user-{_STAMP}"
ORG_ID = f"test-org-{_STAMP}"


def _future(days: int) -> str:
    return (datetime.now(timezone.utc) + timedelta(days=days)).isoformat().replace("+00:00", "Z")


@pytest.fixture(scope="module")
def client():
    return Lunogram(API_KEY, PROJECT_ID, API_URL)


def ok(result):
    # The facade returns the parsed JSON body (dict) or a Response on success,
    # and a ``(response, error)`` tuple on failure. Fail loudly with the
    # server's response body to make the reason debuggable.
    if isinstance(result, tuple):
        response, error = result[0], result[1]
        body = getattr(response, "text", "")
        url = getattr(response, "url", "?")
        history = getattr(response, "history", [])
        sent = getattr(response, "request", None)
        auth_sent = bool(sent and sent.headers.get("Authorization")) if sent else None
        raise AssertionError(
            f"request failed: {error} — url={url} redirects={len(history)} "
            f"auth_sent={auth_sent} — {body[:400]}"
        )
    return result


# --- Users -----------------------------------------------------------------

def test_upsert_user(client):
    user = ok(client.user.upsert({
        "identifier": [{"external_id": USER_ID}],
        "email": f"{USER_ID}@test.example.com",
        "data": {"first_name": "Test", "last_name": "User"},
    }))
    assert user["id"]
    assert user["email"] == f"{USER_ID}@test.example.com"


def test_upsert_user_with_multiple_identifiers(client):
    user = ok(client.user.upsert({
        "identifier": [
            {"external_id": USER_ID},
            {"source": "test-suite", "external_id": f"suite-{USER_ID}"},
        ],
        "data": {"has_completed_onboarding": True},
    }))
    assert len(user["identifier"]) >= 2


def test_post_user_events(client):
    ok(client.user.events.post([
        {"name": "test_event", "identifier": [{"external_id": USER_ID}], "data": {"source": "integration_test"}},
    ]))


def test_upsert_user_scheduled(client):
    scheduled = ok(client.user.scheduled.post({
        "name": "test_reminder",
        "identifier": [{"external_id": USER_ID}],
        "scheduled_at": _future(7),
        "data": {"reason": "integration_test"},
    }))
    assert scheduled["name"] == "test_reminder"


def test_delete_user_scheduled(client):
    ok(client.user.scheduled.delete({
        "name": "test_reminder",
        "identifier": [{"external_id": USER_ID}],
    }))


# --- Organizations ---------------------------------------------------------

def test_upsert_organization(client):
    org = ok(client.organization.upsert({
        "identifier": [{"external_id": ORG_ID}],
        "name": "Test Organization",
        "data": {"industry": "testing"},
    }))
    assert org["id"]
    assert org["name"] == "Test Organization"


def test_add_user_to_organization(client):
    ok(client.organization.add_user({
        "organization": {"identifier": [{"external_id": ORG_ID}]},
        "user": {"identifier": [{"external_id": USER_ID}]},
        "data": {"role": "admin"},
    }))


def test_post_organization_events(client):
    ok(client.organization.events.post([
        {"identifier": [{"external_id": ORG_ID}], "name": "test_org_event", "data": {"source": "integration_test"}},
    ]))


def test_upsert_organization_scheduled(client):
    scheduled = ok(client.organization.scheduled.post({
        "name": "test_contract_renewal",
        "identifier": [{"external_id": ORG_ID}],
        "scheduled_at": _future(30),
    }))
    assert scheduled["name"] == "test_contract_renewal"


def test_delete_organization_scheduled(client):
    ok(client.organization.scheduled.delete({
        "name": "test_contract_renewal",
        "identifier": [{"external_id": ORG_ID}],
    }))


def test_remove_user_from_organization(client):
    ok(client.organization.remove_user({
        "organization": {"identifier": [{"external_id": ORG_ID}]},
        "user": {"identifier": [{"external_id": USER_ID}]},
    }))


# --- Cleanup ---------------------------------------------------------------

def test_delete_organization(client):
    ok(client.organization.delete({"identifier": [{"external_id": ORG_ID}]}))


def test_delete_user(client):
    ok(client.user.delete({"identifier": [{"external_id": USER_ID}]}))
