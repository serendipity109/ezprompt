from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
import os

MYSQL_URI = os.environ.get("MYSQL_URI", "")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "")
DATABASE_URL = f"{MYSQL_URI}/{MYSQL_DATABASE}"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SQLAlchemyCRUD:
    def __init__(self, model):
        self.model = model
        self.engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create(self, **kwargs):
        try:
            record = self.model(**kwargs)
            self.session.add(record)
            self.session.commit()
            return record
        except Exception as e:
            logger.error(f"Error in create: {e}")
            self.session.rollback()

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
