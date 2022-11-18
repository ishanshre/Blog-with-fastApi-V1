from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



sqlite_path = "sqlite:///./blog_sqlite.db"


engine = create_engine(sqlite_path, connect_args={
    "check_same_thread":False
})

SessionLocal = sessionmaker(bind = engine, autocommit=False, autoflush=False)

Base = declarative_base()


#getting the db
# important dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()