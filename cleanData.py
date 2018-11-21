import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys
sys.path.append("../library")
import RecSys as rs
#path = "" # For Google CoLab
pathData = sys.path[0] + "/data/"
pathClean = sys.path[0] + "/clean_data/"

chefmozacccepts = pd.read_csv(pathData+"chefmozaccepts.csv")
chefmozcuisine = pd.read_csv(pathData+"chefmozcuisine.csv")
chefmozhours4 = pd.read_csv(pathData+"chefmozhours4.csv")
chefmozparking = pd.read_csv(pathData+"chefmozparking.csv")
geoplaces2 = pd.read_csv(pathData+"geoplaces2.csv")
rating_final = pd.read_csv(pathData+"rating_final.csv")
usercuisine = pd.read_csv(pathData+"usercuisine.csv")
userpayment = pd.read_csv(pathData+"userpayment.csv")
userprofile = pd.read_csv(pathData+"userprofile.csv")

# This will contain the list of Datas that we will 
# use for the Recommendation System
listOfData_r = [rating_final]

# This doesn't make much sense, we can split the Clasification for have less dummy variables, 
# but we will try make the recomendation with full data
chefmozacccepts['Rpayment_accepts'] = chefmozacccepts['Rpayment']
chefmozacccepts['Rpayment_accepts'] = chefmozacccepts['Rpayment_accepts'].replace(['VISA', 'MasterCard-Eurocard', 
                                                                                  'American_Express','bank_debit_cards',
                                                                                   'Discover', 'Carte_Blanche',
                                                                                   'Diners_Club', 'Visa', 
                                                                                   'Japan_Credit_Bureau'], 'credictCard')
chefmozacccepts['Rpayment_accepts'] = chefmozacccepts['Rpayment_accepts'].replace(['gift_certificates'], 'checks')
chefmozacccepts['Rpayment_accepts'] = chefmozacccepts['Rpayment_accepts'].astype('category')

chefmozcuisine['Rcuisine_Type'] = chefmozcuisine['Rcuisine']
chefmozcuisine['Rcuisine_Type'] = chefmozcuisine['Rcuisine_Type'].replace(['French','Spanish','Italian',
                                                                           'Seafood','Greek','Mediterranean',
                                                                           'Portuguese','Lebanese', 'Moroccan',
                                                                           'Israeli','Tapas','Basque',
                                                                           'Tunisian','Turkish',
                                                                           'North_African'], 'Mediterranean')
chefmozcuisine['Rcuisine_Type'] = chefmozcuisine['Rcuisine_Type'].replace(['Latin_American','Mexican',
                                                                           'Brazilian','Caribbean','Chilean',
                                                                           'Filipino','Cuban','Hawaiian','Peruvian',
                                                                           'Jamaican','Southern','Regional',
                                                                           'Indigenous'], 'South_American')
chefmozcuisine['Rcuisine_Type'] = chefmozcuisine['Rcuisine_Type'].replace(['Fast_Food','Hot_Dogs',
                                                                           'Burgers','Deli-Sandwiches',
                                                                           'Pizzeria'], 'Fast_Food')
chefmozcuisine['Rcuisine_Type'] = chefmozcuisine['Rcuisine_Type'].replace(['Asian','Mongolian','Chinese',
                                                                           'Japanese','Sushi','Vietnamese',
                                                                           'Korean','Thai',
                                                                           'Indian-Pakistani','Tibetan'
                                                                           ,'Southeast_Asian', 'Burmese','Dim_Sum',
                                                                           'Malaysian','Cambodian'], 'Asian')
chefmozcuisine['Rcuisine_Type'] = chefmozcuisine['Rcuisine_Type'].replace(['German','Polish', 
                                                                           'Dutch-Belgian','Continental-European',
                                                                           'Eastern_European','Irish','Hungarian',
                                                                           'British','Romanian','Austrian',
                                                                           'Scandinavian','Swiss','Russian-Ukrainian'],
                                                                          'European')
chefmozcuisine['Rcuisine_Type'] = chefmozcuisine['Rcuisine_Type'].replace(['Afghan','Armenian','Persian'
                                                                           ,'Middle_Eastern'], 'Middle East')
chefmozcuisine['Rcuisine_Type'] = chefmozcuisine['Rcuisine_Type'].replace(['African','Ethiopian'], 'African')
chefmozcuisine['Rcuisine_Type'] = chefmozcuisine['Rcuisine_Type'].replace(['Breakfast-Brunch','Bagels'
                                                                           ,'Juice'], 'Breakfast')
