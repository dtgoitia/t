FROM docker.io/python:3.9.7-slim-buster as stage0

# https://stackoverflow.com/questions/59812009/what-is-the-use-of-pythonunbuffered-in-docker-file
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# TODO: stop using root user
# https://www.tutorialworks.com/podman-rootless-volumes/


FROM stage0 as release

ENV CONFIG_DIR_PATH "/config"

COPY ./requirements.txt /app/requirements.txt
RUN pip install \
      --no-cache-dir \
      -r /app/requirements.txt \
    && rm -rf /app/requirements.txt

COPY ./src /app/src

ENTRYPOINT ["python", "-m", "src.main"]

# TODO: add development stage?