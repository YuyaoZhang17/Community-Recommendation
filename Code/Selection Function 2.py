# %%
import pandas as pd
import numpy as np
from DistanceRanking import DistRank
from Ranking import ranking
from Distance import distance
import random

# %%
df = pd.read_csv("data.csv", dtype={"Zip Code": str})

#%%
# creating safety ranking dynamically after users select their preference


def safety_consideration(safety, data):
    safety_list = ["Property | Theft", "Violent | Sex Abuse", "Violent | Homicide", "Property | Burglary", "Property | Arson",
                   "Violent | Assault with Dangerous Weapon", "Violent | Robbery"]
    not_selected = list(set(safety_list) ^ set(safety))
    data["Ranking of Crime"] = ranking(
        (data[safety]*0.2).apply(sum, axis=1)+(data[not_selected]*0.1).apply(sum, axis=1))
    return data


def indexing2(zip_code: str, grades_dict, data):
    
    grades=grades_dict

    grades["Ranking of Crime"] = grades.pop("Safety")
    grades["Availability of Trains"] = grades.pop("Public Transportation")
    grades["Driving Area"] = grades.pop("Traffic Situation")
    grades["Ranking of Delivery Restaurant"] = grades.pop(
        "Restaurant Delivery")
    grades["Ranking of Child Care"] = grades.pop("Child Care")
    grades["Ranking of Elementary School"] = grades.pop("Elementary School")
    grades["Ranking of Middle School"] = grades.pop("Middle School")
    grades["Ranking of High School"] = grades.pop("High School")
    grades["Ranking of Hospital"] = grades.pop("Hospital")
    grades["Ranking of Grocery|Freshness"] = grades.pop("Grocery | Freshness")
    grades["Ranking of Grocery|Bargain"] = grades.pop("Grocery | Bargain")
    keys = list(grades)

    zip_data = data[data["Zip Code"] == zip_code]
    grade_sum = sum(grades.values())
    weights = np.array(list(grades.values()))/grade_sum
    zip_ranks = {}
    zip_score = {}
    for i in range(len(keys)):
        zip_ranks[keys[i]] = zip_data[keys[i]].iloc[0]
        zip_score[keys[i]] = weights[i]*zip_ranks[keys[i]]

    zip_score["Total"] = sum(zip_score.values())
    zip_score["Safety"] = zip_score.pop("Ranking of Crime")
    zip_score["Public Transportation"] = zip_score.pop("Availability of Trains")
    zip_score["Traffic Situation"] = zip_score.pop("Driving Area")
    zip_score["Restaurant Delivery"] = zip_score.pop("Ranking of Delivery Restaurant")
    zip_score["Child Care"] = zip_score.pop("Ranking of Child Care")
    zip_score["Elementary School"] = zip_score.pop("Ranking of Elementary School")
    zip_score["Middle School"] = zip_score.pop("Ranking of Middle School")
    zip_score["High School"] = zip_score.pop("Ranking of High School")
    zip_score["Hospital"] = zip_score.pop("Ranking of Hospital")
    zip_score["Grocery | Freshness"] = zip_score.pop("Ranking of Grocery|Freshness")
    zip_score["Grocery | Bargain"] = zip_score.pop("Ranking of Grocery|Bargain")


    grades["Safety"] = grades.pop("Ranking of Crime")
    grades["Public Transportation"] = grades.pop("Availability of Trains")
    grades["Traffic Situation"] = grades.pop("Driving Area")
    grades["Restaurant Delivery"] = grades.pop("Ranking of Delivery Restaurant")
    grades["Child Care"] = grades.pop("Ranking of Child Care")
    grades["Elementary School"] = grades.pop("Ranking of Elementary School")
    grades["Middle School"] = grades.pop("Ranking of Middle School")
    grades["High School"] = grades.pop("Ranking of High School")
    grades["Hospital"] = grades.pop("Ranking of Hospital")
    grades["Grocery | Freshness"] = grades.pop("Ranking of Grocery|Freshness")
    grades["Grocery | Bargain"] = grades.pop("Ranking of Grocery|Bargain")
    
    frame = pd.DataFrame(list(zip_score)).rename(columns={0: "Features"})
    frame["Area Score"]=zip_score.values()
    frame=frame[frame["Area Score"]!=0]



    return frame[frame["Features"]=="Total"]["Area Score"].iloc[0]


