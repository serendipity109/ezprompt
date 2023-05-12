import os
import pymysql
from urllib.parse import urlparse


MYSQL_URI = os.environ.get("MYSQL_URI", "")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "")

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
        
    def cursor(self):
        return self.client.cursor()
    
    def ping(self, reconnect=True):
        return self.client.ping(reconnect)
    
    def create_table(self, table, commit=True, recreate=False):
        if recreate:
            self.cursor.execute(f"DROP TABLE IF EXISTS {table}")
        
        self.client.ping(reconnect=True)
        try:
            if not self.cursor:
                cursor = self.client.cursor()
                self.cursor = cursor
            sql = """CREATE TABLE EMPLOYEE (
                    FIRST_NAME  CHAR(20) NOT NULL,
                    LAST_NAME  CHAR(20),
                    AGE INT,  
                    SEX CHAR(1),
                    INCOME FLOAT )"""
            result = self.cursor.execute(sql)
            if commit:
                self.client.connection.commit()
                self.close()
            return result
        except:
            raise "query error"
        
    def query(self, sql, commit=True):
        """
        查询操作
        :param sql:
        :param params:
        :return:
        """
        self.client.ping(reconnect=True)
        try:
            if not self.cursor:
                cursor = self.client.cursor()
                self.cursor = cursor

            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            if commit:
                self.client.connection.commit()
                self.close()
            return result
        except:
            raise "query error"           
