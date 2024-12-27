import telebot
from telebot import types
import os
import sys
sys.path.append(os.getcwd())
from sql_database import sql_requests
from test_prototype.functions import lst, start_func, page_selection, socnet_callback_func, result_callback_func, cancell_func


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

@bot.callback_query_handler(func=lambda call: call.data.startswith('category'))
def category_callback(call):
    choise['category'] = call.data.split(' ')[1] # Получаем выбранную категорию
    page_selection(call, bot, lst.count, 'count')

@bot.callback_query_handler(func=lambda call: call.data.startswith('count'))
def count_callback(call):
    choise['count'] = call.data.split(' ')[1] # Получаем выбранное кол-во
    page_selection(call, bot, lst.socnet, 'socnet')

@bot.callback_query_handler(func=lambda call: call.data.startswith('socnet'))
def socnet_callback(call):
    choise['socnet'] = call.data.split(' ')[1]  # Получаем выбранную соцсеть
    socnet_callback_func(call, bot, choise)

@bot.callback_query_handler(func=lambda call: call.data.startswith('result'))
def result_callback(call):
      # Заполните нужные данные для choice
    result_callback_func(call, bot, choise)

bot.polling()
sql_requests.connection.close()