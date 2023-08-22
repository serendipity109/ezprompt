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
        self.engine = create_engine(
            DATABASE_URL, pool_pre_ping=True
        )  # 如果連線不再活躍，則會自動回收，回收完會重連。
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

    def read_user_by_id(self, user_id):
        try:
            records = self.session.query(self.model).filter_by(user_id=user_id).all()
            if records:
                result = []
                for record in records:
                    result.append(
                        {
                            column.key: getattr(record, column.key)
                            for column in self.model.__table__.columns
                        }
                    )
                return result
            else:
                return None
        except Exception as e:
            logger.error(f"Error in read: {e}")
            self.session.rollback()
            raise Exception(e)

    def read_all(self):
        try:
            records = self.session.query(self.model).all()
            result = []
            for record in records:
                result.append(
                    {
                        column.key: getattr(record, column.key)
                        for column in self.model.__table__.columns
                    }
                )
            return result
        except Exception as e:
            logger.error(f"Error in read_all: {e}")
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

    def delete_user_by_id(self, user_id):
        try:
            # 这将删除所有 user_id 等于指定值的记录
            record_count = (
                self.session.query(self.model).filter_by(user_id=user_id).delete()
            )
            self.session.commit()

            # 如果有任何记录被删除，返回 True，否则返回 False
            return record_count > 0
        except Exception as e:
            logger.error(f"Error in delete_user_by_id: {e}")
            self.session.rollback()
            raise Exception(e)
