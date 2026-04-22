# Python/uv multi-stage build using Chainguard images (runs as nonroot by default)
FROM cgr.dev/chainguard/python:latest-dev AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV UV_PROJECT_ENVIRONMENT=/app/.venv

COPY --chown=nonroot:nonroot pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache --no-dev --no-install-project

COPY --chown=nonroot:nonroot . .
RUN uv sync --frozen --no-cache --no-dev --no-editable

FROM cgr.dev/chainguard/python:latest AS runtime

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8080

ENTRYPOINT ["/app/.venv/bin/uvicorn", "crosstown_traffic.main:app", "--port", "8080", "--host", "0.0.0.0"]
