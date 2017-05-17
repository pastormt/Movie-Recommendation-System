from datetime import datetime

def portionOfData( originalFile, outputFile, reqLines ):
    opf = open(outputFile, 'w')
    count = 0
    readyToBreak = False
    listenerID = None
    with open(originalFile) as openFile:
        for line in openFile:
            thisLine = line.replace('\n', '').split('\t')
            if readyToBreak and (thisLine[0] != listenerID):
                break
            listenerID = thisLine[0]
            opf.write(line)
            count += 1
            if count >= reqLines:
                readyToBreak = True
    opf.close()


def saveWatchersDict(dataFile):
    print("saveWatchersDict @", datetime.now())
    watchersDict = {}
    watcherID = None
    movies = {}

    with open(dataFile,'r') as openFile:
        for line in openFile:
            thisLine = line.replace('\n', '').split(',')
            if int(thisLine[0]) != watcherID:
                if watcherID is not None:
                    watchersDict[watcherID] = movies
                    movies = {}
                watcherID = int(thisLine[0])

            movies[int(thisLine[1])] = float(thisLine[2])

    watchersDict[watcherID] = movies

    return watchersDict

def createTrainingAndTest(watchersDict, testPercent):
    print("createTrainingAndTest @", datetime.now())
    totalWatchers = len(watchersDict)
    numTrainWatchers = int((1 - (testPercent/100)) * totalWatchers)
    count = 0

    trainWatchersDict = {}
    testWatchersDict = {}
    testWatchersAnswers = {}

    for watcherID, moviesDict in watchersDict.items():
        count += 1
        if count <= numTrainWatchers:
            trainWatchersDict[watcherID] = moviesDict
        else:
            testWatchersAnswers[watcherID] = {}
            testWatchersDict[watcherID] = {}

            numMovies = int(len(moviesDict) / 2) + 1
            moviesCount = 0
            for movieID, rating in moviesDict.items():
                moviesCount += 1
                if moviesCount <= numMovies:
                    testWatchersDict[watcherID][movieID] = rating
                else:
                    testWatchersAnswers[watcherID][movieID] = rating

    return [testWatchersAnswers, testWatchersDict, trainWatchersDict]
