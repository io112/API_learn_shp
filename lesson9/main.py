import logging
import os
import time

import flask
import telebot

app = flask.Flask(__name__)
api_key = os.getenv('API_KEY', 'define me')
bot = telebot.TeleBot(api_key)

WEBHOOK_HOST = '4a372d72591a.ngrok.io'
WEBHOOK_PORT = 443
WEBHOOK_URL = f'https://{WEBHOOK_HOST}:{WEBHOOK_PORT}/{api_key}'


@bot.message_handler(content_types=['text'])
def text(message):
    bot.reply_to(message, 'это текст')


@app.route(f'/{api_key}', methods=['POST'])
def tg():
    if flask.request.headers.get('content-type') == 'application/json':
        data = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(data)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    # Setup bot webhook
    bot.delete_webhook()
    time.sleep(0.1)
    bot.set_webhook(WEBHOOK_URL)

    # run Flask
    app.run()
