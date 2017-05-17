import math
import numpy as np
from datetime import datetime
# both predictions and answers will have the same movies for each test user
# the value of the predictions is in how close the predicted ratings are to the actual ratings
# ways to measure this:
# 1) average difference
# 2) correlation / cognitive diversity?
def evaluate( testWatchersPredictions, testWatchersAnswers ):
    print("evaluate @", datetime.now())
    diff = 0.0
    count_predicted = 0
    count_NA = 0 # items that could not be predicted... see calculations.py

    test_predicted = 0.0
    test_actual = 0.0

    squared_error = 0.0

    for userA, predictions in testWatchersPredictions.items():
        for movieID, predicted_rating in predictions.items():
            if predicted_rating != 'NA':
                test_predicted += predicted_rating
                test_actual += testWatchersAnswers[userA][movieID]

                this_diff = math.fabs(predicted_rating - testWatchersAnswers[userA][movieID])
                diff += this_diff
                squared_error += math.pow(this_diff, 2)
                count_predicted += 1
            else:
                count_NA += 1

    RMSE = math.sqrt(squared_error / test_predicted)
    print("Mean diff: ", diff / count_predicted)
    print("RMSE: ", RMSE)

    # standard deviation & mean of actuals
    actual_ratings = []
    for watcher, itemsDict in testWatchersAnswers.items():
        actual_ratings += [v for k,v in itemsDict.items()]
    mean_actual_rating = np.mean(actual_ratings)
    std_dev_actual_rating = np.std(actual_ratings)
    print("Mean Actual Rating: ", mean_actual_rating)
    print("Std Dev Actual Rating: ", std_dev_actual_rating)

    #print("test_predicted ", test_predicted, "test_actual ", test_actual)
    #print("diff ", diff, "count_predicted ", count_predicted, "count_NA ", count_NA)
    return [diff / count_predicted, count_NA, RMSE, std_dev_actual_rating, mean_actual_rating]
