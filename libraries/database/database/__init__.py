import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from marshmallow import ValidationError


HOST = os.getenv('POSTGRES_HOST', 'localhost')
PORT = int(os.getenv('POSTGRES_PORT', '0'))
DATABASE = os.getenv('POSTGRES_DB', 'example')
USER = os.getenv('POSTGRES_USER', 'user')
PASSWORD = os.getenv('POSTGRES_PASSWORD', 'pass1234')


engine = create_engine(f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}')

create_session = sessionmaker(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
