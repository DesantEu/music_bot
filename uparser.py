import ugame
import utable


async def parse(bot, message):
    msg = message.content[2:]
    chan = message.channel

    args = msg.split(" ", 1)
    args[0] = args[0].lower()
    if len(args) == 1:
        args.append('')

    if args[0] in ['uinit', 'ui']:
        await ugame.start_lobby(bot, message)

    if args[0] in ['ustart', 'us']:
        await ugame.start_game(bot, message)

    if args[0] in ['ustop', 'ust']:
        await ugame.stop(bot, message)

    if args[0] in ['ujoin', 'uj']:
        await ugame.join(bot, message)


    if args[0] in ['u']:
        await utable.player_move(int(args[1]), message)
    if args[0] in ['take', 'ut']:
        await utable.take_card(message)
    if args[0] in ['']:
        pass
    if args[0] in ['']:
        pass
    if args[0] in ['']:
        pass
    if args[0] in ['']:
        pass
    

    if args[0] in ['test']:
        await ugame.test(bot, message)
