import discord
#import model_creator as model
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    
    fullMessageStart = str(message.content).split(">",1)
    newFullMessage = fullMessageStart[1]
    #uppercase letter percentage
    uppercaseLetters = 0
    for i in newFullMessage:
        if i.isupper():
            uppercaseLetters+=1
    if len(newFullMessage) == 0:
        uppercaseLetters = 0
    else:
        uppercaseLetters = uppercaseLetters/len(newFullMessage)
    print("percent uppercase letters: " + str(uppercaseLetters*100))
    percentUppercaseLetters = (uppercaseLetters)*100

    #average word length
    words = newFullMessage.split()
    wordLength = 0
    for i in range(len(words)):
        wordLength += len(words[i])
    if len(words) == 0:
        avgWordLength = 0
    else:
        avgWordLength = wordLength/len(words)
    print("average word length: " + str(wordLength))
    
    #time since last message 
    pastMessages = await message.channel.history(limit = 200).flatten()
    pastMessageTimes = []
    print(len(message.raw_mentions))
    for mention in range(len(message.raw_mentions)):
        for msgs in range(len(pastMessages)):
            if message.raw_mentions[mention] == pastMessages[msgs+1].author.id:
                pastMessageTimes.append(pastMessages[msgs+1].created_at)
                if len(pastMessageTimes) == len(message.raw_mentions):
                    break
        break

    for i in range(len(pastMessageTimes)):
        pastMessageTimes[i] =   message.created_at - pastMessageTimes[i] 
        print("delta time since last user message: "+str(pastMessageTimes[i]))
        
    
    #running model and dm user
    
    for member in message.mentions:
        dm =  "You were mentioned in the server " + message.guild.name + " by " +str(member)+ " in the channel " + message.channel.name + " the message has a priority of ______"+"!"
       # await 
        await discord.User.send(member,dm)

    if message.content.startswith('?help'):
        await message.channel.send('If someone mentions someone I send the person whose mentioned a message about the priority of their mention!')

client.run("TOKEN HERE")