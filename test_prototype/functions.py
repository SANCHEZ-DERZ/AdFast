import telebot
from telebot import types
import os
import sys
sys.path.append(os.getcwd())
from AdFast.sql_database import sql_requests
from dataclasses import dataclass
from AdFast import pages_instance, lst, Button


def start_func(message, bot):
    markup = types.InlineKeyboardMarkup()
    markup.row(*create_inline_buttons([Button("Начать поиск места для рекламы", "start_search")]))
    bot.send_message(message.chat.id, f"Приветствую, {message.from_user.first_name}! Это тестовый прототип дизайна бота FastAd. Дальнейший функционал будет добавлен позже. А пока можно потыкать на кнопки ниже :)", reply_markup=markup)
    sql_requests.connection.adding_user_in_database(message.from_user.first_name, message.from_user.id)

def create_inline_buttons(buttons):
    result = []
    for button in buttons:
        result.append(types.InlineKeyboardButton(button.text, callback_data=button.callback_data))
    return result

def create_navigation_buttons(current_page, max_page, item_type):
    buttons = []
    if current_page > 1:
        buttons.append(Button('Назад', f'back_page {item_type}'))
    if current_page < max_page:
        buttons.append(Button('Вперед', f'forward_page {item_type}'))
    buttons = create_inline_buttons(buttons)
    return buttons

def update_pages(call, bot):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    bot.delete_message(call.message.chat.id, call.message.message_id)

def page_selection(call, bot, items, item_type):
    update_pages(call, bot)

    markup = types.InlineKeyboardMarkup()

    # Определяем страницу
    if item_type == 'result':
        pages_instance.max_page_result = len(items) // 4 + (1 if len(items) % 4 != 0 else 0)
     
    current_page = getattr(pages_instance, f'page_{item_type}', None)
    max_page = getattr(pages_instance, f'max_page_{item_type}', None)
    items_temp = items[(current_page - 1)* 4 : min((current_page - 1) * 4 + 4, len(items))]


    for i in range(0, len(items_temp), 2):
        buttons_on_page = []
        button1 = Button(items_temp[i], f'{item_type} {i + 1}' if item_type == 'result' else f'{item_type} {items_temp[i]}')
        buttons_on_page.append(button1)
        if i + 1 < len(items_temp):
            button2 = Button(items_temp[i + 1], f'{item_type} {i + 2}' if item_type == 'result' else f"{item_type} {items_temp[i + 1]}")
            buttons_on_page.append(button2)
        markup.row(*create_inline_buttons(buttons_on_page))
        
    
    # Добавляем кнопки навигации
    markup.row(*create_navigation_buttons(current_page, max_page, item_type))

    # Добавляем кнопку "Отмена"
    markup.add(types.InlineKeyboardButton("Отмена", callback_data=f'cancel_{item_type}'))

    # Определяем текст сообщения в зависимости от item_type
    item_texts = {
        'category': 'Выберите категорию:',
        'count': 'Выберите количество подписчиков:',
        'socnet': 'Выберите социальную сеть:',
        'result': 'Выберите канал:'
    }
    
    message_text = item_texts.get(item_type, "Выберите элемент:")  # Значение по умолчанию

    bot.send_message(call.message.chat.id, message_text, reply_markup=markup)

def cancell_func(call, bot, item_type):
    match item_type:
        case 'count':
            # Если item_type равно 'count', меняем его на 'category'
            new_item_type = 'category'
            page_selection(call, bot, lst.category, new_item_type)
        case 'result':
            # Если item_type равно 'result', меняем его на 'socnet'
            new_item_type = 'socnet'
            page_selection(call, bot, lst.socnet, new_item_type)
        case 'category':
            # Если item_type равно 'category', вызываем start_func
            start_func(call.message, bot)
        case 'socnet':
            # Если item_type равно 'socnet', меняем его на 'count'
            new_item_type = 'count'
            page_selection(call, bot, lst.count, new_item_type)


def socnet_callback_func(call, bot, choise):
    
    l_border, r_border = determine_borders(choise['count'])
    
    lst.result = sql_requests.connection.selecting_info_of_source('name', choise['category'], l_border, r_border, choise['socnet'])
    
    page_selection(call, bot, lst.result, 'result')

def determine_borders(count_choice):
    if count_choice[-1] == '-':
        return 0, 10000
    elif count_choice[-1] == '+':
        return 1000000, 100000000
    else:
        temp_count = list(count_choice.split('-'))
        return int(temp_count[0].replace('.', '')), int(temp_count[1].replace('.', ''))


def result_callback_func(call, bot, choice):
    num = int(call.data.split(' ')[1])
    
    channel_info = sql_requests.connection.getting_info_of_source(choice, num - 1)
    
    message = f"Название: '{channel_info[0]}'\nПодписчики: {channel_info[1]}\nОписание:\n{channel_info[2]}\nКонтакты:\n{channel_info[3]}"
    
    back_button = Button("Вернуться к началу", "start_search")
    
    markup = types.InlineKeyboardMarkup()
    markup.row(*create_inline_buttons([back_button]))
    
    bot.send_message(call.message.chat.id, message)
    bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=markup)

def forward_back(call, bot):

    callback_data = call.data.split()
    action = callback_data[0] 
    item_type = callback_data[1]

    attribute_map = {
        'category': 'page_category',
        'result': 'page_result',
        'count': 'page_count',
        'socnet': 'page_socnet'
    }

    attribute_name = attribute_map.get(item_type)

    if attribute_name:
        if action == 'forward_page':
            setattr(pages_instance, attribute_name, getattr(pages_instance, attribute_name) + 1)
        elif action == 'back_page':
            setattr(pages_instance, attribute_name, getattr(pages_instance, attribute_name) - 1)
    lst_name = getattr(lst, item_type)
    
    page_selection(call, bot, lst_name, item_type)

