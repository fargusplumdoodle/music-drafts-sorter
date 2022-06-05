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

RUN set -ex \
    && pip install -U "poetry==1.1.12"

RUN useradd -ms /bin/bash service
RUN mkdir /code/ && chown service:service /code
USER service

WORKDIR /code/
ADD pyproject.toml /code/
ADD poetry.lock /code/

ENV PATH=/code/.venv/bin:${PATH} \
    PIP_NO_CACHE_DIR=true

RUN set -ex \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-root --no-dev

ADD src /code/
EXPOSE 8000

ENTRYPOINT ["python", "main.py"]