chefmozcuisine['Rcuisine_Type'] = chefmozcuisine['Rcuisine_Type'].replace(['Bar_Pub_Brewery','Bar'], 'Bar')
chefmozcuisine['Rcuisine_Type'] = chefmozcuisine['Rcuisine_Type'].replace(['Cafeteria','Cafe-Coffee_Shop'
                                                                           ,'Tea_House'], 'Coffee_Shop')
chefmozcuisine['Rcuisine_Type'] = chefmozcuisine['Rcuisine_Type'].replace(['Fine_Dining','Organic-Healthy'
                                                                           ,'Vegetarian'], 'Healthy-Vegetarian')
chefmozcuisine['Rcuisine_Type'] = chefmozcuisine['Rcuisine_Type'].replace(['American','California',
                                                                           'Southwestern','Canadian',
                                                                           'Cajun-Creole','Pacific_Northwest',
                                                                           'Tex-Mex'], 'North_American')
chefmozcuisine['Rcuisine_Type'] = chefmozcuisine['Rcuisine_Type'].replace(['Steaks','Barbecue'], 'Meat')
chefmozcuisine['Rcuisine_Type'] = chefmozcuisine['Rcuisine_Type'].replace(['Dessert-Ice_Cream'], 'Ice_Cream')
chefmozcuisine['Rcuisine_Type'] = chefmozcuisine['Rcuisine_Type'].replace(['Doughnuts','Bakery'], 'Bakery')
chefmozcuisine['Rcuisine_Type'] = chefmozcuisine['Rcuisine_Type'].replace(['Contemporary','Fusion','Eclectic'], 'Contemporary')
chefmozcuisine['Rcuisine_Type'] = chefmozcuisine['Rcuisine_Type'].replace(['Australian','Polynesian',
                                                                           'Indonesian','Pacific_Rim'], 'Australian')

chefmozparking['parking'] = chefmozparking['parking_lot']
chefmozparking['parking'] = chefmozparking['parking'].replace(['yes','public', 'valet parking'
                                                               ,'validated parking','fee'], 'yes')
chefmozparking['parking'] = chefmozparking['parking'].replace(['none','street'], 'no')

geoplaces2['have_smoking_area']=geoplaces2['smoking_area']
geoplaces2['have_smoking_area']=geoplaces2['have_smoking_area'].replace(['only at bar', 'permitted'
                                                                         , 'section'],'yes')
geoplaces2['have_smoking_area']=geoplaces2['have_smoking_area'].replace(['none','not permitted'],'no')

geoplaces2['accessibility'] = geoplaces2['accessibility']
geoplaces2['accessibility'] = geoplaces2['accessibility'].replace(['completely', 'partially'],'yes')
geoplaces2['accessibility'] = geoplaces2['accessibility'].replace(['no_accessibility'],'no')

geoplaces2['franchise']=geoplaces2['franchise'].replace('t','no')
geoplaces2['franchise']=geoplaces2['franchise'].replace('f','yes')

userpayment['Upayment_accepts'] = userpayment['Upayment']
userpayment['Upayment_accepts'] = userpayment['Upayment_accepts'].replace(['VISA', 'MasterCard-Eurocard'
                                                                           ,'American_Express','bank_debit_cards'
                                                                           ,'Discover', 'Carte_Blanche', 'Diners_Club'
                                                                           , 'Visa', 'Japan_Credit_Bureau'],
                                                                          'credictCard')
userpayment['Upayment_accepts'] = userpayment['Upayment_accepts'].replace(['gift_certificates'], 'checks')

usercuisine['Rcuisine_Type'] = usercuisine['Rcuisine']
usercuisine['Rcuisine_Type'] = usercuisine['Rcuisine_Type'].replace(['French','Spanish','Italian','Seafood',
                                                                     'Greek','Mediterranean','Portuguese',
                                                                     'Lebanese', 'Moroccan','Israeli',
                                                                     'Tapas','Basque','Tunisian','Turkish'
                                                                     ,'North_African'], 'Mediterranean')
usercuisine['Rcuisine_Type'] = usercuisine['Rcuisine_Type'].replace(['Latin_American','Mexican','Brazilian',
                                                                     'Caribbean','Chilean','Filipino'
                                                                     ,'Cuban','Hawaiian','Peruvian','Jamaican',
                                                                     'Southern','Regional','Indigenous'], 'South_American')
usercuisine['Rcuisine_Type'] = usercuisine['Rcuisine_Type'].replace(['Fast_Food','Hot_Dogs','Burgers','Deli-Sandwiches'
                                                                     ,'Pizzeria'], 'Fast_Food')
