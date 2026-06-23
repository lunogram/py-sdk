"""Smoke tests for the generated model layer and its use in the facade."""

from lunogram.app.objects import _serialize
from lunogram.gen.models import IdentifyRequest, Event


def test_generated_model_serializes_snake_case():
    # Python is snake_case end-to-end, matching the spec, so a generated model
    # dumps straight to the request body with no key-mapping layer.
    req = IdentifyRequest.model_validate(
        {
            "identifier": [{"source": "default", "external_id": "user_123"}],
            "email": "a@b.com",
        }
    )
    body = _serialize(req)
    assert body["identifier"][0]["external_id"] == "user_123"
    assert body["email"] == "a@b.com"
    # exclude_none drops unset optional fields
    assert "phone" not in body


def test_serialize_passes_dicts_through():
    data = {"name": "signed_in", "identifier": []}
    assert _serialize(data) is data


def test_event_model_fields():
    ev = Event.model_validate(
        {
            "name": "signed_in",
            "identifier": [{"source": "default", "external_id": "user_123"}],
            "data": {"plan": "pro"},
        }
    )
    assert ev.name == "signed_in"
    assert ev.data == {"plan": "pro"}
