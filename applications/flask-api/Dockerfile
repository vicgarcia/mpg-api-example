FROM python:3.7-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# update container
RUN apt -y update && apt -y upgrade
RUN apt -y install netcat

# update pip and install poetry
RUN pip install --upgrade pip
RUN pip install poetry

# setup path for codebase

# copy pipfile and install dependencies
RUN mkdir -p /code
COPY . /code

# install poetry dependencies in the container
WORKDIR /code/applications/flask-api
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction
