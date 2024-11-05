from getpass import getpass
from mysql.connector import connect, Error

try:
    with connect(
        host="localhost",
        user="root",
        password="Alex2140",
        database="users_adfast"
    ) as connection:
        delete_user = """
        SELECT * FROM users_adfast
        """
        my_cursor = connection.cursor()
        my_cursor.execute(delete_user)
        rows = my_cursor.fetchall()
        connection.commit()
except Error as e:
    print(e)

print(rows)

