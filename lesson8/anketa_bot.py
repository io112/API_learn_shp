import logging
import os

from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, ForceReply, ReplyKeyboardRemove

api_key = os.getenv('API_KEY', 'define me')

bot = TeleBot(api_key)


@bot.message_handler(commands=['anketa'])
def anketa(message: Message):
    bot.send_message(message.chat.id, 'Режим анкеты включен, введите имя',
                     reply_markup=ForceReply(selective=False))
    bot.register_next_step_handler(message, handle_name)


def handle_name(message: Message):
    if message.text in ['cancel', 'отмена']:
        bot.send_message(message.chat.id, 'Заполнение анкеты прервано')
        return
    bot.send_message(message.chat.id, 'Имя введено, введите фамилию')
    bot.register_next_step_handler(message, handle_surname)


def handle_surname(message: Message):
    if message.text in ['cancel', 'отмена']:
        bot.send_message(message.chat.id, 'Заполнение анкеты прервано')
        return
    keyboard = ReplyKeyboardMarkup(row_width=6)
    keyboard.add(*[KeyboardButton(str(year)) for year in range(1960, 2011, 10)])
    bot.send_message(message.chat.id, 'Имя введено, введите десятилетие рождения', reply_markup=keyboard)
    bot.register_next_step_handler(message, handle_year)


def handle_year(message: Message):
    if message.text in ['cancel', 'отмена']:
        bot.send_message(message.chat.id, 'Заполнение анкеты прервано')
        return
    if not message.text.isdigit():
        bot.send_message(message.chat.id, 'Вы ввели не число, хаха, заново')
        bot.register_next_step_handler(message, handle_year)
        return
    bot.send_message(message.chat.id, 'Десятилетие введено, анкета завершена!',
                     reply_markup=ReplyKeyboardRemove())


@bot.message_handler(func=lambda message: message.text.isdigit())
def text(message: Message):
    bot.send_message(message.chat.id, 'Это число')


@bot.message_handler(content_types=['text'])
def text(message: Message):
    bot.send_message(message.chat.id, f'Это текст {message.text}')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    bot.polling(none_stop=True)