def select(user_type, age, income, safety, grades_dict,address=None,data=df):

    grades = grades_dict

    data = safety_consideration(safety, data)
    # if user type in their address, creating traffic situation ranking dynamically
    if address != None:
        data = data.merge(DistRank(address), on=[
                          "Zip Code", "Driving Area", "Cycling Area", "Walking Area"], how="left")

    if age < 55:
        thre = income*0.30
    else:
        thre = income*0.40


    if user_type == "Renter":
        data = data[(data["Rental for Studio"] < thre) | (
            data["Rental for 1 Bed"] < thre) | (data["Rental for 2 Beds"] < thre)].reset_index(drop=True)

        if len(data)>0:

            for i in range(len(data)):
                grades_sub=grades
                data.loc[i,"Area Score"]=indexing2(data["Zip Code"].loc[i],grades_sub,data)
            data=data.sort_values("Area Score",ascending=False)
    if user_type=="Home Buyer":
        data=data[(data["Price for Sale|Studio"]<thre)|(data["Price for Sale|1 Bed"]<thre)|(data["Price for Sale|2 Beds"]<thre)].reset_index(drop=True)

        if len(data)>0:

            for i in range(len(data)):
                grades_sub=grades
                data.loc[i,"Area Score"]=indexing2(data["Zip Code"].loc[i],grades_sub,data)

            data=data.sort_values("Area Score",ascending=False)

    data=data.drop("Unnamed: 0",axis=1)

    return data


#%%
dic = {}

dic["Availability of Bakery"] = 3
dic["Rating of Bakery"] = 4
dic["Price Level of Bakery"] = 2
dic["Availability of Bar"] = 3
dic["Rating of Bar"] = 2
dic["Price Level of Bar"] = 0
dic["Availability of Cafe"] = 3
dic["Rating of Cafe"] = 3
dic["Price Level of Cafe"] = 1
dic["Child Care"] = 4
dic["Elementary School"] = 5
dic["Middle School"] = 3
dic["High School"] = 2
dic["Hospital"] = 3
dic["Availability of Parks"] = 4
dic["Public Transportation"] = 3
dic["Availability of Pharmacy"] = 2
dic["Restaurant Delivery"] = 3
dic["Safety"] = 3
dic["Availability of Sports Facility"] = 1
dic["Traffic Situation"] = 5
dic["Grocery | Freshness"] = 1
dic["Grocery | Bargain"] = 1


safety=["Property | Theft","Violent | Assault with Dangerous Weapon", "Violent | Homicide"]
#%%

select("Home Buyer",45,1000000,["Violent | Homicide","Property | Arson","Violent | Sex Abuse"],dic,address="80 M St SE, Washington, DC 20003",data=df)

#%%


def select_stu(safety,grades_dict,school=None,data=df):
    data=safety_consideration(safety,data)
    address=school
    grades=grades_dict
    data = data.merge(DistRank(address), on=["Zip Code", "Driving Area", "Cycling Area", "Walking Area"], how="left")
    for i in range(len(data)):
        grades_sub=grades
        data.loc[i,"Area Score"]=indexing2(data["Zip Code"].loc[i],grades_sub,data)
    data=data.sort_values("Area Score",ascending=False)

    data=data.drop("Unnamed: 0",axis=1)

    return data
    


#%%

#%%

aa=select_stu(safety,dic,"The Georgetown University",df)
print(aa)
# %%
