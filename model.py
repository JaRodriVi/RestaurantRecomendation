import sys
sys.path.append("../clean_data")
sys.path.append("../library")

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
import RecSys as rs
import random

######################
######################
######################
path="clean_data/"
chefmozGeo_r = pd.read_csv(path + "chefmozGeo_r.csv", sep=';').drop(['Unnamed: 0'],axis=1)
chefmozProfile_r = pd.read_csv(path + "chefmozProfile_r.csv", sep=';').drop(['Unnamed: 0'],axis=1)
rating_final_r = pd.read_csv(path + "rating_final_r.csv", sep=';').drop(['Unnamed: 0'],axis=1)
userChefmozRelation_r = pd.read_csv(path + "userChefmozRelation_r.csv", sep=';').drop(['Unnamed: 0'],axis=1)
userGeo_r = pd.read_csv(path + "userGeo_r.csv", sep=';').drop(['Unnamed: 0'],axis=1)
userProfile_r = pd.read_csv(path + "userProfile_r.csv", sep=';').drop(['Unnamed: 0'],axis=1)

random.seed(1234)
train, test = train_test_split(userChefmozRelation_r, test_size=0.2)

######################
######################
######################

def filteredListRatedRestaurant(train, min_ratings=0):
    listRatedRestaurant = train.groupby('placeID')['rating'].apply(list).reset_index()
    filteredListRatedRestaurant = listRatedRestaurant[listRatedRestaurant.rating.apply(lambda x: len(x)>=min_ratings)]
    meanListRatedRestaurant = filteredListRatedRestaurant['rating'].apply(np.mean)
    filteredListRatedRestaurant['mean'] = meanListRatedRestaurant
    return filteredListRatedRestaurant.sort_values('mean',ascending=False)

def filteredListRatedRestaurantExcluding(train, excludingRate=0, min_ratings=0):
    trainExcluding = train[train['rating']>=excludingRate]
    listRatedRestaurant = trainExcluding.groupby('placeID')['rating'].apply(list).reset_index()
    filteredListRatedRestaurant = listRatedRestaurant[listRatedRestaurant.rating.apply(lambda x: len(x)>=min_ratings)]
    meanListRatedRestaurant = filteredListRatedRestaurant['rating'].apply(np.mean)
    filteredListRatedRestaurant['mean'] = meanListRatedRestaurant
    return filteredListRatedRestaurant.sort_values('mean',ascending=False)

def recall_at_n(N, test, recommended, train=None):
    """
    :param N: number of recommendations
    :param test: list of movies seen by user in test
    :param train: list of movies seen by user in train. This has to be removed from the recommended list 
    :param recommended: list of movies recommended
    
    :return the recall
    """
    if train is not None: # Remove items in train
        # Esta línea de abajo estaría mal!!! por qué? Respuesta: al usar "set", perdemos el orden en la recomendación
        # rec_true =  set(recommended)- set(train)
        
        # Correct implementation
        rec_true = []
        for r in recommended:
            if r not in train:
                rec_true.append(r)
        # Equivalent 1-line of code:
        # rec_true = [r for r in recommended if r not in train]
    else:
        rec_true = recommended    
    intersection = len(set(test) & set(rec_true[:N]))
    return intersection / float(np.minimum(N, len(test)))

def apk(N, test, recommended, train=None):
    """
    Computes the average precision at N given recommendations.
    
    :param N: number of recommendations
    :param test: list of movies seen by user in test
    :param train: list of movies seen by user in train. This has to be removed from the recommended list 
    :param recommended: list of movies recommended
    
    :return The average precision at N over the test set
    """
    if train is not None: 
        rec_true = []
        for r in recommended:
            if r not in train:
                rec_true.append(r)
    else:
        rec_true = recommended    
    predicted = rec_true[:N] # top-k predictions
    
    score = 0.0 # This will store the numerator
    num_hits = 0.0 # This will store the sum of rel(i)

    for i,p in enumerate(predicted):
        if p in test and p not in predicted[:i]:
            num_hits += 1.0
            score += num_hits/(i+1.0)
    return score / min(len(test), N)

