import mplayer
import shutil
import discord
import msender
import mlogger as ml


async def parse(bot, message):
    msg = message.content[len(bot.prefix):]
    chan = message.channel

    args = msg.split(" ", 1)
    args[0] = args[0].lower()
    if len(args) == 1:
        args.append('')

    if args[0] in ['p', "play"]:
        await mplayer.play(bot, args[1], message)
    elif args[0] in ['pt', "playtop"]:
        await mplayer.play(bot, args[1], message, play_top=True)

    elif args[0] in ['clean', 'clear', 'cc']:
        await mplayer.clear_queue(message)

    elif args[0] == 'stop':
        await mplayer.stop(bot, message)

    elif args[0] in ['s', 'skip']:
        await mplayer.skip(num=args[1], message=message)

    elif args[0] in ['n', 'next']:
        await mplayer.next(message)

    elif args[0] in ['b', 'back']:
        await mplayer.back(message)

    elif args[0] == 'pause':
        await mplayer.pause(message)

    elif args[0] in ['q', 'queue']:
        await mplayer.print_queue(message)
    elif args[0] in ['qq']:
        await mplayer.print_past_queue(message)
    elif args[0] in ['np', 'now']:
        await mplayer.now_playing(message)

    elif args[0] in ['rm', 'remove']:
        await mplayer.remove(args[1], message)

    elif args[0] in ['save', 'ss']:
        await mplayer.save_playlist(args[1], message)
    elif args[0] in ['pp']:
        await mplayer.play_playlist(args[1], message, bot)

    elif args[0] in ['pl']:
        await mplayer.list_playlist(args[1], message, bot)

    elif args[0] in ['v', 'volume']:
        await mplayer.volume_(args[1], message, bot)

    elif args[0] == 'help':
        await help(bot, chan)


async def parse_admin(bot, message):
    msg = message.content.lower()[1:]
    chan = message.channel

    args = msg.split(" ", 1)
    args[0] = args[0].lower()
    if len(args) == 1:
        args.append('')

    if args[0] == 'clean':
        shutil.rmtree('queue')
        await msender.send('Освободил место', message.channel)

    elif args[0] == 'dj':
        bot.dj_check = not bot.dj_check
        await msender.send(f'Проверка на роль: {bot.dj_check}', message.channel)

    elif args[0] == 'debug':
        bot.debug = not bot.debug
        await msender.send(f'Можно ломаться: {bot.debug}', message.channel)

    elif args[0] == 'shutdown':
        await msender.send('Смэрть', chan)
        exit()

    elif args[0] in ['dpl', 'delpl', 'rmpl']:
        await mplayer.del_playlist(args[1], message)

    elif args[0] in ['admin', 'adminonly', 'ao']:
        bot.admin_only = not bot.admin_only
        await msender.send(f'Админ онли: {bot.admin_only}', message.channel)

    elif args[0] == 'help':
        await help(bot, chan, admin=True)


async def help(bot, chan, admin=False):
    commands = []
    descriptions = []
    if admin:
        path = 'help_admin.txt'
    else:
        path = 'help.txt'

    with open(path, 'r', encoding="utf-8") as file:
        for i in file.readlines():
            temp = i.split(" - ")
            commands.append(temp[0])
            descriptions.append(temp[1])
    emb = discord.Embed()
    emb.color = discord.Color.orange()
    prefix = bot.prefix if not admin else bot.admin_prefix
    for i in range(len(commands)):
        emb.add_field(
            name=prefix + f' {prefix}'.join(commands[i].split(", ")), value=descriptions[i], inline=False)
    await chan.send(embed=emb)
