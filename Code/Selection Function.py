#!/usr/bin/env python
# coding: utf-8

# In[125]:


import pandas as pd
import numpy as np

data=pd.read_csv("data.csv",dtype={"Zip Code":str})


def select(user_type,age,income,interest,grocery,commuting,school=None,family=["Single"],data=data):
    filters=[]
    
    if age<55:
        thre=income*0.35
    else:
        thre=income*0.45
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
            
        if grocery=="Freshness":
            filters.append("Ranking of Grocery|Freshness")
        elif grocery=="Discount":
            filters.append("Ranking of Grocery|Bargain")
        
        if ("Parks" or "Hiking") in interest:
            filters.append("Availability of Parks")
            filters.append("Availability of National Parks")
        if "Gyms" in interest:
            filters.append("Availability of Sport Facility")
        if "Bars" in interest:
            filters.append("Ranking of Bar")
        if "Cafe" in interest:
            filters.append("Ranking of Cafe")
        
        data=data.sort_values(by=filters,ascending=False)
            
            
    if user_type=="Home Buyer":
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
            
        if grocery=="Freshness":
            filters.append("Ranking of Grocery|Freshness")
        elif grocery=="Discount":
            filters.append("Ranking of Grocery|Bargain")
        
        if ("Parks" or "Hiking") in interest:
            filters.append("Availability of Parks")
            filters.append("Availability of National Parks")
        if "Gyms" in interest:
            filters.append("Availability of Sport Facility")
        if "Bars" in interest:
            filters.append("Ranking of Bar")
        if "Cafe" in interest:
            filters.append("Ranking of Cafe")

        data=data.sort_values(by=filters,ascending=False)
        
    if user_type=="Student":
        data=pd.concat([data[data["Schools"].str.contains(school)],data[-data["Schools"].str.contains(school)]])
        
        if grocery=="Freshness":
            filters.append("Ranking of Grocery|Freshness")
        elif grocery=="Discount":
            filters.append("Ranking of Grocery|Bargain")
            
        if ("Parks" or "Hiking") in interest:
            filters.append("Availability of Parks")
            filters.append("Availability of National Parks")
        if "Gyms" in interest:
            filters.append("Availability of Sport Facility")
        if "Bars" in interest:
            filters.append("Ranking of Bar")
        if "Cafe" in interest:
            filters.append("Ranking of Cafe")
        if "Library" in interest:
            filters.append("Availablity of Library")
            
        data=data.sort_values(by=filters,ascending=False)
    
    return data[0:5]

