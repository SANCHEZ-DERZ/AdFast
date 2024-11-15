import telebot
from telebot import types
import os
import sys
sys.path.append(os.getcwd())
from AdFast.sql_database import sql_requests

pages = {'page': 1, 'max_page' : 2}

def start_func(message, bot):
    markup = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton("Начать поиск места для рекламы", callback_data="start_search")
    markup.add(start_button)
    bot.send_message(message.chat.id,
f"""Приветствую, {message.from_user.first_name}!
Это тестовый прототип дизайна бота FastAd.
Дальнейший функционал будет добавлен позже.
А пока можно потыкать на кнопки ниже :)""", 
reply_markup=markup)
    sql_requests.adding_user_in_database(message.from_user.first_name, message.from_user.id)


def page_category(call, bot):
    markup = types.InlineKeyboardMarkup()
    lst_categories = ["Fashion", "IT", "Travel", "Busines", "Beauty"]
    rows = [] # создаю пустой массив для кнопок
    start_ind = (pages["page"] - 1) * 4 # определяю стартовый индекс из списка
    ind = start_ind
    while (ind < len(lst_categories) and ind < start_ind + 4): # Добавляю либо 4 кнопки по 2 в строку, либо иду до конца списка
        if len(rows) == 2:
            markup.row(rows[0], rows[1])
            rows = []
        category_btn = types.InlineKeyboardButton(lst_categories[ind], callback_data=f'category {lst_categories[ind]}')
        rows.append(category_btn)
        ind += 1
    # добавляю оставшиеся в массиве кнопки в последнюю строку
    if len(rows) == 2:
        markup.row(rows[0], rows[1])
    else:
        markup.row(rows[0])
    # определяю и добавляю нужные "кнопки перемещения" по страницам
    if pages["page"] == 1 and pages["page"] != pages["max_page"]:
        move_forward_btn = types.InlineKeyboardButton('Вперед', callback_data='forward_page_category')
        markup.row(move_forward_btn)
    elif pages["page"] != 1 and pages["page"] == pages["max_page"]:
        move_back_btn = types.InlineKeyboardButton('Назад', callback_data='back_page_category')
        markup.row(move_back_btn)
    else:
        move_forward_btn = types.InlineKeyboardButton('Вперед', callback_data='forward_page_category')
        move_back_btn = types.InlineKeyboardButton('Назад', callback_data='back_page_category')
        markup.row(move_forward_btn, move_back_btn)
    
    bot.send_message(call.message.chat.id, 'Выбирите категорию ресурса, где хотите разместить рекламу', reply_markup=markup)


def forward_callback_func(call, bot):
    bot.answer_callback_query(call.id, text="Вы нажали кнопку 'Вперед'")
    pages['page'] += 1
    page_category(call, bot)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    bot.delete_message(call.message.chat.id, call.message.message_id)


def back_callback_func(call, bot):
    bot.answer_callback_query(call.id, text="Вы нажали кнопку 'Назад'")
    pages['page'] -= 1
    page_category(call, bot)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    bot.delete_message(call.message.chat.id, call.message.message_id)


def category_callback_func(call, bot):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.answer_callback_query(call.id, text=f"Теперь выберите количество подписчиков:")
    # Создаем новую клавиатуру
    markup = types.InlineKeyboardMarkup()

    # Определяем названия кнопок, которые будут добавлены в клавиатуру
    button_names = ['10.000-', '10.000 - 50.000', '50.000-100.000', '100.000-500.000', '500.000-1.000.000', '1.000.000+']
    # Добавляем кнопки на клавиатуру
    for i in range(0, len(button_names), 2):
        button1 = types.InlineKeyboardButton(button_names[i], callback_data=f"count {button_names[i]}")
        button2 = types.InlineKeyboardButton(button_names[i + 1], callback_data=f"count {button_names[i + 1]}")
        markup.row(button1, button2)
    button_back = types.InlineKeyboardButton('Назад к категориям',callback_data=f'back_count')
    markup.row(button_back)
    bot.send_message(call.message.chat.id, 'Выберите желаемо количество аудитории', reply_markup=markup)


def back_count_callback_func(call, bot):
    pages['page'] = 1
    page_category(call, bot)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    bot.delete_message(call.message.chat.id, call.message.message_id)


def count_callback_func(call, bot):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.answer_callback_query(call.id, text=f"Выберите соц-сеть, в которой хотите разместить рекламу:")
    # Создаем новую клавиатуру
    markup = types.InlineKeyboardMarkup()

    # Определяем названия кнопок, которые будут добавлены в клавиатуру
    button_names = ['Instagam', 'Telegram', 'Tik-tok', 'Vk', 'YouTube', 'Yandex Dzen']
    # Добавляем кнопки на клавиатуру
    for i in range(0, len(button_names), 2):
        button1 = types.InlineKeyboardButton(button_names[i], callback_data=f"socnet {button_names[i]}")
        button2 = types.InlineKeyboardButton(button_names[i + 1], callback_data=f"socnet {button_names[i + 1]}")
        markup.row(button1, button2)
    button_back = types.InlineKeyboardButton('Назад к кол-ву аудитории',callback_data=f'back_social_network')
    markup.row(button_back)
    bot.send_message(call.message.chat.id, 'Выберите соц-сеть, в которой хотите разместить рекламу:', reply_markup=markup)

def socnet_callback_func(call, bot):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.answer_callback_query(call.id, text=f"Вот кандидаты на размещение рекламы:")
    bot.send_message(call.message.chat.id, 'Вот кандидаты на размещение рекламы:', reply_markup=None)