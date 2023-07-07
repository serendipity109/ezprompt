from crud import TransCRUD, ImgsCRUD, Trans, Imgs
from sqlalchemy import select, delete, inspect
from sqlalchemy.sql import func
import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IntegratedCRUD:
    def __init__(self, session):
        self.trans_crud = TransCRUD(session)
        self.imgs_crud = ImgsCRUD(session)

    def create_image(self, trans_data, imgs_data):
        trans = self.trans_crud.create(**trans_data)
        imgs = self.imgs_crud.create(**imgs_data)
        return trans, imgs

    def create_table(self, table_name, table_def):
        if not self.has_table(table_name):
            table_def.create(self.engine)
            print(f"Table '{table_name}' created.")
        else:
            print(f"Table '{table_name}' already exists.")

    def has_table(self, table_name):
        inspector = inspect(self.engine)
        return inspector.has_table(table_name)

    def read_table(self, table_name):
        logger.info(f"Read table {table_name.__tablename__}")
        session = self.Session()
        try:
            column_names = self.get_columns(table_name.__tablename__)
            table = session.query(table_name).all()
            for row in table:
                target = ""
                for column in column_names:
                    value = getattr(row, column)  # 獲取 row 物件中名為 column 的屬性的值
                    target += f"{column}: {value}, "
                logger.info(target)
        except Exception as e:
            logger.error(f"Error while reading table: {e}")
        finally:
            session.close()  # 確保session最後被關閉

    def get_columns(self, table_name):
        inspector = inspect(self.engine)
        columns = inspector.get_columns(table_name)
        column_names = [column["name"] for column in columns]
        return column_names

    def delete_expire_imgs(self):
        session = self.Session()
        try:
            stmt = select(Trans.prompt_id).where(
                Trans.create_time < func.now() - datetime.timedelta(minutes=1)
            )
            result = session.execute(stmt)
            expired_prompt_ids = [row.prompt_id for row in result]

            if expired_prompt_ids:
                stmt_delete_imgs = delete(Imgs).where(
                    Imgs.prompt_id.in_(expired_prompt_ids)
                )
                stmt_delete_trans = delete(Trans).where(
                    Trans.prompt_id.in_(expired_prompt_ids)
                )
                session.execute(stmt_delete_imgs)
                session.execute(stmt_delete_trans)
                session.commit()
            else:
                logger.info("There's no expired trans, imgs!")
        except:
            session.rollback()
            logger.exception("Delete expired imgs error")
            raise
        finally:
            session.close()
