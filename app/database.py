from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLACHEMY_DATABASE_URL = 'postgresql://postgres:wordpress@localhost/fastapi'

engine = create_engine(SQLACHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocmmit=False)
# sessionLocal seres as a factory for creating new sessions

Base = declarative_base()

def get_db():
    """
    this creates a new session via the SessionLocal
    and stores it in the db variable and then yields this db variable back.
    We can then use the new session via the db variable to query the database.
    """
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()