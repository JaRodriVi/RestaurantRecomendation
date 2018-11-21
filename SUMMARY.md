# Summary

This is may KSchool Master in Data Science Final Proyect.
That's my first Data Science Proyect and this proyect teach me the real problem of Data Science, the Datas.

Due to the development of the project I have seen the need to make decisions about the data such as the grouping of variables and the elimination of others in order to make a model.

The model has not been as positive as I would like it to have been, partly because of my fault and my bad timing, but on the other hand because of the chosen data.

Before I look a little over the data with graphics I would like to apologize to the teachers who will evaluate. I'm so sorry Dani and Isra.

## Content
#### Restaurants

* chefmozaccepts.csv
* chefmozcuisine.csv
* chefmozhours4.csv
* chefmozparking.csv
* geoplaces2.csv

#### Consumers

* usercuisine.csv
* userpayment.csv
* userprofile.csv

#### User-Item-Rating

* rating_final.csv



### Clean

The most important clean that we did is the group of the restaurant type.
As we can see:
(imgs/beforeRtype.png)

At first we have a variable with a lot of categories, but we transform as much as possible and we reduce the number of categories
(imgs/afterRtype.png)

### Let go to see ratings

The data-set give us a rating based on 0 - 2. That's I supose that is
* 0 = bad
* 1 = regular
* 2 = good
For that reason I prefer transform rating in -1 - 1, because I think that the bad rating are negative.

We can see there how the transformation affected to us data:

Rating 0 - 2
(/imgs/rating02.png)

Rating -1 - 1
(/imgs/rating-11.png)

As we can see, on our data have bad restaurants :D 

### Co-Matris and User Co-Matrix

The user Co-Matrix is the Co-Matrix but with a little change, we use the information of the user to modify the Co-Matrix and reward the restaurant that have some similarity with their preferences.

There we have de Co-Matrix:
(/imgs/coMatrix.png)

And here the user Co-Matrix of one user
(/imgs/userCoMatrix.png)


For other hand, we can use sorted all restaurant in order to most Rating, so we have this Matrix.
Co-Matrix:
(/imgs/coMatrixSorted.png)

user Co-Matrix of one user
(/imgs/userCoMatrixSorted.png)
