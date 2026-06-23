PYTHON ?= python3.12

.PHONY: install generate check-drift build test

install:
	$(PYTHON) -m pip install -e ".[dev]"

# Regenerate the low-level model layer from the vendored spec.
generate:
	./scripts/generate.sh

# Fail if the committed generated code is stale relative to the spec.
check-drift: generate
	git diff --exit-code src/lunogram/gen

build:
	$(PYTHON) -m build

test:
	$(PYTHON) -m pytest
