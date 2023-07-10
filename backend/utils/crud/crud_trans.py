from .crud import SQLAlchemyCRUD
from .model import Trans
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TransCRUD(SQLAlchemyCRUD):
    def __init__(self):
        super().__init__(Trans)
