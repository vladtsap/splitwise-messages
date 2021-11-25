from envparse import env
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

TELEGRAM_TOKEN = env.str('TELEGRAM_TOKEN')
TELEGRAM_USER_ID = env.int('TELEGRAM_USER_ID')
SPLITWISE_USER_ID = env.int('SPLITWISE_USER_ID')

SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite3"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
