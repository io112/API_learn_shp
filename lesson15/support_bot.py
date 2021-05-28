import os

from discord import Reaction, Message
from discord.ext import commands

TOKEN = os.getenv('TOKEN', 'define me')
bot = commands.Bot(command_prefix='!')
last_support_ticket = 1


@bot.command()
async def start_support(ctx):
    message = await ctx.send('Click to get support')
    await message.add_reaction('😁')


@bot.event
async def on_reaction_add(reaction: Reaction, user):
    global last_support_ticket
    message: Message = reaction.message
    guild = message.guild
    await guild.create_text_channel(name=f'ticket-{last_support_ticket}')
    last_support_ticket += 1


if __name__ == '__main__':
    bot.run(TOKEN)
