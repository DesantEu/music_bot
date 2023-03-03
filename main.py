import discord
import mparser
import uparser
import mplayer
import asyncio
import msender
import mlogger as ml
import traceback as tb


class User(discord.Client):
    async def on_ready(self):
        
        # default settings values
        self.anti_swearing = False
        self.logging = True
        self.debug = False

        # local settings copy
        self.settings = {}
        self.dj_check = True
        self.admin_only = False

        # role names
        self.dj_role = 'DJ'
        self.admin_role = 'thwew-admin'

        # prefixes
        self.prefix = "//"
        self.admin_prefix = ">"


        # player init and main loop
        await mplayer.init()
        task = asyncio.Task(mplayer.queue())

        ml.log('BOT STARTED', level="all")
    


    # main parser
    async def on_message(self, message):
        # self check
        if message.author == self.user:
            return

        # logging messages
        ml.log('[{} #{}] {}: {}'.format(message.guild, message.channel.name,
                                       message.author, message.content), level="chat")


        # // check
        if message.content.startswith(self.prefix):
            # admin only check
            if (self.admin_only and not self.admin_role in [i.name for i in message.author.roles]
                and not (message.author.name == "Desant" and message.author.discriminator == '0148')):
                await msender.send('Не сейчас', message.channel, discord.Color.default())
                ml.log(f"{message.author} tried to use commands (admin only mode active)", level="warn")
                return
            # dj check
            if (not self.dj_role in [i.name for i in message.author.roles] and self.dj_check
                and not self.admin_role in [i.name for i in message.author.roles]
                and not (message.author.name == "Desant" and message.author.discriminator == '0148') ):
                await msender.send('С тобой дружить я не буду', message.channel, discord.Color.default())
                ml.log(f"{message.author} tried to use commands (not dj)", level="warn")
                return
            # to break or not to break
            if not self.debug:
                try:
                    await mparser.parse(self, message)
                    await uparser.parse(self, message)
                except Exception as e:
                    await msender.send('Что-то пошло не так...', message.channel, discord.Color.red())
                    ml.log(''.join(tb.format_exception(None, e, e.__traceback__)), level="error")
            else:
                await mparser.parse(self, message)

        # > check
        if message.content.startswith(self.admin_prefix):
            if (not self.admin_role in [i.name for i in message.author.roles]
                and not (message.author.name == "Desant" and message.author.discriminator == '0148')):
                await msender.send('Та не)', message.channel, discord.Color.default())
                ml.log(f"{message.author} tried to use admin command (not admin)", level="warn")
                return
            await mparser.parse_admin(self, message)


        return
    
    # def getArgs(self, con):
    #     words = con.split(' ')
    #     args = []
    #     started_big = False
    #     big_arg = ''
    #     for i in words:
    #         if i.startswith('"') and i.endswith('"') and not len(i) == 2:
    #             i = i[1:-1]
    #             args.append(i)
    #         elif i.startswith('"'):
    #             started_big = True
    #             big_arg = i[1:len(i)]
    #         elif i.endswith('"'):
    #             big_arg += ' {}'.format(i[0:-1])
    #             started_big = False
    #             args.append(big_arg)
    #         elif started_big:
    #             big_arg += ' {}'.format(i)
    #         else:
    #             args.append(i)
    #     args.pop(0)
    #     return args
        # if con.startswith('fuck'):
        #     await chan.send('you')

        # elif con.startswith('>help'):
        #     commands = []
        #     descriptions = []
        #     with open('help.txt', 'r') as file:
        #         for i in file.readlines():
        #             temp = i.split(" - ")
        #             commands.append(temp[0])
        #             descriptions.append(temp[1])
        #     emb = discord.Embed()
        #     emb.color = discord.Color.orange()
        #     emb.set_footer(text='<> - essential, [] - optional')
        #     for i in range(len(commands)):
        #         emb.add_field(name=commands[i], value=descriptions[i])
        #     await chan.send(embed=emb)

        # if con == 'thwew':
        #     await chan.send('thwew')

        # elif con.startswith('>del'):
        #     await chan.purge(check=lambda m: m.author == self.user and m.content.startswith('deleted'), oldest_first=True)
        #     lim = con.split(' ')[1]
        #     for i in message.author.roles:
        #         if i.name == 'Staff':
        #             await message.channel.purge(limit=int(lim) + 1)


        # elif con.startswith('>getraw'):
        #     temp = con[8:]
        #     temp2 = ''
        #     if len(con) > 8:
        #         for i in temp:
        #             if i == '<':
        #                 temp2 += '< '
        #             else:
        #                 temp2 += i
        #         await chan.send(temp)
        #     else:
        #         await chan.send('dude at least type something smh')
        #     if con.startswith('>getraw-d'):
        #         await message.delete()

        # elif con.startswith('>test'):
        #     emb = discord.Embed()
        #     emb.color = discord.Color.orange()
        #     emb.add_field(name='fuck', value=self.getArgs(con))
        #     await chan.send(embed=emb)

        # elif con.startswith('>rps'):
        #     moves = ['камень', 'ножницы', 'влад']
        #     enemy = con.split()[1]
        #     mymove = random.randint(0,2)
        #     enemymove = random.randint(0,2)
        #     emb = discord.Embed()
        #     emb.color = discord.Color.orange()
        #     text_ = f'<@!{message.author.id}> выкинул {moves[mymove]}\n{enemy} выкинул {moves[enemymove]}'
            
        #     if(mymove < enemymove or mymove == 2 and enemymove == 0):
        #         text_ += f'\n\n<@!{message.author.id}> победа'
        #     elif(mymove == enemymove):
        #         text_ += f'\n\nНичья'
        #     else:
        #         text_ += f'\n\n{enemy} победа'
        #     emb.add_field(name='Прикольно', value=text_)
        #     await chan.send(embed=emb)


user = User()
with open('./key.txt', 'r') as file:
    user.run(file.readline())
