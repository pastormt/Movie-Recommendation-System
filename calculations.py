import numpy
from datetime import datetime
import math
import copy
from scipy import stats

# VERIFIED calcItemSlopes with sample data
# returns a dict of item-item slopes based on Slope One algorithm
# returned datastructure has key, value structure, where key is itemA of reference, and value is a dictionary
# where keys are other itemsB, and values are the slope of itemA to itemB
def calcItemSlopes( trainWatchersDict ):
    print("calcItemSlopes @", datetime.now())
    # first setup item-based dictionary, where each key is an item, and each value is
    # a nested dict where the keys are users and the values are the scores the respective users gave
    #print("trainWatchersDict")
    #print(trainWatchersDict)
    trainItemsDict = {}
    for watcherID, watcherDict in trainWatchersDict.items():
        for itemID, rating in watcherDict.items():
            if itemID in trainItemsDict:
                trainItemsDict[itemID][watcherID] = rating
            else:
                trainItemsDict[itemID] = {watcherID : rating}

    #print("trainItemsDict")
    #print(trainItemsDict)

    itemSlopes = {}
    for itemA, itemADict in trainItemsDict.items():
        for itemB, itemBDict in trainItemsDict.items():
            if itemA != itemB:
                total = 0.0
                count = 0
                for userID in itemADict:
                    if userID in itemBDict:
                        total += itemADict[userID] - itemBDict[userID]
                        count += 1
                if count > 0:
                    if itemA in itemSlopes:
                        itemSlopes[itemA][itemB] = total / count
                    else:
                        itemSlopes[itemA] = {itemB : total / count}

    #print("itemSlopes")
    #print(itemSlopes)
    return itemSlopes

def calcUserSim( moviesDict1, moviesDict2, intersection, lenIntersection ):
    """
    Returns
    _______
    Several measures of how similar 2 dictionaries are (of key = movieID, value = rating).
    """

    ratings1 = []
    ratings2 = []

    for movieID in intersection:
        ratings1.append(moviesDict1[movieID])
        ratings2.append(moviesDict2[movieID])

    # user of moviesDict1 is the Y-VALUE (ie the predicted value, later)
    slope, intercept, r_value, p_value, std_err = stats.linregress(ratings2, ratings1)

    return [r_value, slope, intercept, lenIntersection]

#VERIFIED correct with sample data
def calcUserSims( testWatchersDict, trainWatchersDict ):
    print("calcUserSims @", datetime.now())
    """
    Calculates the similarity between each test watcher and every other watcher
    """

    # for test printing
    testWatcherCount = 0
    totalTestWatchers = len(testWatchersDict)

    # dictionary of user - user similarities
    # key = user A, value = subdict. subdict key = user B, value = similarity to user A
    watchersSims = {}

    #print("testWatchersDict ", testWatchersDict)

    #print("trainWatchersDict ", trainWatchersDict)

    for watcherA, knownMoviesDict in testWatchersDict.items(): # compare this test listener to every other listener
        # for just the current listenerA (below) in testListeners being iterated over, store a dictionary
        # w/ key = listenerID of similar listener, value = inCommon (a list, below, of different similarity measures)
        # need to store these for the listener, rather than recommend upon each right away, so, for this listenerA alone,
        # the dictionary of all similar listeners can be sent to a pruning function
        #print("watcherA ", watcherA)

        watcherASims = {}

        testWatcherCount += 1
        #print("Test watcher ", testWatcherCount, " of ", totalTestWatchers, " @", datetime.now())

        trainWatcherCount = 0
        for watcherB, moviesDictB in trainWatchersDict.items():
            #print("watcherB ", watcherB)

            trainWatcherCount += 1
            #print "Test watcher ", testWatcherCount, " Train watcher ", trainWatcherCount

            if watcherA != watcherB:
                # 1st similarity measure (%, and rating, in common)
                # also calculate item - item similarities for items that one listener listened to, but the other did not
                intersection = {k for k in knownMoviesDict.keys() if k in moviesDictB}

                #print("intersection ", intersection)

                numInCommon = len(intersection)
                if numInCommon > 0:
                    #print("watcherA: ", watcherA)
                    #print("watcherB: ", watcherB)
                    # inCommon is a list of different measures returned by calcUserSim
                    inCommon = calcUserSim(knownMoviesDict, moviesDictB, intersection, numInCommon)
                    watcherASims[watcherB] = inCommon

        watchersSims[watcherA] = watcherASims
    #print("watchersSims ", watchersSims)
    return watchersSims

