# python3.6
# coding: utf-8

import discord
from discord.ext import commands
from random import randint

import utils.helpbook as help_

commandlist = '''
`?cmds` - данный список команд;
`?help` - справка по коду;
`?clear` - очистка чата;
`?errors` - [INDEV] описание исключений;
'''

class Help(object):
    """Команды справки."""

    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='cmds', description='Список команд.')
    async def cmds(self, ctx):
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


    @commands.command(name='errors', description='Описание исключений.')
    async def errors_(self, ctx):
        """Описание исключений."""
        if ctx.channel.id != 496385320644902912 and ctx.channel.id != 496630762536435725:
            channel = discord.utils.get(
                ctx.guild.channels, id=496385320644902912)
            return await ctx.send(f'Команды допущены только в канале {channel.mention}.',
                                  delete_after=8)
        
        await ctx.send('Вот незадача! А тут еще ничего нет... :thinking::thinking:')


    @commands.command(name='help', description='Помощь по коду.')
    async def help(self, ctx, tag: str = None):
        """Помощь по коду."""
        if ctx.channel.id != 496385320644902912 and ctx.channel.id != 496630762536435725:
            channel = discord.utils.get(ctx.guild.channels, id=496385320644902912)
            return await ctx.send(f'Команды допущены только в канале {channel.mention}.',
                                                                delete_after=8)

        list_tags = "\n".join(help_.available_tags_dig_list)

        if tag not in help_.available_tags or tag.isdigit() or tag == None:
            if tag == None:
                return await ctx.send(f'Доступные теги: \n```{list_tags}```')
            if tag.isdigit():
                try:
                    help_.available_tags_dig_list[int(tag)]

                except:
                    return await ctx.send(f'Доступные теги: \n```{list_tags}```')
            else:
                return await ctx.send(f'Доступные теги: \n```{list_tags}```')

        await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at,
                                           color=randint(0x000000, 0xFFFFFF),
                                           title='Справка: %s' % tag,
                                           description=help_.content(tag)
                                           ))



def setup(bot):
    bot.add_cog(Help(bot))
    print('>> Модуль help.py загружен.')
