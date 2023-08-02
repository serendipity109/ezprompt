from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
import logging

DATABASE_URL = "mysql+pymysql://root:password@mysql:3306/requests"
Base = declarative_base()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Record(Base):
    __tablename__ = "records"
    _id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(1000), nullable=False)
    prompt = Column(Text, nullable=False)
    mode = Column(String(10), nullable=False)
    create_time = Column(DateTime, default=func.now())


class SQLAlchemyMon:
    def __init__(
        self,
    ):
        self.model = Record
        self.engine = create_engine(DATABASE_URL, pool_recycle=86400)  # 一天閒置會斷線
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create(self, **kwargs):
        try:
            record = self.model(**kwargs)
            self.session.add(record)
            self.session.commit()
            logger.info("Successfully saved a record!")
            return record
        except Exception as e:
            logger.error(f"Error in create: {e}")
            self.session.rollback()
            raise Exception(e)

    def read(self, _id):
        try:
            record = self.session.query(self.model).get(_id)
            if record:
                return {
                    column.key: getattr(record, column.key)
                    for column in self.model.__table__.columns
                }
            else:
                return None
        except Exception as e:
            logger.error(f"Error in read: {e}")
            self.session.rollback()
            raise Exception(e)

    def update(self, _id, **kwargs):
        try:
            record = self.session.query(self.model).get(_id)
            if record:
                for key, value in kwargs.items():
                    setattr(record, key, value)
                self.session.commit()
                return record
            else:
                return None
        except Exception as e:
            logger.error(f"Error in update: {e}")
            self.session.rollback()
            raise Exception(e)

    def delete(self, _id):
        try:
            record = self.session.query(self.model).get(_id)
            if record:
                self.session.delete(record)
                self.session.commit()
                return True
            else:
                return False
        except Exception as e:
            logger.error(f"Error in delete: {e}")
            self.session.rollback()
            raise Exception(e)
