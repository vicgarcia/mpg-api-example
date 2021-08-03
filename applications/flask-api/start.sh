#!/bin/sh

cd /code/applications/flask-api

# install dependencies
poetry install

# wait for postgres container to start
while ! nc -z postgres-local 5432; do
    echo "postgres is unavailable. waiting ..." && sleep 20
done
echo "postgres is up" && sleep 10

# keep the docker container running doing nothing

# start dev server
poetry run python run.py
