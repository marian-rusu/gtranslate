FROM python:3.7-slim-buster

COPY . /gtranslate

WORKDIR /gtranslate

RUN apt-get update -y && apt-get upgrade -y && \
    pip install --upgrade pip setuptools && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install .

ENV QUERIES_PER_SEC=10 RYPC_PORT=19961
