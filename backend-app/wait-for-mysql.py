import MySQLdb
import time
from sys import stdout
import os

app_env: str = os.getenv('APP_ENV')

host: str = os.getenv('MYSQL_HOST_' + app_env.upper())
user: str = os.getenv('MYSQL_USER')
password: str = os.getenv('MYSQL_PASSWORD')
port: int = int(os.getenv('MYSQL_PORT'))
db: str = os.getenv('MYSQL_DATABASE')

def writeAndFlush(out: str):
    stdout.write(out)
    stdout.flush()

writeAndFlush("Checking MYSQL ...\n")

message = """
    ################################ 
    database connect:
    host = %s
    user = %s
    password = %s
    port = %s
    db = %s
    ################################ \n\n
""" % (host, user, password, port, db)

writeAndFlush(message)

while True:
    try:
        conn = MySQLdb.connect(host=host, user=user, passwd=password , port=port)

        while True:
            cursor = conn.cursor()
            cursor.execute("show databases like '" + db + "'")
            result = cursor.fetchone()

            if result and len(result) > 0:
                writeAndFlush("database %s create successful\n" % db)
                break
            else:
                writeAndFlush("database %s not created... waiting...\n" % db)
                time.sleep(1)

            cursor.close()

        conn.close()
        break
    except Exception as e:
        writeAndFlush("MYSQL not responds.. waiting for mysql up: %s\n" % e)
        time.sleep(1)
