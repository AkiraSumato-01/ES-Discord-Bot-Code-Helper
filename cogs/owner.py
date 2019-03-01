# python3.6
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands

import asyncio
import io
import os
import platform
import sys
import textwrap
import traceback
import psutil
import json
from contextlib import redirect_stdout
from random import randint

from ShellExecutor import *
from checks import *


class Owner(object):
    def __init__(self, bot):
        self.bot = bot
        self.bot.yes = '✔️'
        self.bot.no = '❌'

    @commands.command('for', hidden=True, aliases=['cmdfor'])
    @owner()
    async def for_(self, ctx, command: str, arg: str, condition):

        await ctx.send(f'Выполняю команду `{command}` с условием `{arg}: {condition}`...')
        env = {'ctx': ctx}
        env.update(globals())

        exec(f'async def exfor():\n  for x in {condition}:\n    await ctx.invoke(ctx.bot.get_command("{command}"), {arg}=x)', env)

        func = env['exfor']
        await func()
 
        del(func)
        del(env)
        
        await ctx.send(f'Выполнено!')


    @commands.command(name='owncleanup', hidden=True, aliases=['ocup'])
    @commands.guild_only()
    @owner()
    @commands.bot_has_permissions(manage_messages=True)
    async def owner_cleanup(self, ctx, member: discord.Member, count: int):
        """[RU] Удалить сообщения конкретного участника (разработчик)
        [EN] Delete messages from a specific member (for my developer)
        """

        if count > 100:
            await ctx.send(f'<:naomi_tick_no:525026037868789783> {count} > 100.')
        else:
            def is_member(m):
                return m.author.id == member.id
            await ctx.channel.purge(limit=count, check=is_member)


    @commands.command('del-cog', hidden=True, aliases=['-cog'])
    @owner()
    async def del_cog(self, ctx, path: str):
        """[RU] Удалить модуль
        [EN] Delete module
        """
        try:
            os.remove(path.replace('.', '/') + '.py')
            await ctx.send(f'Успешно удален >> `{path}``')
        except Exception as e:
            await ctx.send(f'Не удалось >> `{path}``\n{type(e).__name__}: {e}')

    @commands.command('del-cmd', hidden=True, aliases=['-cmd'])
    @owner()
    async def del_command(self, ctx, cmd: str):
        """[RU] Удалить команду
        [EN] Delete command
        """
        try:
            self.bot.remove_command(cmd)
            await ctx.send(f'Успешно удален >> `{cmd}``')
        except Exception as e:
            await ctx.send(f'Не удалось >> `{cmd}``\n{type(e).__name__}: {e}')

    @commands.command(name='logout', hidden=True)
    @owner()
    async def logout(self, ctx):
        """[RU] Деавторизовать меня от Discord
        [EN] Logout me from Discord
        """
        def message_check(m):
            return m.author.id == ctx.author.id

        await ctx.send('Мне правда надо деавторизоваться?')
        msg = await self.bot.wait_for('message', check=message_check, timeout=120.0)

        if msg.content.lower() in ['да', 'ага', 'угу', 'давай уже']:
            await ctx.send('Хорошо, я деавтиризуюсь...')
        else:
            return await ctx.send('Остаюсь в сети...')

        await asyncio.sleep(1.2)
        await self.bot.logout()

    @commands.command(name='sysinfo', hidden=True, aliases=['sys', 'system'])
    @owner()
    async def sysinfo(self, ctx):
        """[RU] Системная информация
        [EN] System statistics
        """
        pid = os.getpid()
        py = psutil.Process(pid)

        embed = discord.Embed(timestamp=ctx.message.created_at,
                              color=randint(0x000000, 0xFFFFFF),
                              title='Системная статистика')

        embed.add_field(name='Процессор:',
                        value=f'▫ Кол-во ядер: {psutil.cpu_count()}\n'
                              f'▫ Загрузка: {round(psutil.cpu_percent())}%\n'
                              f'▫ Загрузка ботом: {round(py.cpu_percent())}%')
        embed.add_field(name='Оператива:',
                        value=f'▫ Объем: {psutil.virtual_memory().total\n'
                              f'▫ Загрузка: {round(psutil.virtual_memory().percent)}%\n'
                              f'▫ Загрузка ботом: {round(py.memory_percent())}%')
        embed.add_field(name='Текущий модуль:',
                        value='▫ ' + os.path.basename(__file__))
        embed.add_field(name='Имя процесса:',
                        value='▫ ' + py.name())
        embed.add_field(name='🖥 Платформа:',
                        value='▫ ' + platform.platform())
        embed.add_field(name='Пользователь:',
                        value='▫ ' + py.username())
        embed.add_field(name='Интерпретатор тут:',
                        value='▫ ' + sys.executable)
        embed.add_field(name=f'Discord.py {discord.__version__}',
                        value=chr(173))
        embed.add_field(name=f'Python {platform.python_version()}',
                        value=chr(173))
        
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.command}')

        await ctx.send(embed=embed)

    @commands.command(name='quit', aliases=['quitserver'], hidden=True)
    @owner()
    async def quit_guild(self, ctx, guild: discord.Guild):
        """[RU] Отключить меня от сервера
        [EN] Disconnect me from a server
        """
        try:
            await guild.leave()

        except:
            await ctx.send(f'Возникла ошибка:\n```{traceback.format_exc()}```')

    @commands.command(name='ping', hidden=True)
    @owner()
    async def ping(self, ctx):
        """[RU] Client & API latency
        [EN] Задержка API и клиента
        """

        resp = await ctx.send('Тестируем...')
        diff = resp.created_at - ctx.message.created_at
        await resp.edit(content=f':ping_pong: Pong!\nЗадержка API: {1000 * diff.total_seconds():.1f}мс.\nЗадержка {self.bot.user.name}: {round(self.bot.latency * 1000)}мс')

    @commands.command(hidden=True, aliases=['r'])
    @owner()
    async def restart(self, ctx):
        """[RU] Перезапуск
        [EN] Restart
        """
        await self.bot.change_presence(activity=discord.Game(name='перезагрузка...'), status=discord.Status.dnd)
        await ctx.send(embed=discord.Embed(color=0x13CFEB).set_footer(text="Перезагружаемся..."))
        os.execl(sys.executable, sys.executable, * sys.argv)

    @commands.command(name='exc', hidden=True)
    @owner()
    async def exception(self, ctx):
        """[RU] Выдать исключение
        [EN] Raise an exception
        """
        raise RuntimeError('Вызвано разработчиком.')

    @commands.command(name='load', hidden=True)
    @owner()
    async def cog_load(self, ctx, *, cog: str):
        """[RU] Загрузить модуль
        [EN] Load module
        """

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`Ошибка при загрузке модуля {cog}:`** \n{type(e).__name__} - {e}')
        else:
            await ctx.send(f'**`Модуль {cog} успешно загружен`**')

    @commands.command(name='unload', hidden=True)
    @owner()
    async def cog_unload(self, ctx, *, cog: str):
        """[RU] Выгрузить модуль
        [EN] Unload module
        """

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`Ошибка при выгрузке модуля {cog}:`** \n{type(e).__name__} - {e}')
        else:
            await ctx.send(f'**`Модуль {cog} успешно выгружен`**')

    @commands.command(name='shell', aliases=['sh', 'bash'], hidden=True)
    @owner()
    async def shell(self, ctx, *, code: str):
        """[RU] Терминал Bash (теперь асинхронный!)
        [EN] Bash terminal (now async!)
        """
        async with ctx.channel.typing():
            code_strings = code.replace('```python', '') \
                            .replace('```bash', '') \
                            .replace('```', '') \
                            .split('\n')
            output = []

            def shell_(cmd):
                return os.popen(cmd).read()

            for string in code_strings:
                cmd = await self.bot.loop.run_in_executor(None, shell, string)
                if cmd == '':
                    cmd = 'ℹ | Нет выходных данных.'

                output.append(cmd)
            
            output = "\n".join(output)

            embed = discord.Embed(color=0x42A2EC)
            embed.add_field(name=f'{self.bot.yes} Bash Терминал | Команда выполнена:',
                            value=f"```bash\n{output}```")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

            try:
                await ctx.send(f'{ctx.author.mention}, получен ответ!', embed=embed)
            except:
                try:
                    await ctx.send(f'Мне не удалось отправить ответ в чат.')

    @commands.command(name='add-cog', hidden=True, aliases=['+cog'])
    @owner()
    async def add_cog(self, ctx):
        """[RU] Добавить модуль
        [EN] Add module
        """
        if len(ctx.message.attachments) < 1:
            return await ctx.send('<:naomi_tick_no:525026037868789783> Вы не вложили к сообщению файл с кодом...')
        if len(ctx.message.attachments) > 1:
            return await ctx.send('<:naomi_tick_yes:525026013663723540> К сообщению вложено более одного файла... Ок, загружу все.')

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
                await ctx.send(f'<:naomi_tick_yes:525026013663723540> Успешно загружен >> `{new_path.replace("/", ".")}``', delete_after=10)
            await ctx.message.delete()

    @commands.command(name='execute', aliases=['exec', 'eval', 'run'], hidden=True)
    @owner()
    async def execute(self, ctx, *, code: str):
        """[RU] Интерпретатор Python
        [EN] Python interpreter
        """
        async def v_execution():
            async with ctx.channel.typing():
                env = {
                    'channel': ctx.channel,
                    'author': ctx.author,
                    'guild': ctx.guild,
                    'message': ctx.message,
                    'client': self.bot,
                    'bot': self.bot,
                    'Naomi': self.bot,
                    'naomi': self.bot,
                    'discord': discord,
                    'ctx': ctx
                }

                env.update(globals())
                _code = ''.join(code).replace('```python', '').replace('```', '')

                try:
                    stdout = io.StringIO()
                    interpretate = f'async def virtexec():\n{textwrap.indent(_code, "  ")}'
                    exec(interpretate, env)
                    virtexec = env['virtexec']
                    with redirect_stdout(stdout):
                        function = await virtexec()

                except:
                    stdout = io.StringIO()
                    value = stdout.getvalue()

                    try:
                        msg = discord.Embed(color=randint(0x000000, 0xFFFFFF))
                        msg.add_field(name='<:naomi_tick_no:525026037868789783> Интерпретатор Python:',
                                      value=f"```python\n{value}{traceback.format_exc()}```".replace(self.bot.http.token, '••••••••••'))
                        msg.set_footer(text=f'Интерпретация не удалась - Python {platform.python_version()} | {platform.system()}')
                        await ctx.message.remove_reaction(loading, self.bot.user)
                        return await ctx.send(f'{ctx.author.mention}, боль печаль :с', embed=msg)
                    except:
                            return await ctx.send(f'Мне не удалось отправить ответ в чат.')
                else:
                    value = stdout.getvalue()
                    if not function:
                        if not value:
                            value = 'ℹ | Нет выходных данных.'
                        try:
                            success_msg = discord.Embed(color=randint(0x000000, 0xFFFFFF))
                            success_msg.add_field(name='<:naomi_tick_yes:525026013663723540> Интерпретатор Python:',
                                                  value=f"```python\n{value}```".replace(self.bot.http.token, '••••••••••'))
                            success_msg.set_footer(text=f'Интерпретация успешно завершена - Python {platform.python_version()} | {platform.system()}')
                            await ctx.message.remove_reaction(loading, self.bot.user)
                            return await ctx.send(f'{ctx.author.mention}, все готово!', embed=success_msg)
                        except:
                            return await ctx.send(f'Мне не удалось отправить ответ в чат.')
                    else:
                        try:
                            success_msg = discord.Embed(color=randint(0x000000, 0xFFFFFF))
                            success_msg.add_field(name='<:naomi_tick_yes:525026013663723540> Интерпретатор Python:',
                                                  value=f"```python\n{value}{function}```".replace(self.bot.http.token, '••••••••••'))
                            success_msg.set_footer(text=f'Интерпретация успешно завершена - Python {platform.python_version()} | {platform.system()}')
                            return await ctx.send(f'{ctx.author.mention}, вот! Я все выполнила c:', embed=success_msg)
                        except:
                                return await ctx.send(f'Мне не удалось отправить ответ в чат.')

        self.bot.loop.create_task(v_execution())

def setup(bot):
    bot.add_cog(Owner(bot))
