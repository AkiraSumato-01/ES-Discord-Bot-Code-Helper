import traceback
import sys
import discord
import time
from discord.ext import commands

"""
Error handler by EvieePy
    (https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612)

Edited by AkiraSumato-01
"""

class ErrorHandler:
    """Модуль обработки и оповещения об исключениях."""

    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return
        
        ignored = (commands.CommandNotFound, commands.UserInputError)
        
        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)
        
        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f'Команда "{ctx.command}" отключена.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(f'Команда "{ctx.command}" не может быть выполнена в ЛС.')
            except:
                pass

        # For this error example we check to see where it came from...
        elif isinstance(error, commands.BadArgument):
            return await ctx.send(f'Получен неверный тип аргумента в команде "{ctx.command}".')

        await ctx.send(f'{discord.utils.get(ctx.guild.roles, id=497043277292371969).mention}, возникло исключение...',
            embed=discord.Embed(
                timestamp=ctx.message.created_at,
                color=0xF56415, 
                title='ErrorHandler обнаружил ошибку!',
                description=f'Вызвано участником: {ctx.author}\nПодробности ошибки:```python\n{traceback.format_exc()}```\n```python\n{type(error).__name__}: {error}```')
            )







def setup(bot):
    bot.add_cog(ErrorHandler(bot))
    print('[error_handler.py] ErrorHandler загружен.')
