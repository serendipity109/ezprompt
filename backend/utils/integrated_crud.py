import shutil
import logging
import json
import os

from .crud import Imgs, ImgsCRUD, MJImg, Trans, TransCRUD, UserCRUD, Users
from sqlalchemy import delete, inspect, select
from sqlalchemy.sql import func
from utils import redisTool
from utils.tools import generate_random_id

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# user_crud.create(_id = "2", user_id= "fw-adam", password="6666", credits=100)


class IntegratedCRUD:
    def __init__(self):
        self.user_crud = UserCRUD()
        self.trans_crud = TransCRUD()
        self.imgs_crud = ImgsCRUD()
        self.redis_client = redisTool.RedisClient()

    async def check_trans_valid(self, user_id: str, n: int):
        user_data = self.user_crud.read_by_userid(user_id)
        if user_data:
            credits = user_data["credits"]
            if (credits - n) >= 0:
                return True
        return False

    async def pay_credits(self, user_id: str, n: int):
        user_data = self.user_crud.read_by_userid(user_id)
        credits = user_data["credits"]
        try:
            self.user_crud.update_user_credit(user_id, credits - n)
        except Exception as e:
            logger.error(f"Error in paying: {e}")
            raise Exception(f"Error in paying: {e}")

    async def refund_credits(self, user_id: str, n: int):
        user_data = self.user_crud.read_by_userid(user_id)
        credits = user_data["credits"]
        try:
            self.user_crud.update_user_credit(user_id, credits + n)
        except Exception as e:
            logger.error(f"Error in refunding: {e}")
            raise Exception(f"Error in refunding: {e}")

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
            "model": "midjourney"
        }
        if input.source_url:
            # img2img
            source_url = input.source_url
            redis_json["source_url"] = source_url
        try:
            self.redis_client.set_hash(pmt_id, redis_json)
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

    async def create_user(self, user_id, password, credits):
        if self.user_crud.read_by_userid(user_id) is None:
            try:
                _id = await generate_random_id(10)
                self.user_crud.create(
                    _id=_id, user_id=user_id, password=password, credits=credits
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
                if self.redis_client.delete(pmt_id) == 0:
                    logger.error("Error in delete pmt_id")
                    raise Exception("Error in delete pmt_id")
        try:
            self.trans_crud.delete_user_by_id(user_id)
        except Exception as e:
            logger.error(f"Error in delete trans: {e}")
            raise Exception(f"Error in delete trans: {e}")
        try:
            self.user_crud.delete_user_by_id(user_id)
        except Exception as e:
            logger.error(f"Error in delete users: {e}")
            raise Exception(f"Error in delete users: {e}")
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
            return []
