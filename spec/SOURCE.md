# Spec source

`client.yaml` in this directory is **vendored** (copied verbatim) from a Lunogram
platform **release**. It is the single input to the code generator
(`make generate` → `src/lunogram/gen/models.py`). Do not hand-edit either file.

| | |
| --- | --- |
| Source repo | https://github.com/lunogram/platform |
| Pinned tag | `v0.1.0-rc.2` |
| Spec asset | `client.yaml` |

Every tagged platform release publishes the client OpenAPI spec as a `client.yaml`
asset (see the platform's `.github/workflows/release.yml` → `openapi-specs` job),
so the spec is fetched from a stable, versioned, immutable source — no platform
checkout or branch pin required.

## Release asset URL

```
https://github.com/lunogram/platform/releases/download/v0.1.0-rc.2/client.yaml
```

## Refreshing the spec

To track a newer release, update the **Pinned tag** above and re-fetch:

```bash
TAG=v0.1.0-rc.2
curl -fsSL "https://github.com/lunogram/platform/releases/download/$TAG/client.yaml" -o spec/client.yaml
make generate
```

Commit `spec/client.yaml` and `src/lunogram/gen/models.py` together.
