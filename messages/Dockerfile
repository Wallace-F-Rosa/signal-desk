from python:3.10.12-slim

# uv install
copy --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin

workdir /app
copy pyproject.toml .
copy uv.lock .

run uv sync --frozen --no-install-project

add . /app

run uv sync --frozen

RUN chmod +x entrypoint.sh

cmd ["./entrypoint.sh"]