def evaluate_map(topN, trainGrouped, testGrouped, coMatrix, popularity_baseline):
    # add a prediction column to train
    trainUsersGrouped['prediction'] = trainUsersGrouped['placeID'].apply(
        lambda x: co_occurrance_recommendation(x, coMatrix, topN)
    )
    # join with test data
    joined = pd.merge(trainUsersGrouped, testUsersGrouped, how='inner', on='userID', suffixes=('_train', '_test'))
    # calculate average recall
    map_ = joined.apply(lambda l: 
             apk(N=topN, test=l[4], recommended=l[2], train=l[1]), axis=1).mean()
    print("Co-occurance model: map@%s=%.3f"%(topN, map_))
    # calculate average recall UserCoMatrix
    map_ = joined.apply(lambda l: 
             apk(N=topN, test=l[4], recommended=l[3], train=l[1]), axis=1).mean()
    print("Co-occurance UserCoMatrix model: map@%s=%.3f"%(topN, map_))
    
    map_baseline = joined.apply(lambda l: 
                 apk(N=topN, test=l[4], recommended=popularity_baseline, train=l[1]), axis=1).mean()
    print("Popularity model: map@%s=%.3f"%(topN, map_baseline))
    return map_, map_baseline

def co_occurrance_similarity(item_id, coocurrance, ntop=5):
    """
    Returns the top-N most similar items to a given one, based on the coocurrance matrix
    
    :param item_id: id of input item
    :param cooccurrance: 2-dim numpy array with the co-occurance matrix
    :param ntop: number of items to be retrieved
    
    :return top-N most similar items to the given item_id
    """
    similarItems = coocurrance[item_id, :]
    # return indeces of most similar items in descendign order
    mostSimilar = np.argsort(similarItems)[::-1]
    # remove the item itslef, maybe it's not the first element
    ##### mostSimilar = mostSimilar[1:ntop+1]
    mostSimilar = list(mostSimilar)
    mostSimilar.remove(item_id)
    mostSimilar = np.array(mostSimilar)[:ntop]
    
    # return a numpy array with the index (first column) and the value (second column) of the most similar items
    return np.stack((mostSimilar, similarItems[mostSimilar])).T

def co_occurrance_recommendation(items_id, cooccurrance, ntop=10):
    """
    Obtain the list of ntop recommendations based on a list of items (user history of views)
    
    :param items_id: list of items ids
    :param coocurrence: co-ocurrence matrix (numpy 2-dim array)
    :param ntop: top-K items to be retrieved
    
    :return list of ntop items recommended
    """
    # put together all the similar items and its value. For this, use np.vstack, wich stacks one array after 
    # another (row wise)
    
    if type(items_id)==int:
        list_sim_items = np.vstack([co_occurrance_similarity(id_, cooccurrance, ntop) for id_ in items_id])
        # Group by id and take the maximum frquency to remove duplicates
        largest_freq = pd.DataFrame(list_sim_items, columns=['id', 'freq']).groupby('id').agg(max).reset_index()

        # sort by value in descending order
        sorted_list = largest_freq.sort_values(by='freq', ascending=False)

        # get the top N
        out = sorted_list.values[:ntop, 0]
        
    elif (len(items_id)!=0):
        list_sim_items = np.vstack([co_occurrance_similarity(id_, cooccurrance, ntop) for id_ in items_id])
        # Group by id and take the maximum frquency to remove duplicates
        largest_freq = pd.DataFrame(list_sim_items, columns=['id', 'freq']).groupby('id').agg(max).reset_index()

        # sort by value in descending order
        sorted_list = largest_freq.sort_values(by='freq', ascending=False)

        # get the top N
        out = sorted_list.values[:ntop, 0]
    else :
        out=mostRatedRestaurant[:ntop]
        
    return out

# do the same for different top k values. It might be convenient to define a function!
def evaluate_recall(topN, trainGrouped, testGrouped, coMatrix, popularity_baseline):
    # add a prediction column to train
    trainUsersGrouped['prediction'] = trainUsersGrouped['placeID'].apply(
        lambda x: co_occurrance_recommendation(x, coMatrix, topN)
    )
    # join with test data
    joined = pd.merge(trainUsersGrouped, testUsersGrouped, how='inner', on='userID', suffixes=('_train', '_test'))
    # calculate average recall_coMatrix
    recall = joined.apply(lambda l: 
                 recall_at_n(N=topN, test=l[4], recommended=l[2], train=l[1]), axis=1).mean()
    print("Co-occurance model: recall@%s=%.3f"%(topN, recall))
    # calculate average recall_userCoMatrix
    recall = joined.apply(lambda l: 
                 recall_at_n(N=topN, test=l[4], recommended=l[3], train=l[1]), axis=1).mean()
    print("Co-occurance User model: recall@%s=%.3f"%(topN, recall))
    # calculate average recall for the baseline
    recall_baseline = joined.apply(lambda l: 
                 recall_at_n(N=topN, test=l[4], recommended=popularity_baseline, train=l[1]), axis=1).mean()
    print("Popularity model: recall@%s=%.3f"%(topN, recall_baseline))    
    return recall, recall_baseline


