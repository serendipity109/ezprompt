import shutil
import logging
import os

from .crud import (
    UserCRUD,
    UserInfoCRUD,
    ImgsCRUD,
    TransCRUD,
    MJImg,
)
from sqlalchemy import delete, inspect, select
from sqlalchemy.sql import func
from utils import redisTool
from utils.tools import generate_random_id

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# user_crud.create(user_id= "fw-adam", password="6666", credits=100)


class IntegratedCRUD:
    def __init__(self):
        self.user_crud = UserCRUD()
        self.userinfo_crud = UserInfoCRUD()
        self.trans_crud = TransCRUD()
        self.imgs_crud = ImgsCRUD()
        self.redis_client = redisTool.RedisClient()

    async def check_trans_valid(self, user_id: str, n: int):
        user_data = self.userinfo_crud.read_by_userid(user_id)
        if user_data:
            credits = user_data["credits"]
            if (credits - n) >= 0:
                return True
        return False

    async def insert_mjimage(self, input: MJImg):
        user_id = input.user_id
        prompt = input.prompt
        size = input.size
        dim = ""
        match size:
            case "1:1":
                dim = "1024x1024"
            case "16:9":
                dim = "1456x816"
            case "9:16":
                dim = "816x1456"
        pmt_id = await generate_random_id(10)
        img1, img2, img3, img4 = input.images
        redis_json = {
            "user_id": user_id,
            "prompt": prompt,
            "size": dim,
            "batch": [img1, img2, img3, img4],
            "model": "midjourney",
        }
        if input.source_url:
            # img2img
            source_url = input.source_url
            redis_json["source_url"] = source_url
            redis_json["prompt"] = prompt.replace(source_url + " ", "")
        try:
            self.redis_client.set_hash(pmt_id, redis_json)
        except Exception as e:
            logger.error(f"Error in insert redis: {e}")
            raise Exception(f"Error in insert redis: {e}")
        try:
            self.trans_crud.create(
                user_id=user_id,
                prompt_id=pmt_id,
            )
        except Exception as e:
            logger.error(f"Error in insert trans: {e}")
            raise Exception(f"Error in insert trans: {e}")
        try:
            for img in [img1, img2, img3, img4]:
                self.imgs_crud.create(
                    user_id=user_id,
                    prompt_id=pmt_id,
                    img=img,
                )
        except Exception as e:
            logger.error(f"Error in insert imgs: {e}")
            raise Exception(f"Error in insert imgs: {e}")
        logger.info("Successfully store image data!")

    async def get_token(self, user_id, password):
        if self.user_crud.user_id_exists(user_id):
            user_data = self.userinfo_crud.read_by_userid(user_id)
            if user_data["password"] == password:
                return user_data["token"]
        return ""

    async def create_user(self, user_id, password, token):
        if self.user_crud.read(user_id) is None:
            try:
                self.user_crud.create(user_id=user_id)
                self.userinfo_crud.create(
                    user_id=user_id, password=password, token=token
                )
            except Exception as e:
                logger.error(f"Error in create user: {e}")
                raise Exception(f"Error in create user: {e}")
        else:
            logger.error(f"user_id {user_id} exists!")
            raise Exception(f"user_id {user_id} exists!")

    async def delete_user_by_id(self, user_id):
        try:
            self.imgs_crud.delete_user_by_id(user_id)
        except Exception as e:
            logger.error(f"Error in delete imgs: {e}")
            raise Exception(f"Error in delete imgs: {e}")
        records = self.trans_crud.read_user_by_id(user_id)
        if records:
            records = sorted(records, key=lambda x: x["create_time"], reverse=True)
            for record in records:
                pmt_id = record["prompt_id"]
                try:
                    self.redis_client.delete(pmt_id)
                except:
                    logger.error("Error in delete redis prompt")
                    raise Exception("Error in delete redis prompt")
        try:
            self.trans_crud.delete_user_by_id(user_id)
        except Exception as e:
            logger.error(f"Error in delete trans: {e}")
            raise Exception(f"Error in delete trans: {e}")
        try:
            self.userinfo_crud.delete_user_by_id(user_id)
        except Exception as e:
            logger.error(f"Error in delete userinfo: {e}")
            raise Exception(f"Error in delete userinfo: {e}")
        try:
            self.user_crud.delete_user_by_id(user_id)
        except Exception as e:
            logger.error(f"Error in delete user: {e}")
            raise Exception(f"Error in delete user: {e}")
        if os.path.exists(f"/workspace/output/{user_id}"):
            shutil.rmtree(f"/workspace/output/{user_id}")
        logger.info(f"Successfully delete user {user_id}")

    async def read_user_history(self, user_id):
        records = self.imgs_crud.read_user_by_id(user_id)
        if records:
            records = sorted(records, key=lambda x: x["create_time"], reverse=True)
            history = []
            visited = []
            for record in records:
                pmt_id = record["prompt_id"]
                if pmt_id not in visited:
                    pmt_record = self.redis_client.get_hash(pmt_id)
                    pmt = pmt_record["prompt"]
                    view1 = pmt.split(",")[0]
                    view2 = pmt.replace(view1 + ",", "")
                    img1 = pmt_record["batch"][0]
                    img2 = pmt_record["batch"][1]
                    img3 = pmt_record["batch"][2]
                    img4 = pmt_record["batch"][3]
                    for img in [img4, img3, img2, img1]:
                        logger.info(img)
                        if img:
                            img = img.replace(".png", ".jpg")
                            filename = os.path.basename(img)
                            history.append(
                                {
                                    "id": pmt_id,
                                    "filename": filename,
                                    "url": img,
                                    "view1": view1,
                                    "view2": view2,
                                }
                            )
                    visited.append(pmt_id)
            return history
        else:
            raise Exception(f"user_id {user_id} doesn't exist.")

    async def get_credits(self, user_id: str):
        try:
            user_data = self.userinfo_crud.read_by_userid(user_id)
            credits = user_data["credits"]
            return credits
        except Exception as e:
            logger.error(f"Error in get credits: {e}")
            raise Exception(f"Error get credits: {e}")

    async def pay_credits(self, user_id: str, n: int):
        user_data = self.userinfo_crud.read_by_userid(user_id)
        credits = user_data["credits"]
        try:
            self.userinfo_crud.update_user_credit(user_id, credits - n)
            logger.info(f"User {user_id} Pay 4 credits")
            return credits - n
        except Exception as e:
            logger.error(f"Error in paying: {e}")
            raise Exception(f"Error in paying: {e}")

    async def topup_credits(self, user_id: str, n: int):
        user_data = self.userinfo_crud.read_by_userid(user_id)
        credits = int(user_data["credits"]) + n
        try:
            self.userinfo_crud.update_user_credit(user_id, credits)
            return credits
        except Exception as e:
            logger.error(f"Error in topup: {e}")
            raise Exception(f"Error in topup: {e}")

    # async def read_showcase(self, top_n: int):
    #     records = self.trans_crud.read_top_k_rows(top_n)
