import discord

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    
    # 
    for member in message.mentions:
        dm =  "You were mentioned in server " + message.guild.name + " by " +str(member)+ " in the channel " + message.channel.name + " the message has a priority of ______"
        await discord.User.send(member,dm)

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run('NzQ5MzEwMzA4NTM5MDM5NzU1.X0qHmw.0fs8galcUvlCg4wEiJr_ovXJo08')