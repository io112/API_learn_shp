from telebot import TeleBot
import os

from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

api_key = os.getenv('tg_api_key', 'define me')

bot = TeleBot(api_key)
stats = {}

auth_users = ['paramonod']


def auth(message: Message):
    return message.from_user.username in auth_users


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Oh, hi there!")


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, 'start - Начать общение\nhelp - Посмотреть все команды')


@bot.message_handler(commands=['test'], func=auth)
def test(message):
    bot.reply_to(message, 'Вы молодец')


@bot.message_handler(commands=['health'])
def test_health(message: Message):
    keyboard = ReplyKeyboardMarkup()
    keyboard.row(
        KeyboardButton('Хорошее'),
        KeyboardButton('Отличное'))
    keyboard.row(
        KeyboardButton('Превосходное'),
        KeyboardButton('Хорошее 2')
    )

    bot.send_message(message.chat.id, 'Как настроение?', reply_markup=keyboard)


@bot.message_handler(content_types=['text'], func=lambda message: len(message.text) < 3)
def wrong_text(message):
    bot.reply_to(message, 'Текст должен быть длиннее трех символов')


"""
[12]{2}  11 12 21 22
[12]{3} 111 112 121 122 211 221 222
"""


@bot.message_handler(content_types=['text'], func=lambda m: 'bot' in m.text or 'бот' in m.text)
def wrong_text(message):
    bot.reply_to(message, 'Кто звал бота??')


@bot.message_handler(content_types=['text'], regexp='^(https?)|(ftp)://')  # lambda m: m.text.find('http://') == 0
def link(message: Message):
    bot.send_message(message.chat.id, 'Мне прислали ссылку')


@bot.message_handler(content_types=['text'], regexp='Хорошее|Отличное|Превосходное|Хорошее 2')
def health(message: Message):
    bot.send_message(message.chat.id, 'Спасибо за ответ', reply_markup=ReplyKeyboardRemove())


@bot.message_handler(content_types=['sticker'])
def echo_sticker(message: Message) -> None:
    bot.send_message(message.chat.id, 'Это стикер')


@bot.message_handler(content_types=['text'])
def echo(message: Message) -> None:
    bot.send_message(message.chat.id, 'Это текст')


if __name__ == '__main__':
    bot.polling(none_stop=True)