def userCoMatrix(userInfo,dataFrame,n_items,coMatix='noMatrix'):
    
    if coMatix=='noMatrix':
        coMatix=np.zeros((n_items, n_items))
        
    userCoMatrix = np.zeros((n_items, n_items))
    if type(userInfo)==np.int64:
        userInfo = dataFrame[dataFrame['userID']==userInfo]
        #userInfo['Rcuisine_Type'] = userInfo['Rcuisine_Type'].map(lambda x: print(x))
        userInfo = userInfo[['Rcuisine_Type','dress_preference','need_Parking','Upayment_accepts']].values[0]
    
    columns = ['Rcuisine_Type','dress_preference','need_Parking','Upayment_accepts']
    
    userInfo = zip(columns,userInfo)
    
    for userKey,userValue in userInfo:
        if type(userValue)!=list:
            userValue=[userValue]
        for value in userValue:
            items = [(a,b) for a in generalRdict[userKey][value] for b in generalRdict[userKey][value]]
            for item in items:
                userCoMatrix[item] += 1
    return userCoMatrix+coMatix

def co_occurrance_recommendation_for_user(userInfo, value, coMatrix, df, n_items, ntop=10):
    
    userCoM = userCoMatrix(userInfo, df, n_items, coMatrix)
    return co_occurrance_recommendation(value,userCoM,ntop)

def co_occurrance_recommendation_for_list_users(userInfo, values, coMatrix, df, n_items, ntop=10):
    userValue = zip(userInfo,values)
    return list(map(lambda x: co_occurrance_recommendation_for_user(x[0], x[1], coMatrix, df, n_items, ntop),userValue))

def createDict(tupleIDValues,others,dictionary={}):
    for ID,values in tupleIDValues:
        for value in values:
            if value in dictionary.keys():
                dictionary[value].append(ID)
            else:
                dictionary[value] = [ID]
    for values in others:
        for value in values:
            if not value in dictionary.keys():
                dictionary[value] = []
    return dictionary

######################
######################
######################

random.seed(42)

path = sys.path[0] + "/clean_data/"

chefmozGeo_r = pd.read_csv(path + "chefmozGeo_r.csv", sep=';').drop(['Unnamed: 0'],axis=1)
chefmozProfile_r = pd.read_csv(path + "chefmozProfile_r.csv", sep=';').drop(['Unnamed: 0'],axis=1)
rating_final_r = pd.read_csv(path + "rating_final_r.csv", sep=';').drop(['Unnamed: 0'],axis=1)
userChefmozRelation_r = pd.read_csv(path + "userChefmozRelation_r.csv", sep=';').drop(['Unnamed: 0'],axis=1)
userGeo_r = pd.read_csv(path + "userGeo_r.csv", sep=';').drop(['Unnamed: 0'],axis=1)
userProfile_r = pd.read_csv(path + "userProfile_r.csv", sep=';').drop(['Unnamed: 0'],axis=1)

train, test = train_test_split(userChefmozRelation_r, test_size=0.2)
trainPlaceList = train.groupby('userID')['placeID'].apply(list).reset_index()
testPlaceList = test.groupby('userID')['placeID'].apply(list).reset_index()

mergeTrainTest = pd.merge(trainPlaceList, testPlaceList, how='inner', on='userID', suffixes=('_train', '_test')).set_index('userID')

userProfile_r['Rcuisine_Type'] = userProfile_r['Rcuisine_Type'].map(lambda x: x.split(';'))
chefmozProfile_r['Rcuisine_Type'] = chefmozProfile_r['Rcuisine_Type'].map(lambda x: x.split(';'))

######################
# fixed recommendations for all Users
######################
mostVisited = train.groupby('placeID')['userID'].count()
mostVisitedRestaurant = list(mostVisited.sort_values(ascending=False).index)

mostRated = train.groupby('placeID')['rating'].sum()
mostRatedRestaurant = list(mostRated.sort_values(ascending=False).index)

mostMeanRatedRestaurant = list(filteredListRatedRestaurant(train)['placeID'])
mostMeanRatedExLowerRating = list(filteredListRatedRestaurantExcluding(train)['placeID'])

mostMeanRatedWith5Restaurant =list(filteredListRatedRestaurant(train,min_ratings=5)['placeID'])
mostMeanRatedExLowerWith5Rating =list(filteredListRatedRestaurantExcluding(train, min_ratings=5)['placeID'])

