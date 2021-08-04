An example python project that provides a set of api endpoints for creating a vehicle, creating records for fuel fill-ups for that vehicle, and retrieving fill-ups with calculated miles per gallon.

It uses poetry to create a monorepo of individual poetry projects, where conceptually projects are categorized as either 'applications' or 'libraries'. Each of these projects have their own dependencies. The seperation of libraries and applications is utilized for organizing code that is intended to be shared, where libraries are installed as dependencies into applications.

This project only utilizes one of each, a 'database' library containing sqlalchemy models and alembic configuration for migrations, and a 'flask-api' application containing the flask app to provide the apis. The 'database' library utilizes sqlalchemy as an orm, alembic to manage database migrations, and marshmallow to provide model serialization. The 'flask-api' application utilizes flask as well as the models and serializers that are defined as part of our 'database' libary.

This paradigm could be continued to include as examples a 'notification' library, with code to send emails, and a 'scheduled-task' app, which executes tasks at certain times.

This repository also includes the necessary configuration to run the flask app and postgres database with docker and interact with the apis via the insomnia rest client. The instructions below explain how clone the repo and run the application.


### development

clone repository

```
git clone git@github.com:vicgarcia/mpg-api-example.git
cd mpg-api-example
```

start the docker container for the postgres db

```
docker compose up -d postgres-local
docker compose logs -f postgres-local
```

install dependencies in the database app and run alembic to apply migrations locally

```
cd libraries/database
poetry install
poetry run alembic upgrade head
```

start the flask application container

```
docker compose up -d flask-api-local
docker compose logs -f flask-api-local
```

at this point interact with the api using the provided insomnia.yaml

create a vehicle, list vehicles, create two fillups, then retrieve fillups with calculated mpg

to add a new library or application

```
cd applications
poetry new <application name>

cd libraries
poetry new <library name>
```

to install a library in an application as editable, where changes in the library code will be immediately reflected in the application, add in the `pyproject.toml` of the application

```
<library name> = {path = "../../libraries/<library name>", develop = true}
```
