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
    data = list(data)
    for df in data:
        if ID in list(df.columns):
            df[ID] = df[ID].replace(falseID,realID)        