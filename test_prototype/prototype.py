import telebot
from telebot import types
import os
import sys
sys.path.append(os.getcwd())
from AdFast.sql_database import sql_requests
from AdFast.test_prototype.functions import lst, start_func, page_selection, socnet_callback_func, result_callback_func, cancell_func, forward_back


bot = telebot.TeleBot('7224861304:AAEg-57ikPQaxWCBGc7f2E-w79WiCXV7uIU')
choise = {'category': '', 'count': '', 'socnet': ''}

@bot.message_handler(commands=['start'])
def handle_start(message):
    start_func(message, bot)

@bot.callback_query_handler(func=lambda call: call.data.startswith('start_search'))
def start_callback(call):
    page_selection(call, bot, lst.category, 'category')

@bot.callback_query_handler(func=lambda call: call.data.startswith('cancel'))
def cancel(call):
    cancell_func(call, bot, item_type=(call.data.split('_')[1]))

@bot.callback_query_handler(func=lambda call: call.data.startswith(('category', 'count', 'socnet')))
def unified_callback(call):
    data_type = call.data.split(' ')[0]  # Получаем тип данных (category, count или socnet)
    value = call.data.split(' ')[1]  # Получаем значение

    if data_type == 'category':
        choise['category'] = value  # Получаем выбранную категорию
        page_selection(call, bot, lst.count, 'count')
    elif data_type == 'count':
        choise['count'] = value  # Получаем выбранное кол-во
        page_selection(call, bot, lst.socnet, 'socnet')
    elif data_type == 'socnet':
        choise['socnet'] = value  # Получаем выбранную соцсеть
        socnet_callback_func(call, bot, choise)

@bot.callback_query_handler(func=lambda call: call.data.startswith('forward') or call.data.startswith('back'))
def forward_back_callback(call):
    forward_back(call, bot)

@bot.callback_query_handler(func=lambda call: call.data.startswith('result'))
def result_callback(call):
    result_callback_func(call, bot, choise)


bot.polling()
sql_requests.connection.close()