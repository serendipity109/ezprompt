from .crud import SQLAlchemyCRUD
from .model import Image
import datetime
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImgsCRUD(SQLAlchemyCRUD):
    def __init__(self):
        super().__init__(Image)

    def delete_exp_records(self, days=7):
        seven_days_ago = datetime.datetime.now() - datetime.timedelta(days=days)
        try:
            records = self.session.query(self.model).filter(
                self.model.create_time <= seven_days_ago
            )
            n = 0
            for record in records:
                self.session.delete(record)
                n += 1
            self.session.commit()
            logger.info(f"Delete {str(n)} records from image.")
        except Exception as e:
            logger.error(f"Error in delete_exp_records: {e}")
            self.session.rollback()
            raise Exception(e)
