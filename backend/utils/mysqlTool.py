import pymysql


db_settings = {
    "host": "172.23.0.5",
    "port": 3306,
    "user": "root",
    "password": "mysqladmin",
    "db": "ezprompt"
}

db = pymysql.connect(**db_settings)

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
 
# 使用 execute()  方法执行 SQL 查询 
cursor.execute("SELECT VERSION()")
 
# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchone()
 
print ("Database version : %s " % data)
 
# 关闭数据库连接
db.close()