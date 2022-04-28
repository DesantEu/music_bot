from cv2 import CALIB_HAND_EYE_DANIILIDIS
import ugame
import umessager

main_channel = None
user_channels = {}
category = None
uno_role = None

category_name = '---uno---'
role_name = '---uno---'


async def init(bot, message):
    await create_role()

    await create_category()
    await create_main()
    await umessager.create_main()


async def create_category():
    global category

    category = await ugame.game_guild.create_category(category_name)

    await category.set_permissions(await get_everyone(), read_messages=False, send_messages=False)
    await category.set_permissions(uno_role, read_messages=True, send_messages=True)

    # for i in ugame.game_guild.categories:
    #     if i.name == category_name:
    #         category = i


async def create_main():
    global main_channel

    main_channel = await category.create_text_channel('Лобби')


async def create_user(message):
    global user_channels

    ch = await category.create_text_channel(ugame.get_player(message.author))
    user_channels[message.author] = ch
    # user_channels.append(ch)

    await ch.set_permissions(uno_role, read_messages=False, send_messages=False)
    await ch.set_permissions(message.author, read_messages=True, send_messages=True)

    await message.author.add_roles(uno_role)

    await umessager.send_rules(ch)


async def create_role():
    global uno_role

    uno_role = await ugame.game_guild.create_role(name=role_name)


async def get_everyone():
    for i in ugame.game_guild.roles:
        print(i.name)
        if i.name == '@everyone':
            return i

    print('not found everyone')


async def delete():
    await uno_role.delete()
    await main_channel.delete()
    for i in list(user_channels.values()):
        await i.delete()
    await category.delete()
