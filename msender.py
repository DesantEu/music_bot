import discord
async def send(msg, channel, color=discord.Color.from_rgb(255,166,201)):
    emb = discord.Embed(title=msg)
    emb.color = color
    await channel.send(embed=emb)

async def send_long(msg, channel, title='Thwew', color=discord.Color.from_rgb(255,166,201)):
    # await channel.send("```" + msg + "```")
    emb = discord.Embed()
    emb.color = color
    emb.add_field(name=title, value=msg, inline=False)
    await channel.send(embed=emb)

