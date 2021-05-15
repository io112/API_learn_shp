import os
from datetime import datetime

from discord import Client, TextChannel, User, Guild
from telebot import TeleBot

TOKEN = os.getenv('TOKEN')
LOG_CHANNEL_NAME = 'system_log'


def get_log_channel(guild: Guild):
    log_channels = [channel for channel in guild.channels if channel.name == LOG_CHANNEL_NAME]
    if len(log_channels) > 0:
        return log_channels[0]


bot = TeleBot(os.environ.get('TG_TOKEN'))


@bot.message_handler(content_types=['location'])
def get_loc(message):
    longitude = message.location.longitude
    latitude = message.location.latitude
    bot.reply_to(message, f'Ваша позиция:\nШирота: {latitude}\nДолгота {longitude}')


@bot.message_handler(content_types=['text'])
def text(message):
    bot.reply_to(message, 'это текст')


class EchoBot(Client):

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith('$hello'):
            text = f'Hello {message.author}!'
            await message.channel.send(text)

    async def on_typing(self, channel: TextChannel, user: User, when: datetime):
        log_channel = get_log_channel(channel.guild)
        if user == self.user:
            return
        await log_channel.send(f'Пользователь {user} пишет в канал "{channel.name}"')

    async def on_message_delete(self, message):
        await message.channel.send(f'Удалять сообщения нехорошо, '
                                   f'пользователь {message.author} написал {message.content}')

    async def on_message_edit(self, before, after):
        await before.channel.send(f'Редактировать сообщения нехорошо, '
                                  f'пользователь {before.author} написал {before.content}, а теперь {after.content}')

    async def on_ready(self):
        print(f'Я подключился к дискорду: {self.user}')


if __name__ == '__main__':
    client = EchoBot()
    client.run(TOKEN)
    bot.polling()
