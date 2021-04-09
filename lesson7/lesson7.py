# @shp_bot
import os
from urllib.request import urlretrieve

from telebot import TeleBot

api_key = os.getenv('API_KEY', 'define me')

bot = TeleBot(api_key)
cat_gif = None
cat_video = None


@bot.message_handler(commands=['send_gif'])
def send_picture(message):
    global cat_gif
    if cat_gif is None:
        cat_gif = bot.send_animation(message.chat.id, open('../img/cat2.gif', 'rb'))
    else:
        bot.send_animation(message.chat.id, cat_gif.animation.file_id)


@bot.message_handler(commands=['send_video'])
def send_picture(message):
    global cat_video
    if cat_video is None:
        cat_video = bot.send_video(message.chat.id, open('../img/cat1.gif', 'rb'))
    else:
        bot.send_video(message.chat.id, cat_video.video.file_id)


@bot.message_handler(content_types=['photo'])
def reply_photo(message):
    bot.reply_to(message, 'Спасибо за фотографию!')
    file_id = message.photo[0].file_id
    file_path = bot.get_file(file_id).file_path
    url = f'https://api.telegram.org/file/bot{api_key}/{file_path}'
    urlretrieve(url, 'test.jpg')


@bot.message_handler(content_types=['document'])
def reply_photo(message):
    bot.reply_to(message, 'Спасибо за файл!')
    file_id = message.document.file_id
    file_path = bot.get_file(file_id).file_path
    print(file_path)
    url = f'https://api.telegram.org/file/bot{api_key}/{file_path}'
    urlretrieve(url, file_path)


@bot.message_handler(content_types=['text'])
def formatting(message):
    bot.send_message(message.chat.id,
                     f'```{message.text}```', parse_mode='MarkdownV2')


if __name__ == '__main__':
    bot.polling(none_stop=True)
