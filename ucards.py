from math import floor
import random
import ugame
import umessager

# 0-9 r
# 10-19 g
# 20-29 b
# 30-39 y
# 40-43 skip
# 44-47 reverse
# 48-51 +2
# 52-55 +4
# 56-59 color

player_cards = {}


async def init():
    global player_cards
    for i in ugame.players:
        player_cards[i] = give_cards()
    
    await umessager.send_cards()
    
    


# draw random card
def give_card(player=None):
    global player_cards

    card = random.randrange(60)

    if not player == None:
        player_cards[player].append(card)

    return card


# give 7 cards
def give_cards(player=None):
    global player_cards
    cards = []

    for i in range(7):
        cards.append(give_card())

    if not player ==None:
        player_cards[player] = cards

    return cards


# draw the said card
def give_set_card(card):
    pass


# get card name
def name_card(card: int):
    colors = ['❤️', '💚', '💙', '💛', '🖤']
    names = ['Пропуск', 'Поворот', '+2', '+4', 'Выбирай']

    color = get_color(card)
    num = get_num(card)

    if num < 10:
        return f'{colors[color]} {num}'
    else:
        return f'{colors[color]} {names[num - 10]}'


def name_deck(deck):
    sdeck = ''
    for i in deck:
       sdeck += name_card(i) + '\n'
    return sdeck


def name_deck_num(deck):
    ndeck = ''

    for i in range(len(deck)):
        ndeck += f'{i + 1}. {name_card(deck[i])} \n'
    return ndeck


# 0-9, 10 - skip, 11 - reverse, 12 - +2, 13 - +4, 14 - wild
def get_num(card):
    if card < 40:
        return card % 10
    elif card < 44:
        return 10
    elif card < 48:
        return 11
    elif card < 52:
        return 12
    elif card < 56:
        return 13
    elif card < 60:
        return 14
    else:
        print('num error')
        return -1


def get_color(card):
    if card < 40:  # numeric
        return floor(card / 10)
    elif card < 52:  # sp not black
        return (card - 40) % 4
    elif card < 60:
        return 4
    else:
        print('color error')
        return -1
