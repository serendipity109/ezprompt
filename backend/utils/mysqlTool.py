from datetime import datetime
import os
import pymysql
from pydantic import BaseModel
from urllib.parse import urlparse
import random
import string


MYSQL_URI = os.environ.get("MYSQL_URI", "")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "")

class transInput(BaseModel):
    username: str
    status: str
    img1: str = ""
    img2: str = ""
    img3: str = ""
    img4: str = ""
    elapsed_time: str = "10.0"
    create_time: str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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
            raise "Query error"           

    def create_table(self, table, sql, commit=True, recreate=False):
        """
        建立 table
        """
        if recreate:
            self.query(f"DROP TABLE IF EXISTS {table}", commit)
        
        try:
            self.query(sql, commit)
            return f"Successively created table {table}"
        except:
            raise "Query error"

    def get_columns(self, table_name) -> set:
        """
        取得 table 的 column set
        """
        sql = f"DESCRIBE {table_name}"
        try:
            result = self.query(sql)
            columns = set([r[0] for r in result])
        except:
            raise "Get table columms error"
        return columns
    
    def insert_tran(self, inp, commit=True):
        try:
            inp = transInput(**inp).dict()
        except:
            raise "Input is invalid"
        rule_keys = list(inp.keys())
        rule_vals = [inp[key] for key in rule_keys]
        # sql = f"INSERT INTO `trans` (_id, username, status, img1, elapsed_time, create_time) VALUES ({values})"
        rule_keys.insert(0, "_id")
        rule_vals.insert(0, generate_random_id())
        sql = "INSERT INTO `trans` ({}) VALUES ({})".format(
            ", ".join(rule_keys),
            ", ".join(["%s"] * len(rule_vals)),
        )
        breakpoint()
        self.query(sql, rule_vals)
        try:
            self.query(sql, commit)
        except:
            raise "Get insert transaction error"
        return f"Successively insert transaction!"

def generate_random_id():
    letters_and_digits = string.digits
    random_id = ''.join(random.choice(letters_and_digits) for _ in range(10))
    return random_id
'''
from mysqlTool import MySQLClient
client = MySQLClient()
inp = {'username':'admin', 'status':'200', 'img1':'http://127.0.0.1:9000/ezrender-minio/1489891958.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=XWEUXHZJBAR985SC2RU4%2F20230512%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230512T090245Z&X-Amz-Expires=604800&X-Amz-Security-Token=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiJYV0VVWEhaSkJBUjk4NVNDMlJVNCIsImV4cCI6MTY4MzkyNTM2MCwicGFyZW50IjoibWluaW9hZG1pbiJ9.eeYDMki9st9T4a5w_OdAFsebSHqvbDkZApJM5ww64dfuwCHoKjngRYygx9PXpeGxVh06fxre69ksddQ3yJQI-Q&X-Amz-SignedHeaders=host&versionId=null&X-Amz-Signature=6ebb9d3343593436b7d25e5fd1de35a6cd3ee0bd17027665b6e52fe0c2dd19cb', 'elapsed_time':'10.0'}
client.insert_tran(inp)
'''
