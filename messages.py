import pandas as pd
import numpy as np
import string

def saveMessages():
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

    for i in range(len(csvdata)):
        if (i == 0):
            y.append('Priority')
            continue
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
            y.append('Nonpriority')
        
        word = csvdata['Content'][i]
        if (type(word) == str):
            words = word.split(" ")
            sum = 0
            for i in range(len(words)):
                sum += len(words[i])
            avg = sum / len(words)
            avgwordlength.append(avg)

            percentCapital = len([letter for letter in word if letter.isupper()])/ len(word)
            percentCapLetters.append(percentCapital)
        else:
            avgwordlength.append(0)

            

    npa = np.asarray(replytime, dtype=np.int)
    x.append(npa)
    npa = np.asarray(avgwordlength, dtype=np.int)
    x.append(npa)
    npa = np.asarray(percentCapLetters, dtype=np.float32)
    x.append(npa)

    data.append(x)
    data.append(y)

    return data
