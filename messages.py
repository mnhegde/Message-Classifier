import pandas as pd
import numpy as np
import string
from datetime import datetime, timedelta

def getMsgData():
    data, x, y, replytime, avgwordlength, percentCapLetters, wordcount = [], [], [], [], [], [], []
    timeFormat = '%d-%b-%y %I:%M %p'

    csvdata = pd.read_csv('data/Direct_Messages_-_Private_-_MH_630894986279256074.csv', names=[
                          'AuthorID', 'Author', 'Date', 'Content', 'Attachments', 'Reactions'], sep=",", skiprows=1)

    for i in range(len(csvdata.columns)):
        x.append(np.array(csvdata[csvdata.columns[i]]))

    timestamp = x[2]

    #this is very inefficient. Found method to convert strings stored in csv to datetime objs, would should be math easier and more efficient
    for i in range(len(csvdata)):
        if (i == 0):
            msgtime = datetime.strptime(timestamp[i], timeFormat)
            prevtime = datetime.strptime(timestamp[i - 1], timeFormat)
            msgReplyTime = msgtime - prevtime
            replytime.append(msgReplyTime)
            if (msgReplyTime <= timedelta(minutes=10)):
                y.append('Priority')
            else:
                y.append('Nonpriority')
        else:
            replytime.append(0)
            y.append('Priority')
        
        word = csvdata['Content'][i]
        if (type(word) == str):
            words = word.split(" ")
            wordcount.append(len(words))
            sum = 0
            for i in range(len(words)):
                sum += len(words[i])
            avg = sum / len(words)
            avgwordlength.append(avg)

            percentCapital = len([letter for letter in word if letter.isupper()]) / len(word)
            percentCapLetters.append(percentCapital)
        else:
            wordcount.append(0)
            avgwordlength.append(0)
            percentCapLetters.append(0)

    npa = np.asarray(replytime)
    x.append(npa)
    npa = np.asarray(avgwordlength)
    x.append(npa)
    npa = np.asarray(percentCapLetters)
    x.append(npa)
    npa = np.asarray(wordcount)
    x.append(npa)

    data = formatFeatures(x, y)

    #to add y list to data data has to be given an extra dimension
    data = [data]

    #Removing both nans because it would confuse the model fit
    #also removed the first number id because it is the same as the names listed
    #also removed the text because it is just meaningless bleeps and boops
    for r in range(len(data[0])):
        for g in range(5):
            data[0][r].pop(1)
            
    #This section is the integration of classifiers into their own section
    data.append([])
    for r in range(len(data[0])):
        #this adds the respective classifier to the y section of data
        data[1].append(data[0][r][len(data[0][r])-1])

        #this removes the classifier from the x section that should just be features
        data[0][r].pop(len(data[0][r])-1)


    return data

def formatFeatures(x, y):
    data = []
    for i in range(len(y)):
        msgdata = []
        for j in range(len(x)):
            msgdata.append(x[j][i])
        msgdata.append(y[i])
        data.append(msgdata)

    return data

getMsgData()
