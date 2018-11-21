import sys
sys.path.append("clean_data")
sys.path.append("library")
sys.path.append("model")

import cleanData
import model
import RecSys as rs


class exitClass:
    numberOfExit = 1

nExit = exitClass()
    
    
class User:
    userID = 9999999
    def __init__(self, name, tRestaurant=[], dressPreference = 'other', parking = 'other', pay = 'no'):
        self.name = name
        self.tRestaurant = tRestaurant
        self.dressPreference = dressPreference
        self.parking = parking
        self.pay = pay
    def appendAttr(self, attr,value):
        if attr=="tRestaurant":
            self.tRestaurant.append(value)
        elif attr=="dressPreference":
            self.dressPreference = value
        elif attr=="parking":
            self.parking = value
        elif attr=="pay":
            self.pay = value
    def setAttrs(self,tRestaurant, dressPreference, parking, pay):
        self.tRestaurant = tRestaurant
        self.dressPreference = dressPreference
        self.parking = parking
        self.pay = pay
    def resetUser(self):
        self.name = self.name
        self.tRestaurant = []
        self.dressPreference = 'other'
        self.parking = 'other'
        self.pay = 'no'

print("Hi, my name is Javier.")
name = input("And yours? ")

user = User(name)

print(f"Nice to meet you, {user.name}")

print("Let's start")


def return_option():
    return int(input("Enter a number of an option: "))


def options():
    dict_options={1:tellMeMore, 2:changeUser, 3:recommendMe, 4:testMe, 0:exit}
    print(f"""

    This is me Recommendation System for Restaurant in Mexico.
    
    INFO: {user.name}
        -- Type of Restaurant-> {user.tRestaurant}
        -- Dress Preference --> {user.dressPreference}
        -- Parking -----------> {user.parking}
        -- CreditCard --------> {user.pay}

    1. Tell me more about you.
    2. Change User
    3. Recommend me.
    4. Test me (Info about model)
    0. Exit
    """)
    option = return_option()
    dict_options[option]()

    
def testMe():
    print(f"""
        There have the result of my moldel.
        
        The recallN method consist:
        
        The akp method consist:
        
    """)
    model.testMe()
    return


def recommendMe():
    dict_recommend={1:mostRatedRestaurantModel, 2:coMatrixModel, 3:userCoMatrixModel, 90:options, 0:exit}
    print(f"""
    
        INFO: {user.name}
        -- Type of Restaurant-> {user.tRestaurant}
        -- Dress Preference --> {user.dressPreference}
        -- Parking -----------> {user.parking}
        -- CreditCard --------> {user.pay}

    Choose a recommendation model

    1. Most Rated Restaurant
    2. Co-occurrence Matrix
    3. User Co-occurrence Matrix (NOT FOUND ONLY GLOBAL)
    0. Exit
    """)
    option = return_option()
    dict_recommend[option]()
    
    
def mostRatedRestaurantModel():
    topN=5
    mostRR = model.recommendMostRated(topN)
    print(f"""
        Hi {user.name} with the Most Rated Restaurant Model
        we recommend you the following Restaurant
    """)
    for i in mostRR:
        print(i)
    print("""
        Pls press enter to go to the index.
    """)
    input("Enter a number of an option: ")
    options()
    
    
def coMatrixModel():
    if user.userID == 9999999:
        placeIDs = []
    else :
        placeIDs = model.placeID(user.userID)
    topN=5
    mostCM = model.recommendCoMatrix(placeIDs,topN)
    print(f"""
        Hi {user.name} with the Co-Matrix Restaurant Model
        we recommend you the following Restaurant
    """)
    for i in mostCM:
        print(i)
    print("""
        Pls press enter to go to the index.
    """)
    input("Enter a number of an option: ")
    options()
        
        
def userCoMatrixModel():
    if user.userID == 9999999:
        userInfo=[user.tRestaurant,user.dressPreference,user.parking,user.pay]
        placeIDs = []
    else :
        userInfo=[user.tRestaurant[0],user.dressPreference,user.parking,user.pay]
        placeIDs = model.placeID(user.userID)
    topN = 5
    mostUCM = model.recommendUserCoMatrix(userInfo,placeIDs,topN)
    print(f"""
        Hi {user.name} with the User Co-Matrix Restaurant Model
        we recommend you the following Restaurant
    """)
    for i in mostUCM:
        print(i)
    print("""
        Pls press enter to go to the index.
    """)
    input("Enter a number of an option: ")
    options()

    
def changeUser():
    dict_changeUser = {1:newUser, 2:testUser,0: exit, 90: options}
    print("""
    Please chose one option:
    1.  New User
    2.  Test User
    0.  Exit
    90. Back
    """)
    option = return_option()
    dict_changeUser[option]()
  

def newUser():
    user.resetUser()
    options()

    
