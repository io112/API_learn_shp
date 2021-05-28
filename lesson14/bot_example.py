import os
from typing import Optional

import requests as requests
from discord import Embed, Guild, Role, Member
from discord.ext import commands
from discord.ext.commands import Context
import logging

history = []
# intents = Intents().default()
# intents.members = True
bot = commands.Bot(command_prefix='!')


def get_panda_image() -> str:
    img = requests.get('https://some-random-api.ml/img/red_panda')
    img_link = img.json()['link']
    return img_link


def get_role(guild: Guild, role_name: str) -> Optional[Role]:
    for role in guild.roles:
        if role_name == role.name:
            return role
    return None


@bot.command()
async def set_role(ctx: Context, member: str, role_name: str):
    user = ctx.author
    # for m in ctx.guild.members:
    #     m: Member
    #     if member == m.display_name:
    #         user = m
    role = get_role(ctx.guild, role_name)
    if user is None or role is None:
        await ctx.send('Пользователь или роль не найдена')
        return
    await user.add_roles(role)
    await ctx.send('роль присвоена')


@bot.command()
async def foo(ctx: Context, text='Привет'):
    await ctx.send(text)


@bot.command()
@commands.has_role('test')
async def panda(ctx: Context, arg1='', arg2=1):
    history = []
    # with open('history.txt') as f:
    #     history.append(f.readline().strip())
    if arg1 == 'history':
        try:
            arg2 = int(arg2)
        except:
            await ctx.send('Некорректный ввод')
            return
        if arg2 > len(history):
            await ctx.send('Слишком больше число')
            return
        e = Embed()
        e.set_image(url=history[arg2 - 1])
        await ctx.send(embed=e)
        return
    else:
        img_link = get_panda_image()
        # with open('history.txt', 'wr') as f:
        #     text = f.read()
        #     f.write(img_link + '\r\n' + text)
        e = Embed()
        e.set_image(url=img_link)
        await ctx.send(embed=e)


@bot.event
async def on_ready():
    print('Я пришел')


@bot.event
async def on_message(message: Message):
    await message.channel.send('Обрабатываю.')
    await bot.process_commands(message)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    bot.run(os.environ.get('TOKEN'))
