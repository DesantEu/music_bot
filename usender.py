import discord
from numpy import array

long_message = ''


async def send(msg, channel, color=discord.Color.from_rgb(255, 166, 201)):
    emb = discord.Embed(title=msg)
    emb.color = color
    return await channel.send(embed=emb)


async def send_raw(msg, channel):
    return await channel.send(msg)
