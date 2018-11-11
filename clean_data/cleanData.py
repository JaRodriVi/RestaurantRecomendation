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

# This doesn't make much sense, we can split the Clasification for have less dummy variables, 
# but we will try make the recomendation with full data
chefmozacccepts['Rpayment_accepts'] = chefmozacccepts['Rpayment']
chefmozacccepts['Rpayment_accepts'] = chefmozacccepts['Rpayment_accepts'].replace(['VISA', 'MasterCard-Eurocard', 
                                                                                   'American_Express','bank_debit_cards',
                                                                                   'Discover', 'Carte_Blanche',
                                                                                   'Diners_Club', 'Visa', 
                                                                                   'Japan_Credit_Bureau'], ' credictCard')
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

chefmozhours4['days'] = chefmozhours4['days'].replace(['Mon;Tue;Wed;Thu;Fri;'],'Diary_Days')

chefmozparking['parking'] = chefmozparking['parking_lot']
chefmozparking['parking'] = chefmozparking['parking'].replace(['yes','public', 'valet parking'
                                                               ,'validated parking','fee'], 'yes')
chefmozparking['parking'] = chefmozparking['parking'].replace(['none','street'], 'no')

geoplaces2['have_smoking_area']=geoplaces2['smoking_area']
geoplaces2['have_smoking_area']=geoplaces2['have_smoking_area'].replace(['only at bar', 'permitted'
                                                                         , 'section'],'yes')
geoplaces2['have_smoking_area']=geoplaces2['have_smoking_area'].replace(['none','not permitted'],'no')

geoplaces2['accessibility'] = geoplaces2['accessibility']
geoplaces2['accessibility'] = geoplaces2['accessibility'].replace(['completely', 'partially'],'yes_accessibility')

geoplaces2['franchise']=geoplaces2['franchise'].replace('t','no')
geoplaces2['franchise']=geoplaces2['franchise'].replace('f','yes')

userpayment['Upayment_accepts'] = userpayment['Upayment']
userpayment['Upayment_accepts'] = userpayment['Upayment_accepts'].replace(['VISA', 'MasterCard-Eurocard'
                                                                           ,'American_Express','bank_debit_cards'
                                                                           ,'Discover', 'Carte_Blanche', 'Diners_Club'
                                                                           , 'Visa', 'Japan_Credit_Bureau'],
                                                                          ' credictCard')
userpayment['Upayment_accepts'] = userpayment['Upayment_accepts'].replace(['gift_certificates'], 'checks')
userpayment['Upayment_accepts'] = userpayment['Upayment_accepts'].astype('category')

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
usercuisine['Rcuisine_Type'] = usercuisine['Rcuisine_Type'].replace(['German','Polish', 'Dutch-Belgian','Continental-European','Eastern_European','Irish','Hungarian','British','Romanian','Austrian','Scandinavian','Swiss','Russian-Ukrainian'], 'European')
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

rs.replaceID(realID=132706,falseID=132584,ID='placeID',data=listOfData_r)

###############
# Those will be the data that we will use for the model and app
###############
userProfile_r = userprofile[['userID', 'smoker', 'drink_level','dress_preference', 
                             'ambience', 'transport', 'marital_status','hijos', 
                             'religion', 'activity']]

usercuisine_list = usercuisine.groupby('userID').apply(lambda x: list(x['Rcuisine_Type']))
usercuisine_list = pd.DataFrame({'userID':usercuisine_list.index,'Rcuisine_Type':usercuisine_list.values})
userProfile_r = userProfile_r.merge(usercuisine_list, how = 'left', on = 'userID')

userpayment_list= userpayment.groupby('userID').apply(lambda x: list(x['Upayment_accepts']))
userpayment_list = pd.DataFrame({'userID':userpayment_list.index,'Upayment_accepts':userpayment_list.values})
userProfile_r = userProfile_r.merge(userpayment_list, how = 'left', on = 'userID')

userGeo_r = userprofile[['userID', 'latitude', 'longitude']]

userChefmozRelation_r = rating_final
userChefmozRelation_r = userChefmozRelation_r.merge(userpayment, how='left', on='userID')
userChefmozRelation_r = userChefmozRelation_r.merge(usercuisine, how='left', on='userID')

chefmozProfile_r = geoplaces2[['placeID', 'alcohol', 'smoking_area','dress_code',
                               'accessibility', 'price', 'Rambience', 'franchise',
                               'area', 'other_services']]

chefmozProfile_r= chefmozProfile_r.merge(chefmozacccepts, how = 'left', on = 'placeID')
chefmozProfile_r= chefmozProfile_r.merge(chefmozcuisine, how = 'left', on = 'placeID')
chefmozProfile_r= chefmozProfile_r.merge(chefmozhours4, how = 'left', on = 'placeID')
chefmozProfile_r= chefmozProfile_r.merge(chefmozparking, how = 'left', on = 'placeID')

chefmozGeo_r = geoplaces2[['placeID', 'latitude', 'longitude', 'the_geom_meter',
                           'address', 'city', 'state', 'country', 'fax', 'zip']]

chefmozProfile_r = rs.unionData(chefmozProfile_r,'placeID')

##########
# Write CSV
##########
userProfile_r.to_csv("userProfile_r.csv", sep=';')
userGeo_r.to_csv("userGeo_r.csv", sep=';')
userChefmozRelation_r.to_csv("userChefmozRelation_r.csv", sep=';')
chefmozProfile_r.to_csv("chefmozProfile_r.csv", sep=';')
chefmozGeo_r.to_csv("chefmozGeo_r.csv", sep=';')
rating_final.to_csv("rating_final_r.csv", sep=';')

