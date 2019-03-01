# python3.6
# -*- coding: utf-8 -*-

import asyncio
import os
import sys

import traceback

import discord
import psutil
from discord.ext import commands

from checks import *

class Emergency(commands.Cog, name='Emergency'):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='modules', hidden=True, aliases=['cogs'])
    @owner()
    async def modules(self, ctx):
        """Список загруженных модулей.
        """
        cogs = [self.bot.cogs[e].__module__ for e in self.bot.cogs]
        unloaded = list()
        for cog in self.bot.modules:
            if cog not in cogs:
                unloaded.append(cog)
        embed = discord.Embed(timestamp=ctx.message.created_at, color=0x13CFEB)
        embed.add_field(name=':electric_plug: Подключенные модули:', value=chr(173))
        embed.add_field(name='%s Загруженные:' % ctx.bot.yes,
                        value='```%s```' % '\n'.join([f'• {x}' for x in self.bot.cogs]))
        if len(unloaded) == 0:
            unloaded = 'Видимо, все загружено.'
        else:
            unloaded = '\n'.join([f'• {x}' for x in unloaded])
        embed.add_field(name='%s Не загруженные:' % ctx.bot.no,
                        value='```%s```' % unloaded)
        await ctx.send(embed=embed)
    
    @commands.command(name='reload', hidden=True)
    @owner()
    async def cog_reload(self, ctx, *, cog: str):
        """Перезагрузка модуля.

        Аргументы:
        `:cogs` - имя модуля (включая директорию)
        __                                            __
        Например:
        ```
        n!reload cogs.fun
        ```
        """

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`Ошибка при перезагрузке модуля {cog}:`** \n{type(e).__name__} - {e}')
        else:
            await ctx.send(f'**`Модуль {cog} успешно перезагружен`**')
    

    @commands.command(name='add-file', hidden=True, aliases=['+file'])
    @owner()
    async def add_file(self, ctx, path: str = None):
        """Добавить файл.
        """
        if len(ctx.message.attachments) < 1:
            return await ctx.send('<:naomi_tick_no:525026037868789783> Вы не вложили к сообщению файл с кодом...')
        if len(ctx.message.attachments) > 1:
            return await ctx.send('<:online:455810041002459156> К сообщению вложено более одного файла... Ок, загружу все.')

        if not path:
            path = ''
        else:
            path += '/'

        for ext in ctx.message.attachments:
            full_path = path + f'{ext.filename}'
            await ext.save(full_path)

            await ctx.send(f'<:online:455810041002459156> Файл успешно загружен >> `{full_path}``', delete_after=10)
            await ctx.message.delete()

    @commands.command(name='err+cog', hidden=True, aliases=['e+cog'])
    @owner()
    async def add_cog(self, ctx):
        """Добавить модуль.
        """
        if len(ctx.message.attachments) < 1:
            return await ctx.send('<:naomi_tick_no:525026037868789783> Вы не вложили к сообщению файл с кодом...')
        if len(ctx.message.attachments) > 1:
            return await ctx.send('<:online:455810041002459156> К сообщению вложено более одного файла... Ок, загружу все.')

        for ext in ctx.message.attachments:
            full_path = f'cogs/{ext.filename}'
            await ext.save(full_path)
            new_path = ''

            for x in full_path:
                if x != '.':
                    new_path += x
                else:
                    break
            try:
                self.bot.unload_extension(new_path.replace('/', '.'))
                self.bot.load_extension(new_path.replace('/', '.'))
            except:
                await ctx.send(f'<:naomi_tick_no:525026037868789783> Модуль `{new_path.replace("/", ".")}` не удалось загрузить. Удаляю с хоста...\n```python\n{traceback.format_exc()}```', delete_after=15)
                os.remove(full_path)
            else:
                await ctx.send(f'<:online:455810041002459156> Успешно загружен >> `{new_path.replace("/", ".")}``', delete_after=10)
            await ctx.message.delete()

    @commands.command(name='emergency-restart', hidden=True, aliases=['err', 'erestart'])
    @owner()
    async def danger_restart(self, ctx):
        """Перезагрузка.
        """
        await self.bot.change_presence(activity=discord.Game(name=' перезагрузку...'), status=discord.Status.dnd)
        await ctx.send(embed=discord.Embed(color=0x13CFEB).set_footer(text="Перезагрузка..."))
        os.execl(sys.executable, sys.executable, * sys.argv)

def setup(bot):
    bot.add_cog(Emergency(bot))
