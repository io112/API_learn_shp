from telebot import TeleBot
from telebot.types import Message

bot = TeleBot('1697333266:AAHm6JD9mWWbRr5tgh7tHLAGdVI6VqNhFW4')


@bot.message_handler(content_types=['location'])
def get_loc(message: Message):
    longitude = message.location.longitude
    latitude = message.location.latitude
    bot.reply_to(message, f'Ваша позиция:\nШирота: {latitude}\nДолгота {longitude}')


@bot.message_handler(content_types=['text'])
def text(message: Message):
    bot.reply_to(message, 'это текст')


if __name__ == '__main__':
    bot.polling(none_stop=True)
