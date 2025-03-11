from os import environ

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DB_HOST = environ["DB_HOST"]
DB_USER = environ["DB_USER"]
DB_PASS = environ["DB_PASS"]
DB_NAME = environ["DB_NAME"]
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
