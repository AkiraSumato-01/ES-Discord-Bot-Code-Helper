# python3.6
# coding: utf-8

# Разработка AkiraSumato_01
# Специально для Discord сервера "Создание мода | Бесконечное Лето"
# https://discord.gg/EDh8F3F

import os
import sys
import time
import asyncio
import traceback
import aiohttp

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='?')
bot.remove_command('help')

extensions = ['cogs.help',
              'cogs.owner',
              'cogs.default',
              'cogs.error_handler']

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Не удалось загрузить модуль {extension}.', file=sys.stderr)
            traceback.print_exc()

@bot.event
async def on_ready():
    try:
        await bot.change_presence(activity=discord.Game(name='?help', type=0))
    except:
        await bot.change_presence(game=discord.Game(name='?help', type=0))
    print(f'[{time.ctime()}] Подключение успешно осуществлено!\nВ сети: {bot.user}')

bot.run(os.getenv('TOKEN'),
        bot=True, reconnect=True)
