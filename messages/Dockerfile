from python:3-slim

# create runtime user
run groupadd --system messages
run useradd --system --gid messages -m messages

# uv install
copy --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin

workdir /app
copy pyproject.toml .
copy uv.lock .

run uv sync --frozen --no-install-project

copy . /app

# set runtime user permissions on files after build
run chown -R messages:messages /app
run chmod +x /app/entrypoint.sh

user messages
cmd ["./entrypoint.sh"]

healthcheck --interval=30s --retries=3 --timeout=30s CMD [ "curl", "0.0.0.0:80/ready", "-s", "-f", "-o", "/dev/null", "||", "echo 'Web service down'", "||", "exit 1"]