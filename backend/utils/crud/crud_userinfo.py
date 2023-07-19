from .crud import SQLAlchemyCRUD
from .model import UserInfo
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserInfoCRUD(SQLAlchemyCRUD):
    def __init__(self):
        super().__init__(UserInfo)

    def read_by_userid(self, user_id):
        try:
            record = self.session.query(self.model).filter_by(user_id=user_id).first()
            return {
                column.key: getattr(record, column.key)
                for column in self.model.__table__.columns
            }
        except Exception as e:
            logger.error(f"Error in read_by_username: {e}")
            self.session.rollback()
            raise Exception(f"Error in read_by_username: {e}")

    def update_user_credit(self, user_id, new_credit):
        try:
            record = self.session.query(self.model).filter_by(user_id=user_id).first()
            record.credits = new_credit
            self.session.commit()
            return True
        except Exception as e:
            logger.error(f"Error in update_user_credit: {e}")
            self.session.rollback()
            raise Exception(f"Error in update_user_credit: {e}")
