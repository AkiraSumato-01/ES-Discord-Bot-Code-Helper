# python3.6
# coding: utf-8

import discord
from discord.ext import commands
from random import randint

import utils.helpbook as help_

commandlist = '''
?commands - данный список команд;
?help - справка по коду;
?clear - очистка чата;
?errors - [INDEV] описание исключений;
'''

class Help(object):
    """Команды справки."""

    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='commands', description='Список команд.')
    @commands.guild_only()
    async def commands(self, ctx):
        """Список команд."""
        if ctx.channel.id != 496385320644902912 and ctx.channel.id != 496630762536435725:
            channel = discord.utils.get(ctx.guild.channels, id=496385320644902912)
            return await ctx.send(f'Команды допущены только в канале {channel.mention}.',
                                                                delete_after=8)
        
        await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at,
                                           color=randint(0x000000, 0xFFFFFF),
                                           title='Список команд.',
                                           description=commandlist
                                           ))


    @commands.command(name='errors', description='Помощь по коду.')
    @commands.guild_only()
    async def errors(self, ctx, tag: str = None):
        """Описание исключений."""
        if ctx.channel.id != 496385320644902912 and ctx.channel.id != 496630762536435725:
            channel = discord.utils.get(
                ctx.guild.channels, id=496385320644902912)
            return await ctx.send(f'Команды допущены только в канале {channel.mention}.',
                                  delete_after=8)
        
        await ctx.send('Вот незадача! А тут еще ничего нет... :thinking::thinking:')


    @commands.command(name='help', description='Помощь по коду.')
    @commands.guild_only()
    async def help(self, ctx, tag: str = None):
        """Помощь по коду."""
        if ctx.channel.id != 496385320644902912 and ctx.channel.id != 496630762536435725:
            channel = discord.utils.get(ctx.guild.channels, id=496385320644902912)
            return await ctx.send(f'Команды допущены только в канале {channel.mention}.',
                                                                delete_after=8)

        if tag not in help_.available_tags:
            return await ctx.send(f'Доступные теги: \n{", ".join(help_.available_tags)}')
        
        await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at,
                                           color=randint(0x000000, 0xFFFFFF),
                                           title='Справка: %s' % tag,
                                           description=help_.content(tag)
                                           ))



def setup(bot):
    bot.add_cog(Help(bot))
    print('>> Модуль help.py загружен.')
