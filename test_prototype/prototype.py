#подключение библиотек
import telebot
from telebot import types
import os
import sys
sys.path.append(os.getcwd())
from sql_database import sql_requests


#подключение бота к коду через ключ
bot = telebot.TeleBot('7224861304:AAEg-57ikPQaxWCBGc7f2E-w79WiCXV7uIU')
count_pages = {'category pages': 1}
max_pages = {'category pages': 2}

#выполнение команды /start, создание кнопки к сообщению, добавление пользователя в бд
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton("Начать поиск места для рекламы", callback_data="start")
    markup.add(start_button)
    bot.send_message(message.chat.id,
f"""Приветствую, {message.from_user.first_name}!
Это тестовый прототип дизайна бота FastAd.
Дальнейший функционал будет добавлен позже.
А пока можно потыкать на кнопки ниже :)""", 
reply_markup=markup)
    sql_requests.adding_user_in_database(message.from_user.first_name, message.from_user.id)



def page1_category(call):
    bot.send_message(call.message.chat.id, f'{count_pages["category pages"]} страница категорий из {max_pages["category pages"]} страниц')
    bot.answer_callback_query(call.id, text="Вы нажали кнопку 'Начать'")
    markup = types.InlineKeyboardMarkup()
    category1_btn = types.InlineKeyboardButton("Категория 1", callback_data="category1")
    category2_btn = types.InlineKeyboardButton("Категория 2", callback_data="category2")
    markup.row(category1_btn, category2_btn)
    category3_btn = types.InlineKeyboardButton("Категория 3", callback_data="category3")
    category4_btn = types.InlineKeyboardButton("Категория 4", callback_data="category4")
    markup.row(category3_btn, category4_btn)
    move_forward_btn = types.InlineKeyboardButton('Вперед', callback_data='forward')
    move_back_btn = types.InlineKeyboardButton('Назад', callback_data='back')
    markup.row(move_back_btn, move_forward_btn)
    bot.send_message(call.message.chat.id, 'Выбирите категорию ресурса, где хотите разместить рекламу', reply_markup=markup)

#ответ на кнопку "начать поиск рекламы", создание кнопок с категориями
@bot.callback_query_handler(func=lambda call: call.data == 'start')
def callback_start(call):
    page1_category(call)


def page2_category(call):
    bot.send_message(call.message.chat.id, f'{count_pages["category pages"]} страница категорий из {max_pages["category pages"]} страниц')
    markup = types.InlineKeyboardMarkup()
    category5_btn = types.InlineKeyboardButton("Категория 5", callback_data="category5")
    category6_btn = types.InlineKeyboardButton("Категория 6", callback_data="category6")
    markup.row(category5_btn, category6_btn)
    category7_btn = types.InlineKeyboardButton("Категория 7", callback_data="category7")
    category8_btn = types.InlineKeyboardButton("Категория 8", callback_data="category8")
    markup.row(category7_btn, category8_btn)
    move_forward_btn = types.InlineKeyboardButton('Вперед', callback_data='forward')
    move_back_btn = types.InlineKeyboardButton('Назад', callback_data='back')
    markup.row(move_back_btn, move_forward_btn)
    bot.send_message(call.message.chat.id, 'Выбирите категорию ресурса, где хотите разместить рекламу', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'forward')
def forward_callback(call):
    bot.answer_callback_query(call.id, text="Вы нажали кнопку 'Вперед'")
    if count_pages["category pages"] != max_pages["category pages"]:
        count_pages["category pages"] = count_pages.get("category pages") + 1
    page2_category(call)


@bot.callback_query_handler(func=lambda call: call.data == 'back')
def back_callback(call):
    bot.answer_callback_query(call.id, text="Вы нажали кнопку 'Назад'")
    if count_pages["category pages"] != 1:
        count_pages["category pages"] = count_pages.get("category pages") - 1
    callback_start(call)

bot.polling()

# Close connection
sql_requests.connection.close()