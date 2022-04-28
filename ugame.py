from email.errors import MessageParseError
import ucards
import usender
import uchannels
import umessager
import utable


players = []

rule_takeall = False
rule_specials = False

game_started = False  # initiated game
game_runnging = False  # stqarted playing
game_guild = None


# reset
async def init(bot, message):
    # rule_takeall = False
    # rule_specials = False
    global game_started, game_runnging, game_guild, players

    game_runnging = False
    game_started = False
    game_guild = None
    players = {}


# init new game
async def start_lobby(bot, message):
    global game_guild, players, game_started

    if game_started:
        await usender.send('Лобби уже есть', message.channel)
        return

    game_started = True
    game_guild = message.guild
    players = []

    await uchannels.init(bot, message)
    await usender.send('Создал лобби', message.channel)

    await join(bot, message)


# start playing
async def start_game(bot, message):
    global game_runnging, players

    if not game_started:
        await usender.send('Сначала напиши //ui', message.channel)
        return

    if game_runnging:
        await usender.send('Игра уже идет', message.channel)
        return

    if len(players) < 2:
        await usender.send('Мало игроков', message.channel)
        #! return

    await ucards.init()
    await utable.init()

    # await uchannels.create_category()

    game_runnging = True
    await usender.send('Игра началась', uchannels.main_channel)


# stop the game
async def stop(bot, message):
    if game_started:
        await init(bot, message)
        await uchannels.delete()
        await usender.send('Лобби закрыто', message.channel)
    else:
        await usender.send('Лобби нету', message.channel)


# join the session
async def join(bot, message):
    global players

    if game_runnging:
        await usender.send('Игра уже идет, нельзя присоединиться')
        return

    if not game_started:
        await usender.send('Игра еще не идет, нельзя присоединиться')
        return

    player = message.author

    if player in players:
        await usender.send(f'Вы уже в игре', message.channel)
    else:
        players.append(player)
        await usender.send(f'{get_player(player)} присоединился', uchannels.main_channel)

        await uchannels.create_user(message)

    await update()


async def leave(bot, message):
    pass


def get_player(user):
    return f'{user.name}#{user.discriminator}({user.nick})'


async def update():
    await umessager.update_main()
    


async def test(bot, message):
    await usender.send_raw(f'rule 1: {rule_specials}, rule 2: {rule_takeall}, game_started: {game_started}, game_guild: {game_guild}, players: {players}', message.channel)
