from .crud import SQLAlchemyCRUD
from .model import Transaction
from sqlalchemy import desc
import logging
import datetime


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TransCRUD(SQLAlchemyCRUD):
    def __init__(self):
        super().__init__(Transaction)

    def read_top_n_rows(self, n, user_id=""):
        try:
            if user_id:
                records = (
                    self.session.query(self.model)
                    .filter(self.model.user_id != user_id)
                    .order_by(desc(self.model.create_time))
                    .limit(n)
                    .all()
                )
            else:
                records = (
                    self.session.query(self.model)
                    .order_by(desc(self.model.create_time))
                    .limit(n)
                    .all()
                )
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
            logger.error(f"Error in read_top_k_rows: {e}")
            self.session.rollback()
            raise Exception(e)

    def delete_exp_records(self, days=7):
        seven_days_ago = datetime.datetime.now() - datetime.timedelta(days=days)
        try:
            records = self.session.query(self.model).filter(
                self.model.create_time <= seven_days_ago
            )
            result = []
            n = 0
            for record in records:
                result.append(
                    {
                        column.key: getattr(record, column.key)
                        for column in self.model.__table__.columns
                    }
                )
                self.session.delete(record)
                n += 1
            self.session.commit()
            logger.info(f"Delete {str(n)} records from transaction.")
            return result
        except Exception as e:
            logger.error(f"Error in delete_exp_records: {e}")
            self.session.rollback()
            raise Exception(e)