usercuisine['Rcuisine_Type'] = usercuisine['Rcuisine_Type'].replace(['Asian','Mongolian','Chinese','Japanese','Sushi',
                                                                     'Vietnamese', 'Korean','Thai',
                                                                     'India-Pakistani','Tibetan','Southeast_Asian',
                                                                     'Burmese','Dim_Sum','Malaysian','Cambodian'], 'Asian')
usercuisine['Rcuisine_Type'] = usercuisine['Rcuisine_Type'].replace(['German','Polish', 'Dutch-Belgian',
                                                                     'Continental-European','Eastern_European',
                                                                     'Irish','Hungarian','British',
                                                                     'Romanian','Austrian','Scandinavian',
                                                                     'Swiss','Russian-Ukrainian'], 'European')
usercuisine['Rcuisine_Type'] = usercuisine['Rcuisine_Type'].replace(['Afghan','Armenian','Persian','Middle_Eastern'], 'Middle East')
usercuisine['Rcuisine_Type'] = usercuisine['Rcuisine_Type'].replace(['African','Ethiopian'], 'African')
usercuisine['Rcuisine_Type'] = usercuisine['Rcuisine_Type'].replace(['Breakfast-Brunch','Bagels','Juice'], 'Breakfast')
usercuisine['Rcuisine_Type'] = usercuisine['Rcuisine_Type'].replace(['Bar_Pub_Brewery','Bar'], 'Bar')
usercuisine['Rcuisine_Type'] = usercuisine['Rcuisine_Type'].replace(['Cafeteria','Cafe-Coffee_Shop','Tea_House'], 'Coffee_Shop')
usercuisine['Rcuisine_Type'] = usercuisine['Rcuisine_Type'].replace(['Fine_Dining','Organic-Healthy','Vegetarian'], 'Healthy-Vegetarian')
usercuisine['Rcuisine_Type'] = usercuisine['Rcuisine_Type'].replace(['American','California','Southwestern',
                                                                     'Canadian','Cajun-Creole','Pacific_Northwest',
                                                                     'Tex-Mex'], 'North_American')
usercuisine['Rcuisine_Type'] = usercuisine['Rcuisine_Type'].replace(['Steaks','Barbecue'], 'Meat')
usercuisine['Rcuisine_Type'] = usercuisine['Rcuisine_Type'].replace(['Dessert-Ice_Cream'], 'Ice_Cream')
usercuisine['Rcuisine_Type'] = usercuisine['Rcuisine_Type'].replace(['Doughnuts','Bakery'], 'Bakery')
usercuisine['Rcuisine_Type'] = usercuisine['Rcuisine_Type'].replace(['Contemporary','Fusion','Eclectic'], 'Contemporary')
usercuisine['Rcuisine_Type'] = usercuisine['Rcuisine_Type'].replace(['Australian','Polynesian','Indonesian',
                                                                     'Pacific_Rim'], 'Australian')

userprofile['smoker'] = userprofile['smoker'].map(lambda x: 'yes' if x else 'no')
userprofile['dress_preference'] = userprofile['dress_preference'].replace(['elegant'],'formal')
userprofile['dress_preference'] = userprofile['dress_preference'].replace(['no preference','?'],'other')

rs.replaceID(realID=132706,falseID=132584,ID='placeID',data=listOfData_r)

###############
# Those will be the data that we will use for the model and app
###############
userProfile_r = userprofile[['userID', 'smoker', 'drink_level','dress_preference', 
                             'ambience', 'transport', 'marital_status','hijos', 
                             'religion', 'activity']]
userProfile_r['need_Parking'] = userProfile_r['transport']
userProfile_r['need_Parking'] = userProfile_r['need_Parking'].replace(['car owner'],'yes')
userProfile_r['need_Parking'] = userProfile_r['need_Parking'].replace(['on foot', 'public'],'no')
userProfile_r['need_Parking'] = userProfile_r['need_Parking'].replace(['?'],'other')

usercuisine_list = usercuisine.groupby('userID').apply(lambda x: list(x['Rcuisine_Type']))
usercuisine_list = pd.DataFrame({'userID':usercuisine_list.index,'Rcuisine_Type':usercuisine_list.values})
userProfile_r = userProfile_r.merge(usercuisine_list, how = 'left', on = 'userID')

userpayment_list= userpayment.groupby('userID').apply(lambda x: list(x['Upayment_accepts']))
userpayment_list = pd.DataFrame({'userID':userpayment_list.index,'Upayment_accepts':userpayment_list.values})
userProfile_r = userProfile_r.merge(userpayment_list, how = 'left', on = 'userID')

userProfile_r['Upayment_accepts'] = userProfile_r['Upayment_accepts'].map(lambda x: 'nan' if type(x)==float else ';'.join(list(x)))
userProfile_r['Upayment_accepts'] = userProfile_r['Upayment_accepts'].map(lambda x: 'yes' if 'credictCard' in x.split(';') else 'no')

