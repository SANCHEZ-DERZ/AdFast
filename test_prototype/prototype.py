#подключение библиотек
import telebot
from telebot import types
import os
import sys
sys.path.append(os.getcwd())
from AdFast.sql_database import sql_requests
import functions
#подключение бота к коду через ключ
bot = telebot.TeleBot('7224861304:AAEg-57ikPQaxWCBGc7f2E-w79WiCXV7uIU')

choise = {"category" : "", "count" : "", "socnet" : ""}
#выполнение команды /start, создание кнопки к сообщению, добавление пользователя в бд
@bot.message_handler(commands=['start'])
def start(message):
    functions.start_func(message, bot)
    
#ответ на кнопку "начать поиск рекламы", создание cтраниц с категориями
@bot.callback_query_handler(func=lambda call: call.data == 'start_search')
def callback_start(call):
    functions.page_category(call, bot)

#переключение на страницу вперед
@bot.callback_query_handler(func=lambda call: call.data == 'forward_page_category')
def forward_callback(call):
    functions.forward_callback_func(call, bot)

#переключение на страницу назад   
@bot.callback_query_handler(func=lambda call: call.data == 'back_page_category')
def back_callback(call):
    functions.back_callback_func(call, bot)
    
#Выбор количества подписчиков
@bot.callback_query_handler(func=lambda call: call.data.startswith('category'))
def category_callback(call):
    choise['category'] = call.data[9:]
    functions.category_callback_func(call, bot)

#Возврат при неправильном выборе кол-ва подписчиков
@bot.callback_query_handler(func=lambda call: call.data == 'back_count')
def back_count_callback(call):
    functions.back_count_callback_func(call, bot)
    
    
#Выбор соц-сети
@bot.callback_query_handler(func=lambda call: call.data.startswith('count'))
def count_callback(call):
    choise['count'] = call.data[6:]
    functions.count_callback_func(call, bot)

#Возврат при неправильном выборе соц сети
@bot.callback_query_handler(func=lambda call: call.data == 'back_social_network')
def back_socnet_callback(call):
    functions.category_callback_func(call, bot)

#Выдача списка после выбора соц сети
@bot.callback_query_handler(func=lambda call: call.data.startswith('socnet'))
def socnet_callback(call):
    choise['socnet'] = call.data[7:]
    print(choise['category'], choise['count'], choise['socnet'])
    functions.socnet_callback_func(call, bot)

bot.polling()



# Close connection

sql_requests.connection.close()