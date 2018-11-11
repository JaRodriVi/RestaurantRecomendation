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
# data:: A DataFrame or a list of DataFrame
# -----------
### Replace the falseID for the realID on data[ID]
# -----------
def replaceID(realID, falseID, ID, data):
    for df in data:
        if ID in list(list(df)):
            df[ID] = df[ID].replace(falseID,realID)     
            
# -----------
### params: realID::String
# data:: A DataFrame or a list of DataFrame
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

# -----------
### params: 
# data:: A DataFrame
# column:: String of column to merge
# -----------
### Merge duplicates and clean them from column 
# -----------
def unionData(data,column):
    columns = list(data)
    columns.remove(column)
    dataRe = pd.DataFrame(data['placeID'])
    for col in columns:
        data_list = data.groupby(column).apply(lambda x: ';'.join(map(lambda y: str(y),list(x[col].drop_duplicates()))))
        data_list = pd.DataFrame({column:data_list.index,col:data_list.values})
        dataRe = dataRe.merge(data_list, how = 'left', on = column)
    dataRe=dataRe.drop_duplicates(column)
    return dataRe
    