import pandas as pd
import numpy as np
import string
from datetime import datetime, timedelta

def getMsgData():
    data, x, y, replytime, avgwordlength, percentCapLetters = [], [], [], [], [], []
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
            sum = 0
            for i in range(len(words)):
                sum += len(words[i])
            avg = sum / len(words)
            avgwordlength.append(avg)

            percentCapital = len([letter for letter in word if letter.isupper()]) / len(word)
            percentCapLetters.append(percentCapital)
        else:
            avgwordlength.append(0)
            percentCapLetters.append(0)

    npa = np.asarray(replytime)
    x.append(npa)
    npa = np.asarray(avgwordlength)
    x.append(npa)
    npa = np.asarray(percentCapLetters)
    x.append(npa)

    data = formatFeatures(x, y)
    return data

def formatFeatures(x, y):
    data = []
    for i in range(len(y)):
        msgdata = []
        msgdata.append(x[0][i])
        msgdata.append(x[1][i])
        msgdata.append(x[2][i])
        msgdata.append(x[3][i])
        msgdata.append(x[4][i])
        msgdata.append(x[5][i])
        msgdata.append(y[i])
        data.append(msgdata)

    return data

getMsgData()
