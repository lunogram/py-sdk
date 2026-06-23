# The `gen` package holds code generated from the vendored OpenAPI spec
# (`spec/client.yaml`). Do not hand-edit; run `make generate` to regenerate.
from . import models  # noqa: F401

__all__ = ["models"]
