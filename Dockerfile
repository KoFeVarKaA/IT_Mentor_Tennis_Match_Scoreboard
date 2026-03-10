FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
RUN useradd --no-create-home --gid root runner

ENV UV_PROJECT_ENVIRONMENT=/app/.venv \
    UV_NO_MANAGED_PYTHON=1 \
    UV_NO_CACHE=true \
    UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .
ENV PATH=/app/.venv/bin:$PATH

RUN uv sync --all-extras --frozen --no-install-project

COPY . .
CMD ["python", "main.py"]