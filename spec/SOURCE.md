# Spec source

`client.yaml` in this directory is **vendored** (copied verbatim) from the
platform repository's OpenAPI spec. It is the single input to the code generator
(`make generate` → `src/lunogram/gen/models.py`).

| | |
| --- | --- |
| Source repo | https://github.com/lunogram/platform |
| Spec path | `internal/http/controllers/v1/client/oapi/resources.yml` |
| Pinned ref | `a12f901dc98e7ced44efbad27a388e8bf5ee0f3a` |

The pinned ref is the head of platform PR #262 (the project-in-URL change). It is
a **branch/commit pin during development** — pinning to a commit means the spec
is fetchable from the public repo via the `raw.githubusercontent.com` URL with
no platform release required. Flip this to a `v*.*.*` release tag once the
platform cuts one.

## Raw URL

```
https://raw.githubusercontent.com/lunogram/platform/a12f901dc98e7ced44efbad27a388e8bf5ee0f3a/internal/http/controllers/v1/client/oapi/resources.yml
```

## Refreshing the spec

To pull a newer spec, update the pinned ref above and re-fetch:

```bash
REF=a12f901dc98e7ced44efbad27a388e8bf5ee0f3a
curl -fsSL "https://raw.githubusercontent.com/lunogram/platform/$REF/internal/http/controllers/v1/client/oapi/resources.yml" -o spec/client.yaml
make generate
```

The `spec-sync` GitHub Actions workflow automates exactly this on a weekly
schedule and opens a PR when the spec or generated code changes.
