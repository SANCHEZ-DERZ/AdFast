import telebot as tb
from telebot import types


bot = tb.TeleBot('7217498415:AAEUnbS0-C4jOl64ncBGL5d7VeKrTGjQXMU')


@bot.message_handler()
def message_get(message):
    if message.text.lower() == '/start':
        bot.send_message(message.chat.id, message)
    '''
    elif message.text.lower() == '/info':
        bot.send_message(message.chat.id, 'тестовый бот')
    elif message.text.lower() == '/site':
        markup = types.InlineKeyboardMarkup()
        btn_my_site = types.InlineKeyboardButton("hala madrid", url="https://youtu.be/B7ZO5UjswHM?si=Bze7rERGuFkZvH-T&t=586")
        markup.add(btn_my_site)
        bot.send_message(message.chat.id, "Выберите сайт:", reply_markup=markup)
'''

bot.polling(non_stop=True)

