FROM astral/uv:python3.13-bookworm-slim

LABEL maintainer="mortexafarhadi@gmail.com"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/app/.venv/bin:$PATH"
ENV UV_HTTP_TIMEOUT=1200

WORKDIR /app

COPY ./src/core/pyproject.toml ./src/core/uv.lock ./

# RUN uv lock --upgrade

RUN uv sync --frozen --no-install-project --extra testing

COPY ./src/core/ .

RUN uv sync --frozen --extra testing