def testUser():
    dict_testUser = {90:options,0:exit}
    j = 0
    testUserList = list(model.test.userID)
    stop = len(testUserList)
    while True: 
        for i in range(10):
            if(j+i<stop):
                print(f"{i}.  -------")
                print(f" userID: {testUserList[j+i]}" )
                print(f" Type of restaurant: {model.userProfile_r[model.userProfile_r['userID'] == testUserList[j+i]]['Rcuisine_Type'].values[0]}")
                print(f" Dress Preferent: {model.userProfile_r[model.userProfile_r['userID'] == testUserList[j+i]]['dress_preference'].values[0]}")
                print(f" Need Parking?: {model.userProfile_r[model.userProfile_r['userID'] == testUserList[j+i]]['need_Parking'].values[0]}")
                print(f" Credit Card?: {model.userProfile_r[model.userProfile_r['userID'] == testUserList[j+i]]['Upayment_accepts'].values[0]}")
        print("--------")
        print("10. Next")
        print("90. Back")
        print("0. Exit")
        option = return_option()
        if option == 10:
            j+=10
            if j>stop:
                print("Sorry, no more testUsers")
                j=0
        else:
            if option in range(1,10):
                user.setAttrs(model.userProfile_r[model.userProfile_r['userID'] == testUserList[j+i]]['Rcuisine_Type'].values,model.userProfile_r[model.userProfile_r['userID'] == testUserList[j+i]]['dress_preference'].values[0],model.userProfile_r[model.userProfile_r['userID'] == testUserList[j+i]]['need_Parking'].values[0],model.userProfile_r[model.userProfile_r['userID'] == testUserList[j+i]]['Upayment_accepts'].values[0])
                user.userID=testUserList[j+option]
                break
            else:
                break
    if option in range(1,10):
        options()
    else :            
        dict_testUser[option]()    
    
    
def tellMeMore():
    dict_more = {1:tRestaurant, 2:dressPreference, 3:needParking, 4:pay, 0:exit, 90:options}
    print("""
    What're your preferences:
    1.  Type of Restaurant
    2.  Dress Preference
    3.  Need Parking
    4.  How do you want to pay?
    0.  Exit
    90. Back
    """)
    option = return_option()
    dict_more[option]()

    
def tRestaurant():
    dict_tRestaurant = {1:'Mediterranean', 2:'South_American', 3:'Fast_Food', 4:'Asian', 5:'European', 6:'Middle East', 7:'Breakfast', 8:'Coffee_Shop', 9:'Healthy-Vegetarian', 10:'North_American', 11:'Meat', 12:'Ice_Cream', 13:'Bakery', 14:'Contemporary', 15:'Australian', 16:'Bar', 0:exit, 90:tellMeMore}
    while True:
        print("""
        1.  Mediterranean
        2.  South_American
        3.  Fast_Food
        4.  Asian
        5.  European
        6.  Middle East
        7.  Breakfast
        8.  Coffee_Shop
        9.  Healthy-Vegetarian
        10. North_American
        11. Meat
        12. Ice_Cream
        13. Bakery
        14. Contemporary
        15. Australian
        16. Bar
        0.  Exit
        90. Back
        91. Done
        """)
        option = return_option()
        if option==0 or option==90 or option==91:
            break
        else :
            user.appendAttr("tRestaurant",dict_tRestaurant[option])
    if option==0 or option==90:
        dict_tRestaurant[option]
    elif option==91:
        tellMeMore()
  

def dressPreference():
    dict_dressPreference = {1:'formal',2:'informal', 0:exit, 90:tellMeMore}
    print("""
    1.  Formal
    2.  Informal
    0.  Exit
    90. Back
    """)
    option = return_option()
    if option==0 or option==90:
        dict_pay[option]
    else :
        user.appendAttr("dressPreference",dict_dressPreference[option])
        tellMeMore()

        
def needParking():
    dict_needParking = {1:'yes',2:'no', 0:exit, 90:tellMeMore}
    print("""
    1.  Yes
    2.  No
    0.  Exit
    90. Back
    """)
    option = return_option()
    if option==0 or option==90:
        dict_pay[option]
    else :
        user.appendAttr("parking",dict_needParking[option])
        tellMeMore()

        
def pay():
    dict_pay = {1:'no', 2:'yes', 0:exit, 90:tellMeMore}
    print("""
    1.  Cash
    2.  Credit Card
    0.  Exit
    90. Back
    """)
    option = return_option()
    if option==0 or option==90:
        dict_pay[option]
    else :
        user.appendAttr("pay",dict_pay[option])
        tellMeMore()
        
        
def exit():
    exitClass.numberOfExit=0
    return

print("What do you want to do?")
while exitClass.numberOfExit!=0:
    try:
        options()
    except error:
        print("Pls an option, try again.")