#VERIFIED
# predict using slopeOne
def predict_item_based( testWatchersDict, testWatchersAnswers, itemSlopes ):
    print("predict_item_based @", datetime.now())
    # dict key = user A, value is subdict. subdict keys are the items in testWatchersAnswers[userA]
    # in other words, the hidden movies and their ratings by this user. subdict values are predicted ratings for this user.
    predictions = {}
    # recommend
    #print("itemSlopes")
    #print(itemSlopes)

    #print("testWatchersDict")
    #print(testWatchersDict)

    #print("testWatchersAnswers")
    #print(testWatchersAnswers)

    for watcherA, watcherA_answers in testWatchersAnswers.items():

        watcherA_predictions = {}

        #print("watcherA")
        #print(watcherA)
        for movieID, rating in watcherA_answers.items():
            #print("movieID to predict")
            #print(movieID)
            # "rating" is the answer
            # predicting a rating for this movie
            prediction_total = 0.0
            prediction_count = 0

            for movieID_vis, rating_vis in testWatchersDict[watcherA].items():
                #print("movieID in watcherA visible dict")
                #print(movieID_vis)
                try:
                    prediction_total += testWatchersDict[watcherA][movieID_vis] + itemSlopes[movieID][movieID_vis]
                    prediction_count += 1
                except KeyError:
                    pass

            if prediction_count > 0:
                prediction_avg = prediction_total / prediction_count
                if prediction_avg > 5:
                    prediction_avg = 5
                elif prediction_avg < 0.5:
                    prediction_avg = 0.5
            else:
                prediction_avg = 'NA' # signifies could not predict based on any info

            watcherA_predictions[movieID] = prediction_avg

        predictions[watcherA] = watcherA_predictions
    #print("predictions")
    #print(predictions)
    return predictions

# VERIFIED with sample data
# predict using user-based methods of similarity:
# 1) correlation (or should we add cognitive diversity?)
def predict_user_based( testWatchersDict, testWatchersAnswers, trainWatchersDict, usersSims, minNumInCommon = 1, pruning = .3 ):
    print("predict_user_based @", datetime.now())
    #print("testWatchersDict")
    #print(testWatchersDict)

    #print("testWatchersAnswers")
    #print(testWatchersAnswers)

    #print("usersSims")
    #print(usersSims)

    # the below dictionaries will store all rating predictions for all testWatchers, based upon the movies we know we need to predict
    # which are the ones in a given testWatcher's answers dict
    corr_predictions = {}

    # for each movie rating we want to predict
    for watcherA, watcherA_movies in testWatchersAnswers.items():

        watcherA_corr_predictions = {}
        # for each movie rating we're trying to predict for watcherA
        for movieID, rating in watcherA_movies.items():
            # the below dicts include values ONLY for watchers that have also rated this movieID
            sims = {}

            #for each similar user to userA
            for watcherB, simList in usersSims[watcherA].items():
                #print("watcherB: ", watcherB)
                #print("trainWatchersDict[watcherB]")
                #print(trainWatchersDict[watcherB])

                numInCommon = simList[3]
                if numInCommon >= minNumInCommon:
                    if movieID in trainWatchersDict[watcherB]:
                        # since we cant do anything with "nan" correlations or slopes
                        if not (math.isnan(simList[0]) or math.isnan(simList[1])):
                            sims[watcherB] = simList

            #print("sims ", sims)

            numSimilar = len(sims)
            numKept = numSimilar * pruning
            curKept = 1
            corr_prediction = 0.0
            total_corr = 0.0
            # sort (desc by correlation) the correlation, which is the 0th item in the simList
            for watcherB, sim in sorted(sims.items(), key = lambda kv : kv[1][0], reverse=True):
                if curKept > numKept:
                    break

                corr = sim[0]
                slope = sim[1]
                intercept = sim[2]
                # weight the influence of each linear regression by the strength of the correlation
                #print("watcherB ", watcherB, "corr ", corr)
                #print("watcherA ", watcherA, "movieID ", movieID, "prediction ", slope * trainWatchersDict[watcherB][movieID] + intercept)

                #corr_prediction += math.fabs(corr) * (slope * trainWatchersDict[watcherB][movieID] + intercept)
                #total_corr += math.fabs(corr)
                corr_prediction += corr * (slope * trainWatchersDict[watcherB][movieID] + intercept)
                total_corr += corr

                curKept += 1

            if total_corr > 0:
                corr_prediction /= total_corr
                if corr_prediction > 5:
                    corr_prediction = 5
                elif corr_prediction < 0.5:
                    corr_prediction = 0.5
            else:
                corr_prediction = 'NA'
            watcherA_corr_predictions[movieID] = corr_prediction

        # at this point, watcherA_diff_predictions and watcherA_corr_predictions are populated with predicted ratings
        # for all movies we need to predict for this watcher (ie for all movies in his answers dictionary)
        # add this dictionary to the aggregate dictionary for all watchers

        corr_predictions[watcherA] = watcherA_corr_predictions

    # at this point, have predicted for all users in the test data
    #print("corr_predictions")
    #print(corr_predictions)
    return corr_predictions

#VERIFIED
# fuse the predictions from various prediction systems
def fuse_predictions( systems_list ):
    print("fuse_predictions @", datetime.now())
    # key = userID
    # value = subdict
    # subdict key = movieID
    # subdict value = predicted rating of movieID
    fused = copy.deepcopy(systems_list[0])

    for userA, userA_predictions in fused.items():
        for movieID in userA_predictions.keys():
            predicted_rating = 0.0
            predictions_count = 0
            for i in range(0, len(systems_list)):
                if systems_list[i][userA][movieID] != 'NA':
                    predicted_rating += systems_list[i][userA][movieID]
                    predictions_count += 1
            if predictions_count == 0:
                predicted_rating = 'NA'
            else:
                predicted_rating /= predictions_count

            fused[userA][movieID] = predicted_rating

    return fused
