# python3.6
# coding: utf-8

import discord
import asyncio
from discord.ext import commands
import aiohttp

class Default(object):
    """Стандартные команды."""

    def __init__(self, bot):
        self.bot = bot
    
    async def _hastebin_post(self, text):
        async with aiohttp.ClientSession() as session:
            async with session.post("https://hastebin.com/documents", data=text.encode('utf-8')) as post:
                post = await post.json()
                return "https://hastebin.com/{}".format(post['key'])
    
    @commands.command(name='hastebin', description='Опубликовать код на HASTEBIN.')
    @commands.guild_only()
    async def hastebin(self, ctx, *, code:str=None):
        """Опубликовать код на HASTEBIN."""
        if not code:
            await ctx.send(embed=discord.Embed(
                            timestamp=ctx.message.created_at,
                            color=0xFF0000).set_footer(
                                text='Что публиковать-то?\nВы, сударь, не написали текст после команды.'),
                                delete_after=10)
            await asyncio.sleep(10)
            await ctx.message.delete()
            return False

        given_url = await self._hastebin_post(code)
        await ctx.send('Данный код теперь доступен по ссылке: ' + given_url)
    
    @commands.command(name='clear', description='Очистка чата.', aliases=['purge'])
    @commands.guild_only()
    async def clear(self, ctx, count:int=None):
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
        
        if not count:
            await ctx.send(embed=discord.Embed(
                            timestamp=ctx.message.created_at,
                            color=0xFF0000).set_footer(
                                text='Введите кол-во сообщений, подлежащих удалению.'),
                                delete_after=10)
            await asyncio.sleep(10)
            await ctx.message.delete()
            return False
        
        await ctx.channel.purge(limit=count)
        await ctx.send('Успешно исполнено!', delete_after=5)


def setup(bot):
    bot.add_cog(Default(bot))
    print('>> Модуль default.py загружен.')
