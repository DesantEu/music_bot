import ugame
import uchannels
import usender
import discord
import ucards
import utable

main_message = None
user_messages = {}


async def create_main():
    global main_message

    msg = 'uno\n\nожидаем игроков...'

    main_message = await usender.send_raw(msg, uchannels.main_channel)


async def update_main():
    players = ''


    if not ugame.game_runnging:
        for i in ugame.players:
            players += ugame.get_player(i) + '\n'
    else:
        for i in ugame.players:
            players += f'{ugame.get_player(i)} [{len(ucards.player_cards[i])} крт.]\n'

    msg = f'UNO\n\nигроки: \n\n{players}'
    await main_message.edit(content=msg)


async def send_cards(user=None):
    if user == None:
        for plr in ugame.players:
            cards = ucards.player_cards[plr]
            await send('Ваши карты:\n\n' +
                       ucards.name_deck_num(cards), plr)


async def send(msg, user=None):
    if user == None:
        for plr in ugame.players:
            ch = uchannels.user_channels[plr]
            await usender.send_raw(msg, ch)
    elif user in ugame.players:
        ch = uchannels.user_channels[user]
        await usender.send_raw(msg, ch)
    else:
        print(f'игрок {ugame.get_player(user)} не в игре')


async def send_next():
    next_ = ugame.players[utable.move]
    deck = ucards.name_deck_num(ucards.player_cards[next_])

    await send_exclusive(f'Сейчас ходишь ты вот твои карты: \n\n{deck}', f'Следущий ходит {ugame.get_player(next_)}', next_)

    # for i in ugame.players:
    #     if i == next_:
    #         deck = ucards.name_deck_num(ucards.player_cards[i])
    #         await send(f'Сейчас ходишь ты вот твои карты: \n\n{deck}', i)
    #     else:
    #         await send(f'Следущий ходит {ugame.get_player(next_)}', i)


async def send_taken():
    pass


async def send_rules(channel):
    msg = '//u [карта] - похожить можно\n//ut - это чтобы взять карту'

    await usender.send_raw(msg ,channel)


async def send_exclusive(message_exclusive, message_global, user):
    for i in ugame.players:
        if i == user:
            await send(message_exclusive, i)
        else:
            await send(message_global, i)


async def delete():
    pass
