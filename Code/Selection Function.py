
#%%
# This file is abandoned
import pandas as pd
import numpy as np
from DistanceRanking import DistRank
from Ranking import ranking
from Distance import distance
import random

#%%
df=pd.read_csv("data.csv",dtype={"Zip Code":str})

# creating safety ranking dynamically after users select their preference
def safety_consideration(safety,data):
    safety_list=["Property | Theft","Violent | Sex Abuse","Violent | Homicide","Property | Burglary","Property | Arson",
    "Violent | Assault with Dangerous Weapon","Violent | Robbery"]
    not_selected = list(set(safety_list) ^ set(safety))
    data["Ranking of Crime"]=ranking((data[safety]*0.2).apply(sum,axis=1)+(data[not_selected]*0.1).apply(sum,axis=1))
    return data

def select(user_type,age,income,interest,grocery,safety,commuting,school=None,address=None,family=["Single"],data=df):

    filters=[]
    
    data=safety_consideration(safety,data)
    # if user type in their address, creating traffic situation ranking dynamically
    if address!=None:
        data=data.merge(DistRank(address),on=["Zip Code","Driving Area","Cycling Area","Walking Area"],how="left")

    if age<55:
        thre=income*0.30
    else:
        thre=income*0.40
        filters.append("Availability of Hospital")
        
    if user_type=="Renter":
        data=data[(data["Rental for Studio"]<thre)|(data["Rental for 1 Bed"]<thre)|(data["Rental for 2 Beds"]<thre)]

        
        if "Kids under 6" in family:
            filters.append("Ranking of Child Care")
            filters.append("Ranking of Elementary School")
            filters.append("Ranking of Crime")
        if "Kids 6 to 12" in family:
            filters.append("Ranking of Elementary School")
            filters.append("Ranking of Middle School")
            filters.append("Ranking of Crime")
        if "Kids 13 to 15" in family:
            filters.append("Ranking of Middle School")
            filters.append("Ranking of High School")
            filters.append("Ranking of Crime")
        if "Kids 16 to 18" in family:
            filters.append("Ranking of High School")
            filters.append("Ranking of Crime")

        

        if commuting=="Car":
            filters.append("Driving Area")
        elif commuting=="Bikes":
            filters.append("Cycling Area")
        elif commuting=="Public Transportation":
            filters.append("Availability of Trains")
        elif commuting=="By Foot":
            filters.append("Walking Area")
            
        if grocery=="Freshness":
            filters.append("Ranking of Grocery|Freshness")
        elif grocery=="Discount":
            filters.append("Ranking of Grocery|Bargain")
        
        if "Outdoor Activities" in interest:
            filters.append("Availability of Parks")
            filters.append("Availability of National Parks")
        if "Sports Facility" in interest:
            filters.append("Availability of Sport Facility")
        if "Bars" in interest:
            filters.append("Ranking of Bar")
        if "Cafe" in interest:
            filters.append("Ranking of Cafe")
        
        data=data.sort_values(by=filters,ascending=False)
            
            
    if user_type=="Home Buyer":
        data=data[(data["Price for Sale|Studio"]<thre)|(data["Price for Sale|1 Bed"]<thre)|(data["Price for Sale|2 Beds"]<thre)]
        
        if "Kids under 6" in family:
            filters.append("Ranking of Child Care")
            filters.append("Ranking of Elementary School")
            filters.append("Ranking of Crime")
        if "Kids 6 to 12" in family:
            filters.append("Ranking of Elementary School")
            filters.append("Ranking of Middle School")
            filters.append("Ranking of Crime")
        if "Kids 13 to 15" in family:
            filters.append("Ranking of Middle School")
            filters.append("Ranking of High School")
            filters.append("Ranking of Crime")
        if "Kids 16 to 18" in family:
            filters.append("Ranking of High School")
            filters.append("Ranking of Crime")


        if commuting=="Car":
            filters.append("Driving Area")
        elif commuting=="Bikes":
            filters.append("Cycling Area")
        elif commuting=="Public Transportation":
            filters.append("Availability of Trains")
        elif commuting=="By Foot":
            filters.append("Walking Area")
            
        if grocery=="Freshness":
            filters.append("Ranking of Grocery|Freshness")
        elif grocery=="Discount":
            filters.append("Ranking of Grocery|Bargain")
        
        if "Outdoor Activities" in interest:
            filters.append("Availability of Parks")
            filters.append("Availability of National Parks")
        if "Sports Facility" in interest:
            filters.append("Availability of Sport Facility")
        if "Bars" in interest:
            filters.append("Ranking of Bar")
        if "Cafe" in interest:
            filters.append("Ranking of Cafe")

        data=data.sort_values(by=filters,ascending=False)

    return data



def select_stu(grocery,interest,safety,school=None,data=df):

    
    filters=[]

    data=safety_consideration(safety,data)
    
    data=pd.concat([data[data["Schools"].str.contains(school)],data[-data["Schools"].str.contains(school)]])

    if grocery=="Freshness":
        filters.append("Ranking of Grocery|Freshness")
    elif grocery=="Discount":
        filters.append("Ranking of Grocery|Bargain")

    if "Outdoor Activities" in interest:
        filters.append("Availability of Parks")
        filters.append("Availability of National Parks")
    if "Sports Facility" in interest:
        filters.append("Availability of Sport Facility")
    if "Bars" in interest:
        filters.append("Ranking of Bar")
    if "Cafe" in interest:
        filters.append("Ranking of Cafe")
    if "Library" in interest:
        filters.append("Availability of Library")

    data=data.sort_values(by=filters,ascending=False)
    
    return data




aa=select("Home Buyer",45,150000,["Parks","Cafe"],"Freshness",["Violent | Homicide","Property | Arson","Violent | Sex Abuse"],"Public Transportation",school=None,family=["Spouse","Kids 6 to 12"],data=df,address="80 M St SE, Washington, DC 20003")

print(aa)

# %%
