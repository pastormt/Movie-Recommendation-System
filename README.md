# Movie-Recommendation-System
A collaborative filtering movie recommendation system combining item-based and user-based approaches

## User-based collaborative filtering

### Calculating Similarities
A user-based collaborative filtering approach predicts user A’s rating on item 1 based upon the ratings of “similar” users who have already rated item 1 -- with similarity being a measure that one can define however one sees fit. I measured user-to-user similarity as the correlation between their scores on movies they had both already rated. As correlation measures the strength of the linear relationship between variables, here, a correlation close to 1 meant that user B’s scores could be used to predict user A, and vice versa. 

For the set S of users {B, C, …, J} similar (i.e. correlated) to user A, I calculated least squares fit regression lines between each user U in S and user A, based upon the movies both U and A had already rated. 


### Predicting Ratings
Finally, when it came to making predictions for ratings for movies user A has not yet rated, I proceeded as follows, for each movie M:

Take those users who have already rated movie M, and sort them from most to least correlated with user A

For the pruning percentage P, calculate P x the number of users correlated with user A. For example, if P = 30%, and there are 100 users correlated with user A, take only the 30 users with the highest correlations with A, and call this set of users set SA.

For each user U in SA, use the regression line between U and A to predict A’s rating of movie M. 

Combine the predictions made by each of these regression lines between a user U and A. Here, I use a weighted average -- where the correlation between user U and user A is the weight. That is, I weight the prediction influence of a given user U on user A’s rating of movie M by the correlation between the ratings of U and A on movies they have both rated. 

## Item-based Collaborative Filtering

### Motivation
I considered that, in addition to using similar users to predict a given user’s rating, perhaps some relationships between items will not be captured by this method alone. 

For example, to use a food analogy, suppose everyone rates coffee and chocolate similarly (i.e. the correlation between a given individual’s coffee and chocolate ratings approaches 1). If we have an individual A that we know likes coffee a lot (say rates coffee 10/10), and we only use a user-based approach, we will calculate the similarity between this user’s tastes and that of all other users. But perhaps this user might have many other foods that he likes and and dislikes, and other users may like / dislike many other items as well. If we only calculate the correlations on a user-to-user basis, the high correlation between the scores of coffee and chocolate within a given user may not be found. Perhaps the best way to predict A’s chocolate preference is based upon his known strong appreciation for coffee, if we have observed the two items’ ratings tend to vary together across other users. 

### Slope One
For this reason, I chose to employ an item-based approach as well -- and to do so, I used the popular Slope One algorithm (so called as it is a linear predictor with no slope coefficient -- or in other words, an implied coefficient of one. More formally, a typical linear regression calculates a line f(x) = ax + b, whereas Slope One calculates f(x) = x + b). The single free parameter, b, is the mean difference between 2 items’ ratings. I chose it as some experiments have shown it to be more accurate that linear regression in certain situations, likely due to its reduction of overfitting. Additionally, as it only stores 1 free parameter -- as opposed to 2 -- it requires 1/2 the storage. 

To give an example of Slope One on a sample data set:

### Slope One Example

Say we want to predict user C’s rating of movie 2. We can calculate the average difference between a user’s ratings of movies 1 and 2 based upon those users who have rated both movies. Since we know C’s rating of movie 1, we can use this difference calculation to predict C’s rating of movie 2. 

Free parameter
Calculating the mean difference between a user’s ratings of movies 1 and 2:

User A = 5 (rating for movie 1) - 4 (rating for movie 2) = 1
User B = 3 (rating for movie 1) - 1 (rating for movie 2) = 2
Mean = 1.5

On average, from the users we have who have rated both movies 1 and 2, we can see that movie 1 is rated 1.5 points higher than movie 2. 

### Prediction
Therefore, to predict user C’s rating for movie 2, we proceed as follows:
User C’s movie 2 rating = 4 (user C’s movie 1 rating) - 1.5 = predicted rating of 2.5 

## Comparison vs Benchmark
To evaluate how well our system performed against a benchmark, I considered the simplest possible prediction system would be always predicting the mean movie rating.

By measuring the standard deviation of the test set’s actual ratings, and the root mean square error (RMSE) of the predicted ratings, I was able to compare our system’s predictions to the quality of predicted ratings that could be achieved simply by always guessing the mean actual rating. 

### Keeping in mind that the rating system was out of 5 stars, our measured values are below: 
Mean true rating: 3.54 (stars out of 5)
Standard deviation of true ratings in the test set: 1.03 (stars out of 5)
RMSE of predicted ratings: 0.46 (stars out of 5) for each of our 3 systems (user-based, item-based, and fused)

We can see that the RMSE of our predicted ratings is less than ½ of the standard deviation of the true ratings -- showing that our systems did much better than simply using the mean movie rating as a predictor. 
