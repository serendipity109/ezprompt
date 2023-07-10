from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
)
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"
    _id = Column(String(24), primary_key=True, nullable=False)
    user_id = Column(String(24), nullable=False, unique=True)
    password = Column(String(24), nullable=False)
    credits = Column(Integer, nullable=False, default=100)
    create_time = Column(DateTime, default=func.now())


class Trans(Base):
    __tablename__ = "trans"
    _id = Column(String, primary_key=True)
    user_id = Column(String)
    prompt_id = Column(String)
    img1 = Column(Text)
    img2 = Column(Text)
    img3 = Column(Text)
    img4 = Column(Text)
    create_time = Column(DateTime, default=datetime.now)


class Imgs(Base):
    __tablename__ = "imgs"
    _id = Column(String, primary_key=True)
    user_id = Column(String)
    prompt_id = Column(String)
    img = Column(Text)
    create_time = Column(DateTime, default=datetime.now)
