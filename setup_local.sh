uv pip compile --universal -o requirements.txt pyproject.toml

uv pip compile --extra=dev --output-file=requirements-all.txt pyproject.toml

uv pip install --no-deps -e .

uv pip install -r requirements-all.txt