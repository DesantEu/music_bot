from random import randrange
import ucards
import ugame
import umessager

table = None  # card on the table
move = None  # which player moves now
direction = 1  # 1 or -1 for down and up
take_amount = 1  # amount of cards you will have to take
move_nick = None
take = 1
need_color = False


async def init():
    global table, move

    move = randrange(len(ugame.players))

    while table == None or table >= 40:
        table = ucards.give_card()
        print(f"на столе {ucards.name_card(table)}")

    await umessager.send(f'Первая карта {ucards.name_card(table)}')

    # need to do it the stupid way here
    await umessager.send_exclusive(f'Вы ходите первым!', f'Первый ходит {ugame.get_player(ugame.players[move])}', ugame.players[move])


async def player_move(card_num, message):
    global move_nick, direction, take

    if not message.author == ugame.players[move]:
        await umessager.send(f"Cейчас не твой ход", message.author)
        return

    card = await get_user_card(card_num, message.author)
    num = ucards.get_num(card)
    color = ucards.get_color(card)
    tnum = ucards.get_num(table)
    tcolor = ucards.get_color(table)

    card_num -= 1

    move_nick = ugame.get_player(ugame.players[move])

    if num < 10: # numbered cards
        if num == tnum or color == tcolor:
            await move_legit(card, card_num, message)
        else:
            await move_not_legit(message)
    elif color < 4:
        if color == tcolor: # colored specials
            if num == 10: # skip
                move += 1
            elif num == 11: # reverse
                direction *= -1
            elif num == 12: # +2
                if take == 1:
                    take = 2
                else:
                    take += 2
            elif num == 13: # +4
                if take == 1:
                    take = 2
                else:
                    take += 4
                move -= 1
            elif num == 14: # wild
                move -= 1
            await move_legit(card, card_num, message)
        else:
            await move_not_legit(message)

    # TODO


async def get_user_card(card_num, player):  # get users card by number
    card_num = card_num - 1
    if card_num < 0 or card_num >= len(ucards.player_cards[player]):
        await umessager.send(f'ты ебобо нет такой карты', player)
        return None
    return ucards.player_cards[player][card_num]


async def move_legit(card, card_num, message):  # what to do if move was legit
    global table, move

    num = ucards.get_num(card)

    table = card

    await umessager.send(f'{move_nick} походил {ucards.name_card(card)}')

    move += 1

    if move < 0:
        move += len(ugame.players)

    if move >= len(ugame.players):
        move -= len(ugame.players)

    ucards.player_cards[message.author].pop(card_num)


    await umessager.send_next()

    await ugame.update()

    # todo add specials check


async def move_not_legit(message):
    await umessager.send(f'ты еблан так нельзя', message.author)


async def take_card(message):
    global take

    if not message.author == ugame.players[move]:
        await umessager.send(f"Cейчас не твой ход", message.author)
        return

    for i in range(take):
        ucards.give_card(message.author)
        await umessager.send_exclusive(f'Вы взяли карту. Вот что получилось:\n\n{ucards.name_deck_num(ucards.player_cards[message.author])}', 
        f'{ugame.get_player(message.author)} берет карту', message.author)

    if take > 1:
        await umessager.send(f'{ugame.get_player(ugame.players[move])} берет {take}')
        # todo

    take = 1


async def pick_color():
    pass


async def skip():
    pass
