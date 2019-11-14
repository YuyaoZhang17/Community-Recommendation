#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import numpy as np

data=pd.read_csv("data.csv")

def indexing(cur_zip,new_zip,grades):
    grades["Ranking of Crime"] = grades.pop("Safety")
    grades["Availability of Trains"]=grades.pop("Public Transportation")
    grades["Driving Area"]=grades.pop("Traffic Situation")
    grades["Ranking of Delivery Restaurant"]=grades.pop("Restaurant Delivery")
    grades["Ranking of Bakery"]=grades.pop("Bakery")
    grades["Ranking of Bar"]=grades.pop("Bar")
    grades["Ranking of Cafe"]=grades.pop("Cafe")
    grades["Ranking of Child Care"]=grades.pop("Child Care")
    grades["Ranking of Elementary School"]=grades.pop("Elementary School")
    grades["Ranking of Middle School"]=grades.pop("Middle School")
    grades["Ranking of High School"]=grades.pop("High School")
    grades["Ranking of Hospital"]=grades.pop("Hospital")
    grades["Availability of Parks"]=grades.pop("Parks")
    grades["Availability of Pharmacy"]=grades.pop("Pharmacy")
    grades["Availability of Sport Facility"]=grades.pop("Sport Facility")
    keys=list(grades)
    cur_data=data[data["Zip Code"]==cur_zip]
    new_data=data[data["Zip Code"]==new_zip]
    grade_sum=sum(grades.values())
    weights=np.array(list(grades.values()))/grade_sum
    cur_ranks={}
    new_ranks={}
    cur_score={}
    new_score={}
    index={}
    for i in range(len(keys)):
        cur_ranks[keys[i]]=cur_data[keys[i]].iloc[0]
        new_ranks[keys[i]]=new_data[keys[i]].iloc[0]
        cur_score[keys[i]]=weights[i]*cur_ranks[keys[i]]
        new_score[keys[i]]=weights[i]*new_ranks[keys[i]]
        index[keys[i]]=(new_score[keys[i]]-cur_score[keys[i]])/cur_score[keys[i]]
    index["Safety"]=index.pop("Ranking of Crime")
    index["Public Transportation"]=index.pop("Availability of Trains")
    index["Traffic Situation"]=index.pop("Driving Area")
    index["Restaurant Delivery"]=index.pop("Ranking of Delivery Restaurant")
    index["Bakery"]=index.pop("Ranking of Bakery")
    index["Bar"]=index.pop("Ranking of Bar")
    index["Cafe"]=index.pop("Ranking of Cafe")
    index["Child Care"]=index.pop("Ranking of Child Care")
    index["Elementary School"]=index.pop("Ranking of Elementary School")
    index["Middle School"]=index.pop("Ranking of Middle School")
    index["High School"]=index.pop("Ranking of High School")
    index["Hospital"]=index.pop("Ranking of Hospital")
    index["Parks"]=index.pop("Availability of Parks")
    index["Pharmacy"]=index.pop("Availability of Pharmacy")
    index["Sport Facility"]=grades.pop("Availability of Sport Facility")
    index["Total"]=sum(index.values())
    
    return index
    
    
        
    
    
    


# In[ ]:




