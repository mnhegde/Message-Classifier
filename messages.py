import pandas as pd
import numpy as np
import string

def getMsgData():
    data = []
    x = []
    y = []
    replytime = []
    avgwordlength = []
    percentCapLetters = []
    csvdata = pd.read_csv('data/Direct_Messages_-_Private_-_MH_630894986279256074.csv', names=[
                          'AuthorID', 'Author', 'Date', 'Content', 'Attachments', 'Reactions'], sep=",", skiprows=1)

    for i in range(len(csvdata.columns)):
        x.append(np.array(csvdata[csvdata.columns[i]]))

    timestamp = x[2]

    #this is very inefficient. Found method to convert strings stored in csv to datetime objs, would should be math easier and more efficient
    for i in range(len(csvdata)):
        if (i != 0):
            currentmsg = timestamp[i].split(" ")
            prevmsg = timestamp[i - 1].split(" ")
            msgtime = currentmsg[1].split(":")
            prevtime = prevmsg[1].split(":")
            if (currentmsg[0] == prevmsg[0] and currentmsg[2] == prevmsg[2]):
                if (int(msgtime[1]) >= 10):
                    msgreplytime = int(msgtime[1]) - int(prevtime[1])
                    if (abs(msgreplytime) <= 10):
                        replytime.append(msgreplytime)
                        y.append('Priority')
                else:
                    msgreplytime = 60 - (10 - int(msgtime[1]))
                    if (msgreplytime == int(prevtime[1])):
                        replytime.append(msgreplytime)
                        y.append('Priority')
            else:
                replytime.append(0)
                y.append('Nonpriority')
        else:
            y.append('Priority')
            replytime.append(0)
        
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


    npa = np.asarray(replytime, dtype=np.int)
    x.append(npa)
    npa = np.asarray(avgwordlength, dtype=np.int)
    x.append(npa)
    npa = np.asarray(percentCapLetters, dtype=np.float32)
    x.append(npa)

    data = formatFeatures(x, y)
    return data

def formatFeatures(x, y):
    data = []
    print(len(x[6]))
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
