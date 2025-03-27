FROM python:3.13-slim AS builder

COPY pyproject.toml /code/pyproject.toml

RUN apt-get update \
    && apt-get install -y \
        build-essential \
    && apt-get clean \
    && pip install --no-cache-dir --user /code/.


    
FROM python:3.13-slim

LABEL maintainer="Samuele Galli <s.galli@arca24.com>"
EXPOSE 8000

RUN apt-get update \
    && apt-get install -y \
        nano \
    && apt-get clean

RUN useradd --create-home --shell /bin/bash arcabot

COPY --from=builder --chown=arcabot /root/.local /home/arcabot/.local

ENV PATH=/home/arcabot/.local/bin:$PATH

WORKDIR /usr/src/app
COPY src .

USER arcabot
CMD ["sh", "entrypoint.sh"]