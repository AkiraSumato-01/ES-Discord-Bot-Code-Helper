# python3.6
# coding: utf-8

import discord
from discord.ext import commands
from random import randint

import utils.helpbook as help_
import io

commandlist = '''
`?cmds` - данный список команд;
`?help [тег]` - справка по коду;
`?clear [кол-во сообщений]` - очистка чата;
`?buns` - плюшки;
`?hastebin [код]` - опубликовать код на hastebin.com;
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

        if tag not in help_.available_tags or tag.isdigit() or tag is None:
            if tag == None:
                return await ctx.send(f'Доступные теги: \n```{list_tags}```')
            if tag.isdigit():
                try:
                    help_.available_tags_dig_list[int(tag)]

                except:
                    return await ctx.send(f'Доступные теги: \n```{list_tags}```')
            else:
                return await ctx.send(f'Доступные теги: \n```{list_tags}```')

        if tag.isdigit():
            tag_show = tag + ' ' + help_.available_tags[int(tag)-1]

        else:
            for i in range(len(help_.available_tags)):
                if help_.available_tags[i] == tag:
                    tag_show = str(i+1) + ' ' + tag

        await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at,
                                           color=randint(0x000000, 0xFFFFFF),
                                           title='Справка: %s' % tag_show,
                                           description=help_.content(tag)
                                           ))


    @commands.command(name='buns', description='Плюшки.')
    async def buns(self, ctx):
        """Плюшки."""
        if not ctx.author.permissions_in(ctx.channel).manage_messages:
            await ctx.send(embed=discord.Embed(
                            timestamp=ctx.message.created_at,
                            color=0xFF0000).set_footer(
                                text='Удивительно! Вы пытаетесь использовать команду, \
                                но у Вас нет прав!'),
                                delete_after=10)
        if ctx.channel.id != 496385320644902912 and ctx.channel.id != 496630762536435725:
            channel = discord.utils.get(ctx.guild.channels, id=496385320644902912)
            return await ctx.send(f'Команды допущены только в канале {channel.mention}.',
                     delete_after=8)

        await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at,
                                     color=randint(0x000000, 0xFFFFFF),
                                     title='Плюшки.',
                                     description=io.open('buns.txt', 'r', encoding='utf-8').read()
                                     ))
def setup(bot):
    bot.add_cog(Help(bot))
    print('>> Модуль help.py загружен.')
