from datetime import datetime
import logging
import os
import pymysql
from pydantic import BaseModel
from urllib.parse import urlparse
import random
import string


MYSQL_URI = os.environ.get("MYSQL_URI", "")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "")

logger = logging.getLogger(__name__)


class MySQLClient:
    def __init__(self):
        url_config = urlparse(MYSQL_URI)
        self.host = url_config.hostname
        self.port = url_config.port
        self.user = url_config.username
        self.password = url_config.password

        self.client = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            charset="utf8mb4",
            database=MYSQL_DATABASE,
        )

    def ping(self, reconnect=True):
        return self.client.ping(reconnect)

    def query(self, sql, params=(), commit=True):
        self.client.ping(reconnect=True)
        try:
            with self.client.cursor() as cursor:
                cursor.execute(sql, params)
                result = cursor.fetchall()
                if commit:
                    self.client.commit()
                    self.client.close()
                return result
        except:
            logger.exception("Query error")
            raise

    def create_table(self, table, sql, commit=True, recreate=False):
        """
        建立 table
        """
        if recreate:
            self.query(f"DROP TABLE IF EXISTS {table}", commit)
        try:
            self.query(sql, commit)
            logger.info(f"Successively created table {table}")
        except:
            logger.exception("Query error")
            raise

    def get_columns(self, table_name) -> set:
        """
        取得 table 的 column set
        """
        sql = f"DESCRIBE {table_name}"
        try:
            result = self.query(sql)
            columns = set([r[0] for r in result])
        except:
            logger.exception("Get table columms error")
            raise
        return columns

    def insert_tran(self, inp, commit=True):
        try:
            inp = transInput(**inp).dict()
        except:
            logger.exception("Trans input is invalid")
            raise
        rule_keys = list(inp.keys())
        rule_vals = [inp[key] for key in rule_keys]
        rule_keys.insert(0, "_id")
        trans_id = generate_random_id()
        rule_vals.insert(0, trans_id)
        sql = "INSERT INTO `trans` ({}) VALUES ({})".format(
            ", ".join(rule_keys),
            ", ".join(["%s"] * len(rule_vals)),
        )
        rv = []
        for val in rule_vals:
            if val == "":
                rv.append(None)
            else:
                rv.append(val)
        try:
            self.query(sql, rv, commit)
        except:
            logger.exception("Get insert transaction error")
            raise
        imgs = ["img1", "img2", "img3", "img4"]
        for img in imgs:
            if inp[img]:
                img_inp = {
                    "trans_id": trans_id,
                    "username": inp["username"],
                    "img": inp[img],
                    "create_time": inp["create_time"],
                }
                self.insert_img(img_inp)
        logger.info("Successively insert transaction!")

    def insert_img(self, inp, commit=True):
        try:
            inp = imgInput(**inp).dict()
        except:
            logger.exception("Img input is invalid")
            raise
        rule_keys = list(inp.keys())
        rule_vals = [inp[key] for key in rule_keys]
        rule_keys.insert(0, "_id")
        rule_vals.insert(0, generate_random_id())
        sql = "INSERT INTO `imgs` ({}) VALUES ({})".format(
            ", ".join(rule_keys),
            ", ".join(["%s"] * len(rule_vals)),
        )
        try:
            self.query(sql, rule_vals, commit)
        except:
            logger.exception("Get insert image error")
            raise
        logger.info("Successively insert image!")

    def delete_expire_imgs(self, commit=True):
        for table in ["imgs", "trans"]:
            sql = f"DELETE FROM {table} WHERE create_time < DATE_SUB(NOW(), INTERVAL 7 DAY);"
            try:
                self.query(sql, params=(), commit=commit)
            except:
                logger.exception("Get delete expire error")
                raise
            logger.info("Successively delete expire trans, imgs!")            

def generate_random_id():
    letters_and_digits = string.digits
    random_id = "".join(random.choice(letters_and_digits) for _ in range(10))
    return random_id


"""
from mysqlTool import MySQLClient
client = MySQLClient()
inp = {'username':'admin', 'status':'200', 'img1':
    'http://127.0.0.1:9000/ezrender-minio/...', 'elapsed_time':'10.0'}
client.insert_tran(inp)
"""


class transInput(BaseModel):
    username: str
    status: str
    img1: str = ""
    img2: str = ""
    img3: str = ""
    img4: str = ""
    elapsed_time: str = "10.0"
    create_time: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class imgInput(BaseModel):
    _id: str
    trans_id: str
    username: str
    img: str = ""
    create_time: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
