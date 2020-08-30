import discord
import datetime
import config
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import pickle
from model_creator import open_batch_data

message_classifier_model = open_batch_data('message_classifier_model.pkl')

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    if message.author == client.user:
        return
    if message.content.startswith('?help'):
        await message.channel.send('If someone mentions someone I send the person whose mentioned a message about the priority of their mention!')
        
        
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
    print("number of words: "+str(len(words)))
    
    #time since last message 
    pastMessages = await message.channel.history(limit = 200).flatten()
    pastMessageTimes = []
    for mention in range(len(message.raw_mentions)):
        for msgs in range(len(pastMessages)):
            if message.raw_mentions[mention] == pastMessages[msgs].author.id:
                pastMessageTimes.append(pastMessages[msgs].created_at)
                if len(pastMessageTimes) == len(message.raw_mentions):
                    break
            else:
                pastMessageTimes.append(datetime.datetime.now())
                if len(pastMessageTimes) == len(message.raw_mentions):
                    break
        break

    for i in range(len(pastMessageTimes)):
        pastMessageTimes[i] =   message.created_at - pastMessageTimes[i] 
        print("delta time since last user message: "+str(pastMessageTimes[i]))
        
    
    #running model and dm user
    thumbsUp = '\N{THUMBS UP SIGN}'
    thumbsDown = '\N{THUMBS DOWN SIGN}'
    await message.channel.send("React with thumbs up or down if my priority prediction was correct or not!")
    await message.add_reaction(thumbsUp)
    await message.add_reaction(thumbsDown)
    for i in range(len(message.mentions)):
        member = message.mentions[i]
        features = [pastMessageTimes[i].total_seconds()/60,avgWordLength,percentUppercaseLetters,len(words)]
        prediction = message_classifier_model.predict([features])
        dm =  "You were mentioned in **"+  message.channel.name + "** on server **" + message.guild.name + "** by **" +str(member)+  "** the message has a priority of **"+prediction[0]+"**!"
        await discord.User.send(member,dm)
        



client.run(config.BOT_TOKEN)