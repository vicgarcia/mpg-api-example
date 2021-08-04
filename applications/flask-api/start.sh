#!/bin/sh

# wait for postgres container to start
while ! nc -z postgres-local 5432; do
    echo "postgres is unavailable. waiting ..." && sleep 20
done
echo "postgres is up" && sleep 10

# start dev server
cd /code/applications/flask-api
poetry run python run.py
