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
        DELETE FROM users_adfast WHERE NAME = 'SANCHEZ'
        """
        with connection.cursor() as cursor:
            cursor.execute(delete_user)
            connection.commit()
except Error as e:
    print(e)

