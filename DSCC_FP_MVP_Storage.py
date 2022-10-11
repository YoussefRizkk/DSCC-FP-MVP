import DSCC_FP_MVP_Configuration as config
import mysql.connector
from mysql.connector import errorcode
from sqlalchemy import create_engine

# Connecting to a database
print(config.host)
connect_db = mysql.connector.connect(
    host=config.host,
    user=config.user,
    password=config.password
)

# cursor_object = connect_db.cursor()
print(connect_db)
# Creating a database


# cursor_object.execute('CREATE DATABASE mydb')
# print(cursor_object.etchwarnings())
# try:
#     cursor_object.execute('CREATE DATABASE mydb')
# except sql.Error as err:
#     print(f'DB Error {err}')

# try:
#     cursor_object.execute('USE mydb')
#     print('Database selected')
# except:
#     print('Database not selected')

# cursor_object.execute('SHOW TABLES')
# print(cursor_object.fetchall())
