import mysql.connector
import os
import sys
sys.path.append(os.getcwd())
import config


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


#выбор столбца из таблицы, где %s означает имя столбца
# пример работы функции:
# print(selecting_info_of_source('name'))
# >>> [('CodeCamp',), ('easyoffer',)]
def selecting_info_of_source(command, category, subscribers_begin, subscribers_end):
    try:
        selecting = f"""SELECT %s FROM sources
            WHERE category = "%s" and subscribers BETWEEN %d and %d
        """ % (command, category, subscribers_begin, subscribers_end)
        cur = connection.cursor()
        cur.execute(selecting)
        rows = cur.fetchall()
        connection.commit()
        return rows
    except mysql.connector.Error as e:
        print(e)


def adding_source_in_database(name, link, platform, subscribers, category):
    try:
        insert_source = f"""INSERT INTO sources (name, link, platform, subscribers, category)
        VALUES
            ('%s', '%s', '%s', %d, '%s');
        """ % (name, link, platform, subscribers, category)
        cur = connection.cursor()
        cur.execute(insert_source)
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



