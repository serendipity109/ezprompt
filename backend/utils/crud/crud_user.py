from .crud import SQLAlchemyCRUD
from .model import User
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserCRUD(SQLAlchemyCRUD):
    def __init__(self):
        super().__init__(User)

    def user_id_exists(self, user_id):
        if self.session.query(self.model).filter_by(user_id=user_id).first():
            return True
        else:
            return False
