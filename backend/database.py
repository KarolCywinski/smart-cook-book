from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Base class for creating database models
class Base(DeclarativeBase):
    pass

# Make sure that every new session is binded to the same engine
engine = create_engine('sqlite:///cookbook.db', echo=False)
Session = sessionmaker(bind=engine)

# Enforce using foreign keys
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()