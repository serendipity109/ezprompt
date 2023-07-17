from .crud import SQLAlchemyCRUD
from .model import Image
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImgsCRUD(SQLAlchemyCRUD):
    def __init__(self):
        super().__init__(Image)