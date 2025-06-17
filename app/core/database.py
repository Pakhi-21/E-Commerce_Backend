
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./ecommerce.db"

# Establish a connection to the Sqlite database
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Connect to the database and provide a session for interacting with it
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# Base class for models
Base = declarative_base()
