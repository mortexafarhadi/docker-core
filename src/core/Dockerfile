# FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim
FROM astral/uv:python3.13-bookworm-slim

LABEL maintainer="mortexafarhadi@gmail.com"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/projects/app/.venv/bin:$PATH"
ENV UV_HTTP_TIMEOUT=1200

WORKDIR /projects/app

## set mirror for debian
RUN printf "Types: deb\n\
URIs: http://mirror-linux.runflare.com/debian\n\
     https://linux-mirror.liara.ir/repository/debian/\n\
Suites: bookworm bookworm-updates bookworm-security\n\
Components: main contrib non-free non-free-firmware\n" \
> /etc/apt/sources.list.d/debian.sources

## for install mysql/mariadb package
# RUN for i in 1 2 3; do apt-get update && break || sleep 5; done && \
#     apt-get install -y --no-install-recommends build-essential gcc \
#     python3-dev default-libmysqlclient-dev pkg-config libssl-dev \
#     libffi-dev netcat-openbsd && rm -rf /var/lib/apt/lists/*

## for install nc package
RUN for i in 1 2 3; do apt-get update && break || sleep 5; done && \
    apt-get install -y --no-install-recommends netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project --extra production

COPY . .

RUN uv sync --frozen --extra production

## for install unuse mysql/mariadb package
# RUN apt-get remove -y build-essential gcc python3-dev default-libmysqlclient-dev \
#     pkg-config libssl-dev libffi-dev

RUN chmod +x ./___deploy/*.sh

ENTRYPOINT [ "sh", "-c", "./___deploy/script.sh" ]
