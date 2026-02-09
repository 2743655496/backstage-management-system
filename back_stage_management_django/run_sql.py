import os
import pymysql
from dotenv import load_dotenv
# 加载 .env 文件（本地开发 & Docker 都生效）
load_dotenv()
SQL_DIR = "./sql"

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = int(os.getenv("MYSQL_PORT"))
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")

conn = pymysql.connect(
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DB,
    autocommit=True
)

cursor = conn.cursor()

print("开始执行 SQL 文件...")

for file in sorted(os.listdir(SQL_DIR)):
    if file.endswith(".sql"):
        path = os.path.join(SQL_DIR, file)
        print(f"执行 {path} ...")
        with open(path, "r", encoding="utf-8") as f:
            sql = f.read()
            cursor.execute(sql)

cursor.close()
conn.close()

print("所有 SQL 文件执行完毕！")
