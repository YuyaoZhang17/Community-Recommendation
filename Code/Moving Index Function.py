#!/usr/bin/env python
# coding: utf-8

# In[61]:


import pandas as pd
import numpy as np

data=pd.read_csv("data.csv")

def indexing(cur_zip,new_zip,grades):
    grades["Ranking of Crime"] = grades.pop("Safety")
    grades["Availability of Trains"]=grades.pop("Public Transportation")
    grades["Driving Area"]=grades.pop("Traffic Situation")
    grades["Ranking of Delivery Restaurant"]=grades.pop("Restaurant Delivery")
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
    index["Total"]=sum(index.values())
    
    return index
    
    
        
    
    
    


# In[ ]:




