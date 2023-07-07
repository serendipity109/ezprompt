from crud import SQLAlchemyCRUD
from model import Users
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserCRUD(SQLAlchemyCRUD):
    def __init__(self):
        super().__init__(Users)
