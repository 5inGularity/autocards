from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from . import models

SQLALCHEMY_DATABASE_URL = "postgresql://example:example@db:5432/example"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)  # create tables
