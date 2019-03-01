import discord
from discord.ext import commands

class NotOwner(commands.CheckFailure):
    pass

owners = [297421244402368522, 293411329866334218]

def owner():
    async def predicate(ctx):
        if ctx.author.id in owners or ctx.author.id == ctx.bot.owner.id:
            return True
        else:
            raise NotOwner()

    return commands.check(predicate)