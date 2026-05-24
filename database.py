from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker , DeclarativeBase 

DATABASE_URL = "postgresql://postgres:root@localhost:5432/docplatform"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
class Base(DeclarativeBase):
    pass