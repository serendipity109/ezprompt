import pymysql


class MySQLClient:
    def __init__(self):
        db_settings = {
            "host": "172.23.0.5",
            "port": 3306,
            "user": "root",
            "password": "mysqladmin",
            "db": "ezprompt"
        }
        self.client = pymysql.connect(**db_settings)
        
    def cursor(self):
        return self.client.cursor()
    
    def create_table(self, table, sql, commit, recreate=False):
        if recreate:
            self.cursor.execute(f"DROP TABLE IF EXISTS {table}")
        
        sql = f"""CREATE TABLE {table} (
                  USERID  CHAR(30) NOT NULL,
                  AGE INT,  
                  SEX CHAR(1),
                  INCOME FLOAT )"""
        
        self.client.ping(reconnect=True)
        try:
            if not self.cursor:
                cursor = self.client.cursor()
                self.cursor = cursor

            result = self.cursor.execute(sql)
            if commit:
                self.client.connection.commit()
                self.close()
            return result
        except:
            raise "query error"
             