import discord
import subprocess
import os
import msender


class User(discord.Client):
    async def on_ready(self):
        self.prefix = "//"
        self.admin_prefix = ">"
        self.admin_role = 'thwew-admin'

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
    if not message == '':
        await msender.send('Поднял бота', message.channel, white_color)

async def kill(message):
    proc.kill()
    await msender.send('Убил бота)(', message.channel, white_color)


white_color = discord.Color.from_rgb(255,255,255)
user = User()
with open('./tweaker_key.txt', 'r') as file:
    user.run(file.readline())
