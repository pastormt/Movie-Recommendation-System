import preprocessing
import calculations
import evaluation

watchersDict = preprocessing.saveWatchersDict("./movieLens/500K_ratings.csv")
testWatchersAnswers, testWatchersDict, trainWatchersDict = preprocessing.createTrainingAndTest(watchersDict, 20)
itemSlopes = calculations.calcItemSlopes(trainWatchersDict)
usersSims = calculations.calcUserSims(testWatchersDict, trainWatchersDict)
itemPredictions = calculations.predict_item_based(testWatchersDict, testWatchersAnswers, itemSlopes)
userPredictions = calculations.predict_user_based(testWatchersDict, testWatchersAnswers, trainWatchersDict, usersSims, 1, 0.75)
fusedPredictions = calculations.fuse_predictions([itemPredictions, userPredictions])
print("Evaluation: Item Predictions vs Actual")
print(evaluation.evaluate(itemPredictions, testWatchersAnswers))
print("Evaluation: User Predictions vs Actual")
print(evaluation.evaluate(userPredictions, testWatchersAnswers))
print("Evaluation: Fused Predictions vs Actual")
print(evaluation.evaluate(fusedPredictions, testWatchersAnswers))

'''
print("trainWatchersDict")
print(trainWatchersDict)
print("testWatchersDict")
print(testWatchersDict)
print("testWatchersAnswers")
print(testWatchersAnswers)
print("usersSims")
print(usersSims)
print("watchersDict")
print(watchersDict)
'''
