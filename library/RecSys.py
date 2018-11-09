### This will be the library for my Recommendation System
## Restaurant Recommendation System
## Data from Kaggle
# https://www.kaggle.com/uciml/restaurant-data-with-consumer-ratings

import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns

# -----------
### params: realID::String
# realID::String
# falseID::String
# ID::String
# data:: single DataFrame or a list of DataFrame
# -----------
### Replace the falseID for the realID on data[ID]
# -----------
def replaceID(realID, falseID, ID, data):
    for df in data:
        if ID in list(list(df)):
            df[ID] = df[ID].replace(falseID,realID)     
            
# -----------
### params: realID::String
# data:: single DataFrame or a list of DataFrame
# find:: String
# -----------
### Find in data the "find" parametter, and return for 
### each data a list of columns that have "find"
# -----------
def checkData(data, find):
    dataFind = []
    indexAndColumn = []
    for i in range(len(data)):
        df = data[i]
        for col in list(df):
            if (len(df[df[col].astype(str)==find])!=0):
                indexAndColumn.append((i,col))
                dataFind.append(df[df[col]==find])
    return indexAndColumn,dataFind 
    