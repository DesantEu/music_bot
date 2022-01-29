import discord
import subprocess
import os
import msender
import atexit


class User(discord.Client):
    async def on_ready(self):
        self.prefix = "//"
        self.admin_prefix = ">"
        self.admin_role = 'thwew-admin'

        await kill()
        await start()

        print('tweaker started')

    async def on_message(self, message):
        if message.content.startswith(self.admin_prefix):
            if not self.admin_role in [i.name for i in message.author.roles]:
                await msender.send('Не', message.channel, discord.Color.lighter_grey())
                return
            else:
                con = message.content[1:]
                if con == 'restart':
                    await kill(message)
                    await start(message)

                elif con == 'start':
                    await start()

                elif con == 'kill':
                    await kill(message)

                

async def start(message=''):
    # os.system(r'python -u "d:\projects\music_bot\main.py"')
    global proc

    start_command = r'python -u main.py'
    proc = subprocess.Popen(start_command.split(' '))

    with open('pids.txt', 'w+') as file:
        file.write(file.read() + str(proc.pid) + ' ')

    if not message == '':
        await msender.send('Поднял бота', message.channel, white_color)

async def kill(message=''):
    with open('pids.txt', 'w+') as file:
        if not file.read() == '':
            pids = file.read().split(' ')

            for pid in pids:
                subprocess.Popen(f'taskkill /f /im {pid}'.split(' '))

            file.write('')

    if not message == '':
        await msender.send('Убил бота)(', message.channel, white_color)

def exit_override():
    with open('pids.txt', 'w+') as file:
        file.write('')

atexit.register(exit_override)

white_color = discord.Color.from_rgb(255,255,255)
user = User()
with open('./tweaker_key.txt', 'r') as file:
    user.run(file.readline())