mostMeanRatedWith10Restaurant =list(filteredListRatedRestaurant(train,min_ratings=10)['placeID'])
mostMeanRatedExLowerWith10Rating =list(filteredListRatedRestaurantExcluding(train,min_ratings=10)['placeID'])
######################
######################
######################
# Co-occurrence Matrix
######################
restaurantPerUser = (train[train['rating']>=0].groupby('userID')['placeID'].apply(np.array).to_dict())
n_items = len(chefmozGeo_r['placeID'].unique())
coMatrix = np.zeros((n_items, n_items)) # co-occurrence matrix
for user,restaurant in restaurantPerUser.items():
    for r in restaurant:
        coMatrix[r, restaurant] += 1
        
######################
######################
######################
# User Co-occurrence Matrix
######################

chefmozProfline_PlaceID = chefmozProfile_r['placeID'].values
chefmozProfline_RType = chefmozProfile_r['Rcuisine_Type'].values
userProfile_Rtype = userProfile_r['Rcuisine_Type'].values
tupleRType_PlaceID = zip(chefmozProfline_PlaceID,chefmozProfline_RType)

restIDName = chefmozGeo_r.groupby('placeID')['name'].apply(id).to_dict()
restRTypeID = createDict(tupleRType_PlaceID,userProfile_Rtype)
restAlcoholID = chefmozProfile_r.groupby('alcohol')['placeID'].apply(np.array).to_dict()
restSmokeID = chefmozProfile_r.groupby('have_smoking_area')['placeID'].apply(np.array).to_dict()
restDressID = chefmozProfile_r.groupby('dress_code')['placeID'].apply(np.array).to_dict()
restDressID['other'] = []
restAccesID = chefmozProfile_r.groupby('accessibility')['placeID'].apply(np.array).to_dict()
restPriceID = chefmozProfile_r.groupby('price')['placeID'].apply(np.array).to_dict()
restAmbienceID = chefmozProfile_r.groupby('Rambience')['placeID'].apply(np.array).to_dict()
restParkingID = chefmozProfile_r.groupby('parking')['placeID'].apply(np.array).to_dict()
restParkingID['other'] = []
restCredictID = chefmozProfile_r.groupby('CreditCardAccepts')['placeID'].apply(np.array).to_dict()
restCredictID['no'] = []

generalRdict= {'Rcuisine_Type':restRTypeID, 'drink_level':restAlcoholID, 'dress_preference':restDressID, 'ambience':restAmbienceID, 'need_Parking':restParkingID, 'smoker':restSmokeID, 'Upayment_accepts':restCredictID, 'restPriceID':restPriceID, 'restAccesID':restAccesID}

def createUserCoMatrix(userInfo):
    return userCoMatrix(userInfo,userProfile_r,n_items,coMatrix)

######################
######################
######################
# Recommend me
######################

def recommendMostRated(n):
    return mostRatedRestaurant[:n]


def recommendCoMatrix(test,topN):
    return co_occurrance_recommendation(test, coMatrix, topN)


def recommendUserCoMatrix(userInfo,placeIDs,topN):
    return co_occurrance_recommendation_for_list_users(userInfo,placeIDs,coMatrix,userProfile_r,n_items,topN)


######################
######################
######################
# Test me
######################
######################
######################
######################
Ntop=5


trainUsersGrouped = train[train['rating']>=0].groupby('userID')['placeID'].apply(list).reset_index()

trainUsersGrouped['prediction_coMatrix'] = trainUsersGrouped['placeID'].apply(lambda x: co_occurrance_recommendation(x, coMatrix, Ntop))

usersIDs = trainUsersGrouped['userID'].values
placeIDs = trainUsersGrouped['placeID'].values

trainUsersGrouped['predictions_userCoMatrix'] = co_occurrance_recommendation_for_list_users(usersIDs,placeIDs,coMatrix,userProfile_r,n_items,Ntop)

testUsersGrouped = test[test['rating']>=0].groupby('userID')['placeID'].apply(list).reset_index()

joined = pd.merge(trainUsersGrouped, testUsersGrouped, how='inner', on='userID', suffixes=('_train', '_test'))
def placeID(userID):
    placeReturn = joined[joined['userID']==userID]['placeID_train']
    return placeReturn.values[0]

def testMe():
    print("recall method")
    for k in [3,5,10,30]:
        evaluate_recall(k, trainUsersGrouped, testUsersGrouped, coMatrix, mostRatedRestaurant)
        
    print("apk method") 
    for k in [3,5,10,30]:
        evaluate_recall(k, trainUsersGrouped, testUsersGrouped, coMatrix, mostRatedRestaurant)