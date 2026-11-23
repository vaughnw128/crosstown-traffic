# Python/uv multi-stage build on Wolfi with a pinned Python minor (runs as nonroot)
FROM cgr.dev/chainguard/wolfi-base AS builder

RUN apk add --no-cache python-3.14

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV UV_PROJECT_ENVIRONMENT=/app/.venv \
    UV_PYTHON=python3.14 \
    UV_PYTHON_DOWNLOADS=never \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache --no-dev --no-install-project

COPY . .
RUN uv sync --frozen --no-cache --no-dev --no-editable

FROM cgr.dev/chainguard/wolfi-base AS runtime

RUN apk add --no-cache python-3.14

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

USER 65532:65532

EXPOSE 8080

ENTRYPOINT ["/app/.venv/bin/uvicorn", "crosstown_traffic.main:app", "--port", "8080", "--host", "0.0.0.0"]
