from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

DATABASE_URL = "sqlite+pysqlite:///gsmarena.db"

engine = create_engine(DATABASE_URL, future=True)
Base = declarative_base()
db_session = Session(bind=engine, autocommit=False, autoflush=False)
