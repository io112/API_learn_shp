from telebot import TeleBot

api_key = '<TOKEN>'

bot = TeleBot(api_key)
stats = {}


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Oh, hi there!")


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, 'start - Начать общение\nhelp - Посмотреть все команды')


@bot.message_handler()
def echo(message):
    bot.send_message(message.chat.id, f'Hi, '
                                      f'{message.from_user.first_name} {message.from_user.last_name}')
    username = message.from_user.username
    if username not in stats:
        stats[username] = 0
        bot.reply_to(message, "Привет, новенький")
    stats[username] += 1
    bot.reply_to(message, f"Количество сообщений {stats[username]}")


if __name__ == '__main__':
    bot.polling(none_stop=True)