userProfile_r['Rcuisine_Type'] = userProfile_r['Rcuisine_Type'].map(lambda x: 'nan' if type(x)==float else ';'.join(list(set(list(x)))))

userGeo_r = userprofile[['userID', 'latitude', 'longitude']]

chefmozProfile_r = geoplaces2[['placeID', 'alcohol', 'have_smoking_area','dress_code',
                               'accessibility', 'price', 'Rambience', 'franchise', 'other_services']]

chefmozProfile_r= chefmozProfile_r.merge(chefmozacccepts, how = 'left', on = 'placeID')
chefmozProfile_r= chefmozProfile_r.merge(chefmozcuisine, how = 'left', on = 'placeID')
chefmozProfile_r= chefmozProfile_r.merge(chefmozhours4, how = 'left', on = 'placeID')
chefmozProfile_r= chefmozProfile_r.merge(chefmozparking, how = 'left', on = 'placeID')

chefmozGeo_r = geoplaces2[['placeID', 'name', 'latitude', 'longitude', 'the_geom_meter',
                           'address', 'city', 'state', 'country', 'fax', 'zip']]

chefmozProfile_r = rs.unionData(chefmozProfile_r,'placeID')
chefmozProfile_r['CreditCardAccepts'] = chefmozProfile_r['Rpayment_accepts'].\
    map(lambda x:'yes' if 'credictCard' in str(x).split(';') else 'no')

userChefmozRelation_r = rating_final.copy()
userChefmozRelation_r['rating'] = userChefmozRelation_r['rating'].apply(lambda x: x-1)
userChefmozRelation_r['food_rating'] = userChefmozRelation_r['food_rating'].apply(lambda x: x-1)
userChefmozRelation_r['service_rating'] = userChefmozRelation_r['service_rating'].apply(lambda x: x-1)

##########
# Drop Session
##########
chefmozProfile_r = chefmozProfile_r.drop(['Rpayment','Rpayment_accepts','Rcuisine','hours','days'], axis=1)

listPlaceID2Drop = list(chefmozProfile_r[chefmozProfile_r["Rcuisine_Type"]=='nan']['placeID'].values)
rating_final = rating_final.drop(rating_final[rating_final['placeID'].isin(listPlaceID2Drop)].index)
chefmozGeo_r = chefmozGeo_r.drop(chefmozGeo_r[chefmozGeo_r['placeID'].isin(listPlaceID2Drop)].index)
userChefmozRelation_r=userChefmozRelation_r.drop(userChefmozRelation_r[userChefmozRelation_r['placeID'].
                                                                       isin(listPlaceID2Drop)].index)
chefmozProfile_r = chefmozProfile_r.drop(chefmozProfile_r[chefmozProfile_r['placeID'].isin(listPlaceID2Drop)].index)

##########
# Reset placeID and userID
##########

userDict = pd.DataFrame(list(range(1,len(userProfile_r['userID'].unique())+1)),
                        index = userProfile_r['userID']).to_dict()[0]
restDict = pd.DataFrame(list(range(len(chefmozProfile_r['placeID'].unique()))),
                        index = chefmozProfile_r['placeID']).to_dict()[0]
userProfile_r['userID'] = userProfile_r['userID'].map(lambda x: userDict[x])
userGeo_r['userID'] = userGeo_r['userID'].map(lambda x: userDict[x])
userChefmozRelation_r['userID'] = userChefmozRelation_r['userID'].map(lambda x: userDict[x])
rating_final['userID'] = rating_final['userID'].map(lambda x: userDict[x])
userChefmozRelation_r['placeID'] = userChefmozRelation_r['placeID'].map(lambda x: restDict[x])
chefmozProfile_r['placeID'] = chefmozProfile_r['placeID'].map(lambda x: restDict[x])
chefmozGeo_r['placeID'] = chefmozGeo_r['placeID'].map(lambda x: restDict[x])
rating_final['placeID'] = rating_final['placeID'].map(lambda x: restDict[x])

##########
# Write CSV
##########
userProfile_r.to_csv(pathClean+"userProfile_r.csv", sep=';')
userGeo_r.to_csv(pathClean+"userGeo_r.csv", sep=';')
userChefmozRelation_r.to_csv(pathClean+"userChefmozRelation_r.csv", sep=';')
chefmozProfile_r.to_csv(pathClean+"chefmozProfile_r.csv", sep=';')
chefmozGeo_r.to_csv(pathClean+"chefmozGeo_r.csv", sep=';')
rating_final.to_csv(pathClean+"rating_final_r.csv", sep=';')