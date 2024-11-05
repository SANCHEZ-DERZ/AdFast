import mysql.connector
import os
import sys
sys.path.append(os.getcwd())
import AdFast.config as config
print(config.__file__)
   


def adding_user_in_database(user_name, user_id):
    try:
        insert_user = f"""INSERT INTO users_adfast (name, user_id)
        VALUES
            ('%s', '%s');
        """ % (user_name, user_id)
        cur = connection.cursor()
        cur.execute(insert_user)
        connection.commit()
    except mysql.connector.Error as e:
        print(e)

# Connect to server
connection = mysql.connector.connect(
    host=config.my_sql_host,
    user=config.my_sql_user,
    password=config.my_sql_password,
    database=config.my_sql_database
    )



