from getpass import getpass
from mysql.connector import connect, Error


choise = {"category" : "IT", "count" : "10.000-", "socnet" : "Telegram"}

try:
    with connect(
        host="localhost",
        user="root",
        password="Alex2140",
        database="users_adfast"
    ) as connection:
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
        selecting = f"""SELECT name, subscribers, description, contact FROM sources
            WHERE category = "%s" and subscribers BETWEEN %d and %d and platform = "%s"
            ORDER BY subscribers DESC
        """ % (choise['category'], l_border, r_border, choise['socnet'])
        cur = connection.cursor()
        cur.execute(selecting)
        rows = cur.fetchall()
        connection.commit()
        # Преобразуем rows в список
        result_list = [row for row in rows]  # Список кортежей
        # Если нужно получить плоский список значений из первого столбца:
        flat_list = [row[0] for row in rows]  # Плоский список значений
        print(result_list[5])
except Error as e:
    print(e)


