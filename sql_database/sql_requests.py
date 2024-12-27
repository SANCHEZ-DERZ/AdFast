import mysql.connector
from mysql.connector import connect, Error
import os
import sys
sys.path.append(os.getcwd())
import config as config


class DatabaseConnection:
    def __init__(self, host, user, password, database):
        self._host = host
        self._user = user
        self._password = password
        self._database = database
        self._connection = None

    def connect(self):
        try:
            self._connection = mysql.connector.connect(
                host=self._host,
                user=self._user,
                password=self._password,
                database=self._database
            )
            if self._connection.is_connected():
                print("Успешное подключение к базе данных")
        except Error as e:
            print(f"Ошибка при подключении к базе данных: {e}")

    def close(self):
        """Закрывает соединение с базой данных."""
        if self._connection and self._connection.is_connected():
            self._connection.close()
            print("Соединение с базой данных закрыто")
    
    def adding_user_in_database(self, user_name, user_id):
        try:
            insert_user = f"""INSERT INTO users_adfast (name, user_id)
            VALUES
                ('%s', '%s');
            """ % (user_name, user_id)
            cur = self._connection.cursor()
            cur.execute(insert_user)
            self._connection.commit()
        except mysql.connector.Error as e:
            print(e)

    #выбор столбца из таблицы, где %s означает имя столбца
    # пример работы функции:
    # print(selecting_info_of_source('name'))
    # >>> [('CodeCamp',), ('easyoffer',)]
    def selecting_info_of_source(self, command, category, subscribers_begin, subscribers_end, platform):
        try:
            selecting = f"""SELECT %s FROM sources
                WHERE category = "%s" and subscribers BETWEEN %d and %d and platform = "%s"
                ORDER BY subscribers DESC
            """ % (command, category, subscribers_begin, subscribers_end, platform)
            cur = self._connection.cursor()
            cur.execute(selecting)
            rows = cur.fetchall()
            self._connection.commit()
            # Преобразуем rows в список
            result_list = [row for row in rows]  # Список кортежей
            # Если нужно получить плоский список значений из первого столбца:
            flat_list = [row[0] for row in rows]  # Плоский список значений
            return flat_list
        except mysql.connector.Error as e:
            print(e)

    def getting_info_of_source(self, choise, num):
        l_border = 0
        r_border = 0
        if choise['count'][-1] == '-':
            l_border = 0
            r_border = 10000
        elif choise['count'][-1] == '+':
            l_border = 1000000
            r_border = 100000000
        else:
            temp_count = list(choise['count'].split('-'))
            l_border = int(temp_count[0].replace('.', ''))
            r_border = int(temp_count[1].replace('.', ''))
        try:
            selecting = f"""SELECT name, subscribers, description, contact FROM sources
                WHERE category = "%s" and subscribers BETWEEN %d and %d and platform = "%s"
                ORDER BY subscribers DESC
            """ % (choise['category'], l_border, r_border, choise['socnet'])
            cur = self._connection.cursor()
            cur.execute(selecting)
            rows = cur.fetchall()
            self._connection.commit()
            # Преобразуем rows в список
            result_list = [row for row in rows]  # Список кортежей
            return result_list[num]
        except mysql.connector.Error as e:
            print(e)


        

# Connect to server
connection = DatabaseConnection(config.my_sql_host, config.my_sql_user, config.my_sql_password, config.my_sql_database)

connection.connect()

