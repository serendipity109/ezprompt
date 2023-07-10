import datetime
import logging
import json

from .crud import Imgs, ImgsCRUD, MJImg, Trans, TransCRUD, UserCRUD, Users
from sqlalchemy import delete, inspect, select
from sqlalchemy.sql import func
from utils import redisTool
from utils.tools import generate_random_id

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

redis_client = redisTool.RedisClient()
# user_crud.create(_id = "2", user_id= "fw-adam", password="6666", credits=100)


class IntegratedCRUD:
    def __init__(self):
        self.user_crud = UserCRUD()
        self.trans_crud = TransCRUD()
        self.imgs_crud = ImgsCRUD()

    async def check_trans_valid(self, user_id: str, n: int):
        user_data = self.user_crud.read_by_userid(user_id)
        if user_data and (user_data["credits"] - n) >= 0:
            self.user_crud.update_user_credit(user_id, user_data["credits"] - n)
            return True
        else:
            return False

    async def insert_mjimage(self, input: MJImg):
        user_id = input.user_id
        prompt = input.prompt
        size = input.size
        pmt_id = await generate_random_id(10)
        img1, img2, img3, img4 = input.images
        redis_value = {
            "user_id": user_id,
            "prompt": prompt,
            "size": size,
            "img1": img1,
            "img2": img2,
            "img3": img3,
            "img4": img4,
        }
        if input.source_url:
            source_url = input.source_url
            redis_value["source_url"] = source_url
        try:
            redis_client.set(pmt_id, json.dumps(redis_value))
        except Exception as e:
            logger.error(f"Error in insert redis: {e}")
            raise Exception(f"Error in insert redis: {e}")
        try:
            self.trans_crud.create(
                _id=await generate_random_id(10),
                user_id=user_id,
                prompt_id=pmt_id,
                img1=img1,
                img2=img2,
                img3=img3,
                img4=img4,
            )
        except Exception as e:
            logger.error(f"Error in insert trans: {e}")
            raise Exception(f"Error in insert trans: {e}")
        try:
            for img in [img1, img2, img3, img4]:
                self.imgs_crud.create(
                    _id=await generate_random_id(10),
                    user_id=user_id,
                    prompt_id=pmt_id,
                    img=img,
                )
        except Exception as e:
            logger.error(f"Error in insert imgs: {e}")
            raise Exception(f"Error in insert imgs: {e}")
        logger.info("Successfully store image data!")

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
