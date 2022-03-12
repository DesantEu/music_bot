import discord

long_message = ''


async def send(msg, channel, color=discord.Color.from_rgb(255, 166, 201)):
    emb = discord.Embed(title=msg)
    emb.color = color
    await channel.send(embed=emb)


async def long_add(msg):
    long_message += '\n' + msg


async def long_send(channel, title="Thwew", color=discord.Color.from_rgb(255, 166, 201)):
    emb = discord.Embed()
    emb.color = color
    emb.add_field(name=title, value=long_message, inline=False)
    await channel.send(embed=emb)


async def long_clear():
    global long_message
    long_message = ''

async def send_long(msg, channel, title='Thwew', color=discord.Color.from_rgb(255, 166, 201)):
    # await channel.send("```" + msg + "```")
    emb = discord.Embed()
    emb.color = color
    emb.add_field(name=title, value=msg, inline=False)
    await channel.send(embed=emb)
