# python3.6
# coding: utf-8

import discord
import asyncio
from discord.ext import commands

class Default(object):
    """Стандартные команды."""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='clear', description='Очистка чата.', aliases=['purge'])
    @commands.guild_only()
    async def clear(self, ctx, count:int):
        """Очистка чата."""

        if not ctx.author.permissions_in(ctx.channel).manage_messages:
            await ctx.send(embed=discord.Embed(
                            timestamp=ctx.message.created_at,
                            color=0xFF0000).set_footer(
                                text='Удивительно! Вы пытаетесь использовать команду, \
                                но у Вас нет прав!'),
                                delete_after=10)
            await asyncio.sleep(10)
            await ctx.message.delete()
            return False
        
        await ctx.channel.purge(limit=count)
        await ctx.send('Успешно исполнено!', delete_after=5)


def setup(bot):
    bot.add_cog(Default(bot))
    print('>> Модуль default.py загружен.')
