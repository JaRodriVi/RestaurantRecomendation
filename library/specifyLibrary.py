import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys
from sklearn.model_selection import train_test_split

sys.path.append("../library")
import RecSys as rs
path = "../clean_data/"

chefmozGeo_r = pd.read_csv(path + "chefmozGeo_r.csv", sep=';').drop(['Unnamed: 0'],axis=1)
chefmozProfile_r = pd.read_csv(path + "chefmozProfile_r.csv", sep=';').drop(['Unnamed: 0'],axis=1)
rating_final_r = pd.read_csv(path + "rating_final_r.csv", sep=';').drop(['Unnamed: 0'],axis=1)
userChefmozRelation_r = pd.read_csv(path + "userChefmozRelation_r.csv", sep=';').drop(['Unnamed: 0'],axis=1)
userGeo_r = pd.read_csv(path + "userGeo_r.csv", sep=';').drop(['Unnamed: 0'],axis=1)
userProfile_r = pd.read_csv(path + "userProfile_r.csv", sep=';').drop(['Unnamed: 0'],axis=1)

train, test = train_test_split(rating_final_r, test_size=0.2)

userProfile_r['Rcuisine_Type'] = userProfile_r['Rcuisine_Type'].map(lambda x: x.split(';'))
chefmozProfile_r['Rcuisine_Type'] = chefmozProfile_r['Rcuisine_Type'].map(lambda x: x.split(';'))

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

def userCoMatrix(userID,dataFrame,n_items,coMatix='noMatrix'):
    
    if coMatix=='noMatrix':
        coMatix=np.zeros((n_items, n_items))
        
    userCoMatrix = np.zeros((n_items, n_items))
    userInfo = dataFrame[dataFrame['userID']==userID]
    userInfo['Rcuisine_Type'] = userInfo['Rcuisine_Type'].map(lambda x: x.split(';'))
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
    list_sim_items = np.vstack([co_occurrance_similarity(id_, cooccurrance, ntop) for id_ in items_id])
    # Group by id and take the maximum frquency to remove duplicates
    largest_freq = pd.DataFrame(list_sim_items, columns=['id', 'freq']).groupby('id').agg(max).reset_index()
    
    # sort by value in descending order
    sorted_list = largest_freq.sort_values(by='freq', ascending=False)
    
    # get the top N
    out = sorted_list.values[:ntop, 0]
    return out

def co_occurrance_recommendation_for_user(userID, value, coMatrix, df, n_items, ntop=10):
    userCoM = userCoMatrix(userID, df, n_items, coMatrix)
    return co_occurrance_recommendation(value,userCoM,ntop)

def co_occurrance_recommendation_for_list_users(usersID, values, coMatrix, df, n_items, ntop=10):
    userValue = zip(usersID,values)
    return list(map(lambda x: co_occurrance_recommendation_for_user(x[0], x[1], coMatrix, df, n_items, ntop),userValue))