FROM python:3.10-slim

RUN set -ex \
    && RUN_DEPS=" \
 	build-essential \
 	ffmpeg \
    " \
    && apt-get update \
    && apt-get install -y --no-install-recommends $RUN_DEPS \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get -y auto-remove


RUN mkdir /code/
WORKDIR /code/
ADD pyproject.toml /code/
ADD poetry.lock /code/

ENV PATH=/code/.venv/bin:${PATH} \
    PIP_NO_CACHE_DIR=true

RUN set -ex \
    && pip install -U "poetry==1.1.12"  \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-root --no-dev

ADD src /code/
EXPOSE 8000

ENTRYPOINT ["/code/build/docker-entrypoint.sh"]
