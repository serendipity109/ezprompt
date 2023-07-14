from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    _id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(20), nullable=False, unique=True)


class UserInfo(Base):
    __tablename__ = "user_info"
    _id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        String(20), ForeignKey("user.user_id"), nullable=False, unique=True
    )
    password = Column(String(24), nullable=False)
    credits = Column(Integer, nullable=False, default=0)
    token = Column(String(30), nullable=False)
    create_time = Column(DateTime, default=func.now())
    update_time = Column(DateTime, default=func.now(), onupdate=func.now())


class Transaction(Base):
    __tablename__ = "transaction"
    _id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(20), ForeignKey("user.user_id"))
    prompt_id = Column(String(20), nullable=True, unique=True)
    create_time = Column(DateTime, default=func.now())


class Image(Base):
    __tablename__ = "image"
    _id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(20), ForeignKey("user.user_id"))
    prompt_id = Column(String(20), ForeignKey("transaction.prompt_id"))
    img = Column(String(100))
    create_time = Column(DateTime, default=func.now())
