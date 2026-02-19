#!/bin/bash
#

source $HOME/.bashrc
source .venv/bin/activate 
uv sync && uv pip install -e . && echo "Done"

uv run pytest
uv run ty check src/arkhon-rheo/
uv run ty check tests/
uv run ruff check src/arkhon-rheo/
uv run ruff check tests/
uv run radon src/arkhon-rheo/
uv run radon tests/

