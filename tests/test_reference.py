"""Smoke tests for the hand-written facade.

These cover the cross-cutting concerns the facade owns on top of the generated
model layer: project_id UUID validation and the project-scoped path factory
(exactly one `/projects/<project_id>/` prefix per resource).
"""

import pytest

from lunogram import Lunogram
from lunogram.utils.reference import client as Reference

PROJECT_ID = "11111111-2222-3333-4444-555555555555"
API_KEY = "test-key"


# --- UUID validation -------------------------------------------------------

def test_valid_uuid_accepted():
    ref = Reference(PROJECT_ID)
    assert ref.project_id == PROJECT_ID


@pytest.mark.parametrize("bad", ["", "not-a-uuid", "1234", None, 123])
def test_invalid_project_id_rejected(bad):
    with pytest.raises(ValueError):
        Reference(bad)


def test_client_validates_project_id():
    with pytest.raises(ValueError):
        Lunogram(api_key=API_KEY, project_id="nope")


# --- project-scoped path factory ------------------------------------------

ALL_PATHS = [
    ("user.base", lambda r: r.user.base),
    ("user.events", lambda r: r.user.events),
    ("user.scheduled", lambda r: r.user.scheduled),
    ("user.devices", lambda r: r.user.devices),
    ("user.inbox", lambda r: r.user.inbox),
    ("user.inbox_count", lambda r: r.user.inbox_count),
    ("user.inbox_read", lambda r: r.user.inbox_read),
    ("user.inbox_archived", lambda r: r.user.inbox_archived),
    ("organization.base", lambda r: r.organization.base),
    ("organization.events", lambda r: r.organization.events),
    ("organization.users", lambda r: r.organization.users),
    ("organization.scheduled", lambda r: r.organization.scheduled),
    ("organization.inbox", lambda r: r.organization.inbox),
    ("organization.inbox_count", lambda r: r.organization.inbox_count),
    ("organization.inbox_read", lambda r: r.organization.inbox_read),
    ("organization.inbox_archived", lambda r: r.organization.inbox_archived),
    ("push.vapid", lambda r: r.push.vapid),
    ("auth_methods.sessions", lambda r: r.auth_methods.sessions("aaaa")),
]


@pytest.mark.parametrize("name,getter", ALL_PATHS, ids=[n for n, _ in ALL_PATHS])
def test_exactly_one_project_prefix(name, getter):
    ref = Reference(PROJECT_ID)
    url = getter(ref)
    expected = f"/projects/{PROJECT_ID}/"
    # The load-bearing invariant: exactly one project-scoped prefix per resource.
    assert url.count(expected) == 1, f"{name}: expected exactly one prefix in {url!r}"
    assert f"/api/client/projects/{PROJECT_ID}/" in url
    # The endpoint joins cleanly — no doubled slash after the host.
    assert "//api/client/" not in url


def test_paths_are_under_client_api():
    ref = Reference(PROJECT_ID)
    assert ref.user.base.endswith(f"/projects/{PROJECT_ID}/users")
    assert ref.organization.events.endswith(f"/projects/{PROJECT_ID}/organizations/events")


def test_url_endpoint_override():
    ref = Reference(PROJECT_ID, "https://staging.example.com/api")
    assert ref.user.base == f"https://staging.example.com/api/client/projects/{PROJECT_ID}/users"


def test_default_endpoint():
    ref = Reference(PROJECT_ID)
    assert ref.user.base == f"https://console.lunogram.com/api/client/projects/{PROJECT_ID}/users"
