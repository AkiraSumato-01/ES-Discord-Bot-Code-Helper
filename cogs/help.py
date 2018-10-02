import discord
from discord.ext import commands
from random import randint

import utils.helpbook as help_


class Help(object):
    """Команда справки по Ren'Py коду."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def help(self, ctx, tag:str = None):
        if ctx.channel.id != 496385320644902912:
            channel = discord.utils.get(ctx.guild.channels, id=496385320644902912)
            return await ctx.send(f'Команды допущены только в канале {channel.mention}.',
                                                                delete_after=8)

        if tag not in help_.available_tags:
            return await ctx.send(f'Доступные теги: \n{", ".join(help_.available_tags)}')
        
        await ctx.send(embed=discord.Embed(color=randint(0x000000, 0xFFFFFF),
                                           title='Справка: %s' % tag,
                                           description=help_.content(tag)
                                           ))



def setup(bot):
    bot.add_cog(Help(bot))
    print('>> Модуль help.py загружен.')
