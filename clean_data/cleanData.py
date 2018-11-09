import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys
sys.path.append("../library")
import RecSys as rs
#patch = "" # For Google CoLab
path = "../data/"

chefmozacccepts = pd.read_csv(path+"chefmozaccepts.csv")
chefmozcuisine = pd.read_csv(path+"chefmozcuisine.csv")
chefmozhours4 = pd.read_csv(path+"chefmozhours4.csv")
chefmozparking = pd.read_csv(path+"chefmozparking.csv")
geoplaces2 = pd.read_csv(path+"geoplaces2.csv")
rating_final = pd.read_csv(path+"rating_final.csv")
usercuisine = pd.read_csv(path+"usercuisine.csv")
userpayment = pd.read_csv(path+"userpayment.csv")
userprofile = pd.read_csv(path+"userprofile.csv")
# This will contain the list of Datas that we will 
# use for the Recommendation System
listOfData_r = [rating_final]

rs.replaceID(realID=132706,falseID=132584,ID='placeID',data=listOfData_r)